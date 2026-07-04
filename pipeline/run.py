"""Orquestador del pipeline NotGeo.

Uso:
  python run.py                              # NDVI del mes pasado
  python run.py --index ndvi --start 2024-01 --end 2024-06
  python run.py --index evi --start 2025-03 --end 2025-03 --sin-stats
"""
import argparse
from datetime import date

from auth import init_ee
from coleccion_01 import aoi
from composite_03 import composite_mensual
from config import INDICES
from estadisticas_05 import estadisticas
from export_04 import exportar


def meses(desde: str, hasta: str):
    """Genera (año, mes) inclusive entre 'YYYY-MM' y 'YYYY-MM'."""
    y0, m0 = map(int, desde.split("-"))
    y1, m1 = map(int, hasta.split("-"))
    y, m = y0, m0
    while (y, m) <= (y1, m1):
        yield y, m
        m += 1
        if m > 12:
            m, y = 1, y + 1


def main():
    hoy = date.today()
    prev = date(hoy.year, hoy.month, 1)
    prev = date(prev.year - 1, 12, 1) if prev.month == 1 else date(prev.year, prev.month - 1, 1)
    default_mes = f"{prev.year}-{prev.month:02d}"

    p = argparse.ArgumentParser(description="Pipeline NotGeo · Sentinel-2 → índices → GeoTIFF")
    p.add_argument("--index", default="ndvi", choices=INDICES)
    p.add_argument("--start", default=default_mes, help="YYYY-MM (default: mes pasado)")
    p.add_argument("--end", default=None, help="YYYY-MM (default: igual a start)")
    p.add_argument("--sin-stats", action="store_true", help="omite estadísticas zonales")
    args = p.parse_args()
    end = args.end or args.start

    init_ee()
    region = aoi()
    print(f"→ {args.index.upper()} · {args.start} a {end}")

    ok, fail = 0, 0
    for anio, mes in meses(args.start, end):
        try:
            img = composite_mensual(anio, mes, args.index, region)
            exportar(img, args.index, anio, mes, region)
            if not args.sin_stats:
                estadisticas(img, args.index, anio, mes)
            ok += 1
        except ValueError as e:
            print(f"  ⚠ {e}")
            fail += 1

    print(f"Listo: {ok} meses exportados, {fail} sin datos.")


if __name__ == "__main__":
    main()
