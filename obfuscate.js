import fs from 'fs';
import path from 'path';
import * as cheerio from 'cheerio';
import JavaScriptObfuscator from 'javascript-obfuscator';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const TARGET_DIR = __dirname;
// We'll output to a dist folder, or overwrite in place? 
// In-place overwrite is requested since we want the repo to contain ONLY compiled files.
// But first, we need to make sure we don't obfuscate node_modules, .git, etc.
const IGNORED_DIRS = ['node_modules', '.git', 'tests', 'dist', 'soul'];

const obfuscatorOptions = {
    compact: true,
    controlFlowFlattening: true,
    controlFlowFlatteningThreshold: 0.75,
    deadCodeInjection: true,
    deadCodeInjectionThreshold: 0.4,
    debugProtection: true,
    debugProtectionInterval: 2000,
    disableConsoleOutput: true,
    identifierNamesGenerator: 'hexadecimal',
    log: false,
    numbersToExpressions: true,
    renameGlobals: false,
    selfDefending: true,
    simplify: true,
    splitStrings: true,
    splitStringsChunkLength: 10,
    stringArray: true,
    stringArrayCallsTransform: true,
    stringArrayCallsTransformThreshold: 0.5,
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

function processFile(filePath) {
    const ext = path.extname(filePath);
    if (ext === '.js') {
        if (filePath.endsWith('obfuscate.js') || filePath.endsWith('playwright.config.ts')) return;
        const code = fs.readFileSync(filePath, 'utf-8');
        try {
            const obfuscated = JavaScriptObfuscator.obfuscate(code, obfuscatorOptions).getObfuscatedCode();
            fs.writeFileSync(filePath, obfuscated, 'utf-8');
            console.log(`[JS] Obfuscated: ${filePath}`);
        } catch (e) {
            console.error(`[JS] Failed to obfuscate ${filePath}:`, e.message);
        }
    } else if (ext === '.html') {
        const html = fs.readFileSync(filePath, 'utf-8');
        const $ = cheerio.load(html);
        let modified = false;

        $('script').each((i, el) => {
            const src = $(el).attr('src');
            // Only process inline scripts (no src) or local scripts? Wait, if we process .js files anyway,
            // we only need to process inline scripts here.
            if (!src) {
                const code = $(el).html();
                if (code && code.trim().length > 0) {
                    try {
                        const obfuscated = JavaScriptObfuscator.obfuscate(code, obfuscatorOptions).getObfuscatedCode();
                        $(el).html(`\n${obfuscated}\n`);
                        modified = true;
                    } catch (e) {
                        console.error(`[HTML] Failed to obfuscate inline script in ${filePath}:`, e.message);
                    }
                }
            }
        });

        if (modified) {
            fs.writeFileSync(filePath, $.html(), 'utf-8');
            console.log(`[HTML] Obfuscated inline scripts: ${filePath}`);
        }
    }
}

function walkDir(dir) {
    const files = fs.readdirSync(dir);
    for (const file of files) {
        const fullPath = path.join(dir, file);
        if (fs.statSync(fullPath).isDirectory()) {
            if (!IGNORED_DIRS.includes(file)) {
                walkDir(fullPath);
            }
        } else {
            processFile(fullPath);
        }
    }
}

console.log('Starting repository obfuscation...');
walkDir(TARGET_DIR);
console.log('Obfuscation complete.');
