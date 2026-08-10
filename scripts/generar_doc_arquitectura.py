# -*- coding: utf-8 -*-
"""Genera docs/ARQUITECTURA_OBJETIVO_SGMC.md desde modelo_objetivo.py.

La documentacion no se escribe a mano: se deriva del modelo. Asi es imposible
que el documento y el diseno divergan, que es exactamente lo que le paso a este
proyecto con bd.md y el Excel.
"""
import os
import sys
import subprocess

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from modelo_objetivo import (MODELO, GRUPOS, RETIRADAS, CAMPOS_RETIRADOS, REGLAS,
                             RENOMBRADOS, RETIPADOS)

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SALIDA = os.path.join(RAIZ, "docs", "ARQUITECTURA_OBJETIVO_SGMC.md")

L = []
w = L.append


def pk_de(tabla):
    return next((c["nombre"] for c in MODELO[tabla]["columnas"] if c.get("pk")), "?")


# ------------------------------------------------------------------ cabecera
w("# Arquitectura objetivo del SGMC")
w("")
w("**Generado automáticamente** por `scripts/generar_doc_arquitectura.py` desde")
w("`scripts/modelo_objetivo.py`. No editar a mano: los cambios se hacen en el modelo y se")
w("regenera. Validado con `scripts/validar_modelo.py`.")
w("")
w("Este documento define **el diseño de datos que se construye**: tablas, columnas, claves,")
w("referencias y reglas. Lo que la hoja tiene hoy, columna a columna, está en `bd.md`, también")
w("generado; para qué sirve cada pieza y quién la usa, en `FUNCIONAL_SGMC.md`. Los tres se")
w("complementan y ninguno sustituye a los otros dos.")
w("")
w("**El modelo describe datos, no interfaz.** No hay aquí vistas, acciones ni slices: no existen en")
w("`modelo_objetivo.py`. Mientras no se declaren, el paso de vistas de cualquier manual se queda en")
w("«se construye sola», que es la clase de instrucción que este proyecto tiene prohibida.")
w("")
n_cols = sum(len(d["columnas"]) for d in MODELO.values())
n_refs = sum(1 for d in MODELO.values() for c in d["columnas"] if c["tipo"] == "Ref")
nuevas = [t for t, d in MODELO.items() if d.get("nueva")]
w(f"**{len(MODELO)} tablas · {n_cols} columnas · {n_refs} referencias · {len(REGLAS)} reglas**")
w("")
w("---")
w("")

# ---------------------------------------------------------------- convenciones
w("## 1. Convenciones")
w("")
w("Cinco reglas que el modelo anterior no tenía, y cuya ausencia explica sus fallos:")
w("")
w("1. **Toda tabla tiene una clave primaria única, de tipo texto, llamada `<Prefijo>ID`.**")
w("2. **Toda referencia se llama igual que la clave a la que apunta.** La mezcla de `OTID` con")
w("   `Numero_OT` fue causa directa de registros huérfanos. Cuando el mismo destino se referencia")
w("   con dos roles distintos, como técnico y supervisor, el alias se declara y se justifica.")
w("3. **Un dato se guarda en un solo lugar.** Nada de evidencia repetida entre campos embebidos y")
w("   tablas hijas.")
w("4. **Las tablas hijas llevan `IsPartOf`:** se crean, editan y borran con su padre.")
w("5. **Los catálogos llevan `Activo`,** para retirar un valor sin romper el histórico.")
w("")

# ------------------------------------------------------------------- cambios
w("## 2. Qué cambia respecto del modelo actual")
w("")
w("### 2.1 Tablas nuevas")
w("")
w("| Tabla | Por qué |")
w("|---|---|")
for t in nuevas:
    w(f"| `{t}` | {MODELO[t]['proposito']} |")
w("")
w("### 2.2 Tablas que se retiran")
w("")
w("| Tabla | Motivo |")
w("|---|---|")
for t, motivo in RETIRADAS.items():
    w(f"| `{t}` | {motivo} |")
w("")
w("### 2.3 Campos que se retiran")
w("")
w("`MAN_Mantenimientos` pasa de 24 columnas heterogéneas a un registro de ejecución limpio. El")
w("resto son campos que guardaban por segunda vez un dato alcanzable por referencia.")
w("")
for tabla, campos in CAMPOS_RETIRADOS.items():
    w(f"**`{tabla}`**")
    w("")
    w("| Campo | Motivo |")
    w("|---|---|")
    for campo, motivo in campos.items():
        w(f"| `{campo}` | {motivo} |")
    w("")

# --------------------------------------------------- cableado de referencias
w("### 2.4 Cableado de referencias")
w("")
w("El defecto raíz del sistema actual no es que falten columnas: es que las que existen son")
w("texto. AppSheet responde `Invalid dereference. Column OTID is not a Ref`, y con eso caen el")
w("geofencing, la navegación padre-hijo y todo reporte por activo.")
w("")
w("Una referencia de AppSheet **guarda el valor de la clave de la tabla destino**. Por eso")
w("renombrar y retipar no son dos tareas sino una: si la clave se llama `Numero_OT` y quien la")
w("apunta se llama `OTID`, la conversión no tiene contra qué resolver.")
w("")
w("Los nombres actuales se verificaron el 2026-08-07 leyendo `BD/Modelo de Datos (2).xlsx` con")
w("`openpyxl`, encabezado por encabezado, sobre las cinco tablas implicadas.")
w("")
w("#### Conservan el nombre, cambian de tipo")
w("")
w("| Tabla | Columna | Tipo actual | Tipo objetivo | Apunta a | Nota |")
w("|---|---|---|---|---|---|")
for tabla, mapa in RETIPADOS.items():
    for columna, (actual, destino, destino_tabla, motivo) in mapa.items():
        w(f"| `{tabla}` | `{columna}` | {actual} | **{destino}** | `{destino_tabla}` | {motivo} |")
w("")
w("#### Cambian de nombre")
w("")
w("| Tabla | Nombre actual | Nombre objetivo | Por qué |")
w("|---|---|---|---|")
for tabla, mapa in RENOMBRADOS.items():
    for actual, (objetivo, motivo) in mapa.items():
        w(f"| `{tabla}` | `{actual}` | **`{objetivo}`** | {motivo} |")
w("")
w("#### La trampa del nombre reutilizado")
w("")
w("`OT_OrdenesTrabajo.Activo` guarda hoy el identificador del activo, pero en el modelo objetivo")
w("`Activo` es la bandera `Yes/No` que llevan todas las tablas. **Son dos columnas distintas que")
w("se llaman igual en momentos distintos.** Al migrar hay que renombrar la vieja antes de crear la")
w("nueva; en el orden inverso el Sheets queda con dos columnas `Activo` y AppSheet resuelve una de")
w("las dos sin avisar cuál. `validar_modelo.py` lo señala como aviso V-14.")
w("")

# -------------------------------------------------------------------- modelo
w("## 3. Diagrama de relaciones")
w("")
w("```mermaid")
w("erDiagram")
for tabla, d in MODELO.items():
    for c in d["columnas"]:
        if c["tipo"] == "Ref" and c.get("ref"):
            card = '||--o{' if c.get("es_parte_de") else '}o--||'
            if c.get("es_parte_de"):
                w(f"    {c['ref']} ||--o{{ {tabla} : \"{c['nombre']}\"")
            else:
                w(f"    {tabla} }}o--|| {c['ref']} : \"{c['nombre']}\"")
w("```")
w("")

# ------------------------------------------------------------------- tablas
w("## 4. Definición de las tablas")
w("")
for grupo in GRUPOS:
    tablas = [t for t, d in MODELO.items() if d["grupo"] == grupo]
    if not tablas:
        continue
    w(f"### 4.{GRUPOS.index(grupo) + 1} {grupo} ({len(tablas)})")
    w("")
    for tabla in tablas:
        d = MODELO[tabla]
        marca = " · **NUEVA**" if d.get("nueva") else ""
        w(f"#### `{tabla}`{marca}")
        w("")
        w(d["proposito"])
        w("")
        w("| Columna | Tipo | Clave | Referencia | Obligatoria | Nota |")
        w("|---|---|---|---|---|---|")
        for c in d["columnas"]:
            clave = "PK" if c.get("pk") else ""
            ref = f"`{c['ref']}`" + (" · IsPartOf" if c.get("es_parte_de") else "") if c.get("ref") else ""
            obl = "Sí" if c.get("obligatoria") else ""
            nota = c.get("nota", "")
            if c.get("valor_inicial"):
                nota = (nota + ". " if nota else "") + f"Valor inicial: `{c['valor_inicial']}`"
            if c.get("alias_justificado"):
                nota = (nota + ". " if nota else "") + c["alias_justificado"]
            w(f"| `{c['nombre']}` | {c['tipo']} | {clave} | {ref} | {obl} | {nota} |")
        w("")

# ------------------------------------------------------------------- reglas
w("## 5. Reglas y automatizaciones")
w("")
for r in REGLAS:
    destino = f"`{r['tabla']}`" + (f".`{r['columna']}`" if r["columna"] != "(tabla)" else "")
    w(f"### {r['id']} · {r['tipo']} sobre {destino}")
    w("")
    w(r["descripcion"])
    w("")
    w("```")
    w(r["expresion"])
    w("```")
    if r.get("mensaje_error"):
        w("")
        w(f"Mensaje de error: `{r['mensaje_error']}`")
    w("")
    w(f"Cubre: {r['cubre']}")
    w("")

# --------------------------------------------------------------- validacion
w("## 6. Validación automática")
w("")
w("El modelo se comprueba con `python scripts/validar_modelo.py`, que aplica dieciséis reglas:")
w("")
w("| Regla | Comprueba |")
w("|---|---|")
for rid, desc in [
    ("V-01", "Cada tabla tiene una clave primaria única, de tipo texto y terminada en `ID`"),
    ("V-02", "Todos los tipos declarados existen en AppSheet"),
    ("V-03", "Ninguna columna está declarada dos veces en la misma tabla"),
    ("V-04", "Toda referencia apunta a una tabla que existe"),
    ("V-05", "La referencia se llama como la clave destino, o declara un alias justificado"),
    ("V-06", "Ninguna tabla queda huérfana: o referencia, o es referenciada, o es hoja con IsPartOf"),
    ("V-07", "La evidencia se almacena solo en las tablas hijas, nunca embebida"),
    ("V-08", "`IsPartOf` solo se declara sobre columnas de tipo `Ref`"),
    ("V-09", "Toda tabla declara grupo y propósito"),
    ("V-10", "Las reglas apuntan a tablas y columnas que existen"),
    ("V-11", "Las rutas de desreferencia son navegables, incluido el cambio de contexto en `SELECT()`"),
    ("V-12", "Lo declarado como retirado no sigue vivo en el modelo"),
    ("V-13", "Cada flujo funcional tiene la columna que lo soporta"),
    ("V-14", "Todo renombrado aterriza en una columna que existe, y avisa si reutiliza el nombre viejo"),
    ("V-15", "Toda referencia declara de dónde sale: renombrado, retipado o columna nueva"),
    ("V-16", "Lo retipado coincide en tipo y destino con lo que declara el modelo"),
]:
    w(f"| {rid} | {desc} |")
w("")
w("**V-11 es la regla que habría evitado el defecto raíz del modelo actual:** comprueba que")
w("`DISTANCE([Coordenadas_Cierre], [OTID].[ActivoID].[Ubicacion])` sea navegable. Contra el modelo")
w("en producción falla, porque `OTID` es texto y no referencia. Esa comprobación, hecha en su")
w("momento, habría ahorrado meses.")
w("")

# ------------------------------------------------------------------ despliegue
w("## 7. Orden de despliegue")
w("")
w("**No es *Regenerate Structure* sobre la aplicación anterior.** Ese camino se intentó y no")
w("converge: *Regenerate* fusiona en vez de reemplazar y conserva las columnas viejas a propósito.")
w("La aplicación se **reconstruye desde cero** sobre la hoja generada del modelo.")
w("")
w("1. **Copia de respaldo manual** del Sheets. No se toca nada sin ella.")
w("2. Generar la hoja del modelo y verificarla hasta `FASE A CERRADA`, sin pestañas ocultas.")
w("3. Crear la aplicación nueva y dar de alta las tablas, con su clave en `Text`.")
w("4. Cablear las referencias, empezando por las claves de destino. **Es el paso crítico.**")
w("5. Reponer las reglas RG-01 a RG-20 y los filtros de seguridad.")
w("6. Ocultar en la aplicación lo que la hoja de origen traiga de más, si se heredó una hoja.")
w("7. Ejercitar la aplicación con las pruebas de aceptación.")
w("")
w("El paso a paso, con la ficha de cada tabla, está en `MANUAL_DESPLIEGUE.md`, también generado.")
w("")
w("---")
w("*Documento generado. Para modificarlo, edita `scripts/modelo_objetivo.py` y ejecuta")
w("`python scripts/generar_doc_arquitectura.py`.*")

with open(SALIDA, "w", encoding="utf-8") as f:
    f.write("\n".join(L) + "\n")
print("Generado:", SALIDA)
print(f"{len(MODELO)} tablas, {n_cols} columnas, {n_refs} referencias, {len(REGLAS)} reglas")
