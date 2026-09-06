import fs from 'fs';
import path from 'path';

const baseDir = 'c:/Users/papic/AETERNA-PLATFORM/aeterna.website';
const files = fs.readdirSync(baseDir).filter(f => f.endsWith('.html'));

const candidates = [];

for (const file of files) {
    const content = fs.readFileSync(path.join(baseDir, file), 'utf8');
    const hasGate = content.includes('aeternaLicenseModal');
    const calcMatches = content.match(/onclick=["'][^"']*(?:simulate|execute|run|calc|compute|solve|trigger)[^"']*["']/gi) || [];
    const isHud = /hud/i.test(file);
    const isVht = /vht/i.test(file);

    if (calcMatches.length > 0 || isHud || isVht) {
        candidates.push({
            file,
            hasGate,
            calcMatchesCount: calcMatches.length,
            isHud,
            isVht,
            sample: calcMatches.slice(0, 4)
        });
    }
}
console.log(JSON.stringify(candidates, null, 2));
