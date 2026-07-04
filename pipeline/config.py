"""Configuración central del pipeline NotGeo."""
from pathlib import Path

# ── Proyecto GEE ──
GEE_PROJECT = "notgeo-497602"

# ── Rutas ──
REPO_ROOT = Path(__file__).resolve().parent.parent
VECTORES = REPO_ROOT / "assets" / "data" / "vectores"
AOI_GEOJSON = VECTORES / "limite_comunal.geojson"
ZONAS_GEOJSON = VECTORES / "zonas_censales.geojson"
OUT_DIR = REPO_ROOT / "assets" / "data" / "productos"

# ── Sentinel-2 ──
S2_COLLECTION = "COPERNICUS/S2_SR_HARMONIZED"
MAX_CLOUD_PCT = 40          # filtro por metadato de escena
SCALE = 10                  # m/pixel
CRS = "EPSG:32719"          # UTM 19S

# ── Índices disponibles (fórmulas en indices_02.py) ──
INDICES = ["ndvi", "evi", "savi", "ndre", "gndvi", "ndwi"]

# ── Umbral para "área verde" (fracción de pixel con vegetación vigorosa) ──
NDVI_VERDE = 0.4
