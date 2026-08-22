/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * QANTUM PRIME - MAIN JAVASCRIPT
 * v27.1.0 IMMORTAL Edition
 * ═══════════════════════════════════════════════════════════════════════════════
 */

'use strict';

// ═══════════════════════════════════════════════════════════════════════════════
// CONFIGURATION
// ═══════════════════════════════════════════════════════════════════════════════

const CONFIG = {
    totalLines: 752312,
    totalTests: 6685,
    totalFiles: 1550,
    modules: 6,
    failover: 0.08,
    regions: 5,
    version: 'v30.6.4-OMEGA-SUPREME',
    taglines: [
        '"DEATH IS NOT AN OPTION" - Ghost Protocol v2 Active',
        '"THE TESTS THAT REFUSE TO DIE" - Fatality Engine Armed',
        '"QUANTUM IMMORTALITY ACHIEVED" - Chronos-Paradox Online',
        '"SWARM INTELLIGENCE DISTRIBUTED" - 5 Regions Active',
        '"PROPHECY MODE ENABLED" - Oracle Analytics Ready',
        '"FORTRESS SHIELDS MAXIMUM" - Security Core Armed'
    ],
    // Telemetry configuration
    telemetry: {
        wsUrl: 'ws://192.168.0.6:8888',
        reconnectInterval: 5000,
        maxRetries: 3
    }
};

// ═══════════════════════════════════════════════════════════════════════════════
// TELEMETRY - REAL-TIME / SIMULATION MODE
// ═══════════════════════════════════════════════════════════════════════════════

class QAntumTelemetry {
    constructor() {
        this.ws = null;
        this.isLive = false;
        this.retries = 0;
        this.data = this.getSimulatedData();
        this.listeners = [];
    }
    
    connect() {
        try {
            this.ws = new WebSocket(CONFIG.telemetry.wsUrl);
            
            this.ws.onopen = () => {
                console.log('%c⚡ LIVE MODE ACTIVATED - Connected to QAntum Neural Hub', 'color: #10b981; font-weight: bold;');
                this.isLive = true;
                this.retries = 0;
                this.updateModeIndicator(true);
            };
            
            this.ws.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    this.data = data;
                    this.notifyListeners(data);
                } catch (e) {
                    console.warn('Invalid telemetry data:', e);
                }
            };
            
            this.ws.onclose = () => {
                this.isLive = false;
                this.updateModeIndicator(false);
                this.scheduleReconnect();
            };
            
            this.ws.onerror = () => {
                this.isLive = false;
                this.updateModeIndicator(false);
            };
        } catch (e) {
            console.log('%c🎮 SIMULATION MODE - QAntum Neural Hub offline', 'color: #f59e0b;');
            this.isLive = false;
            this.updateModeIndicator(false);
            this.startSimulation();
        }
    }
    
    scheduleReconnect() {
        if (this.retries < CONFIG.telemetry.maxRetries) {
            this.retries++;
            console.log(`%c🔄 Reconnecting to Neural Hub (${this.retries}/${CONFIG.telemetry.maxRetries})...`, 'color: #06b6d4;');
            setTimeout(() => this.connect(), CONFIG.telemetry.reconnectInterval);
        } else {
            console.log('%c🎮 SIMULATION MODE ACTIVE - Using generated data', 'color: #f59e0b;');
            this.startSimulation();
        }
    }
    
    updateModeIndicator(isLive) {
        const indicator = document.getElementById('mode-indicator');
        const statusDot = document.querySelector('.terminal-status .status-dot');
        const statusText = document.querySelector('.terminal-status span:last-child');
        
        if (indicator) {
            indicator.textContent = isLive ? '🟢 LIVE' : '🟡 SIMULATION';
            indicator.className = isLive ? 'mode-live' : 'mode-simulation';
        }
        
        if (statusDot) {
            statusDot.style.background = isLive ? '#10b981' : '#f59e0b';
            statusDot.style.boxShadow = isLive ? '0 0 10px #10b981' : '0 0 10px #f59e0b';
        }
        
        if (statusText) {
            statusText.textContent = isLive ? 'LIVE' : 'SIMULATION';
        }
    }
    
    getSimulatedData() {
        return {
            lines: CONFIG.totalLines + Math.floor(Math.random() * 100),
            testsRunning: Math.floor(Math.random() * 1000) + 500,
            passRate: 97 + Math.random() * 2.9,
            activeWorkers: Math.floor(Math.random() * 500) + 800,
            ghostBypasses: Math.floor(Math.random() * 100) + 50,
            healedSelectors: Math.floor(Math.random() * 50) + 10,
            regions: {
                'us-east': { workers: 312, status: 'active' },
                'eu-west': { workers: 256, status: 'active' },
                'ap-south': { workers: 198, status: 'active' },
                'us-west': { workers: 287, status: 'active' },
                'eu-central': { workers: 241, status: 'active' }
            },
            timestamp: Date.now()
        };
    }
    
    startSimulation() {
        setInterval(() => {
            this.data = this.getSimulatedData();
            this.notifyListeners(this.data);
        }, 3000);
    }
    
    onData(callback) {
        this.listeners.push(callback);
    }
    
    notifyListeners(data) {
        this.listeners.forEach(cb => cb(data));
    }
    
    getData() {
        return this.data;
    }
}

// Global telemetry instance
const telemetry = new QAntumTelemetry();

// ═══════════════════════════════════════════════════════════════════════════════
// PARTICLES GENERATOR
// ═══════════════════════════════════════════════════════════════════════════════

function initParticles() {
    const container = document.querySelector('.particles');
    if (!container) return;
    
    const particleCount = 30;
    container.innerHTML = '';
    
    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        container.appendChild(particle);
    }
}

// ═══════════════════════════════════════════════════════════════════════════════
// NAVIGATION
// ═══════════════════════════════════════════════════════════════════════════════

function initNavigation() {
    const nav = document.querySelector('nav');
    const mobileMenuBtn = document.querySelector('.mobile-menu');
    const navLinks = document.querySelector('.nav-links');
    
    // Scroll effect
    let lastScroll = 0;
    window.addEventListener('scroll', () => {
        const currentScroll = window.scrollY;
        
        if (currentScroll > 50) {
            nav.classList.add('scrolled');
        } else {
            nav.classList.remove('scrolled');
        }
        
        lastScroll = currentScroll;
    });
    
    // Mobile menu toggle
    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            mobileMenuBtn.innerHTML = navLinks.classList.contains('active') ? '✕' : '☰';
        });
    }
    
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
                
                // Close mobile menu
                if (navLinks && navLinks.classList.contains('active')) {
                    navLinks.classList.remove('active');
                    mobileMenuBtn.innerHTML = '☰';
                }
            }
        });
    });
}

// ═══════════════════════════════════════════════════════════════════════════════
// TYPEWRITER EFFECT
// ═══════════════════════════════════════════════════════════════════════════════

function initTypewriter() {
    const element = document.querySelector('.hero-tagline');
    if (!element) return;
    
    let currentIndex = 0;
    let currentText = '';
    let isDeleting = false;
    let typeSpeed = 50;
    
    function type() {
        const fullText = CONFIG.taglines[currentIndex];
        
        if (isDeleting) {
            currentText = fullText.substring(0, currentText.length - 1);
            typeSpeed = 25;
        } else {
            currentText = fullText.substring(0, currentText.length + 1);
            typeSpeed = 50;
        }
        
        element.textContent = currentText;
        
        if (!isDeleting && currentText === fullText) {
            // Pause at end
            typeSpeed = 3000;
            isDeleting = true;
        } else if (isDeleting && currentText === '') {
            isDeleting = false;
            currentIndex = (currentIndex + 1) % CONFIG.taglines.length;
            typeSpeed = 500;
        }
        
        setTimeout(type, typeSpeed);
    }
    
    // Start typing
    setTimeout(type, 1000);
}

// ═══════════════════════════════════════════════════════════════════════════════
// COUNTER ANIMATION
// ═══════════════════════════════════════════════════════════════════════════════

function animateCounter(element, target, suffix = '', duration = 2000) {
    const start = 0;
    const startTime = performance.now();
    
    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        // Easing function (ease-out-expo)
        const easeProgress = 1 - Math.pow(2, -10 * progress);
        const current = Math.floor(start + (target - start) * easeProgress);
        
        if (target >= 1000000) {
            element.textContent = (current / 1000000).toFixed(1) + 'M' + suffix;
        } else if (target >= 1000) {
            element.textContent = Math.floor(current / 1000) + 'k' + suffix;
        } else if (target < 1) {
            element.textContent = current.toFixed(2) + suffix;
        } else {
            element.textContent = current.toLocaleString() + suffix;
        }
        
        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }
    
    requestAnimationFrame(update);
}

function initCounters() {
    const counters = document.querySelectorAll('[data-count]');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !entry.target.dataset.counted) {
                const target = parseFloat(entry.target.dataset.count);
                const suffix = entry.target.dataset.suffix || '';
                animateCounter(entry.target, target, suffix);
                entry.target.dataset.counted = 'true';
            }
        });
    }, { threshold: 0.5 });
    
    counters.forEach(counter => observer.observe(counter));
}

// ═══════════════════════════════════════════════════════════════════════════════
// COPY FUNCTIONS
// ═══════════════════════════════════════════════════════════════════════════════

function copyToClipboard(text, button) {
    navigator.clipboard.writeText(text).then(() => {
        const originalText = button.innerHTML;
        button.innerHTML = '✓';
        button.style.color = '#10b981';
        
        setTimeout(() => {
            button.innerHTML = originalText;
            button.style.color = '';
        }, 2000);
    }).catch(err => {
        console.error('Copy failed:', err);
    });
}

function initCopyButtons() {
    // Install command copy
    const installCopy = document.querySelector('.install-box .copy-btn');
    if (installCopy) {
        installCopy.addEventListener('click', function() {
            copyToClipboard('npm install qantum-prime', this);
        });
    }
    
    // Code block copy
    document.querySelectorAll('.copy-code').forEach(btn => {
        btn.addEventListener('click', function() {
            const codeBlock = this.closest('.code-block');
            const code = codeBlock.querySelector('.code-content').textContent;
            copyToClipboard(code, this);
        });
    });
}

// ═══════════════════════════════════════════════════════════════════════════════
// REVEAL ON SCROLL
// ═══════════════════════════════════════════════════════════════════════════════

function initRevealOnScroll() {
    const reveals = document.querySelectorAll('.reveal, .reveal-left, .reveal-right, .reveal-scale');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });
    
    reveals.forEach(el => observer.observe(el));
}

// ═══════════════════════════════════════════════════════════════════════════════
// FEATURE CARDS INTERACTION
// ═══════════════════════════════════════════════════════════════════════════════

function initFeatureCards() {
    const cards = document.querySelectorAll('.feature-card');
    
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-12px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = '';
        });
    });
}

// ═══════════════════════════════════════════════════════════════════════════════
// ARCHITECTURE LAYERS INTERACTION
// ═══════════════════════════════════════════════════════════════════════════════

function initArchLayers() {
    const layers = document.querySelectorAll('.arch-layer');
    
    layers.forEach((layer, index) => {
        layer.style.animationDelay = `${index * 0.1}s`;
        layer.classList.add('reveal');
    });
}

// ═══════════════════════════════════════════════════════════════════════════════
// HERO STATS ANIMATION
// ═══════════════════════════════════════════════════════════════════════════════

function initHeroStats() {
    const stats = [
        { selector: '#lines-count', value: 715861, suffix: '+' },
        { selector: '#failover-count', value: 0.08, suffix: 'ms' },
        { selector: '#modules-count', value: 6, suffix: '' },
        { selector: '#regions-count', value: 5, suffix: '' }
    ];
    
    stats.forEach(stat => {
        const el = document.querySelector(stat.selector);
        if (el) {
            el.dataset.count = stat.value;
            el.dataset.suffix = stat.suffix;
        }
    });
}

// ═══════════════════════════════════════════════════════════════════════════════
// KEYBOARD SHORTCUTS
// ═══════════════════════════════════════════════════════════════════════════════

function initKeyboardShortcuts() {
    document.addEventListener('keydown', (e) => {
        // Ctrl/Cmd + K = Focus search (if exists)
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            const searchInput = document.querySelector('input[type="search"]');
            if (searchInput) searchInput.focus();
        }
        
        // Escape = Close modals
        if (e.key === 'Escape') {
            const modal = document.querySelector('.modal.active');
            if (modal) modal.classList.remove('active');
        }
    });
}

// ═══════════════════════════════════════════════════════════════════════════════
// PERFORMANCE OPTIMIZATION
// ═══════════════════════════════════════════════════════════════════════════════

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// ═══════════════════════════════════════════════════════════════════════════════
// LAZY LOADING
// ═══════════════════════════════════════════════════════════════════════════════

function initLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
}

// ═══════════════════════════════════════════════════════════════════════════════
// DARK/LIGHT MODE (Future Feature)
// ═══════════════════════════════════════════════════════════════════════════════

function initThemeToggle() {
    const toggle = document.querySelector('.theme-toggle');
    if (!toggle) return;
    
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const saved = localStorage.getItem('theme');
    
    if (saved) {
        document.documentElement.setAttribute('data-theme', saved);
    } else if (prefersDark) {
        document.documentElement.setAttribute('data-theme', 'dark');
    }
    
    toggle.addEventListener('click', () => {
        const current = document.documentElement.getAttribute('data-theme');
        const next = current === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', next);
        localStorage.setItem('theme', next);
    });
}

// ═══════════════════════════════════════════════════════════════════════════════
// CONSOLE EASTER EGG
// ═══════════════════════════════════════════════════════════════════════════════

function initConsoleEasterEgg() {
    console.log(`
%c╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   ██████╗  █████╗ ███╗   ██╗████████╗██╗   ██╗███╗   ███╗    ║
║  ██╔═══██╗██╔══██╗████╗  ██║╚══██╔══╝██║   ██║████╗ ████║    ║
║  ██║   ██║███████║██╔██╗ ██║   ██║   ██║   ██║██╔████╔██║    ║
║  ██║▄▄ ██║██╔══██║██║╚██╗██║   ██║   ██║   ██║██║╚██╔╝██║    ║
║  ╚██████╔╝██║  ██║██║ ╚████║   ██║   ╚██████╔╝██║ ╚═╝ ██║    ║
║   ╚══▀▀═╝ ╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝    ╚═════╝ ╚═╝     ╚═╝    ║
║                                                               ║
║              P R I M E   v27.1.0-IMMORTAL                     ║
║                                                               ║
║     "The Testing Framework That Refuses to Die"               ║
║                                                               ║
║     📊 ${CONFIG.totalLines.toLocaleString()} Lines of Code                            ║
║     🧩 ${CONFIG.modules} Core Modules                                       ║
║     ⚡ ${CONFIG.failover}ms Failover                                        ║
║     🌍 ${CONFIG.regions} Global Regions                                      ║
║                                                               ║
║     👻 Ghost Protocol v2 - ACTIVE                             ║
║     🎯 Fatality Engine - ARMED                                ║
║     🔮 Oracle Analytics - READY                               ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
`, 'color: #6366f1; font-family: monospace; font-size: 10px;');

    console.log('%c🔒 Security Warning: This is a browser feature intended for developers.', 'color: #ef4444; font-weight: bold;');
    console.log('%c🚀 Want to contribute? Visit: https://github.com/papica777-eng/QAntumPage', 'color: #10b981;');
}

// ═══════════════════════════════════════════════════════════════════════════════
// INITIALIZATION
// ═══════════════════════════════════════════════════════════════════════════════

function initApp() {
    try { initParticles(); } catch(e){}
    try { initNavigation(); } catch(e){}
    try { initTypewriter(); } catch(e){}
    try { initHeroStats(); } catch(e){}
    try { initCounters(); } catch(e){}
    try { initCopyButtons(); } catch(e){}
    try { initRevealOnScroll(); } catch(e){}
    try { initFeatureCards(); } catch(e){}
    try { initArchLayers(); } catch(e){}
    try { initLazyLoading(); } catch(e){}
    try { initKeyboardShortcuts(); } catch(e){}
    try { initThemeToggle(); } catch(e){}
    try { initConsoleEasterEgg(); } catch(e){}
    try { initFeatureButtons(); } catch(e){}
    try { telemetry.connect(); } catch(e){}
    try {
        telemetry.onData((data) => {
            updateDashboardStats(data);
        });
    } catch(e){}
    console.log(`%c⚡ QAntum Prime ${CONFIG.version} initialized`, 'color: #10b981; font-weight: bold;');
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initApp);
} else {
    initApp();
}

// ═══════════════════════════════════════════════════════════════════════════════
// INTERACTIVE FEATURE BUTTONS & TERMINAL ENGINE
// ═══════════════════════════════════════════════════════════════════════════════

const FEATURE_DATA = {
    ghost: {
        title: 'Ghost Protocol v2',
        stats: [
            { label: 'Detection Bypass', value: '100%' },
            { label: 'Protected Sites', value: '2,847' },
            { label: 'Bot Challenges', value: '0 Failed' }
        ],
        visual: 'ghost'
    },
    heal: {
        title: 'Self-Healing Engine',
        stats: [
            { label: 'Auto-Repair Rate', value: '97%' },
            { label: 'Strategies Active', value: '15' },
            { label: 'Selectors Fixed', value: '12,483' }
        ],
        visual: 'heal'
    },
    swarm: {
        title: 'Global Swarm Network',
        stats: [
            { label: 'Active Nodes', value: '1,247' },
            { label: 'Regions', value: '5 Continents' },
            { label: 'Throughput', value: '40x Faster' }
        ],
        visual: 'swarm'
    },
    oracle: {
        title: 'The Oracle AI',
        stats: [
            { label: 'Tests Generated', value: '12,847' },
            { label: 'Coverage', value: '94.7%' },
            { label: 'Scan Time', value: '< 30sec' }
        ],
        visual: 'oracle'
    },
    chronos: {
        title: 'Chronos Engine',
        stats: [
            { label: 'Prediction Accuracy', value: '89%' },
            { label: 'Time Zones', value: '24' },
            { label: 'Failures Prevented', value: '847' }
        ],
        visual: 'chronos'
    },
    fortress: {
        title: 'Fortress Security',
        stats: [
            { label: 'Vulnerabilities Found', value: '2,391' },
            { label: 'SQLi Blocked', value: '100%' },
            { label: 'XSS Protected', value: '100%' }
        ],
        visual: 'fortress'
    }
};

let terminalLogTimer = null;
let terminalHeartbeatTimer = null;

function getTimestamp() {
    const now = new Date();
    return now.toTimeString().split(' ')[0];
}

function appendTerminalLog(htmlLine) {
    const terminal = document.getElementById('terminalOutput');
    if (!terminal) return;
    
    const row = document.createElement('div');
    row.className = 'terminal-line py-0.5 animate-fadeIn font-mono text-xs';
    row.innerHTML = `<span class="text-gray-500 select-none mr-1.5">[${getTimestamp()}]</span> ${htmlLine}`;
    terminal.appendChild(row);
    
    terminal.scrollTop = terminal.scrollHeight;
}

const FEATURE_SCRIPTS = {
    ghost: [
        '<span class="text-cyan-400 font-bold">👻 [GHOST_PROTOCOL]</span> Initializing stealth testing session for target <span class="text-indigo-300">https://app.enterprise.io</span>',
        '<span class="text-purple-400 font-bold">⚡ [JA4_SPOOF]</span> Negotiating TLS ClientHello: cipher suites [0x1301, 0x1302, 0x1303] (Chrome 128 / Win64)',
        '<span class="text-yellow-400 font-bold">🛡️ [CHALLENGE]</span> Cloudflare Turnstile token validation challenge detected',
        '<span class="text-cyan-300 font-bold">🔮 [BEZIER]</span> Generating natural human-curved mouse trajectory (micro-jitter: 0.02ms)',
        '<span class="text-emerald-400 font-bold">✅ [BYPASSED]</span> Bot check cleared in 18ms. HTTP 200 OK authenticated session established.'
    ],
    heal: [
        '<span class="text-purple-400 font-bold">🔮 [SELF_HEAL]</span> Executing E2E Playwright step: <code class="text-pink-300">click("#submit-checkout-btn")</code>',
        '<span class="text-red-400 font-bold">⚠️ [DOM_MUTATION]</span> Target selector <code class="text-red-300">#submit-checkout-btn</code> not found (DOM 404 fault)',
        '<span class="text-cyan-400 font-bold">🧠 [CATUSKOTI_AST]</span> Initiating multi-layer proximity AST search across 184 DOM subtrees...',
        '<span class="text-yellow-300 font-bold">🎯 [LOCATOR_MATCH]</span> Discovered candidate: <code class="text-emerald-300">button[data-qa="complete-order"]</code> (Confidence: 99.8%)',
        '<span class="text-emerald-400 font-bold">🩹 [HEALED]</span> Selector repaired in-memory without test disruption. Step passed in 4ms!'
    ],
    swarm: [
        '<span class="text-emerald-400 font-bold">🐝 [SWARM_EXEC]</span> Distributing test runners across 5 global edge regions (1,247 active workers)',
        '<span class="text-gray-300 font-bold">🌍 [REGIONS]</span> Frankfurt (256), Virginia (312), Tokyo (198), Oregon (287), São Paulo (241)',
        '<span class="text-cyan-400 font-bold">⚡ [DISPATCH]</span> Parallelizing 6,685 full integration test suites via zero-copy WebSockets',
        '<span class="text-indigo-300 font-bold">📊 [THROUGHPUT]</span> 450 concurrent suites/sec | Zero mutex locks | Zero flaky timeouts',
        '<span class="text-emerald-400 font-bold">🚀 [BENCHMARK]</span> 6,685 tests completed in 14.2s. 40.2x speedup compared to standard Selenium.'
    ],
    oracle: [
        '<span class="text-indigo-400 font-bold">🔍 [ORACLE_AI]</span> Autonomous crawler scanning application sitemap and GraphQL schema...',
        '<span class="text-cyan-300 font-bold">📄 [DISCOVERY]</span> Mapped 847 routes, 12,483 state transitions, 412 API endpoints',
        '<span class="text-purple-300 font-bold">✍️ [AUTO_GEN]</span> Synthesizing 500+ unit, integration and visual regression test suites in TypeScript',
        '<span class="text-yellow-300 font-bold">📈 [COVERAGE]</span> Total test coverage increased from 42% to 94.7% with zero human manual test writing',
        '<span class="text-emerald-400 font-bold">✅ [ORACLE_SYNC]</span> Automated test suites compiled and committed to CI/CD pipeline.'
    ],
    chronos: [
        '<span class="text-yellow-400 font-bold">⏱️ [CHRONOS_ENGINE]</span> Analyzing temporal race conditions and async promise resolutions...',
        '<span class="text-yellow-300 font-bold">⚠️ [PREDICTION]</span> 89% probability of flakiness detected in payment webhook callback step',
        '<span class="text-cyan-400 font-bold">🔄 [MUTEX_BARRIER]</span> Dynamically inserting deterministic memory barrier before webhook resolution',
        '<span class="text-emerald-400 font-bold">✅ [PREVENTED]</span> Flaky test failure neutralized. Deterministic execution guaranteed.'
    ],
    fortress: [
        '<span class="text-pink-400 font-bold">🛡️ [FORTRESS_AUDIT]</span> Launching AST security taint analysis and vulnerability fuzzing...',
        '<span class="text-cyan-300 font-bold">🔒 [FUZZING]</span> Testing 2,391 payloads for SQLi, XSS, CSRF, Reentrancy, and timing side-channels',
        '<span class="text-purple-400 font-bold">📜 [POST_QUANTUM]</span> Generating ML-DSA-87 / Ed25519 cryptographic test execution attestation',
        '<span class="text-emerald-400 font-bold">✅ [FORTRESS_VERIFIED]</span> All 2,391 security edge cases passed. System zero-day hardened.'
    ]
};

function runTerminalCommand(feature) {
    if (terminalLogTimer) clearTimeout(terminalLogTimer);
    showFeatureDemo(feature);
    
    const lines = FEATURE_SCRIPTS[feature] || FEATURE_SCRIPTS.ghost;
    let idx = 0;
    
    function streamNextLine() {
        if (idx < lines.length) {
            appendTerminalLog(lines[idx]);
            idx++;
            terminalLogTimer = setTimeout(streamNextLine, 350);
        }
    }
    
    streamNextLine();
}

function clearTerminalLogs() {
    const terminal = document.getElementById('terminalOutput');
    if (terminal) {
        terminal.innerHTML = '';
        appendTerminalLog('<span class="text-cyan-400 font-bold">[READY]</span> Terminal reset. Select a feature or run a command to simulate.');
    }
}

function startAmbientTerminalHeartbeat() {
    if (terminalHeartbeatTimer) clearInterval(terminalHeartbeatTimer);
    
    const ambientLogs = [
        '<span class="text-emerald-400 font-bold">[HEARTBEAT]</span> Node <code class="text-cyan-300">0x4121</code> synced | 0 flaky tests | Swarm latency: 12ms',
        '<span class="text-purple-400 font-bold">[TELEMETRY]</span> 1,247 edge nodes active across 5 regions | Memory drift: 0.00KB',
        '<span class="text-cyan-300 font-bold">[GHOST_PROBE]</span> Cloudflare JA4 handshake valid | Zero bot detections reported',
        '<span class="text-yellow-400 font-bold">[ORACLE_SYNC]</span> Automated regression sweep: 6,685 / 6,685 passed (100% pass rate)'
    ];
    
    let ambientIdx = 0;
    terminalHeartbeatTimer = setInterval(() => {
        const terminal = document.getElementById('terminalOutput');
        if (!terminal) return;
        if (terminal.children.length > 30) {
            terminal.removeChild(terminal.firstChild);
        }
        appendTerminalLog(ambientLogs[ambientIdx % ambientLogs.length]);
        ambientIdx++;
    }, 4500);
}

function initTerminalStream() {
    const terminal = document.getElementById('terminalOutput');
    if (!terminal) return;
    
    terminal.innerHTML = '';
    
    const bootLogs = [
        '<span class="text-cyan-400 font-bold">[INIT]</span> QAntum Prime Runtime v30.6.4-OMEGA initializing...',
        '<span class="text-purple-400 font-bold">[CORE]</span> Bare-metal AST & Catuṣkoṭi logic controllers: <span class="text-emerald-400 font-bold">ONLINE</span>',
        '<span class="text-emerald-400 font-bold">[SWARM]</span> Connected to 1,247 distributed edge nodes across 5 regions',
        '<span class="text-cyan-300 font-bold">[GHOST]</span> Stealth bypass active (TLS JA4 / Chromium headless masking ready)',
        '<span class="text-yellow-300 font-bold">[ORACLE]</span> 847 routes indexed | 0 flaky tests detected in workspace',
        '<span class="text-emerald-400 font-bold">[READY]</span> Autonomous testing engine primed and awaiting trigger.'
    ];
    
    let idx = 0;
    function printBootLine() {
        if (idx < bootLogs.length) {
            appendTerminalLog(bootLogs[idx]);
            idx++;
            setTimeout(printBootLine, 250);
        } else {
            setTimeout(() => {
                runTerminalCommand('ghost');
                startAmbientTerminalHeartbeat();
            }, 600);
        }
    }
    
    printBootLine();
}

function initFeatureButtons() {
    showFeatureDemo('ghost');
    initTerminalStream();
}

function showFeatureDemo(feature) {
    const data = FEATURE_DATA[feature];
    if (!data) return;
    
    // Update active button
    document.querySelectorAll('.feature-btn').forEach(btn => {
        btn.classList.remove('active', 'border-cyan-400/40', 'bg-cyan-950/30', 'text-white');
        if (btn.dataset.feature === feature) {
            btn.classList.add('active', 'border-cyan-400/40', 'bg-cyan-950/30', 'text-white');
        }
    });
    
    // Update panel
    const titleEl = document.getElementById('fdpTitle');
    const contentEl = document.getElementById('fdpContent');
    const visualEl = document.getElementById('fdpVisual');
    
    if (titleEl) titleEl.textContent = data.title;
    
    if (contentEl) {
        contentEl.innerHTML = data.stats.map(s => 
            `<div class="fdp-stat p-2.5 rounded-xl bg-black/40 border border-white/5"><div class="text-[10px] text-gray-400 font-mono mb-1">${s.label}</div><div class="fdp-value text-base font-black text-cyan-400">${s.value}</div></div>`
        ).join('');
    }
    
    if (visualEl) {
        visualEl.innerHTML = getVisualHTML(data.visual);
    }
}

function getVisualHTML(type) {
    switch(type) {
        case 'ghost':
            return `<div class="ghost-visual flex items-center justify-between">
                <div class="gv-node px-3 py-1.5 rounded bg-red-950/50 border border-red-500/40 text-red-300 text-[11px] font-bold">Cloudflare</div>
                <div class="gv-arrow text-gray-500 font-bold">→</div>
                <div class="gv-node active px-3 py-1.5 rounded bg-cyan-950/60 border border-cyan-400 text-cyan-300 text-[11px] font-bold shadow-[0_0_15px_rgba(0,240,255,0.3)]">QAntum Prime</div>
                <div class="gv-arrow text-gray-500 font-bold">→</div>
                <div class="gv-node target px-3 py-1.5 rounded bg-emerald-950/50 border border-emerald-500/40 text-emerald-300 text-[11px] font-bold">Target ✓</div>
            </div>`;
        case 'heal':
            return `<div class="heal-visual space-y-2">
                <div class="flex justify-between text-[11px] font-mono"><span class="text-red-400">#submit-btn (404)</span><span class="text-emerald-400">Fixed ✓</span></div>
                <div class="w-full bg-white/10 h-2 rounded-full overflow-hidden"><div class="bg-gradient-to-r from-purple-500 to-cyan-400 h-full w-full animate-pulse"></div></div>
                <div class="text-[11px] font-mono text-cyan-300">[data-qa="complete-order"] (99.8% Match)</div>
            </div>`;
        case 'swarm':
            return `<div class="swarm-visual grid grid-cols-8 gap-1.5">${Array(32).fill(0).map((_, i) => `<div class="h-4 rounded bg-cyan-400/20 border border-cyan-400/40 animate-pulse" style="animation-delay:${(i%8)*100}ms"></div>`).join('')}</div>`;
        case 'oracle':
            return `<div class="oracle-visual font-mono text-xs space-y-1">
                <div class="text-cyan-400 font-bold flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-cyan-400 animate-ping"></span> AI Crawler Mapping:</div>
                <div class="flex justify-between text-gray-300 text-[11px] pt-1">
                    <span>📄 Pages: 847</span>
                    <span>🔗 State Links: 12,483</span>
                    <span>✅ Specs: 500+</span>
                </div>
            </div>`;
        case 'chronos':
            return `<div class="chronos-visual font-mono text-xs space-y-2">
                <div class="flex gap-2">
                    <span class="px-2 py-0.5 rounded bg-cyan-400/20 text-cyan-300 border border-cyan-400/40 text-[10px] font-bold">🌍 EU (256)</span>
                    <span class="px-2 py-0.5 rounded bg-purple-400/20 text-purple-300 border border-purple-400/40 text-[10px] font-bold">🌎 US (312)</span>
                    <span class="px-2 py-0.5 rounded bg-emerald-400/20 text-emerald-300 border border-emerald-400/40 text-[10px] font-bold">🌏 ASIA (198)</span>
                </div>
                <div class="text-[11px] text-yellow-300 bg-yellow-950/40 p-2 rounded border border-yellow-500/30">⚠️ Flakiness prevented → Mutex channel locked in-flight</div>
            </div>`;
        case 'fortress':
            return `<div class="fortress-visual grid grid-cols-4 gap-1.5 font-mono text-center text-[10px]">
                <span class="p-1.5 rounded bg-emerald-950/40 border border-emerald-500/30 text-emerald-300">SQLi ✓</span>
                <span class="p-1.5 rounded bg-emerald-950/40 border border-emerald-500/30 text-emerald-300">XSS ✓</span>
                <span class="p-1.5 rounded bg-emerald-950/40 border border-emerald-500/30 text-emerald-300">CSRF ✓</span>
                <span class="p-1.5 rounded bg-emerald-950/40 border border-emerald-500/30 text-emerald-300">Auth ✓</span>
            </div>`;
        default:
            return '';
    }
}

// Make functions globally available
window.showFeatureDemo = showFeatureDemo;
window.runTerminalCommand = runTerminalCommand;
window.clearTerminalLogs = clearTerminalLogs;
window.initTerminalStream = initTerminalStream;

// ═══════════════════════════════════════════════════════════════════════════════
// REAL-TIME DASHBOARD UPDATE
// ═══════════════════════════════════════════════════════════════════════════════

function updateDashboardStats(data) {
    const proofStats = {
        'lines': data.lines,
        'tests': data.testsRunning,
        'workers': data.activeWorkers,
        'passRate': data.passRate?.toFixed(1) + '%'
    };
    
    document.querySelectorAll('[data-live]').forEach(el => {
        const key = el.dataset.live;
        if (proofStats[key]) {
            el.textContent = typeof proofStats[key] === 'number' 
                ? proofStats[key].toLocaleString() 
                : proofStats[key];
        }
    });
}

// Export for potential module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { CONFIG, animateCounter, copyToClipboard, telemetry };
}

