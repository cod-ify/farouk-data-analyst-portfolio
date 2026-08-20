/* main.js — thin bootstrapper. Wires up nav, glossary tooltips and charts.
   Individual pages need no bespoke inline JS. */
document.addEventListener('DOMContentLoaded', function () {
  if (window.Nav) window.Nav.init();
  if (window.Tooltip) window.Tooltip.init();
  if (window.Charts) window.Charts.autoInit();
});
