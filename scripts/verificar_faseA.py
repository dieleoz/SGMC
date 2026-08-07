# -*- coding: utf-8 -*-
"""Verifica la Fase A contra un .xlsx exportado del Sheets de produccion.

Compara encabezado por encabezado contra el modelo objetivo. No compara contra
lo que alguien reporto: compara contra scripts/modelo_objetivo.py.

Uso:  python scripts/verificar_faseA.py "BD/Modelo de Datos (4).xlsx"
Salida: 0 si la Fase A esta cerrada, 1 si falta algo.

Por que existe
--------------
La Fase A la aplico un asistente distinto, a mano sobre la hoja, y se reporto
como cerrada al 100%. Este proyecto arrastra un historial de subsanaciones
reportadas como cerradas que no lo estaban, de modo que el reporte no cierra
nada: lo cierra el archivo.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from modelo_objetivo import (MODELO, RENOMBRADOS, RETIPADOS, CAMPOS_RETIRADOS,
                             CLAVE_LEGIBLE, CLAVE_GENERADA)

try:
    import openpyxl
except ImportError:
    print("Falta openpyxl."); sys.exit(2)

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ruta = sys.argv[1] if len(sys.argv) > 1 else os.path.join(RAIZ, "BD", "Modelo de Datos (4).xlsx")
if not os.path.isabs(ruta):
    ruta = os.path.join(RAIZ, ruta)

wb = openpyxl.load_workbook(ruta, read_only=True)

fallos, avisos, oks = [], [], []


def falla(codigo, msg):
    fallos.append("[%s] %s" % (codigo, msg))


def aviso(codigo, msg):
    avisos.append("[%s] %s" % (codigo, msg))


def encabezados(hoja):
    ws = wb[hoja]
    fila = next(ws.iter_rows(min_row=1, max_row=1))
    return [str(c.value).strip() for c in fila if c.value is not None]


def filas(hoja):
    ws = wb[hoja]
    return sum(1 for r in ws.iter_rows(min_row=2, values_only=True)
               if any(v not in (None, "") for v in r))


# ------------------------------------------------ F-01 los renombrados llegaron
for tabla, mapa in RENOMBRADOS.items():
    if tabla not in wb.sheetnames:
        falla("F-01", "%s no existe en el libro" % tabla)
        continue
    h = encabezados(tabla)
    for viejo, (nuevo, _m) in mapa.items():
        if nuevo not in h:
            falla("F-01", "%s.%s no existe. El renombrado desde '%s' no se aplico"
                  % (tabla, nuevo, viejo))
            continue
        oks.append("%s.%s" % (tabla, nuevo))
        # El nombre viejo solo puede sobrevivir si el modelo objetivo lo reutiliza
        # para otra cosa. Es el caso de OT_OrdenesTrabajo.Activo, que pasa de ser
        # el vinculo al activo a ser la bandera Yes/No.
        if viejo in h:
            reutilizado = any(c["nombre"] == viejo for c in MODELO[tabla]["columnas"])
            if reutilizado:
                aviso("F-01", "%s.%s sigue existiendo, pero el modelo lo reutiliza como "
                              "columna propia. Correcto, no es un fallo" % (tabla, viejo))
            else:
                falla("F-01", "%s.%s sigue con el nombre viejo" % (tabla, viejo))

# --------------------------------------- F-02 toda columna del modelo esta o no
RETIRADAS_OK = {t: set(c) for t, c in CAMPOS_RETIRADOS.items()}
for tabla, d in MODELO.items():
    if tabla not in wb.sheetnames:
        falla("F-02", "%s no existe en el libro" % tabla)
        continue
    h = set(encabezados(tabla))
    faltan = [c["nombre"] for c in d["columnas"] if c["nombre"] not in h]
    if faltan:
        falla("F-02", "%s: faltan %d columnas del modelo: %s"
              % (tabla, len(faltan), ", ".join(faltan)))

# ------------------------------------ F-03 lo retirado sigue ahi, y esta bien
for tabla, campos in CAMPOS_RETIRADOS.items():
    if tabla not in wb.sheetnames:
        continue
    h = set(encabezados(tabla))
    vivos = [c for c in campos if c in h]
    if vivos:
        aviso("F-03", "%s conserva %d columnas marcadas como retiradas: %s. "
                      "Es lo esperado: la Fase A no borra nada"
              % (tabla, len(vivos), ", ".join(vivos)))

# --------------------------------------------- F-04 lo retipado sigue pendiente
n_retipar = sum(len(m) for m in RETIPADOS.values())
aviso("F-04", "%d columnas siguen pendientes de retipar a Ref. Es trabajo de la "
              "Fase B, en el editor de AppSheet, no de la hoja" % n_retipar)

# ------------------------------------------------------ F-05 limpieza del CHK
if "CHK_Checklists" in wb.sheetnames:
    ws = wb["CHK_Checklists"]
    ids = [str(r[0]).strip() for r in ws.iter_rows(min_row=2, values_only=True)
           if r and r[0] not in (None, "")]
    # d02d8a3d se retira de la lista de conservadas y pasa a la de borradas: ESPEC-001C
    # ordeno eliminarla porque su MantenimientoID guardaba 'OT-0001', que es una ORDEN.
    # No basta con dejar de exigir que exista; hay que exigir que NO exista.
    for basura in ("CHK001", "0356e6d7", "d02d8a3d"):
        if basura in ids:
            falla("F-05", "CHK_Checklists: '%s' sigue ahi. Debia borrarse" % basura)
    if not any(b in ids for b in ("CHK001", "0356e6d7", "d02d8a3d")):
        oks.append("CHK_Checklists: las tres filas de ensayo estan borradas")

# ---------------------------------------------- F-06 catalogos nuevos poblados
POBLACION_MINIMA = {
    "UNF_UnidadesFuncionales": (4, "las cuatro unidades funcionales, con claves 7 a 10"),
    "EOT_EstadosOrden": (7, "los siete estados del ciclo de vida"),
    "MOT_MotivosPendiente": (5, "los cinco motivos del supuesto D-07"),
    "ASG_AsignacionZona": (1, "al menos una asignacion, o el Security Filter deja a "
                              "cada tecnico en cero activos"),
}
for tabla, (minimo, para_que) in POBLACION_MINIMA.items():
    if tabla not in wb.sheetnames:
        falla("F-06", "%s no existe" % tabla)
        continue
    n = filas(tabla)
    if n < minimo:
        falla("F-06", "%s tiene %d filas y necesita al menos %d: %s"
              % (tabla, n, minimo, para_que))
    else:
        oks.append("%s poblada con %d filas" % (tabla, n))

# -------------------------------------- F-07 las claves de UNF son las de ACT
if "UNF_UnidadesFuncionales" in wb.sheetnames and "ACT_Activos" in wb.sheetnames:
    ws = wb["UNF_UnidadesFuncionales"]
    claves = {str(r[0]).strip() for r in ws.iter_rows(min_row=2, values_only=True)
              if r and r[0] not in (None, "")}
    h = encabezados("ACT_Activos")
    if "UnidadFuncionalID" in h:
        i = h.index("UnidadFuncionalID")
        ws2 = wb["ACT_Activos"]
        usados = {str(r[i]).strip() for r in ws2.iter_rows(min_row=2, values_only=True)
                  if r and len(r) > i and r[i] not in (None, "")}
        huerfanos = usados - claves
        if huerfanos:
            falla("F-07", "ACT_Activos.UnidadFuncionalID usa %s, que no existe en "
                          "UNF_UnidadesFuncionales. La conversion a Ref dejaria esas "
                          "filas huerfanas" % sorted(huerfanos))
        else:
            oks.append("Las %d unidades funcionales distintas usadas por ACT_Activos resuelven "
                       "contra UNF" % len(usados))

# ------------------------------- F-08 los estados de la orden resuelven contra EOT
if "EOT_EstadosOrden" in wb.sheetnames and "OT_OrdenesTrabajo" in wb.sheetnames:
    ws = wb["EOT_EstadosOrden"]
    claves = {str(r[0]).strip() for r in ws.iter_rows(min_row=2, values_only=True)
              if r and r[0] not in (None, "")}
    h = encabezados("OT_OrdenesTrabajo")
    if "EstadoOrdenID" in h:
        i = h.index("EstadoOrdenID")
        ws2 = wb["OT_OrdenesTrabajo"]
        usados = {str(r[i]).strip() for r in ws2.iter_rows(min_row=2, values_only=True)
                  if r and len(r) > i and r[i] not in (None, "")}
        huerfanos = usados - claves
        if huerfanos:
            falla("F-08", "OT_OrdenesTrabajo.EstadoOrdenID usa %s, que no existe en "
                          "EOT_EstadosOrden" % sorted(huerfanos))
        else:
            oks.append("Los %d estados distintos usados por las ordenes resuelven contra "
                       "EOT_EstadosOrden" % len(usados))

# ------------------------- F-09 la asignacion de zona resuelve por los dos lados
def _claves(hoja, col=0):
    ws = wb[hoja]
    return {str(r[col]).strip().replace(".0", "") for r in ws.iter_rows(min_row=2, values_only=True)
            if r and r[col] not in (None, "")}


def _usados(hoja, columna):
    h = encabezados(hoja)
    if columna not in h:
        return None
    i = h.index(columna)
    ws = wb[hoja]
    return {str(r[i]).strip().replace(".0", "") for r in ws.iter_rows(min_row=2, values_only=True)
            if r and len(r) > i and r[i] not in (None, "")}


if "ASG_AsignacionZona" in wb.sheetnames:
    for columna, destino in (("UsuarioID", "USR_Usuarios"),
                             ("UnidadFuncionalID", "UNF_UnidadesFuncionales")):
        usados = _usados("ASG_AsignacionZona", columna)
        if usados is None:
            falla("F-09", "ASG_AsignacionZona.%s no existe" % columna)
            continue
        huerfanos = usados - _claves(destino)
        if huerfanos:
            falla("F-09", "ASG_AsignacionZona.%s usa %s, que no existe en %s. El Security Filter "
                          "devolveria cero activos para esos usuarios"
                  % (columna, sorted(huerfanos), destino))
        else:
            oks.append("ASG_AsignacionZona.%s resuelve contra %s" % (columna, destino))

# ---------------------- F-10 los hijos resuelven contra sus padres
# El fallo que esta comprobacion habria atrapado: CHK_Checklists.OTID se renombro
# a MantenimientoID y su fila siguio guardando 'OT-0001', que es una ORDEN.
# Renombrar un encabezado no cambia lo que el dato significa.
CADENA = [
    ("CHK_Checklists", "MantenimientoID", "MAN_Mantenimientos"),
    ("CHD_ChecklistDetalle", "ChecklistID", "CHK_Checklists"),
    ("FOT_Fotografias", "MantenimientoID", "MAN_Mantenimientos"),
    ("FIR_Firmas", "MantenimientoID", "MAN_Mantenimientos"),
    ("MAN_Mantenimientos", "OTID", "OT_OrdenesTrabajo"),
    ("OT_OrdenesTrabajo", "ActivoID", "ACT_Activos"),
    ("LST_ValoresLista", "PreguntaID", "FRM_Preguntas"),
]
for tabla, columna, destino in CADENA:
    if tabla not in wb.sheetnames or destino not in wb.sheetnames:
        continue
    usados = _usados(tabla, columna)
    if usados is None:
        falla("F-10", "%s.%s no existe" % (tabla, columna))
        continue
    if not usados:
        continue                      # tabla vacia: nada que resolver todavia
    huerfanos = usados - _claves(destino)
    if huerfanos:
        falla("F-10", "%s.%s guarda %s, que no existe en %s. Al convertir a Ref esas filas "
                      "quedan huerfanas y AppSheet no lo anuncia"
              % (tabla, columna, sorted(huerfanos)[:5], destino))
    else:
        oks.append("%s.%s resuelve contra %s (%d valores)"
                   % (tabla, columna, destino, len(usados)))

# ------------- F-11 las listas de claves dicen la verdad sobre la hoja
# CLAVE_LEGIBLE decide cuando V-17 permite comparar un Ref contra un literal.
# Si la lista y la hoja divergen, V-17 miente en una de las dos direcciones: o
# bloquea trabajo correcto, o deja pasar el defecto que existe para cazar.
#
# La comprobacion es ASIMETRICA a proposito:
#   - FALLO si una tabla FUERA de CLAVE_LEGIBLE tiene clave de texto legible.
#     Ese es el caso que bloquea trabajo correcto.
#   - AVISO si una tabla DENTRO la tiene numerica. Molesta, no rompe.
#   - CLAVE_GENERADA queda exenta de las dos: sus valores parecen legibles hoy
#     solo por el fixture de la Fase A, y seran aleatorios en cuanto la
#     aplicacion cree la primera fila.
def _clave_es_legible(hoja):
    ws = wb[hoja]
    for r in ws.iter_rows(min_row=2, values_only=True):
        if r and r[0] not in (None, ""):
            v = r[0]
            return isinstance(v, str) and not v.replace(".", "").replace("-", "").isdigit()
    return None                      # tabla vacia: no se puede decidir


for tabla in MODELO:
    if tabla not in wb.sheetnames or tabla in CLAVE_GENERADA:
        continue
    legible = _clave_es_legible(tabla)
    if legible is None:
        continue
    if legible and tabla not in CLAVE_LEGIBLE:
        falla("F-11", "%s tiene clave de texto legible en la hoja y NO esta en CLAVE_LEGIBLE. "
                      "V-17 bloqueara una comparacion correcta contra ella" % tabla)
    elif not legible and tabla in CLAVE_LEGIBLE:
        aviso("F-11", "%s esta en CLAVE_LEGIBLE pero su clave en la hoja es numerica. "
                      "Sacala, o V-17 dejara pasar un defecto real" % tabla)
    elif legible:
        oks.append("%s: clave legible, coherente con CLAVE_LEGIBLE" % tabla)

for tabla in CLAVE_GENERADA:
    if tabla in wb.sheetnames and tabla in CLAVE_LEGIBLE:
        falla("F-11", "%s esta en CLAVE_GENERADA y tambien en CLAVE_LEGIBLE. Su clave sera "
                      "aleatoria en cuanto la app cree una fila: no puede estar en las dos" % tabla)

# ------------------------------------------------------------------- informe
print("=" * 78)
print("VERIFICACION DE LA FASE A")
print("=" * 78)
print("Archivo: %s" % os.path.basename(ruta))
print("Hojas:   %d" % len(wb.sheetnames))
print("-" * 78)
if oks:
    print("CONFORMES (%d):" % len(oks))
    for o in oks:
        print("  ok", o)
    print()
if fallos:
    print("FALLOS (%d) — la Fase A NO esta cerrada:" % len(fallos))
    for f in fallos:
        print("  x", f)
    print()
if avisos:
    print("AVISOS (%d) — esperados, no bloquean:" % len(avisos))
    for a in avisos:
        print("  -", a)
    print()
print("=" * 78)
print("FASE A CERRADA" if not fallos else "FASE A INCOMPLETA: faltan %d puntos" % len(fallos))
sys.exit(1 if fallos else 0)
