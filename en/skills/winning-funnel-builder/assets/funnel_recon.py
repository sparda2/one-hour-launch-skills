#!/usr/bin/env python3
"""Map a funnel from the OUTSIDE — sales page, checkout, order bumps, upsells,
downsells, thank-you pages — using only PUBLIC pages. Never buys, never
submits forms, never logs in, never uses card numbers.

Usage:
  funnel_recon.py <sales_url> <out_dir> [--page-json path/to/page.json ...]
                  (page.html next to each page.json is read too)
                  [--max-probes 60] [--no-wayback]

Techniques (in order, cheapest first):
  1. Links on the sales page(s) (from page_extract.py page.json files):
     checkout links, other same-site pages. PLUS the funnel builder's own
     data embedded in the page: GoHighLevel pages ship the WHOLE funnel
     (every step's URL + name, e.g. "ups1", "ds1", "thank-you") in
     __NUXT_DATA__; ClickFunnels / others ship step or checkout URLs in JSON.
  2. The site's own public indexes: robots.txt (Sitemap + Disallow lines often
     name /upsell paths), sitemaps, WordPress REST page list (/wp-json/wp/v2/pages).
  3. The CHECKOUT page's public HTML + its own JS: checkout builders embed the
     order bumps / upsells / downsells (names, prices, images) and the
     post-purchase redirect URLs in the page so the browser can render them.
  4. Bounded probing of conventional step slugs (/upsell, /oto1, /gracias…),
     next to the sales page path and at the root. GET only, rate-limited,
     soft-404s and homepage redirects discarded.
  5. Wayback Machine index of the domain (old URLs of upsell pages).

Writes <out_dir>/funnel_map.json and prints ONE line of JSON.
"""
import hashlib, html, json, os, re, sys, time, urllib.parse, urllib.request
import ssl

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36"
STEP_WORDS = r"upsell|up-sell|oto|one[-_]?time|downsell|down-sell|thank|thanks|gracias|obrigado|confirm|success|bonus|vip|upgrade|premium|special|especial|oferta|offer|order[-_]?bump|bump|post[-_]?purchase|members|acceso|access|checkout|pago|pay"
CHECKOUT_RX = re.compile(r"checkout|/pay|pay\.|cart|/order|hotmart|kiwify|gumroad|stripe|thrivecart|samcart|paypal|lemonsqueezy|payhip|systeme|impultienda|monetizze|eduzz|clickfunnels|/orders?/", re.I)
SLUGS = ["upsell", "upsell1", "upsell-1", "upsell2", "upsell-2", "oto", "oto1", "oto-1", "oto2", "oto-2",
         "downsell", "downsell1", "downsell-1", "one-time-offer", "special-offer", "oferta-especial",
         "oferta", "oferta-unica", "upgrade", "vip", "bonus", "thank-you", "thankyou", "thanks",
         "gracias", "obrigado", "confirmation", "order-confirmation", "confirmacion", "success",
         "checkout", "pago", "obrigado-compra", "gracias-compra"]
SOFT404 = re.compile(r"404|not found|no encontrada|página no existe|page not found|não encontrada", re.I)

_ctx = ssl.create_default_context()
_last = [0.0]


def fetch(url, timeout=20, limit=3_000_000):
    """GET with a 0.5 s rate limit. Returns (status, final_url, text)."""
    wait = 0.5 - (time.time() - _last[0])
    if wait > 0:
        time.sleep(wait)
    _last[0] = time.time()
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "es-ES,es;q=0.9,en;q=0.8"})
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=_ctx) as r:
            return r.status, r.geturl(), r.read(limit).decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, url, ""
    except Exception as e:
        return 0, url, f"ERR {type(e).__name__}"


def norm(u):
    p = urllib.parse.urlsplit(u)
    return urllib.parse.urlunsplit((p.scheme, p.netloc.lower(), p.path.rstrip("/") or "/", "", ""))


def title_of(text):
    m = re.search(r"<title[^>]*>(.*?)</title>", text, re.I | re.S)
    return html.unescape(m.group(1)).strip()[:140] if m else ""


def guess_type(url, title=""):
    s = (url + " " + title).lower()
    for t, rx in [("downsell", r"downsell|down-sell|\bds[-_]?\d"), ("upsell", r"upsell|up-sell|\bups[-_]?\d|\boto[-_]?\d?\b|one[-_]?time|upgrade|\bvip\b|special|especial|oferta-unica"),
                  ("thank-you", r"thank|gracias|obrigado|confirm|success"), ("checkout", CHECKOUT_RX.pattern),
                  ("bonus", r"bonus|bono")]:
        if re.search(rx, s):
            return t
    return "page"


def ghl_steps(page_html):
    """Decode GoHighLevel's __NUXT_DATA__ (devalue format) -> funnelSteps list."""
    m = re.search(r'<script[^>]*id="__NUXT_DATA__"[^>]*>(.*?)</script>', page_html, re.S)
    if not m:
        return None
    arr = json.loads(m.group(1))

    def res(v, d=0):
        if d > 14:
            return None
        if isinstance(v, int) and not isinstance(v, bool) and 0 <= v < len(arr):
            return deref(arr[v], d + 1)
        return v

    def deref(x, d=0):
        if isinstance(x, dict):
            return {k: res(v, d) for k, v in x.items()}
        if isinstance(x, list):
            if x and isinstance(x[0], str) and x[0] in ("Reactive", "ShallowReactive", "Ref", "ShallowRef"):
                return res(x[1], d)
            return [res(v, d) for v in x]
        return x

    for x in arr:
        if isinstance(x, dict) and "funnelSteps" in x:
            info = {k: res(x[k]) for k in ("funnelSteps", "funnelNextStep", "funnelName", "domain", "pageUrl") if k in x}
            return info
    return None


def main(sales_url, out, page_jsons, max_probes=60, wayback=True):
    os.makedirs(out, exist_ok=True)
    found, evidence = {}, []

    def add(url, kind, how, **extra):
        k = norm(url)
        e = found.setdefault(k, {"url": url, "type": kind, "how": [], **extra})
        if how not in e["how"]:
            e["how"].append(how)
        e.update({k2: v for k2, v in extra.items() if v})

    base = urllib.parse.urlsplit(sales_url)
    root = f"{base.scheme}://{base.netloc}"
    st, final, home = fetch(root + "/")
    home_hash = hashlib.md5(home.encode()).hexdigest() if home else ""

    # 1. links on the rendered sales pages
    for pj in page_jsons:
        d = json.load(open(pj))
        for l in d.get("links", []) + [b.get("href", "") for b in d.get("blocks", []) if b.get("t") == "cta"]:
            if not l.startswith("http"):
                continue
            if CHECKOUT_RX.search(l):
                add(l, "checkout", "link on sales page")
            elif urllib.parse.urlsplit(l).netloc == base.netloc and re.search(STEP_WORDS, l, re.I):
                add(l, guess_type(l), "link on sales page")

    # 1b. funnel-builder data embedded in the page (GoHighLevel: the whole funnel)
    builder = {}
    for pj in page_jsons:
        ph = os.path.join(os.path.dirname(pj), "page.html")
        if not os.path.exists(ph):
            continue
        page_html = open(ph).read()
        info = ghl_steps(page_html)
        if info and info.get("funnelSteps"):
            dom = info.get("domain") or base.netloc
            builder = {"builder": "gohighlevel", "funnel_name": info.get("funnelName"),
                       "next_step_after_sales": info.get("funnelNextStep"), "steps": info["funnelSteps"]}
            for stp in info["funnelSteps"]:
                u = f"https://{dom}{stp.get('url', '')}"
                add(u, guess_type(stp.get("url", ""), stp.get("name", "")), "GoHighLevel funnel data in page",
                    step_name=stp.get("name"), sequence=stp.get("sequence"), split_test=stp.get("split"))
        for u in set(re.findall(r"https?://[^\s\"'<>\\]+", page_html)):
            if CHECKOUT_RX.search(u) and not re.search(r"\.(js|css|png|jpe?g|webp|svg|woff2?|ttf|eot|ico)(\?|#|$)|leadconnectorhq|filesafe|fonts\.|gstatic", u, re.I):
                add(u, "checkout", "checkout URL inside page code")

    # 2. public indexes
    st, _, robots = fetch(root + "/robots.txt")
    sitemaps = re.findall(r"(?im)^sitemap:\s*(\S+)", robots) or [root + "/sitemap.xml", root + "/wp-sitemap.xml",
                                                                   root + "/sitemap_index.xml"]
    for path in re.findall(r"(?im)^disallow:\s*(\S+)", robots):
        if re.search(STEP_WORDS, path, re.I):
            add(root + path, guess_type(path), "robots.txt Disallow")
    seen_maps, page_urls = set(), set()
    queue = list(sitemaps)
    while queue and len(seen_maps) < 15:
        sm = queue.pop(0)
        if sm in seen_maps:
            continue
        seen_maps.add(sm)
        st, _, xml = fetch(sm)
        if st != 200:
            continue
        locs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", xml)
        for loc in locs:
            if loc.endswith(".xml"):
                queue.append(loc)
            else:
                page_urls.add(loc)
    st, _, wp = fetch(root + "/wp-json/wp/v2/pages?per_page=100&_fields=link,slug,title")
    if st == 200 and wp.startswith("["):
        for p in json.loads(wp):
            page_urls.add(p["link"])
    for u in page_urls:
        add(u, guess_type(u), "site index (sitemap / WordPress)")

    # 3. checkout pages: embedded offers + redirect URLs
    offers = []
    for k, e in list(found.items()):
        if e["type"] != "checkout":
            continue
        st, fin, page = fetch(e["url"])
        e.update(status=st, final_url=fin, title=title_of(page))
        if st != 200:
            continue
        origin = "{0.scheme}://{0.netloc}".format(urllib.parse.urlsplit(fin))
        js = ""
        for src in re.findall(r"<script[^>]+src=\"([^\"]+)\"", page)[:12]:
            src = urllib.parse.urljoin(fin, src)
            if src.startswith(origin):
                js += fetch(src, limit=800_000)[2]
        blob = html.unescape(page) + "\n" + js
        for m in re.finditer(r"(?:upsells?|downsells?|bumps?|bonuses|offers?)\"?\s*(?:value=|:|=)\s*\"?(\[\{.*?\}\])", blob, re.I | re.S):
            try:
                arr = json.loads(m.group(1))
            except Exception:
                continue
            for o in arr:
                if isinstance(o, dict) and (o.get("name") or o.get("title")):
                    offers.append({"checkout": fin, "name": o.get("name") or o.get("title"),
                                   "price": o.get("price"), "original_price": o.get("originalPrice") or o.get("original_price"),
                                   "image": o.get("mockup") or o.get("image"), "billing": o.get("billing_type"),
                                   "where": "embedded in checkout (order bump / upsell list)"})
        for u in set(re.findall(r"https?://[^\s\"'<>\\]+", blob)):
            if re.search(r"upsell|\boto|downsell|thank|gracias|obrigado|success|post[-_]?purchase", u, re.I) and not re.search(r"\.(js|css|png|jpe?g|webp|svg|woff2?)(\?|$)|fonts\.|gstatic|googleapis|cdn\.|jsdelivr|unpkg", u, re.I):
                add(u, guess_type(u), "referenced by checkout code")
        flow = re.search(r"id=\"upsells-flow\"\s+value=\"([^\"]*)\"", page)
        if flow:
            e["upsell_flow"] = flow.group(1)
        if re.search(r"downsell", blob, re.I):
            e["supports_downsell"] = True

    # 4. bounded slug probing next to the sales path and at the root
    sales_dir = base.path.rstrip("/").rsplit("/", 1)[0]
    stem = base.path.strip("/").split("/")[-1]
    cands = []
    for s in SLUGS:
        cands += [f"{root}/{s}", f"{root}{sales_dir}/{s}", f"{root}/{stem}-{s}", f"{root}/{stem}/{s}"]
    probes = 0
    for c in dict.fromkeys(cands):
        if probes >= max_probes or norm(c) in found:
            continue
        probes += 1
        st, fin, page = fetch(c, timeout=12, limit=400_000)
        if st != 200 or not page or page.startswith("ERR"):
            continue
        h = hashlib.md5(page.encode()).hexdigest()
        t = title_of(page)
        if h == home_hash or norm(fin) == norm(root + "/") or SOFT404.search(t):
            continue
        add(fin, guess_type(fin, t), "slug probe", status=st, title=t)

    # 5. Wayback Machine
    if wayback:
        st, _, cdx = fetch(f"https://web.archive.org/cdx/search/cdx?url={base.netloc}/*&output=json&fl=original,statuscode"
                           f"&filter=statuscode:200&collapse=urlkey&limit=3000", timeout=40)
        if st == 200 and cdx.startswith("["):
            for row in json.loads(cdx)[1:]:
                if re.search(STEP_WORDS, row[0], re.I) and not re.search(r"\.(js|css|png|jpe?g|webp|svg|ico|xml|json)(\?|$)", row[0], re.I):
                    add(row[0], guess_type(row[0]), "Wayback Machine (may be old)")
        else:
            evidence.append("wayback unavailable")

    # verify every non-checkout candidate once (status + title)
    for k, e in found.items():
        if "status" in e or e["type"] == "checkout":
            continue
        st, fin, page = fetch(e["url"], timeout=12, limit=400_000)
        e.update(status=st, final_url=fin, title=title_of(page))

    result = {"sales_url": sales_url, "root": root, "builder_funnel": builder,
              "pages": sorted(found.values(), key=lambda e: (e.get("sequence") or 99, e["type"])),
              "embedded_offers": offers, "probes_used": probes, "notes": evidence}
    with open(os.path.join(out, "funnel_map.json"), "w") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    live = [e for e in found.values() if e.get("status") == 200]
    return {"ok": True, "pages_found": len(found), "live": len(live),
            "by_type": {t: sum(1 for e in live if e["type"] == t) for t in sorted({e["type"] for e in live})},
            "embedded_offers": len(offers), "builder_steps": len(builder.get("steps", [])),
            "map": os.path.join(out, "funnel_map.json")}


if __name__ == "__main__":
    args, pjs, opts = [], [], {"max_probes": 60, "wayback": True}
    it = iter(sys.argv[1:])
    for a in it:
        if a == "--page-json":
            pjs.append(next(it))
        elif a == "--max-probes":
            opts["max_probes"] = int(next(it))
        elif a == "--no-wayback":
            opts["wayback"] = False
        else:
            args.append(a)
    try:
        print(json.dumps(main(args[0], args[1], pjs, **opts)))
    except Exception as e:
        print(json.dumps({"ok": False, "error": f"{type(e).__name__}: {e}"}))
