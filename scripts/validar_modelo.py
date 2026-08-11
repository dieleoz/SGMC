# -*- coding: utf-8 -*-
"""Valida internamente el modelo objetivo del SGMC antes de desplegarlo.

Comprueba lo que en el modelo anterior fallo en produccion y nadie detecto a
tiempo: referencias que apuntan a nada, claves que no coinciden con el nombre
por el que se las referencia, evidencia duplicada y tablas huerfanas.

Uso:  python scripts/validar_modelo.py
Salida: 0 si el modelo es consistente, 1 si hay errores.
"""
import os
import re
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from modelo_objetivo import (MODELO, TIPOS, GRUPOS, RETIRADAS, CAMPOS_RETIRADOS, REGLAS,
                             RENOMBRADOS, RETIPADOS, CLAVE_LEGIBLE,
                             CLAVE_ES_LA_PALABRA,
                             CLAVE_GENERADA)

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
# Una tabla de configuracion no la referencia nadie: se lee con LOOKUP(). Lo
# declara ella misma en el modelo, no una excepcion escondida en el validador.
raices |= {t for t, d in MODELO.items() if d.get("acceso_por_lookup")}
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
    elif r["columna"] not in ("(tabla)", "(varias)"):
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


def _expresiones_a_validar():
    """Toda expresion del modelo, venga de REGLAS o de una columna.

    V-11 solo recorria REGLAS. V-17, dos secciones mas abajo, si recorre ademas
    las columnas -y esa asimetria era el agujero-: una expresion escrita en el
    `formula` o el `valid_if` de una columna **no se validaba en absoluto**.

    Lo demostro el arquitecto el 2026-08-10 metiendo en una columna la peor
    expresion posible -desreferenciar un Yes/No y nombrar una columna que no
    existe, los dos defectos que V-11 nacio para cazar-. El validador respondio
    APTO PARA DESPLEGAR. La misma expresion dentro de REGLAS daba dos errores.

    Hoy no hay ninguna columna con `formula` ni `valid_if` sin regla propia, asi
    que esto no caza nada: entra ANTES de que la haya. ESPEC-005 propone crear
    las dos primeras.
    """
    for r in REGLAS:
        yield r["id"], r["tabla"], r["expresion"]
    for tabla, d in MODELO.items():
        for c in d["columnas"]:
            for campo in ("valid_if", "formula", "valor_inicial"):
                if c.get(campo):
                    yield "%s.%s (%s)" % (tabla, c["nombre"], campo), tabla, c[campo]


for _ident, _tabla, _expresion in _expresiones_a_validar():
    r = {"id": _ident, "tabla": _tabla, "expresion": _expresion}
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

# ------------- V-17 no comparar un Ref contra un literal de texto
# Un Ref guarda la CLAVE del destino, no su nombre. Comparar la columna a secas
# contra una cadena legible es casi siempre un error, y de los peores: no falla,
# simplemente devuelve siempre lo mismo. Si ademas la expresion es una App
# formula, ESCRIBE ese resultado constante sobre los datos.
#
# Caso real, 2026-08-07: RG-16 decia [EstadoActivoID] <> "Retirado" sobre una
# EST_Activo con claves 1 a 4. Siempre cierto, y al ser App formula habria
# repuesto Activo=TRUE sobre el activo que acababa de darse de baja.
# V-11 no lo veia: solo comprueba cadenas de mas de un salto.
# Cuatro formas de escribir la misma comparacion. Las cuatro se cazan.
_LIT = r'"[^"]*"' + "|" + r"'[^']*'"
COMPARA = [
    re.compile(r'\[(\w+)\](?!\s*\.\s*\[)\s*(?:=|<>|<=|>=|<|>)\s*(' + _LIT + ')'),   # [Col] = "x"
    re.compile(r'(' + _LIT + r')\s*(?:=|<>|<=|>=|<|>)\s*\[(\w+)\](?!\s*\.\s*\[)'),   # "x" = [Col]
    re.compile(r'(?:IN|CONTAINS|SWITCH)\(\s*\[(\w+)\](?!\s*\.\s*\[)\s*,([^)]*)'),          # IN([Col], LIST("x"))
]


def _revisar_literales(ident, tabla, expresion):
    if tabla not in MODELO:
        return
    cols = {c["nombre"]: c for c in MODELO[tabla]["columnas"]}
    encontrados = []
    for i, patron in enumerate(COMPARA):
        for m in patron.findall(expresion):
            columna, resto = (m[1], m[0]) if i == 1 else (m[0], m[1])
            literales = re.findall(_LIT, resto) if i == 2 else [resto]
            for lit in literales:
                encontrados.append((columna, lit[1:-1] if len(lit)>1 else lit))
    for columna, literal in encontrados:
        c = cols.get(columna)
        if not c or c["tipo"] != "Ref":
            continue
        destino = c.get("ref")
        # Contra un catalogo cuya clave ES la palabra, la comparacion es
        # CORRECTA. EOT_EstadosOrden se construyo asi a proposito.
        #
        # Se pregunta a CLAVE_ES_LA_PALABRA, no a CLAVE_LEGIBLE. Preguntarselo a
        # la segunda es lo que apago esta regla el 2026-08-10: la resiembra metio
        # EST_Activo en CLAVE_LEGIBLE -clave EST-01..EST-04- y con eso V-17 dejo
        # de cazar [EstadoActivoID] <> "Retirado", que es el defecto para el que
        # nacio. Una lista que responde "como se ve la clave" no puede responder
        # tambien "contra que se puede comparar".
        if destino in CLAVE_ES_LA_PALABRA:
            continue
        pk = next((x["nombre"] for x in MODELO[destino]["columnas"] if x.get("pk")), "?")
        error("V-17", f"{ident}: compara {tabla}.{columna} con el literal '{literal}'. "
                      f"Es un Ref a {destino}, cuya clave {pk} NO es texto legible: "
                      f"guarda un identificador. Prueba con [{columna}].[Nombre]")


for r in REGLAS:
    _revisar_literales(r["id"], r["tabla"], r["expresion"])
for tabla, d in MODELO.items():
    for c in d["columnas"]:
        for campo in ("valid_if", "formula", "valor_inicial"):
            if c.get(campo):
                _revisar_literales(f"{tabla}.{c['nombre']} ({campo})", tabla, c[campo])

# ------- V-18 la misma regla declarada dos veces, con expresiones distintas
#
# Una regla puede estar escrita en DOS sitios: en la columna -`formula`,
# `valid_if`, `valor_inicial`- y en REGLAS. Cuando divergen, cada consumidor
# lee una cosa distinta y nadie lo nota.
#
# Paso con RG-19 y era la unica: la columna decia
#     [Precision_GPS] > LOOKUP("UMBRAL_GPS", ...)
# y REGLAS decia
#     OR(ISBLANK(LOOKUP(...)), [Precision_GPS] > LOOKUP(...))
#
# No es un matiz. RECONSTRUCCION_EXPRESIONES -lo que el ejecutor teclea- toma la
# de REGLAS, la del OR. Sin la guarda, la regla es falsa siempre; CON la guarda,
# es falsa **solo mientras el parametro UMBRAL_GPS exista**. Bastaba con borrar
# esa fila -y hay dos cuentas con permiso de edicion sobre el Sheets- para que
# CierreConExcepcion saliera TRUE en todos los cierres.
#
# Lo escribe el arquitecto y tiene razon en la urgencia: ESPEC-004 propone
# retirar RG-19, y con ella desapareceria el unico caso, dejando la divergencia
# sin vigilancia. La comprobacion va ANTES que la retirada.
# Se compara SOLO la propiedad que corresponde al tipo de la regla. Compararlas
# todas daba un falso positivo inmediato: RG-01 es un Valid_If y la misma
# columna tiene HERE() como valor inicial, que es otra propiedad y no una
# divergencia. Un falso positivo en un gate que bloquea el despliegue ensena a
# desactivarlo.
_PROPIEDAD = {
    "Valid_If": "valid_if",
    "App formula": "formula",
    "Initial value": "valor_inicial",
    }
for r in REGLAS:
    _t, _c = r["tabla"], r.get("columna")
    _campo = _PROPIEDAD.get(r["tipo"])
    if not _c or _c.startswith("(") or not _campo:
        continue
    _col = next((x for x in MODELO.get(_t, {}).get("columnas", [])
                 if x["nombre"] == _c), None)
    if _col:
        _v = (_col.get(_campo) or "").strip()
        if _v and _v != (r.get("expresion") or "").strip():
            error("V-18",
                  f"{r['id']} esta declarada DOS VECES con expresiones distintas. "
                  f"{_t}.{_c}.{_campo} dice «{_v}» y REGLAS dice "
                  f"«{r['expresion']}». Cada consumidor lee una: "
                  f"RECONSTRUCCION_EXPRESIONES toma la de REGLAS")

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
    "Geofencing de cierre": ("MAN_Mantenimientos", "Coordenadas_Cierre_LatLong"),
    # "Precision del GPS" se retiro con ESPEC-004/ORDEN-004: USERLOCATIONACCURACY() no existe
    # en AppSheet, Precision_GPS se retiro del modelo (CAMPOS_RETIRADOS). La excepcion por GPS
    # deficiente ahora es una marca del tecnico, cubierta por el flujo de abajo.
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

# ------------------------------ V-14 el renombrado aterriza en algo que existe
# Un renombrado que apunta a una columna inexistente deja la migracion a medias:
# el operador renombra en el Sheets y luego no encuentra donde cablear.
for tabla, mapa in RENOMBRADOS.items():
    if tabla not in MODELO:
        error("V-14", f"RENOMBRADOS declara {tabla}, que no existe en el modelo objetivo")
        continue
    vivos = {c["nombre"] for c in MODELO[tabla]["columnas"]}
    retirados = set(CAMPOS_RETIRADOS.get(tabla, {}))
    for actual, (objetivo, _motivo) in mapa.items():
        if objetivo not in vivos and objetivo not in retirados:
            error("V-14", f"{tabla}.{actual} se renombra a '{objetivo}', que no existe en el "
                          f"modelo ni figura como retirado")
        if actual in vivos and actual != objetivo:
            aviso("V-14", f"{tabla}.{actual} se renombra a '{objetivo}', pero '{actual}' sigue "
                          f"siendo una columna viva con otro significado. Al migrar, renombra "
                          f"antes de crear la nueva, o el Sheets quedara con dos columnas iguales")

# -------------------------- V-15 toda referencia declara como llega a existir
# Cada Ref sobre una tabla que ya existe tiene que venir de algun sitio: de un
# renombrado, de un retipado, o ser columna nueva. La que no declara nada es la
# que nadie crea el dia de la migracion.
# Solo se exige en las tablas cuyos encabezados reales se leyeron uno por uno.
for tabla in RENOMBRADOS:
    if tabla not in MODELO:
        continue
    objetivos = {obj for obj, _ in RENOMBRADOS[tabla].values()}
    retipadas = set(RETIPADOS.get(tabla, {}))
    for c in MODELO[tabla]["columnas"]:
        if c["tipo"] != "Ref" or not c.get("ref"):
            continue
        if MODELO[c["ref"]].get("nueva"):
            continue          # apunta a tabla nueva: no habia como cablearla antes
        if c["nombre"] in objetivos or c["nombre"] in retipadas or c.get("nueva"):
            continue
        error("V-15", f"{tabla}.{c['nombre']} es Ref a {c['ref']} y no declara de donde sale: "
                      f"ni renombrado, ni retipado, ni columna nueva")

# -------------------- V-16 lo retipado existe y coincide con el tipo objetivo
for tabla, mapa in RETIPADOS.items():
    if tabla not in MODELO:
        error("V-16", f"RETIPADOS declara {tabla}, que no existe en el modelo objetivo")
        continue
    cols = {c["nombre"]: c for c in MODELO[tabla]["columnas"]}
    for columna, (_actual, destino_tipo, destino_tabla, _motivo) in mapa.items():
        if columna not in cols:
            error("V-16", f"{tabla}.{columna} figura como retipado pero no existe en el modelo")
            continue
        c = cols[columna]
        if c["tipo"] != destino_tipo:
            error("V-16", f"{tabla}.{columna} se retipa a {destino_tipo}, pero el modelo lo "
                          f"declara {c['tipo']}")
        if destino_tipo == "Ref" and c.get("ref") != destino_tabla:
            error("V-16", f"{tabla}.{columna} se retipa a Ref hacia {destino_tabla}, pero el "
                          f"modelo lo apunta a {c.get('ref')}")


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
