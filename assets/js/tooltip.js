/* tooltip.js — glossary-term tooltips. Exposes window.Tooltip.init().

   Markup contract (emitted by templates.py):
     <button class="term" data-term="p-value">p-value <svg>...</svg></button>
   Definitions come from a single embedded JSON block:
     <script type="application/json" id="glossary-data">{"p-value": "...", ...}</script>
*/
(function () {
  'use strict';

  function init() {
    var dataScript = document.getElementById('glossary-data');
    if (!dataScript) return;
    var glossary;
    try {
      glossary = JSON.parse(dataScript.textContent);
    } catch (e) {
      return;
    }

    var openTooltip = null;
    var openTrigger = null;

    function closeTooltip() {
      if (openTooltip) {
        openTooltip.remove();
        openTooltip = null;
      }
      if (openTrigger) {
        openTrigger.setAttribute('aria-expanded', 'false');
        openTrigger = null;
      }
    }

    function openFor(trigger) {
      var term = trigger.getAttribute('data-term');
      var def = glossary[term];
      if (!def) return;
      closeTooltip();

      var tip = document.createElement('span');
      tip.className = 'term-tooltip';
      tip.id = 'term-tooltip-' + term.replace(/[^a-z0-9]/gi, '');
      tip.textContent = def;
      document.body.appendChild(tip);

      var rect = trigger.getBoundingClientRect();
      var top = rect.bottom + window.scrollY + 8;
      var left = rect.left + window.scrollX;
      var maxLeft = window.scrollX + document.documentElement.clientWidth - tip.offsetWidth - 12;
      tip.style.position = 'absolute';
      tip.style.top = top + 'px';
      tip.style.left = Math.max(8, Math.min(left, maxLeft)) + 'px';

      trigger.setAttribute('aria-describedby', tip.id);
      trigger.setAttribute('aria-expanded', 'true');
      openTooltip = tip;
      openTrigger = trigger;
    }

    document.querySelectorAll('.term[data-term]').forEach(function (trigger) {
      trigger.setAttribute('aria-expanded', 'false');
      trigger.addEventListener('click', function (e) {
        e.stopPropagation();
        if (openTrigger === trigger) {
          closeTooltip();
        } else {
          openFor(trigger);
        }
      });
      trigger.addEventListener('mouseenter', function () { openFor(trigger); });
      trigger.addEventListener('mouseleave', function () {
        if (openTrigger === trigger) closeTooltip();
      });
      trigger.addEventListener('focus', function () { openFor(trigger); });
      trigger.addEventListener('blur', closeTooltip);
    });

    document.addEventListener('click', closeTooltip);
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closeTooltip();
    });
  }

  window.Tooltip = { init: init };
})();
