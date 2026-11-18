// Seamless-loop helpers for grid posts. All motion is periodic in window.DURATION.
const TAU = Math.PI * 2;
const D = () => window.DURATION;
const osc = (t, k, off) => Math.sin(TAU * k * t / D() + (off || 0));
// spec: [x, y, size, colour|'ring:colour', R, kx, ky, phase]
function loopCircles(sc, spec) {
  sc._lc = spec.map(s => {
    const d = document.createElement('div'); d.className = 'circ';
    d.style.width = d.style.height = s[2] + 'px';
    if (String(s[3]).startsWith('ring:')) d.style.border = '6px solid ' + s[3].slice(5); else d.style.background = s[3];
    sc.insertBefore(d, sc.firstChild); return { d, s };
  });
}
function moveLoop(sc, t) {
  (sc._lc || []).forEach(({ d, s }) => {
    const [x, y, size, , R, kx, ky, ph] = s;
    const cx = x + R * Math.cos(TAU * kx * t / D() + ph), cy = y + R * Math.sin(TAU * ky * t / D() + ph);
    d.style.transform = `translate(${cx - size / 2}px, ${cy - size / 2}px) scale(${1 + .06 * osc(t, 2, ph)})`;
  });
}
