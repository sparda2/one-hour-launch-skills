/* Winning Funnel Builder — shared page behaviour (no dependencies).
 * Every generated page loads ../funnel.config.js (sets window.FUNNEL) then this.
 *
 * Honesty is built in: every trigger below renders ONLY from real config data.
 * No config value -> the element stays hidden. Nothing here invents buyers,
 * stock counts, ratings or deadlines. (See references/page-structure.md.)
 */
(function () {
  var C = window.FUNNEL || {};
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return [].slice.call((r || document).querySelectorAll(s)); };
  var store = {
    get: function (k) { try { return localStorage.getItem('wfb_' + k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem('wfb_' + k, v); } catch (e) {} }
  };

  /* 1. CTA routing: data-cta="checkout|accept|decline|next" -> URL from config,
        carrying UTM / fbclid params forward so attribution survives every step. */
  function carry(url) {
    try {
      var u = new URL(url, location.href), here = new URLSearchParams(location.search);
      ['utm_source','utm_medium','utm_campaign','utm_content','utm_term','fbclid','gclid','xcod','sck'].forEach(function (k) {
        if (here.get(k) && !u.searchParams.has(k)) u.searchParams.set(k, here.get(k));
      });
      return u.toString();
    } catch (e) { return url; }
  }
  $$('[data-cta]').forEach(function (a) {
    var dest = (C.cta || {})[a.getAttribute('data-cta')];
    if (dest) a.setAttribute('href', carry(dest));
    else a.setAttribute('data-cta-missing', '1'); /* README lists these to fill */
  });

  /* 2. Sticky announcement bar — only if config provides the text. */
  (function () {
    var bar = $('[data-bar]');
    if (!bar) return;
    if (C.bar && C.bar.text) { bar.textContent = C.bar.text; bar.hidden = false; }
    else bar.hidden = true;
  })();

  /* 3. Countdown — ONLY for a real deadline in config (ISO date). Never a
        per-visitor reset. Past the deadline it hides instead of lying. */
  $$('[data-countdown]').forEach(function (el) {
    var end = C.deadline ? Date.parse(C.deadline) : NaN;
    if (!end || isNaN(end)) { el.hidden = true; return; }
    function tick() {
      var ms = end - Date.now();
      if (ms <= 0) { el.hidden = true; return; }
      var s = Math.floor(ms / 1000), d = Math.floor(s / 86400), h = Math.floor(s % 86400 / 3600),
          m = Math.floor(s % 3600 / 60), sec = s % 60, p = function (n) { return (n < 10 ? '0' : '') + n; };
      el.textContent = (d ? d + 'd ' : '') + p(h) + ':' + p(m) + ':' + p(sec);
      el.hidden = false;
    }
    tick(); setInterval(tick, 1000);
  });

  /* 4. FAQ accordion (progressive enhancement; <details> also works). */
  $$('[data-faq] [data-q]').forEach(function (q) {
    q.addEventListener('click', function () {
      var item = q.closest('[data-faq-item]') || q.parentNode;
      item.classList.toggle('open');
    });
  });

  /* 5. Exit-intent popup — restates the real offer ONCE per visitor. No fake
        scarcity; shows only what config already states honestly elsewhere. */
  (function () {
    var p = $('[data-exit]');
    if (!p || store.get('exit')) return;
    function show() { if (store.get('exit')) return; p.hidden = false; store.set('exit', '1'); }
    document.addEventListener('mouseout', function (e) { if (!e.relatedTarget && e.clientY <= 0) show(); });
    var closed = false;
    window.addEventListener('scroll', function () { /* mobile: deep scroll + back-up intent */
      if (closed) return; if (window.scrollY > document.body.scrollHeight * 0.6) closed = true;
    });
    $$('[data-exit-close]').forEach(function (b) { b.addEventListener('click', function () { p.hidden = true; }); });
  })();

  /* 6. Social-proof popup ("someone just bought") — OFF unless config.proof.live
        is a real, user-supplied list of recent orders. Default: never shown. */
  (function () {
    var host = $('[data-proof-live]'), feed = (C.proof && C.proof.live) || [];
    if (!host) return;
    if (!Array.isArray(feed) || !feed.length) { host.hidden = true; return; }
    var i = 0;
    function next() {
      var item = feed[i % feed.length]; i++;
      host.textContent = item; host.hidden = false;
      setTimeout(function () { host.hidden = true; }, 6000);
      setTimeout(next, 16000);
    }
    setTimeout(next, 8000);
  })();

  /* 7. Tab-away attention: when the visitor switches to another tab, swap the
        page <title> (and favicon, if configured) to pull them back; restore on
        return. Config: C.tabAway = { titles:[...], favicon:"url" }. Sensible
        defaults so it works with no config. */
  (function () {
    var cfg = C.tabAway || {};
    var msgs = (cfg.titles && cfg.titles.length) ? cfg.titles
      : ['\u{1F44B} Wait! Don’t go…', '\u{1F525} Your offer is still here', '← Come back 💚'];
    var realTitle = document.title, realIcon = null, link = document.querySelector('link[rel~="icon"]');
    if (link) realIcon = link.getAttribute('href');
    var timer = null, i = 0;
    function setIcon(href) { if (link && href != null) link.setAttribute('href', href); }
    document.addEventListener('visibilitychange', function () {
      if (document.hidden) {
        if (cfg.favicon) setIcon(cfg.favicon);
        i = 0;
        timer = setInterval(function () { document.title = msgs[i++ % msgs.length]; }, 1200);
        document.title = msgs[0];
      } else {
        if (timer) { clearInterval(timer); timer = null; }
        document.title = realTitle; setIcon(realIcon);
      }
    });
  })();
})();
