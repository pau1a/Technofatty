console.log("MAIN.JS LOADED FROM SERVER");

document.addEventListener('DOMContentLoaded', function () {
  const menuOverlay = document.querySelector('.menu-overlay');
  const hamburgerBtn = document.querySelector('.hamburger-btn');
  const closeBtn = document.querySelector('.menu-overlay__close');

  console.log("Script loaded", { menuOverlay, hamburgerBtn, closeBtn });

  if (hamburgerBtn && menuOverlay) {
    hamburgerBtn.addEventListener('click', function () {
      console.log("Hamburger clicked");
      menuOverlay.classList.add('is-open');
      menuOverlay.removeAttribute('hidden');
      console.log("Hidden removed?", menuOverlay.hasAttribute('hidden'));
    });
  }

  if (closeBtn && menuOverlay) {
    closeBtn.addEventListener('click', function () {
      console.log("Close clicked");
      menuOverlay.classList.remove('is-open');
      menuOverlay.setAttribute('hidden', '');
      console.log("Hidden reapplied?", menuOverlay.hasAttribute('hidden'));
    });
  }
});
