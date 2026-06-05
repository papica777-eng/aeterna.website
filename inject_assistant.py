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
    <div id="omni-assistant-container">
        <style>
            #omni-assistant-container {{
                position: fixed;
                bottom: 24px;
                right: 24px;
                z-index: 99999;
                font-family: 'Outfit', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                display: flex;
                flex-direction: column;
                align-items: flex-end;
                pointer-events: none;
            }}
            #omni-assistant-container * {{
                box-sizing: border-box;
            }}
            #omni-toggle-btn {{
                width: 56px;
                height: 56px;
                border-radius: 50%;
                border: 1px solid rgba(181, 95, 230, 0.45);
                background: rgba(14, 20, 35, 0.85);
                backdrop-filter: blur(20px);
                -webkit-backdrop-filter: blur(20px);
                color: #b55fe6;
                box-shadow: 0 0 20px rgba(181, 95, 230, 0.3);
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                pointer-events: auto;
                transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                position: relative;
                padding: 0;
            }}
            #omni-toggle-btn:hover {{
                transform: scale(1.1);
            }}
            #omni-toggle-btn .ping-ring {{
                position: absolute;
                inset: 0;
                border-radius: 50%;
                border: 1px solid #b55fe6;
                opacity: 0.2;
                animation: omni-ping 1.5s cubic-bezier(0, 0, 0.2, 1) infinite;
            }}
            @keyframes omni-ping {{
                75%, 100% {{
                    transform: scale(1.4);
                    opacity: 0;
                }}
            }}
            #omni-chat-window {{
                width: 380px;
                max-width: calc(100vw - 48px);
                height: 500px;
                max-h: calc(100vh - 120px);
                margin-bottom: 16px;
                border-radius: 12px;
                border: 1px solid rgba(0, 240, 255, 0.3);
                background: linear-gradient(135deg, rgba(14, 20, 35, 0.95) 0%, rgba(8, 12, 24, 0.98) 100%);
                backdrop-filter: blur(25px);
                -webkit-backdrop-filter: blur(25px);
                box-shadow: 0 0 30px rgba(0, 240, 255, 0.15);
                display: flex;
                flex-direction: column;
                overflow: hidden;
                pointer-events: auto;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                transform-origin: bottom right;
                transform: scale(0);
                opacity: 0;
            }}
            #omni-chat-window.open {{
                transform: scale(1);
                opacity: 1;
            }}
            .omni-header {{
                padding: 12px 16px;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
                display: flex;
                justify-content: space-between;
                align-items: center;
                background: rgba(0, 0, 0, 0.4);
                flex-shrink: 0;
            }}
            .omni-header-title {{
                display: flex;
                align-items: center;
                gap: 8px;
            }}
            .omni-header-dot {{
                width: 8px;
                height: 8px;
                border-radius: 50%;
                background-color: #00f0ff;
                animation: omni-pulse 2s infinite;
            }}
            @keyframes omni-pulse {{
                0%, 100% {{ opacity: 1; }}
                50% {{ opacity: 0.4; }}
            }}
            .omni-header-text {{
                font-family: 'JetBrains Mono', monospace;
                font-size: 11px;
                font-weight: 700;
                letter-spacing: 0.1em;
                color: #00f0ff;
            }}
            .omni-header-controls {{
                display: flex;
                align-items: center;
                gap: 12px;
            }}
            .omni-lang-pill {{
                display: flex;
                align-items: center;
                background: rgba(0, 0, 0, 0.3);
                padding: 2px;
                border-radius: 4px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }}
            .omni-lang-btn {{
                background: transparent;
                border: none;
                color: #718096;
                font-size: 10px;
                font-weight: 700;
                padding: 2px 6px;
                border-radius: 3px;
                cursor: pointer;
                transition: all 0.2s;
            }}
            .omni-lang-btn.active {{
                color: #fff;
                background: rgba(0, 240, 255, 0.2);
                border: 1px solid rgba(0, 240, 255, 0.4);
            }}
            .omni-close-btn {{
                background: transparent;
                border: none;
                color: #a0aec0;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: color 0.2s;
                padding: 0;
            }}
            .omni-close-btn:hover {{
                color: #fff;
            }}
            #omni-chat-messages {{
                flex: 1;
                padding: 16px;
                overflow-y: auto;
                display: flex;
                flex-direction: column;
                gap: 16px;
                font-size: 13px;
            }}
            .omni-msg-row {{
                display: flex;
                gap: 12px;
            }}
            .omni-msg-row.user {{
                flex-direction: row-reverse;
            }}
            .omni-msg-bubble {{
                border-radius: 8px;
                padding: 12px;
                max-width: 80%;
                line-height: 1.5;
                border: 1px solid rgba(255, 255, 255, 0.1);
                background: rgba(255, 255, 255, 0.04);
                color: #e2e8f0;
            }}
            .omni-msg-row.user .omni-msg-bubble {{
                background: rgba(181, 95, 230, 0.15);
                border-color: rgba(181, 95, 230, 0.25);
                color: #fff;
                border-top-right-radius: 0;
            }}
            .omni-msg-row.bot .omni-msg-bubble {{
                border-top-left-radius: 0;
            }}
            .omni-msg-author {{
                font-size: 10px;
                font-weight: 700;
                letter-spacing: 0.1em;
                font-family: 'JetBrains Mono', monospace;
                margin-bottom: 4px;
                color: #fff;
            }}
            .omni-input-area {{
                padding: 12px;
                border-top: 1px solid rgba(255, 255, 255, 0.1);
                background: rgba(0, 0, 0, 0.4);
                flex-shrink: 0;
            }}
            .omni-form {{
                display: flex;
                gap: 8px;
            }}
            #omni-chat-input {{
                flex: 1;
                background: rgba(0, 0, 0, 0.5);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 13px;
                color: #fff;
                outline: none;
                transition: border-color 0.2s;
            }}
            #omni-chat-input:focus {{
                border-color: rgba(0, 240, 255, 0.4);
            }}
            .omni-send-btn {{
                width: 36px;
                height: 36px;
                border-radius: 6px;
                border: 1px solid rgba(0, 240, 255, 0.3);
                background: rgba(0, 240, 255, 0.1);
                color: #00f0ff;
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                transition: all 0.2s;
                padding: 0;
            }}
            .omni-send-btn:hover {{
                background: #00f0ff;
                color: #000;
            }}
            #omni-chat-loading {{
                padding: 0 16px 12px;
                display: none;
                align-items: center;
                gap: 8px;
                font-size: 10px;
                font-family: 'JetBrains Mono', monospace;
                color: #00f0ff;
            }}
            #omni-chat-loading.show {{
                display: flex;
            }}
            .rotate-spin {{
                animation: omni-spin 1s linear infinite;
            }}
            @keyframes omni-spin {{
                from {{ transform: rotate(0deg); }}
                to {{ transform: rotate(360deg); }}
            }}
            .terminal-scroll::-webkit-scrollbar {{
                width: 4px;
            }}
            .terminal-scroll::-webkit-scrollbar-track {{
                background: rgba(255,255,255,0.01);
            }}
            .terminal-scroll::-webkit-scrollbar-thumb {{
                background: rgba(0,240,255,0.2);
                border-radius: 2px;
            }}
        </style>
        
        <!-- Chat Window -->
        <div id="omni-chat-window">
            <!-- Header -->
            <div class="omni-header">
                <div class="omni-header-title">
                    <div class="omni-header-dot"></div>
                    <span class="omni-header-text">OMNI-ASSISTANT</span>
                </div>
                <div class="omni-header-controls">
                    <div class="omni-lang-pill">
                        <button id="omni-lang-bg" class="omni-lang-btn active">BG</button>
                        <button id="omni-lang-en" class="omni-lang-btn">EN</button>
                    </div>
                    <button id="omni-close-btn" class="omni-close-btn">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>
                    </button>
                </div>
            </div>
            
            <!-- Messages Area -->
            <div id="omni-chat-messages" class="terminal-scroll">
                <!-- Initial System Message will be injected by JS -->
            </div>

            <!-- Loading Indicator -->
            <div id="omni-chat-loading">
                <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="rotate-spin"><line x1="12" x2="12" y1="2" y2="6"/><line x1="12" x2="12" y1="18" y2="22"/><line x1="4.93" x2="7.76" y1="4.93" y2="7.76"/><line x1="16.24" x2="19.07" y1="16.24" y2="19.07"/><line x1="2" x2="6" y1="12" y2="12"/><line x1="18" x2="22" y1="12" y2="12"/><line x1="4.93" x2="7.76" y1="19.07" y2="16.24"/><line x1="16.24" x2="19.07" y1="7.76" y2="4.93"/></svg>
                PROCESSING SYNAPSES...
            </div>
            
            <!-- Input Area -->
            <div class="omni-input-area">
                <form id="omni-chat-form" class="omni-form">
                    <input type="text" id="omni-chat-input" placeholder="Задай въпрос за системата..." autocomplete="off">
                    <button type="submit" class="omni-send-btn">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m22 2-7 20-4-9-9-4Z"/><path d="M22 2 11 13"/></svg>
                    </button>
                </form>
            </div>
        </div>

        <!-- Toggle Button -->
        <button id="omni-toggle-btn">
            <div class="ping-ring"></div>
            
            <!-- AETERNA Purple Glowing Logo -->
            <svg id="omni-icon-bot" style="width: 32px; height: 32px; transition: transform 0.5s;" viewBox="0 0 100 100">
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
            
            <svg id="omni-icon-msg" style="display: none;" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
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
                iconBot.style.display = 'none';
                iconMsg.style.display = 'block';
            }});
            toggleBtn.addEventListener('mouseleave', () => {{
                iconBot.style.display = 'block';
                iconMsg.style.display = 'none';
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
                msgDiv.className = 'omni-msg-row bot';
                
                const iconHtml = '<div class="w-6 h-6 rounded flex items-center justify-center shrink-0" style="background: rgba(181, 95, 230, 0.1); border: 1px solid rgba(181, 95, 230, 0.2); display: flex; align-items: center; justify-content: center; width: 24px; height: 24px; border-radius: 4px; flex-shrink: 0;"><svg style="width: 16px; height: 16px;" viewBox="0 0 100 100"><defs><linearGradient id="purpleGlow-mini" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#b55fe6" /><stop offset="100%" stop-color="#ff2a85" /></linearGradient></defs><rect x="26" y="26" width="48" height="48" rx="10" fill="none" stroke="#b55fe6" stroke-width="4" transform="rotate(45 50 50)" /><rect x="32" y="32" width="36" height="36" rx="8" fill="url(#purpleGlow-mini)" transform="rotate(45 50 50)" /><circle cx="50" cy="50" r="5" fill="#ffffff" /></svg></div>';

                const contentHtml = `
                    <div class="omni-msg-bubble">
                        <div class="omni-msg-author">AETERNA.AIC</div>
                        <div style="white-space: pre-wrap;">${{welcomeMessages[currentLang]}}</div>
                    </div>
                `;

                msgDiv.innerHTML = iconHtml + contentHtml;
                chatMessages.appendChild(msgDiv);
            }}

            renderWelcomeMessage();

            langBgBtn.addEventListener('click', () => {{
                currentLang = 'bg';
                langBgBtn.classList.add('active');
                langEnBtn.classList.remove('active');
                chatInput.placeholder = "Задай въпрос за системата...";
                renderWelcomeMessage();
                conversationHistory = [];
            }});

            langEnBtn.addEventListener('click', () => {{
                currentLang = 'en';
                langEnBtn.classList.add('active');
                langBgBtn.classList.remove('active');
                chatInput.placeholder = "Ask about the architecture...";
                renderWelcomeMessage();
                conversationHistory = [];
            }});

            function toggleChat() {{
                isChatOpen = !isChatOpen;
                if (isChatOpen) {{
                    chatWindow.classList.add('open');
                    setTimeout(() => chatInput.focus(), 300);
                }} else {{
                    chatWindow.classList.remove('open');
                }}
            }}

            toggleBtn.addEventListener('click', toggleChat);
            closeBtn.addEventListener('click', toggleChat);

            function appendMessage(text, isUser = false) {{
                const msgDiv = document.createElement('div');
                msgDiv.className = 'omni-msg-row' + (isUser ? ' user' : ' bot');
                
                let iconHtml = '';
                if (isUser) {{
                    iconHtml = '<div class="w-6 h-6 rounded flex items-center justify-center shrink-0" style="background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); display: flex; align-items: center; justify-content: center; width: 24px; height: 24px; border-radius: 4px; flex-shrink: 0;"><svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg></div>';
                }} else {{
                    iconHtml = '<div class="w-6 h-6 rounded flex items-center justify-center shrink-0" style="background: rgba(181, 95, 230, 0.1); border: 1px solid rgba(181, 95, 230, 0.2); display: flex; align-items: center; justify-content: center; width: 24px; height: 24px; border-radius: 4px; flex-shrink: 0;"><svg style="width: 16px; height: 16px;" viewBox="0 0 100 100"><defs><linearGradient id="purpleGlow-mini2" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#b55fe6" /><stop offset="100%" stop-color="#ff2a85" /></linearGradient></defs><rect x="26" y="26" width="48" height="48" rx="10" fill="none" stroke="#b55fe6" stroke-width="4" transform="rotate(45 50 50)" /><rect x="32" y="32" width="36" height="36" rx="8" fill="url(#purpleGlow-mini2)" transform="rotate(45 50 50)" /><circle cx="50" cy="50" r="5" fill="#ffffff" /></svg></div>';
                }}

                const formattedText = text.replace(/\\*\\*(.*?)\\*\\*/g, '<strong>$1</strong>').replace(/\\n/g, '<br>');

                const contentHtml = `
                    <div class="omni-msg-bubble">
                        ${{!isUser ? '<div class="omni-msg-author">AETERNA.AIC</div>' : ''}}
                        <div style="white-space: pre-wrap;">${{formattedText}}</div>
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
                loadingIndicator.classList.add('show');
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
                    const response = await fetch('https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent', {{
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
                    loadingIndicator.classList.remove('show');
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
            new_content = content.replace('</body>', chunk + '\n</body>')
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"✅ Injected context-aware assistant into {filename}")
        else:
            print(f"❌ </body> tag not found in {filename}")
    except Exception as e:
        print(f"❌ Error processing {os.path.basename(filepath)}: {e}")

if __name__ == "__main__":
    directory = "Z:\\aeterna.website"
    files = glob.glob(os.path.join(directory, "*.html"))
    for file in files:
        inject_to_file(file)
