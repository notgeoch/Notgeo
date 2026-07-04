"""04 · Export: descarga el producto final como GeoTIFF.

El área de Viña del Mar a 10 m (~1.2M pixeles, 1 banda) pesa unos pocos MB,
dentro del límite de getDownloadURL — descarga directa, sin pasar por Drive.
"""
from pathlib import Path

import ee
import requests

from config import CRS, OUT_DIR, SCALE


def exportar(img: ee.Image, indice: str, anio: int, mes: int, region: ee.Geometry) -> Path:
    out = OUT_DIR / indice
    out.mkdir(parents=True, exist_ok=True)
    destino = out / f"{indice}_{anio}-{mes:02d}.tif"

    url = img.getDownloadURL({
        "region": region,
        "scale": SCALE,
        "crs": CRS,
        "format": "GEO_TIFF",
    })

    r = requests.get(url, timeout=600)
    r.raise_for_status()
    destino.write_bytes(r.content)
    mb = destino.stat().st_size / 1e6
    print(f"  ✔ {destino.relative_to(OUT_DIR.parent.parent.parent)} ({mb:.1f} MB)")
    return destino
