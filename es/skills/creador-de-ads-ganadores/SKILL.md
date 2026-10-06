---
name: creador-de-ads-ganadores
description: Creador de Ads Ganadores — pipeline diario completo de creativos para Meta Ads. Para cada producto de tu Google Sheet maestro investiga a los mejores anunciantes del mundo por la API de la Ads Library (cero navegador), crea 5 anuncios de imagen nuevos con IA modelados sobre ganadores reales, los audita uno a uno y los entrega en tu Google Drive con links en la hoja. Incluye una configuración guiada que lleva a cualquiera de "acabo de instalar esto" a sus primeros 5 ads. Usar cuando el usuario diga 'creador de ads ganadores', 'crea mis anuncios', 'la rutina de ads', 'corre la rutina', 'regenera los anuncios', 'configura el creador de ads', suba esta skill y pida configurarla, o pida los 5 ads de un producto.
---

> Versión 2 de la rutina (4-ago-2026): research 100% por API, banco de
> ganadores, agente visual y disciplina de costes — todo medido en producción
> real.

# DÓNDE VIVE TODO — el Google Drive de la persona

No se guarda nada en el ordenador que ejecuta esta skill (las sesiones en la
nube se borran al terminar). Todo vive en una carpeta de Drive llamada
**"Creador de Ads Ganadores"**:

```
Creador de Ads Ganadores/
├── Creador de Ads Ganadores — Maestro   (Google Sheet, pestañas abajo)
├── Anuncios/<PRODUCTO>/<YYYY-MM-DD>/AD01.jpg … AD05.jpg
├── Research/<PRODUCTO>_<FECHA>.md
└── Ganadores/<PRODUCTO>/…               (creativos ganadores vistos por el agente VISUAL)
```

| Pestaña | Qué guarda |
|---|---|
| Productos | PRODUCTO \| LINK PRODUCTO (landing) \| IDIOMA \| LINK RESEARCH \| LINK CREATIVOS — una fila = un producto |
| Ajustes | ajuste \| valor \| última actualización — las respuestas de la persona + el checklist de configuración |
| Mis reglas | regla \| añadida el — las reglas extra de la persona |
| Banco de ganadores | fecha \| producto \| anunciante \| page_id \| link del anuncio \| duplicaciones \| días en circulación \| hook \| descripción visual \| fórmula espacial \| posición del texto \| transcripción |
| Registro de conceptos | fecha \| producto \| AD# \| ganador modelado \| fórmula \| nivel de embudo \| titular \| 2 alternos |
| Caché de landings | producto \| URL landing \| cifras verificadas \| garantía \| URL mockup héroe \| titulares reales \| verificado el |
| Log de corridas | fecha \| producto \| etapa \| minutos-agente \| notas (regla de coste 5) |

**Dos formas de mover datos (las dos baratas):**
- **Tablas** (pestañas de arriba) → el conector de Google Sheets / Google
  Drive. Lee solo las filas que necesites (p. ej. las filas del banco del
  nicho de este producto).
- **Archivos** (JPG, informes) → JAMÁS por el chat (una imagen como texto
  cuesta una fortuna). Van por el **Drive uploader** de la persona con
  `assets/drive_sync.py` (junto a este archivo), ejecutado con
  `UPLOADER_URL` / `UPLOADER_TOKEN` exportados desde la pestaña Ajustes.
  Alternativa local: en un ordenador con Google Drive para escritorio, escribe
  los archivos directamente en la carpeta sincronizada "Creador de Ads
  Ganadores".

**`_assets/` = la carpeta de trabajo local de UNA corrida.** Al empezar,
llénala desde Drive: filas del banco → `_assets/banco.md`, Caché de landings →
`_assets/landings_cache.json`, Registro de conceptos → `_assets/conceptos.md`,
los 5 ads de ayer de cada producto → `_assets/ayer/<PRODUCTO>/`
(`drive_sync.py pull`). El "relevo por disco" de las reglas de coste ocurre
aquí. Al terminar, se guarda de vuelta (PASO 6).

**Encontrarlo en una sesión nueva:** busca en Drive el nombre exacto
"Creador de Ads Ganadores — Maestro". Una coincidencia → úsala. Varias →
pregunta cuál. Ninguna → configuración de primera vez. Jamás crees una
segunda hoja maestra.

Esta skill NO tiene bloque de configuración que editar. Esta skill es la
fuente canónica de la rutina: las corridas programadas solo apuntan a ella.
Editar la rutina = editar este archivo.

# CONFIGURACIÓN GUIADA — de "acabo de instalar esto" a los primeros 5 ads

Ejecuta esta sección PRIMERO siempre que no exista aún la hoja maestra, o su
pestaña Ajustes no diga `Setup = complete`, o la persona pida configurar /
reparar el Creador de Ads Ganadores. Con la configuración completa, ve
directo al PASO 0.

**Cómo guiar (innegociable):**
- Habla en el idioma de la persona. Asume que NO es técnica: una acción a la
  vez, la ruta exacta de clics, qué va a ver y cómo saber que funcionó.
- COMPRUEBA antes de preguntar: detecta tú todo lo que puedas (tools, red,
  variables de entorno). Pide solo lo que no puedes detectar ni hacer.
- Agrupa todo lo que necesite una sesión NUEVA en UN solo reinicio
  (conectores, red y variables de entorno solo se cargan al iniciar sesión).
- Muestra el progreso en cada turno como checklist corto: ✅ hecho, 👉 ahora,
  ⬜ siguiente.
- Jamás pidas contraseñas, tokens ni API keys en el chat. Las keys van en las
  variables del entorno (ver S2), nunca en la hoja ni en el chat.

**S1 — Detecta lo que falta (todo de una vez).** Busca en las tools
disponibles (incluidas las diferidas / tool search) y prueba:
- **Tool de la Ads Library de Meta** (p. ej. `ads_library_search`). Falta →
  ❌ Meta. Haz una consulta canary ('shoes', US, activos). Error sobre la
  cuenta publicitaria → ❌ Cuenta publicitaria (Meta solo abre la tool de la
  Ads Library a quien tiene al menos una cuenta publicitaria ACTIVA).
- **Tools de Google Drive + Google Sheets** (buscar, crear una hoja,
  leer/escribir celdas). Faltan → ❌ Drive.
- **Red (sesión en la nube de Claude Code, `echo $CLAUDE_CODE_REMOTE` =
  true):** abre `https://www.facebook.com/ads/library/`,
  `https://script.google.com` y un sitio cualquiera (p. ej.
  `https://gumroad.com`). Bloqueado → ❌ Red.
- **Navegador headless** para el agente VISUAL: `python3 -c "import
  playwright"` y un binario de Chromium. Falta → instálalo tú (`pip install
  playwright`; usa el Chromium preinstalado si existe, si no `playwright
  install chromium`). Solo pregunta si eso falla.
- **Motor de imágenes:** haz UNA pregunta (AskUserQuestion si está
  disponible): ¿qué generador de imágenes va a usar? Ofrece: una API de
  imágenes que ya pague (p. ej. OpenAI images, Google Gemini/Imagen, fal.ai,
  Replicate — la más potente que tenga, máxima resolución, 1:1, idealmente que
  acepte una imagen de referencia para el mockup de su producto), un CLI o un
  conector. Para una API, comprueba que su key existe como variable de entorno
  (p. ej. `OPENAI_API_KEY`, `GEMINI_API_KEY`, `FAL_KEY`,
  `REPLICATE_API_TOKEN`) — prueba `[ -n "$NOMBRE" ]`, jamás la imprimas.
  Falta → ❌ Key. Avisa: un conector que devuelve las imágenes al chat es caro
  (regla de coste 2) — mejor una API.
- **La skill misma** aparece como skill instalada (no solo como archivo
  subido). No instalada → ❌ Instalar.

**S2 — Arregla todo en UNA ronda y luego UN reinicio.** Una lista numerada
solo con los ❌:
- ❌ Instalar → claude.ai → Configuración → Capacidades → Skills → "Subir
  skill" → elige el ZIP de la skill (del pack). Las skills instaladas están
  disponibles en la app de Claude Y en las sesiones en la nube de Claude Code
  de la misma cuenta.
- ❌ Meta → claude.ai → Configuración → Conectores
  (claude.ai/customize/connectors) → el conector de Meta Ads del directorio, o
  "Add custom connector" con la URL de su MCP de Meta → Connect → inicia
  sesión en Meta → aprueba.
- ❌ Cuenta publicitaria → business.facebook.com → crea o reactiva una cuenta
  publicitaria (debe estar activa; normalmente pide un método de pago).
- ❌ Drive → misma página de conectores → Google Drive (y Google Sheets si
  aparece aparte) → Connect → su cuenta de Google → permitir.
- ❌ Red → en la barra del título de la sesión de Claude Code, menú del
  entorno → Edit → Network access → **Full** → Save.
- ❌ Key → saca la API key del panel del proveedor → en la misma pantalla Edit
  del entorno, añádela en **Environment variables** como `NOMBRE=key` (p. ej.
  `OPENAI_API_KEY=…`) → Save. Jamás la pegues en el chat.
Luego dile que abra una sesión NUEVA (app de escritorio de Claude → Code →
Cloud, o claude.ai/code) y envíe el mensaje para retomar (S9). Si no hay
ningún ❌, sáltate el reinicio.

**S3 — Verifica tras el reinicio.** Repite S1. Si algo sigue en ❌ → la causa
más probable en una línea y el único arreglo. No sigas hasta que Meta, Drive y
el motor de imágenes funcionen.

**S4 — Crea la casa.** Busca en Drive "Creador de Ads Ganadores — Maestro".
Ninguna → crea la carpeta "Creador de Ads Ganadores" (conector de Drive, tipo
carpeta) y dentro la hoja maestra con las 7 pestañas y sus encabezados
(negrita, color, fijados, filtros activos). Lee los encabezados de vuelta.
Dale el link.

**S5 — El Drive uploader (una vez, ~3 minutos).** Explica en una línea por
qué: "para que las imágenes de tus ads vayan directo a tu Drive sin gastar
tokens".
1. Genera un token aleatorio de 32 caracteres (letras + dígitos).
2. Lee `assets/drive-uploader.gs`, rellena ROOT_FOLDER_ID (el id de la
   carpeta "Creador de Ads Ganadores") y TOKEN, y dale el código completo en
   un solo bloque.
3. Guía: script.google.com → **Nuevo proyecto** → selecciona todo, pega →
   nómbralo "Creador de Ads Ganadores uploader" → 💾 Guardar → **Implementar
   → Nueva implementación** → ⚙️ tipo **Aplicación web** → Ejecutar como
   **Yo** → Quién tiene acceso **Cualquier usuario** → **Implementar** →
   **Autorizar acceso** → su cuenta → si Google dice "Google no ha verificado
   esta aplicación": **Configuración avanzada → Ir a … (no seguro)** →
   Permitir (es su propio script) → copia la **URL de la aplicación web** y
   pégala aquí.
4. Guarda UPLOADER_URL y UPLOADER_TOKEN en la pestaña Ajustes (la hoja es
   privada; dile que no la comparta).
5. Prueba: `drive_sync.py ping`, luego sube un archivo pequeño de prueba a
   `Anuncios/_prueba`, lístalo y bájalo de vuelta. Todo ok → ✅. Si falla,
   causas más comunes: el acceso no está en "Cualquier usuario", o copió la
   URL del editor en vez de la URL que termina en /exec.
En un ordenador local con Google Drive para escritorio, ofrece saltarse S5 y
guardar los archivos directamente en la carpeta sincronizada.

**S6 — Productos.** Pide sus productos (o impórtalos de la hoja de Winning
Offer Spy si quiere): de cada uno, el nombre, la URL de la landing y el idioma
de los anuncios. Escríbelos en la pestaña Productos. Abre cada landing UNA
vez: confirma que carga y rellena la Caché de landings (cifras reales,
garantía, URL del mockup héroe, titulares reales — PASO 5 regla 5).

**S7 — Ajustes.** Ejecuta PASO 0 → "Cómo obtener los ajustes" (máximo 2
rondas). PAGINAS_PROPIAS: reutiliza las de Winning Offer Spy si existe su
hoja maestra (confírmalas); si no, pregunta (page_id: Ads Library → busca su
página → clic → la URL muestra `view_all_page_id=NÚMERO`). REGLAS_NICHO:
pregunta su nicho y propón las reglas correspondientes.

**S8 — Prueba rápida (antes de la corrida real).**
- Motor de imágenes: UNA generación barata y pequeña con un prompt simple →
  guárdala → súbela a `Anuncios/_prueba/` → dale el link para que la vea → ✅.
- Meta: la consulta canary de S1 ya pasó.
Escribe `Setup = complete` en Ajustes y di: "Configuración lista. Creo ahora
tus primeros 5 ads para <UN producto> (≈ DEADLINE). Puedes cerrar esta
ventana — sigue corriendo en la nube." y ve a LA RUTINA con
PRODUCTOS_CORRIDA = ese UN producto (primera corrida: siempre un producto).

**S9 — Mensaje para retomar (dalo cada vez que haga falta reiniciar):**
`Continúa la configuración del Creador de Ads Ganadores donde lo dejamos.`
(El checklist vive en la pestaña Ajustes. Si la skill aún no está instalada,
adjunta el archivo de la skill a ese mensaje.)

**Después de la primera corrida:** pídele que mire los 5 ads con sus propios
ojos: ¿texto perfecto? ¿fotografía profesional o look plantilla? ¿cada cifra
existe en su landing? ¿parece un ganador real o algo genérico? Cada "no me
gusta X" → ofrece añadirlo a la pestaña Mis reglas (así se construyó la
rutina original: a base de rechazos). Repite con ese producto 2-3 días; cuando
salga bien sin tocar nada, suma el resto de productos. Ofrece la corrida
diaria programada (desatendida) solo después de eso.

# PASO 0 — AJUSTES DE LA CORRIDA (pregunta, jamás asumas)

## Los ajustes (guardados en la pestaña Ajustes)

| Ajuste | Qué es | Por defecto si a la persona le da igual |
|---|---|---|
| PRODUCTOS_CORRIDA | Qué filas de Productos correr | Todas (primera corrida: UN producto) |
| MOTOR_IMAGENES | El generador de imágenes IA más potente disponible, cómo llamarlo (API + nombre de la variable de entorno, comando CLI o conector), máxima resolución, 1:1 | **Ninguno — hay que preguntarlo** |
| MOTOR_LIMITES | Límite de jobs simultáneos del plan de imágenes — se respeta con un semáforo, no lanzando de menos | Preguntar; 4 si no se sabe |
| PAGINAS_PROPIAS | Las páginas de la persona, EXCLUIDAS del research de competencia | De la hoja de Winning Offer Spy si existe; si no, preguntar |
| REGLAS_NICHO | Compliance por nicho: salud = sin claims médicos ni dosis; dinero = sin promesas de ingresos; etc. | Sin claims médicos, dosis, promesas de ingresos, antes/después ni ratings inventados |
| MODELO_TOP | El modelo Claude más potente del plan — SOLO donde se diseña: director+crítico y reparador | El modelo más capaz disponible |
| MODELO_ECO | Un modelo económico — research, generación, auditoría y la sesión que orquesta | Un modelo tipo Sonnet |
| DEADLINE | Hora límite de entrega. Lo que no llegue, se reporta con causa — la corrida no se estira | 1 hora después del arranque |
| UPLOADER_URL / UPLOADER_TOKEN | El Drive uploader (S5) | Los fija la configuración |

## Reglas personales

Lee la pestaña Mis reglas antes de empezar y aplica cada regla como regla
DURA adicional de esta corrida. Es cómo la persona añade sus propias lecciones
sin editar esta skill (las actualizaciones del pack sobrescribirían los
cambios aquí). Si una regla personal contradice una de esta skill, sigue la
personal y menciónalo en el resumen final. Cuando la persona rechace algo y
enuncie una regla, ofrece añadirla a la pestaña Mis reglas.

## Cómo obtener los ajustes

1. **Los ajustes del mensaje de invocación mandan.** P. ej.
   `/creador-de-ads-ganadores solo para <PRODUCTO>` → PRODUCTOS_CORRIDA queda
   fijado; no lo vuelvas a preguntar.
2. **Corrida interactiva (hay una persona en el chat):**
   - Pestaña Ajustes con datos → muestra los ajustes guardados en UNA tabla
     compacta y haz UNA pregunta: "¿Corremos con estos, cambias algunos o
     empezamos de cero?"
   - Primera vez → pide los ajustes que falten en COMO MÁXIMO 2 rondas
     (AskUserQuestion para los de opción, chat normal para texto libre), con
     un ejemplo de cada uno y los valores por defecto ofrecidos.
   - Después imprime la tabla final de ajustes y ARRANCA (sin otra
     confirmación).
3. **Corrida desatendida (tarea programada, Grok Bot, `claude -p` headless, o
   el mensaje dice "desatendida"/"unattended"):** NUNCA preguntes. Usa el
   mensaje, luego la pestaña Ajustes, luego los valores por defecto. Si faltan
   la hoja maestra, filas en Productos, MOTOR_IMAGENES o el uploader: PARA sin
   correr e imprime qué falta más un comando de ejemplo que lo incluya.
4. **Guarda** los ajustes finales en la pestaña Ajustes (con la fecha de hoy).
5. **Pre-vuelo (cada corrida):** la tool de Meta, la lectura/escritura en
   Sheets, `drive_sync.py ping` y la key del motor de imágenes deben funcionar
   ANTES de arrancar el pipeline. Si algo falla, PARA y di exactamente qué
   arreglar (S1-S2) — jamás generes ads que no se pueden entregar.

# LA RUTINA

Ejecuta el pipeline COMPLETO cada corrida: se regenera TODO cada día, todos los
productos de PRODUCTOS_CORRIDA, y los anuncios nuevos deben ser DIFERENTES a los de ayer.
Filosofía madre: **SE MODELA A LOS MEJORES ANUNCIANTES DEL MUNDO — jamás
reinventar la rueda.** La creatividad está en la ADAPTACIÓN fiel a tu producto.
Reporta corto, resultados, cero teoría.

## LAS 5 REGLAS DE COSTE (medidas en producción — violarlas multiplica la factura)

1. **EL RELEVO VA POR DISCO, NO POR CONTEXTO.** Cada agente escribe su resultado
   COMPLETO a un archivo en `_assets/` y devuelve al chat UNA línea. El siguiente
   agente LEE el archivo. Nunca pegues el contenido de un agente en el prompt del
   siguiente: pagas lo mismo 4 veces y al resumir pierdes la luz, el encuadre y
   la posición del texto del ganador.
2. **UNA IMAGEN EN CONTEXTO SE RE-COBRA EN CADA TURNO.** El coste aproximado es
   (ancho × alto) / 750 tokens, y se paga de nuevo con cada turno posterior del
   agente que la abrió. Por eso: se audita sobre copias pequeñas (~768px), cada
   imagen se abre UNA vez, y jamás se mete una imagen 4K al contexto. No subas
   la resolución de auditoría sin una prueba de que un fallo real es invisible
   a 768 — casi siempre el problema es el checklist, no la resolución.
3. **RESEARCH POR API, CERO NAVEGADOR.** El navegador con capturas de pantalla
   es lo más caro de todo el pipeline (medido: costaba varias veces más que el
   diseño). La API de la Ads Library da la señal por casi nada. El navegador
   solo se usa para lo único que la API no da: VER un creativo concreto — y de
   la forma barata (ver agente VISUAL).
4. **SI LA CORRIDA MUERE A MITAD, NO SE RELANZA SIN PREGUNTAR.** Relanzar
   repite las etapas caras ya pagadas (research y dirección). Lo correcto:
   PARAR, decir qué se cayó y cuánto costaría repetirlo, y esperar respuesta.
   Si el dueño no está: entregar lo que haya y reportar.
5. **MEDIR ANTES DE DIAGNOSTICAR.** Cuando la rutina vaya lenta o cara, saca el
   desglose real por etapa (minutos-agente y coste) antes de tocar nada. En
   nuestra medición el research era el 51% del reloj y el 73% del gasto — y la
   intuición culpaba a la generación de imágenes, que NO era el cuello.

## PASO 1 — Leer la fuente de verdad

Lee la pestaña Productos de la hoja maestra (conector de Google Sheets). Cada
fila = un producto con su landing y su idioma. Producto nuevo (fila sin
carpeta en la carpeta `Anuncios/` de Drive) → créale
carpeta y córrele el pipeline completo.

## PASO 2 — Research por API (todos los productos, todos los días)

**PROHIBIDO abrir el navegador para explorar la biblioteca.** Todo el research
va por la API de la Ads Library (`ads_library_search` del conector de Meta),
en DOS PASADAS — porque la búsqueda por keyword tiene tope de resultados y no
pagina, así que sus conteos son solo un PISO:

1. **Pasada de descubrimiento**: 3-5 keywords del nicho → identificar 6-8
   `page_id` candidatos (quién está corriendo ads del tema).
2. **Pasada de medición**: una llamada POR `page_id` — ahí el conteo total SÍ es
   el tamaño real del anunciante y la duplicación se cuenta exacta (mismo
   título/creativo repetido en N anuncios = lo que ese anunciante ESCALA).

De cada candidato la API te da lo FRESCO: quién escala HOY, cuántas
duplicaciones, días en circulación y el hook literal. Señales: ≥3 duplicaciones
interesante, ≥8 ganador claro, ≥15 brutal; meses en circulación = ganador
aunque no tenga duplicaciones. EXCLUIR SIEMPRE tus PAGINAS_PROPIAS.

**EL BANCO — tu activo acumulado.** La API da señal pero NO imágenes. La
fórmula visual sale de tu BANCO: los informes de research anteriores
(`_assets/research/`, traídos de `Research/` en Drive) y la pestaña Banco de
ganadores, donde cada ganador VISTO quedó deconstruido (descripción visual,
fórmula espacial, transcripción, hook). El research cruza cada candidato de la
API contra el banco y lo marca **BANCO: sí / no**:
- BANCO: sí → señal fresca + estructura visual verificada. Los mejores para modelar.
- BANCO: no → pasa al agente VISUAL (paso 2.5) para verlo UNA vez y meterlo al banco.
**Jamás se inventa una descripción visual que no se vio.** El banco arranca
vacío: tus primeras 1-2 semanas el agente visual trabaja más; después casi todo
sale BANCO: sí. Es inversión, no gasto recurrente.

El research escribe su informe a `_assets/research/<PRODUCTO>_<FECHA>.md` y
devuelve una línea. Los sets en otros idiomas del MISMO producto no investigan
aparte: adaptan el informe del hermano principal sin suavizarlo.

## PASO 2.5 — Agente VISUAL: ver los ganadores nuevos (la forma barata)

Corre SOLO si el research marcó ganadores BANCO: no. Su único trabajo es VER
esos anuncios — sin fotografiar la pantalla:

1. Abre el link del anuncio CONCRETO en la biblioteca (su snapshot), no la
   búsqueda general. La biblioteca sirve el creativo sin login.
2. **CERO capturas de pantalla.** Extrae del DOM la URL de la imagen del
   creativo (el `<img>` más grande del CDN de Facebook) con una sola llamada de
   JavaScript.
3. Descarga el JPG a `_assets/ganadores/<PRODUCTO>/` con curl.
4. Ábrelo con Read y deconstrúyelo: tipo de plano, luz, objetos, DÓNDE vive el
   texto, paleta, personas/manos/caras, fórmula espacial en una línea,
   transcripción. Eso va al banco → mañana ese ganador ya es BANCO: sí.

Por qué así: un JPG de ~600px son ~480 tokens; una captura de página completa
~2.000 y se re-cobra cada turno. Además obtienes el ARCHIVO ORIGINAL del
anuncio, no una foto de una pantalla. Reglas duras: máximo 5 ganadores por
producto; prohibido screenshot/zoom/leer la página entera; si hay varios
agentes visuales, el navegador va de UNO EN UNO (comparten pestaña y se pisan;
además el paralelo dispara el rate-limit de la biblioteca).

**Regla del director:** si hoy hubo ganadores vistos, UNO de los 5 ads modela
SÍ O SÍ a un ganador visto hoy — modelando su ESTRUCTURA, jamás copiando su
texto ni su marca.

## PASO 3 — La cadena de agentes por producto

- **RESEARCH** (MODELO_ECO): API dos pasadas + cruce contra banco → informe a
  disco. Si trae <5 ganadores utilizables, se repite ESE research con MODELO_TOP.
- **VISUAL** (MODELO_ECO): solo BANCO: no → descarga y deconstruye (paso 2.5).
- **DIRECTOR+CRÍTICO** (MODELO_TOP): lee el informe DEL DISCO (íntegro, no un
  resumen) y diseña los 5 anuncios Y se auto-ataca con el checklist adversarial
  en el mismo pase: suavidad del hook, prueba de la portada, idioma perfecto,
  compliance, fidelidad a la fórmula del ganador, zona segura, generabilidad
  (textos citados entre comillas exactas; props con texto ELIMINADOS). Escribe
  `spec_<PRODUCTO>.json` con: ganador modelado, fórmula, nivel de embudo,
  titular elegido + 2 alternos, textos overlay EXACTOS y el prompt final.
- **GENERACIÓN** (mecánica): ejecuta el MOTOR_IMAGENES con los 5 prompts del
  spec. Respeta MOTOR_LIMITES con un semáforo compartido (así todos los
  productos pueden ir en paralelo sin inventar "olas" ni tandas manuales).
- **AUDITOR** (MODELO_ECO): mira los 5 en copia ~768px, UNA vez cada uno. El
  formato importa: **5 preguntas fijas por ad** (¿qué prueba visual del
  producto contiene? ¿el texto está perfecto y en el idioma correcto? ¿hay
  rostro identificable, precio o botón? ¿respeta la fórmula del ganador? ¿le
  habla al comprador real?) + 1 chequeo de VARIEDAD del set completo (¿los 5
  son distintos entre sí y distintos de ayer?). Un checklist libre de 12 puntos
  se skimmea; 5 preguntas fijas no. Ante la duda, rechaza. Si el veredicto
  vuelve con CERO aprobados, repite la auditoría UNA vez (suele ser señal de
  carrera con la generación: carpeta aún vacía) — y marca "no entregado" si
  falta un archivo, en vez de inventarse un veredicto.
- **REPARADOR** (MODELO_TOP, solo si hay rechazos): corrige EL CONCEPTO en una
  sola tanda. PROHIBIDO dar por bueno un ad sin abrir su imagen con Read.

Todo el relevo entre agentes va por disco (REGLA DE COSTE 1). La sesión
principal solo orquesta — y hace su propio **SPOT-CHECK**: antes de reportar,
abre 1-2 copias de auditoría por producto y las mira. Nada se declara
entregado sin que un par de ojos lo haya visto — el día que nadie miró, se
entregó basura con el veredicto en verde. Las copias de auditoría van en
carpeta POR FECHA (`_assets/audit/<PRODUCTO>/<FECHA>/`): con carpeta plana, un
producto cuya generación falla conserva las copias de AYER y el auditor las
aprueba como si fueran de hoy.

## PASO 4 — Dirección creativa (las reglas del oficio)

- **El set de 5 es un MINI-EMBUDO**: AD1 dolor oculto que el lector cree
  normal; AD2 valida el dolor + insinúa la salida (sub-dolor DISTINTO); AD3
  transformación lograda; AD4 mecanismo único / prueba legítima; AD5 venta
  directa (CTA + garantía + "descarga inmediata", SIN precio). Mapa flexible;
  el set completo cubre de frío a caliente.
- **Cada ad modela un ganador REAL distinto** del banco/research. Prohibido
  repetir ganador, fórmula o estructura del día anterior (mira los de ayer y el
  registro de conceptos antes de dirigir).
- **Titulares — 3 candidatos + prueba de la portada**: formatos distintos
  (pregunta que duele / acusación suave / error / revelación / confesión /
  número); impreso en una revista compitiendo con 20 más, ¿el lector la
  levanta? Máx 8-10 palabras; especificidad brutal; habla del lector, no del
  producto. Los 2 alternos se registran (sirven para el copy).
- **Cross-idioma**: la señal reina es la duplicación MUNDIAL, no el idioma. Los
  sets en otros idiomas modelan a los TOP de cualquier idioma y se adaptan
  SIN suavizar: el hook debe igualar el voltaje del original. "Suave" = rechazo.
- **Mockups — SIN cuota**: si el ganador modelado lleva producto en cuadro, ese
  producto es el TUYO (mockup oficial de tu landing como referencia del
  generador — jamás en blanco, genérico o inventado; y jamás el atajo de
  ponerle texto encima). Si el ganador no lleva producto, no lo metas a la
  fuerza. Adáptate a lo que encuentres, como un gran diseñador.

## PASO 5 — Reglas duras de generación (violarlas = rehacer)

1. TODO el texto visible en el idioma de la fila del Sheet, perfecto.
2. CERO precios, símbolos de moneda, %, tachados o "value".
3. **PERSONAS — regla calibrada**: manos y cuerpos SÍ. Lo prohibido es el
   **ROSTRO IDENTIFICABLE**: cara nítida, en foco, con peso en la composición
   (una cara de IA delata el anuncio). SÍ pasan — y son buen diseño — la
   silueta a contraluz, la cara en sombra, el perfil en penumbra, la
   desenfocada por profundidad de campo y la figura pequeña y lejana. No seas
   más extremo que esto: la versión dura ("si se ve un ojo, fuera") cuesta
   fotografía buena sin ganar nada. (Excepción posible: un producto donde la
   cara ES el producto — ahí va con disclosure de IA visible.)
4. Sin escasez fabricada, sin claims médicos, sin social proof no verificable.
   Permitido: oferta de lanzamiento / descarga inmediata / acceso de por vida /
   garantía real / CTA imperativo.
5. **NÚMEROS VERACES + CACHÉ DE LANDINGS**: toda cifra (conteos, garantía) se
   verifica contra la landing real UNA vez y se cachea en
   `_assets/landings_cache.json` (conteos, garantía, mockup héroe, titulares
   reales). Las corridas siguientes usan el caché — solo se re-verifica si el
   dueño avisa que tocó una landing. Usa los titulares y el copy REALES de tus
   landings en los briefs: son mejores que inventados. Si una cifra no se puede
   verificar, va sin cifra.
6. **PROHIBIDO EL LOOK PLANTILLA**: sin botón ni pill ni badge (el CTA es UNA
   línea de texto plano); vetado el esqueleto titular-arriba/subtítulo/botón
   (máximo 1 de 5 con titular arriba); el titular vive DENTRO del espacio que
   la foto ya tiene; fotografía con luz real y dirección concreta; los 5
   distintos entre sí (encuadre, hora, posición del texto, fórmula).
7. **Props con texto se ELIMINAN del prompt** (reglas, pestañas, lomos,
   pantallas): pedir "blur" no basta, salen letras rotas. El texto pequeño del
   producto va fuera de cuadro o muy desenfocado; NUNCA redibujarlo. Y las
   reglas van INTEGRADAS en la descripción del prompt, nunca como lista final
   ("no gibberish, no faces") — el modelo la imprime dentro del ad.
8. **REGLA ANTI-ATAJO**: prohibido resolver un problema técnico eliminando el
   elemento que vende. Si algo no puede existir sin romperse, SE CAMBIA EL
   CONCEPTO. Cada frame necesita PRUEBA VISUAL (producto reconocible, mecanismo
   o resultado) y debe hablarle al COMPRADOR real. Portada en blanco, página
   vacía o prop mudo = rechazo aunque esté "limpio".
9. **Barrido de compliance** sobre el texto visible antes de generar (regex
   según REGLAS_NICHO): dosis, curar/tratar, perder peso, before/after, "solo
   quedan N", ratings inventados. El arreglo mantiene el voltaje: mueve el
   héroe del término prohibido al criterio/mecanismo.
10. ZONA SEGURA en cada prompt: componer titular y elementos clave en el centro
    para que el 1:1 funcione recortado a 9:16 (sirve para Stories sin regenerar).

## PASO 6 — Entrega

JPG a resolución NATIVA (sin reescalar, calidad ~95) como AD01.jpg…AD05.jpg en
`_assets/out/<PRODUCTO>/<YYYY-MM-DD>/`. Verifica resolución y FRESCURA
(mtime del JPG ≥ mtime de su fuente — un JPG viejo pasa el chequeo de tamaño).
Luego sube cada uno a `Anuncios/<PRODUCTO>/<YYYY-MM-DD>/` en Drive con
`drive_sync.py upload` y comprueba que cada subida devolvió ok (subida fallida
= "no entregado", jamás "entregado"). No borres carpetas de días anteriores.
Escribe el link de la carpeta de Drive en la columna LINK CREATIVOS de la
pestaña Productos, y el link en Drive del informe de research (sube
`_assets/research/<PRODUCTO>_<FECHA>.md` a `Research/`) en LINK RESEARCH.

**Guarda la memoria (mismo paso, cada corrida):** añade los ganadores nuevos
deconstruidos a la pestaña Banco de ganadores, los 5 conceptos al Registro de
conceptos, los datos de landing nuevos o cambiados a la Caché de landings, y
los minutos-agente por etapa al Log de corridas. Sube los JPG de ganadores
nuevos a `Ganadores/<PRODUCTO>/`. La corrida de mañana se alimenta de esto —
saltarse este paso hace que mañana repita lo de hoy y vuelva a pagar el
agente VISUAL.

## PASO 7 — Resumen final

Por producto: ganadores del día (anunciante + duplicaciones + BANCO sí/no),
los 5 anuncios indicando QUÉ GANADOR modela cada uno y en qué se diferencian de
ayer, ruta de la carpeta, y el resultado del spot-check. Honesto con lo que
falló y con lo que quedó fuera del DEADLINE (con su causa).

## ESCALADO — de secuencial a scriptado (cuando ya esté estable)

Arranca SECUENCIAL: un producto de punta a punta, luego el siguiente. Cada
fallo sistemático detectado se corrige en la plantilla ANTES del siguiente
producto (el error se paga una vez, no N). Cuando la rutina lleve 1-2 semanas
estable, pídele a tu Claude que la SCRIPTE: un script previo que regenera los
datos por producto, y un Workflow que corre TODOS los productos en paralelo
(research → dirección → generación → auditoría → reparación → entrega) con el
semáforo del generador y el DEADLINE por etapa. Reglas del modo scriptado:
los prompts de los agentes viven ESCRITOS en el script (no se redactan cada
mañana); nada de inventar tandas manuales; y si hay que cambiar el pipeline,
se cambia el script EN FRÍO, se deja escrito por qué, y se corre al día
siguiente. La rutina no se rediseña cada mañana.
