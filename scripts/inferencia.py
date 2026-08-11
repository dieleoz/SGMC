# -*- coding: utf-8 -*-
"""Como consigue cada columna su tipo en AppSheet. Un solo sitio.

Por que existe
--------------
`MODELO` declara `tipo` con la misma apariencia con la que declara `nombre`, y
no son lo mismo: **`nombre` se cumple solo** -lo escribe generar_plantilla.py en
la cabecera de la hoja- mientras que **`tipo` es un deseo que alguien tiene que
ir a instalar a mano en el editor**. Guardados en el mismo diccionario, con el
mismo aspecto, el segundo parece un hecho.

De ahi salio el fallo del 2026-08-10. `docs/PROMPT_CABLEADO.md` titulaba su
paso 3 «Los tipos que no se infieren» y enumeraba 61 columnas: una LISTA BLANCA
DE EXCEPCIONES sobre un default presunto-correcto. Las otras 150 se daban por
buenas por omision. La plataforma garantiza lo contrario, y el resultado fue
`RG-03` puesta sobre una columna `Text` que el modelo declara `Yes/No`:
comparar texto contra el booleano TRUE es siempre falso, asi que la regla
existe, esta bien escrita y no hace nada.

Y el «que reportar» del encargo cerraba el bucle en falso: «cualquier tipo que
encontraras distinto del que dice este documento». **El ejecutor no puede
reportar una diferencia contra un valor que nunca se le dio.**

Que resuelve este modulo
------------------------
Convierte la seccion 13 de la base de conocimiento -que era CONOCIMIENTO, y por
eso no evito nada- en algo que los generadores CONSUMEN. Se escribio a las
14:33 y a las 15:44 se genero el encargo que omitia 150 columnas: no fue olvido,
es que ningun generador podia leerla.

Aqui se responde una sola pregunta por columna: **quien consigue este tipo.**
"""
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "scripts"))

from modelo_objetivo import MODELO

# ------------------------------------------------- tipos que NADIE puede inferir
#
# Ningun valor de celda los establece: no hay nada que se pueda escribir en la
# hoja para que AppSheet elija Ref o Enum. Sembrar datos no los alcanza, y por
# eso el remedio «declarar un valor de siembra por columna» se queda corto en
# estas 67 -el 32% del modelo-.
#
# Con Ref ademas hay una razon de fondo para NO intentarlo: el prefijo de tabla
# rompe el parecido de nombre a proposito. Es el coste de la convencion y a la
# vez su proteccion: sin el, AppSheet convertiria en referencia cualquier
# columna que se parezca a una tabla.
NUNCA_INFERIBLE = {
    "Ref": "ningun contenido produce una referencia, y el prefijo de tabla rompe "
           "el parecido de nombre a proposito",
    "Enum": "el contenido no declara el conjunto de valores permitidos",
    "LongText": "indistinguible de Text por contenido",
    "ChangeTimestamp": "lo escribe el servidor; por contenido no se distingue de "
                       "una fecha cualquiera",
    "Image": "la celda solo lleva un nombre de archivo",
    "Signature": "igual que Image",
    }

# --------------------------------------------- lo que AppSheet lee DEL NOMBRE
#
# Cada entrada dice: patron, a que tipo lo lleva, y DE DONDE SABEMOS que lo
# hace. La procedencia va explicita porque mezclarlas fue parte del problema:
#
#   documentado  esta en la documentacion oficial de AppSheet (13)
#   observado    lo vimos ocurrir en esta aplicacion, con fecha
#   supuesto     nos lo parece y no esta comprobado
#
# `ubicacion` NO esta aqui: el propio repositorio registro que no dispara nada
# -de ahi que `Ubicacion` saliera `Text` y hubiera que renombrarla-.
GATILLOS_NOMBRE = [
    (r"latlong|geolocation", "LatLong", "documentado",
     "13, tabla de palabras reconocidas"),
    (r"gps", "LatLong", "observado",
     "Precision_GPS salio LatLong el 2026-08-10 estando su tabla VACIA: no pudo "
     "ser el contenido"),
    (r"birthday|dob|\b(day|month|year)\b", "Date", "documentado", "13"),
    (r"fecha", "Date o DateTime", "observado",
     "ACT_Activos.FechaBaja salio DateTime estando vacia en las 368"),
    (r"\?$|^(is|has)[A-Z]", "Yes/No", "documentado", "13"),
    ]

# --------------------------------------------------------------- el bloque ciego
#
# 38 columnas Yes/No -el 18% del modelo- y NINGUNA cumple un gatillo documentado:
# no acaban en `?` ni empiezan por `is`/`has`. Que AppSheet las tipe Yes/No
# depende de que lea TRUE/FALSE en el contenido, y eso no esta en 13 ni lo hemos
# visto ocurrir aqui.
#
# Se declara como supuesto en vez de callarlo. 27 de las 38 las nombra alguna
# regla, y RG-04 y RG-16 solas cabalgan sobre las 24 columnas `Activo`.
SUPUESTO_BOOLEANO = (
    "supuesto sin verificar: que el contenido TRUE/FALSE produzca Yes/No no "
    "esta en la documentacion ni lo hemos observado. Si falla, la columna sale "
    "Text y toda comparacion contra TRUE es siempre falsa, sin dar error")


def como_se_consigue(tabla, col):
    """Devuelve (quien, motivo). `quien` es 'a mano', 'nombre' o 'contenido'."""
    tipo, nombre = col["tipo"], col["nombre"]

    if tipo in NUNCA_INFERIBLE:
        return "a mano", NUNCA_INFERIBLE[tipo]

    for patron, lleva, fuente, ref in GATILLOS_NOMBRE:
        if not re.search(patron, nombre, re.I):
            continue
        if lleva.split()[0] == tipo or tipo in lleva.split(" o "):
            return "nombre", "su nombre lo dispara (%s: %s)" % (fuente, ref)
        return "a mano", ("su nombre dispara la inferencia a %s y NO lo es "
                          "(%s: %s)" % (lleva, fuente, ref))

    if tipo == "Yes/No":
        return "a mano", SUPUESTO_BOOLEANO

    return "contenido", "AppSheet deberia acertar leyendo los valores"


def clasificar():
    """Las 211 columnas repartidas por quien consigue su tipo."""
    salida = {"a mano": [], "nombre": [], "contenido": []}
    for t in MODELO:
        for c in MODELO[t]["columnas"]:
            quien, motivo = como_se_consigue(t, c)
            salida[quien].append((t, c, motivo))
    return salida


if __name__ == "__main__":
    r = clasificar()
    total = sum(len(v) for v in r.values())
    print("COMO CONSIGUE SU TIPO CADA UNA DE LAS %d COLUMNAS" % total)
    print("")
    for quien in ("a mano", "nombre", "contenido"):
        print("  %-10s %3d" % (quien, len(r[quien])))
    print("")
    print("Las de 'a mano' NO las consigue nadie si el encargo no las nombra.")
    print("El 2026-08-10 el encargo nombraba 61 y habia %d." % len(r["a mano"]))
