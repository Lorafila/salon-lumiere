(function () {
  'use strict';
  document.documentElement.classList.add('js');
  var fine = window.matchMedia('(hover:hover) and (pointer:fine)').matches;
  var calm = window.matchMedia('(prefers-reduced-motion:reduce)').matches;

  var nav = document.getElementById('nav');
  var btn = document.querySelector('.menu-btn');
  if (nav && btn) {
    btn.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      btn.setAttribute('aria-expanded', String(open));
    });
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) { nav.classList.remove('open'); btn.setAttribute('aria-expanded', 'false'); }
    });
  }

  // Language switcher: keep the current #section and remember the choice (language code only).
  document.querySelectorAll('.lang a').forEach(function (a) {
    a.addEventListener('click', function () {
      try { localStorage.setItem('salon-lang', a.getAttribute('lang')); } catch (err) { /* storage may be blocked */ }
      a.setAttribute('href', a.getAttribute('href').split('#')[0] + location.hash);
    });
  });

  // Pointer effects (fine pointers only, never with reduced motion): spotlight on tiles, magnetic buttons.
  if (fine && !calm) {
    document.querySelectorAll('.tile').forEach(function (t) {
      t.addEventListener('pointermove', function (e) {
        var r = t.getBoundingClientRect();
        t.style.setProperty('--mx', (e.clientX - r.left) + 'px');
        t.style.setProperty('--my', (e.clientY - r.top) + 'px');
      });
    });
    document.querySelectorAll('.btn').forEach(function (b) {
      b.addEventListener('pointermove', function (e) {
        var r = b.getBoundingClientRect();
        b.style.transform = 'translate(' + ((e.clientX - r.left - r.width / 2) * 0.18).toFixed(1) + 'px,' + ((e.clientY - r.top - r.height / 2) * 0.25).toFixed(1) + 'px)';
      });
      b.addEventListener('pointerleave', function () { b.style.transform = ''; });
    });
  }

  // Concierge form: three steps, validated per step. Demo only - it never sends or stores anything.
  var form = document.getElementById('contact-form');
  if (!form) return;
  var d = form.dataset, status = form.querySelector('.status'), prog = form.querySelector('.progress');
  var steps = Array.prototype.slice.call(form.querySelectorAll('.step'));
  var back = form.querySelector('.back'), next = form.querySelector('.next'), submit = form.querySelector('.submit');
  var cur = 0;

  function show(n, focus) {
    cur = n;
    steps.forEach(function (s, k) { s.hidden = k !== n; });
    prog.textContent = d.msgProgress.replace('{n}', n + 1).replace('{total}', steps.length);
    back.hidden = n === 0; next.hidden = n === steps.length - 1; submit.hidden = n !== steps.length - 1;
    if (focus) { var f = steps[n].querySelector('input,select,textarea'); if (f) f.focus(); }
  }
  function validate(step) {
    var first = null;
    step.querySelectorAll('[required]').forEach(function (el) {
      var msg = '', err;
      if (el.type === 'radio') {
        if (!form.querySelector('input[name="' + el.name + '"]:checked')) msg = d.msgRequired;
        err = document.getElementById('f-' + el.name + '-err');
        err.textContent = msg;
      } else {
        if (!el.value.trim()) msg = d.msgRequired;
        else if (el.type === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(el.value)) msg = d.msgEmail;
        document.getElementById(el.id + '-err').textContent = msg;
        el.setAttribute('aria-invalid', msg ? 'true' : 'false');
      }
      if (msg && !first) first = el;
    });
    if (first) { status.textContent = d.msgSummary; status.className = 'status error'; first.focus(); return false; }
    status.textContent = ''; status.className = 'status';
    return true;
  }
  show(0, false);
  next.addEventListener('click', function () { if (validate(steps[cur])) show(cur + 1, true); });
  back.addEventListener('click', function () { status.textContent = ''; status.className = 'status'; show(cur - 1, true); });
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (cur < steps.length - 1) { next.click(); return; }
    if (!validate(steps[cur])) return;
    status.textContent = d.msgSuccess; status.className = 'status ok';
    form.reset(); show(0, false);
  });
})();
