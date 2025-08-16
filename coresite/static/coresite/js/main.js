console.log("MAIN.JS LOADED FROM SERVER");

document.addEventListener('DOMContentLoaded', function () {
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
});
