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
# depende enteramente de que lea TRUE/FALSE en el contenido.
#
# **Verificado a medias el 2026-08-10** contrastando el .xlsx contra los datos
# vivos: 28 de las 38 devuelven Y/N por la API, y eso es lo que devuelve una
# columna Yes/No -una Text devolveria el literal TRUE-. Las 10 restantes estan en
# tablas VACIAS, asi que no hay contenido del que inferir, y ahi es exactamente
# donde fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto.
#
# Se quedan en "a mano" a proposito. Que 28 hayan salido bien no las convierte en
# seguras: salieron bien por una heuristica que nadie nos garantiza, y el coste
# de mirarlas es un vistazo mientras el de equivocarse es una regla decorativa.
SUPUESTO_BOOLEANO = (
    "no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el "
    "contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que "
    "es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas "
    "vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 "
    "sin efecto (S-30)")


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


# ------------------------------------------------------ la etiqueta, que nadie declaraba
#
# `Label` es la columna que representa una fila en las listas y en los
# desplegables. **No la declaraba ni el modelo ni ningun documento**: la elegia
# AppSheet, y elige la primera columna de texto, que casi siempre es la clave.
#
# Nadie lo miraba porque no rompe nada: la aplicacion funciona igual. Lo que
# pasa es que el tecnico abre el desplegable de un activo y ve `ACT-0001`,
# `ACT-0002`, `ACT-0003` en vez de `Poste SOS-001`. Veinte tablas son destino de
# alguna referencia; USR_Usuarios lo es de seis, asi que quien asigna una orden
# elige entre `USR-001` y `USR-004`.
#
# Es el ejemplo mas limpio del patron: un atributo que el repositorio da por
# supuesto y la plataforma decide. Ninguno de los ocho verificadores puede verlo
# -la API devuelve filas, no esquema-, asi que lo unico que cabe es decir cual
# debe ser y que alguien lo compruebe.
ETIQUETAS = ("Nombre", "Nombres", "Pregunta", "Descripcion")

# Las transaccionales NO tienen etiqueta natural, y no es un hueco: una orden o
# un mantenimiento se identifican por su clave y su fecha, no por un nombre. Se
# declaran aqui para que quede dicho que se decidio, no que se olvido.
# ESPEC-005: OT_OrdenesTrabajo sale de aqui. Su motivo era «se identifica por su
# numero», y ese numero paso a ser un UNIQUEID(): dejo de identificar nada ante
# una persona.
SIN_ETIQUETA_NATURAL = {
    "MAN_Mantenimientos": "una ejecucion se identifica por su orden y su hora",
    "CHK_Checklists": "un checklist se identifica por su mantenimiento",
    }


# La etiqueta que NO es una columna de la hoja, sino una columna virtual que
# AppSheet calcula. Es la salida que documenta Google para una etiqueta
# compuesta de varias columnas -«Add a virtual column… enter a CONCATENATE()
# expression»- y la que ESPEC-005 adopta.
#
# Va en un diccionario aparte y no en ETIQUETAS a proposito: se probo anadir
# "Etiqueta" a esa tupla y NO FUNCIONA, porque etiqueta_de() solo mira MODELO y
# una columna virtual no esta ahi. El plan original se corrigio por ejecucion,
# no por lectura.
ETIQUETA_VIRTUAL = {
    "OT_OrdenesTrabajo": "Etiqueta",
    "PLA_PlanMantenimiento": "Etiqueta",
    }


def etiqueta_de(tabla):
    """Que columna deberia ser el Label. None si su clave es la identificacion."""
    if tabla in ETIQUETA_VIRTUAL:
        return ETIQUETA_VIRTUAL[tabla]
    if tabla in SIN_ETIQUETA_NATURAL:
        return None
    cols = [c["nombre"] for c in MODELO[tabla]["columnas"]]
    return next((n for n in ETIQUETAS if n in cols), None)


def etiquetas_pendientes():
    """Las tablas destino de alguna referencia, con la etiqueta que les toca."""
    destinos = {c["ref"] for t in MODELO for c in MODELO[t]["columnas"] if c.get("ref")}
    cuantas = {}
    for t in MODELO:
        for c in MODELO[t]["columnas"]:
            if c.get("ref"):
                cuantas[c["ref"]] = cuantas.get(c["ref"], 0) + 1
    return sorted(((t, etiqueta_de(t), cuantas.get(t, 0)) for t in destinos),
                  key=lambda x: -x[2])


# ------------------------------- que columnas virtuales hay, y cuales son etiqueta
#
# Cuatro generadores repetian la misma heuristica -«App formula sobre (tabla) es
# una columna virtual, se llama Etiqueta y lleva Label»- y solo dos se
# corrigieron cuando dejo de ser cierta. El quinto parche habria sido el
# siguiente generador que alguien escriba.
#
# La heuristica era correcta mientras las unicas virtuales fueran etiquetas.
# ESPEC-006 propone EstaVencida, que es virtual y NO es etiqueta: con la forma
# sola, el encargo de la ventana emitia dos filas llamadas «Etiqueta» sobre la
# misma tabla, una de ellas con la expresion equivocada.
#
# Aqui se responde una vez y la leen todos. Es la misma leccion que
# alcance_reglas.py: lo que varios consumidores deducen por su cuenta, acaba
# deduciendose distinto.
def columnas_virtuales(reglas):
    """Las (regla, nombre) de toda columna virtual declarada."""
    return [(r, r.get("nombre_virtual") or "(sin nombre declarado)")
            for r in reglas
            if r.get("tipo") == "App formula" and r.get("columna") == "(tabla)"]


def etiquetas_virtuales(reglas):
    """Solo las que ademas hacen de Label. No toda virtual lo es."""
    return [(r, n) for r, n in columnas_virtuales(reglas) if r.get("es_label")]
