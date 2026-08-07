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
from modelo_objetivo import MODELO, GRUPOS, RETIRADAS, CAMPOS_RETIRADOS, REGLAS

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
w("Este documento define el sistema que se va a construir, no el que existe. El actual está")
w("descrito en `AUDITORIA_PLAN_Y_ROADMAP.md` y no sirve como base: sus referencias no están")
w("cableadas, cuatro tablas están vacías y la cadena relacional existe solo en el papel.")
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
w("### 2.3 Campos que se retiran de `MAN_Mantenimientos`")
w("")
w("La tabla pasaba de 25 columnas heterogéneas a un registro de ejecución limpio.")
w("")
w("| Campo | Motivo |")
w("|---|---|")
for campo, motivo in CAMPOS_RETIRADOS.get("MAN_Mantenimientos", {}).items():
    w(f"| `{campo}` | {motivo} |")
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
w("El modelo se comprueba con `python scripts/validar_modelo.py`, que aplica trece reglas:")
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
w("1. **Copia de respaldo manual** de la aplicación y del Sheets. No se toca nada sin ella.")
w("2. Crear las tablas nuevas y sus columnas en el Sheets.")
w("3. *Regenerate Structure* de cada tabla afectada en AppSheet.")
w("4. Tipar las columnas y cablear las referencias. **Este es el paso crítico.**")
w("5. Migrar los datos existentes al modelo nuevo.")
w("6. Retirar tablas y campos obsoletos, ya sin datos vivos.")
w("7. Configurar las reglas RG-01 a RG-10.")
w("8. Poblar con datos de prueba y ejercitar la aplicación.")
w("9. Construir los reportes.")
w("")
w("El detalle está en `prompts/PROMPT_CONSTRUCCION_SGMC.md`.")
w("")
w("---")
w("*Documento generado. Para modificarlo, edita `scripts/modelo_objetivo.py` y ejecuta")
w("`python scripts/generar_doc_arquitectura.py`.*")

with open(SALIDA, "w", encoding="utf-8") as f:
    f.write("\n".join(L) + "\n")
print("Generado:", SALIDA)
print(f"{len(MODELO)} tablas, {n_cols} columnas, {n_refs} referencias, {len(REGLAS)} reglas")
