/* Per-project config read by assets/kit/funnel.js. One file per funnel.
 * Only set values that are REAL — the kit hides any trigger whose data is absent. */
window.FUNNEL = {
  /* Where each CTA goes. The checkout is the seller's real payment URL. */
  cta: {
    checkout: "https://YOUR-CHECKOUT-URL",   /* replace with the real checkout */
    accept:   "upsell-1.html",
    decline:  "downsell-1.html",
    next:     "thank-you.html"
  },
  bar: { text: "Launch price — ends when the launch closes" },
  /* Real deadline only (ISO). Leave null for no countdown — never a per-visit timer. */
  deadline: null,              /* e.g. "2026-10-31T23:59:00-05:00" */
  /* Live-purchase toast. Empty = hidden. */
  proof: { live: [] },         /* e.g. ["Ana from Bogotá just got access", …] */
  /* Tab-away attention: titles cycled in the browser tab when the visitor
     switches away (and an optional favicon). Leave out to use the defaults. */
  tabAway: { titles: ["👋 Wait! Don’t go…", "🔥 Your offer is still here", "← Come back 💚"] },
  /* Anti-copy speed bump: blocks right-click + view-source/devtools shortcuts.
     Deters casual copying only; set true to enable. */
  antiCopy: false
};
