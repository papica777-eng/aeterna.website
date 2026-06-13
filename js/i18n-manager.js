/**
 * AETERNA i18n Manager v2.0
 * Unified localization system for all HUD modules
 * Supports BG/EN dynamic language switching
 */

class AeternaI18n {
  constructor(defaultLang = 'bg') {
    this.currentLang = defaultLang;
    this.translations = {};
    this.translationCache = new Map();
  }

  /**
   * Load translations from JSON source
   */
  async loadTranslations(jsonPath) {
    try {
      const response = await fetch(jsonPath);
      this.translations = await response.json();
      return true;
    } catch (e) {
      console.warn('Failed to load translations from ' + jsonPath);
      return false;
    }
  }

  /**
   * Register inline translations (for module-specific strings)
   */
  registerTranslations(moduleTranslations) {
    this.translations = { ...this.translations, ...moduleTranslations };
  }

  /**
   * Get translation key with fallback
   */
  t(key, fallback = key) {
    if (this.translationCache.has(key)) {
      return this.translationCache.get(key);
    }

    const translation = this.translations[this.currentLang]?.[key] || fallback;
    this.translationCache.set(key, translation);
    return translation;
  }

  /**
   * Set current language and re-render UI
   */
  setLanguage(langCode) {
    if (this.translations[langCode]) {
      this.currentLang = langCode;
      this.translationCache.clear();
      
      // Update HTML lang attribute
      document.documentElement.lang = langCode;
      
      // Update all data-i18n elements
      document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        const translated = this.t(key);
        
        // Preserve HTML structure if needed
        if (el.hasAttribute('data-i18n-html')) {
          el.innerHTML = translated;
        } else {
          el.textContent = translated;
        }
      });
      
      // Update language button states
      document.querySelectorAll('[data-lang-btn]').forEach(btn => {
        btn.classList.toggle('active', btn.getAttribute('data-lang-btn') === langCode);
      });
      
      // Trigger custom event for module-specific updates
      window.dispatchEvent(new CustomEvent('i18n-changed', { detail: { lang: langCode } }));
      
      return true;
    }
    return false;
  }

  /**
   * Get current language code
   */
  getCurrentLanguage() {
    return this.currentLang;
  }

  /**
   * Get all available languages
   */
  getAvailableLanguages() {
    return Object.keys(this.translations);
  }
}

// Global instance
window.aeterna_i18n = new AeternaI18n();
