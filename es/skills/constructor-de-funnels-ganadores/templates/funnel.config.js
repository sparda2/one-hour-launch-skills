/* Config por proyecto que lee assets/kit/funnel.js. Un archivo por funnel.
 * Pon solo valores REALES — el kit oculta cualquier gatillo sin datos. */
window.FUNNEL = {
  /* A dónde va cada CTA. El checkout es la URL de pago real del vendedor. */
  cta: {
    checkout: "https://YOUR-CHECKOUT-URL",   /* reemplaza con el checkout real */
    accept:   "upsell-1.html",
    decline:  "downsell-1.html",
    next:     "thank-you.html"
  },
  bar: { text: "Precio de lanzamiento — termina cuando cierra el lanzamiento" },
  /* Solo deadline real (ISO). null = sin countdown — nunca un timer por visita. */
  deadline: null,              /* e.g. "2026-10-31T23:59:00-05:00" */
  /* Toast de compra en vivo. Vacío = oculto. */
  proof: { live: [] },         /* p. ej. ["Ana de Bogotá acaba de obtener acceso", …] */
  /* Atención al cambiar de pestaña: títulos que rotan en la pestaña del navegador. */
  tabAway: { titles: ["👋 ¡Espera! No te vayas…", "🔥 Tu oferta sigue aquí", "← Vuelve 💚"] },
  /* Speed bump anti-copia: bloquea clic derecho + atajos de ver-código/devtools.
     Solo disuade copia casual; pon true para activarlo. */
  antiCopy: false
};
