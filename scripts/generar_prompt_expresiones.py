# -*- coding: utf-8 -*-
"""Genera docs/PROMPT_EXPRESIONES.md: el encargo de la Fase C.

Por que existe
--------------
Las 21 reglas estaban en sdd/RECONSTRUCCION_EXPRESIONES.md, que es un documento
de RECONSTRUCCION: cuenta que expresion habia y por que, no como ponerla. Quien
lo abria para ejecutar no encontraba ni el orden, ni de que depende cada una, ni
en que tabla hay que estar. Y eso se paga: el 2026-08-10 se intento cablear el
geofencing tres veces, dos de ellas con consejos que proponian REESCRIBIR la
expresion para que el error desapareciera -un LOOKUP global que habria colapsado
los tres radios distintos en uno, y quitar un salto hacia una columna que no
existe-. Las dos habrian dejado el cierre en campo aceptando lo que debe
rechazar, sin dar error.

Lo que aporta y el otro no tenia
--------------------------------
  1. **Que referencias atraviesa cada expresion.** Una expresion con puntos no
     falla por estar mal escrita: falla porque un salto de la cadena no esta
     cableado. Aqui cada regla lleva su cadena desglosada, asi que el error
     dice donde mirar en vez de invitar a reescribirla.
  2. **En que tabla hay que estar.** El mismo nombre -EstadoActivoID- es la
     CLAVE de EST_Activo y la REFERENCIA hacia ella en ACT_Activos. Ponerlo mal
     produce la referencia ciclica que AppSheet rechaza, y ya paso.
  3. **El orden.** Lo que escribe en la hoja va al final, cuando ya se puede
     comprobar que escribio.

Uso:  python scripts/generar_prompt_expresiones.py
"""
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "scripts"))

from modelo_objetivo import MODELO, REGLAS
from sistema import APP_NOMBRE, APP_URL
from lectura_de_vuelta import bloque
from navegacion_editor import mapa_markdown

SALIDA = os.path.join(RAIZ, "docs", "PROMPT_EXPRESIONES.md")

L = []
w = L.append

# Que columna es Ref y hacia donde, para desglosar las cadenas de puntos.
ref_de = {(t, c["nombre"]): c["ref"]
          for t in MODELO for c in MODELO[t]["columnas"] if c.get("ref")}
# Que nombres son clave en una tabla y referencia en otra: los que se prestan
# al clic en la tabla equivocada.
es_clave = {c["nombre"]: t for t in MODELO for c in MODELO[t]["columnas"] if c.get("pk")}


def _ambito(expresion):
    """Los tramos de la expresion donde manda OTRA tabla.

    SELECT(ASG_AsignacionZona[UnidadFuncionalID], AND([UsuarioID]...)) cambia el
    contexto: dentro de ese SELECT, [UsuarioID] es de ASG_AsignacionZona, no de
    la tabla de la regla. Sin esto, RG-04 salia como "SIN CABLEAR" -y un falso
    positivo en un encargo ejecutable manda a alguien a arreglar lo que no esta
    roto, que es peor que no avisar-.
    """
    tramos = []
    for m in re.finditer(r"\b(?:SELECT|FILTER|ANY|COUNT|MAXROW|MINROW)\s*\(\s*(\w+)\[", expresion):
        tabla = m.group(1)
        if tabla not in MODELO:
            continue
        hondo, fin = 0, None
        for i in range(m.end() - len(tabla) - 1, len(expresion)):
            if expresion[i] == "(":
                hondo += 1
            elif expresion[i] == ")":
                hondo -= 1
                if hondo == 0:
                    fin = i
                    break
        tramos.append((m.start(), fin if fin is not None else len(expresion), tabla))
    return tramos


def cadenas(tabla, expresion):
    """Las cadenas de saltos entre tablas, cada una por separado.

    `[OTID].[ActivoID].[Ubicacion_LatLong]` desde MAN_Mantenimientos es UNA
    cadena de dos saltos. `[TecnicoID].[Correo]` y `[SupervisorID].[Correo]` son
    DOS cadenas de un salto cada una, y concatenarlas leia
    "USR_Usuarios -> USR_Usuarios", que no significa nada.

    El ultimo corchete no es un salto: es la columna que se lee al final.
    """
    tramos = _ambito(expresion)
    salida, vistas = [], set()
    for m in re.finditer(r"(?:\[\w+\]\s*\.\s*)+\[\w+\]", expresion):
        nombres = re.findall(r"\[(\w+)\]", m.group(0))
        aqui = next((t for ini, fin, t in tramos if ini <= m.start() <= fin), tabla)
        saltos = []
        for n in nombres[:-1]:
            destino = ref_de.get((aqui, n))
            saltos.append((aqui, n, destino))
            if not destino:
                break
            aqui = destino
        clave = tuple(saltos)
        if saltos and clave not in vistas:
            vistas.add(clave)
            salida.append(saltos)
    return salida


# Lo que ESCRIBE en la hoja va al final: hasta que no se puede comprobar que
# escribio, no conviene soltarlo sobre 368 filas.
# Una columna VIRTUAL no escribe: la calcula AppSheet y no toca la hoja. Estaba
# clasificada entre las que escriben solo por ser App formula, y con eso el
# encargo mandaba tomar una instantanea antes de poner algo que no puede tocar
# un dato.
def _escribe(r):
    if r["tipo"] == "App formula" and r.get("columna") == "(tabla)":
        return False
    return r["tipo"] in ("App formula", "Bot", "Bot programado", "Initial value")


ESCRIBEN = ("App formula", "Bot", "Bot programado", "Initial value")

# Los Security Filter van al final del todo, DESPUES incluso de las que
# escriben: en cuanto entran, la API deja de devolver las filas de esa tabla y
# ni instantanea.py ni auditar_cableado.py pueden volver a comprobar nada ahi.
# Poner un filtro es apagar la luz de la habitacion en la que estas trabajando.
ULTIMAS = ("Security Filter",)
orden = sorted(REGLAS, key=lambda r: (r["tipo"] in ULTIMAS,
                                     _escribe(r), r["id"]))

con_cadena = [(r, cadenas(r["tabla"], r.get("expresion") or "")) for r in orden]
atraviesan = [(r, c) for r, c in con_cadena if c]

w("# Encargo de las expresiones — Fase C")
w("")
w("**Autocontenido. Cópialo íntegro desde la línea siguiente.**")
w("")
w("**Generado** por `scripts/generar_prompt_expresiones.py`. No editar a mano: las expresiones y")
w("las cadenas de referencias salen de `scripts/modelo_objetivo.py`.")
w("")
w("---")
w("")
w("Vas a poner **%d reglas** en la aplicación **`%s`** de Google AppSheet." % (len(REGLAS), APP_NOMBRE))
w("Las %d referencias son el paso anterior. **Este documento no sabe si están puestas** —sale del"
  % len(ref_de))
w("modelo, así que describe el destino—. Compruébalo antes de empezar:")
w("")
w("```bash")
w("python scripts/auditar_cableado.py")
w("```")
w("")
w("Si no sale con **0 correcciones**, para: una expresión con puntos sobre una referencia sin cablear")
w("falla, y el error te va a mandar a mirar la expresión en vez del cableado.")
w("")
w("```")
w("%s" % APP_URL)
w("```")
w("")

w(mapa_markdown())
w("")
w("## Lo primero, porque ya salió mal tres veces")
w("")
w("**Una expresión con puntos no falla por estar mal escrita. Falla porque un salto de su cadena no")
w("está cableado.**")
w("")
w("El error de AppSheet lo dice literalmente. Cuando `RG-01` daba")
w("`Can't find column \"RadioGeofencingKm\" in table \"SED_Sedes\"`, no había que buscar otro nombre")
w("de columna: había que ver por qué la cadena aterrizaba en `SED_Sedes`. Y era que")
w("`ACT_Activos.TipoActivoID` apuntaba a la tabla de sedes.")
w("")
w("> **NO reescribas una expresión para que el error desaparezca.** Se propusieron dos veces dos")
w("> arreglos que parecían razonables: sustituir el radio por un `LOOKUP` a `PAR_Parametros`, y")
w("> quitar un salto de la cadena. El primero habría colapsado en un solo número los **tres radios**")
w("> distintos —1,5 km para la fibra óptica, 0,05 km para un poste SOS—, y el segundo apunta a una")
w("> columna que no existe. Ninguno de los dos da error: dejan el cierre en campo **aceptando lo que")
w("> debe rechazar**.")
w("")
w("Si una expresión falla, mira la tabla que nombra el error y búscala en la columna **«atraviesa»**")
w("de la tabla de abajo. Ahí está el salto roto.")
w("")

w("## Lo segundo: en qué tabla estás")
w("")
w("El mismo nombre es **clave** en una tabla y **referencia** en otra. `EstadoActivoID` es la clave")
w("de `EST_Activo` y la referencia hacia ella en `ACT_Activos`. Editarlo en la tabla equivocada")
w("produce esto:")
w("")
w("```")
w("Column Name 'EstadoActivoID' in Schema 'EST_Activo_Schema'")
w("contains a cyclical table reference to 'EST_Activo'.")
w("```")
w("")
w("Ya pasó el 2026-08-10. **Antes de tocar una columna, comprueba en qué tabla estás.** Cada regla")
w("de abajo dice la suya, y no es negociable: la misma columna en otra tabla es otra cosa.")
w("")

w("## Las %d reglas" % len(REGLAS))
w("")
w("Cada una: entra a la **tabla**, abre la **columna**, y pon la expresión en la **propiedad** que")
w("dice. Las que **escriben en la hoja** van al final a propósito.")
w("")
w("| # | Regla | Tabla | Columna | Propiedad | Atraviesa |")
w("|---|---|---|---|---|---|")
for i, (r, c) in enumerate(con_cadena, 1):
    saltos = " · ".join(
        " → ".join("`%s`" % (d or "**SIN DECLARAR**") for _t, _n, d in ruta)
        for ruta in c) or "—"
    w("| %d | `%s` | `%s` | `%s` | `%s` | %s |"
      % (i, r["id"], r["tabla"], r.get("columna") or "—", r["tipo"], saltos))
w("")
w("> Las de `App formula`, `Initial value` y las de tipo bot **escriben**. Ponerlas antes de haber")
w("> comprobado las demás significa soltarlas sobre el inventario entero sin saber qué escriben.")
w(">")
w("> **Y los dos `Security Filter` van los últimos de todos.** En cuanto entran, la API deja de")
w("> devolver las filas de esa tabla —llama sin usuario, así que `USEREMAIL()` queda en blanco— y")
w("> ni `instantanea.py` ni `auditar_cableado.py` pueden volver a comprobar nada ahí. Ponerlos")
w("> antes es apagar la luz de la habitación en la que estás trabajando.")
w("")

_bots = [r for r in REGLAS if r["tipo"].startswith("Bot")]
w("## Los %d bots no van en una columna, y esto es lo que faltaba" % len(_bots))
w("")
w("Las otras %d se ponen en una propiedad de una columna o de una tabla. **Un bot no.** Vive en"
  % (len(REGLAS) - len(_bots)))
w("`Automation > Bots` —el icono del rayo— y tiene tres partes, no una expresión suelta:")
w("")
w("```")
w("Event       cuando se dispara:  la tabla + Adds / Updates / Adds and Updates,")
w("                                o Schedule si es programado")
w("Condition   una expresion que decide si sigue")
w("Step        lo que hace")
w("```")
w("")
w("La tabla de arriba da el **Event** en la columna de la expresión y la **Condition** en el detalle.")
w("El `Step` lo dice la descripción de cada regla.")
w("")
w("### La trampa: un bot que AÑADE UNA FILA se hace en dos sitios")
w("")
w("Si el `Step` es *añadir una fila a otra tabla*, **no se configura dentro del bot**. AppSheet")
w("interpreta que quieres generar un documento y te pide una plantilla PDF y valores de retorno, y")
w("ahí es donde se atasca todo el mundo.")
w("")
w("El orden es este:")
w("")
w("1. **`Data > Actions` → `Add Action`.** Ahí se define *qué fila se crea y con qué valores*:")
w("   `For a record of this table` = la tabla de origen, y `Do this` = **`Data: add a new row to")
w("   another table using values from this row`**.")
w("2. **`Automation > Bots` → tu bot → `Add a step` → `Run a data action`**, y eliges la que")
w("   acabas de crear.")
w("")
# Quienes crean filas se derivan de la descripcion de la regla, no de una lista
# escrita a mano. La habia -«RG-10 y RG-12»- y ESPEC-006 retira RG-12: el texto
# habria seguido mandando configurar un bot que ya no existe.
_crean = sorted(r["id"] for r in REGLAS
                if r["tipo"].startswith("Bot")
                and any(x in (r.get("descripcion") or "").lower()
                        for x in ("genera una orden", "genera las ordenes",
                                  "crear una orden", "anade una fila")))
if _crean:
    w("Afecta a %s, %s." % (" y a ".join("`%s`" % x for x in _crean),
      "que es la que crea órdenes" if len(_crean) == 1
      else "que son las %d que crean órdenes" % len(_crean)))
    w("")
# Este aviso decia «no pongas RG-10 ni RG-12: OTID no tiene generador». Era
# cierto, y ESPEC-005 lo resolvio: OTID paso a UNIQUEID(). Estaba escrito a mano,
# asi que habria sobrevivido a su propia solucion y seguido prohibiendo algo ya
# permitido. Se deriva.
from modelo_objetivo import CLAVE_GENERADA as _CG
if "OT_OrdenesTrabajo" not in _CG:
    w("> **Y un aviso que vale más que el procedimiento:** un bot que crea filas en")
    w("> `OT_OrdenesTrabajo` tiene un problema abierto. `OTID` es clave legible y **nadie la**")
    w("> **genera**, así que la fila nacería sin identificador y AppSheet la descarta sin decir")
    w("> nada. **No pongas %s en producción hasta que se resuelva.**" % " ni ".join("`%s`" % x for x in _crean))
else:
    w("> **`%s` ya se pueden poner.** `OTID` era clave legible y nadie la generaba, así que la fila"
      % "` y `".join(_crean))
    w("> nacía sin identificador y AppSheet la descartaba en silencio. `ESPEC-005` lo resolvió:")
    w("> `OT_OrdenesTrabajo` está en `CLAVE_GENERADA` y su clave sale de `UNIQUEID()`.")
    w(">")
    w("> Lo que sí sigue abierto es **cuándo dispararlos**: crean órdenes, y con eso pueblan una")
    w("> tabla que hoy está en cero. Ver `ENCARGO_VENTANA.md`.")
w("")

w("## Las expresiones, enteras")
w("")
w("**Cópialas de aquí. No las escribas de memoria ni las adaptes.**")
w("")
for r, c in con_cadena:
    w("### %s — `%s.%s`" % (r["id"], r["tabla"], r.get("columna") or ""))
    w("")
    w("**%s**%s" % (r["tipo"], (" · cubre `%s`" % r["cubre"]) if r.get("cubre") else ""))
    w("")
    if r.get("expresion"):
        w("```")
        w(r["expresion"])
        w("```")
        w("")
    if r.get("descripcion"):
        w("%s" % r["descripcion"])
        w("")
    if c:
        # Dos cadenas de la misma expresion comparten prefijo -RG-01 recorre
        # [OTID].[ActivoID] dos veces- y contarlo dos veces daria "5
        # referencias" donde hay 3. Lo que se enumera son los saltos DISTINTOS,
        # que es lo que hay que ir a comprobar.
        saltos, vistos = [], set()
        for ruta in c:
            for salto in ruta:
                if salto not in vistos:
                    vistos.add(salto)
                    saltos.append(salto)
        w("Atraviesa **%d %s**:" % (len(saltos),
          "referencia" if len(saltos) == 1 else "referencias distintas"))
        w("")
        for t, n, d in saltos:
            w("- `%s.%s` → `%s`%s" % (t, n, d or "?",
              "  ← **este salto no está declarado en el modelo**" if not d else ""))
        w("")
        w("Si el error nombra una de esas tablas y no es la que toca, el fallo está en ese salto,")
        w("no en la expresión.")
        w("")

w("## Cómo se comprueba, y por qué depende de ti")
w("")
w(bloque("expresiones"))
w("")
w("## Dos que hoy NO se pueden poner, y hay que saberlo antes de intentarlo")
w("")
w("**`RG-02` es imposible tal como está declarada.** Usa `USERLOCATIONACCURACY()`, y esa función")
w("**no existe en AppSheet**: la plataforma no expone la precisión del GPS al motor de expresiones.")
w("La captura manual sí muestra al técnico los metros en pantalla, pero ese número no se puede")
w("guardar en una columna. Deja `Precision_GPS` con tipo `Number` y **sin `Initial value`**.")
w("")
w("Y arrastra dos más, así que no las des por buenas aunque las pongas:")
w("")
w("```")
w("RG-02   Precision_GPS = USERLOCATIONACCURACY()       no existe -> nunca se puebla")
w("RG-19   CierreConExcepcion = Precision_GPS > umbral   blanco > numero -> siempre falso")
w("RG-03   MotivoExcepcion obligatorio si excepcion      nunca se pide")
w("```")
w("")
w("Tres reglas bien configuradas y el mecanismo entero inerte. **Está pendiente de decidir** si")
w("`CierreConExcepcion` pasa a ser una casilla que marca el técnico; hasta entonces, ponlas y no las")
w("cuentes como funcionando.")
w("")
w("> Es el patrón del día: una regla puede estar puesta, bien escrita, sin dar un solo error, y no")
w("> hacer nada. Pasó por el tipo (`RG-03`), por el dato (`RG-06`, con `GeneraAlerta` vacía) y aquí")
w("> por una función que no existe. `python scripts/verificar_datos.py` caza el segundo caso —G-05—;")
w("> los otros dos solo se ven mirando.")
w("")

w("## Al terminar")
w("")
w("Antes de dar por buena ninguna:")
w("")
w("```bash")
w("python scripts/auditar_cableado.py      # que las %d referencias sigan donde estaban" % len(ref_de))
w("python scripts/validar_modelo.py        # que ninguna regla compare un Ref con un literal")
w("```")
w("")
w("La segunda existe por un motivo concreto. Comparar una columna `Ref` con un texto —")
w("`[EstadoActivoID] <> \"Retirado\"`— **es siempre falso y no da error**: la referencia guarda")
w("`EST-04`, no la palabra. Hay que escribir `[EstadoActivoID].[Nombre]`.")
w("")
w("Reporta: qué reglas pusiste, cuáles dieron error y **con qué texto exacto**, y qué tabla nombraba")
w("cada error. Ese texto es el diagnóstico, no un estorbo.")
w("")

w("## Lo que NO debes hacer")
w("")
w("- **No reescribas una expresión para silenciar un error.** Es la regla de arriba y es la que más")
w("  veces se ha roto.")
w("- **No pruebes expresiones escribiéndolas dentro de una columna.** Se prueban en el Asistente de")
w("  Expresiones, que solo evalúa, y se cierra **sin dar a `Done`**.")
w("- **No cambies ninguna referencia.** Están puestas y auditadas. Si una está mal, se reporta.")
w("- **No publiques.** Ninguna coordenada está levantada en campo: se derivan del PK sobre el")
w("  trazado, así que la comprobación de distancia todavía no significa nada en la vía.")

with open(SALIDA, "w", encoding="utf-8") as f:
    f.write("\n".join(L) + "\n")

print("Generado:", SALIDA)
print("%d reglas · %d atraviesan referencias · %d escriben en la hoja"
      % (len(REGLAS), len(atraviesan), sum(1 for r in REGLAS if _escribe(r))))
