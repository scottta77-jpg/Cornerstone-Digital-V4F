/* ============================================================
   CORNERSTONE DIGITAL — Global JS
   ============================================================ */

document.addEventListener('DOMContentLoaded', function () {

  // --- Mobile menu ---
  const toggle  = document.querySelector('.mobile-menu-toggle');
  const closeBtn = document.querySelector('.mobile-menu__close');
  const overlay = document.querySelector('.mobile-menu__overlay');
  const menu    = document.getElementById('mobile-menu');

  function openMenu() {
    if (!menu) return;
    menu.setAttribute('aria-hidden', 'false');
    if (toggle) toggle.setAttribute('aria-expanded', 'true');
    document.body.style.overflow = 'hidden';
  }

  function closeMenu() {
    if (!menu) return;
    menu.setAttribute('aria-hidden', 'true');
    if (toggle) toggle.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = '';
  }

  if (toggle)   toggle.addEventListener('click', openMenu);
  if (closeBtn) closeBtn.addEventListener('click', closeMenu);
  if (overlay)  overlay.addEventListener('click', closeMenu);

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeMenu();
  });

  // --- Footer year ---
  document.querySelectorAll('.js-year').forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });

  // --- FAQ accordion ---
  // Works with <div class="faq-item"> / <div class="faq-item__head"> pattern.
  // Toggles .is-open on the item and aria-expanded on the head.
  document.querySelectorAll('.faq-item').forEach(function (item) {
    var head = item.querySelector('.faq-item__head');
    if (!head) return;

    // Honour any aria-expanded="true" set in HTML (first item open on load)
    if (head.getAttribute('aria-expanded') === 'true') {
      item.classList.add('is-open');
    }

    head.addEventListener('click', function () {
      var isOpen = item.classList.contains('is-open');

      // Close all items in the same FAQ list
      var list = item.closest('ul, ol, div.faq-list, div.about-faq__list, .services-faq__list');
      var scope = list ? list.querySelectorAll('.faq-item') : document.querySelectorAll('.faq-item');
      scope.forEach(function (other) {
        other.classList.remove('is-open');
        var otherHead = other.querySelector('.faq-item__head');
        if (otherHead) otherHead.setAttribute('aria-expanded', 'false');
      });

      // Toggle clicked item
      if (!isOpen) {
        item.classList.add('is-open');
        head.setAttribute('aria-expanded', 'true');
      }
    });

    // Keyboard: Enter / Space activates the head
    head.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        head.click();
      }
    });
  });

  // --- Active nav link ---
  var currentPath = window.location.pathname.replace(/\/$/, '') || '/';
  document.querySelectorAll('.nav-link, .mobile-nav-link').forEach(function (link) {
    var href = (link.getAttribute('href') || '').replace(/\/$/, '') || '/';
    if (href === currentPath) {
      link.setAttribute('aria-current', 'page');
    } else {
      link.removeAttribute('aria-current');
    }
  });

});
