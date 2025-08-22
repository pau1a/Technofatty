(function() {
  const body = document.body;
  const enabled = body.dataset.analyticsEnabled === 'true';
  if (!enabled) return;

  const provider = body.dataset.analyticsProvider;
  const siteId = body.dataset.analyticsSiteId;
  const consentRequired = body.dataset.consentRequired === 'true';

  function hasConsent() {
    if (!consentRequired) return true;
    return document.cookie.split(';').some(c => c.trim() === 'analytics_consent=true');
  }

  function dispatch(eventName, meta) {
    if (!hasConsent()) return;
    meta = meta || {};
    if (provider === 'plausible' && typeof window.plausible === 'function') {
      window.plausible(eventName, {props: meta});
    } else if (provider === 'ga4' && typeof window.gtag === 'function') {
      window.gtag('event', eventName, meta);
    }
  }

  if (provider === 'ga4' && typeof window.gtag === 'function') {
    window.dataLayer = window.dataLayer || [];
    window.gtag('js', new Date());
    window.gtag('config', siteId);
  }

  const fired = new Set();

  function handle(el) {
    const name = el.dataset.analyticsEvent;
    if (!name) return false;
    const metaAttr = el.dataset.analyticsMeta;
    let meta = {};
    if (metaAttr) {
      try { meta = JSON.parse(metaAttr); } catch (e) {}
    }
    dispatch(name, meta);
    return true;
  }

  document.addEventListener('click', e => {
    let el = e.target;
    while (el && el !== document) {
      if (handle(el)) break;
      el = el.parentElement;
    }
  });

  document.addEventListener('submit', e => {
    const el = e.target;
    if (el.dataset.analyticsEvent) {
      if (el.checkValidity && !el.checkValidity()) return;
      handle(el);
    }
  });

  document.addEventListener('focusin', e => {
    let el = e.target;
    while (el && el !== document) {
      const name = el.dataset.analyticsEvent;
      if (name) {
        if (fired.has(name)) break;
        fired.add(name);
        handle(el);
        break;
      }
      el = el.parentElement;
    }
  });
})();
