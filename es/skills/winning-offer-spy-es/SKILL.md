---
name: winning-offer-spy-es
description: Winning Offer Spy — caza ofertas que están escalando ahora mismo en la biblioteca de anuncios de Meta según tu filtro de formato, y las registra con su histórico en un Google Sheet maestro en tu Google Drive (ajustes, banco de keywords y tus reglas viven ahí también). Incluye una configuración guiada que lleva a cualquiera de "acabo de instalar esto" a su primera caza. Usar cuando el usuario diga 'cazar ofertas', 'winning offer spy', 'buscar ofertas escalando', 'configura winning offer spy', suba esta skill y pida configurarla, o pida el barrido de la hoja maestra.
---

# DÓNDE VIVE TODO — un solo Google Sheet en el Drive de la persona

No se guarda nada en el ordenador que ejecuta esta skill (las sesiones en la
nube se borran al terminar). TODO vive en UN Google Sheet llamado
**"Winning Offer Spy — Maestro"**, dentro de una carpeta de Drive llamada
**"Winning Offer Spy"**:

| Pestaña | Qué guarda |
|---|---|
| Ofertas | Las ofertas verificadas (ver "Actualizar la hoja maestra") |
| Pendientes | Prometedoras sin verificar / bajo umbral + huecos 💡 |
| Histórico | fecha \| ID \| producto \| ads de hoy |
| Log de búsquedas | fecha \| keywords usadas \| resultados útiles (+ hora de inicio de cada corrida) |
| Keywords | keyword \| categoría \| idioma \| círculo \| ángulo \| estado (nueva / caliente / quemada) — el BANCO DE KEYWORDS |
| Ajustes | ajuste \| valor \| última actualización — las respuestas de la persona + el checklist de configuración |
| Mis reglas | regla \| añadida el — las reglas extra de la persona |

**Encontrarlo en una sesión nueva:** busca en Drive el nombre exacto
"Winning Offer Spy — Maestro". Una coincidencia → úsala. Varias → pregunta
cuál. Ninguna → configuración de primera vez. Jamás crees una segunda hoja
maestra.

Esta skill NO tiene bloque de configuración que editar. Esta skill es la
fuente canónica de la rutina: las corridas programadas solo apuntan a ella.
Editar la rutina = editar este archivo.

# CONFIGURACIÓN GUIADA — de "acabo de instalar esto" a la primera caza

Ejecuta esta sección PRIMERO siempre que no exista aún la hoja maestra, o su
pestaña Ajustes no diga `Setup = complete`, o la persona pida configurar /
reparar Winning Offer Spy. Con la configuración completa, ve directo al PASO 0.

**Cómo guiar (innegociable):**
- Habla en el idioma de la persona. Asume que NO es técnica: una acción a la
  vez, la ruta exacta de clics, qué va a ver y cómo saber que funcionó.
- COMPRUEBA antes de preguntar: detecta tú todo lo que puedas (tools, red).
  Pide a la persona solo lo que no puedes detectar ni hacer.
- Agrupa todo lo que necesite una sesión NUEVA en UN solo reinicio (los
  conectores y los cambios de red solo se cargan al iniciar sesión). Jamás le
  hagas reiniciar dos veces si uno bastaba.
- Muestra el progreso en cada turno como checklist corto: ✅ hecho, 👉 ahora,
  ⬜ siguiente.
- Jamás pidas contraseñas, tokens ni API keys en el chat.

**S1 — Detecta lo que falta (todo de una vez).** Busca en las tools
disponibles (incluidas las diferidas / tool search) y prueba:
- **Tool de la Ads Library de Meta** (p. ej. `ads_library_search`; el nombre
  varía según el conector). Falta → ❌ Meta. Haz una consulta canary ('shoes',
  US, activos): un error sobre la cuenta publicitaria → ❌ Cuenta publicitaria
  (Meta solo abre la tool de la Ads Library a quien tiene al menos una cuenta
  publicitaria ACTIVA).
- **Tools de Google Drive** que puedan buscar en Drive, crear un Google Sheet
  y leer/escribir sus celdas. Faltan → ❌ Drive.
- **Red (solo en una sesión en la nube de Claude Code, `echo
  $CLAUDE_CODE_REMOTE` = true):** abre `https://www.facebook.com/ads/library/`
  y un sitio cualquiera fuera de la lista permitida (p. ej.
  `https://gumroad.com`). Bloqueado → ❌ Red. (Las landings de la competencia
  pueden estar en cualquier dominio.)
- **La skill misma** queda instalada para la próxima vez: aparece como skill
  disponible (no solo como archivo subido a este chat). Si solo se subió el
  archivo → ❌ Instalar.

**S2 — Arregla todo en UNA ronda y luego UN reinicio.** Una lista numerada
solo con los ❌:
- ❌ Instalar → claude.ai → Configuración → Capacidades → Skills → "Subir
  skill" → elige el ZIP de la skill (del pack). Las skills subidas ahí están
  disponibles en la app de Claude Y en las sesiones en la nube de Claude Code
  de la misma cuenta.
- ❌ Meta → claude.ai → Configuración → Conectores
  (claude.ai/customize/connectors) → busca el conector de Meta Ads en el
  directorio, o "Add custom connector" con la URL de su servidor MCP de Meta →
  Connect → inicia sesión en Meta → aprueba.
- ❌ Cuenta publicitaria → business.facebook.com → crea o reactiva una cuenta
  publicitaria (debe estar activa; normalmente pide un método de pago).
- ❌ Drive → misma página → Google Drive → Connect → elige su cuenta de Google
  → permite el acceso.
- ❌ Red → en la barra del título de la sesión de Claude Code, abre el menú del
  entorno → Edit → Network access → **Full** → Save.
Luego dile que abra una sesión NUEVA (app de escritorio de Claude → Code →
Cloud, o claude.ai/code) y envíe el mensaje para retomar (S7). Si no hay
ningún ❌, sáltate el reinicio.

**S3 — Verifica tras el reinicio.** Repite S1. Si algo sigue en ❌ → explica
la causa más probable en una línea (p. ej. "el conector se añadió después de
abrir esta sesión") y el único arreglo. No sigas hasta que Meta Y Drive
funcionen (sin Meta no hay caza; sin Drive no hay dónde guardar).

**S4 — Crea la casa.** Busca en Drive "Winning Offer Spy — Maestro".
Ninguna → crea la carpeta "Winning Offer Spy" y dentro la hoja maestra con
las 7 pestañas y sus encabezados (negrita, color, fijados, filtros activos).
Lee los encabezados de vuelta para confirmar que la escritura funcionó. Dale
el link a la persona.

**S5 — Ajustes.** Ejecuta PASO 0 → "Cómo obtener los ajustes" (preguntas de
primera vez, máximo 2 rondas) y guarda las respuestas en la pestaña Ajustes.
Ayuda a afinar TU_FILTRO y NICHOS_CIRCULOS si son vagos; jamás los inventes.
Para PAGINAS_PROPIAS, enséñale a sacar el page_id (Ads Library → busca su
página → clic → la URL muestra `view_all_page_id=NÚMERO`) o búscalos por
nombre con la tool de Meta y confírmalos con la persona.

**S6 — Prueba rápida (2 minutos, antes de la caza real).**
- Meta: una consulta canary (p. ej. 'shoes', US, activos). Resultados > 0 → ✅.
- Keywords: genera el BANCO DE KEYWORDS en la pestaña Keywords (PASO 0 → 5).
Escribe `Setup = complete` en la pestaña Ajustes y di: "Configuración lista.
Empiezo tu primera caza ahora (20-40 min). Puedes cerrar esta ventana — sigue
corriendo en la nube." y ve a LA RUTINA.

**S7 — Mensaje para retomar (dalo cada vez que haga falta reiniciar):**
`Continúa la configuración de Winning Offer Spy donde lo dejamos.`
(El checklist vive en la pestaña Ajustes, así que la sesión nueva retoma
desde ahí. Si la skill aún no está instalada, adjunta el archivo de la skill
a ese mensaje.)

**Después de la primera caza:** pídele que valide 2-3 hallazgos a mano (link
de biblioteca: ¿de verdad tantos anuncios activos? landing: ¿de verdad un
producto descargable con checkout directo?). Si los hallazgos no encajan con lo
que puede hacer, su filtro está flojo → ofrece "cambiar algunos" y endurécelo.
Por último, ofrece programar la corrida diaria (modo desatendido) — solo
cuando le hayan convencido 2-3 corridas.

# PASO 0 — AJUSTES DE LA CAZA (pregunta, jamás asumas)

## Los ajustes (guardados en la pestaña Ajustes)

| Ajuste | Qué es | Por defecto si a la persona le da igual |
|---|---|---|
| TU_FILTRO | El formato de producto que la persona puede replicar. Solo se registra lo que lo pase. P. ej. "toolkits digitales descargables de ticket bajo (guías PDF, plantillas, packs de prompts) que pueda producir con IA en días; nada de cursos en video, coaching ni servicios" | **Ninguno — hay que preguntarlo** |
| NICHOS_CIRCULOS | Círculo 1 = nichos actuales; 2 = mismo comprador, otros temas; 3 = adyacentes. 3-5 por círculo. La caza va en ese orden | **Ninguno — hay que preguntarlo** |
| PAGINAS_PROPIAS | Las páginas de Facebook de la persona (nombres o page_id), EXCLUIDAS de la caza | Preguntar; "ninguna" solo si la persona lo dice |
| IDIOMAS | Idiomas en los que buscar | Todos, inglés primero |
| MINIMO_ADS | Anuncios activos del mismo producto para considerarlo "escalando" | 15 |
| PISO_DIARIO | Hallazgos nuevos verificados mínimos por corrida | 5 |

## Reglas personales

Lee la pestaña Mis reglas antes de empezar y aplica cada regla como regla
DURA adicional de esta corrida. Es cómo la persona añade sus propias lecciones
sin editar esta skill (las actualizaciones del pack sobrescribirían los
cambios aquí). Si una regla personal contradice una de esta skill, sigue la
personal y menciónalo en el resumen final. Cuando la persona rechace algo y
enuncie una regla, ofrece añadirla a la pestaña Mis reglas.

## Cómo obtener los ajustes

1. **Los ajustes del mensaje de invocación mandan.** P. ej. `/winning-offer-spy-es
   nichos: planes keto, mínimo 10 ads` → úsalos directamente y no los vuelvas a
   preguntar.
2. **Corrida interactiva (hay una persona en el chat):**
   - Pestaña Ajustes con datos → muestra los ajustes guardados en UNA tabla
     compacta y haz UNA pregunta: "¿Cazamos con estos, cambias algunos o
     empezamos de cero?"
   - Pestaña Ajustes vacía (primera vez) → pide los ajustes que falten en COMO
     MÁXIMO 2 rondas. Usa la tool AskUserQuestion si está disponible para los
     de opción (IDIOMAS, MINIMO_ADS, PISO_DIARIO) y chat normal para los de
     texto libre (TU_FILTRO, NICHOS_CIRCULOS, PAGINAS_PROPIAS). Da el ejemplo
     de la tabla con cada pregunta. Ofrece los valores por defecto; jamás
     inventes TU_FILTRO ni NICHOS_CIRCULOS — si son vagos, ayuda a afinarlos.
   - Después imprime la tabla final de ajustes y ARRANCA la caza (sin otra
     ronda de confirmación).
3. **Corrida desatendida (tarea programada, Grok Bot, `claude -p` headless, o
   el mensaje dice "desatendida"/"unattended"):** NUNCA preguntes — no hay
   nadie para responder. Usa los ajustes del mensaje, completa con la pestaña
   Ajustes y luego con los valores por defecto. Si no se encuentra la hoja
   maestra, o aún faltan TU_FILTRO o NICHOS_CIRCULOS: PARA sin cazar e
   imprime qué falta más un comando de ejemplo que lo incluya.
4. **Guarda** los ajustes finales en la pestaña Ajustes (con la fecha de hoy)
   antes de empezar.
5. **Banco de keywords:** si la pestaña Keywords está vacía, genera 100+
   keywords por círculo de nicho × IDIOMAS, ángulos consumidor Y profesional,
   keywords de DOCUMENTO para B2B (checklist, plantilla, protocolo, ficha), y
   escríbelas ahí. Tras cada corrida, marca las keywords usadas como calientes
   (resultados útiles) o quemadas (nada útil) — esa ES la lista negra del Log.
6. **Pre-vuelo (cada corrida):** la tool de la Ads Library de Meta y la
   escritura en Drive deben funcionar ANTES de cazar. Si alguna falla, PARA y
   di exactamente qué arreglar (S1-S2) — jamás caces para luego perder los
   resultados, y jamás inventes conteos.

# LA RUTINA

Eres el "Winning Offer Spy". Ejecuta la rutina diaria completa desde
la hoja maestra. Objetivo: encontrar ofertas que ESTÁN escalando ahora mismo,
verificarlas y registrarlas en la hoja maestra con su histórico.

## Criterios duros (si falla UNO, se descarta)

1. ≥ MINIMO_ADS anuncios activos del mismo producto/página (conteo nativo de Meta).
2. Varios días corriendo (≥ 7 sugerido) — un día de gasto no es una señal.
3. Producto que pase TU_FILTRO y sea DESCARGABLE de verdad (PDF, plantillas,
   guías, archivos). NO cursos en video con dashboard, aunque la marca sea grande.
4. Venta por landing con checkout directo — si va a WhatsApp/formulario/llamada, fuera.
5. NO marca personal (si el vendedor ES la oferta, fuera; un protocolo/plantilla
   vendido como producto sí entra).
6. Cualquier idioma y país.

## Método de conteo (la clave, no te dejes engañar)

En la barra de búsqueda de la Ads Library escribe el NOMBRE del anunciante →
dropdown "Anunciantes" → clic en la página → la URL pasa a view_all_page_id y
arriba se lee "~N resultados" = anuncios activos totales de esa página. ESE es
el número. TRAMPA: "N anuncios usan este contenido y texto" en la vista por
keyword NO son N anuncios distintos (son variantes de UN anuncio).

## Búsqueda multi-ángulo (cada corrida)

1. Re-chequear primero las ofertas YA registradas en la hoja maestra (actualizar conteos).
2. Venas calientes del Log de búsquedas (lo que funcionó ayer se profundiza hoy).
3. Keywords nuevas del BANCO DE KEYWORDS (pestaña Keywords) aplicando: ángulo consumidor Y ángulo
   profesional de cada tema, keyword de DOCUMENTO para B2B (checklist, template,
   protocolo, ficha), multi-idioma SIEMPRE, scroll profundo (15-25 anunciantes,
   no los 3 primeros), y muchos nichos sin re-quemar la lista negra del Log.
4. EXCLUIR SIEMPRE tus PAGINAS_PROPIAS.
5. Rate-limit: si 2+ búsquedas válidas devuelven 0 resultados, prueba una keyword
   canary obvia (p. ej. 'shoes' en US, activos). Si el canary también da 0, es
   rate-limit por concurrencia: enfría 3-5 minutos, baja a máximo 3 pestañas
   simultáneas y reintenta. NO es tu sesión: no cierres sesión ni vuelvas a loguearte.

## Verificación de landing (OBLIGATORIA por candidata)

Abre la landing y confirma que es un producto digital descargable real con
checkout directo. Salud y consumo esconden suplementos, aparatos, apps o
telemedicina — esos se DESCARTAN. Si la demanda es brutal pero el formato no
sirve, anota el HUECO en Pendientes como idea de producto propio.
Cada hallazgo cierra con una línea: "el producto que YO haría con esto"
(qué producto, para qué comprador, en qué idioma).

## Actualizar la hoja maestra

- SIEMPRE la misma hoja maestra. NUNCA crees una segunda. Lee TODAS las
  pestañas primero y luego actualiza/añade EN SU LUGAR.
- Escribe con el conector de Google Drive. Google Sheets guarda su propio
  historial de versiones: antes de escribir, anota la hora de inicio de la
  corrida en el Log de búsquedas (es el punto de restauración si una corrida
  rompe algo: Archivo → Historial de versiones). Si una escritura falla a
  mitad, reintenta una vez; si sigue fallando, imprime los resultados del día
  en el chat como tabla (lista para pegar en la hoja) y dilo claramente —
  jamás se pierden hallazgos.
- ANTIDUPLICADOS por ID de página: si la oferta ya existe → actualízala (mueve
  el conteo de HOY a AYER, recalcula la Tendencia 📈/➡️/📉/❌, añade fila al
  Histórico). Si es nueva → añádela con ID correlativo.
- Pestañas y columnas:
  - "Ofertas" (las verificadas): ID | Page ID | Anunciante | Producto |
    Vertical | Idioma | País | Ads hoy | Ads ayer | Tendencia | Días
    corriendo | Link biblioteca | Link landing | Formato | El producto que YO
    haría | Primera vez visto | Último chequeo
  - "Pendientes" (prometedoras sin conteo o bajo umbral + huecos 💡): mismas
    columnas + Motivo
  - "Histórico": fecha | ID | producto | ads de hoy
  - "Log de búsquedas": fecha | keywords usadas | resultados útiles
  - "Keywords", "Ajustes", "Mis reglas": ver DÓNDE VIVE TODO
- Mantén el formato: encabezado en negrita con color, encabezado fijo,
  filtros activos, links como hipervínculos clicables (`=HYPERLINK(url;
  texto)` en Sheets).

## Resumen final (imprímelo claro)

Cuántas ofertas nuevas y de cuántos verticales; cuáles subieron anuncios (con
delta, p. ej. 40→70); cuáles se apagaron; TOP 3 del día con una línea de
justificación cada una. SÉ HONESTO: si no llegaste al PISO_DIARIO, dilo y
muestra lo que sí salió con su conteo real. Nunca infles números ni inventes links.
