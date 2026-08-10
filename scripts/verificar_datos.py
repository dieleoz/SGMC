# -*- coding: utf-8 -*-
"""Comprueba que los DATOS de la hoja sostienen lo que el modelo declara.

El sexto verificador, y nace del unico hueco que los otros cinco compartian:
NINGUNO ABRE EL ARCHIVO DE DATOS PARA MIRAR SI LAS COLUMNAS ESTAN POBLADAS.

  validar_modelo        valida la declaracion. No importa openpyxl siquiera
  verificar_faseA       mira la hoja, pero comprueba estructura y tipos
  verificar_documentos  compara la prosa con el modelo
  verificar_enlaces     resuelve enlaces
  verificar_reproducible  compara dos pasadas del generador entre si

Que se colo por ese hueco
-------------------------
El 2026-08-10, ocho cambios pasaron los cinco en verde y tres eran defectuosos:

  - Ubicacion_LatLong quedo vacia en las 368 filas siendo obligatoria, y es la
    columna que RG-01 desreferencia para el geofencing. DISTANCE() contra
    blanco no da error: da un valor que rechaza el cierre legitimo.
  - SED_Sedes.UnidadFuncionalID quedo vacia en 5 de 6 siendo obligatoria, y
    RG-21 la compara. La regla volvia la fila imposible de guardar.
  - ACT_Activos.SedeID nacio vacia en las 368, asi que el cambio que la
    introdujo no lo ejercita ni una fila.

Los tres son el mismo fallo: **estructura entregada sin poblacion**. Y los tres
son invisibles para un verificador que solo lea declaraciones.

La otra mitad
-------------
Una Ref que resuelve puede apuntar a lo que no es (R-04), pero una Ref que NO
resuelve es directamente una fila que la aplicacion descarta sin avisar. Eso
tampoco lo miraba nadie: verificar_app compara el NUMERO de filas, no su
contenido.

Uso:  python scripts/verificar_datos.py ["BD/<archivo>.xlsx"]
Sale con codigo 1 si una columna obligatoria esta vacia en filas que existen,
o si una referencia no resuelve.
"""
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "scripts"))

try:
    import openpyxl
except ImportError:
    print("Falta openpyxl."); sys.exit(2)

from modelo_objetivo import MODELO
from sistema import VOLCADO

ARCHIVO = sys.argv[1] if len(sys.argv) > 1 else VOLCADO
if not os.path.isabs(ARCHIVO):
    ARCHIVO = os.path.join(RAIZ, ARCHIVO)

# Columnas que el modelo declara obligatorias y que HOY se sabe que operacion
# tiene que rellenar. No son un permiso indefinido: cada una lleva la fecha a
# partir de la cual el aviso pasa a fallo, igual que hace D-04 con los
# aplazamientos. Un aviso que no caduca deja de leerse (CLAUDE.md 7.11).
POBLA_OPERACION = {
    ("ACT_Activos", "SedeID"):
        ("solo la lleva el equipo bajo techo; el de via no tiene sede", None),
    ("SED_Sedes", "UnidadFuncionalID"):
        ("la UF de cada edificacion sale de su PR, y el PR de las sedes lo "
         "tiene operacion, no el contrato", "2026-08-31"),
    }


def texto(v):
    return "" if v is None else str(v).strip()


wb = openpyxl.load_workbook(ARCHIVO, data_only=True, read_only=True)
datos = {}
for t in MODELO:
    if t not in wb.sheetnames:
        continue
    ws = wb[t]
    cab = [texto(c.value) for c in next(ws.iter_rows(min_row=1, max_row=1))]
    filas = []
    for r in ws.iter_rows(min_row=2, values_only=True):
        if r is None or all(v in (None, "") for v in r):
            continue
        filas.append({c: (r[i] if i < len(r) else None)
                      for i, c in enumerate(cab) if c})
    datos[t] = filas

fallos, avisos = [], []
ancho = "=" * 78
print(ancho)
print("LOS DATOS SOSTIENEN EL MODELO")
print(ancho)
try:                                    # en Windows relpath revienta entre unidades
    _mostrado = os.path.relpath(ARCHIVO, RAIZ)
except ValueError:
    _mostrado = ARCHIVO
print("Archivo: %s" % _mostrado)
print("")

# ------------------------------------------- G-01  obligatoria y sin poblar
print("G-01  Columnas obligatorias, en las tablas que tienen filas")
print("")
for t in MODELO:
    filas = datos.get(t)
    if not filas:
        continue        # tabla vacia: F-11 ya avisa, aqui no hay nada que medir
    for col in MODELO[t]["columnas"]:
        if not col.get("obligatoria"):
            continue
        n = col["nombre"]
        vacias = [f for f in filas if not texto(f.get(n))]
        if not vacias:
            continue
        clave = (t, n)
        if clave in POBLA_OPERACION:
            motivo, limite = POBLA_OPERACION[clave]
            import datetime
            caducado = limite and datetime.date(*map(int, limite.split("-"))) \
                < datetime.date.today()
            linea = ("%s.%s vacia en %d de %d. La rellena operacion: %s"
                     % (t, n, len(vacias), len(filas), motivo))
            if caducado:
                fallos.append("[G-01] %s. El plazo vencio el %s" % (linea, limite))
            else:
                avisos.append("[G-01] %s%s"
                              % (linea, " (hasta el %s)" % limite if limite else ""))
            continue
        fallos.append(
            "[G-01] %s.%s es OBLIGATORIA y esta vacia en %d de %d filas. La "
            "aplicacion no dejara guardar, o peor: la expresion que la lea "
            "comparara contra blanco y no dara error"
            % (t, n, len(vacias), len(filas)))

# ---------------------------------------------- G-02  referencias que no resuelven
print("G-02  Las %d referencias, contra los datos reales"
      % sum(1 for t in MODELO for c in MODELO[t]["columnas"] if c.get("ref")))
print("")
huerfanas = 0
for t in MODELO:
    for col in MODELO[t]["columnas"]:
        destino = col.get("ref")
        if not destino or destino not in MODELO:
            continue
        pk = next((c["nombre"] for c in MODELO[destino]["columnas"] if c.get("pk")), None)
        if not pk:
            continue
        validas = {texto(f.get(pk)) for f in datos.get(destino, [])}
        if not validas:
            continue    # destino vacio: no se puede juzgar, F-11 ya lo dice
        malas = [texto(f.get(col["nombre"])) for f in datos.get(t, [])
                 if texto(f.get(col["nombre"]))
                 and texto(f.get(col["nombre"])) not in validas]
        if malas:
            huerfanas += len(malas)
            ejemplo = " · ".join(sorted(set(malas))[:4])
            fallos.append(
                "[G-02] %s.%s: %d valores no existen en %s.%s. AppSheet no da "
                "error: descarta la fila. Ejemplos: %s"
                % (t, col["nombre"], len(malas), destino, pk, ejemplo))

# ------------------------------------------- G-03  una columna, un tipo Python
#
# AppSheet infiere el tipo del CONTENIDO. Una columna con 'TRUE' de cadena y
# True booleano mezclados le da una senal contradictoria, y la resuelve por
# mayoria: la minoria se pierde. Es el mismo mecanismo que descartaba a un
# tecnico entero por tener la clave alfanumerica entre diez numericas.
print("G-03  Homogeneidad de tipo dentro de cada columna")
print("")
for t in MODELO:
    for col in MODELO[t]["columnas"]:
        n = col["nombre"]
        tipos = {type(f.get(n)).__name__ for f in datos.get(t, [])
                 if f.get(n) not in (None, "")}
        if len(tipos) > 1:
            avisos.append(
                "[G-03] %s.%s mezcla %s. AppSheet tipa por la mayoria"
                % (t, n, " y ".join(sorted(tipos))))

# -------------------------------------------------------------------- salida
for f in fallos:
    print("  x %s" % f)
if fallos:
    print("")
for a in avisos:
    print("  ! %s" % a)

print("")
print(ancho)
if fallos:
    print("LOS DATOS NO SOSTIENEN EL MODELO: %d fallos, %d avisos"
          % (len(fallos), len(avisos)))
    print("Estructura entregada sin poblacion. Es lo que los otros cinco")
    print("verificadores no pueden ver, porque no abren el archivo de datos.")
    print(ancho)
    sys.exit(1)

print("DATOS COHERENTES: 0 obligatorias vacias sin motivo · 0 referencias huerfanas")
print("%d avisos" % len(avisos))
print(ancho)
