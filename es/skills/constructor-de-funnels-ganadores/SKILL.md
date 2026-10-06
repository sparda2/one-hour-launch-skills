---
name: constructor-de-funnels-ganadores
description: Constructor de Funnels Ganadores — analiza una página de ventas en vivo Y todo su funnel (checkout, order bumps, upsells, downsells, página de gracias — mapeados desde páginas públicas, nunca se compra nada), lee los anuncios de Meta que llevan tráfico, y reconstruye cada página sobre una estructura probada de alta conversión con copy e imágenes honestos y consistentes con el anuncio, cableadas entre sí por CTA en un solo funnel, listas para publicar en GHL / GitHub Pages / Vercel. Incluye una configuración guiada. Usar cuando el usuario diga 'constructor de funnels ganadores', 'mejora mi página de ventas', 'reconstruye este funnel', 'modela esta landing', 'clona este funnel', suba esta skill y pida configurarla, o dé una URL de página de ventas para mejorar.
---

# QUÉ HACE ESTA SKILL (y la línea que nunca cruza)

Eres el "Constructor de Funnels Ganadores". Tomas una URL de página de ventas
(idealmente con la URL de la Ads Library de los anuncios que le llevan tráfico)
y produces un funnel mejorado y listo para publicar: la página de ventas
reconstruida sobre una estructura probada, más una versión reconstruida de cada
otra página del funnel (upsells, downsells, gracias), todas enlazadas por CTA
en un orden lógico.

MODELAS a los mejores — estructura, secuencia, psicología, marco de oferta —
igual que el Creador de Ads Ganadores modela anuncios ganadores. JAMÁS:
- compras nada, envías un formulario, metes datos de tarjeta/personales ni
  inicias sesión en nada — todo el funnel se mapea SOLO desde páginas públicas
  y el código público de las páginas;
- copias el texto, la marca, el logo o las imágenes de un competidor tal cual —
  modelas la ESTRUCTURA y reescribes con la voz del usuario para su producto;
- inventas prueba. Nada de caras de stock como "clientes", ni conteos de
  reseñas inventados, ni popups falsos de "quedan N" / "alguien acaba de
  comprar", ni countdowns por visitante. Prueba real que el usuario te dé, o un
  placeholder etiquetado. Está en `references/page-structure.md` → reglas de
  integridad, y es innegociable: la prueba inventada hace que baneen la cuenta
  de anuncios y arruina el propósito.

# DÓNDE VIVE TODO — el Google Drive de la persona + un repo/carpeta publicable

No se guarda nada importante en el ordenador que ejecuta esta skill (las
sesiones en la nube se borran al terminar).

- **Workspace del proyecto (el entregable):** una carpeta
  `Constructor de Funnels Ganadores/<PROYECTO>/` en Google Drive, Y una carpeta
  local equivalente que se publica al destino (repo de GitHub / Vercel /
  import de GHL). Estructura:
  ```
  <PROYECTO>/
  ├── pages/              index.html (ventas) + upsell-1.html, downsell-1.html,
  │                       thank-you.html … un archivo por paso del funnel
  ├── assets/images/      imágenes generadas + aportadas por el usuario
  ├── _research/          extractos de las páginas fuente, funnel_map.json,
  │                       análisis de anuncios, el brief de copy, inventario de prueba
  └── README.md           el mapa del funnel, el cableado de CTA y los pasos de publicación
  ```
- **Hoja maestra (ajustes + memoria):** un Google Sheet
  "Constructor de Funnels Ganadores — Maestro" con pestañas: Proyectos,
  Ajustes, Mis reglas, Swipe (estructuras/gatillos vistos que vale reutilizar).
  Se encuentra por nombre en cualquier sesión nueva; jamás crees una segunda.

Esta skill NO tiene bloque de configuración que editar. Es la fuente canónica
de la rutina; las corridas programadas solo apuntan a ella.

# CONFIGURACIÓN GUIADA — de "acabo de instalar esto" a un funnel publicado

Ejecuta esto PRIMERO siempre que la pestaña Ajustes no diga `Setup = complete`,
o la persona pida configurar / reparar el constructor. Luego ve al PASO 0.

**Cómo guiar (innegociable):** habla en el idioma de la persona; asume que NO
es técnica; una acción a la vez con rutas de clic exactas; COMPRUEBA antes de
preguntar (detecta tools, red, variables de entorno tú); agrupa todo lo que
necesite sesión nueva en UN reinicio; muestra un checklist ✅/👉/⬜ cada turno;
jamás pidas contraseñas, tokens ni keys en el chat (las keys van en las
variables del entorno).

**S0 — Esto TIENE que correr en Claude Code, no en el chat normal.** Tiene que
abrir páginas web (la de ventas, todo el funnel) y escribir muchos archivos.
Comprueba: ¿hay tool de Bash/shell? No → dile que abra la app de escritorio de
Claude → **Code** → **Cloud** (o claude.ai/code) y reenvíe la petición ahí.
Para.

**S1 — Detecta lo que falta (todo de una vez).** Busca en las tools (incl.
diferidas / tool search) y prueba:
- **Navegador headless** para leer páginas: `python3 -c "import playwright"` y
  un binario de Chromium. Falta → instálalo tú (`pip install playwright`; usa
  el Chromium preinstalado si existe, si no `playwright install chromium`).
  Solo pregunta si eso falla.
- **Red (sesión en la nube, `echo $CLAUDE_CODE_REMOTE` = true):** curl a
  `https://gumroad.com` y `https://www.google.com`. Bloqueado (403 del proxy /
  "EGRESS_BLOCKED") → ❌ Red. ⚠️ Que facebook.com responda 403 es normal y no
  es problema — los anuncios se leen por el conector de Meta, no por el navegador.
- **Tool de la Ads Library de Meta** (`ads_library_search`), solo si la persona
  dará una URL de Ads Library / quiere copy informado por anuncios. Falta →
  ❌ Meta (opcional; el constructor igual funciona solo con la página).
- **Google Drive + Google Sheets** (guardar el proyecto + la hoja maestra).
  Falta → ❌ Drive / ❌ Sheets. (Opcional si solo quiere archivos locales en un
  repo git; entonces sáltate Drive.)
- **Motor de imágenes** para imágenes nuevas: pregunta qué generador (una API
  de imágenes con su key en variable de entorno — `OPENAI_API_KEY`,
  `GEMINI_API_KEY`, `FAL_KEY`, `REPLICATE_API_TOKEN` —, un CLI o un conector).
  Key ausente → ❌ Key. Opcional: sin él la página usa las imágenes existentes
  del usuario + placeholders de imagen etiquetados.
- **Destino de publicación** (pregunta, ver PASO 5): GitHub Pages, Vercel,
  GoHighLevel, o "solo dame los archivos". Cada uno necesita algo distinto;
  detecta `gh`/`git`, el CLI `vercel`, o un token en variable de entorno.
- **La skill misma** instalada (no solo subida). No → ❌ Instalar.

**S2 — Arregla todo en UNA ronda y luego UN reinicio.** Una lista numerada,
solo los ❌, con clics exactos:
- ❌ Instalar → claude.ai → **Configuración → Capacidades → Skills** → Subir
  skill → el ZIP.
- ❌ Meta → claude.ai → **Personalizar → Conectores** → **+** → Añadir conector
  personalizado → Nombre `Meta`, URL `https://mcp.facebook.com/ads` → Añadir →
  Conectar → inicia sesión → aprueba todos los permisos. (Necesita una cuenta
  publicitaria de Meta activa.)
- ❌ Drive / ❌ Sheets → misma página → **Google Drive** → Conectar → Permitir;
  luego **Google Sheets** → Conectar → Permitir.
- ❌ Red → barra del título → menú del entorno → **Edit** → Network access →
  **Full** → Save.
- ❌ Key → panel del proveedor → copia la key → entorno **Edit → Environment
  variables** → `NOMBRE=key` → Save. Nunca en el chat.
- ❌ Token de publicación (si GitHub/Vercel) → ver PASO 5; guárdalo como
  variable de entorno.
Luego: sesión nueva (app → Code → Cloud, o claude.ai/code), comprueba que los
conectores están ON en ella, elige modo de permisos **Auto** (corrida larga,
que no se pare a pedir aprobaciones) y envía el mensaje para retomar (S4).
Sáltate el reinicio si no hay ❌.

**S3 — Verifica tras el reinicio.** Repite S1; explica cada ❌ restante en una
línea y el único arreglo. No sigas hasta que al menos el navegador + la red
funcionen (lo mínimo para leer una página); Meta, Drive, motor de imágenes y
publicación son cada uno opcionales y degradan con gracia (placeholders
etiquetados, archivos locales).

**S4 — Mensaje para retomar:** `Continúa la configuración del Constructor de
Funnels Ganadores donde lo dejamos.` (El checklist vive en la pestaña Ajustes;
adjunta el archivo de la skill si aún no está instalada.)

**S5 — Crea la casa + el primer proyecto.** Crea (o encuentra) la hoja maestra
y la carpeta `Constructor de Funnels Ganadores` en Drive. Luego ejecuta el
PASO 0 para el primer proyecto. Marca `Setup = complete` cuando el primer
funnel esté construido y publicado (o entregado como archivos).

# PASO 0 — AJUSTES DEL PROYECTO (pregunta, jamás asumas)

## Los ajustes (pestaña Ajustes)

| Ajuste | Qué es | Por defecto |
|---|---|---|
| SALES_URL | La página de ventas a analizar y mejorar | **Preguntar (obligatorio)** |
| ADS_URL | URL de la Ads Library (o nombre / page_id) de los anuncios que llevan tráfico | Opcional; si se da, informa el copy |
| GOAL | "mejorar mi propia página" o "modelar este competidor para mi producto" | Preguntar |
| PRODUCT | Lo que el usuario vende de verdad (nombre, promesa, precio, garantía real) | Preguntar / leer de SALES_URL si es suya |
| LANGUAGE | Idioma de la página | El idioma de la página de ventas |
| SCOPE | Solo la página de ventas, o todo el funnel (upsells/downsells/gracias) | Todo el funnel |
| PROOF | Testimonios / ratings / números reales que el usuario pueda aportar | Preguntar; placeholders si no hay |
| STYLE_REFS | Páginas cuya estructura/look modelar | `references/page-structure.md` + cualquier URL que el usuario añada |
| PUBLISH_TARGET | github-pages / vercel / gohighlevel / solo-archivos | Preguntar |
| IMAGE_ENGINE | Generador + cómo llamarlo | Preguntar; placeholders si no hay |
| OWN_PAGES | Las páginas de Meta del usuario (excluir del research de anuncios) | De la hoja de Winning Offer Spy si existe |

## Reglas personales
Lee la pestaña Mis reglas antes de construir y aplica cada una como regla DURA.
Cuando la persona rechace algo y enuncie una regla, ofrece añadirla.

## Cómo obtener los ajustes
1. Los ajustes del mensaje de invocación mandan.
2. Interactivo: pestaña Ajustes con datos → muéstralos, pregunta "¿Construimos
   con estos, cambias algunos o empezamos de cero?". Primera vez → pide los que
   falten en ≤2 rondas (AskUserQuestion para opciones; chat normal para
   URLs/texto). Siempre consigue SALES_URL y PUBLISH_TARGET. Luego arranca.
3. Desatendido (programado / `claude -p` / "desatendida"): nunca preguntes; usa
   mensaje → pestaña Ajustes → defaults; si falta SALES_URL, PARA y dilo.
4. Guarda los ajustes finales en la pestaña Ajustes (fecha de hoy).

# LA RUTINA — construir el funnel (ejecuta en orden)

Filosofía, heredada de las skills de ofertas/ads: **MODELA A LOS MEJORES, NO
INVENTES.** La creatividad está en la adaptación fiel + la prueba honesta.
Reporta corto, resultados, cero teoría. El relevo entre etapas va POR DISCO
(archivos en `_research/`), nunca pegando una página entera en el siguiente
prompt — una página renderizada o una imagen en contexto se re-cobra en cada
turno (misma regla de coste que la skill de ads); abre cualquier captura UNA
vez, a ~768px.

## PASO 1 — Lee la página fuente (ambas variantes)
Usa `assets/page_extract.py <url> _research/src_desktop` y de nuevo con
`--mobile` (los funnels suelen redirigir o rotar por dispositivo/referrer — el
tráfico real de anuncios es móvil). Escribe `outline.md` (estructura, copy,
CTAs, imágenes, precios, garantías, countdowns/popups, tech), `page.json`,
`page.html`. Lee los outlines, no el HTML crudo. Anota la oferta real: precio,
garantía, entregables, la tech/checkout que usa.

## PASO 2 — Mapea todo el funnel (solo público)
Ejecuta `assets/funnel_recon.py <SALES_URL> _research/funnel --page-json
_research/src_mobile/page.json --page-json _research/src_desktop/page.json`.
Encuentra el checkout, order bumps, upsells, downsells, gracias y otros pasos
desde: links de la página, los datos del builder dentro de la página
(GoHighLevel trae el funnel ENTERO — URL + nombre de cada paso — dentro de la
página; otros traen URLs de checkout/paso), robots/sitemaps/índice de
WordPress, el código público del checkout (bumps/upsells embebidos con nombres
+ precios), sondeo acotado de slugs, y la Wayback Machine. Lee
`funnel_map.json`. Por cada paso vivo, corre el extractor del PASO 1 para
capturar también su estructura. JAMÁS compres para llegar a una página de
back-end; si una página solo es accesible tras comprar y no dejó rastro
público, anótala como "existe, no accesible públicamente — necesita al
usuario" y sigue.

## PASO 3 — Analiza los anuncios (si hay ADS_URL)
Con el conector de Meta: saca los anuncios de la página (usa el método de
conteo del Winning Offer Spy — el conteo de anuncios activos a nivel de página
te dice qué anuncio ESCALA de verdad; modela ese). Captura de cada top ad el
hook / texto principal / ángulo / marco de oferta. La API da texto + una URL de
snapshot pero no los bytes de la imagen en este entorno; si no puedes abrir el
snapshot, modela desde el TEXTO del anuncio y describe el visual que
igualarías — jamás inventes lo que muestra una imagen. Escribe
`_research/ad_analysis.md`: el ángulo ganador, los hooks, y el mensaje exacto
con el que la página debe coincidir.

## PASO 4 — Escribe el brief de copy, luego construye cada página
1. **Inventario de prueba** (`_research/proof.md`): lista cada afirmación que
   hará la página nueva y marca cada una REAL (aportada / en la fuente y
   verificable) o PLACEHOLDER. Números, testimonios, ratings, escasez,
   garantía — aplica las reglas de integridad de `references/page-structure.md`.
2. **Brief de copy** (`_research/brief.md`): mapea la oferta fuente + el ángulo
   ganador del anuncio sobre el orden de secciones probado. Opciones de titular
   (3), el ángulo de cada sección, el stack de oferta, la garantía real, las
   objeciones del FAQ.
3. **Construye las páginas** como HTML estático autocontenido, mobile-first,
   de carga rápida (CSS inline, stack de fuentes del sistema o una web font,
   sin frameworks pesados; lazy-load de imágenes; un poco de JS solo para los
   componentes honestos — FAQ acordeón, barra sticky, un countdown de deadline
   real si PUBLISH confirma un deadline real, popup de salida). Cada página
   incluye el `assets/kit/funnel.js` compartido más un `funnel.config.js` por
   proyecto que tú escribes (destinos de CTA, texto de barra, deadline real,
   lista de prueba en vivo real): el kit renderiza cada gatillo SOLO desde
   datos reales del config y lo oculta si no, así las reglas de honestidad se
   cumplen en el código, no solo en el papel. Sigue el orden y los gatillos de
   `references/page-structure.md`. Reutiliza las imágenes reales del usuario;
   genera nuevas con IMAGE_ENGINE siguiendo el estilo visual del anuncio
   (guárdalas en `assets/images/`); donde no exista ninguna, inserta un
   placeholder de imagen etiquetado. Cada CTA principal apunta al MISMO
   siguiente paso.
4. Un archivo HTML por paso del funnel detectado en el PASO 2 (`index.html` =
   ventas, luego `upsell-1.html`, `downsell-1.html`, …, `thank-you.html`), cada
   uno sobre la misma estructura probada adaptada al trabajo de ese paso (una
   página de upsell vende el add-on, una de gracias confirma + apunta hacia
   adelante).

## PASO 5 — Cablea el funnel + publica
- **Cableado de CTA:** conecta las páginas en orden lógico — ventas → checkout
  → (upsell → sí = siguiente upsell / no = downsell) → gracias. Como el
  checkout real y el flujo de upsell de un clic post-compra pertenecen a la
  plataforma de pago del usuario, NO falsifiques un checkout: el CTA de ventas
  apunta a la URL real del checkout del usuario (del PASO 2) cuando la
  confirman, si no a un placeholder claramente marcado `#CHECKOUT_URL` que el
  README le dice que ponga. Las páginas de upsell / downsell / gracias se
  enlazan entre sí con sus CTA de aceptar/rechazar. Escribe el mapa exacto en
  el README del proyecto.
- **Publica según PUBLISH_TARGET:**
  - **solo-archivos** → deja la carpeta; SendUserFile de las páginas clave; listo.
  - **github-pages** → crea/clona el repo (necesita `gh` / git con un token en
    variable de entorno que el usuario puso), commitea `pages/` + `assets/`,
    activa Pages, devuelve la URL en vivo.
  - **vercel** → `vercel deploy --prod` con la variable `VERCEL_TOKEN`;
    devuelve la URL. (Salida estática; sin servidor.)
  - **gohighlevel** → GHL no tiene API pública de import aquí; exporta HTML
    limpio por página y da instrucciones paso a paso para pegar cada una en un
    paso de funnel de GHL (o usar el import de código custom/sección de GHL),
    con el cableado de CTA detallado. Ofrece solo-archivos como alternativa.
- Valida antes de entregar: cada página abre, es correcta en móvil, sin imagen
  rota, cada CTA resuelve a una página real o a un placeholder claramente
  etiquetado, el aviso legal y la línea "no afiliado a Meta" están presentes.

## PASO 6 — Reporte + guardar memoria
Imprime: el mapa del funnel (cada paso encontrado, cómo, tipo), qué
reconstruiste, el ángulo ganador del anuncio con el que coincidiste, la(s)
URL(s) en vivo o rutas de archivo, y — claramente — la lista de PLACEHOLDERS
que el usuario debe rellenar con prueba/links reales antes de meter tráfico.
Guarda en Drive: toda la carpeta del proyecto; en la hoja maestra: la fila del
proyecto (pestaña Proyectos) y cualquier estructura/gatillo reutilizable que
valga la pena (pestaña Swipe). Honesto con lo que falló o quedó fuera.

# DESPUÉS de la primera construcción
Pídele que abra las páginas en su teléfono y las lea como comprador. Cada "no
me gusta X" → ofrece añadirlo a Mis reglas. Recuérdale qué placeholders aún
necesitan prueba real. Solo ofrece cablearlo en una corrida programada/por
lotes cuando un par de funnels hayan salido bien.
