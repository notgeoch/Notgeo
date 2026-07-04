"""03 · Composite mensual: mediana del índice sobre el mes, recortado al AOI."""
import ee

from coleccion_01 import s2_collection
from indices_02 import aplicar


def composite_mensual(anio: int, mes: int, indice: str, region: ee.Geometry) -> ee.Image:
    """Mediana mensual del índice, recortada al límite comunal.

    Devuelve una imagen de 1 banda (nombre = índice) o lanza ValueError
    si el mes no tiene escenas utilizables.
    """
    start = ee.Date.fromYMD(anio, mes, 1)
    end = start.advance(1, "month")

    col = s2_collection(start.format("YYYY-MM-dd").getInfo(),
                        end.format("YYYY-MM-dd").getInfo(),
                        region)

    n = col.size().getInfo()
    if n == 0:
        raise ValueError(f"Sin escenas S2 utilizables para {anio}-{mes:02d}")

    img = aplicar(col, indice).median().clip(region)
    print(f"  {anio}-{mes:02d} · {indice.upper()} · {n} escenas")
    return img.set({"year": anio, "month": mes, "index": indice, "n_scenes": n})
