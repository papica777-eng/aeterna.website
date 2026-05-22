/**
 * BROWSER POOL - GhostShield Protected Browser Instances
 * Version: 1.0.0-SINGULARITY
 * 
 * Features:
 * - 50ms TLS rotation per browser instance
 * - GhostShield integration for fingerprint polymorphism
 * - Pool management with auto-scaling
 */

import { GhostShield } from './GhostShield.js';
import { SharedMemoryV2, getSharedMemory } from './SharedMemoryV2.js';

export interface GhostBrowserInstance {
    id: string;
    browserType: 'chromium' | 'firefox' | 'webkit';
    currentFingerprintId: string;
    lastTlsRotation: number;
    requestCount: number;
    isActive: boolean;
    createdAt: number;
}

export interface BrowserPoolConfig {
    maxBrowsers: number;
    tlsRotationIntervalMs: number;
    idleTimeoutMs: number;
    ghostShieldEnabled: boolean;
}

interface BrowserPoolStats {
    totalBrowsers: number;
    activeBrowsers: number;
    totalRequests: number;
    totalRotations: number;
    avgRotationLatencyMs: number;
}

const DEFAULT_CONFIG: BrowserPoolConfig = {
    maxBrowsers: 10,
    tlsRotationIntervalMs: 50,
    idleTimeoutMs: 300000,
    ghostShieldEnabled: true
};

export class BrowserPool {
    private config: BrowserPoolConfig;
    private instances: Map<string, GhostBrowserInstance> = new Map();
    private ghostShields: Map<string, GhostShield> = new Map();
    private rotationIntervals: Map<string, ReturnType<typeof setInterval>> = new Map();
    private sharedMemory: SharedMemoryV2;
    private isInitialized: boolean = false;
    private stats: BrowserPoolStats;

    constructor(config: Partial<BrowserPoolConfig> = {}) {
        this.config = { ...DEFAULT_CONFIG, ...config };
        this.sharedMemory = getSharedMemory('browser_pool');
        this.stats = {
            totalBrowsers: 0,
            activeBrowsers: 0,
            totalRequests: 0,
            totalRotations: 0,
            avgRotationLatencyMs: 0
        };
        this.initializeSharedMemory();
    }

    private initializeSharedMemory(): void {
        this.sharedMemory.createSegment('browser_pool_state', {
            instances: [],
            stats: this.stats,
            lastUpdate: Date.now()
        });
    }

    public async initialize(): Promise<void> {
        if (this.isInitialized) {
            return;
        }

        this.isInitialized = true;
    }

    public async acquireBrowser(
        preferredType: 'chromium' | 'firefox' | 'webkit' = 'chromium'
    ): Promise<GhostBrowserInstance | null> {
        if (this.instances.size >= this.config.maxBrowsers) {
            for (const [, instance] of this.instances) {
                if (!instance.isActive) {
                    instance.isActive = true;
                    instance.browserType = preferredType;
                    await this.syncToSharedMemory();
                    return instance;
                }
            }
            return null;
        }

        const instance = await this.createBrowserInstance(preferredType);
        return instance;
    }

    private async createBrowserInstance(
        browserType: 'chromium' | 'firefox' | 'webkit'
    ): Promise<GhostBrowserInstance> {
        const instanceId = this.generateUUID();
        
        const ghostShield = new GhostShield({
            rotationIntervalMs: this.config.tlsRotationIntervalMs,
            sharedMemorySegmentId: `ghost_browser_${instanceId}`,
            fingerprintPoolSize: 50
        });
        
        await ghostShield.initialize();
        const signature = ghostShield.getCurrentSignature();
        
        const instance: GhostBrowserInstance = {
            id: instanceId,
            browserType,
            currentFingerprintId: signature.id,
            lastTlsRotation: Date.now(),
            requestCount: 0,
            isActive: true,
            createdAt: Date.now()
        };

        this.instances.set(instanceId, instance);
        this.ghostShields.set(instanceId, ghostShield);
        
        if (this.config.ghostShieldEnabled) {
            this.startTlsRotation(instanceId);
        }

        this.stats.totalBrowsers++;
        this.stats.activeBrowsers++;
        
        await this.syncToSharedMemory();
        return instance;
    }

    private startTlsRotation(instanceId: string): void {
        const interval = setInterval(async () => {
            await this.rotateTls(instanceId);
        }, this.config.tlsRotationIntervalMs);
        
        this.rotationIntervals.set(instanceId, interval);
    }

    private async rotateTls(instanceId: string): Promise<void> {
        const startTime = Date.now();
        const instance = this.instances.get(instanceId);
        const shield = this.ghostShields.get(instanceId);
        
        if (!instance || !shield) {
            return;
        }

        const signature = shield.getCurrentSignature();
        instance.currentFingerprintId = signature.id;
        instance.lastTlsRotation = Date.now();
        
        this.stats.totalRotations++;
        const latency = Date.now() - startTime;
        this.stats.avgRotationLatencyMs = 
            (this.stats.avgRotationLatencyMs * (this.stats.totalRotations - 1) + latency) / 
            this.stats.totalRotations;
    }

    public async releaseBrowser(instanceId: string): Promise<boolean> {
        const instance = this.instances.get(instanceId);
        if (!instance) {
            return false;
        }

        instance.isActive = false;
        this.stats.activeBrowsers--;
        await this.syncToSharedMemory();
        return true;
    }

    public async destroyBrowser(instanceId: string): Promise<boolean> {
        const instance = this.instances.get(instanceId);
        const shield = this.ghostShields.get(instanceId);
        const interval = this.rotationIntervals.get(instanceId);
        
        if (!instance) {
            return false;
        }

        if (interval) {
            clearInterval(interval);
            this.rotationIntervals.delete(instanceId);
        }
        
        if (shield) {
            shield.destroy();
            this.ghostShields.delete(instanceId);
        }
        
        this.instances.delete(instanceId);
        this.stats.totalBrowsers--;
        if (instance.isActive) {
            this.stats.activeBrowsers--;
        }
        
        await this.syncToSharedMemory();
        return true;
    }

    private async syncToSharedMemory(): Promise<void> {
        const acquired = await this.sharedMemory.acquireLock('browser_pool_state');
        if (acquired) {
            const instanceArray = Array.from(this.instances.values());
            this.sharedMemory.write('browser_pool_state', {
                instances: instanceArray,
                stats: this.stats,
                lastUpdate: Date.now()
            });
            this.sharedMemory.releaseLock('browser_pool_state');
        }
    }

    public getStats(): BrowserPoolStats {
        return { ...this.stats };
    }

    public async shutdown(): Promise<void> {
        for (const interval of this.rotationIntervals.values()) {
            clearInterval(interval);
        }
        this.rotationIntervals.clear();
        
        for (const shield of this.ghostShields.values()) {
            shield.destroy();
        }
        this.ghostShields.clear();
        this.instances.clear();
        this.isInitialized = false;
    }

    private generateUUID(): string {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
            const r = (Math.random() * 16) | 0;
            const v = c === 'x' ? r : (r & 0x3) | 0x8;
            return v.toString(16);
        });
    }
}

let globalPool: BrowserPool | null = null;

export function getBrowserPool(config?: Partial<BrowserPoolConfig>): BrowserPool {
    if (!globalPool) {
        globalPool = new BrowserPool(config);
    }
    return globalPool;
}

export async function resetBrowserPool(): Promise<void> {
    if (globalPool) {
        await globalPool.shutdown();
        globalPool = null;
    }
}
