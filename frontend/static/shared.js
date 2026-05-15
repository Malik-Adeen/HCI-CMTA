/**
 * shared.js — loaded on every page
 * Handles: language persistence, font size persistence, back-to-top, AI chat widget
 */

const CMTA = {

  // ── Language ──────────────────────────────────────────────────────
  getLang() { return localStorage.getItem('cmta-lang') || 'en'; },
  setLang(lang) { localStorage.setItem('cmta-lang', lang); },

  applyLang(lang) {
    const isUrdu = lang === 'ur';
    document.documentElement.lang = isUrdu ? 'ur' : 'en';
    document.documentElement.dir = isUrdu ? 'rtl' : 'ltr';
    document.body.classList.toggle('font-urdu', isUrdu);

    // Swap all elements that have data-en / data-ur attributes
    // Use textContent for plain text, but if the attribute contains markup
    // (e.g. nested <span> used in some footer strings) use innerHTML so
    // the markup is rendered instead of shown escaped in the UI.
    document.querySelectorAll('[data-en]').forEach(el => {
      const raw = isUrdu ? (el.dataset.ur || el.dataset.en) : el.dataset.en;
      if (raw && /<[^>]+>/.test(raw)) {
        el.innerHTML = raw;
      } else {
        el.textContent = raw;
      }
    });
    
    // Update placeholders if present
    document.querySelectorAll('[data-en-placeholder]').forEach(el => {
      el.placeholder = isUrdu ? (el.dataset.urPlaceholder || el.dataset.enPlaceholder) : el.dataset.enPlaceholder;
    });

    // Update toggle button label
    const btn = document.getElementById('lang-toggle');
    if (btn) btn.textContent = isUrdu ? 'English' : 'اردو';
  },

  toggleLang() {
    const next = this.getLang() === 'en' ? 'ur' : 'en';
    this.setLang(next);
    this.applyLang(next);
  },

  // ── Font size ─────────────────────────────────────────────────────
  getFontSize() { return parseInt(localStorage.getItem('cmta-font') || '16'); },

  applyFontSize(size) {
    document.documentElement.style.fontSize = size + 'px';
    localStorage.setItem('cmta-font', size);
  },

  changeFont(delta) {
    const next = Math.min(22, Math.max(14, this.getFontSize() + delta));
    this.applyFontSize(next);
  },

  // ── Init (called on DOMContentLoaded) ────────────────────────────
  init() {
    this.applyLang(this.getLang());
    this.applyFontSize(this.getFontSize());

    // Wire font buttons if present
    const dec = document.getElementById('font-dec');
    const inc = document.getElementById('font-inc');
    if (dec) dec.onclick = () => CMTA.changeFont(-1);
    if (inc) inc.onclick = () => CMTA.changeFont(1);

    // Wire lang toggle if present
    const lt = document.getElementById('lang-toggle');
    if (lt) lt.onclick = () => CMTA.toggleLang();

    // Back to top
    const backTop = document.getElementById('back-top');
    if (backTop) {
      window.addEventListener('scroll', () => {
        const show = window.scrollY > 400;
        backTop.style.opacity      = show ? '1' : '0';
        backTop.style.pointerEvents = show ? 'auto' : 'none';
      });
    }

    // ── PWA Service Worker ──────────────────────────────────────────
    if ('serviceWorker' in navigator) {
      window.addEventListener('load', () => {
        navigator.serviceWorker.register('/service-worker.js')
          .then(reg => console.log('[CMTA SW] Registered, scope:', reg.scope))
          .catch(err => console.warn('[CMTA SW] Registration failed:', err));
      });
    }

    // ── PWA Install Prompt (Android A2HS banner) ────────────────────
    let deferredPrompt = null;
    window.addEventListener('beforeinstallprompt', e => {
      e.preventDefault();
      deferredPrompt = e;
      const banner = document.getElementById('pwa-install-banner');
      if (banner) banner.classList.remove('hidden');
    });
    window.addEventListener('appinstalled', () => {
      deferredPrompt = null;
      const banner = document.getElementById('pwa-install-banner');
      if (banner) banner.classList.add('hidden');
    });
    // Expose so inline onclick can trigger it
    window.cmtaInstallApp = () => {
      if (!deferredPrompt) return;
      deferredPrompt.prompt();
      deferredPrompt.userChoice.then(() => { deferredPrompt = null; });
    };
  }
};

document.addEventListener('DOMContentLoaded', () => CMTA.init());

// Global wrappers so inline onclick="toggleLang()" and onclick="changeFont(n)" work on every page
window.toggleLang  = () => CMTA.toggleLang();
window.changeFont  = (d) => CMTA.changeFont(d);
