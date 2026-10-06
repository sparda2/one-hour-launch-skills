# La estructura de página de ventas probada (destilada de las páginas de referencia)

Este es el esqueleto que sigue cada página generada. Está sacado de ingeniería inversa de una página de ventas larga y sin VSL que está escalando ahora mismo (la referencia "peptides"), contrastada con la propia página del usuario. Mantén el ORDEN; adapta el contenido al producto. Una sección solo se omite si el producto de verdad no tiene material honesto para ella — jamás se rellena con prueba inventada.

## Orden de las secciones (arriba → abajo)

1. **Barra de anuncio (sticky).** Una línea: la promesa central o el marco del lanzamiento. Deadline honesto opcional (ver reglas de integridad).
2. **Hero.** Titular grande y específico (el resultado, hoy/esta semana, concreto), un subtítulo de una línea, la imagen mockup del producto, 3 chips de confianza (p. ej. "acceso inmediato · pago único · garantía <real>"), CTA principal. Sin precio en el hero.
3. **Mecanismo / "cómo funciona".** El producto mostrado como un sistema en 3 pasos, cada uno con su sub-imagen. Convierte un PDF/app en una "máquina que produce el resultado".
4. **La verdad incómoda / agitación del problema.** Nombra la situación dolorosa actual del lector con sus propias palabras (info dispersa, prueba y error, dinero perdido). Refleja el hook del anuncio.
5. **Lo que logras / bullets de resultado.** El estado posterior, orientado al beneficio, específico. Empareja cada dolor del §4 con su solución.
6. **Lo que incluye (entregables).** Cada módulo/activo con una línea de valor y una miniatura. Aquí se construye el valor percibido.
7. **Para quién es / para quién no.** Dos columnas. Califica al comprador y sube la convicción.
8. **Prueba (SOLO real).** Testimonios con atribución, capturas tipo chat, ratings — SOLO si el usuario los aporta. Si no, un bloque placeholder que el usuario rellena; jamás caras de stock presentadas como clientes.
9. **Stack de oferta + revelación del precio.** Lista todo lo incluido con una línea de "valor" honesta, luego el precio real, luego el CTA. Marco de pago único, bonos, regalos.
10. **Garantía.** La garantía real, dicha claro, con el sello. Reversión de riesgo.
11. **Urgencia (SOLO honesta).** Un deadline de lanzamiento real o un cupo real. Si no hay escasez real, usa urgencia anclada en el valor ("el precio de lanzamiento sube después del lanzamiento") sin contadores en vivo falsos. Ver reglas de integridad.
12. **FAQ.** 5–8 objeciones reales respondidas, la última sobre el reembolso.
13. **CTA final + recap del precio.** Repite la oferta y el botón.
14. **Footer + aviso legal.** Copyright, la línea "no afiliado a Meta/Facebook", enlaces a privacidad/términos/reembolso.
15. **Popup de salida (opcional).** Reitera la oferta una vez. Solo marco honesto.

Los CTA se repiten cada ~1,5 pantallas en una página larga (la de peptides tiene 8). Todos los CTA principales apuntan al MISMO siguiente paso (checkout). El texto de cada CTA varía ("Obtener acceso inmediato", "Quiero esta oferta", "Consigue X por $Y").

## Gatillos psicológicos que vale la pena copiar (usados por las referencias)

- **Titular específico y orientado al resultado** con marco temporal ("tu primer protocolo armado esta noche").
- **Nombrar el mecanismo** — dale un nombre de marca al método/app para que se sienta un sistema, no un archivo.
- **Apilar valor** antes del precio, luego un precio único que parece pequeño frente al stack.
- **Reversión de riesgo** — una garantía concreta y condicional ("si en N días no hiciste X, 100% de vuelta").
- **Dos opciones / para quién es** como calificación.
- **FAQ que maneja objeciones** terminando en el reembolso.
- **Repetición de CTA** con textos variados, todos a un checkout.
- **Barra de anuncio + popup de salida** para recuperar atención.
- **Mobile-first**: el tráfico real es móvil; diseña para el teléfono primero.

## Gatillos a usar SOLO cuando son reales (reglas de integridad — innegociables)

Estas son las partes engañosas de la página de referencia. La skill puede construir el COMPONENTE, pero solo cableado a datos verdaderos que el usuario confirme:

- **Contador / countdown** → solo para un deadline real (un lanzamiento que de verdad termina, un carrito que de verdad cierra). Nunca un contador por visitante que se reinicia al recargar.
- **Popups de stock / "compra en vivo" ("María acaba de comprar", "quedan 12")** → solo con datos reales de pedidos. Por defecto: APAGADO. Jamás inventar nombres, conteos ni "9 de 200 disponibles".
- **Testimonios / ratings / "4.9 (847 reseñas)"** → solo reales, aportados por el usuario, atribuibles. Jamás caras de stock (p. ej. randomuser.me) ni conteos de reseñas inventados.
- **Precios, ahorros, "valor $224"** → los números reales del checkout del usuario. Si una cifra no está verificada, no se muestra.
- **Claims médicos / de ingresos / de resultados** → siguen las reglas de compliance del nicho; mantén el aviso legal.

Cuando el usuario no aporta nada de lo anterior, la skill inserta un bloque claramente etiquetado `<!-- PLACEHOLDER: añadir testimonios reales aquí -->` y lo lista en el reporte final como "necesita prueba real antes de publicar". Una página que inventa prueba hace que baneen la cuenta de anuncios del negocio y es lo contrario de lo que una oferta escalando necesita a largo plazo.

## Qué sacar de los ANUNCIOS (Ads Library) hacia la página

Los anuncios que llevan tráfico fijan la expectativa del lector; la página debe coincidir con ellos (message match):
- El **hook / texto principal** de los top ads → el titular del hero y el lenguaje de dolor del §4.
- El **ángulo** que se está escalando (qué dolor, qué promesa) → el lead de la página.
- El **marco de oferta** (precio, bono, garantía) visto en los anuncios → mantenerlo consistente en la página.
- El **estilo visual** de los top ads de imagen → el look de las imágenes hero/mockup de la página.
Usa el método de conteo del Winning Offer Spy (conteo de anuncios activos a nivel de página) para saber qué anuncio escala de verdad, y modela ese.
