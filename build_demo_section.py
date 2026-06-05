import os
import re

HTML_DEMO_BLOCK = """
    <!-- Interactive HUD Demo Section -->
    <section id="hud-demo" class="py-24 px-6 md:px-12 max-w-7xl mx-auto relative z-10 border-t border-white/5">
        <div class="text-center mb-16">
            <h2 class="text-4xl md:text-5xl font-black mb-4 tracking-tighter uppercase">
                <span data-i18n="demo.title">LIVE HUD INTERACTIVE DEMO</span>
            </h2>
            <p class="text-gray-400 max-w-2xl mx-auto text-sm leading-relaxed" data-i18n="demo.subtitle">
                Experience our TRL 7 Validated Virtual Human Twin modules and security interfaces running live. Each module showcases deterministic logic and real-time computation.
            </p>
        </div>

        <div class="grid lg:grid-cols-[400px_1fr] gap-8 items-start">
            <!-- Left Side: HUD List & Details -->
            <div class="space-y-4">
                <!-- HUD List Container -->
                <div class="glass-premium p-4 rounded-xl border border-white/5 space-y-2" id="demo-hud-list">
                    <!-- HUD Items will be rendered here dynamically -->
                </div>

                <!-- HUD Description & Achievement Card -->
                <div class="glass-premium p-6 rounded-xl border border-white/5 relative overflow-hidden" id="demo-details-card">
                    <div class="absolute -right-16 -top-16 w-32 h-32 bg-accent-cyan/5 rounded-full blur-2xl"></div>
                    <div class="flex items-center gap-3 mb-4">
                        <div id="demo-hud-icon-container" class="w-10 h-10 rounded-lg flex items-center justify-center border transition-all duration-300">
                            <!-- Selected HUD Icon -->
                        </div>
                        <div>
                            <h3 id="demo-hud-title" class="text-sm font-black tracking-wide uppercase transition-colors duration-300"></h3>
                            <span class="text-[9px] font-mono text-gray-500 uppercase tracking-widest font-bold" id="demo-hud-status">STATUS :: ACTIVE</span>
                        </div>
                    </div>
                    
                    <div class="space-y-4">
                        <div>
                            <div class="text-[9px] font-mono text-gray-500 uppercase tracking-widest mb-1">Functional Substrate</div>
                            <p id="demo-hud-desc" class="text-gray-300 text-xs leading-relaxed min-h-[40px]"></p>
                        </div>
                        <div>
                            <div class="text-[9px] font-mono text-gray-500 uppercase tracking-widest mb-1">Milestone Achievement</div>
                            <p id="demo-hud-ach" class="text-accent-emerald font-semibold text-xs leading-relaxed font-mono min-h-[40px]"></p>
                        </div>
                    </div>

                    <!-- Progress & Controls -->
                    <div class="mt-6 pt-4 border-t border-white/5 flex items-center justify-between gap-4">
                        <div class="flex items-center gap-2">
                            <button id="demo-play-pause-btn" class="w-8 h-8 rounded bg-white/5 border border-white/10 flex items-center justify-center hover:bg-white/10 hover:border-white/20 transition-all text-white cursor-pointer">
                                <i data-lucide="pause" class="w-3.5 h-3.5" id="demo-play-pause-icon"></i>
                            </button>
                            <span class="text-[10px] font-mono text-gray-500" id="demo-timer-label">15.0s</span>
                        </div>
                        <a id="demo-launch-btn" href="#" target="_blank" class="px-3 py-1.5 rounded border border-accent-cyan/20 bg-accent-cyan/5 text-[9px] font-black tracking-widest text-accent-cyan uppercase hover:bg-accent-cyan hover:text-black transition-all flex items-center gap-1.5">
                            <i data-lucide="external-link" class="w-3 h-3"></i>
                            <span data-i18n="demo.launch">LAUNCH HUD</span>
                        </a>
                    </div>
                </div>
            </div>

            <!-- Right Side: Live IFrame Frame -->
            <div class="glass-premium rounded-xl overflow-hidden border border-white/10 shadow-2xl flex flex-col h-[650px] relative">
                <!-- Browser Header Mock -->
                <div class="bg-black/80 px-4 py-3 border-b border-white/10 flex justify-between items-center shrink-0">
                    <div class="flex items-center gap-3 w-full">
                        <div class="flex gap-1.5 shrink-0">
                            <span class="w-2.5 h-2.5 rounded-full bg-red-500/80"></span>
                            <span class="w-2.5 h-2.5 rounded-full bg-yellow-500/80"></span>
                            <span class="w-2.5 h-2.5 rounded-full bg-emerald-500/80"></span>
                        </div>
                        <div class="bg-black/50 border border-white/5 rounded-md px-3 py-1 text-[10px] font-mono text-gray-500 flex-1 max-w-md flex items-center gap-2 overflow-hidden whitespace-nowrap">
                            <i data-lucide="lock" class="w-3 h-3 text-accent-emerald shrink-0"></i>
                            <span class="text-gray-400 select-all shrink-0">https://aeterna.website/</span>
                            <span id="demo-browser-url" class="text-white select-all overflow-hidden text-ellipsis">vht_longevity.html</span>
                        </div>
                    </div>
                    <div class="flex items-center gap-2">
                        <button id="demo-refresh-btn" class="text-gray-500 hover:text-white transition-colors cursor-pointer" title="Reload Frame">
                            <i data-lucide="refresh-cw" class="w-3.5 h-3.5"></i>
                        </button>
                        <button id="demo-fullscreen-btn" class="text-gray-500 hover:text-white transition-colors cursor-pointer" title="Fullscreen Frame">
                            <i data-lucide="maximize" class="w-3.5 h-3.5"></i>
                        </button>
                    </div>
                </div>

                <!-- Webpage IFrame -->
                <div class="flex-1 bg-[#020104] relative">
                    <iframe id="demo-iframe" src="./vht_longevity.html" class="w-full h-full border-0 absolute inset-0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" loading="lazy"></iframe>
                    <!-- Loading Mask -->
                    <div id="demo-iframe-loader" class="absolute inset-0 bg-[#050505]/95 flex flex-col items-center justify-center gap-4 transition-all duration-300 opacity-0 pointer-events-none z-20">
                        <div class="w-8 h-8 border-2 border-accent-cyan border-t-transparent rounded-full animate-spin"></div>
                        <span class="font-mono text-[10px] tracking-widest text-accent-cyan animate-pulse">SYNCHRONIZING SUBSTRATE...</span>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Interactive HUD Demo Controller Logic -->
    <script>
        const HUD_DEMO_DATA = [
            {
                id: 'longevity',
                url: './vht_longevity.html',
                icon: 'infinity',
                color: 'orange-400',
                translations: {
                    bg: {
                        title: 'LONGEVITY HUD (ДЪЛГОЛЕТИЕ)',
                        desc: 'Изследване на епигенетично препрограмиране, стареене на клетките и целеви протоколи за удължаване на живота.',
                        ach: 'Постигнахме -4.4 години биологично подмладяване (AgeAccel) чрез симулация на D+Q сенолитично прочистване.'
                    },
                    en: {
                        title: 'LONGEVITY HUD',
                        desc: 'Researching epigenetic reprogramming, cellular senescence, and targeted life-extension protocols.',
                        ach: 'Achieved -4.4 years biological age reduction (AgeAccel) through simulated D+Q senolytic clearance protocols.'
                    }
                }
            },
            {
                id: 'cardio',
                url: './vht_cardio.html',
                icon: 'heart',
                color: 'red-400',
                translations: {
                    bg: {
                        title: 'CARDIO HUD (КАРДИО)',
                        desc: 'Хемодинамика, симулиране на исхемична превенция и коронарен кръвоток в реално време.',
                        ach: 'Успешно предотвратяване на исхемия и моделиране на съдово съпротивление с 99.2% точност.'
                    },
                    en: {
                        title: 'CARDIO HUD',
                        desc: 'Hemodynamics, ischemia prevention simulation, and real-time coronary blood flow modeling.',
                        ach: 'Successfully simulated ischemia prevention and coronary vascular resistance with 99.2% accuracy.'
                    }
                }
            },
            {
                id: 'diabet',
                url: './vht_diabet.html',
                icon: 'activity',
                color: 'accent-emerald',
                translations: {
                    bg: {
                        title: 'DIABETES HUD (ДИАБЕТ)',
                        desc: 'Моделиране на глюкозната хомеостаза, инсулинова реакция и дългосрочно HbA1c стабилизиране.',
                        ach: 'Проектиран затворен цикъл на инсулиново регулиране и превенция на хипогликемия в реално време.'
                    },
                    en: {
                        title: 'DIABETES HUD',
                        desc: 'Glucose homeostasis modeling, insulin response curve, and long-term HbA1c stabilization.',
                        ach: 'Developed a closed-loop virtual insulin regulation model preventing hypoglycemia in real time.'
                    }
                }
            },
            {
                id: 'neuro',
                url: './clinical-oncology.html',
                icon: 'brain',
                color: 'accent-pink',
                translations: {
                    bg: {
                        title: 'LIVE 3D NEURO HUD (НЕВРО)',
                        desc: '3D интерактивна симулация на синаптичната плътност и глимфатичния дренаж на Алцхаймер и Глиобластом.',
                        ach: 'Постигнахме 98.50% синаптично възстановяване (BDNF) и 97.13% C-index безопасност на модела.'
                    },
                    en: {
                        title: 'LIVE 3D NEURO HUD',
                        desc: 'Interactive 3D simulation of synaptic density and glymphatic clearance in Alzheimer\'s and Glioblastoma.',
                        ach: 'Achieved 98.50% Synaptic Density recovery (BDNF) and 97.13% C-index safety model precision.'
                    }
                }
            },
            {
                id: 'oncology',
                url: './oncology_hud.html',
                icon: 'dna',
                color: 'accent-purple',
                translations: {
                    bg: {
                        title: 'ONCOLOGY HUD (ОНКОЛОГИЯ)',
                        desc: 'Симулация на ракови мутации, ДНК транскрипция и експресия на туморни гени (TCGA-GBM).',
                        ach: 'Интегриран алгоритъм за синтетична леталност, блокиращ туморната пролиферация в затворен цикъл.'
                    },
                    en: {
                        title: 'ONCOLOGY HUD',
                        desc: 'Cancer mutation simulation, DNA transcription, and tumor gene expression mapping (TCGA-GBM).',
                        ach: 'Integrated a closed-loop synthetic lethality solver to identify pathways blocking tumor proliferation.'
                    }
                }
            },
            {
                id: 'cohort',
                url: './aeterna_cohort_sim.html',
                icon: 'users',
                color: 'yellow-400',
                translations: {
                    bg: {
                        title: '100K COHORT SIMULATION (КОХОРТА)',
                        desc: 'Симулация на огромни групи пациенти за изследване на странични ефекти от медикаменти и терапевтични отговори.',
                        ach: 'Симулирано поведение на 100 000 виртуални пациенти едновременно за под 100ms на цикъл.'
                    },
                    en: {
                        title: '100K COHORT SIMULATION',
                        desc: 'Large-scale patient population simulation for checking drug side-effects and therapeutic response variance.',
                        ach: 'Simulated the therapeutic behavior of 100,000 virtual patients concurrently in under 100ms per iteration.'
                    }
                }
            },
            {
                id: 'pharma',
                url: './aeterna_pharma_shadow.html',
                icon: 'shield',
                color: 'gray-400',
                translations: {
                    bg: {
                        title: 'PHARMA SHADOW HUD (ФАРМА)',
                        desc: 'Защитени виртуални клинични изпитания на лекарствени съединения без риск за човешки пациенти.',
                        ach: 'Съкращаване на фаза 1 клинични симулации с 84% при пълно съответствие с изискванията на EMA.'
                    },
                    en: {
                        title: 'PHARMA SHADOW HUD',
                        desc: 'Secure virtual clinical drug trials for evaluating compound toxicity and efficacy with zero human risk.',
                        ach: 'Reduced Phase-1 clinical simulation trial cycle duration by 84% under full EMA-compliance protocols.'
                    }
                }
            },
            {
                id: 'sovereign',
                url: './sovereign-hud.html',
                icon: 'shield-alert',
                color: 'accent-cyan',
                translations: {
                    bg: {
                        title: 'SOVEREIGN HUD (СУВЕРЕНЕН)',
                        desc: 'Мониторинг на ядрото на AETERNA, разпределени уязвимости и Ring-0 сигурност.',
                        ach: 'Провеждане на автоматизирани одити за сигурност на Web3 смарт договори с нулева реакция на фалшиви сигнали.'
                    },
                    en: {
                        title: 'SOVEREIGN HUD',
                        desc: 'AETERNA core substrate monitoring, distributed vulnerability tracking, and Ring-0 security execution.',
                        ach: 'Conducted automated Web3 smart contract audits with zero-false-positive rates under PQC encryption.'
                    }
                }
            }
        ];

        const colorClasses = {
            'orange-400': {
                text: 'text-orange-400',
                border: 'border-orange-500/30',
                bg: 'bg-orange-500/10'
            },
            'red-400': {
                text: 'text-red-400',
                border: 'border-red-400/30',
                bg: 'bg-red-400/10'
            },
            'accent-emerald': {
                text: 'text-[#00ffaa]',
                border: 'border-[#00ffaa]/30',
                bg: 'bg-[#00ffaa]/10'
            },
            'accent-pink': {
                text: 'text-[#ff2a85]',
                border: 'border-[#ff2a85]/30',
                bg: 'bg-[#ff2a85]/10'
            },
            'accent-purple': {
                text: 'text-[#b55fe6]',
                border: 'border-[#b55fe6]/30',
                bg: 'bg-[#b55fe6]/10'
            },
            'yellow-400': {
                text: 'text-yellow-400',
                border: 'border-yellow-400/30',
                bg: 'bg-yellow-400/10'
            },
            'gray-400': {
                text: 'text-gray-400',
                border: 'border-gray-400/30',
                bg: 'bg-gray-400/10'
            },
            'accent-cyan': {
                text: 'text-[#00f0ff]',
                border: 'border-[#00f0ff]/30',
                bg: 'bg-[#00f0ff]/10'
            }
        };

        let demoActiveIndex = 0;
        let demoTimer = 0; // ms
        const demoDuration = 15000; // 15 seconds
        const demoInterval = 100; // update progress every 100ms
        let demoIntervalId = null;
        let demoIsPlaying = true;

        function initDemoSection() {
            const listContainer = document.getElementById('demo-hud-list');
            if (!listContainer) return;
            listContainer.innerHTML = '';
            
            HUD_DEMO_DATA.forEach((hud, idx) => {
                const item = document.createElement('div');
                item.className = 'relative overflow-hidden cursor-pointer p-3 rounded-lg border border-white/5 hover:border-white/20 transition-all duration-300 flex items-center justify-between group';
                item.setAttribute('data-hud-idx', idx);
                
                // Progress overlay
                const progressBg = document.createElement('div');
                progressBg.id = `demo-progress-${idx}`;
                progressBg.className = 'absolute inset-y-0 left-0 bg-white/5 transition-all duration-100 pointer-events-none';
                progressBg.style.width = '0%';
                
                const infoDiv = document.createElement('div');
                infoDiv.className = 'flex items-center gap-3 relative z-10';
                
                const colorInfo = colorClasses[hud.color] || colorClasses['accent-cyan'];
                
                // Icon container with resolved class
                const iconContainer = document.createElement('div');
                iconContainer.className = `w-5 h-5 rounded ${colorInfo.bg} flex items-center justify-center ${colorInfo.text}`;
                iconContainer.innerHTML = `<i data-lucide="${hud.icon}" class="w-3.5 h-3.5"></i>`;
                
                const nameSpan = document.createElement('span');
                nameSpan.className = 'text-xs font-bold text-gray-400 group-hover:text-white transition-colors';
                nameSpan.id = `demo-name-${idx}`;
                
                infoDiv.appendChild(iconContainer);
                infoDiv.appendChild(nameSpan);
                
                const fileSpan = document.createElement('span');
                fileSpan.className = 'text-[9px] font-mono text-gray-500 relative z-10';
                fileSpan.textContent = hud.url.replace('./', '');
                
                item.appendChild(progressBg);
                item.appendChild(infoDiv);
                item.appendChild(fileSpan);
                
                item.addEventListener('click', () => {
                    selectDemoHud(idx, true);
                });
                
                listContainer.appendChild(item);
            });
            
            if (window.lucide) {
                window.lucide.createIcons();
            }
            
            selectDemoHud(0, false);
            startDemoTimer();
        }

        function selectDemoHud(index, manualClick = false) {
            if (manualClick) {
                setDemoPlayState(false);
            }
            
            HUD_DEMO_DATA.forEach((_, idx) => {
                const pb = document.getElementById(`demo-progress-${idx}`);
                if (pb) pb.style.width = '0%';
                
                const item = document.querySelector(`[data-hud-idx="${idx}"]`);
                if (item) {
                    item.classList.remove('border-white/20', 'bg-white/5');
                    item.classList.add('border-white/5');
                    const name = document.getElementById(`demo-name-${idx}`);
                    if (name) {
                        name.classList.remove('text-white');
                        name.classList.add('text-gray-400');
                    }
                }
            });
            
            demoActiveIndex = index;
            demoTimer = 0;
            
            const activeHud = HUD_DEMO_DATA[index];
            
            const activeItem = document.querySelector(`[data-hud-idx="${index}"]`);
            if (activeItem) {
                activeItem.classList.remove('border-white/5');
                activeItem.classList.add('border-white/20', 'bg-white/5');
                const name = document.getElementById(`demo-name-${index}`);
                if (name) {
                    name.classList.remove('text-gray-400');
                    name.classList.add('text-white');
                }
            }
            
            const iframe = document.getElementById('demo-iframe');
            const loader = document.getElementById('demo-iframe-loader');
            
            if (iframe && iframe.src !== activeHud.url) {
                loader.classList.remove('opacity-0', 'pointer-events-none');
                iframe.src = activeHud.url;
                iframe.onload = () => {
                    loader.classList.add('opacity-0', 'pointer-events-none');
                };
            }
            
            const urlText = document.getElementById('demo-browser-url');
            if (urlText) {
                urlText.textContent = activeHud.url.replace('./', '');
            }
            
            const launchBtn = document.getElementById('demo-launch-btn');
            if (launchBtn) {
                launchBtn.href = activeHud.url;
            }
            
            updateDemoHudText();
        }

        function updateDemoHudText() {
            const activeHud = HUD_DEMO_DATA[demoActiveIndex];
            const lang = (window.state && window.state.lang) || 'bg';
            const activeTrans = activeHud.translations[lang] || activeHud.translations['en'];
            
            const titleEl = document.getElementById('demo-hud-title');
            if (titleEl) {
                titleEl.textContent = activeTrans.title;
                const colorInfo = colorClasses[activeHud.color] || colorClasses['accent-cyan'];
                titleEl.className = `text-sm font-black tracking-wide uppercase ${colorInfo.text} transition-colors duration-300`;
            }
            
            const descEl = document.getElementById('demo-hud-desc');
            if (descEl) descEl.textContent = activeTrans.desc;
            
            const achEl = document.getElementById('demo-hud-ach');
            if (achEl) achEl.textContent = activeTrans.ach;
            
            const iconContainer = document.getElementById('demo-hud-icon-container');
            if (iconContainer) {
                const colorInfo = colorClasses[activeHud.color] || colorClasses['accent-cyan'];
                iconContainer.className = `w-10 h-10 rounded-lg flex items-center justify-center border ${colorInfo.bg} ${colorInfo.border} ${colorInfo.text}`;
                iconContainer.innerHTML = `<i data-lucide="${activeHud.icon}" class="w-5 h-5"></i>`;
                if (window.lucide) window.lucide.createIcons();
            }
            
            HUD_DEMO_DATA.forEach((hud, idx) => {
                const nameSpan = document.getElementById(`demo-name-${idx}`);
                if (nameSpan) {
                    nameSpan.textContent = (hud.translations[lang] || hud.translations['en']).title.split(' (')[0];
                }
            });
        }

        function startDemoTimer() {
            if (demoIntervalId) clearInterval(demoIntervalId);
            
            demoIntervalId = setInterval(() => {
                if (!demoIsPlaying) return;
                
                demoTimer += demoInterval;
                const progressPercentage = (demoTimer / demoDuration) * 100;
                
                const pb = document.getElementById(`demo-progress-${demoActiveIndex}`);
                if (pb) {
                    pb.style.width = `${progressPercentage}%`;
                }
                
                const timerLabel = document.getElementById('demo-timer-label');
                if (timerLabel) {
                    const secondsLeft = Math.max(0, (demoDuration - demoTimer) / 1000).toFixed(1);
                    timerLabel.textContent = `${secondsLeft}s`;
                }
                
                if (demoTimer >= demoDuration) {
                    const nextIdx = (demoActiveIndex + 1) % HUD_DEMO_DATA.length;
                    selectDemoHud(nextIdx, false);
                }
            }, demoInterval);
        }

        function setDemoPlayState(play) {
            demoIsPlaying = play;
            const playPauseIcon = document.getElementById('demo-play-pause-icon');
            if (playPauseIcon) {
                if (demoIsPlaying) {
                    playPauseIcon.setAttribute('data-lucide', 'pause');
                } else {
                    playPauseIcon.setAttribute('data-lucide', 'play');
                }
                if (window.lucide) window.lucide.createIcons();
            }
        }

        window.updateDemoHud = function() {
            updateDemoHudText();
        };

        document.addEventListener('DOMContentLoaded', () => {
            initDemoSection();
            
            const playPauseBtn = document.getElementById('demo-play-pause-btn');
            if (playPauseBtn) {
                playPauseBtn.addEventListener('click', () => {
                    setDemoPlayState(!demoIsPlaying);
                });
            }
            
            const refreshBtn = document.getElementById('demo-refresh-btn');
            if (refreshBtn) {
                refreshBtn.addEventListener('click', () => {
                    const iframe = document.getElementById('demo-iframe');
                    if (iframe) {
                        const loader = document.getElementById('demo-iframe-loader');
                        if (loader) loader.classList.remove('opacity-0', 'pointer-events-none');
                        iframe.src = iframe.src;
                    }
                });
            }
            
            const fullscreenBtn = document.getElementById('demo-fullscreen-btn');
            if (fullscreenBtn) {
                fullscreenBtn.addEventListener('click', () => {
                    const iframe = document.getElementById('demo-iframe');
                    if (iframe) {
                        if (iframe.requestFullscreen) {
                            iframe.requestFullscreen();
                        } else if (iframe.webkitRequestFullscreen) {
                            iframe.webkitRequestFullscreen();
                        } else if (iframe.msRequestFullscreen) {
                            iframe.msRequestFullscreen();
                        }
                    }
                });
            }
        });
    </script>
"""

def main():
    filepath = "Z:\\\\aeterna.website\\\\index.html"
    if not os.path.exists(filepath):
        print(f"❌ Error: {filepath} not found.")
        return
        
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Check if already injected
    if 'id="hud-demo"' in content:
        print("⚠️ Demo section already exists in index.html, removing old version...")
        # Remove old section and controller script
        content = re.sub(r'<!-- Interactive HUD Demo Section -->.*?<!-- Interactive HUD Demo Controller Logic -->.*?<\/script>', '', content, flags=re.DOTALL)

    # 1. Inject the HTML block right before <!-- Technical Changelog & Milestones Section -->
    target_section_marker = "<!-- Technical Changelog & Milestones Section -->"
    if target_section_marker in content:
        content = content.replace(target_section_marker, HTML_DEMO_BLOCK + "\\n\\n    " + target_section_marker)
        print("✅ HTML Block injected successfully.")
    else:
        print("❌ Error: Target section marker not found in index.html")
        return

    # 2. Inject translation keys inside translations.bg
    bg_search_str = '"scientific.card6_status_val": "Синтетична леталност"'
    bg_replace_str = bg_search_str + ',\\n                "demo.title": "ИНТЕРАКТИВНО ДЕМО НА HUD СИСТЕМИТЕ",\\n                "demo.subtitle": "Изпитайте на живо нашите TRL 7 валидирани модули за Виртуален човешки близнак и интерфейси за сигурност. Всеки модул демонстрира детерминистична логика и изчисления в реално време.",\\n                "demo.launch": "СТАРТИРАЙ HUD"'
    if bg_search_str in content:
        content = content.replace(bg_search_str, bg_replace_str)
        print("✅ BG Translations injected successfully.")
    else:
        print("❌ Warning: BG translations target not found. Skipping translations injection.")

    # 3. Inject translation keys inside translations.en
    en_search_str = '"scientific.card6_status_val": "Synthetic Lethality"'
    en_replace_str = en_search_str + ',\\n                "demo.title": "LIVE HUD INTERACTIVE DEMO",\\n                "demo.subtitle": "Experience our TRL 7 Validated Virtual Human Twin modules and security interfaces running live. Each module showcases deterministic logic and real-time computation.",\\n                "demo.launch": "LAUNCH HUD"'
    if en_search_str in content:
        content = content.replace(en_search_str, en_replace_str)
        print("✅ EN Translations injected successfully.")
    else:
        print("❌ Warning: EN translations target not found. Skipping translations injection.")

    # 4. Inject hook call in setLanguage(langCode)
    hook_search_str = "setTRLStep(state.trlStep);\\n        }"
    hook_replace_str = "setTRLStep(state.trlStep);\\n            \\n            // Sync HUD Demo Translations\\n            if (typeof updateDemoHud === 'function') {\\n                updateDemoHud();\\n            }\\n        }"
    if hook_search_str in content:
        content = content.replace(hook_search_str, hook_replace_str)
        print("✅ setLanguage hook injected successfully.")
    else:
        # Fallback to handle alternate formatting (single spacing)
        hook_search_str_alt = "setTRLStep(state.trlStep);\\n        }"
        # Let's search with regex to be sure
        match = re.search(r'setTRLStep\(state\.trlStep\);\s*\}', content)
        if match:
            matched_text = match.group(0)
            replacement = matched_text.replace("}", "\\n            if (typeof updateDemoHud === 'function') { updateDemoHud(); }\\n        }")
            content = content.replace(matched_text, replacement)
            print("✅ setLanguage hook injected successfully via regex.")
        else:
            print("❌ Error: Could not find setLanguage closing hook.")
            return

    # Write the modified content back
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print("🎉 Injection completed successfully!")

if __name__ == "__main__":
    main()
