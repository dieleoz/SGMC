# -*- coding: utf-8 -*-
"""Valida internamente el modelo objetivo del SGMC antes de desplegarlo.

Comprueba lo que en el modelo anterior fallo en produccion y nadie detecto a
tiempo: referencias que apuntan a nada, claves que no coinciden con el nombre
por el que se las referencia, evidencia duplicada y tablas huerfanas.

Uso:  python scripts/validar_modelo.py
Salida: 0 si el modelo es consistente, 1 si hay errores.
"""
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from modelo_objetivo import MODELO, TIPOS, GRUPOS, RETIRADAS, CAMPOS_RETIRADOS, REGLAS

errores, avisos = [], []


def error(regla, msg):
    errores.append(f"[{regla}] {msg}")


def aviso(regla, msg):
    avisos.append(f"[{regla}] {msg}")


# ---------------------------------------------------------------- V-01 claves
for tabla, d in MODELO.items():
    pks = [c for c in d["columnas"] if c.get("pk")]
    if len(pks) == 0:
        error("V-01", f"{tabla} no tiene clave primaria")
    elif len(pks) > 1:
        error("V-01", f"{tabla} tiene {len(pks)} claves primarias: {[c['nombre'] for c in pks]}")
    else:
        pk = pks[0]
        if pk["tipo"] != "Text":
            aviso("V-01", f"{tabla}.{pk['nombre']} es {pk['tipo']}; la convencion es Text")
        if not pk["nombre"].endswith("ID"):
            error("V-01", f"{tabla}.{pk['nombre']} es clave pero no termina en ID")

# ------------------------------------------------------ V-02 tipos declarados
for tabla, d in MODELO.items():
    for c in d["columnas"]:
        if c["tipo"] not in TIPOS:
            error("V-02", f"{tabla}.{c['nombre']} usa el tipo '{c['tipo']}', que no es valido")

# ------------------------------------------------- V-03 columnas sin duplicar
for tabla, d in MODELO.items():
    vistos = defaultdict(int)
    for c in d["columnas"]:
        vistos[c["nombre"]] += 1
    for nombre, n in vistos.items():
        if n > 1:
            error("V-03", f"{tabla}.{nombre} esta declarada {n} veces")

# ------------------------------------------------ V-04 referencias resolubles
for tabla, d in MODELO.items():
    for c in d["columnas"]:
        if c["tipo"] == "Ref":
            destino = c.get("ref")
            if not destino:
                error("V-04", f"{tabla}.{c['nombre']} es Ref pero no declara tabla destino")
            elif destino not in MODELO:
                error("V-04", f"{tabla}.{c['nombre']} apunta a '{destino}', que no existe en el modelo")
        elif c.get("ref"):
            error("V-04", f"{tabla}.{c['nombre']} declara destino pero su tipo es {c['tipo']}, no Ref")

# --------------------------------- V-05 la referencia se llama como la clave
for tabla, d in MODELO.items():
    for c in d["columnas"]:
        if c["tipo"] == "Ref" and c.get("ref") in MODELO:
            pk = next((x for x in MODELO[c["ref"]]["columnas"] if x.get("pk")), None)
            if pk and c["nombre"] != pk["nombre"] and not c.get("alias_justificado"):
                error("V-05", f"{tabla}.{c['nombre']} apunta a {c['ref']}, cuya clave es "
                              f"{pk['nombre']}. Renombra o declara alias_justificado")

# ------------------------------------------------------ V-06 tablas alcanzables
entrantes = defaultdict(set)
for tabla, d in MODELO.items():
    for c in d["columnas"]:
        if c["tipo"] == "Ref" and c.get("ref"):
            entrantes[c["ref"]].add(tabla)
raices = {"MAN_Mantenimientos", "OT_OrdenesTrabajo", "NOV_Novedades", "ASG_AsignacionZona"}
for tabla in MODELO:
    salientes = [c for c in MODELO[tabla]["columnas"] if c["tipo"] == "Ref"]
    # Una hoja legitima: cuelga de un padre con IsPartOf, luego nadie la referencia
    es_hoja = any(c.get("es_parte_de") for c in MODELO[tabla]["columnas"])
    if not entrantes[tabla] and not salientes and tabla not in raices:
        error("V-06", f"{tabla} no referencia ni es referenciada: quedaria huerfana")
    elif not entrantes[tabla] and tabla not in raices and not es_hoja:
        aviso("V-06", f"{tabla} no es referenciada por nadie. Confirma que es punto de entrada")

# ------------------------------------------------- V-07 evidencia sin duplicar
# Solo cuenta el ALMACENAMIENTO de evidencia, no los indicadores booleanos que
# la exigen: FRM_Preguntas.RequiereFoto es una bandera, no una fotografia.
for tabla, d in MODELO.items():
    if tabla in ("FOT_Fotografias", "FIR_Firmas", "NOV_Novedades"):
        continue
    for c in d["columnas"]:
        if c["tipo"] in ("Image", "Signature"):
            error("V-07", f"{tabla}.{c['nombre']} almacena evidencia fuera de las tablas hijas. "
                          f"Es la duplicacion que se acordo eliminar")

# ------------------------------------------------------- V-08 IsPartOf con Ref
for tabla, d in MODELO.items():
    for c in d["columnas"]:
        if c.get("es_parte_de") and c["tipo"] != "Ref":
            error("V-08", f"{tabla}.{c['nombre']} declara IsPartOf pero no es Ref")

# ------------------------------------------------------ V-09 grupos declarados
for tabla, d in MODELO.items():
    if d.get("grupo") not in GRUPOS:
        error("V-09", f"{tabla} declara el grupo '{d.get('grupo')}', que no existe")
    if not d.get("proposito"):
        error("V-09", f"{tabla} no declara proposito")

# ------------------------------------- V-10 las reglas apuntan a algo existente
for r in REGLAS:
    if r["tabla"] not in MODELO:
        error("V-10", f"La regla {r['id']} apunta a la tabla {r['tabla']}, que no existe")
    elif r["columna"] != "(tabla)":
        nombres = [c["nombre"] for c in MODELO[r["tabla"]]["columnas"]]
        if r["columna"] not in nombres:
            error("V-10", f"La regla {r['id']} apunta a {r['tabla']}.{r['columna']}, que no existe")

# ---------------------------- V-11 las rutas de desreferencia son navegables
def validar_ruta(regla_id, tabla_origen, ruta):
    """Comprueba que [A].[B].[C] sea navegable desde la tabla de origen."""
    actual = tabla_origen
    for i, campo in enumerate(ruta):
        cols = {c["nombre"]: c for c in MODELO[actual]["columnas"]}
        if campo not in cols:
            error("V-11", f"{regla_id}: '{campo}' no existe en {actual} "
                          f"(ruta {'.'.join(ruta)})")
            return
        c = cols[campo]
        ultimo = i == len(ruta) - 1
        if not ultimo:
            if c["tipo"] != "Ref":
                error("V-11", f"{regla_id}: no se puede desreferenciar {actual}.{campo}, "
                              f"es {c['tipo']} y no Ref")
                return
            actual = c["ref"]


import re
for r in REGLAS:
    if r["tabla"] not in MODELO:
        continue
    expr = r["expresion"]
    # Dentro de SELECT(Tabla[Col], ...) el contexto cambia a esa tabla.
    contextos = [(r["tabla"], expr)]
    for m in re.finditer(r"SELECT\(\s*(\w+)\[", expr):
        otra = m.group(1)
        if otra in MODELO:
            contextos.append((otra, expr[m.end():]))
            expr = expr[:m.start()]          # el resto se evalua en la tabla base
            contextos[0] = (r["tabla"], expr)
        else:
            error("V-11", f"{r['id']}: SELECT sobre '{otra}', que no existe en el modelo")
    for tabla_ctx, trozo in contextos:
        for cadena in re.findall(r"(?:\[\w+\]\.)+\[\w+\]", trozo):
            ruta = re.findall(r"\[(\w+)\]", cadena)
            validar_ruta(r["id"], tabla_ctx, ruta)

# ------------------------------- V-12 lo retirado no sigue vivo en el modelo
for tabla in RETIRADAS:
    if tabla in MODELO:
        error("V-12", f"{tabla} figura como retirada y sigue declarada en el modelo")
for tabla, campos in CAMPOS_RETIRADOS.items():
    if tabla in MODELO:
        vivos = {c["nombre"] for c in MODELO[tabla]["columnas"]}
        for campo in campos:
            if campo in vivos:
                error("V-12", f"{tabla}.{campo} figura como retirado y sigue declarado")

# ------------------------------------------------ V-13 cobertura de los flujos
COBERTURA = {
    "Geofencing de cierre": ("MAN_Mantenimientos", "Coordenadas_Cierre"),
    "Precision del GPS": ("MAN_Mantenimientos", "Precision_GPS"),
    "Excepcion por GPS deficiente": ("MAN_Mantenimientos", "CierreConExcepcion"),
    "Segunda visita": ("MAN_Mantenimientos", "RequiereSegundaVisita"),
    "Devolucion del supervisor": ("MAN_Mantenimientos", "ObservacionRechazo"),
    "Aprobacion del supervisor": ("MAN_Mantenimientos", "AprobadoSupervisor"),
    "Checklist por tipo de activo": ("TIP_TiposActivo", "FormularioID"),
    "Radio por tipo de activo": ("TIP_TiposActivo", "RadioGeofencingKm"),
    "Trazabilidad de la pregunta": ("CHD_ChecklistDetalle", "PreguntaID"),
    "Version del formulario": ("CHK_Checklists", "VersionFormulario"),
    "Orden de seguimiento": ("OT_OrdenesTrabajo", "OTOrigenID"),
    "Novedad desde campo": ("NOV_Novedades", "Descripcion"),
    "Criticidad para disponibilidad": ("ACT_Activos", "Criticidad"),
}
for flujo, (tabla, columna) in COBERTURA.items():
    if tabla not in MODELO:
        error("V-13", f"El flujo '{flujo}' necesita la tabla {tabla}, que no existe")
    elif columna not in {c["nombre"] for c in MODELO[tabla]["columnas"]}:
        error("V-13", f"El flujo '{flujo}' necesita {tabla}.{columna}, que no existe")


# ------------------------------------------------------------------- informe
def informe():
    print("=" * 78)
    print("VALIDACION DEL MODELO OBJETIVO — SGMC")
    print("=" * 78)
    n_cols = sum(len(d["columnas"]) for d in MODELO.values())
    n_refs = sum(1 for d in MODELO.values() for c in d["columnas"] if c["tipo"] == "Ref")
    print(f"Tablas: {len(MODELO)}  |  Columnas: {n_cols}  |  Referencias: {n_refs}  "
          f"|  Reglas: {len(REGLAS)}")
    print(f"Tablas retiradas: {len(RETIRADAS)}  |  "
          f"Campos retirados de MAN: {len(CAMPOS_RETIRADOS.get('MAN_Mantenimientos', {}))}")
    por_grupo = defaultdict(int)
    for d in MODELO.values():
        por_grupo[d["grupo"]] += 1
    print("Por grupo: " + ", ".join(f"{g} {por_grupo[g]}" for g in GRUPOS))
    nuevas = [t for t, d in MODELO.items() if d.get("nueva")]
    print(f"Tablas nuevas ({len(nuevas)}): {', '.join(nuevas)}")
    print("-" * 78)
    if errores:
        print(f"ERRORES ({len(errores)}) — el modelo no se puede desplegar asi:")
        for e in errores:
            print("  x", e)
    else:
        print("ERRORES: ninguno")
    print()
    if avisos:
        print(f"AVISOS ({len(avisos)}) — revisar, no bloquean:")
        for a in avisos:
            print("  -", a)
    else:
        print("AVISOS: ninguno")
    print("=" * 78)
    print("APTO PARA DESPLEGAR" if not errores else "NO APTO: corrige los errores")
    return 1 if errores else 0


if __name__ == "__main__":
    sys.exit(informe())
