# -*- coding: utf-8 -*-
"""Genera docs/sdd/RECONSTRUCCION_EXPRESIONES.md desde el modelo.

La version anterior de este documento truncaba tres expresiones con '...',
entre ellas el Security Filter de ACT_Activos. Y era el documento que el manual
senala como "si solo lee uno, que sea este". Aqui no se trunca nada.

Uso:  python scripts/generar_reconstruccion.py
"""
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "scripts"))
from catalogo_tipos import TIPOS_ACTIVO
from modelo_objetivo import (MODELO, REGLAS, RENOMBRADOS, CAMPOS_RETIRADOS,
                             COLUMNAS_SIN_DECIDIR)

L = []
w = L.append

w("# Reconstruccion de la capa de expresiones — lista de reposicion")
w("")
w("**Generado de `scripts/modelo_objetivo.py`.** Es lo que tiene que existir en la aplicacion.")
w("**Ninguna expresion esta truncada**: se copian y se pegan enteras.")
w("")
def reparto_radios():
    """El reparto de radios, derivado del catalogo. Nunca escrito a mano."""
    from collections import Counter
    c = Counter(t[7] for t in TIPOS_ACTIVO)
    return " · ".join("%s km en %d" % (k, n) for k, n in sorted(c.items()))


w("## 1. Los nombres viejos, y por que la lista NO se aplica en bloque")
w("")
w("La Fase A renombro columnas en la hoja. Toda expresion que cite un nombre viejo quedo rota.")
w("")
w("> **Cuidado: cinco de estos nombres siguen VIVOS en otras tablas.** El mapeo solo vale **tabla por")
w("> tabla**. Un buscar-y-reemplazar global rompe `SED_Sedes` y `MAN_Mantenimientos`.")
w("")
w("| Tabla | Nombre viejo | Nombre correcto | Aviso |")
w("|---|---|---|---|")
vivos = {}
for t, d in MODELO.items():
    for c in d["columnas"]:
        vivos.setdefault(c["nombre"], []).append(t)
for tabla, mapa in sorted(RENOMBRADOS.items()):
    for viejo, (nuevo, _) in sorted(mapa.items()):
        otras = [x for x in vivos.get(viejo, []) if x != tabla]
        aviso = "**Sigue vivo en %s**" % ", ".join("`%s`" % x for x in otras[:3]) if otras else ""
        w("| `%s` | `%s` | `%s` | %s |" % (tabla, viejo, nuevo, aviso))
w("")
w("**El caso que mas engana:** en `OT_OrdenesTrabajo` conviven `ActivoID` —la referencia al activo—")
w("y `Activo` —la bandera Si/No—. Una formula que diga `Activo` **no da error**: apunta a la bandera")
w("y devuelve lista vacia.")
w("")
w("## 2. Las %d reglas, con su expresion completa" % len(REGLAS))
w("")
for r in REGLAS:
    w("### %s — `%s`%s" % (r.get("id"), r.get("tabla"),
                           " · `%s`" % r["columna"] if r.get("columna") else ""))
    w("")
    w("**Tipo:** %s%s" % (r.get("tipo"), " · cubre %s" % r["cubre"] if r.get("cubre") else ""))
    w("")
    # Una regla App formula sobre "(tabla)" es una COLUMNA VIRTUAL, y sin decirlo
    # este documento no sirve para lo que existe: rehacer el cableado tras un
    # Delete-and-re-add. Emitia el identificador y la expresion, y con eso no se
    # puede reconstruir nada -falta el nombre de la columna, que sea virtual, y
    # que lleva el Label-.
    # El nombre y el Label los declara la REGLA, no los supone este generador.
    # Los suponia -«se llama Etiqueta y lleva Label»- porque las dos primeras
    # virtuales eran etiquetas. ESPEC-006 propone una tercera, EstaVencida, que
    # no es etiqueta: la suposicion habria emitido dos instrucciones falsas.
    if r.get("tipo") == "App formula" and r.get("columna") == "(tabla)":
        _nombre = r.get("nombre_virtual", "(sin nombre declarado)")
        w("> **Es una COLUMNA VIRTUAL, no una columna de la hoja.** Se crea con")
        w("> *Data > Columns > `Add virtual column`*, se llama **`%s`**, y lleva esa expresión"
          % _nombre)
        w("> en su `App formula`.")
        if r.get("es_label"):
            w("> ")
            w("> Y además **`Show?` activo** y **`Label` marcado**. Si la tabla ya tenía otra")
            w("> columna con `Label`, se desmarca primero: solo puede haber una.")
        w("")
    exp = str(r.get("expresion", "")).strip()
    if exp:
        w("```")
        w(exp)
        w("```")
        w("")
    # Se emite `descripcion` y no solo `nota`, y la diferencia no era cosmetica:
    # NINGUNA de las 23 reglas tiene `nota` -todas usan `descripcion`-, asi que este
    # bloque no se ejecuto nunca desde que existe, y este documento jamas llego a
    # explicar una sola regla.
    #
    # Lo destapo ORDEN-008. La condicion 1 de su dictamen exigia meter la instruccion
    # «cablear DESPUES del Initial value» dentro de `descripcion` PARA QUE LLEGARA A
    # QUIEN CABLEA, y quien cablea lee justo este documento: aqui la regla salia como
    # «Tipo: Editable_If, FALSE» y nada mas. Sin esto el operador la pega en Editable?
    # sin tocar Initial value, y ningun tecnico puede guardar una fotografia.
    _texto = r.get("descripcion") or r.get("nota")
    if _texto:
        w("> %s" % _texto.replace(chr(10), " "))
        w("")
    # RG-01 desreferencia una columna que puede estar vacia, y contra vacio la
    # comparacion rechaza TAMBIEN el cierre legitimo. La expresion es la de
    # arriba y no tiene variante: lo que hay que comprobar es que la columna
    # este poblada, y eso se deriva del archivo, no se supone.
    if r.get("id") == "RG-01":
        w("**Antes de pegarla, compruebe que el radio esta poblado.** Esta regla desreferencia")
        w("`TIP_TiposActivo.RadioGeofencingKm`. **Si esa columna esta vacia, la comparacion se hace")
        w("contra blanco y rechaza tambien el cierre legitimo**: fallarian las dos pruebas del par,")
        w("la que debe aceptar y la que debe rechazar, y la tanda dejaria de discriminar.")
        w("")
        w("```bash")
        w("python scripts/verificar_faseA.py \"BD/Modelo_Datos_PLANTILLA.xlsx\"")
        w("```")
        w("")
        w("En la hoja vigente estan **poblados los %d**, con %s. Un literal en su lugar "
          "-por ejemplo `<= 1.0`- hace que el sistema pruebe \"estas en el corredor\" en vez de "
          "\"estas frente al equipo\", que es su proposito." % (len(TIPOS_ACTIVO), reparto_radios()))
        w("")
w("## 3. Las claves, todas `Text`")
w("")
w("| Tabla | Clave |")
w("|---|---|")
for t, d in sorted(MODELO.items()):
    pk = [c["nombre"] for c in d["columnas"] if c.get("pk")]
    if pk:
        w("| `%s` | `%s` |" % (t, pk[0]))
w("")
w("## 4. Las %d referencias"
  % sum(1 for d in MODELO.values() for c in d["columnas"] if c.get("ref")))
w("")
w("**Son las del modelo, no las 15 de `ESPEC-002`.** Aquellas eran las que faltaban en la aplicacion")
w("anterior; en una construida de cero no sobrevive ninguna.")
w("")
w("| Tabla | Columna | `Ref` a | `IsPartOf` |")
w("|---|---|---|---|")
for t, d in sorted(MODELO.items()):
    for c in d["columnas"]:
        if c.get("ref"):
            w("| `%s` | `%s` | `%s` | %s |"
              % (t, c["nombre"], c["ref"], "**SI**" if c.get("es_parte_de") else "no"))
w("")
w("## 5. Lo que NO se repone: columnas retiradas")
w("")
claves = {c["nombre"]: t for t, d in MODELO.items() for c in d["columnas"] if c.get("pk")}
n_ret = sum(len(v) for v in CAMPOS_RETIRADOS.values()) + len(COLUMNAS_SIN_DECIDIR)
w("**%d columnas.** Siguen en la hoja a proposito. En la aplicacion: tipo `Text`, `Show?`" % n_ret)
w("desmarcado, sin formula. **No se borran.**")
w("")
w("| Tabla | Columna | Por que | |")
w("|---|---|---|---|")
for t, campos in sorted(CAMPOS_RETIRADOS.items()):
    for c, motivo in sorted(campos.items()):
        tr = "**TRAMPA -> `%s`**" % claves[c] if c in claves and claves[c] != t else ""
        w("| `%s` | `%s` | %s | %s |" % (t, c, motivo, tr))
for (t, c), motivo in sorted(COLUMNAS_SIN_DECIDIR.items()):
    w("| `%s` | `%s` | %s | **SIN DECIDIR** |" % (t, c, motivo))
w("")
n_tr = len([1 for t, campos in CAMPOS_RETIRADOS.items() for c in campos
            if c in claves and claves[c] != t])
w("**Las %d marcadas TRAMPA** se llaman igual que la clave de otra tabla, asi que **AppSheet las" % n_tr)
w("convierte a `Ref` sola**. Hay que deshacerlo.")
w("")
w("---")
w("*Generado. Para actualizarlo, cambie `modelo_objetivo.py` y vuelva a generar.*")

salida = os.path.join(RAIZ, "docs", "sdd", "RECONSTRUCCION_EXPRESIONES.md")
with open(salida, "w", encoding="utf-8") as f:
    f.write("\n".join(L) + "\n")
print("Generado:", salida)
print("%d reglas sin truncar, %d referencias, %d columnas retiradas"
      % (len(REGLAS), sum(1 for d in MODELO.values() for c in d["columnas"] if c.get("ref")), n_ret))
