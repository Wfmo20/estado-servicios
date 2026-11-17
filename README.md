# Estado de servicios

Página que muestra el estado de **Zoom, Microsoft Teams, Outlook / Microsoft 365 y Gmail**, junto con los servicios publicados en [status.informatica.uc.cl](https://status.informatica.uc.cl/).

## Cómo funciona

| Servicio | Fuente | Frecuencia |
|---|---|---|
| Zoom | API pública de status.zoom.us | En vivo, cada 3 min |
| Servicios UC (incluye Teams, Correo M365 y Zoom institucional) | API pública de status.informatica.uc.cl | En vivo, cada 3 min |
| Gmail | Google Workspace Status Dashboard | En vivo, cada 3 min |
| Microsoft 365 / Outlook / Teams (global) | status.cloud.microsoft, vía GitHub Actions (`scripts/microsoft.py`) → `data/microsoft.json` | Cada 15 min |

Microsoft no permite consultar su API directamente desde el navegador, por eso un workflow de GitHub Actions la descarga y guarda el resultado en el repositorio.

El botón **«Avisarme en este navegador»** muestra una notificación del sistema cuando un servicio empeora o se recupera (mientras la página esté abierta).

## Publicar en GitHub Pages

1. Sube esta carpeta a un repositorio de GitHub.
2. En **Settings → Pages**, elige *Deploy from a branch*, rama `main`, carpeta `/ (root)`.
3. En **Settings → Actions → General → Workflow permissions**, marca *Read and write permissions*.
4. En la pestaña **Actions**, ejecuta una vez «Actualizar estado Microsoft 365» con *Run workflow*.

La página quedará en `https://<usuario>.github.io/<repositorio>/`.

## Limitaciones

- El estado de Microsoft es el **global público**. Los incidentes que afectan solo a la cuenta de la universidad aparecen en el *Estado del servicio* del centro de administración de Microsoft 365, que requiere acceso de administrador, o en la sección UC de esta página.
- GitHub pausa los workflows programados si el repositorio pasa 60 días sin actividad. El workflow hace al menos un commit por hora, lo que lo mantiene activo.
