/* nav.js — accessible mobile navigation shared across the static site. */
(function () {
  'use strict';

  function init() {
    var toggle = document.querySelector('.nav-toggle');
    var links = document.querySelector('.nav-links');
    if (!toggle || !links) return;

    function closeMenu() {
      links.classList.remove('open');
      toggle.setAttribute('aria-expanded', 'false');
    }

    toggle.addEventListener('click', function () {
      var willOpen = !links.classList.contains('open');
      links.classList.toggle('open', willOpen);
      toggle.setAttribute('aria-expanded', String(willOpen));
    });

    links.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', closeMenu);
    });

    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape') closeMenu();
    });

    window.addEventListener('resize', function () {
      if (window.innerWidth > 760) closeMenu();
    });
  }

  window.Nav = { init: init };
})();
