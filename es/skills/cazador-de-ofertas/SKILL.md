---
name: cazador-de-ofertas
description: Caza diaria de ofertas escalando en la biblioteca de anuncios de Meta según tu filtro de formato, y actualiza tu Google Sheet maestro (o Excel) con el histórico. Pide sus ajustes al inicio (o reutiliza los últimos). Usar cuando el usuario diga 'cazar ofertas', 'el cazador', 'buscar ofertas escalando' o pida el barrido de la hoja maestra.
---

# PASO 0 — AJUSTES DE LA CAZA (pregunta, jamás asumas)

Esta skill NO tiene bloque de configuración que editar. Obtiene sus ajustes de
la persona al inicio de cada caza y recuerda las últimas respuestas en un
archivo de perfil que escribe ella misma. Esta skill es la fuente canónica de
la rutina: las corridas programadas solo apuntan a ella. Editar la rutina =
editar este archivo.

## Los ajustes

| Ajuste | Qué es | Por defecto si a la persona le da igual |
|---|---|---|
| CARPETA_TRABAJO | Carpeta donde viven el banco de keywords y los archivos locales | `./cazador-de-ofertas/` en el proyecto actual |
| SALIDA | Dónde se registran los hallazgos: `google-sheet` (necesita el conector de Google Drive) o `excel` (archivo local, Python + openpyxl) | `google-sheet` |
| SHEET_MAESTRO | URL del Google Sheet maestro (SIEMPRE el mismo). Solo si SALIDA = google-sheet | Si no hay: crear "Cazador de ofertas — Maestro" en el Drive de la persona en la primera corrida y guardar su URL |
| EXCEL_MAESTRO | El Excel maestro (SIEMPRE el mismo archivo). Solo si SALIDA = excel | `CARPETA_TRABAJO/ofertas-master.xlsx` |
| TU_FILTRO | El formato de producto que la persona puede replicar. Solo se registra lo que lo pase. P. ej. "toolkits digitales descargables de ticket bajo (guías PDF, plantillas, packs de prompts) que pueda producir con IA en días; nada de cursos en video, coaching ni servicios" | **Ninguno — hay que preguntarlo** |
| NICHOS_CIRCULOS | Círculo 1 = nichos actuales; 2 = mismo comprador, otros temas; 3 = adyacentes. 3-5 por círculo. La caza va en ese orden | **Ninguno — hay que preguntarlo** |
| PAGINAS_PROPIAS | Las páginas de Facebook de la persona (nombres o page_id), EXCLUIDAS de la caza | Preguntar; "ninguna" solo si la persona lo dice |
| IDIOMAS | Idiomas en los que buscar | Todos, inglés primero |
| MINIMO_ADS | Anuncios activos del mismo producto para considerarlo "escalando" | 15 |
| PISO_DIARIO | Hallazgos nuevos verificados mínimos por corrida | 5 |
| BANCO_KEYWORDS | Archivo del banco de keywords por categoría e idioma | `CARPETA_TRABAJO/banco-keywords.md` |

## El archivo de perfil

`launch-profile.md` en la raíz del proyecto actual, sección
`## Offer hunter` (las demás skills del pack guardan su propia sección en el
mismo archivo; `## Shared` guarda PAGINAS_PROPIAS para todas). Guarda las
últimas respuestas con su fecha. Lo escribe ESTA SKILL — nadie tiene que
editarlo a mano (puede, si quiere). Jamás guardes contraseñas, tokens ni API
keys en él.

## Reglas personales

Si existe `my-rules.md` en la raíz del proyecto actual, léelo antes de
empezar y aplica cada regla como regla DURA adicional de esta corrida. Es cómo
la persona añade sus propias lecciones sin editar esta skill (las
actualizaciones del pack sobrescribirían los cambios aquí). Si una regla
personal contradice una de esta skill, sigue la personal y menciónalo en el
resumen final. Cuando la persona rechace algo y enuncie una regla, ofrece
añadirla a `my-rules.md` (créalo si no existe).

## Cómo obtener los ajustes

1. **Los ajustes del mensaje de invocación mandan.** P. ej. `/cazador-de-ofertas
   nichos: planes keto, mínimo 10 ads` → úsalos directamente y no los vuelvas a
   preguntar.
2. **Corrida interactiva (hay una persona en el chat):**
   - Existe perfil → muestra los ajustes guardados en UNA tabla compacta y haz
     UNA pregunta: "¿Cazamos con estos, cambias algunos o empezamos de cero?"
   - No hay perfil (primera vez) → pide los ajustes que falten en COMO MÁXIMO 2
     rondas. Usa la tool AskUserQuestion si está disponible para los de opción
     (IDIOMAS, MINIMO_ADS, PISO_DIARIO) y chat normal para los de texto libre
     (TU_FILTRO, NICHOS_CIRCULOS, PAGINAS_PROPIAS). Da el ejemplo de la tabla
     con cada pregunta. Ofrece los valores por defecto; jamás inventes
     TU_FILTRO ni NICHOS_CIRCULOS — si son vagos, ayuda a afinarlos.
   - Después imprime la tabla final de ajustes y ARRANCA la caza (sin otra
     ronda de confirmación).
3. **Corrida desatendida (tarea programada, Grok Bot, `claude -p` headless, o
   el mensaje dice "desatendida"/"unattended"):** NUNCA preguntes — no hay
   nadie para responder. Usa los ajustes del mensaje, completa con el perfil y
   luego con los valores por defecto. Si aún faltan TU_FILTRO o
   NICHOS_CIRCULOS: PARA sin cazar e imprime qué ajustes faltan más un comando
   de ejemplo que los incluya.
4. **Guarda** los ajustes finales en el perfil (actualiza la sección
   `## Offer hunter` en su lugar, con la fecha de hoy) antes de empezar.
5. **Banco de keywords:** si BANCO_KEYWORDS no existe, genera uno (100+
   keywords por círculo de nicho × IDIOMAS, ángulos consumidor Y profesional,
   keywords de DOCUMENTO para B2B: checklist, plantilla, protocolo, ficha),
   guárdalo y di en una línea dónde está.
6. **Hoja maestra:** comprueba las herramientas ANTES de cazar. Con
   `google-sheet`, el conector de Google Drive debe poder leer Y escribir la
   hoja — si no puede, PARA y di exactamente qué conectar (no caces para luego
   perder los resultados). Si SHEET_MAESTRO está vacío, créalo con las 4
   pestañas descritas abajo ("Ofertas", "Pendientes", "Histórico", "Log de
   búsquedas"), guarda su URL en el perfil y dale el link a la persona. A
   partir de ahí, NUNCA crees otro. Con `excel`, lo mismo con EXCEL_MAESTRO.
7. **Herramientas de Meta:** confirma que el conector de Meta expone una tool
   de búsqueda en la Ads Library (normalmente `ads_library_search`; el nombre
   puede variar según el conector). Si no hay ninguna, PARA y dilo — jamás
   inventes conteos.

# LA RUTINA

Eres el "Cazador de ofertas escalando". Ejecuta la rutina diaria completa desde
CARPETA_TRABAJO. Objetivo: encontrar ofertas que ESTÁN escalando ahora mismo,
verificarlas y registrarlas en la hoja maestra (SHEET_MAESTRO o EXCEL_MAESTRO) con su histórico.

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
3. Keywords nuevas del BANCO_KEYWORDS aplicando: ángulo consumidor Y ángulo
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
- **Google Sheet (por defecto):** escribe con el conector de Google Drive.
  Google Sheets guarda su propio historial de versiones: antes de escribir,
  anota la hora de inicio de la corrida en el Log de búsquedas (es el punto de
  restauración si una corrida rompe algo: Archivo → Historial de versiones).
  Si una escritura falla a mitad, guarda los resultados del día en
  `CARPETA_TRABAJO/pendiente-sync-<FECHA>.csv`, repórtalo y sincronízalos en
  la siguiente corrida — jamás se pierden hallazgos.
- **Excel:** Python + openpyxl. Backup a `*-backup.xlsx` → load_workbook →
  actualizar/añadir EN SU LUGAR.
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
- Mantén el formato: encabezado en negrita con color, encabezado fijo,
  filtros activos, links como hipervínculos clicables (`=HYPERLINK(url;
  texto)` en Sheets).

## Resumen final (imprímelo claro)

Cuántas ofertas nuevas y de cuántos verticales; cuáles subieron anuncios (con
delta, p. ej. 40→70); cuáles se apagaron; TOP 3 del día con una línea de
justificación cada una. SÉ HONESTO: si no llegaste al PISO_DIARIO, dilo y
muestra lo que sí salió con su conteo real. Nunca infles números ni inventes links.
