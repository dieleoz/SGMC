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
LARGO_KM = 137.17   # suma de las cuatro Unidades Funcionales del contrato
# Apendice Tecnico 1, Tabla 3, paginas 5 y 6: 50,01 + 22,00 + 17,80 + 47,36.
# La ANI y el Ministerio publican 137 km, y otros documentos del proyecto 137,03.
# Se usa la del contrato porque es la fuente contractual, y porque el propio
# contrato advierte que las longitudes son aproximadas y que mandan los PR.
#
# EL CORREDOR ATRAVIESA TRES RUTAS DE INVIAS, no una (Tabla 1, pagina 4):
#
#   55CN03   Cruce Ruta 55, Desviacion del Sisga   PR0+0+000 -> PR6+194
#   5607     Choconta (Brisas)                     PR7+146   -> PR46+080
#   5608     Guateque                              PR0+000   -> PR92+048
#
# Y AQUI ESTA LA PRUEBA DE QUE UN PR NO IDENTIFICA UN PUNTO: el corredor tiene
# DOS puntos distintos llamados "PR 0+000" -el arranque en el Sisga sobre la
# 55CN03 y Guateque sobre la 5608-, separados por unos 50 km. La ambiguedad no
# es una hipotesis: esta en la tabla del contrato.
#
# El PK, que es lineal y continuo de 0 al final, si identifica. Lo que este
# script genera es PR sin ruta, asi que vale para repartir los activos por el
# corredor y NO vale como referencia de campo.

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


# Las cuatro unidades funcionales REALES, con su nombre y su longitud.
#
# Fuente: ANI, "ABC del corredor de la Transversal del Sisga", consultado el
# 2026-08-10. Antes esto se repartia en cuartos iguales de 34,26 km, que era
# invencion nuestra: no son iguales ni de lejos -la primera mide 49 km y la
# tercera 18-, asi que cada activo sintetico caia en la UF equivocada en cuanto
# se alejaba de los extremos.
#
# (id, nombre, km_desde, km_hasta)
#
# Estas son las del CONTRATO, Apendice Tecnico 1, Tabla 3, paginas 5 y 6.
# Sustituyen a las de la pagina de la ANI, que venian redondeadas -49, 22, 18 y
# 47- y con los nombres cortos. El contrato manda.
UNIDADES = [
    (7,  "Sisga - Macheta - Manta - Guateque",                     0.00,  50.01),
    (8,  "Guateque - Garagoa - Macanal",                          50.01,  72.01),
    (9,  "Macanal - Santa Maria",                                 72.01,  89.81),
    (10, "Santa Maria - Cachipay - San Luis de Gaceno - Aguaclara", 89.81, 137.17),
]

# LOS LIMITES DE VERDAD SON PR, NO KILOMETROS, y el contrato lo dice: "las
# longitudes son aproximadas. El Concesionario sera responsable de ejecutar las
# obras correspondientes a la longitud efectiva de cada Unidad Funcional
# considerando los PR inicial y final identificados en las tablas anteriores"
# (Tabla 3, nota 1, pagina 6). Los kilometros de arriba son la suma acumulada de
# las longitudes por UF y sirven para repartir activos sinteticos; para situar un
# equipo de verdad se usa su PR con su ruta.
#
#   UF1  Sisga PR0+0+000 (55CN03)      -> Guateque PR4+885 (5608)    50,01 km
#   UF2  Guateque PR4+885 (5608)       -> Macanal PR26+879 (5608)    22,00 km
#   UF3  Macanal PR26+879 (5608)       -> Santa Maria PR44+680       17,80 km
#   UF4  Santa Maria PR44+680 (5608)   -> Aguaclara PR92+048 (5608)  47,36 km


def unidad_funcional(frac):
    """La UF en la que cae un punto, por su kilometro real del corredor."""
    km = frac * LARGO_KM
    for uid, _nombre, desde, hasta in UNIDADES:
        if desde <= km < hasta:
            return uid
    return UNIDADES[-1][0]


COLS = ["ActivoID", "CodigoActivo", "Nombre", "TipoActivoID", "UnidadFuncionalID",
        "PR", "CalzadaID", "Ubicacion", "EstadoActivoID", "CodigoQR", "SentidoID",
        "Activo", "FrecuenciaID", "Observaciones", "Criticidad", "FechaBaja", "MotivoBaja"]


def generar_filas(existentes=None):
    """Completa cada familia hasta la cantidad del Plan Maestro.

    `existentes` dice cuantos activos REALES hay ya de cada familia. Esos no se
    regeneran: se completa lo que falta y se numera a continuacion, para que la
    familia sume exactamente lo que dice el Plan Maestro y no haya dos codigos
    iguales. Sin argumento genera las familias enteras.

    El codigo va con el formato de operacion -SOS-001, con ceros- y no con el
    SOS_1 que se uso al principio, que era invencion nuestra. El de operacion
    ademas ordena bien en una hoja de calculo.

    Reproducible: misma semilla, mismo reparto, mismas coordenadas. El desfase
    por familia se deriva de las letras del prefijo porque hash() de una cadena
    va salado por proceso y reasignaba PR, unidad funcional y coordenada en cada
    ejecucion.
    """
    existentes = existentes or {}
    random.seed(20260809)
    filas = []
    n = 0
    for prefijo, nombre, cantidad, clave_tipo, frec in FAMILIAS:
        ya = existentes.get(prefijo, 0)
        for i in range(ya + 1, cantidad + 1):
            n += 1
            desfase = sum(ord(x) for x in prefijo) % 7 / 100.0
            frac = ((i - 0.5) / cantidad + desfase) % 1.0
            filas.append({
                "ActivoID": BASE_ID + n,
                "CodigoActivo": "%s-%03d" % (prefijo, i),
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
