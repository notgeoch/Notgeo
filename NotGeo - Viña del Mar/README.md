# NotGeo — Viña del Mar

Plataforma de monitoreo ambiental satelital para Viña del Mar, Chile.

**🌐 Sitio web:** https://notgeoch.github.io/Notgeo

## Indicadores disponibles

| Indicador | Fuente | Escala |
|-----------|--------|--------|
| NDVI — Vegetación | Sentinel-2 / Landsat | Mensual + Anual |
| AOD — Aerosoles | MODIS | Mensual + Anual |
| NO₂ — Dióxido de nitrógeno | Sentinel-5P | Mensual + Anual |
| SO₂ — Dióxido de azufre | Sentinel-5P | Mensual + Anual |
| LST — Temperatura superficial | Landsat | Mensual + Anual |
| Huella Urbana | Sentinel-1 + Sentinel-2 | Anual |

## Estructura

```
Notgeo/
├── index.html          ← Página principal
├── explorer.html       ← Explorador de mapas interactivos
├── assets/
│   ├── css/            ← Estilos
│   ├── js/             ← Lógica de mapas (generada por el pipeline)
│   └── data/           ← Datos (GeoTIFF, GeoJSON, CSV — generados por el pipeline)
└── scripts/gee/        ← Pipeline Python (Google Earth Engine → GitHub Pages)
```

## Pipeline de datos

El pipeline procesa imágenes satelitales en Google Earth Engine y descarga los resultados al repo:

```bash
# Instalar dependencias
pip install -r requirements-gee.txt

# Autenticar con Earth Engine (cuenta notgeoch@gmail.com)
earthengine authenticate

# Ejecutar pipeline completo
python -m scripts.gee.pipeline

# Solo descargar desde Drive (sin procesar)
python -m scripts.gee.drive.download_drive_to_repo
```

## Tecnologías

- **Frontend:** HTML + Leaflet + MapLibre GL + GeoTIFF.js + Bootstrap 5
- **Datos:** Google Earth Engine + Google Drive
- **Hosting:** GitHub Pages (gratuito)

---
*Basado en la arquitectura de GENIUS UPLA (Quilpué)*
