# -*- coding: utf-8 -*-
"""Prueba negativa de auditar_cableado.py: que caza lo que dice cazar.

Por que existe
--------------
`auditar_cableado.py` se usa como criterio de aceptacion del cableado: "sale
con 0 correcciones cuando esta bien". El arquitecto senalo que ese criterio se
puede satisfacer SIN ARREGLAR NADA, porque las tres formas de sacar una
referencia del recuento no exigen que este bien:

  - vaciar su tabla destino la mueve a "ciega"
  - una caida de la API la movia a "ausente" (ya corregido: ahora aborta)
  - y si nadie mira, un 0 se lee como un aprobado

Un verificador que solo se ha visto pasar no esta probado. Este script le mete
defectos a proposito y comprueba que los caza. Es la misma disciplina con la
que se probo verificar_reproducible reintroduciendo la no idempotencia, y la
que fallo el dia que verificar_datos "salio con codigo 1" por un crash y se
tomo por una deteccion.

Que NO hace
-----------
No toca la aplicacion ni la red. Sustituye la lectura de la API por tablas
inventadas, que es lo unico que permite fabricar un defecto sin romper nada
real. Lo que se prueba es el RAZONAMIENTO del auditor, no su conexion.

Uso:  python scripts/probar_auditor.py
Sale con codigo 1 si alguno de los casos no se comporta como debe.
"""
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "scripts"))

from modelo_objetivo import MODELO

# La misma logica de clasificacion que usa el auditor, sobre datos de mentira.
# Se copia a proposito en vez de importarse: el auditor lee de la red al
# importarse, y una prueba que necesita credenciales para correr no se corre.
declarado = {(t, c["nombre"]): c["ref"]
             for t in MODELO for c in MODELO[t]["columnas"] if c.get("ref")}


def clasificar(inversas_por_destino, vacias):
    """Reproduce el veredicto del auditor a partir de columnas virtuales."""
    real, atribuida = {}, set()
    for destino, columnas in inversas_por_destino.items():
        for col in columnas:
            if not col.startswith("Related "):
                continue
            resto = col[len("Related "):]
            txt, sufijo = resto.split(" By ", 1) if " By " in resto else (resto, None)
            origen = next((t for t in MODELO
                           if txt in (t, t + "s", t.rstrip("s"))), None)
            if not origen:
                continue
            if sufijo:
                nombre, directa = sufijo, True
            else:
                cand = [c["nombre"] for c in MODELO[origen]["columnas"]
                        if c.get("ref") == destino]
                nombre, directa = (cand[0], False) if len(cand) == 1 else (None, False)
            if nombre:
                real[(origen, nombre)] = destino
                if directa:
                    atribuida.add((origen, nombre))
    juzgable = {k: v for k, v in declarado.items() if v not in vacias}
    return {
        "mal": [k for k, v in juzgable.items() if k in real and real[k] != v],
        "faltan": [k for k in juzgable if k not in real],
        "sobran": [k for k in real if k not in declarado],
        "probadas": [k for k, v in juzgable.items()
                     if real.get(k) == v and k in atribuida],
        "compatibles": [k for k, v in juzgable.items()
                        if real.get(k) == v and k not in atribuida],
        }


# Todas las tablas del modelo con sus inversas correctas, como punto de partida.
def escenario_sano():
    inv = {}
    for (origen, col), destino in declarado.items():
        cuantas = sum(1 for c in MODELO[origen]["columnas"] if c.get("ref") == destino)
        etiqueta = ("Related %s By %s" % (origen, col) if cuantas > 1
                    else "Related %s" % origen)
        inv.setdefault(destino, set()).add(etiqueta)
    return {t: sorted(inv.get(t, set())) for t in MODELO}


ancho = "=" * 78
print(ancho)
print("PRUEBA NEGATIVA DEL AUDITOR DE CABLEADO")
print(ancho)
print("Se le meten defectos a proposito y se comprueba que los caza.")
print("")

fallos = []


def caso(titulo, resultado, condicion, explicacion):
    ok = condicion(resultado)
    print("  %s %s" % ("ok  " if ok else "FALLA", titulo))
    if not ok:
        fallos.append("%s -- %s" % (titulo, explicacion))
        print("        %s" % explicacion)


# --------------------------------------------------------------- 1. sano
base = escenario_sano()
r = clasificar(base, vacias=[])
caso("un cableado correcto no produce correcciones",
     r, lambda x: not (x["mal"] or x["faltan"] or x["sobran"]),
     "da correcciones sobre un cableado sano: %s" % r)

# ------------------------------------------- 2. una Ref apunta a otra tabla
#
# El defecto real del 2026-08-10: TipoActivoID apuntando a SED_Sedes.
malo = {t: list(v) for t, v in base.items()}
malo["TIP_TiposActivo"] = [x for x in malo["TIP_TiposActivo"]
                           if "ACT_Activos" not in x]
malo["SED_Sedes"] = malo["SED_Sedes"] + ["Related ACT_Activos By TipoActivoID"]
r = clasificar(malo, vacias=[])
caso("caza una Ref que apunta a la tabla equivocada",
     r, lambda x: ("ACT_Activos", "TipoActivoID") in x["mal"],
     "no vio TipoActivoID -> SED_Sedes")

# ----------------------------- 3. una columna de texto convertida en Ref
sobra = {t: list(v) for t, v in base.items()}
sobra["SED_Sedes"] = sobra["SED_Sedes"] + ["Related ACT_Activos By CodigoQR"]
r = clasificar(sobra, vacias=[])
caso("caza una columna de texto convertida en Ref",
     r, lambda x: ("ACT_Activos", "CodigoQR") in x["sobran"],
     "no vio CodigoQR como Ref indebida")

# ------------------------------------------------- 4. una Ref que falta
falta = {t: list(v) for t, v in base.items()}
falta["UNF_UnidadesFuncionales"] = [x for x in falta["UNF_UnidadesFuncionales"]
                                    if "ACT_Activos" not in x]
r = clasificar(falta, vacias=[])
caso("caza una Ref declarada y ausente",
     r, lambda x: ("ACT_Activos", "UnidadFuncionalID") in x["faltan"],
     "no vio que falta UnidadFuncionalID")

# ------------------ 5. LO QUE NO DEBE HACER: dar por buena la que no ve
#
# El criterio "0 correcciones" no puede satisfacerse vaciando el destino. Con
# UNF vacia, la referencia sale del recuento -es correcto, no se puede leer-,
# pero NO puede aparecer como correcta.
r = clasificar(falta, vacias=["UNF_UnidadesFuncionales"])
caso("con el destino vacio, NO la cuenta como correcta",
     r, lambda x: ("ACT_Activos", "UnidadFuncionalID")
     not in x["probadas"] + x["compatibles"] + x["faltan"],
     "una referencia invisible se colo en el recuento")

# ------------- 6. sin ' By ', la columna no esta probada aunque coincida
#
# El hallazgo del arquitecto: sin desambiguacion, atribuir la columna es
# preguntarselo al modelo. Tiene que quedar como compatible, nunca como
# verificada.
r = clasificar(base, vacias=[])
caso("sin ' By ', la Ref queda compatible y no verificada",
     r, lambda x: ("ACT_Activos", "UnidadFuncionalID") in x["compatibles"]
     and ("ACT_Activos", "UnidadFuncionalID") not in x["probadas"],
     "atribuyo la columna sin que la aplicacion la nombrara")

print("")
print(ancho)
if fallos:
    for f in fallos:
        print("  x %s" % f)
    print(ancho)
    print("EL AUDITOR NO CAZA LO QUE DICE CAZAR")
    print(ancho)
    sys.exit(1)
print("EL AUDITOR CAZA LOS 6 CASOS")
print("Su '0 correcciones' significa algo, y su 'verificada' no se regala.")
print(ancho)
