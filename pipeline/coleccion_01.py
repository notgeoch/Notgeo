"""01 · Colección: filtra Sentinel-2 por fecha, nubes y área de interés.

Nada se descarga aquí: se define la colección que GEE procesará en la nube.
"""
import json

import ee

from config import AOI_GEOJSON, MAX_CLOUD_PCT, S2_COLLECTION


def aoi() -> ee.Geometry:
    """Límite comunal de Viña del Mar como geometría EE."""
    with open(AOI_GEOJSON) as f:
        gj = json.load(f)
    feature = gj["features"][0]
    return ee.Geometry(feature["geometry"])


def mask_clouds_scl(img: ee.Image) -> ee.Image:
    """Enmascara nubes/sombras usando la banda SCL (Scene Classification Layer).

    Clases removidas: 3 sombra de nube, 8 nube media prob., 9 nube alta prob.,
    10 cirros, 11 nieve.
    """
    scl = img.select("SCL")
    mask = (
        scl.neq(3).And(scl.neq(8)).And(scl.neq(9)).And(scl.neq(10)).And(scl.neq(11))
    )
    return img.updateMask(mask)


def s2_collection(start: str, end: str, region: ee.Geometry) -> ee.ImageCollection:
    """Colección Sentinel-2 SR armonizada, filtrada y enmascarada.

    start / end: fechas ISO 'YYYY-MM-DD'.
    """
    return (
        ee.ImageCollection(S2_COLLECTION)
        .filterDate(start, end)
        .filterBounds(region)
        .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", MAX_CLOUD_PCT))
        .map(mask_clouds_scl)
    )
