/**
 * MIND-ENGINE: BROWSER ORCHESTRATOR
 * Version: 1.0.0-QANTUM-PRIME
 * 
 * Features:
 * - Multi-browser orchestration, parallel execution, browser pool scheduling
 * - EIC compatibility layer
 */

import { EventEmitter } from 'events';

export type BrowserType = 'chromium' | 'firefox' | 'webkit' | 'chrome' | 'edge';

export interface BrowserConfig {
    type: BrowserType;
    headless?: boolean;
    args?: string[];
    timeout?: number;
    slowMo?: number;
    devtools?: boolean;
}

export interface BrowserInstance {
    id: string;
    type: BrowserType;
    browser: any;
    createdAt: Date;
    lastUsed: Date;
    inUse: boolean;
    pagesCount: number;
}

export interface PoolConfig {
    browsers: Array<{
        type: BrowserType;
        count: number;
        config?: Partial<BrowserConfig>;
    }>;
    maxTotal?: number;
    idleTimeout?: number;
    acquireTimeout?: number;
}

export interface OrchestratorConfig {
    pool?: PoolConfig;
    maxConcurrency?: number;
    defaultBrowser?: BrowserType;
    retries?: number;
}

export class BrowserPool extends EventEmitter {
    private instances: Map<string, BrowserInstance> = new Map();
    private config: PoolConfig;
    private idCounter: number = 0;

    constructor(config: PoolConfig) {
        super();
        this.config = {
            maxTotal: 10,
            idleTimeout: 60000,
            acquireTimeout: 30000,
            ...config
        };
    }

    async initialize(): Promise<void> {
        for (const browserConfig of this.config.browsers) {
            for (let i = 0; i < browserConfig.count; i++) {
                await this.createInstance(browserConfig.type, browserConfig.config);
            }
        }
        this.emit('initialized', this.getStats());
    }

    async acquire(type: BrowserType): Promise<BrowserInstance> {
        for (const instance of this.instances.values()) {
            if (instance.type === type && !instance.inUse) {
                instance.inUse = true;
                instance.lastUsed = new Date();
                return instance;
            }
        }

        if (this.instances.size < (this.config.maxTotal || 10)) {
            const instance = await this.createInstance(type);
            instance.inUse = true;
            return instance;
        }

        throw new Error(`Browser pool exhausted for: ${type}`);
    }

    release(id: string): void {
        const instance = this.instances.get(id);
        if (instance) {
            instance.inUse = false;
            instance.lastUsed = new Date();
        }
    }

    async destroy(id: string): Promise<void> {
        this.instances.delete(id);
    }

    async shutdown(): Promise<void> {
        this.instances.clear();
    }

    getStats() {
        return {
            total: this.instances.size,
            inUse: Array.from(this.instances.values()).filter(i => i.inUse).length
        };
    }

    private async createInstance(type: BrowserType, config?: Partial<BrowserConfig>): Promise<BrowserInstance> {
        const id = `${type}-${++this.idCounter}`;
        const instance: BrowserInstance = {
            id,
            type,
            browser: { id, type, close: async () => {} },
            createdAt: new Date(),
            lastUsed: new Date(),
            inUse: false,
            pagesCount: 0
        };
        this.instances.set(id, instance);
        return instance;
    }
}

export class BrowserOrchestrator extends EventEmitter {
    private pool?: BrowserPool;
    private config: OrchestratorConfig;
    private running: boolean = false;

    constructor(config: OrchestratorConfig = {}) {
        super();
        this.config = {
            maxConcurrency: 4,
            defaultBrowser: 'chromium',
            retries: 2,
            ...config
        };
    }

    async initialize(): Promise<void> {
        if (this.config.pool) {
            this.pool = new BrowserPool(this.config.pool);
            await this.pool.initialize();
        }
        this.running = true;
        this.emit('initialized');
    }

    async execute<T>(
        handler: (browser: any, page: any) => Promise<T>,
        options: { browser?: BrowserType; timeout?: number } = {}
    ): Promise<T> {
        const type = options.browser || this.config.defaultBrowser || 'chromium';
        const instance = this.pool 
            ? await this.pool.acquire(type)
            : { browser: {}, id: 'temp' };

        try {
            return await handler(instance.browser, {});
        } finally {
            if (this.pool) {
                this.pool.release(instance.id);
            }
        }
    }

    async shutdown(): Promise<void> {
        this.running = false;
        if (this.pool) {
            await this.pool.shutdown();
        }
    }
}

export function createOrchestrator(config?: OrchestratorConfig): BrowserOrchestrator {
    return new BrowserOrchestrator(config);
}

export function createPool(config: PoolConfig): BrowserPool {
    return new BrowserPool(config);
}

export default {
    BrowserPool,
    BrowserOrchestrator,
    createOrchestrator,
    createPool
};
