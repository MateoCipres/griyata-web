# Griyata Parfums

Catálogo web de Griyata Parfums: perfumes árabes originales, sellados de fábrica. Pedidos por WhatsApp.

- `index.html`: la página publicada (generada, no editar a mano).
- `fuente/plantilla.html`: el código de la página.
- `fuente/data.json`: perfumes, precios y notas.
- `fuente/fotos/`, `fuente/logo.png`: imágenes.

Para publicar un cambio: doble clic en `publicar.bat` (arma la página, guarda y sube a GitHub).

## Actualización automática

La página se actualiza sola desde la planilla de Google (hojas publicadas "Catálogo" y "Fotos", nunca "Stock").
GitHub corre `actualizar.py` cada 15 minutos (`.github/workflows/actualizar.yml`): lee la planilla, baja las fotos nuevas, arma la página y la publica si algo cambió.
Para forzarlo: pestaña Actions → "Actualizar desde la planilla" → Run workflow.
