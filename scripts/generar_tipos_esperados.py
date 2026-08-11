# -*- coding: utf-8 -*-
"""Genera docs/TIPOS_ESPERADOS.md: que tipo debe tener cada columna en el editor.

Por que existe
--------------
AppSheet infiere el tipo de cada columna de DOS senales -el nombre y el
contenido- y ninguna de las dos es fiable aqui:

  - Sin contenido cae en Text. Ocho tablas llegaron VACIAS, asi que sus
    columnas enteras se tiparon a ciegas. Y en las tablas pobladas pasa lo
    mismo con cada columna vacia.
  - Con contenido, el NOMBRE puede mandar sobre el dato. Es la senal que se
    aprovecho a proposito al renombrar a `_LatLong`, y el 2026-08-10 mordio al
    reves: `Precision_GPS` -que es un Number, los metros de precision- salio
    LatLong porque su nombre lleva GPS.

Nada de esto lo ve ningun script del repositorio. **La API v2 devuelve filas,
no esquema**: no hay forma de preguntarle de que tipo es una columna. Se mira
en el editor, columna por columna, y este documento es la lista contra la que
mirar.

Lo que costo no tenerla
-----------------------
`RG-03` quedo puesta y bien escrita -`[CierreConExcepcion] = TRUE` en
Required_If- sobre una columna que AppSheet tipo Text. Comparar texto contra el
booleano TRUE es SIEMPRE falso y no da error: el motivo de excepcion no se pide
nunca, y el tecnico cierra con excepcion sin justificar. La regla existe, esta
bien redactada, y no hace nada.

Uso:  python scripts/generar_tipos_esperados.py
"""
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "scripts"))

from modelo_objetivo import MODELO, REGLAS
from sistema import APP_NOMBRE

SALIDA = os.path.join(RAIZ, "docs", "TIPOS_ESPERADOS.md")
FOTO = os.path.join(RAIZ, "BD", "instantaneas", "antes-de-fase-c.json")

# Palabras que AppSheet reconoce en el NOMBRE y con las que decide el tipo por
# su cuenta, mande lo que mande el contenido. Documentadas en
# BASE_CONOCIMIENTO_APPSHEET.md 13.
#
# El prefijo de Yes/No va SIN ignorar mayusculas a proposito: con re.I,
# `EstadoActivoID` casa con "Es"+"t" y sale marcada como booleana, que es un
# falso positivo. Y un falso positivo en una lista de 93 columnas para revisar a
# mano no es ruido inocente: gasta la atencion justo donde hace falta.
GATILLOS = [
    (r"latlong|geolocation|gps|ubicacion|coordenada", "LatLong", re.I),
    (r"birthday|dob|fecha|day|month|year", "Date o DateTime", re.I),
    (r"^(es|tiene|requiere|permite|aplica)[A-Z_]|\?$", "Yes/No", 0),
    (r"correo|email", "Email", re.I),
    (r"telefono|phone", "Phone", re.I),
    ]

datos = {}
if os.path.exists(FOTO):
    datos = json.load(open(FOTO, encoding="utf-8"))

# Que columnas toca alguna regla: son las que fallan en silencio si el tipo esta
# mal, porque la expresion sigue siendo valida y devuelve algo.
#
# Por (tabla, columna). Atribuir por nombre suelto daba las 23 columnas `Activo`
# con RG-04 y RG-16 encima, y esta es la columna que ordena el trabajo.
from alcance_reglas import por_columna
tocadas = por_columna()

L = []
w = L.append


def riesgo(tabla, col):
    """Por que AppSheet pudo equivocarse con esta columna."""
    n, tipo = col["nombre"], col["tipo"]
    filas = datos.get(tabla)
    motivos = []
    if datos and not filas:
        motivos.append("la tabla llegó **vacía**: el tipo se eligió sin un solo dato")
    elif filas is not None:
        llenas = sum(1 for f in filas if str(f.get(n, "")).strip())
        if llenas == 0:
            motivos.append("la columna está **vacía en las %d filas**" % len(filas))
    for patron, cual, banderas in GATILLOS:
        if re.search(patron, n, banderas) and not tipo.startswith(cual.split()[0]):
            motivos.append("su nombre dispara la inferencia a **%s**, y no lo es" % cual)
            break
    return motivos


w("# Qué tipo debe tener cada columna")
w("")
w("**Generado** por `scripts/generar_tipos_esperados.py`. No editar a mano.")
w("")
w("---")
w("")
w("Esta lista existe porque **ningún script del repositorio puede comprobarla**. La API v2 de")
w("AppSheet devuelve **filas, no esquema**: no hay forma de preguntarle de qué tipo es una columna.")
w("Se mira en `Data > Columns`, columna por columna, contra esto.")
w("")
w("## Por qué AppSheet se equivoca, y cómo")
w("")
w("Infiere el tipo de **dos** señales, y aquí las dos fallan:")
w("")
w("- **Sin contenido cae en `Text`.** Ocho tablas llegaron vacías, así que sus columnas enteras se")
w("  tiparon a ciegas. En las tablas pobladas pasa igual con cada columna vacía.")
w("- **Con contenido, el nombre puede mandar sobre el dato.** Es la señal que aprovechamos al")
w("  renombrar a `_LatLong` — y que mordió al revés: **`Precision_GPS` salió `LatLong`** porque su")
w("  nombre lleva `GPS`, cuando son los metros de precisión, un `Number`.")
w("")
w("> **Lo que cuesta no mirarlo.** `RG-03` quedó puesta y bien escrita —`[CierreConExcepcion] = TRUE`")
w("> en `Required_If`— sobre una columna que AppSheet tipó `Text`. Comparar texto contra el booleano")
w("> `TRUE` es **siempre falso y no da error**: el motivo de excepción no se pide nunca, y el técnico")
w("> cierra con excepción sin justificar. La regla existe, está bien redactada, y no hace nada.")
w("")

sospechosas = []
for t in MODELO:
    for c in MODELO[t]["columnas"]:
        m = riesgo(t, c)
        if m:
            sospechosas.append((t, c, m))

w("## Empieza por estas %d" % len(sospechosas))
w("")
w("Son las que AppSheet tuvo que adivinar. **El resto también hay que mirarlo**, pero si el tiempo")
w("es poco, aquí está donde se concentra el error.")
w("")
w("| Tabla | Columna | Debe ser | Reglas que la usan | Por qué pudo salir mal |")
w("|---|---|---|---|---|")
for t, c, m in sospechosas:
    reglas = tocadas.get((t, c["nombre"]), set())
    w("| `%s` | `%s` | **`%s`** | %s | %s |"
      % (t, c["nombre"], c["tipo"],
         ", ".join("`%s`" % x for x in sorted(reglas)) if reglas else "—",
         "; ".join(m)))
w("")
w("> **La columna «reglas que la usan» es la que ordena el trabajo.** Una columna con el tipo mal y")
w("> sin ninguna regla encima molesta al usuario. Una columna con el tipo mal y una regla encima")
w("> **rompe la regla en silencio**, que es lo que no se puede permitir.")
w("")

w("## Todas, tabla por tabla")
w("")
for t in sorted(MODELO):
    filas = datos.get(t)
    estado = ("**tabla vacía: todos sus tipos se eligieron a ciegas**" if datos and not filas
              else "%d filas" % len(filas) if filas is not None else "")
    w("### `%s`%s" % (t, " — %s" % estado if estado else ""))
    w("")
    w("| Columna | Tipo | |")
    w("|---|---|---|")
    for c in MODELO[t]["columnas"]:
        extra = []
        if c.get("pk"):
            extra.append("**clave**")
        if c.get("ref"):
            extra.append("→ `%s`" % c["ref"])
        if c.get("obligatoria"):
            extra.append("obligatoria")
        if c.get("valores"):
            extra.append("valores: %s" % " · ".join("`%s`" % v for v in c["valores"]))
        w("| `%s` | **`%s`** | %s |" % (c["nombre"], c["tipo"], " · ".join(extra)))
    w("")

w("## Al terminar")
w("")
w("No hay comando que cierre esto. Lo único que se puede hacer es dejar constancia: **anota qué tipo")
w("tenía cada una antes de cambiarla**. Si mañana algo se comporta raro, esa lista es la única forma")
w("de saber si lo tocamos nosotros.")
w("")
w("Y lo que sí se puede comprobar después, porque un cambio de tipo puede disparar una escritura:")
w("")
w("```bash")
w("python scripts/instantanea.py guardar despues-de-los-tipos")
w("python scripts/instantanea.py comparar antes-de-fase-c despues-de-los-tipos")
w("```")

with open(SALIDA, "w", encoding="utf-8") as f:
    f.write("\n".join(L) + "\n")

print("Generado:", SALIDA)
print("%d columnas en total · %d sospechosas de estar mal tipadas"
      % (sum(len(MODELO[t]["columnas"]) for t in MODELO), len(sospechosas)))
