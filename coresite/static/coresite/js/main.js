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
});
