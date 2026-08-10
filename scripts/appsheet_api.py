# -*- coding: utf-8 -*-
"""Cliente de API REST de AppSheet v2 para el proyecto SGMC.

Permite consultar, agregar, editar y eliminar datos directamente a través de
la API oficial de AppSheet (api.appsheet.com), respetando la lógica de la app.

Cual es la app la dice scripts/sistema.py. No se escribe aqui.

AVISO: este cliente NO lo pidio nadie y no forma parte del alcance. La API REST
de AppSheet requiere plan de pago y la aplicacion es Prototype, asi que lo mas
probable es que no responda. Ademas expone Delete contra datos de produccion, y
la regla del proyecto es que el historico no se borra. Antes de usarlo, decidir
si se queda.
"""

import json
import os
import sys
import urllib.request
import urllib.error

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "scripts"))
from modelo_objetivo import MODELO
from sistema import APP_ID as APP_ID_VIGENTE, APP_NOMBRE

# Cargar .env si existe en la raíz
env_file = os.path.join(RAIZ, ".env")
if os.path.exists(env_file):
    with open(env_file, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                os.environ.setdefault(key.strip(), val.strip())

APP_ID = os.environ.get("APPSHEET_APP_ID", APP_ID_VIGENTE)
API_KEY = os.environ.get("APPSHEET_API_KEY", "")
API_URL = "https://api.appsheet.com/api/v2/apps/{app_id}/tables/{table_name}/Action"


def ejecutar_accion(tabla, accion, filas=None, propiedades=None):
    """Ejecuta una acción (Find, Add, Edit, Delete) sobre una tabla en AppSheet API v2.
    
    Returns:
        dict/list parsed JSON de respuesta.
    """
    url = API_URL.format(app_id=APP_ID, table_name=tabla)
    payload = {
        "Action": accion,
        "Properties": propiedades or {
            "Locale": "es-CO",
            "Timezone": "SA Pacific Standard Time"
        }
    }
    if filas is not None:
        payload["Rows"] = filas

    data_bytes = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data_bytes,
        headers={
            "ApplicationAccessKey": API_KEY,
            "Content-Type": "application/json"
        }
    )

    try:
        with urllib.request.urlopen(req) as response:
            res_text = response.read().decode("utf-8")
            if not res_text:
                return []
            return json.loads(res_text)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8") if e.fp else ""
        raise RuntimeError(f"Error HTTP {e.code} en tabla {tabla}: {e.reason}. Detalle: {body}")
    except urllib.error.URLError as e:
        raise RuntimeError(f"Error de conexión en tabla {tabla}: {e.reason}")


def buscar(tabla, selector=None):
    """Obtiene filas de la tabla especificada."""
    props = {"Locale": "es-CO", "Timezone": "SA Pacific Standard Time"}
    if selector:
        props["Selector"] = selector
    return ejecutar_accion(tabla, "Find", propiedades=props)


def agregar(tabla, filas):
    """Agrega una o más filas a la tabla especificada."""
    return ejecutar_accion(tabla, "Add", filas=filas)


def editar(tabla, filas):
    """Edita una o más filas en la tabla especificada (requiere la clave primaria)."""
    return ejecutar_accion(tabla, "Edit", filas=filas)


def eliminar(tabla, filas):
    """Elimina una o más filas en la tabla especificada (requiere la clave primaria)."""
    return ejecutar_accion(tabla, "Delete", filas=filas)


def verificar_tablas_appsheet():
    """Recorre las 28 tablas del modelo objetivo y prueba la API de AppSheet en cada una."""
    print("=" * 78)
    print("VERIFICACION DE CONEXION API APPSHEET — LAS 28 TABLAS DEL MODELO")
    print("=" * 78)
    print(f"App ID:  {APP_ID}")
    print(f"API Key: {API_KEY[:8]}...{API_KEY[-6:]}")
    print("-" * 78)

    exitos, errores = 0, 0
    resumen = []

    for tabla in sorted(MODELO.keys()):
        try:
            filas = buscar(tabla)
            num_filas = len(filas) if isinstance(filas, list) else 0
            cols = list(filas[0].keys()) if num_filas > 0 else []
            num_cols = len(cols)
            resumen.append((tabla, "OK", num_filas, num_cols))
            print(f"  OK   {tabla:<25} | {num_filas:>4} filas | {num_cols:>3} columnas")
            exitos += 1
        except Exception as e:
            resumen.append((tabla, "ERROR", 0, str(e)))
            print(f"  FAIL {tabla:<25} | ERROR: {e}")
            errores += 1

    print("=" * 78)
    print(f"RESULTADO: {exitos}/28 tablas accesibles vía API. Errores: {errores}")
    print("=" * 78)
    return errores == 0


if __name__ == "__main__":
    verificar_tablas_appsheet()
