import { Page, Locator, expect } from '@playwright/test';

// Complexity: O(1)
export class ClinicalPortalPage {
  readonly page: Page;
  readonly languageSelect: Locator;
  readonly conditionSelect: Locator;
  readonly simulateButton: Locator;
  readonly patientNameInput: Locator;
  readonly exportPdfButton: Locator;
  readonly fhirExportButton: Locator;
  readonly dynamicRecipeList: Locator;
  readonly canvasLabel: Locator;

  constructor(page: Page) {
    this.page = page;
    // Real DOM Selectors from CLINICAL_DOCTOR_PORTAL.html
    this.languageSelect = page.locator('#langSelect');
    this.conditionSelect = page.locator('#geneMutation');
    this.simulateButton = page.locator('#simBtn, button[type="submit"]');
    this.patientNameInput = page.locator('#patientId');
    this.exportPdfButton = page.locator('button:has-text("PDF")');
    this.fhirExportButton = page.locator('button:has-text("FHIR")');
    this.dynamicRecipeList = page.locator('#drugRecommendations');
    this.canvasLabel = page.locator('#timelineWeekLabel');
  }

  async goto() {
    await this.page.goto('/CLINICAL_DOCTOR_PORTAL.html');
    await this.page.waitForLoadState('networkidle');
  }

  async selectLanguage(lang: string) {
    await this.languageSelect.waitFor({ state: 'visible' });
    const previousState = await this.languageSelect.inputValue();
    await this.languageSelect.selectOption(lang);
    const newState = await this.languageSelect.inputValue();
    expect(newState).toBe(lang);
  }

  async selectCondition(condition: string) {
    await this.conditionSelect.waitFor({ state: 'visible' });
    await this.conditionSelect.selectOption(condition);
  }

  async runSimulation() {
    await this.simulateButton.waitFor({ state: 'visible' });
    await this.simulateButton.click();
    // Hybrid Verification - wait for result to be visible
    await this.dynamicRecipeList.waitFor({ state: 'visible' });
  }

  async getRecipeListText() {
    return this.dynamicRecipeList.innerText();
  }
}
