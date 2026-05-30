/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * UKAME MATRIX - SALES & LEADS INGESTION API
 * ═══════════════════════════════════════════════════════════════════════════════
 */

import { Router } from 'express';
import * as fs from 'fs';
import * as path from 'path';

const router = Router();
const DB_PATH = path.join(__dirname, '../../data/ukame_leads.json');

// Ensure DB exists
if (!fs.existsSync(DB_PATH)) {
    fs.mkdirSync(path.dirname(DB_PATH), { recursive: true });
    fs.writeFileSync(DB_PATH, JSON.stringify([]));
}

router.post('/submit-lead', async (req, res) => {
    try {
        const { area, floors, families, costUKAME, powerUKAME, contactEmail, contactPhone } = req.body;

        if (!contactEmail && !contactPhone) {
            return res.status(400).json({ error: 'Имейл или телефон са задължителни за оферта.' });
        }

        const newLead = {
            id: `UKAME-LEAD-${Date.now()}`,
            timestamp: new Date().toISOString(),
            parameters: { area: Number(area), floors: Number(floors), families: Number(families) },
            projections: { estimatedCostBGN: Number(costUKAME), targetPowerKW: Number(powerUKAME) },
            contact: { email: contactEmail || null, phone: contactPhone || null },
            status: 'NEW_OPPORTUNITY'
        };

        const dbData = JSON.parse(fs.readFileSync(DB_PATH, 'utf-8'));
        dbData.push(newLead);
        fs.writeFileSync(DB_PATH, JSON.stringify(dbData, null, 2));

        console.log(`[⚡ UKAME API] Нов Соларен Клиент Записан: ${newLead.id} за ${powerUKAME}kW`);

        res.json({ success: true, leadId: newLead.id, message: 'Инвестиционният профил е запазен. Екипът ни ще се свърже с вас.' });
    } catch (err) {
        console.error('[UKAME API Error]', err);
        res.status(500).json({ error: 'Грешка при запазване на заявката.' });
    }
});

router.get('/leads', (req, res) => {
    const dbData = JSON.parse(fs.readFileSync(DB_PATH, 'utf-8'));
    res.json(dbData);
});

export default router;