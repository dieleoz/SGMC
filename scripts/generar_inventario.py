# -*- coding: utf-8 -*-
"""Genera el inventario de 355 activos repartidos por el corredor.

PARA PRUEBAS. Los codigos son reales -salen del Plan Maestro- pero las
coordenadas son SINTETICAS: se interpolan sobre el trazado del corredor con
dispersion aleatoria. Sirven para ejercitar el geofencing, la navegacion y el
filtro por zona. NO son el levantamiento de campo, que es la decision D-01.

Cada fila lleva Observaciones = "COORDENADA SINTETICA - pendiente levantamiento"
para que nadie las confunda con las reales.

El corredor: El Sisga (Cundinamarca) - Macheta - Guateque - Santa Maria -
San Luis de Gaceno - El Secreto - Aguaclara (Casanare). 137,03 km.

Uso:  python scripts/generar_inventario.py
"""
import os
import random
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "scripts"))

try:
    import openpyxl
except ImportError:
    print("Falta openpyxl."); sys.exit(2)



# Los sinteticos arrancan en 1000 para NO pisar identificadores vivos.
# El 2026-08-09 arrancaban en 1 y reescribieron los 34 activos reales: las seis
# ordenes existentes pasaron a apuntar a otro equipo -ActivoID 26 era FO-001, la
# fibra optica, y quedo como un poste SOS- y la referencia seguia resolviendo,
# asi que ningun verificador lo veia.
BASE_ID = 1000

# Trazado del corredor, de oeste a este. Puntos de paso conocidos.
TRAZADO = [
    (5.100, -73.720, "El Sisga"),
    (5.080, -73.610, "Macheta"),
    (5.000, -73.470, "Guateque"),
    (4.860, -73.260, "Santa Maria"),
    (4.820, -73.170, "San Luis de Gaceno"),
    (4.795, -73.020, "El Secreto"),
    (4.780, -72.900, "Aguaclara"),
]
LARGO_KM = 137.03   # longitud oficial del corredor

# El trazado de arriba es una aproximacion de 7 puntos: su poligonal mide menos
# que el corredor real, que serpentea. El PR se escala a los 137,03 oficiales
# para que las cifras sean las que usa operacion.

# Las familias y su tipo salen de catalogo_tipos.py, que es la fuente unica.
#
# Aqui estaban escritas a mano, con el TipoActivoID puesto al lado de cada una.
# Nueve apuntaban al tipo de otra cosa -la impresora al del NAS, el portatil al
# del servidor, el carril de peaje al de la bascula- y eran 78 activos de 355
# con el checklist equivocado. Al no vivir el reparto en ningun sitio
# comprobable, nadie podia verlo.
from catalogo_tipos import FAMILIAS, tipo_de_familia


def punto(frac):
    """Coordenada a la fraccion `frac` del corredor, con dispersion lateral."""
    n = len(TRAZADO) - 1
    pos = frac * n
    i = min(int(pos), n - 1)
    t = pos - i
    lat = TRAZADO[i][0] + (TRAZADO[i + 1][0] - TRAZADO[i][0]) * t
    lon = TRAZADO[i][1] + (TRAZADO[i + 1][1] - TRAZADO[i][1]) * t
    # +-150 m perpendicular, que es el ancho razonable de una via y sus margenes
    lat += random.uniform(-0.0013, 0.0013)
    lon += random.uniform(-0.0013, 0.0013)
    return "%.6f, %.6f" % (lat, lon)


def pr(frac):
    """Punto de referencia INVIAS, formato PR km+metros."""
    km = frac * LARGO_KM
    return "%02d+%03d" % (int(km), int(round((km - int(km)) * 1000)))


def unidad_funcional(frac):
    """Cuatro UF repartidas por el corredor. IDs 7 a 10, como en la hoja."""
    return 7 + min(int(frac * 4), 3)


COLS = ["ActivoID", "CodigoActivo", "Nombre", "TipoActivoID", "UnidadFuncionalID",
        "PR", "CalzadaID", "Ubicacion", "EstadoActivoID", "CodigoQR", "SentidoID",
        "Activo", "FrecuenciaID", "Observaciones", "Criticidad", "FechaBaja", "MotivoBaja"]


def generar_filas():
    """Los 355 activos sinteticos. Lo llama tambien generar_plantilla.py.

    Reproducible: misma semilla, mismo reparto, mismas coordenadas. El desfase
    por familia se deriva de las letras del prefijo porque hash() de una cadena
    va salado por proceso y reasignaba PR, unidad funcional y coordenada de los
    355 en cada ejecucion.
    """
    random.seed(20260809)
    filas = []
    n = 0
    for prefijo, nombre, cantidad, clave_tipo, frec in FAMILIAS:
        for i in range(1, cantidad + 1):
            n += 1
            desfase = sum(ord(x) for x in prefijo) % 7 / 100.0
            frac = ((i - 0.5) / cantidad + desfase) % 1.0
            filas.append({
                "ActivoID": BASE_ID + n,
                "CodigoActivo": "%s_%d" % (prefijo, i),
                "Nombre": "%s %03d" % (nombre, i),
                "TipoActivoID": tipo_de_familia(clave_tipo),
                "UnidadFuncionalID": unidad_funcional(frac),
                "PR": pr(frac),
                "CalzadaID": 1 + (n % 2),
                "Ubicacion": punto(frac),
                "EstadoActivoID": 1,
                "CodigoQR": "",
                "SentidoID": "SA" if n % 2 else "AS",
                "Activo": "TRUE",
                "FrecuenciaID": frec,
                "Observaciones": "ACTIVO SINTETICO DE PRUEBA - NO ES INVENTARIO REAL",
                "Criticidad": "",
                "FechaBaja": "",
                "MotivoBaja": "",
            })
    return filas


if __name__ == "__main__":
    filas = generar_filas()

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "ACT_Activos"
    ws.append(COLS)
    for f in filas:
        ws.append([f[c] for c in COLS])

    salida = os.path.join(RAIZ, "BD", "ACT_Activos_355_SINTETICO.xlsx")
    wb.save(salida)

    print("Generado:", salida)
    print()
    print("%-6s %-32s %6s %6s" % ("COD", "TIPO", "CANT", "TIPO_ID"))
    for prefijo, nombre, cantidad, clave, frec in FAMILIAS:
        print("%-6s %-32s %6d %6d  frec=%s"
              % (prefijo, nombre, cantidad, tipo_de_familia(clave), frec or "a demanda"))
    print()
    print("TOTAL: %d activos" % len(filas))
    print()
    print("Muestra:")
    for f in [filas[0], filas[53], filas[54], filas[200], filas[-1]]:
        print("   %-10s %-26s UF%-3s PR %-8s %s"
              % (f["CodigoActivo"], f["Nombre"][:26], f["UnidadFuncionalID"], f["PR"], f["Ubicacion"]))
    print()
    print("Coordenadas: interpoladas sobre el trazado real del corredor,")
    print("con +-150 m de dispersion. SINTETICAS, no de campo.")
