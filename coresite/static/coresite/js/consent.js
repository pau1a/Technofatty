"use strict";

document.addEventListener('DOMContentLoaded', () => {
  const banner = document.querySelector('[data-consent-banner]');
  const body = document.body;
  if (!banner || !body) return;

  const required = body.dataset.consentRequired === 'true';
  const granted = body.dataset.consentGranted === 'true';
  if (!required || granted) return;

  // Accessibility attributes and reveal
  banner.removeAttribute('hidden');
  banner.setAttribute('role', 'dialog');
  banner.setAttribute('aria-modal', 'true');
  banner.setAttribute('aria-hidden', 'false');

  const focusableSelectors = 'a, button';
  const focusables = banner.querySelectorAll(focusableSelectors);
  const firstFocusable = focusables[0];
  const lastFocusable = focusables[focusables.length - 1];
  let previousFocus = document.activeElement;
  if (firstFocusable) firstFocusable.focus();

  function trapFocus(e) {
    if (!firstFocusable || !lastFocusable) return;
    if (e.key === 'Tab') {
      if (e.shiftKey) {
        if (document.activeElement === firstFocusable) {
          e.preventDefault();
          lastFocusable.focus();
        }
      } else {
        if (document.activeElement === lastFocusable) {
          e.preventDefault();
          firstFocusable.focus();
        }
      }
    } else if (e.key === 'Escape') {
      setConsent('rejected');
    }
  }

  banner.addEventListener('keydown', trapFocus);

  function hideBanner() {
    banner.setAttribute('hidden', '');
    banner.setAttribute('aria-hidden', 'true');
    banner.removeEventListener('keydown', trapFocus);
    if (previousFocus) previousFocus.focus();
  }

  function setConsent(state) {
    const name = body.dataset.consentCookieName || 'tf_consent';
    const maxAge = parseInt(body.dataset.consentCookieMaxAge, 10) || 0;
    const samesite = body.dataset.consentCookieSamesite || 'Lax';
    const secure = body.dataset.consentCookieSecure === 'true';

    let cookie = `${encodeURIComponent(name)}=${encodeURIComponent(state)}; Max-Age=${maxAge}; Path=/; SameSite=${samesite}`;
    if (secure) cookie += '; Secure';
    document.cookie = cookie;

    try {
      window.localStorage.setItem(name, state);
    } catch (err) {
      /* ignore */
    }

    body.dataset.consentGranted = 'true';
    hideBanner();
  }

  banner.querySelectorAll('[data-consent-choice]').forEach(btn => {
    btn.addEventListener('click', e => {
      e.preventDefault();
      const choice = btn.dataset.consentChoice === 'accept' ? 'accepted' : 'rejected';
      setConsent(choice);
    });
  });
});

