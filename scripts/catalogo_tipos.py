# -*- coding: utf-8 -*-
"""El catalogo de tipos de activo y las familias del Plan Maestro, en un sitio.

Por que existe
--------------
Habia dos taxonomias distintas y nadie lo habia escrito:

  - TIP_TiposActivo, con 18 tipos, que es lo que la aplicacion usa para decidir
    QUE CHECKLIST ve el tecnico.
  - Las 18 familias del Plan Maestro, que es como operacion cuenta los equipos.

No son la misma lista. Nueve familias no tenian tipo propio y se colgaban del
tipo de otra cosa: la impresora heredaba el checklist del NAS, el portatil el
del servidor, el carril de peaje el de la bascula. Eran 78 activos de 355
—el 22%— con el checklist equivocado, y como TipoActivoID resolvia contra una
fila que existe, ningun verificador lo veia.

El catalogo pasa a 27 tipos: los 18 de siempre mas los 9 que faltaban. Ahora
cada familia del Plan Maestro tiene tipo propio, checklist propio y radio de
geofencing propio.

Quien lo lee
------------
  scripts/generar_plantilla.py   construye TIP_TiposActivo y FRM_Formularios
  scripts/generar_inventario.py  asigna TipoActivoID a cada uno de los 355

Cambiar el reparto aqui lo cambia en los dos. Antes estaba escrito a mano en
generar_inventario.py y solo alli.
"""

# (id, clave, nombre, categoria, tiene_qr, requiere_gps, formulario, radio_km)
#
# El radio es la distancia maxima al activo para poder cerrar una orden, y la
# lee RG-01. Tres valores, por como es el equipo en el terreno:
#
#   0,05 km  equipo puntual: se esta delante de el o no se esta
#   0,1  km  instalacion con recinto: peaje, bascula, subestacion, portico
#   1,5  km  la fibra, que es lineal y no tiene un "delante"
#
# Un radio en blanco NO es neutro: RG-01 compara contra vacio y rechaza tambien
# el cierre legitimo. Por eso los 27 lo llevan.
TIPOS_ACTIVO = [
    ( 1, "SOS",       "SOS",                   "ITS",            True,  True,  "FRM_SOS",  0.05),
    ( 2, "CCTV",      "CCTV",                  "ITS",            True,  True,  "FRM_CCTV", 0.05),
    ( 3, "PMVF",      "PMVF",                  "ITS",            True,  True,  "FRM_PMVF", 0.1),
    ( 4, "PMVM",      "PMVM",                  "ITS",            True,  True,  "FRM_PMVM", 0.1),
    ( 5, "SGM",       "SGM",                   "ITS",            True,  True,  "FRM_SGM",  0.05),
    ( 6, "SGE",       "SGE",                   "ITS",            True,  True,  "FRM_SGE",  0.05),
    ( 7, "SSA",       "SSA",                   "ITS",            True,  True,  "FRM_SSA",  0.05),
    ( 8, "GENERADOR", "GENERADOR",             "Eléctrico",      True,  True,  "FRM_GENE", 0.1),
    ( 9, "BASCULA",   "BASCULA",               "ITS",            True,  True,  "FRM_BASC", 0.1),
    (10, "FO",        "FO",                    "Comunicaciones", True,  True,  "FRM_FO",   1.5),
    (11, "VW",        "VW",                    "TI",             True,  True,  "FRM_VW",   0.05),
    (12, "SWITCH",    "SWITCH",                "TI",             True,  True,  "FRM_SWIT", 0.05),
    (13, "ROUTER",    "ROUTER",                "TI",             True,  True,  "FRM_ROUT", 0.05),
    (14, "FIREWALL",  "FIREWALL",              "TI",             True,  True,  "FRM_FIRE", 0.05),
    (15, "UPS",       "UPS",                   "Eléctrico",      True,  True,  "FRM_UPS",  0.05),
    (16, "SERVIDOR",  "SERVIDOR",              "TI",             True,  False, "FRM_SERV", 0.05),
    (17, "NAS",       "NAS",                   "TI",             True,  False, "FRM_NAS",  0.05),
    (18, "SUBESTA",   "SUBESTACIÓN",           "Eléctrico",      True,  True,  "FRM_SUBE", 0.1),
    # --- los nueve que faltaban, anadidos el 2026-08-09 -----------------------
    (19, "BASD",      "BASCULA DINAMICA",      "ITS",            True,  True,  "FRM_BASD", 0.1),
    (20, "PJC",       "PEAJE CARRIL",          "ITS",            True,  True,  "FRM_PJC",  0.1),
    (21, "PJE",       "PEAJE ELECTRONICA",     "ITS",            True,  True,  "FRM_PJE",  0.1),
    (22, "ETD",       "ESTACION TOMA DATOS",   "ITS",            True,  True,  "FRM_ETD",  0.05),
    (23, "PSEG",      "PASO SEGURO",           "ITS",            True,  True,  "FRM_PSEG", 0.05),
    (24, "SWL3",      "SWITCH CAPA 3",         "TI",             True,  True,  "FRM_SWL3", 0.05),
    (25, "PORT",      "COMPUTADOR PORTATIL",   "TI",             True,  False, "FRM_PORT", 0.05),
    (26, "IMPR",      "IMPRESORA",             "TI",             True,  False, "FRM_IMPR", 0.05),
    (27, "OCR",       "CAMARA OCR PESAJE",     "ITS",            True,  True,  "FRM_OCR",  0.05),
    ]

# Las 18 familias del Plan Maestro que se cuentan por unidades. Suman 355.
#
# (prefijo, nombre, cantidad, clave_de_tipo, frecuencia)
#
# La frecuencia sale de la columna PERIODICIDAD del Plan Maestro, contra
# FRE_Frecuencias: 4=Mensual 5=Bimensual 6=Trimestral 7=Semestral 8=Anual.
# PORT va sin frecuencia: su periodicidad es "A demanda", que no es una.
FAMILIAS = [
    ("SOS",  "S.O.S (Postes de Auxilio)",  54, "SOS",      4),
    ("CCTV", "Camara CCTV",                26, "CCTV",     6),
    ("PMVF", "PMV Fijo (Portico)",         11, "PMVF",     5),
    ("PMVM", "PMV Movil (Remolque)",       19, "PMVM",     4),
    ("SGE",  "Galibo Electronico",          4, "SGE",      6),
    ("SGM",  "Galibo Mecanico",             4, "SGM",      7),
    ("SSA",  "Sensor Ambiental",            4, "SSA",      7),
    ("ETD",  "Estacion Toma Datos",         4, "ETD",      7),
    ("PSEG", "Paso Seguro",                16, "PSEG",     6),
    ("SWL3", "Switch Capa 3",               4, "SWL3",     6),
    ("SWIT", "Switch Capa 2",             142, "SWITCH",   7),
    ("PJC",  "Peaje Carril",               12, "PJC",      4),
    ("PJE",  "Peaje Electronica",          12, "PJE",      4),
    ("SERV", "Servidor",                    7, "SERVIDOR", 4),
    ("BASC", "Bascula Dinamica",            2, "BASD",     7),
    ("OCR",  "Camara OCR Pesaje",           2, "OCR",      4),
    ("PORT", "Computador Portatil",        29, "PORT",     ""),
    ("IMPR", "Impresora",                   3, "IMPR",     4),
    ]

# clave -> id, para que las familias no repitan numeros a mano
ID_POR_CLAVE = {t[1]: t[0] for t in TIPOS_ACTIVO}

TOTAL_SINTETICOS = sum(f[2] for f in FAMILIAS)


def tipo_de_familia(clave):
    """El TipoActivoID de una familia del Plan Maestro."""
    if clave not in ID_POR_CLAVE:
        raise KeyError("La familia apunta al tipo '%s', que no esta en TIPOS_ACTIVO" % clave)
    return ID_POR_CLAVE[clave]


def comprobar():
    """Invariantes del catalogo. Las llama validar_modelo.py."""
    fallos = []

    ids = [t[0] for t in TIPOS_ACTIVO]
    if len(set(ids)) != len(ids):
        fallos.append("Hay TipoActivoID repetidos en TIPOS_ACTIVO")
    if ids != list(range(1, len(ids) + 1)):
        fallos.append("Los TipoActivoID no son 1..%d correlativos" % len(ids))

    claves = [t[1] for t in TIPOS_ACTIVO]
    if len(set(claves)) != len(claves):
        fallos.append("Hay claves repetidas en TIPOS_ACTIVO")

    formularios = [t[6] for t in TIPOS_ACTIVO]
    if len(set(formularios)) != len(formularios):
        fallos.append("Dos tipos comparten FormularioID: compartirian checklist")

    for t in TIPOS_ACTIVO:
        if t[7] in (None, ""):
            fallos.append("%s no tiene radio. RG-01 comparia contra vacio y "
                          "rechazaria tambien el cierre legitimo" % t[2])

    for prefijo, _, _, clave, _ in FAMILIAS:
        if clave not in ID_POR_CLAVE:
            fallos.append("La familia %s apunta al tipo '%s', que no existe" % (prefijo, clave))

    usados = set(f[3] for f in FAMILIAS)
    if len(usados) != len(FAMILIAS):
        fallos.append("Dos familias del Plan Maestro comparten tipo: una de las "
                      "dos veria el checklist de la otra")

    if TOTAL_SINTETICOS != 355:
        fallos.append("Las familias suman %d, no los 355 del Plan Maestro" % TOTAL_SINTETICOS)

    return fallos


if __name__ == "__main__":
    fallos = comprobar()
    print("Tipos de activo: %d   ·   Familias del Plan Maestro: %d   ·   Activos: %d"
          % (len(TIPOS_ACTIVO), len(FAMILIAS), TOTAL_SINTETICOS))
    print()
    print("%-6s %-24s %-16s %8s  %s" % ("ID", "TIPO", "FAMILIA", "RADIO", "FORMULARIO"))
    familia_de = {f[3]: f[0] for f in FAMILIAS}
    for t in TIPOS_ACTIVO:
        print("%-6d %-24s %-16s %8s  %s"
              % (t[0], t[2], familia_de.get(t[1], "—"), t[7], t[6]))
    print()
    if fallos:
        for f in fallos:
            print("  x", f)
        raise SystemExit(1)
    print("Catalogo coherente.")
