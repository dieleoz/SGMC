# -*- coding: utf-8 -*-
"""Genera BD/Modelo_Datos_PLANTILLA.xlsx entero, en un comando.

Es EL ENTREGABLE. El funcional recibe este archivo, lo completa con el dato
real y desde ahi sigue las guias. Por eso tiene que salir generado y limpio:
28 pestanas con exactamente las columnas que el modelo declara, sin las 47 que
la hoja heredada arrastraba.

Por que existe
--------------
La plantilla se armaba con dos scripts y varios pasos a mano. generar_hoja_limpia
daba la estructura, generar_inventario daba los 355, y unirlos, anadir _LEEME y
poblar el radio no estaba escrito en ningun sitio. Eso la convertia en un
artefacto que se conserva en vez de generarse -justo lo que este proyecto
decidio no volver a tener- y arrastraba dos defectos que nadie podia ver:

  - TIP_TiposActivo con 18 tipos contra 18 familias del Plan Maestro que NO son
    la misma lista. 78 activos con el checklist de otro equipo.
  - RadioGeofencingKm vacio, que hace que RG-01 compare contra blanco.

Que hace
--------
  1. Crea las 28 pestanas con las columnas de MODELO, en su orden.
  2. Migra los datos del libro origen emparejando por NOMBRE de columna.
     Lo que el modelo no declara, no viaja.
  3. Rehace TIP_TiposActivo desde catalogo_tipos: 27 tipos con su radio.
  4. Completa FRM_Formularios con los formularios que falten, uno por tipo.
  5. Anade los 355 activos sinteticos detras de los 34 del fixture.
  6. Pone _LEEME delante, que es lo unico que el funcional lee sin que se lo
     expliquen.

Uso:  python scripts/generar_plantilla.py ["BD/<origen>.xlsx"]
"""
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "scripts"))

from modelo_objetivo import MODELO
from catalogo_tipos import TIPOS_ACTIVO, FAMILIAS, comprobar
from generar_inventario import generar_filas

try:
    import openpyxl
    from openpyxl.styles import Font
except ImportError:
    print("Falta openpyxl."); sys.exit(2)

ORIGEN = sys.argv[1] if len(sys.argv) > 1 else "BD/Modelo_Datos_09082026.xlsx"
if not os.path.isabs(ORIGEN):
    ORIGEN = os.path.join(RAIZ, ORIGEN)
SALIDA = os.path.join(RAIZ, "BD", "Modelo_Datos_PLANTILLA.xlsx")

# El catalogo se comprueba ANTES de escribir nada. Si dos familias comparten
# tipo, la plantilla saldria con activos viendo el checklist de otro equipo, y
# eso no lo detecta ningun verificador posterior: la referencia resuelve.
fallos = comprobar()
if fallos:
    print("El catalogo de tipos no es coherente. No se genera nada:")
    for f in fallos:
        print("   x", f)
    sys.exit(1)


def texto(v):
    return "" if v is None else str(v).strip()


# ----------------------------------------------------------------- 1. estructura
src = openpyxl.load_workbook(ORIGEN, data_only=True, read_only=True)
dst = openpyxl.Workbook()
dst.remove(dst.active)

resumen = []
descartadas = []

for tabla in MODELO:
    cols = [c["nombre"] for c in MODELO[tabla]["columnas"]]
    ws = dst.create_sheet(tabla)
    ws.append(cols)

    if tabla not in src.sheetnames:
        resumen.append((tabla, len(cols), 0, "pestana nueva, sin datos de origen"))
        continue

    o = src[tabla]
    cab = [texto(c.value) for c in next(o.iter_rows(min_row=1, max_row=1))]
    idx = {n: i for i, n in enumerate(cab) if n}

    fuera = [n for n in cab if n and n not in cols]
    if fuera:
        descartadas.append((tabla, fuera))

    n = 0
    for r in o.iter_rows(min_row=2, values_only=True):
        if not r or all(v in (None, "") for v in r):
            continue
        fila = [r[idx[c]] if c in idx and idx[c] < len(r) else None for c in cols]
        if all(v in (None, "") for v in fila):
            continue
        ws.append(fila)
        n += 1
    resumen.append((tabla, len(cols), n, ""))

resumen = {t: [c, f, nota] for t, c, f, nota in resumen}


def columnas(tabla):
    return [c["nombre"] for c in MODELO[tabla]["columnas"]]


def escribir(tabla, filas_dict):
    """Reescribe una pestana entera desde diccionarios columna -> valor."""
    ws = dst[tabla]
    cols = columnas(tabla)
    ws.delete_rows(2, ws.max_row)
    for f in filas_dict:
        ws.append([f.get(c, "") for c in cols])
    resumen[tabla][1] = len(filas_dict)


def leer(tabla):
    """Las filas de una pestana ya construida, como diccionarios."""
    ws = dst[tabla]
    cols = columnas(tabla)
    out = []
    for r in ws.iter_rows(min_row=2, values_only=True):
        if r is None or all(v in (None, "") for v in r):
            continue
        out.append({c: (r[i] if i < len(r) else None) for i, c in enumerate(cols)})
    return out


# --------------------------------------------- 2. TIP_TiposActivo, desde el catalogo
#
# Se rehace entera, no se parchea. Los 18 que venian de la hoja traian el radio
# vacio en los 18 y el nombre de la subestacion con la tilde rota.
tipos = []
for tid, _clave, nombre, categoria, qr, gps, formulario, radio in TIPOS_ACTIVO:
    tipos.append({
        "TipoActivoID": tid,
        "Nombre": nombre,
        "Categoria": categoria,
        "FormularioID": formulario,
        "TieneQR": "TRUE" if qr else "FALSE",
        "RequiereGPS": "TRUE" if gps else "FALSE",
        "RadioGeofencingKm": radio,
        "Activo": "TRUE",
    })
escribir("TIP_TiposActivo", tipos)

# ------------------------------------------- 3. FRM_Formularios, uno por tipo
#
# Los existentes se conservan tal cual: su columna Version la leen los
# checklists ya creados (RG-09), y reescribirla dejaria el historico apuntando
# a una version de formulario que nunca existio. Solo se anaden los que faltan.
formularios = leer("FRM_Formularios")
existentes = {texto(f["FormularioID"]) for f in formularios}
anadidos = []
for tid, _clave, nombre, _cat, _qr, _gps, formulario, _radio in TIPOS_ACTIVO:
    if formulario in existentes:
        continue
    formularios.append({
        "FormularioID": formulario,
        "Nombre": "Checklist %s" % nombre,
        "Descripcion": "Checklist mantenimiento preventivo %s" % nombre,
        "Version": 1,
        "Activo": "TRUE",
    })
    anadidos.append(formulario)
escribir("FRM_Formularios", formularios)

# ------------------------------------------------- 4. los 355 detras del fixture
#
# Los sinteticos arrancan en ActivoID 1000 para no pisar los 34 del fixture, a
# los que apuntan las seis ordenes existentes.
activos = leer("ACT_Activos")
fixture = len(activos)
for f in generar_filas():
    activos.append({c: f.get(c, "") for c in columnas("ACT_Activos")})
escribir("ACT_Activos", activos)

# ------------------------------------------------------------------ 5. _LEEME
#
# Va delante porque es lo unico que el funcional lee sin que se lo expliquen.
sin_preguntas = sorted({texto(f["FormularioID"]) for f in formularios}
                       - {texto(p["FormularioID"]) for p in leer("FRM_Preguntas")})

LEEME = [
    ("PLANTILLA DE DATOS - SGMC", True),
    ("", False),
    ("%d pestanas con la estructura exacta que espera la aplicacion." % len(MODELO), False),
    ("NO anada ni quite columnas: la aplicacion las lee por nombre.", False),
    ("", False),
    ("NINGUNA COORDENADA DE ESTE ARCHIVO ES REAL", True),
    ("Las %d primeras filas de ACT_Activos son el fixture de pruebas: todas comparten" % fixture, False),
    ("una coordenada que esta en Bogota, no en el corredor.", False),
    ("Las %d siguientes son generadas: estan sobre el corredor pero son inventadas." % (len(activos) - fixture), False),
    ("Las %d lo dicen en su columna Observaciones." % len(activos), False),
    ("", False),
    ("LO QUE HAY QUE COMPLETAR", True),
    ("", False),
    ("PESTANA | COLUMNA | QUE PONER", False),
    ("ACT_Activos | Ubicacion | COORDENADA REAL, formato  4.812345, -73.201234", False),
    ("    SIN ESTO NINGUN TECNICO PUEDE CERRAR UNA ORDEN EN VIA", False),
    ("ACT_Activos | PR | Punto de referencia INVIAS real, formato  12+400", False),
    ("ACT_Activos | CodigoActivo | El codigo con el que operacion conoce el equipo", False),
    ("ACT_Activos | Criticidad | Alta / Media / Baja. Vacia en las %d" % len(activos), False),
    ("FRM_Preguntas | todas | Las preguntas de cada checklist.", False),
    ("    HOY SOLO EXISTEN LAS 15 DE FRM_SOS: %d formularios vacios." % len(sin_preguntas), False),
    ("USR_Usuarios | Correo | EXACTAMENTE la cuenta con la que inicia sesion", False),
    ("ASG_AsignacionZona | todas | Que unidad funcional atiende cada tecnico.", False),
    ("    Sin fila, ese tecnico no ve ningun activo.", False),
    ("UNF_UnidadesFuncionales | PRInicial/Final | Vacias. El filtro por zona no tiene tramo del que colgar", False),
    ("", False),
    ("LO QUE NO HAY QUE TOCAR", True),
    ("", False),
    ("Nombres de pestanas y de columnas.", False),
    ("Las columnas de identificador: relacionan las tablas entre si.", False),
    ("Las pestanas de catalogo: ya estan completas.", False),
    ("TIP_TiposActivo.RadioGeofencingKm: es la distancia para poder cerrar, por tipo.", False),
    ("    Dejarla en blanco hace que se rechace TAMBIEN el cierre legitimo.", False),
    ("", False),
    ("COMO ESTAN LOS DATOS HOY", True),
    ("", False),
    ("ACT_Activos | %d filas | %d del fixture + %d generados del Plan Maestro"
     % (len(activos), fixture, len(activos) - fixture), False),
    ("    Codigos SOS_1..SOS_54, CCTV_1..CCTV_26, SWIT_1..SWIT_142", False),
    ("    Frecuencia de mantenimiento: la del Plan Maestro, por tipo", False),
    ("TIP_TiposActivo | %d filas | Un tipo por checklist, con su radio de cierre"
     % len(TIPOS_ACTIVO), False),
    ("    Eran %d, y %d de las %d familias del Plan Maestro colgaban del tipo de otra cosa:"
     % (len(TIPOS_ACTIVO) - len(anadidos), len(anadidos), len(FAMILIAS)), False),
    ("    la impresora veia el checklist del NAS y el portatil el del servidor.", False),
    ("FRM_Formularios | %d filas | Uno por tipo. %d se anadieron con el catalogo"
     % (len(formularios), len(anadidos)), False),
    ("USR_Usuarios | %d filas" % len(leer("USR_Usuarios")), False),
    ("OT_OrdenesTrabajo | %d filas | De prueba" % len(leer("OT_OrdenesTrabajo")), False),
    ("", False),
    ("Documentacion: repositorio del proyecto, empezando por ESTADO.md", False),
]

# --------------------------------------- 6. claves y referencias, todas a texto
#
# El modelo declara las claves como Text y las referencias apuntan a ellas. La
# hoja heredada guardaba el fixture como texto -'1'- y los generados salian como
# numero -1001-, asi que ACT_Activos.ActivoID mezclaba los dos tipos.
#
# AppSheet compara el valor de la referencia con el de la clave. Con la clave
# mezclada la comparacion depende de como llegue cada fila, y el sintoma es una
# referencia que a veces resuelve y a veces no, sin error. Aqui se decide una
# vez, derivado del modelo: si es clave o es Ref, viaja como texto.
def a_texto(v):
    if v is None or v == "":
        return v
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    if isinstance(v, int):
        return str(v)
    return v


normalizadas = 0
for tabla in MODELO:
    cols = columnas(tabla)
    objetivo = [i for i, c in enumerate(MODELO[tabla]["columnas"])
                if c.get("pk") or c.get("tipo") == "Ref"]
    if not objetivo:
        continue
    ws = dst[tabla]
    for fila in ws.iter_rows(min_row=2):
        for i in objetivo:
            nuevo = a_texto(fila[i].value)
            if nuevo is not fila[i].value:
                fila[i].value = nuevo
                normalizadas += 1

hoja = dst.create_sheet("_LEEME", 0)
for texto_fila, negrita in LEEME:
    hoja.append([texto_fila])
    if negrita:
        hoja.cell(row=hoja.max_row, column=1).font = Font(bold=True)
hoja.column_dimensions["A"].width = 95

dst.save(SALIDA)

# ------------------------------------------------------------------- informe
print("Generado:", SALIDA)
print("Origen:  ", os.path.basename(ORIGEN))
print()
print("%-26s %6s %8s  %s" % ("TABLA", "COLS", "FILAS", ""))
for t in sorted(resumen):
    c, f, nota = resumen[t]
    print("%-26s %6d %8d  %s" % (t, c, f, nota))
print()
print("Pestanas: %d + _LEEME   ·   Columnas: %d   ·   Filas: %d"
      % (len(resumen), sum(v[0] for v in resumen.values()),
         sum(v[1] for v in resumen.values())))
print()
print("Claves y referencias normalizadas a texto: %d" % normalizadas)
print()
print("Tipos de activo: %d   ·   Formularios anadidos: %d   ·   Activos: %d (%d fixture + %d generados)"
      % (len(TIPOS_ACTIVO), len(anadidos), len(activos), fixture, len(activos) - fixture))
if anadidos:
    print("   ", " · ".join(anadidos))
print()
if descartadas:
    total = sum(len(f) for _, f in descartadas)
    print("=== %d columnas del origen que NO viajan (el modelo no las declara) ===" % total)
    for t, fuera in sorted(descartadas):
        print("  %-24s %s" % (t, " · ".join(sorted(fuera))))
print()
print("Comprueba con:  python scripts/verificar_faseA.py \"BD/Modelo_Datos_PLANTILLA.xlsx\"")
