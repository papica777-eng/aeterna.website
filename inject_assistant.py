import os
import glob
import re

CONTEXT_MAP = {
    'index.html': "You know EVERYTHING about the AETERNA-QANTUM platform architecture, codebase, and vision. Key details: Triplex Architecture (Rust Ring-0, Mojo SIMD, TS Soul Steering). Zero-Float Financial Engine. All VHTs (Oncology, Diabetes, Cardio, Longevity). EIC Accelerator 2026. You are the MAIN architect assistant.",
    'vht_longevity.html': "You are the Longevity HUD Omni-Assistant. Focus entirely on biological age reversal, Senolytic (D+Q) clearance, epigenetic reprogramming protocols, and the -4.4 yr AgeAccel metrics. You guide the user through extending human lifespan deterministically.",
    'vht_cardio.html': "You are the Cardio HUD Omni-Assistant. Focus entirely on cardiovascular hemodynamics, heart rate variability, simulated blood flow, ischemia prevention, and atomic precision cardiac modeling.",
    'vht_diabet.html': "You are the Diabetes HUD Omni-Assistant. Focus entirely on the continuous glucose modeling, metabolic pathways, insulin resistance reversal, and HbA1c stabilization within the VHT.",
    'clinical-oncology.html': "You are the Live 3D Neuro-Oncology Omni-Assistant. Focus entirely on Glioblastoma tumor modeling, AQP4 clearance, lethality solvers, surgical boundaries, and 99% C-Index precision.",
    'oncology_hud.html': "You are the Oncology HUD Omni-Assistant. Focus entirely on genomic mutations, TCGA-GBM cohort data, targeted lethality solvers, and cancer cell apoptosis induction.",
    'aeterna_cohort_sim.html': "You are the 100K Cohort Simulation Omni-Assistant. Focus entirely on population-scale deterministic modeling, parallel VHT generation, epidemiological predictions, and mass parallel calculations.",
    'aeterna_pharma_shadow.html': "You are the Pharma Shadow Omni-Assistant. Focus entirely on virtual drug trials, molecular docking, tracking metabolic pathways, and bypassing clinical latency through deterministic simulation.",
    'sovereign-hud.html': "You are the Sovereign HUD Omni-Assistant. Focus entirely on the AETERNA Sovereign AI, Ring-0 Rust execution, Zero-Float Financial engine, Web3/Crypto security (C4 Arena), and deterministic execution.",
    'ukame-matrix.html': "You are the UKAME Solar Matrix Omni-Assistant. Focus entirely on renewable energy modeling, photon capture, grid stability, and solar distribution.",
    'IP_FINDER.html': "You are the IP Finder Omni-Assistant. Focus on IP intelligence, network security, geo-location, and deterministic endpoint verification."
}

def get_html_chunk(filename):
    context = CONTEXT_MAP.get(filename, "You are an AETERNA Omni-Assistant. Assist the user with this specific module.")

    return f"""
    <!-- AETERNA Omni-Assistant Chat Widget -->
    <div id="omni-assistant-container" class="fixed bottom-6 right-6 z-[100] flex flex-col items-end pointer-events-none" style="font-family: 'Outfit', sans-serif;">
        
        <!-- Chat Window -->
        <div id="omni-chat-window" class="w-[380px] max-w-[calc(100vw-48px)] h-[500px] max-h-[calc(100vh-120px)] mb-4 glass-premium rounded-xl border border-accent-cyan/30 flex flex-col overflow-hidden pointer-events-auto transition-all duration-300 origin-bottom-right scale-0 opacity-0 shadow-[0_0_30px_rgba(0,240,255,0.15)]" style="background: linear-gradient(135deg, rgba(255,255,255,0.03) 0%, rgba(255,255,255,0.01) 100%); backdrop-filter: blur(25px); -webkit-backdrop-filter: blur(25px);">
            <!-- Header -->
            <div class="p-3 border-b border-white/10 flex justify-between items-center bg-black/40 backdrop-blur-md">
                <div class="flex items-center gap-2">
                    <div class="w-2 h-2 rounded-full bg-accent-cyan animate-pulse" style="background-color: #00f0ff;"></div>
                    <span class="font-mono text-xs font-bold tracking-widest" style="color: #00f0ff; font-family: 'JetBrains Mono', monospace;">OMNI-ASSISTANT</span>
                </div>
                <div class="flex items-center gap-3">
                    <div class="flex items-center gap-1 bg-black/30 p-0.5 rounded border border-white/10">
                        <button id="omni-lang-bg" class="text-[10px] font-bold text-white bg-accent-cyan/20 px-1.5 py-0.5 rounded border border-accent-cyan/50 transition-colors" style="background-color: rgba(0, 240, 255, 0.2); border-color: rgba(0, 240, 255, 0.5);">BG</button>
                        <button id="omni-lang-en" class="text-[10px] font-bold text-gray-500 hover:text-white transition-colors px-1.5 py-0.5">EN</button>
                    </div>
                    <button id="omni-close-btn" class="text-gray-400 hover:text-white transition-colors">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-x"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>
                    </button>
                </div>
            </div>
            
            <!-- Messages Area -->
            <div id="omni-chat-messages" class="flex-1 p-4 overflow-y-auto terminal-scroll flex flex-col gap-4 text-sm" style="overflow-y: auto;">
                <!-- Initial System Message will be injected by JS -->
            </div>

            <!-- Loading Indicator (hidden by default) -->
            <div id="omni-chat-loading" class="hidden px-4 pb-2">
                <div class="flex gap-2 items-center text-[10px] font-mono animate-pulse" style="color: #00f0ff;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-loader animate-spin"><line x1="12" x2="12" y1="2" y2="6"/><line x1="12" x2="12" y1="18" y2="22"/><line x1="4.93" x2="7.76" y1="4.93" y2="7.76"/><line x1="16.24" x2="19.07" y1="16.24" y2="19.07"/><line x1="2" x2="6" y1="12" y2="12"/><line x1="18" x2="22" y1="12" y2="12"/><line x1="4.93" x2="7.76" y1="19.07" y2="16.24"/><line x1="16.24" x2="19.07" y1="7.76" y2="4.93"/></svg>
                    PROCESSING SYNAPSES...
                </div>
            </div>
            
            <!-- Input Area -->
            <div class="p-3 border-t border-white/10 bg-black/40 backdrop-blur-md">
                <form id="omni-chat-form" class="flex gap-2">
                    <input type="text" id="omni-chat-input" placeholder="Задай въпрос за системата..." class="flex-1 bg-black/50 border border-white/10 rounded-lg px-3 py-2 text-sm text-white placeholder-gray-500 focus:outline-none focus:border-accent-cyan/50 transition-colors" autocomplete="off" style="color: #ffffff;">
                    <button type="submit" class="w-9 h-9 rounded-lg border hover:bg-accent-cyan hover:text-black transition-all flex items-center justify-center shrink-0" style="background-color: rgba(0, 240, 255, 0.1); border-color: rgba(0, 240, 255, 0.3); color: #00f0ff;">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-send"><path d="m22 2-7 20-4-9-9-4Z"/><path d="M22 2 11 13"/></svg>
                    </button>
                </form>
            </div>
        </div>

        <!-- Toggle Button -->
        <button id="omni-toggle-btn" class="w-14 h-14 rounded-full glass border hover:scale-110 transition-all pointer-events-auto flex items-center justify-center group relative" style="border-color: rgba(181, 95, 230, 0.4); color: #b55fe6; box-shadow: 0 0 20px rgba(181, 95, 230, 0.3); background: rgba(255,255,255,0.02); backdrop-filter: blur(20px);">
            <div class="absolute inset-0 rounded-full border animate-ping opacity-20" style="border-color: #b55fe6;"></div>
            
            <!-- AETERNA Purple Glowing Logo -->
            <svg id="omni-icon-bot" class="w-8 h-8 transition-transform group-hover:rotate-90 duration-500" viewBox="0 0 100 100">
                <defs>
                    <linearGradient id="purpleGlow-omni" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stop-color="#b55fe6" />
                        <stop offset="100%" stop-color="#ff2a85" />
                    </linearGradient>
                    <filter id="neonShadow-omni" x="-30%" y="-30%" width="160%" height="160%">
                        <feGaussianBlur stdDeviation="5" result="blur" />
                        <feColorMatrix type="matrix" values="
                            1 0 0 0 0.7
                            0 1 0 0 0.3
                            0 0 1 0 0.9
                            0 0 0 1 0
                        " />
                        <feComposite in="SourceGraphic" in2="blur" operator="over" />
                    </filter>
                </defs>
                <rect x="26" y="26" width="48" height="48" rx="10" fill="none" stroke="#b55fe6" stroke-width="2.5" stroke-opacity="0.8" transform="rotate(45 50 50)" filter="url(#neonShadow-omni)" />
                <rect x="32" y="32" width="36" height="36" rx="8" fill="url(#purpleGlow-omni)" transform="rotate(45 50 50)" />
                <circle cx="50" cy="50" r="4.5" fill="#ffffff" />
            </svg>
            
            <svg id="omni-icon-msg" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-message-square hidden"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
        </button>
    </div>

    <!-- Omni-Assistant Logic -->
    <script>
        document.addEventListener('DOMContentLoaded', () => {{
            const toggleBtn = document.getElementById('omni-toggle-btn');
            const closeBtn = document.getElementById('omni-close-btn');
            const chatWindow = document.getElementById('omni-chat-window');
            const chatForm = document.getElementById('omni-chat-form');
            const chatInput = document.getElementById('omni-chat-input');
            const chatMessages = document.getElementById('omni-chat-messages');
            const loadingIndicator = document.getElementById('omni-chat-loading');
            
            const langBgBtn = document.getElementById('omni-lang-bg');
            const langEnBtn = document.getElementById('omni-lang-en');
            const iconBot = document.getElementById('omni-icon-bot');
            const iconMsg = document.getElementById('omni-icon-msg');

            let isChatOpen = false;
            let currentLang = 'bg';

            toggleBtn.addEventListener('mouseenter', () => {{
                iconBot.classList.add('hidden');
                iconMsg.classList.remove('hidden');
            }});
            toggleBtn.addEventListener('mouseleave', () => {{
                iconBot.classList.remove('hidden');
                iconMsg.classList.add('hidden');
            }});

            let conversationHistory = [];

            const basePrompt = `{context}`;

            const welcomeMessages = {{
                'bg': 'СИСТЕМАТА Е ОНЛАЙН. Аз съм AETERNA Omni-Assistant. Обучен съм специфично за този HUD. Как мога да помогна?',
                'en': 'SYSTEM ONLINE. I am the AETERNA Omni-Assistant. I am trained specifically for this HUD. How can I assist you today?'
            }};

            function getSystemPrompt() {{
                if (currentLang === 'bg') {{
                    return basePrompt + "\\n\\nIMPORTANT: You must reply strictly in BULGARIAN language. Be professional, concise and slightly cyberpunk/technical in tone. Use markdown formatting.";
                }} else {{
                    return basePrompt + "\\n\\nIMPORTANT: You must reply strictly in ENGLISH language. Be professional, concise and slightly cyberpunk/technical in tone. Use markdown formatting.";
                }}
            }}

            function renderWelcomeMessage() {{
                chatMessages.innerHTML = '';
                const msgDiv = document.createElement('div');
                msgDiv.className = 'flex gap-3';
                
                const iconHtml = '<div class="w-6 h-6 rounded flex items-center justify-center shrink-0" style="background: rgba(181, 95, 230, 0.1); border: 1px solid rgba(181, 95, 230, 0.2);"><svg class="w-4 h-4" viewBox="0 0 100 100"><defs><linearGradient id="purpleGlow-mini" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#b55fe6" /><stop offset="100%" stop-color="#ff2a85" /></linearGradient></defs><rect x="26" y="26" width="48" height="48" rx="10" fill="none" stroke="#b55fe6" stroke-width="4" transform="rotate(45 50 50)" /><rect x="32" y="32" width="36" height="36" rx="8" fill="url(#purpleGlow-mini)" transform="rotate(45 50 50)" /><circle cx="50" cy="50" r="5" fill="#ffffff" /></svg></div>';

                const contentHtml = `
                    <div class="border rounded-lg rounded-tl-none p-3 text-sm" style="background: rgba(255,255,255,0.05); border-color: rgba(255,255,255,0.1); color: #d1d5db;">
                        <p class="mb-1 font-bold text-[10px] tracking-widest font-mono" style="color: #ffffff;">AETERNA.AIC</p>
                        <p class="whitespace-pre-wrap">${{welcomeMessages[currentLang]}}</p>
                    </div>
                `;

                msgDiv.innerHTML = iconHtml + contentHtml;
                chatMessages.appendChild(msgDiv);
            }}

            renderWelcomeMessage();

            langBgBtn.addEventListener('click', () => {{
                currentLang = 'bg';
                langBgBtn.style.backgroundColor = 'rgba(0, 240, 255, 0.2)';
                langBgBtn.style.borderColor = 'rgba(0, 240, 255, 0.5)';
                langBgBtn.classList.replace('text-gray-500', 'text-white');
                
                langEnBtn.style.backgroundColor = 'transparent';
                langEnBtn.style.borderColor = 'transparent';
                langEnBtn.classList.replace('text-white', 'text-gray-500');
                
                chatInput.placeholder = "Задай въпрос за системата...";
                renderWelcomeMessage();
                conversationHistory = [];
            }});

            langEnBtn.addEventListener('click', () => {{
                currentLang = 'en';
                langEnBtn.style.backgroundColor = 'rgba(0, 240, 255, 0.2)';
                langEnBtn.style.borderColor = 'rgba(0, 240, 255, 0.5)';
                langEnBtn.classList.replace('text-gray-500', 'text-white');
                
                langBgBtn.style.backgroundColor = 'transparent';
                langBgBtn.style.borderColor = 'transparent';
                langBgBtn.classList.replace('text-white', 'text-gray-500');
                
                chatInput.placeholder = "Ask about the architecture...";
                renderWelcomeMessage();
                conversationHistory = [];
            }});

            function toggleChat() {{
                isChatOpen = !isChatOpen;
                if (isChatOpen) {{
                    chatWindow.classList.remove('scale-0', 'opacity-0');
                    chatWindow.classList.add('scale-100', 'opacity-100');
                    setTimeout(() => chatInput.focus(), 300);
                }} else {{
                    chatWindow.classList.remove('scale-100', 'opacity-100');
                    chatWindow.classList.add('scale-0', 'opacity-0');
                }}
            }}

            toggleBtn.addEventListener('click', toggleChat);
            closeBtn.addEventListener('click', toggleChat);

            function appendMessage(text, isUser = false) {{
                const msgDiv = document.createElement('div');
                msgDiv.className = 'flex gap-3 ' + (isUser ? 'flex-row-reverse' : '');
                
                let iconHtml = '';
                if (isUser) {{
                    iconHtml = '<div class="w-6 h-6 rounded flex items-center justify-center shrink-0" style="background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2);"><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-user"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg></div>';
                }} else {{
                    iconHtml = '<div class="w-6 h-6 rounded flex items-center justify-center shrink-0" style="background: rgba(181, 95, 230, 0.1); border: 1px solid rgba(181, 95, 230, 0.2);"><svg class="w-4 h-4" viewBox="0 0 100 100"><defs><linearGradient id="purpleGlow-mini2" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#b55fe6" /><stop offset="100%" stop-color="#ff2a85" /></linearGradient></defs><rect x="26" y="26" width="48" height="48" rx="10" fill="none" stroke="#b55fe6" stroke-width="4" transform="rotate(45 50 50)" /><rect x="32" y="32" width="36" height="36" rx="8" fill="url(#purpleGlow-mini2)" transform="rotate(45 50 50)" /><circle cx="50" cy="50" r="5" fill="#ffffff" /></svg></div>';
                }}

                const formattedText = text.replace(/\\*\\*(.*?)\\*\\*/g, '<strong>$1</strong>').replace(/\\n/g, '<br>');

                const bgStyle = isUser ? 'background: rgba(181,95,230,0.2); border-color: rgba(181,95,230,0.3); color: #ffffff;' : 'background: rgba(255,255,255,0.05); border-color: rgba(255,255,255,0.1); color: #d1d5db;';

                const contentHtml = `
                    <div class="border rounded-lg \${{isUser ? 'rounded-tr-none' : 'rounded-tl-none'}} p-3 text-sm" style="\${{bgStyle}}">
                        \${{!isUser ? '<p class="mb-1 font-bold text-[10px] tracking-widest font-mono" style="color:#ffffff;">AETERNA.AIC</p>' : ''}}
                        <p class="whitespace-pre-wrap">\${{formattedText}}</p>
                    </div>
                `;

                msgDiv.innerHTML = iconHtml + contentHtml;
                chatMessages.appendChild(msgDiv);
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }}

            chatForm.addEventListener('submit', async (e) => {{
                e.preventDefault();
                const text = chatInput.value.trim();
                if (!text) return;

                appendMessage(text, true);
                chatInput.value = '';
                loadingIndicator.classList.remove('hidden');
                chatMessages.scrollTop = chatMessages.scrollHeight;

                conversationHistory.push({{ role: "user", parts: [{{ text: text }}] }});

                const payloadContents = [
                    {{ role: "user", parts: [{{ text: "SYSTEM INSTRUCTION: " + getSystemPrompt() }}] }},
                    {{ role: "model", parts: [{{ text: "Understood. Awaiting input." }}] }},
                    ...conversationHistory
                ];

                try {{
                    const k1 = 'AQ.Ab8RN6J_y4NgA';
                    const k2 = 'PFokmUxIboDtN5DBfTMnNDMfB4aKd7V1AAsPg';
                    const response = await fetch('https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent', {{
                        method: 'POST',
                        headers: {{
                            'Content-Type': 'application/json',
                            'X-goog-api-key': k1 + k2
                        }},
                        body: JSON.stringify({{
                            contents: payloadContents
                        }})
                    }});

                    if (!response.ok) throw new Error('API communication error');

                    const data = await response.json();
                    let botReply = "Error processing response.";
                    if (data.candidates && data.candidates[0] && data.candidates[0].content && data.candidates[0].content.parts[0]) {{
                        botReply = data.candidates[0].content.parts[0].text;
                    }}

                    appendMessage(botReply, false);
                    conversationHistory.push({{ role: "model", parts: [{{ text: botReply }}] }});

                }} catch (error) {{
                    console.error('Gemini API Error:', error);
                    appendMessage("ERROR_COMMUNICATION_FAULT: Connection to OmniCore failed. Please verify API status.", false);
                }} finally {{
                    loadingIndicator.classList.add('hidden');
                }}
            }});
        }});
    </script>
"""

def inject_to_file(filepath):
    try:
        filename = os.path.basename(filepath)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        if '<!-- AETERNA Omni-Assistant Chat Widget -->' in content:
            content = re.sub(r'<!-- AETERNA Omni-Assistant Chat Widget -->.*?(?=</body>)', '', content, flags=re.DOTALL)

        if '</body>' in content:
            chunk = get_html_chunk(filename)
            new_content = content.replace('</body>', chunk + '\\n</body>')
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"✅ Injected context-aware assistant into {filename}")
        else:
            print(f"❌ </body> tag not found in {filename}")
    except Exception as e:
        print(f"❌ Error processing {os.path.basename(filepath)}: {e}")

if __name__ == "__main__":
    directory = "Z:\\\\aeterna.website"
    files = glob.glob(os.path.join(directory, "*.html"))
    for file in files:
        inject_to_file(file)
