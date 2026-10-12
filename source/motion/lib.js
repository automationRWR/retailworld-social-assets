// Retailworld reel motion kit. Every frame is a pure function of t (seconds): render(t).
const cl = x => Math.max(0, Math.min(1, x));
const P = (t, a, d) => cl((t - a) / d);
const E = {
  o3: t => 1 - Math.pow(1 - t, 3),
  o5: t => 1 - Math.pow(1 - t, 5),
  io: t => t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2,
  back: t => { const c1 = 1.9, c3 = c1 + 1; return 1 + c3 * Math.pow(t - 1, 3) + c1 * Math.pow(t - 1, 2); },
  el: t => t <= 0 ? 0 : t >= 1 ? 1 : Math.pow(2, -10 * t) * Math.sin((t * 10 - .75) * 2 * Math.PI / 3) + 1
};
const $ = s => document.querySelector(s);
const $$ = s => Array.from(document.querySelectorAll(s));
const lerp = (a, b, k) => a + (b - a) * k;

// split "line one|line two" into masked words; class per line via [cls]text
function split(el) {
  const src = el.getAttribute('data-text') || el.textContent; el.textContent = '';
  src.split('|').forEach(line => {
    const ln = document.createElement('span'); ln.className = 'ln';
    let cls = ''; const m = line.match(/^\[([^\]]+)\](.*)$/); if (m) { cls = m[1]; line = m[2]; }
    if (cls) ln.className += ' ' + cls;
    line.split(' ').forEach((w, i, arr) => {
      const wm = document.createElement('span'); wm.className = 'wm';
      const s = document.createElement('span'); s.className = 'w'; s.textContent = w; wm.appendChild(s); ln.appendChild(wm);
      if (i < arr.length - 1) ln.appendChild(document.createTextNode(' '));
    });
    el.appendChild(ln);
  });
  el._w = Array.from(el.querySelectorAll('.w'));
}

// animate words in (and optionally out)
function words(el, t, start, o) {
  o = Object.assign({ type: 'rise', st: 0.07, d: 0.6, out: null, outD: 0.35 }, o || {});
  el._w.forEach((w, i) => {
    const p = P(t, start + i * o.st, o.d);
    let tr = '', op = 1, fl = '';
    if (o.type === 'rise') { const k = E.o5(p); tr = `translateY(${(1 - k) * 115}%) rotate(${(1 - k) * 9}deg)`; }
    else if (o.type === 'pop') { const k = E.back(p); tr = `scale(${k})`; op = cl(p * 3); w.parentNode.style.overflow = 'visible'; }
    else if (o.type === 'drop') { const k = E.el(p); tr = `translateY(${(1 - k) * -140}%)`; op = cl(p * 4); w.parentNode.style.overflow = 'visible'; }
    else if (o.type === 'blur') { const k = E.o3(p); tr = `scale(${1.6 - .6 * k})`; op = k; fl = `blur(${(1 - k) * 24}px)`; w.parentNode.style.overflow = 'visible'; }
    else if (o.type === 'side') { const k = E.o5(p); tr = `translateX(${(1 - k) * 60}vw) rotate(${(1 - k) * -12}deg)`; op = cl(p * 2); w.parentNode.style.overflow = 'visible'; }
    if (o.out !== null) { const q = E.io(P(t, o.out + i * 0.03, o.outD)); tr += ` translateY(${-q * 120}%)`; op *= 1 - q; }
    w.style.transform = tr; w.style.opacity = op; w.style.filter = fl;
  });
}

// scene visibility + circle wipe in
function scene(el, t, start, end, o) {
  o = Object.assign({ x: 540, y: 1700, d: 0.75 }, o || {});
  if (t < start || t > end) { el.style.display = 'none'; return false; }
  el.style.display = 'block';
  const r = E.io(P(t, start, o.d)) * 2400;
  el.style.clipPath = start === 0 ? 'none' : `circle(${r}px at ${o.x}px ${o.y}px)`;
  return true;
}

// drifting background circles; spec: [x,y,size,color|'ring:color',speed,radius,phase]
function circles(sc, spec) {
  if (window.NO_CIRCLES) { sc._c = []; return; }
  sc._c = spec.map(s => {
    const d = document.createElement('div'); d.className = 'circ';
    d.style.width = d.style.height = s[2] + 'px';
    if (String(s[3]).startsWith('ring:')) d.style.border = '6px solid ' + s[3].slice(5); else d.style.background = s[3];
    sc.insertBefore(d, sc.firstChild); return { d, s };
  });
}
function moveCircles(sc, t) {
  (sc._c || []).forEach(({ d, s }) => {
    const [x, y, size, , sp, R, ph] = s;
    const cx = x + R * Math.cos(t * sp + ph), cy = y + R * Math.sin(t * sp * 1.3 + ph);
    const sc2 = 1 + 0.08 * Math.sin(t * sp * 2 + ph);
    d.style.transform = `translate(${cx - size / 2}px, ${cy - size / 2}px) scale(${sc2})`;
  });
}
function pop(el, t, start, o) {
  o = Object.assign({ d: 0.6, base: '' }, o || {});
  const p = P(t, start, o.d), k = E.back(p);
  el.style.opacity = cl(p * 3); el.style.transform = `${o.base} scale(${k})`;
}
function rise(el, t, start, o) {
  o = Object.assign({ d: 0.8, dy: 200, base: '' }, o || {});
  const k = E.o5(P(t, start, o.d));
  el.style.opacity = cl(k * 1.5); el.style.transform = `${o.base} translateY(${(1 - k) * o.dy}px)`;
}
window.addEventListener('DOMContentLoaded', () => {
  $$('[data-text]').forEach(split);
  const sc = $$('.sc'); if (sc.length > 2) sc.forEach((x, i) => { if (i > 0 && i < sc.length - 1) { const l = x.querySelector('.logo'); if (l) l.remove(); } });
  if (window.setup) setup();
});
