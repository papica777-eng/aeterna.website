import { test, expect } from '@playwright/test';
import { ClinicalPortalPage } from './pages/ClinicalPortalPage';

test.describe('Clinical Doctor Portal E2E Tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/CLINICAL_DOCTOR_PORTAL.html');
    await page.waitForLoadState('networkidle');
  });

  test('1. Preset loader updates patient form accurately', async ({ page }) => {
    const portalPage = new ClinicalPortalPage(page);
    
    // Click Glioblastoma preset button
    await page.click('button:has-text("Глиобластом (GBM)"), button:has-text("Glioblastoma (GBM)")');
    
    // Verify form values populated
    await expect(page.locator('#patientId')).toHaveValue('PT-GBM-4401');
    await expect(page.locator('#patientAge')).toHaveValue('58');
    await expect(page.locator('#geneMutation')).toHaveValue('TP53_LOSS');
    await expect(page.locator('#ki67')).toHaveValue('85');
    await expect(page.locator('#spo2')).toHaveValue('89');
    await expect(page.locator('#tumorSize')).toHaveValue('4.2');
  });

  test('2. Full simulation workflow and dynamic calculation verification', async ({ page }) => {
    const portalPage = new ClinicalPortalPage(page);
    
    // Select Pancreas preset and run simulation
    await page.click('button:has-text("Панкреас (PAAD)"), button:has-text("Pancreas (PAAD)")');
    await portalPage.runSimulation();

    // Verify results dashboard becomes visible
    await expect(page.locator('#resultsDashboard')).toBeVisible();

    // Verify dynamic KPI elements contain non-zero calculated numbers
    const survivalText = await page.locator('#resSurvival').innerText();
    expect(survivalText).toMatch(/\d+(\.\d+)?\s+(meseca|months|месеца)/i);

    const shrinkageText = await page.locator('#resShrinkage').innerText();
    expect(shrinkageText).toMatch(/-\d+\.\d+%/);

    const cindexText = await page.locator('#resCIndex').innerText();
    expect(parseFloat(cindexText)).toBeGreaterThan(95);

    // Verify Canvas visual element exists and timeline slider updates label
    await expect(page.locator('#tumorCanvas')).toBeVisible();
    await page.fill('#tumorTimeline', '24');
    await page.dispatchEvent('#tumorTimeline', 'input');
    await expect(page.locator('#timelineWeekLabel')).toContainText('24');
  });

  test('3. Language switching updates dynamic recipes and labels in real time', async ({ page }) => {
    const portalPage = new ClinicalPortalPage(page);

    await portalPage.selectCondition('KRAS_G12D');
    await portalPage.runSimulation();

    // BG default
    const bgText = await portalPage.getRecipeListText();
    expect(bgText).toContain('AMG-510');

    // EN switch
    await portalPage.selectLanguage('en');
    await page.waitForTimeout(200);
    const enText = await portalPage.getRecipeListText();
    expect(enText).toContain('inhibitor');

    // FR switch
    await portalPage.selectLanguage('fr');
    await page.waitForTimeout(200);
    const frText = await portalPage.getRecipeListText();
    expect(frText).toContain('Inhibiteur');

    // ES switch
    await portalPage.selectLanguage('es');
    await page.waitForTimeout(200);
    const esText = await portalPage.getRecipeListText();
    expect(esText).toContain('Inhibidor');
  });

  test('4. Export buttons trigger download handlers', async ({ page }) => {
    const portalPage = new ClinicalPortalPage(page);
    await portalPage.runSimulation();

    // Verify FHIR export download event triggers
    const fhirDownloadPromise = page.waitForEvent('download');
    await page.click('button:has-text("FHIR")');
    const fhirDownload = await fhirDownloadPromise;
    expect(fhirDownload.suggestedFilename()).toContain('.json');

    // Verify CSV export download event triggers
    const csvDownloadPromise = page.waitForEvent('download');
    await page.click('button:has-text("CSV"), button:has-text("Таблица")');
    const csvDownload = await csvDownloadPromise;
    expect(csvDownload.suggestedFilename()).toContain('.csv');

    // Verify TXT export download event triggers
    const txtDownloadPromise = page.waitForEvent('download');
    await page.click('button:has-text("EHR"), button:has-text("Текст")');
    const txtDownload = await txtDownloadPromise;
    expect(txtDownload.suggestedFilename()).toContain('.txt');
  });
});
