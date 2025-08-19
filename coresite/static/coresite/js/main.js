console.log("MAIN.JS LOADED FROM SERVER - START");

document.addEventListener('DOMContentLoaded', function () {
  console.log("DOMContentLoaded fired");
  const menuOverlay = document.querySelector('.menu-overlay');
  const hamburgerBtn = document.querySelector('.hamburger-btn');
  const closeBtn = document.querySelector('.menu-overlay__close');
  const backdrop = document.querySelector('.menu-backdrop');

  console.log("Script loaded", { menuOverlay, hamburgerBtn, closeBtn, backdrop });

  function openMenu() {
    menuOverlay.classList.add('is-open');
    backdrop.classList.add('is-active');
    menuOverlay.setAttribute('aria-hidden', 'false');
    hamburgerBtn.setAttribute('aria-expanded', 'true');
  }

  function closeMenu() {
    menuOverlay.classList.remove('is-open');
    backdrop.classList.remove('is-active');
    menuOverlay.setAttribute('aria-hidden', 'true');
    hamburgerBtn.setAttribute('aria-expanded', 'false');
  }

  if (hamburgerBtn && menuOverlay) {
    hamburgerBtn.addEventListener('click', function () {
      console.log("Hamburger clicked");
      openMenu();
    });
  }

  if (closeBtn && menuOverlay) {
    closeBtn.addEventListener('click', function () {
      console.log("Close clicked");
      closeMenu();
    });
  }

  if (backdrop) {
    backdrop.addEventListener('click', function () {
      console.log("Backdrop clicked");
      closeMenu();
    });
  }

  // Sticky Header with Opacity Transition
  const header = document.querySelector('.site-header');
  const scrollThresholdForFullOpacity = 200; // Scroll distance in pixels for full opacity
  let hasReachedFullOpacity = false; // Flag to keep opacity at 1 permanently

  console.log("Header element:", header);
  if (header) {
    window.addEventListener('scroll', function() {
      const scrollY = window.scrollY;

      if (hasReachedFullOpacity) {
        // If already fully opaque, maintain opacity 1 and manage 'is-sticky' class
        header.style.setProperty('--header-bg-opacity', '1');
        if (scrollY > 0 && !header.classList.contains('is-sticky')) {
          header.classList.add('is-sticky');
        } else if (scrollY === 0 && header.classList.contains('is-sticky')) {
          header.classList.remove('is-sticky');
        }
        return; // Exit early as no further opacity calculation is needed
      }

      let opacity = 0.5; // Starting opacity for hero-mode

      if (scrollY > 0) {
        // Calculate scroll progress (0 to 1) over the defined threshold
        const scrollProgress = Math.min(1, scrollY / scrollThresholdForFullOpacity);
        // Interpolate opacity from 0.5 to 1
        opacity = 0.5 + (0.5 * scrollProgress); // 0.5 is the difference between 1 and 0.5
      }

      // Apply the calculated opacity as a CSS custom property
      header.style.setProperty('--header-bg-opacity', opacity.toFixed(2));

      // Check if full opacity has been reached
      if (opacity >= 1) {
        hasReachedFullOpacity = true;
        header.style.setProperty('--header-bg-opacity', '1'); // Ensure it's exactly 1
      }

      // Existing 'is-sticky' class logic for other visual changes (e.g., box-shadow, position: fixed)
      if (scrollY > 0 && !header.classList.contains('is-sticky')) {
        header.classList.add('is-sticky');
      } else if (scrollY === 0 && header.classList.contains('is-sticky')) {
        header.classList.remove('is-sticky');
      }
    });
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

  /**
   * Handles newsletter signup form submission with Fetch API for a smooth UX.
   * This is a progressive enhancement; the form works without JS.
   */
  function initSignupForm() {
    const signupForm = document.querySelector('.signup-form');
    if (!signupForm) {
      return;
    }

    const statusEl = signupForm.querySelector('#signup-status');

    signupForm.addEventListener('submit', function(event) {
      event.preventDefault();

      const formData = new FormData(signupForm);
      const submitButton = signupForm.querySelector('button[type="submit"]');
      const originalButtonText = submitButton.textContent;
      submitButton.disabled = true;
      submitButton.textContent = 'Submitting...';

      fetch(signupForm.action, {
        method: 'POST',
        body: formData,
        headers: { 'X-Requested-With': 'XMLHttpRequest' },
      })
      .then(response => response.json())
      .then(data => {
        statusEl.textContent = data.message;
        statusEl.classList.remove('visually-hidden');
        if (data.success) {
          signupForm.reset();
          if (window.dataLayer) {
            window.dataLayer.push({ 'event': 'generate_lead', 'lead_type': 'newsletter_signup' });
          }
        }
      })
      .catch(error => {
        console.error('Signup form submission error:', error);
        statusEl.textContent = 'Could not connect. Please try again later.';
      })
      .finally(() => {
        submitButton.disabled = false;
        submitButton.textContent = originalButtonText;
      });
    });
  }
  initSignupForm();
});
