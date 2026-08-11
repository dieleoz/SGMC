# -*- coding: utf-8 -*-
"""Donde vive cada cosa en el editor de AppSheet. El mapa de clics.

Por que existe
--------------
Los encargos decian QUE poner -tabla, columna, propiedad, expresion- y no DONDE.
Y el editor no es evidente: `Required_If` no se llama asi en pantalla, esta
detras de un icono `=` dentro de una seccion plegada llamada `Require?`; un bot
que anade una fila no se configura en el bot; y `Security Filter` esta a tres
pliegues de profundidad.

El resultado fue que cada paso necesitaba que alguien tradujera el encargo a
clics, y en esa traduccion se colaron los errores del dia: la condicion de RG-03
acabo en `Valid If` en vez de en `Require?`, y el bot de RG-10 dio vueltas por
pantallas de plantilla PDF.

Esto no es documentacion de AppSheet: es lo que se vio en pantalla el
2026-08-10, con los nombres literales de los controles.
"""
import sys

# Donde se abre cada clase de cosa, y por que camino.
RUTAS = {
    "columna": (
        "Data > Columns > <tabla>",
        "El lapiz ✏️ a la izquierda del nombre abre el panel de la columna. Se "
        "cierra con `Done`, abajo a la derecha del panel."),
    "tabla": (
        "Data > Tables > <tabla>",
        "Despliega `Table settings`. `Are updates allowed` esta arriba; "
        "`Security filter` esta mas abajo, dentro de `Security`."),
    "bot": (
        "Automation > Bots",
        "El icono del rayo en el menu izquierdo. `Create a new Bot`."),
    "accion": (
        "Data > Actions",
        "`Add Action`. Aqui se define QUE fila se crea y con que valores."),
    }

# Dentro del panel de una columna, en que seccion vive cada propiedad.
# El orden es el que aparece en pantalla, de arriba abajo.
SECCIONES_COLUMNA = [
    ("Show?", "si la columna se ve en la aplicacion"),
    ("Type", "el tipo. Es un <select> nativo del navegador"),
    ("Type Details", "lo que depende del tipo: `Source table` de una Ref, los "
                     "valores de un Enum, la longitud de un Text"),
    ("Data Validity", "**`Valid If`**, **`Invalid value error`** y **`Require?`**"),
    ("Auto Compute", "**`App formula`**, **`Initial value`** y `Suggested values`"),
    ("Update Behavior", "**`Editable?`** -que es donde vive `Editable_If`- y "
                        "`Reset on edit?`"),
    ("Display", "**`Label`**, `Display name` y `Description`"),
    ("Other Properties", "`Searchable`, `Scannable`, `NFC` y `Sensitive data`"),
    ]

# Como se llama en pantalla lo que el modelo llama de otra forma. Es donde se
# pierde la gente: el nombre de la regla no es el nombre del control.
COMO_SE_LLAMA = {
    "Valid_If": ("Data Validity > Valid If",
                 "y el mensaje va en `Invalid value error`, justo debajo"),
    "Required_If": ("Data Validity > Require?",
                    "**no es una casilla que se marque**: hay que pulsar el "
                    "icono `=` que hay al lado para escribir la expresion. "
                    "El 2026-08-10 acabo escrita en `Valid If`, que la habria "
                    "vuelto imposible de guardar"),
    "App formula": ("Auto Compute > App formula", "**escribe en la hoja**"),
    "Initial value": ("Auto Compute > Initial value",
                      "solo se aplica a filas NUEVAS; el usuario puede "
                      "cambiarla despues salvo que `Editable?` lo impida"),
    "Editable_If": ("Update Behavior > Editable?",
                    "el icono `=` al lado de la casilla"),
    "Label": ("Display > Label",
              "exige que `Show?` este activo, y solo puede haber UNA por tabla"),
    "Key": ("la casilla `Key` en la lista de columnas, no dentro del panel",
            "sobre una tabla VACIA, AppSheet no deja marcarla si la columna no "
            "tiene `Initial value` que genere la clave"),
    "Security Filter": ("Data > Tables > <tabla> > Table settings > Security > "
                        "Security filter", ""),
    "Are updates allowed": ("Data > Tables > <tabla> > Table settings",
                            "tres casillas: `Updates`, `Adds`, `Deletes`"),
    }

# Un bot tiene tres partes, y la tercera es la que atasca.
BOT = """
`Automation > Bots` → `Create a new Bot`, y tres partes:

  Event       la tabla + `Data change type`: Adds, Updates, Adds and Updates.
              O `Schedule` si es programado, con su cadencia
  Condition   una expresion que decide si sigue
  Step        `Add a step` → lo que hace

**La trampa del `Step`.** Si lo que hace es ANADIR UNA FILA a otra tabla, no se
configura dentro del bot: AppSheet interpreta que quieres generar un documento y
pide plantilla PDF y valores de retorno. Van dos sitios, en este orden:

  1. `Data > Actions` → `Add Action`
       For a record of this table  = la tabla de origen
       Do this = **Data: add a new row to another table using values from this row**
       Table to add to = la tabla destino, y los valores de cada columna

  2. `Automation > Bots` → tu bot → `Add a step` → **`Run a data action`**,
     y eliges la que acabas de crear
"""

# ------------------- el editor puede mostrarte tipos que ya no son los que hay
#
# Si arriba aparece el aviso «A newer version of the app exists», lo que ves en
# `Data > Columns` puede ser **cache**, no el estado real. Se descubrio el
# 2026-08-11 cotejando tipos: sin recargar en duro, OT_OrdenesTrabajo mostraba
# nueve columnas como `Text` cuando ya estaban puestas.
#
# El dano no es que se vea mal: es que quien coteja **reporta tipos falsos**, y
# lo hace de buena fe y con la pantalla delante. Un cotejo a ojo es la unica
# evidencia que existe para los tipos -la API devuelve filas, no esquema-, asi
# que una lectura sobre cache contamina justo lo que no se puede recuperar.
#
# Antes de cotejar nada: **Ctrl+Shift+R**.
CACHE_DEL_EDITOR = (
    "Si el editor muestra «A newer version of the app exists», recarga en duro "
    "con Ctrl+Shift+R ANTES de leer ningun tipo. Lo que hay en pantalla puede "
    "ser cache, y un cotejo sobre cache reporta tipos falsos con toda la "
    "confianza del mundo.")

SENAL_DE_GUARDADO = """
**El boton `SAVE` de la cabecera pasa de gris a AZUL** cuando el editor recoge un
cambio, y vuelve a gris al guardar. Ese ciclo -gris, azul, gris- es la senal.

Si sigue gris, **el cambio no llego al modelo interno** y se pierde al recargar.
No basta con haber cambiado el valor del control.
"""


def mapa_markdown():
    """El mapa entero, para meterlo en un encargo."""
    L = ["### Dónde está cada cosa en el editor", "",
         "Los nombres de las reglas **no son** los nombres de los controles. Ahí es donde se pierde",
         "la gente, y ahí se coló más de un error del 2026-08-10.", "",
         "| Lo que dice el encargo | Dónde está en pantalla |", "|---|---|"]
    for k, (donde, nota) in COMO_SE_LLAMA.items():
        L.append("| `%s` | %s%s |" % (k, donde, " — %s" % nota if nota else ""))
    L += ["", "**Dentro del panel de una columna**, las secciones van en este orden:", ""]
    for nombre, que in SECCIONES_COLUMNA:
        L.append("- **`%s`** — %s" % (nombre, que))
    L += ["", "### Antes de leer nada: recarga en duro", "", CACHE_DEL_EDITOR,
          "", "### Los bots", BOT, "### Cómo saber que quedó guardado", SENAL_DE_GUARDADO]
    return "\n".join(L)


if __name__ == "__main__":
    # La consola de Windows es cp1252 y no puede imprimir las flechas del mapa.
    # Se escribe a stdout con reconfigure en vez de recortar el contenido: el
    # documento es para leerse, no para caber en una terminal.
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    print(mapa_markdown())
