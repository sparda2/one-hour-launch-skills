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
  /* Toast de compra en vivo: SOLO pedidos reales recientes. Vacío = nunca se muestra. */
  proof: { live: [] }          /* e.g. ["Ana from Bogotá just got access", …] */
};
