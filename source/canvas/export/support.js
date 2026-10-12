// Minimal offline renderer for .dc.html artboards (export only).
window.DCLogic = class { constructor(p) { this.props = p || {}; this.state = {}; } setState() {} forceUpdate() {} };
(function () {
  function get(path, scope) {
    path = path.trim();
    if (path === 'true') return true; if (path === 'false') return false;
    if (/^-?\d+(\.\d+)?$/.test(path)) return Number(path);
    return path.split('.').reduce(function (o, k) { return o == null ? undefined : o[k]; }, scope);
  }
  function interp(str, scope) {
    return str.replace(/\{\{\s*([^}]+?)\s*\}\}/g, function (_, p) { var v = get(p, scope); return v == null ? '' : String(v); });
  }
  function build(node, scope, parent) {
    if (node.nodeType === 3) { parent.appendChild(document.createTextNode(interp(node.nodeValue, scope))); return; }
    if (node.nodeType !== 1) return;
    var tag = node.tagName.toLowerCase();
    if (tag === 'sc-for') {
      var list = get(node.getAttribute('list').replace(/[{}]/g, ''), scope) || [];
      var as = node.getAttribute('as') || 'item';
      list.forEach(function (it, i) {
        var s = Object.create(scope); s[as] = it; s.$index = i;
        Array.prototype.forEach.call(node.childNodes, function (c) { build(c, s, parent); });
      });
      return;
    }
    if (tag === 'sc-if') {
      if (get(node.getAttribute('value').replace(/[{}]/g, ''), scope)) Array.prototype.forEach.call(node.childNodes, function (c) { build(c, scope, parent); });
      return;
    }
    var el = node.namespaceURI === 'http://www.w3.org/2000/svg' ? document.createElementNS(node.namespaceURI, node.tagName) : document.createElement(node.tagName);
    Array.prototype.forEach.call(node.attributes, function (a) { el.setAttribute(a.name, interp(a.value, scope)); });
    var kids = node.content ? node.content.childNodes : node.childNodes;
    Array.prototype.forEach.call(kids, function (c) { build(c, scope, el); });
    parent.appendChild(el);
  }
  document.addEventListener('DOMContentLoaded', function () {
    var code = document.querySelector('script[data-dc-script]').textContent;
    var C = new Function(code + '\n;return Component;')();
    var vals = new C({}).renderVals();
    var xdc = document.querySelector('x-dc');
    var helmet = xdc.querySelector('helmet');
    if (helmet) { Array.prototype.forEach.call(helmet.children, function (c) { document.head.appendChild(c.cloneNode(true)); }); helmet.remove(); }
    var root = document.createElement('div');
    Array.prototype.forEach.call(xdc.childNodes, function (c) { build(c, vals, root); });
    xdc.replaceWith(root);
    document.fonts.ready.then(function () { setTimeout(function () { window.__ready = true; }, 300); });
  });
})();
