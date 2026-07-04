"""Autenticación en Google Earth Engine con service account.

Busca la credencial en este orden:
1. Variable de entorno GEE_SERVICE_ACCOUNT_KEY (contenido JSON — GitHub Actions)
2. Archivo local indicado en GEE_KEY_FILE
"""
import json
import os

import ee

from config import GEE_PROJECT


def init_ee():
    key_json = os.environ.get("GEE_SERVICE_ACCOUNT_KEY")
    key_file = os.environ.get("GEE_KEY_FILE")

    if key_json:
        info = json.loads(key_json)
        credentials = ee.ServiceAccountCredentials(info["client_email"], key_data=key_json)
    elif key_file and os.path.exists(key_file):
        with open(key_file) as f:
            info = json.load(f)
        credentials = ee.ServiceAccountCredentials(info["client_email"], key_file)
    else:
        raise SystemExit(
            "Sin credenciales: define GEE_SERVICE_ACCOUNT_KEY (JSON) o GEE_KEY_FILE (ruta)."
        )

    ee.Initialize(credentials, project=GEE_PROJECT)
    print(f"✔ Earth Engine inicializado · proyecto {GEE_PROJECT} · {info['client_email']}")
