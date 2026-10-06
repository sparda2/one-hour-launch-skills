# Winning Offer Spy: checklist de configuración

Sigue estos pasos en orden. Son unos 15 minutos. Cada paso tiene una comprobación ✅ para que sepas que funcionó antes de seguir. El asistente que trae la skill también lo revisa todo, pero si lo dejas hecho antes no tendrás que reiniciar la sesión.

> ⚠️ **Esta skill TIENE que correr en Claude Code, no en el chat normal de Claude.**
> El spy abre la landing de cada competidor para verificar la oferta, corre entre 20 y 40 minutos y guarda su trabajo en tu Drive. Eso solo lo puede hacer Claude Code. En el chat normal no puede leer las landings y se queda atascado.

---

## Paso 1: Ten una cuenta publicitaria de Meta activa

Meta solo te deja buscar en la Ads Library desde Claude si tienes al menos una cuenta publicitaria **activa**.

1. Entra en **business.facebook.com** → **Configuración del negocio** → **Cuentas publicitarias**.
2. Si no tienes ninguna, créala. Si la tuya está desactivada, reactívala. Meta suele pedir un método de pago. No hace falta lanzar ningún anuncio.

✅ Tu cuenta publicitaria aparece como **Activa**.

## Paso 2: Conecta Meta a Claude (el MCP de Meta)

1. Entra en **claude.ai → Personalizar → Conectores** (claude.ai/customize/connectors).
2. Haz clic en **+** → **Añadir conector personalizado**.
3. Rellena:
   - **Nombre:** `Meta`
   - **URL:** `https://mcp.facebook.com/ads`
4. Haz clic en **Añadir** y luego en **Conectar**.
5. Inicia sesión con la cuenta de Facebook que gestiona tu cuenta publicitaria y **aprueba todos los permisos** que pide (anuncios, negocio, páginas).

✅ El conector Meta aparece como **Conectado**.

## Paso 3: Conecta Google Drive Y Google Sheets

Son **dos conectores distintos** y necesitas los dos.

1. En la misma página de Conectores, busca **Google Drive** → **Conectar** → elige tu cuenta de Google → **Permitir**.
2. Busca **Google Sheets** → **Conectar** → **Permitir**.

✅ Google Drive y Google Sheets aparecen los dos como **Conectados**.

## Paso 4: Instala la skill

1. Descarga `dist/winning-offer-spy-ES.zip` del pack.
2. Entra en **claude.ai → Configuración → Capacidades → Skills → Subir skill** y elige el ZIP.

✅ "winning-offer-spy-es" aparece en tu lista de skills. También queda disponible automáticamente en las sesiones en la nube de Claude Code.

## Paso 5: Abre Claude Code en la nube con acceso completo a internet

1. Abre la **app de escritorio de Claude → Code → Cloud**, o entra en **claude.ai/code**.
2. Abre una sesión nueva. Si te pide un repositorio, cualquiera de los tuyos sirve: el spy guarda todo en tu Drive.
3. Activa el **acceso completo a internet**, para que el spy pueda abrir las landings de la competencia:
   - En la barra del título de la sesión, haz clic en el **menú del entorno** → **Edit**.
   - **Network access → Full** → **Save**.
   - **Abre una sesión nueva.** El cambio solo aplica a las sesiones que se abran después de guardar.
4. En la sesión nueva:
   - Abre su **menú de conectores** y comprueba que **Meta**, **Google Drive** y **Google Sheets** están **activados**.
   - Elige el modo de permisos **Auto**, para que la caza no se pare a pedir aprobación a cada paso.

## Paso 6: Comprueba que todo funciona (copia estos prompts)

Envíalos de uno en uno en tu sesión nueva de Claude Code:

| Prompt | Lo que deberías ver |
|---|---|
| `¿tienes acceso a ads_library_search?` | "Sí" |
| `Haz una búsqueda de prueba en la Ads Library: "shoes", US, anuncios activos.` | Unos cuantos anuncios y un conteo total estimado |
| `Abre https://gumroad.com y dime su título.` | El título de la página. Eso significa que el acceso completo a internet funciona |

> Si Claude intenta abrir `facebook.com` directamente y recibe un **403**, es normal. Facebook bloquea las visitas automáticas. La Ads Library se lee por el conector de Meta, así que no le afecta.

## Paso 7: Configura y haz tu primera caza

Escribe:

```
Configura Winning Offer Spy paso a paso y luego haz mi primera caza.
```

El asistente:
- crea tu carpeta **"Winning Offer Spy"** y tu Google Sheet maestro en tu Drive, y te da el link;
- te pregunta tu **filtro de producto**, tus **nichos**, tus **páginas de Facebook**, los **idiomas** y los **umbrales**, en máximo 2 rondas;
- hace una prueba rápida y luego tu primera caza (20–40 minutos). Puedes cerrar la ventana: sigue corriendo en la nube.

✅ Recibes un resumen con tus 3 mejores ofertas y tu hoja queda rellena.

---

## Problemas comunes

| Problema | Solución |
|---|---|
| "No tengo acceso a ads_library_search" | El conector de Meta no está conectado, o está desactivado en el menú de conectores de esta sesión. Arréglalo (Paso 2) y abre una sesión nueva |
| La Ads Library da un error de cuenta publicitaria | No tienes una cuenta publicitaria **activa** (Paso 1). Después de activarla, desconecta y vuelve a conectar el conector de Meta |
| "No puedo crear o escribir la hoja" | Falta conectar Google Sheets. Lo necesitas **además** de Google Drive (Paso 3) |
| Las landings no abren, o sale "EGRESS_BLOCKED" | El acceso a internet no está en **Full**, o sigues en una sesión que se abrió antes del cambio (Paso 5) |
| `facebook.com` devuelve 403 | Es normal, no hay nada que arreglar |
| Te pide aprobación todo el rato | Cambia la sesión al modo de permisos **Auto** |
| Estás en el chat normal de Claude | Pásate a **Claude Code → Cloud** (Paso 5). Desde el chat normal el spy no puede leer las landings |
