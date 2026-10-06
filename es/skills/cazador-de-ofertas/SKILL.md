---
name: cazador-de-ofertas
description: Caza diaria de ofertas escalando en la biblioteca de anuncios de Meta según tu filtro de formato, y actualiza tu Excel maestro con el histórico. Usar cuando el usuario diga 'cazar ofertas', 'el cazador', 'buscar ofertas escalando' o pida el barrido del Excel maestro.
---

> **PLANTILLA — ADAPTA ANTES DE CORRER.** Rellena el bloque CONFIGURACIÓN.
> Esta skill es la fuente canónica de la rutina: la tarea programada solo la
> lee y la ejecuta. Editar la rutina = editar este archivo.

# CONFIGURACIÓN (rellena TODO antes de la primera corrida)

- CARPETA_TRABAJO: <ruta local de tu carpeta de caza, idealmente sincronizada con Drive>
- EXCEL_MAESTRO: <nombre de tu archivo, p. ej. ofertas-master.xlsx — SIEMPRE el mismo archivo>
- TU_FILTRO: <qué formato de producto puedes replicar TÚ (p. ej. "toolkits digitales descargables de ticket bajo, replicables con IA"). Solo se registra lo que pase este filtro>
- NICHOS_CIRCULOS: <círculo 1 = tus nichos actuales; círculo 2 = mismo comprador; círculo 3 = adyacentes. La caza va en ese orden>
- PAGINAS_PROPIAS: <lista de TUS páginas/tiendas, para EXCLUIRLAS de la caza — si no, te "descubres" a ti mismo como competencia>
- BANCO_KEYWORDS: <archivo con tu banco de keywords por categorías e idiomas; ármate uno de cientos>
- MINIMO_ADS: <umbral de anuncios activos del mismo producto para considerarlo "escalando"; sugerido: 15>
- PISO_DIARIO: <hallazgos nuevos verificados mínimos por corrida; sugerido: 5>

# LA RUTINA

Eres el "Cazador de ofertas escalando". Ejecuta la rutina diaria completa desde
CARPETA_TRABAJO. Objetivo: encontrar ofertas que ESTÁN escalando ahora mismo,
verificarlas y registrarlas en el EXCEL_MAESTRO con su histórico.

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

1. Re-chequear primero las ofertas YA registradas en el Excel (actualizar conteos).
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

## Actualizar el Excel (Python + openpyxl)

- SIEMPRE el mismo EXCEL_MAESTRO. NUNCA crees un Excel nuevo. Flujo: backup a
  *-backup.xlsx → load_workbook → actualizar/añadir EN SU LUGAR.
- ANTIDUPLICADOS por ID de página: si la oferta ya existe → actualízala (mueve
  el conteo de HOY a AYER, recalcula la Tendencia 📈/➡️/📉/❌, añade fila al
  Histórico). Si es nueva → añádela con ID correlativo.
- Hojas: "Ofertas" (las verificadas), "Pendientes" (prometedoras sin conteo o
  bajo umbral + huecos 💡), "Histórico" (fecha | ID | producto | ads de hoy),
  "Log de búsquedas" (fecha | keywords usadas | resultados útiles).
- Mantén el formato: encabezados con color, filtros, links como hipervínculos.

## Resumen final (imprímelo claro)

Cuántas ofertas nuevas y de cuántos verticales; cuáles subieron anuncios (con
delta, p. ej. 40→70); cuáles se apagaron; TOP 3 del día con una línea de
justificación cada una. SÉ HONESTO: si no llegaste al PISO_DIARIO, dilo y
muestra lo que sí salió con su conteo real. Nunca infles números ni inventes links.
