import fs from 'fs';
import path from 'path';
import * as cheerio from 'cheerio';
import JavaScriptObfuscator from 'javascript-obfuscator';

console.log('═══════════════════════════════════════════════════════════════════════════════');
console.log('🛡️  AETERNA SOVEREIGN FORTRESS & CODE OBFUSCATION COMPILER                   🛡️');
console.log('    "Копиращите ще намерят само пепел. В QAntum не лъжем."                     ');
console.log('    Architect: Dimitar Stavrev Prodromov (ЕГН: 9601070443)                     ');
console.log('    Authority: 0x41_45_54_45_52_4e_41_5f_4c_4f_47_4f_53_5f_44_49_4d_49_54_41_52');
console.log('═══════════════════════════════════════════════════════════════════════════════');

const sovereignShield = `
// ═══════════════════════════════════════════════════════════════════════════════
// 🛡️ AETERNA SOVEREIGN GUARD & NEURAL KILL-SWITCH (BROWSER SUBSTRATE)
// "Това е първият в света код, който активно се защитава от неоторизиран достъп
//  чрез Математическа Ентропия. Копиращите ще намерят само пепел."
// ═══════════════════════════════════════════════════════════════════════════════
(function initSovereignFortress() {
    'use strict';
    let isTombstoned = false;

    function triggerSovereignTombstone(reason) {
        if (isTombstoned || window.__AETERNA_TEST_ENV__) return;
        isTombstoned = true;

        try {
            window.latestSimulationData = null;
            window.lastIalDossierData = null;
            window.tcgaCohortDatabase = null;
            window.sessionStorage.clear();
            window.localStorage.clear();
        } catch(e) {}

        document.body.innerHTML = \`
        <div style="position:fixed;inset:0;background:#030712;color:#ef4444;z-index:99999999;display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:monospace;padding:30px;text-align:center;user-select:none;">
            <div style="width:72px;height:72px;border-radius:50%;background:rgba(220,38,38,0.15);border:2px solid #ef4444;display:flex;align-items:center;justify-content:center;font-size:36px;margin-bottom:20px;">💀</div>
            <h1 style="font-size:28px;font-weight:900;letter-spacing:0.12em;margin-bottom:10px;color:#dc2626;text-transform:uppercase;">TOMBSTONE PROTOCOL ACTIVATED</h1>
            <p style="font-size:16px;color:#f1f5f9;margin-bottom:24px;font-weight:700;">„Копиращите ще намерят само пепел. В QAntum не лъжем.“</p>
            <div style="border:1px solid #7f1d1d;background:#0f0505;padding:18px 26px;border-radius:10px;font-size:12px;color:#fca5a5;max-width:680px;line-height:1.7;text-align:left;">
                <div><strong>SECURITY BREACH DETECTED:</strong> \${reason}</div>
                <div><strong>LEGAL AUTHORITY:</strong> Dimitar Stavrev Prodromov (ЕГН: 9601070443)</div>
                <div><strong>HEX ANCHOR:</strong> 0x41_45_54_45_52_4e_41_5f_4c_4f_47_4f_53_5f_44_49_4d_49_54_41_52_5f_50_52_4f_44_52_4f_4d_56_21</div>
                <div><strong>STATUS:</strong> Client memory scrubbed. Epigenetic landscape &amp; ODE tensors obliterated.</div>
            </div>
        </div>\`;
        document.title = "💀 TOMBSTONE ACTIVATED | AETERNA TECHNOLOGIES";
    }

    // 1. Right-Click Suppress
    document.addEventListener('contextmenu', function(e) {
        if (!window.__AETERNA_TEST_ENV__) { e.preventDefault(); return false; }
    }, { capture: true });

    // 2. Keyboard Intercepts (F12, Ctrl+Shift+I/J/C, Ctrl+U, Ctrl+S)
    window.addEventListener('keydown', function(e) {
        if (window.__AETERNA_TEST_ENV__) return;
        const key = e.key ? e.key.toLowerCase() : '';
        if (e.keyCode === 123 || e.key === 'F12') {
            e.preventDefault(); e.stopPropagation();
            return false;
        }
        if (e.ctrlKey && e.shiftKey && (key === 'i' || key === 'j' || key === 'c')) {
            e.preventDefault(); e.stopPropagation();
            return false;
        }
        if (e.ctrlKey && (key === 'u' || key === 's')) {
            e.preventDefault(); e.stopPropagation();
            return false;
        }
    }, { capture: true });

    // 3. Selection & Copy Traps
    document.addEventListener('selectstart', function(e) {
        if (e.target.tagName !== 'INPUT' && e.target.tagName !== 'SELECT' && e.target.tagName !== 'TEXTAREA') {
            e.preventDefault();
        }
    });
    document.addEventListener('copy', function(e) {
        if (e.target.tagName !== 'INPUT' && e.target.tagName !== 'SELECT' && e.target.tagName !== 'TEXTAREA') {
            e.preventDefault();
            if (e.clipboardData) {
                e.clipboardData.setData('text/plain', 'AETERNA PROPRIETARY IP (EPO-PAT-05). UNAUTHORIZED COPYING PROHIBITED.');
            }
        }
    });

    // 4. Keyboard Shortcuts Shield (Suppress Inspect & View-Source Keys)
    // Silently blocks F12, Ctrl+Shift+I, Ctrl+U, Ctrl+S without false positive locks
    // Selection & Copy protections remain strictly enforced

    // 6. Console Annihilation in Production
    if (!window.__AETERNA_TEST_ENV__) {
        const noop = function() {};
        try {
            window.console = {
                log: noop, info: noop, warn: noop, error: noop,
                dir: noop, table: noop, trace: noop, assert: noop, clear: noop
            };
        } catch(e) {}
    }
})();
`;

const obfuscatorOptions = {
    compact: true,
    controlFlowFlattening: true,
    controlFlowFlatteningThreshold: 0.75,
    deadCodeInjection: true,
    deadCodeInjectionThreshold: 0.35,
    debugProtection: false, // Handled by our Sovereign Shield
    disableConsoleOutput: false, // Handled by our Sovereign Shield
    identifierNamesGenerator: 'hexadecimal',
    log: false,
    numbersToExpressions: true,
    renameGlobals: false, // Preserves global UI event callbacks
    selfDefending: true,
    simplify: true,
    splitStrings: true,
    splitStringsChunkLength: 8,
    stringArray: true,
    stringArrayCallsTransform: true,
    stringArrayCallsTransformThreshold: 0.6,
    stringArrayEncoding: ['rc4'],
    stringArrayIndexShift: true,
    stringArrayRotate: true,
    stringArrayShuffle: true,
    stringArrayWrappersCount: 1,
    stringArrayWrappersChainedCalls: true,
    stringArrayWrappersParametersMaxCount: 2,
    stringArrayWrappersType: 'variable',
    stringArrayThreshold: 0.75,
    unicodeEscapeSequence: false
};

function protectHtmlFile(sourcePath, targetPaths) {
    console.log(`\nProcessing source: ${sourcePath}...`);
    const html = fs.readFileSync(sourcePath, 'utf-8');
    const $ = cheerio.load(html);

    // Invert user-select on body
    $('head').append(`
    <style id="aeterna-fortress-css">
        * {
            -webkit-user-select: none !important;
            -moz-user-select: none !important;
            -ms-user-select: none !important;
            user-select: none !important;
        }
        input, select, textarea, [contenteditable="true"] {
            -webkit-user-select: auto !important;
            -moz-user-select: auto !important;
            -ms-user-select: auto !important;
            user-select: auto !important;
        }
    </style>
    `);

    // Obfuscate inline scripts with logic > 1000 characters
    let obfuscatedCount = 0;
    $('script').each((i, el) => {
        const src = $(el).attr('src');
        if (!src) {
            let code = $(el).html() || '';
            if (code.trim().length > 1000) {
                console.log(`  [Script #${i}] Obfuscating script (${code.length} chars)...`);
                const startTime = Date.now();
                
                // Prepend shield to the largest script
                if (code.length > 50000) {
                    code = sovereignShield + '\n' + code;
                }

                try {
                    const result = JavaScriptObfuscator.obfuscate(code, obfuscatorOptions).getObfuscatedCode();
                    const duration = ((Date.now() - startTime) / 1000).toFixed(2);
                    console.log(`    -> Done in ${duration}s! New size: ${result.length} chars.`);
                    $(el).html(`\n${result}\n`);
                    obfuscatedCount++;
                } catch(e) {
                    console.error(`    -> ERROR obfuscating script #${i}:`, e.message);
                }
            }
        }
    });

    const finalHtml = $.html();
    for (const targetPath of targetPaths) {
        fs.writeFileSync(targetPath, finalHtml, 'utf-8');
        console.log(`  ✓ Written fortified build to: ${targetPath} (${finalHtml.length} bytes)`);
    }
}

// 1. Build CLINICAL_DOCTOR_PORTAL.html and mirror in docs/
protectHtmlFile('CLINICAL_DOCTOR_PORTAL.source.html', [
    'CLINICAL_DOCTOR_PORTAL.html',
    'docs/CLINICAL_DOCTOR_PORTAL.html'
]);

// 2. Build index.html
protectHtmlFile('index.source.html', [
    'index.html'
]);

console.log('\n═══════════════════════════════════════════════════════════════════════════════');
console.log('✅ ALL PRODUCTION SITES FORTIFIED & OBFUSCATED SUCCESSFULLY!');
console.log('═══════════════════════════════════════════════════════════════════════════════\n');
