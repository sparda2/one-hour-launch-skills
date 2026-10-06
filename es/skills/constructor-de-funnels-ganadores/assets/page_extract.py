#!/usr/bin/env python3
"""Render a page like a real browser and dump its STRUCTURE as text, without
screenshots (cost rule: an image in context is re-charged every turn).

Usage:
  page_extract.py <url> <out_dir> [--shot] [--mobile]

  --mobile  render as an iPhone visitor arriving from a Facebook ad (many
            funnels rotate or redirect by device / referrer: always extract
            BOTH the desktop and the mobile variant of a sales page)

Writes to <out_dir>:
  outline.md   sections in page order: headings, copy, CTAs (+href), images
               (src/alt), forms, prices, guarantees, countdowns, popups
  page.json    the same data, machine-readable, plus links / scripts / tech
  page.html    the rendered HTML (for exact copy look-ups)
  shot.jpg     ONLY with --shot: one 768px-wide, ~1600px-tall JPG for a single
               visual check (open it ONCE, never re-open)

Prints ONE line of JSON (counts + paths).
"""
import json, os, re, sys

CHROME_CANDIDATES = [
    os.environ.get("CHROME_PATH", ""),
    "/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
]

TECH_PATTERNS = {
    "gohighlevel": r"leadconnectorhq|msgsndr|gohighlevel|highlevel",
    "clickfunnels": r"clickfunnels|cf2\.|myclickfunnels",
    "hotmart": r"hotmart|pay\.hotmart",
    "kiwify": r"kiwify",
    "gumroad": r"gumroad",
    "stripe": r"stripe\.com|buy\.stripe|checkout\.stripe",
    "shopify": r"shopify|myshopify",
    "systeme": r"systeme\.io",
    "thrivecart": r"thrivecart",
    "samcart": r"samcart",
    "wordpress": r"wp-content|wp-includes",
    "elementor": r"elementor",
    "lemonsqueezy": r"lemonsqueezy",
    "paypal": r"paypal",
    "monetizze": r"monetizze",
    "eduzz": r"eduzz",
    "payhip": r"payhip",
}

JS_EXTRACT = r"""
() => {
  const vis = el => { const s = getComputedStyle(el); const r = el.getBoundingClientRect();
    return s.display !== 'none' && s.visibility !== 'hidden' && (r.width > 0 || r.height > 0); };
  const txt = el => (el.innerText || '').replace(/\s+/g, ' ').trim();
  const blocks = [];
  const seen = new Set();
  // Text leaves: div/span/strong… that hold their own text (page builders rarely use <p>)
  const ownText = el => [...el.childNodes].filter(n => n.nodeType === 3).map(n => n.textContent).join(' ').replace(/\s+/g, ' ').trim();
  const sel = 'h1,h2,h3,h4,h5,p,li,blockquote,button,a,img,form,video,iframe,div,span,strong,em,b,small,label,td,summary,[class*="countdown" i],[class*="timer" i],[class*="popup" i],[class*="modal" i],[class*="sticky" i],[class*="banner" i]';
  const walker = [...document.querySelectorAll(sel)].filter(el => {
    const tag = el.tagName.toLowerCase();
    if (['div','span','strong','em','b','small','label','td'].includes(tag)) {
      const c = String(el.className || '');
      if (/countdown|timer|popup|modal|sticky|banner/i.test(c)) return true;
      if (el.closest('a,button,h1,h2,h3,h4,h5,p,li,blockquote,summary')) return false;
      return ownText(el).length >= 12;
    }
    return true;
  });
  for (const el of walker) {
    if (seen.has(el)) continue; seen.add(el);
    const tag = el.tagName.toLowerCase();
    const cls = (el.className && el.className.baseVal === undefined ? el.className : '') || '';
    const hidden = !vis(el);
    if (tag === 'img') {
      const src = el.currentSrc || el.src || '';
      if (!src || (el.naturalWidth && el.naturalWidth < 40)) continue;
      blocks.push({t: 'img', src, alt: el.alt || '', w: el.naturalWidth, h: el.naturalHeight, hidden});
    } else if (tag === 'a' || tag === 'button') {
      const s = txt(el); if (!s || s.length > 140) continue;
      const r = el.getBoundingClientRect(); const st = getComputedStyle(el);
      const looksButton = tag === 'button' || /btn|button|cta/i.test(cls) || (st.backgroundColor !== 'rgba(0, 0, 0, 0)' && r.height >= 36);
      blocks.push({t: looksButton ? 'cta' : 'link', text: s, href: el.href || '', hidden});
    } else if (tag === 'form') {
      const fields = [...el.querySelectorAll('input,select,textarea')].map(i => i.name || i.type || i.placeholder).filter(Boolean);
      blocks.push({t: 'form', action: el.action || '', fields, hidden});
    } else if (tag === 'video' || tag === 'iframe') {
      blocks.push({t: tag, src: el.src || el.currentSrc || '', hidden});
    } else if (/countdown|timer/i.test(cls)) {
      blocks.push({t: 'countdown', text: txt(el).slice(0, 120), cls: String(cls).slice(0, 80), hidden});
    } else if (/popup|modal/i.test(cls)) {
      blocks.push({t: 'popup', text: txt(el).slice(0, 300), cls: String(cls).slice(0, 80), hidden});
    } else if (/sticky|banner/i.test(cls)) {
      blocks.push({t: 'bar', text: txt(el).slice(0, 200), cls: String(cls).slice(0, 80), hidden});
    } else {
      const s = ['div','span','strong','em','b','small','label','td'].includes(tag) ? ownText(el) : txt(el); if (!s) continue;
      if (tag === 'p' || tag === 'li' || tag === 'blockquote') {
        if (el.closest('a,button')) continue;
        if (el.querySelector('p,li,h1,h2,h3')) continue;
      }
      blocks.push({t: tag, text: s.slice(0, 1200), hidden});
    }
  }
  const scripts = [...document.scripts].map(s => s.src).filter(Boolean);
  const inline = [...document.scripts].filter(s => !s.src).map(s => s.textContent).join('\n').slice(0, 200000);
  const links = [...document.querySelectorAll('a[href]')].map(a => a.href);
  const meta = {};
  for (const m of document.querySelectorAll('meta[name],meta[property]')) meta[m.getAttribute('name') || m.getAttribute('property')] = m.content;
  return {title: document.title, lang: document.documentElement.lang, meta, blocks, scripts, links: [...new Set(links)], inline,
          height: document.body.scrollHeight};
}
"""

PRICE_RE = re.compile(r"(?:[$€£R]\$?\s?\d[\d.,]*|\d[\d.,]*\s?(?:USD|EUR|MXN|COP|BRL|€|\$))")
GUARANTEE_RE = re.compile(r"\b(\d{1,3})\s*(?:-|\s)?(?:day|días|dias|dia)s?\b.{0,40}(?:guarantee|garant)", re.I)
URGENCY_RE = re.compile(r"(only|solo|últim|ultim|expires|expira|termina|ends|hoy|today|limited|limitad|quedan|left|spots|cupos)", re.I)


def find_chrome():
    for c in CHROME_CANDIDATES:
        if c and os.path.exists(c):
            return c
    return None


MOBILE_UA = ("Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 "
             "(KHTML, like Gecko) Mobile/15E148 [FBAN/FBIOS;FBAV/450.0]")
DESKTOP_UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/129.0 Safari/537.36")


def main(url, out_dir, shot=False, mobile=False):
    from playwright.sync_api import sync_playwright
    os.makedirs(out_dir, exist_ok=True)
    with sync_playwright() as p:
        kw = {"headless": True, "args": ["--no-sandbox"]}
        exe = find_chrome()
        if exe:
            kw["executable_path"] = exe
        browser = p.chromium.launch(**kw)
        # Cloud sessions route traffic through an egress proxy with its own CA:
        # use it and trust it (read-only page analysis, nothing is submitted).
        proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
        extra = {"proxy": {"server": proxy}, "ignore_https_errors": True} if proxy else {}
        dev = ({"viewport": {"width": 390, "height": 844}, "is_mobile": True, "has_touch": True,
                "user_agent": MOBILE_UA} if mobile else
               {"viewport": {"width": 1280, "height": 900}, "user_agent": DESKTOP_UA})
        ctx = browser.new_context(locale="es-ES", extra_http_headers={"Referer": "https://l.facebook.com/"},
                                  **dev, **extra)
        page = ctx.new_page()
        resp = page.goto(url, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(2500)
        for _ in range(25):  # scroll to trigger lazy content and scroll-based popups
            page.mouse.wheel(0, 1400)
            page.wait_for_timeout(250)
        page.wait_for_timeout(1500)
        data = page.evaluate(JS_EXTRACT)
        final_url = page.url
        html = page.content()
        if shot:
            if not mobile:
                page.set_viewport_size({"width": 768, "height": 1600})
            page.evaluate("window.scrollTo(0,0)")
            page.wait_for_timeout(500)
            page.screenshot(path=os.path.join(out_dir, "shot.jpg"), type="jpeg", quality=60)
        browser.close()

    blob = html + "\n" + "\n".join(data["scripts"]) + "\n" + "\n".join(data["links"])
    tech = sorted(k for k, rx in TECH_PATTERNS.items() if re.search(rx, blob, re.I))
    inline = data.pop("inline")
    timers = sorted(set(re.findall(r"(countdown|setInterval|exit[-_ ]?intent|mouseleave|beforeunload|localStorage|sessionStorage)", inline, re.I)))
    text_all = " ".join(b.get("text", "") for b in data["blocks"])
    data.update({
        "url": url, "final_url": final_url, "status": resp.status if resp else None, "tech": tech,
        "script_signals": timers,
        "prices": sorted(set(PRICE_RE.findall(text_all)))[:40],
        "guarantees": sorted(set(m.group(0) for m in GUARANTEE_RE.finditer(text_all)))[:10],
        "urgency_phrases": sorted(set(m.group(0).lower() for m in URGENCY_RE.finditer(text_all)))[:20],
    })
    with open(os.path.join(out_dir, "page.json"), "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    with open(os.path.join(out_dir, "page.html"), "w") as f:
        f.write(html)

    lines = [f"# {data['title']}", f"URL: {final_url} (status {data['status']}) · lang: {data['lang']} · tech: {', '.join(tech) or '?'}",
             f"Prices seen: {', '.join(data['prices']) or '-'} · Guarantees: {', '.join(data['guarantees']) or '-'}",
             f"Script signals: {', '.join(timers) or '-'} · Page height: {data['height']}px", ""]
    last = None
    for b in data["blocks"]:
        h = " (hidden)" if b.get("hidden") else ""
        t = b["t"]
        if t in ("h1", "h2", "h3", "h4", "h5"):
            lines.append(f"\n{'#' * min(6, int(t[1]) + 1)} {b['text']}{h}")
        elif t == "cta":
            lines.append(f"  [CTA] {b['text']} → {b['href']}{h}")
        elif t == "link":
            continue
        elif t == "img":
            lines.append(f"  [IMG {b.get('w')}x{b.get('h')}] {b['alt'][:80]} · {b['src'][:160]}{h}")
        elif t in ("countdown", "popup", "bar"):
            lines.append(f"  [{t.upper()}] {b.get('text', '')} {{{b.get('cls', '')}}}{h}")
        elif t == "form":
            lines.append(f"  [FORM] → {b['action']} fields={b['fields']}{h}")
        elif t in ("video", "iframe"):
            lines.append(f"  [{t.upper()}] {b['src'][:160]}{h}")
        else:
            if b["text"] == last:
                continue
            lines.append(f"- {b['text']}{h}")
            last = b["text"]
    with open(os.path.join(out_dir, "outline.md"), "w") as f:
        f.write("\n".join(lines))
    return {"ok": True, "status": data["status"], "final_url": final_url, "blocks": len(data["blocks"]),
            "ctas": sum(1 for b in data["blocks"] if b["t"] == "cta"), "tech": tech,
            "outline": os.path.join(out_dir, "outline.md")}


if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    try:
        print(json.dumps(main(a[0], a[1], shot="--shot" in sys.argv, mobile="--mobile" in sys.argv)))
    except Exception as e:
        print(json.dumps({"ok": False, "error": f"{type(e).__name__}: {e}"}))
