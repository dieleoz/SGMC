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

random.seed(20260809)   # reproducible: el mismo inventario en cada ejecucion

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
LARGO_KM = 137.03

# Los 18 tipos que se cuentan por unidades, del Plan Maestro. Suman 355.
TIPOS = [
    ("SOS",  "S.O.S (Postes de Auxilio)",        54, 1),
    ("CCTV", "Camara CCTV",                      26, 2),
    ("PMVF", "PMV Fijo (Portico)",               11, 3),
    ("PMVM", "PMV Movil (Remolque)",             19, 4),
    ("SGE",  "Galibo Electronico",                4, 6),
    ("SGM",  "Galibo Mecanico",                   4, 5),
    ("SSA",  "Sensor Ambiental",                  4, 7),
    ("ETD",  "Estacion Toma Datos",               4, 7),
    ("PSEG", "Paso Seguro",                      16, 7),
    ("SWL3", "Switch Capa 3",                     4, 12),
    ("SWIT", "Switch Capa 2",                   142, 12),
    ("PJC",  "Peaje Carril",                     12, 9),
    ("PJE",  "Peaje Electronica",                12, 9),
    ("SERV", "Servidor",                          7, 16),
    ("BASC", "Bascula Dinamica",                  2, 9),
    ("OCR",  "Camara OCR Pesaje",                 2, 2),
    ("PORT", "Computador Portatil",              29, 16),
    ("IMPR", "Impresora",                         3, 17),
]


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


filas = []
n = 0
for prefijo, nombre, cantidad, tipo_id in TIPOS:
    for i in range(1, cantidad + 1):
        n += 1
        # repartidos uniformemente, cada tipo con su propio desfase
        frac = ((i - 0.5) / cantidad + hash(prefijo) % 7 / 100.0) % 1.0
        filas.append({
            "ActivoID": str(n),
            "CodigoActivo": "%s_%d" % (prefijo, i),
            "Nombre": "%s %03d" % (nombre, i),
            "TipoActivoID": str(tipo_id),
            "UnidadFuncionalID": str(unidad_funcional(frac)),
            "PR": pr(frac),
            "CalzadaID": str(1 + (n % 2)),
            "Ubicacion": punto(frac),
            "EstadoActivoID": "1",
            "CodigoQR": "",
            "SentidoID": "SA" if n % 2 else "AS",
            "Activo": "TRUE",
            "FrecuenciaID": "",
            "Observaciones": "COORDENADA SINTETICA - pendiente levantamiento D-01",
            "Criticidad": "",
            "FechaBaja": "",
            "MotivoBaja": "",
        })

COLS = ["ActivoID", "CodigoActivo", "Nombre", "TipoActivoID", "UnidadFuncionalID",
        "PR", "CalzadaID", "Ubicacion", "EstadoActivoID", "CodigoQR", "SentidoID",
        "Activo", "FrecuenciaID", "Observaciones", "Criticidad", "FechaBaja", "MotivoBaja"]

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
print("%-6s %-32s %6s" % ("COD", "TIPO", "CANT"))
for prefijo, nombre, cantidad, _ in TIPOS:
    print("%-6s %-32s %6d" % (prefijo, nombre, cantidad))
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
