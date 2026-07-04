"""02 · Índices espectrales de vegetación (Sentinel-2).

Bandas S2: B2 Azul · B3 Verde · B4 Rojo · B5 Red Edge · B8 NIR · B11 SWIR.
Reflectancia = DN / 10000.
"""
import ee

L_SAVI = 0.5  # factor de corrección de suelo


def _refl(img: ee.Image) -> ee.Image:
    return img.divide(10000)


def ndvi(img: ee.Image) -> ee.Image:
    return img.normalizedDifference(["B8", "B4"]).rename("ndvi")


def evi(img: ee.Image) -> ee.Image:
    r = _refl(img)
    return r.expression(
        "2.5 * (NIR - RED) / (NIR + 6*RED - 7.5*BLUE + 1)",
        {"NIR": r.select("B8"), "RED": r.select("B4"), "BLUE": r.select("B2")},
    ).rename("evi")


def savi(img: ee.Image) -> ee.Image:
    r = _refl(img)
    return r.expression(
        "((NIR - RED) / (NIR + RED + L)) * (1 + L)",
        {"NIR": r.select("B8"), "RED": r.select("B4"), "L": L_SAVI},
    ).rename("savi")


def ndre(img: ee.Image) -> ee.Image:
    return img.normalizedDifference(["B8", "B5"]).rename("ndre")


def gndvi(img: ee.Image) -> ee.Image:
    return img.normalizedDifference(["B8", "B3"]).rename("gndvi")


def ndwi(img: ee.Image) -> ee.Image:
    return img.normalizedDifference(["B8", "B11"]).rename("ndwi")


FORMULAS = {
    "ndvi": ndvi,
    "evi": evi,
    "savi": savi,
    "ndre": ndre,
    "gndvi": gndvi,
    "ndwi": ndwi,
}


def aplicar(coleccion: ee.ImageCollection, indice: str) -> ee.ImageCollection:
    """Mapea el índice elegido sobre toda la colección."""
    fn = FORMULAS[indice]
    return coleccion.map(fn)
