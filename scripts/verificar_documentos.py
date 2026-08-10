# -*- coding: utf-8 -*-
"""Comprueba que la prosa no contradiga al modelo.

Uso:  python scripts/verificar_documentos.py

Por que existe
--------------
Este proyecto no falla por falta de cuidado: falla porque los documentos se
escriben leyendo otros documentos en vez de volcar el modelo.

  - bd.md decia "24 hojas" cuando habia 32. Se arreglo generandolo.
  - El manual mandaba editar CHD_ChecklistDetalle para cambiar preguntas. Esa
    tabla guarda RESPUESTAS: seguir la instruccion reescribe el historico.
  - Se propusieron como tablas nuevas ROL_Roles, FRM_Formularios, FRM_Secciones
    y FRM_Preguntas. Las cuatro ya estaban en MODELO.

Ninguna de las tres la detecto una persona leyendo. Las tres son mecanicas.

Lo que comprueba
----------------
  D-01  Toda tabla citada en la prosa existe en MODELO, RETIRADAS o PROPUESTAS
  D-02  Ninguna tabla PROPUESTA existe ya en MODELO
  D-03  Toda referencia Tabla.Columna apunta a una columna que existe
  D-04  Ningun mecanismo descartado en DECISIONES reaparece vivo en MODELO
  D-05  Toda tabla de MODELO aparece citada en alguna parte de la prosa

Que NO comprueba: si la prosa es cierta. Solo si sus nombres existen. Un
documento puede pasar las cinco y seguir estando equivocado -por eso sigue
haciendo falta el arquitecto-.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from modelo_objetivo import (MODELO, RETIRADAS, PROPUESTAS, DECISIONES,
                             CAMPOS_RETIRADOS, COLUMNAS_PROPUESTAS,
                             COLUMNAS_SIN_DECIDIR)

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Documentos que se revisan. Los historicos no: describen estados superados a
# proposito, y corregirlos borraria la trazabilidad de por que se cambio.
CARPETAS = ["docs", "Manuales", "."]
EXCLUIR = ["docs/historico", "docs\\historico", "node_modules", ".git"]

# TABLA en el formato del proyecto: tres o cuatro mayusculas, guion bajo, nombre.
RE_TABLA = re.compile(r"\b([A-Z]{2,4}_[A-Za-z][A-Za-z0-9]*)\b")
RE_COLUMNA = re.compile(r"\b([A-Z]{2,4}_[A-Za-z][A-Za-z0-9]*)\.([A-Za-z_][A-Za-z0-9_]*)\b")

# Tokens que TIENEN forma de tabla y no lo son. Cada uno se declara aqui con lo
# que realmente es, para que nadie lo confunda mas adelante.
NO_SON_TABLAS = {
    # Valores de TIP_TiposActivo.FormularioID, no tablas
    "FRM_SOS", "FRM_CCTV", "FRM_PMVF", "FRM_PMVM", "FRM_SGM", "FRM_SGE",
    "FRM_SSA", "FRM_GENE", "FRM_BASC", "FRM_FO", "FRM_VW", "FRM_SWIT",
    "FRM_ROUT", "FRM_FIRE", "FRM_UPS", "FRM_SERV", "FRM_NAS", "FRM_SUBE",
    # Trozo del nombre de un archivo de contexto
    "ITS_TI",
    # Nombre de una vista de AppSheet, no de una tabla
    "OT_Detail",
    # Funcion de AppSheet, no tabla
    "REF_ROWS",
    # Identificador de codigo de este mismo script, citado en ESPEC-003
    "RE_TABLA",
}

# Claves de fila que se citan como Tabla.Valor y parecen columnas.
RE_CLAVE_FILA = re.compile(r"^([A-Z0-9_]+|[0-9a-f]{6,}|.*\d.*)$")

fallos = []
avisos = []


def falla(regla, msg):
    fallos.append("[%s] %s" % (regla, msg))


def aviso(regla, msg):
    avisos.append("[%s] %s" % (regla, msg))


def documentos():
    out = []
    for carpeta in CARPETAS:
        base = os.path.join(RAIZ, carpeta)
        if not os.path.isdir(base):
            continue
        for dirpath, dirnames, filenames in os.walk(base):
            rel_dir = os.path.relpath(dirpath, RAIZ)
            if any(x in rel_dir for x in EXCLUIR):
                dirnames[:] = []
                continue
            for f in filenames:
                if f.endswith(".md"):
                    out.append(os.path.join(dirpath, f))
            if carpeta == ".":
                dirnames[:] = []   # la raiz no se recorre entera
    return sorted(set(out))


CONOCIDAS = set(MODELO) | set(RETIRADAS) | set(PROPUESTAS)
citadas = {}          # tabla -> [documentos donde aparece]

# ------------------------------------------------------------------ D-02
# Se comprueba antes de leer nada: es un defecto del modelo, no de la prosa.
for t in PROPUESTAS:
    if t in MODELO:
        falla("D-02", "%s figura como PROPUESTA y ya existe en MODELO. "
                      "Se propuso algo que ya estaba: retirala de PROPUESTAS" % t)

# ------------------------------------------------------------------ D-04
for d in DECISIONES:
    desc = d[2]
    pendiente = d[4] if len(d) > 4 else None
    if "." not in desc:
        continue
    tabla, columna = desc.split(".", 1)
    if tabla not in MODELO:
        continue
    vivas = [c["nombre"] for c in MODELO[tabla]["columnas"]]
    if columna not in vivas or columna in CAMPOS_RETIRADOS.get(tabla, {}):
        continue
    if pendiente:
        aviso("D-04", "%s se descarto y sigue viva. Programada para retirarse en %s"
                      % (desc, pendiente))
    else:
        falla("D-04", "%s se descarto en DECISIONES pero sigue viva en MODELO, y "
                      "nadie declaro cuando se retira" % desc)

# ------------------------------------------------------------- D-01 y D-03
for ruta in documentos():
    rel = os.path.relpath(ruta, RAIZ).replace("\\", "/")
    with open(ruta, encoding="utf-8") as f:
        texto = f.read()

    # Un documento puede declarar que habla de estados superados.
    if "NO ENTREGAR" in texto[:2000] or "documento historico" in texto[:2000].lower():
        continue

    # Salida explicita: un documento que menciona un nombre PARA DESCARTARLO -o que
    # cita la salida de este mismo script- lo declara con una linea
    #     <!-- verificar_documentos: ignorar NOMBRE, NOMBRE -->
    # Es deliberadamente incomoda y greppable: si aparece en muchos sitios, el
    # problema es el criterio, no el documento.
    ignorar_aqui = set()
    for m in re.finditer(r"<!--\s*verificar_documentos:\s*ignorar\s+([^>]+?)\s*-->", texto):
        ignorar_aqui.update(x.strip() for x in m.group(1).split(","))

    vistas = set()
    for m in RE_TABLA.finditer(texto):
        t = m.group(1)
        if t in NO_SON_TABLAS or t in ignorar_aqui:
            continue
        citadas.setdefault(t, []).append(rel)
        if t not in CONOCIDAS and t not in vistas:
            vistas.add(t)
            falla("D-01", "%s cita la tabla %s, que no esta en MODELO ni en "
                          "RETIRADAS ni en PROPUESTAS. Si hace falta, declarala "
                          "en PROPUESTAS con su motivo" % (rel, t))

    for m in RE_COLUMNA.finditer(texto):
        t, c = m.group(1), m.group(2)
        if t not in MODELO:
            continue          # tabla propuesta o retirada: sus columnas aun no existen
        vivas = {x["nombre"] for x in MODELO[t]["columnas"]}
        if c in vivas or c in CAMPOS_RETIRADOS.get(t, {}):
            continue          # citar lo retirado es legitimo: se habla de ello
        if (t, c) in COLUMNAS_PROPUESTAS:
            continue          # declarada como propuesta, con su motivo
        if (t, c) in COLUMNAS_SIN_DECIDIR:
            continue          # existe en la hoja, pendiente de decidir. Avisa D-06
        if RE_CLAVE_FILA.match(c):
            continue          # PAR_Parametros.UMBRAL_GPS es una fila, no una columna
        if (t, c) in vistas:
            continue
        vistas.add((t, c))
        falla("D-03", "%s cita %s.%s y esa columna no existe en el modelo" % (rel, t, c))

# ------------------------------------------------------------------ D-06
# Columnas que estan en la hoja y el modelo no declara. No fallan -la decision
# esta declarada como pendiente- pero no se pueden olvidar.
for (t, c), motivo in sorted(COLUMNAS_SIN_DECIDIR.items()):
    aviso("D-06", "%s.%s existe en la hoja y el modelo no la declara. %s" % (t, c, motivo))

# ------------------------------------------------------------------ D-05
for t in MODELO:
    if t not in citadas:
        aviso("D-05", "%s existe en el modelo y no la menciona ningun documento. "
                      "Una tabla que nadie explica es una tabla que nadie usa" % t)

# ------------------------------------------------------------------ salida
print("=" * 78)
print("VERIFICACION DE DOCUMENTOS CONTRA EL MODELO")
print("=" * 78)
print("Documentos revisados: %d" % len(documentos()))
print("Tablas del modelo: %d | propuestas: %d | retiradas: %d"
      % (len(MODELO), len(PROPUESTAS), len(RETIRADAS)))
print("Decisiones de una sola forma: %d" % len(DECISIONES))
print()

for x in fallos:
    print("  x " + x)
if fallos:
    print()
for x in avisos:
    print("  - " + x)
if avisos:
    print()

print("=" * 78)
if fallos:
    print("%d FALLOS. La prosa contradice al modelo." % len(fallos))
    sys.exit(1)
print("DOCUMENTOS CONSISTENTES CON EL MODELO (%d avisos)" % len(avisos))
