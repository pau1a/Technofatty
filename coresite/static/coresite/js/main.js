document.addEventListener('DOMContentLoaded', function () {
  const menuOverlay = document.querySelector('.menu-overlay');
  const hamburgerBtn = document.querySelector('.hamburger-btn');
  const closeBtn = document.querySelector('.menu-overlay__close');
  const backdrop = document.querySelector('.menu-backdrop');
  const focusableSelectors = 'a, button';
  let firstFocusable = null;
  let lastFocusable = null;

  function trapFocus(e) {
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
      closeMenu();
      hamburgerBtn.focus();
    }
  }

  function openMenu() {
    menuOverlay.classList.add('is-open');
    backdrop.classList.add('is-active');
    menuOverlay.setAttribute('aria-hidden', 'false');
    hamburgerBtn.setAttribute('aria-expanded', 'true');
    const focusables = menuOverlay.querySelectorAll(focusableSelectors);
    if (focusables.length) {
      [firstFocusable] = focusables;
      lastFocusable = focusables[focusables.length - 1];
      firstFocusable.focus();
    }
    menuOverlay.addEventListener('keydown', trapFocus);
  }

  function closeMenu() {
    menuOverlay.classList.remove('is-open');
    backdrop.classList.remove('is-active');
    menuOverlay.setAttribute('aria-hidden', 'true');
    hamburgerBtn.setAttribute('aria-expanded', 'false');
    menuOverlay.removeEventListener('keydown', trapFocus);
    hamburgerBtn.focus();
  }

  if (hamburgerBtn && menuOverlay) {
    hamburgerBtn.addEventListener('click', openMenu);
  }

  if (closeBtn && menuOverlay) {
    closeBtn.addEventListener('click', closeMenu);
  }

  if (backdrop) {
    backdrop.addEventListener('click', closeMenu);
  }

  const newsletterForm = document.getElementById('newsletter_form');
  if (newsletterForm) {
    const submitBtn = newsletterForm.querySelector('button[type="submit"]');

    const setState = (state) => {
      newsletterForm.classList.remove('is-success', 'is-error', 'is-busy');
      if (state) { newsletterForm.classList.add(`is-${state}`); }

      const busy = state === 'busy';
      newsletterForm.setAttribute('aria-busy', busy ? 'true' : 'false');
      if (busy) { newsletterForm.setAttribute('aria-disabled', 'true'); }
      else { newsletterForm.removeAttribute('aria-disabled'); }

      if (submitBtn) { submitBtn.disabled = busy; }
    };

    newsletterForm.addEventListener('submit', function () {
      setState('busy');
    });

    newsletterForm.addEventListener('newsletter:success', () => setState('success'));
    newsletterForm.addEventListener('newsletter:error', () => setState('error'));
    window.addEventListener('pageshow', () => setState());
  }

  // Sticky Header with Opacity Transition
  const header = document.querySelector('.site-header');
  const scrollThresholdForFullOpacity = 200; // Scroll distance in pixels for full opacity
  if (header) {
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    let lastScrollY = 0;
    let hasReachedFullOpacity = prefersReducedMotion;
    let ticking = false;

    const updateHeader = () => {
      const scrollY = lastScrollY;

      if (prefersReducedMotion) {
        header.style.setProperty('--header-bg-opacity', '1');
      } else if (!hasReachedFullOpacity) {
        let opacity = 0.5;
        if (scrollY > 0) {
          const progress = Math.min(1, scrollY / scrollThresholdForFullOpacity);
          opacity = 0.5 + (0.5 * progress);
        }
        header.style.setProperty('--header-bg-opacity', opacity.toFixed(2));
        if (opacity >= 1) { hasReachedFullOpacity = true; }
      }

      if (scrollY > 0) { header.classList.add('is-sticky'); }
      else { header.classList.remove('is-sticky'); }

      ticking = false;
    };

    window.addEventListener('scroll', () => {
      lastScrollY = window.scrollY;
      if (!ticking) {
        requestAnimationFrame(updateHeader);
        ticking = true;
      }
    });

    lastScrollY = window.scrollY;
    updateHeader();
  }

  /**
   * Handles the hero video fade-in to ensure the placeholder image is the LCP.
   * This script looks for a placeholder image and a video. If found, it waits for
   * the video to be ready and for a minimum delay, then smoothly fades the video in.
   */
  function initHeroVideoSwap() {
    const video = document.querySelector('.hero__video');
    const placeholder = document.querySelector('.hero__placeholder');

    // Exit if the required hero elements aren't on this page
    if (!video || !placeholder) {
      return;
    }

    let videoReady = false;
    let minDelayDone = false;

    const trySwap = () => {
      // Check if swap can happen and hasn't already
      if (videoReady && minDelayDone && video.classList.contains('is-loading')) {
        
        // Make video renderable by removing the loading class and attributes
        video.classList.remove('is-loading');
        video.removeAttribute('inert');
        video.removeAttribute('aria-hidden');

        // Use requestAnimationFrame to ensure the 'display' change is painted
        // before we trigger the opacity transition for a smooth fade.
        requestAnimationFrame(() => {
          placeholder.style.opacity = '0';
          video.style.opacity = '1';
        });
      }
    };

    // Listen for when the video is ready to play through
    video.addEventListener('canplaythrough', () => { videoReady = true; trySwap(); }, { once: true });

    // Enforce a minimum 2-second delay to ensure a fast LCP paint
    setTimeout(() => { minDelayDone = true; trySwap(); }, 2000);
  }

  // Initialize the hero video swap logic
  initHeroVideoSwap();
});
