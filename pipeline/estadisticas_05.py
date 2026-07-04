"""05 · Estadísticas zonales: promedio del índice y fracción verde por zona censal."""
import json
from pathlib import Path

import ee

from config import NDVI_VERDE, OUT_DIR, SCALE, ZONAS_GEOJSON


def _zonas() -> ee.FeatureCollection:
    with open(ZONAS_GEOJSON) as f:
        gj = json.load(f)
    feats = [
        ee.Feature(ee.Geometry(ft["geometry"]),
                   {"zona": str(ft["properties"].get("GEOCODIGO", i))})
        for i, ft in enumerate(gj["features"])
    ]
    return ee.FeatureCollection(feats)


def estadisticas(img: ee.Image, indice: str, anio: int, mes: int) -> Path:
    """Promedio por zona censal; para NDVI agrega fracción de superficie 'verde'.

    Con imagen multibanda, reduceRegions repite el reductor por banda y nombra
    cada salida como la banda -> columnas 'ndvi' y 'frac_verde'.
    """
    banda = img.select(indice)
    if indice == "ndvi":
        banda = banda.addBands(banda.gte(NDVI_VERDE).rename("frac_verde"))

    stats = banda.reduceRegions(
        collection=_zonas(), reducer=ee.Reducer.mean(), scale=SCALE
    )

    data = stats.getInfo()
    filas = []
    for ft in data["features"]:
        p = ft["properties"]
        # Con 1 banda la columna se llama 'mean'; con varias, el nombre de la banda.
        valor = p.get(indice, p.get("mean"))
        fila = {"zona": p.get("zona")}
        fila[indice] = None if valor is None else round(valor, 4)
        if "frac_verde" in p and p["frac_verde"] is not None:
            fila["frac_verde"] = round(p["frac_verde"], 4)
        filas.append(fila)

    out = OUT_DIR / indice
    out.mkdir(parents=True, exist_ok=True)
    destino = out / f"{indice}_{anio}-{mes:02d}_zonas.json"
    destino.write_text(json.dumps(filas, ensure_ascii=False, indent=1))
    print(f"  ✔ estadísticas zonales → {destino.name} ({len(filas)} zonas)")
    return destino
