# -*- coding: utf-8 -*-
"""Compara el cableado REAL de la aplicacion contra el que declara el modelo.

Por que existe
--------------
El 2026-08-10 se cablearon las referencias en el editor y el informe decia
"39/39 asignadas a su Source table correspondiente". No era cierto: dos
apuntaban a la tabla equivocada, tres columnas que son Text se habian
convertido en Ref, y cuatro no estaban puestas.

Nada lo detectaba. validar_modelo daba APTO, la API daba 28/28 y las 368 filas
seguian ahi. Es la regla R-04 en su forma mas pura: **una referencia que
resuelve puede apuntar a lo que no es**, y preguntar "apunta a algo" nunca
contesta "apunta a lo correcto".

Como lo averigua sin poder leer el esquema
------------------------------------------
La API v2 devuelve FILAS, no esquema: no hay forma de preguntarle de que tipo
es una columna. Pero cuando se crea una Ref, AppSheet anade a la tabla DESTINO
una columna virtual inversa llamada `Related <Origen>` o, si hay mas de una
referencia entre el mismo par, `Related <Origen> By <Columna>`.

Esas columnas virtuales SI viajan en las filas. Asi que el grafo de referencias
se reconstruye leyendo los nombres de columna de cada tabla poblada. Es una
lectura indirecta y hay que decirlo: lo que se mide es la consecuencia de la
referencia, no la referencia.

El agujero, dicho en voz alta
-----------------------------
La columna virtual vive en el DESTINO. Si el destino esta vacio, la API no
devuelve ninguna fila y por tanto ningun nombre de columna: de esas
referencias este script NO PUEDE DECIR NADA. No las da por buenas ni por malas,
las separa. Confundir "no lo puedo ver" con "esta bien" es como se llego aqui.

No toca la APLICACION: usa solo la accion Find, no escribe ni borra en ella.
Si escribe en el REPOSITORIO: reemite docs/CORRECCIONES_CABLEADO.md con lo que
quede pendiente. Correrlo cambia ese archivo en disco.

Uso:  python scripts/auditar_cableado.py
Sale con codigo 1 si alguna referencia visible no coincide con el modelo.
"""
import json
import os
import sys
import urllib.error
import urllib.request

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "scripts"))

from modelo_objetivo import MODELO
from sistema import APP_ID, APP_NOMBRE

# La clave nunca se escribe aqui ni en ningun documento: vive en .env, que esta
# en .gitignore. Sin ella el script no corre, y eso es lo correcto.
_env = os.path.join(RAIZ, ".env")
if os.path.exists(_env):
    for _l in open(_env, encoding="utf-8"):
        if "=" in _l and not _l.strip().startswith("#"):
            _k, _v = _l.split("=", 1)
            os.environ.setdefault(_k.strip(), _v.strip())

API_KEY = os.environ.get("APPSHEET_API_KEY", "")
if not API_KEY:
    print("Falta APPSHEET_API_KEY. Ponla en .env (que no se sube a git).")
    sys.exit(2)

URL = "https://api.appsheet.com/api/v2/apps/%s/tables/%s/Action"

# Las que no se pueden medir y ALGUIEN MIRO EN EL EDITOR.
#
# No convierte la referencia en verificada: una lectura visual no es una
# medicion, y por eso se guarda con fecha y con quien la hizo. Lo que hace es
# distinguir "nadie la ha mirado" de "se miro el dia tal", que es justo la
# diferencia que se paso por alto cuando se dio por bueno un "39/39 asignadas"
# que nadie habia comprobado.
#
# CADUCA sola: si la referencia se vuelve medible -porque su tabla destino deja
# de estar vacia- manda la medicion y esto sobra. Y si alguien vuelve a cablear,
# esta confirmacion habla de un estado anterior. Por eso lleva fecha.
CONFIRMADAS_A_OJO = {
    ("FOT_Fotografias", "MantenimientoID"): ("2026-08-10", "Diego, en el editor"),
    ("FIR_Firmas", "MantenimientoID"): ("2026-08-10", "Diego, en el editor"),
    ("CHK_Checklists", "MantenimientoID"): ("2026-08-10", "Diego, en el editor"),
    ("CHD_ChecklistDetalle", "ChecklistID"): ("2026-08-10", "Diego, en el editor"),
    ("MAN_Mantenimientos", "OTID"): ("2026-08-10", "Diego, en el editor"),
    ("OT_OrdenesTrabajo", "OTOrigenID"): ("2026-08-10", "Diego, en el editor"),
    }


def filas(tabla):
    pet = urllib.request.Request(
        URL % (APP_ID, tabla),
        json.dumps({"Action": "Find", "Properties": {}, "Rows": []}).encode(),
        {"ApplicationAccessKey": API_KEY, "Content-Type": "application/json"})
    try:
        cuerpo = urllib.request.urlopen(pet, timeout=30).read().decode()
    except urllib.error.URLError as e:
        return None, str(e)
    try:
        return json.loads(cuerpo or "[]"), None
    except ValueError:
        return [], None


def columna_de(origen, destino, sufijo):
    """Que columna del origen produjo esta virtual inversa, y con que fuerza.

    Devuelve (columna, atribuida). `atribuida` dice si la COLUMNA esta probada
    o solo supuesta, y la diferencia no es un matiz:

      con ' By '   AppSheet nombra la columna. Es prueba directa: por eso se
                   vio que ACT_Activos.TipoActivoID apuntaba a SED_Sedes.
      sin ' By '   AppSheet solo nombra la tabla, porque hay UNA sola
                   referencia entre el par. Para saber cual columna la
                   produjo hay que preguntarselo AL MODELO -y el modelo es
                   justo lo que estamos tratando de verificar-.

    Ese segundo caso es INFERENCIA CIRCULAR y hay que decirlo. Prueba "existe
    alguna referencia a ese destino", nunca "esta en esa columna". Si el
    ejecutor pusiera la referencia correcta en la columna equivocada, la
    inversa se llamaria igual y este script diria que esta bien.

    Y tiene una ironia que conviene tener presente: el metodo es mas fuerte
    cuando las cosas estan MAL -varias referencias al mismo destino obligan a
    AppSheet a desambiguar con ' By '- y mas debil cuando estan bien.
    """
    if sufijo:
        return sufijo, True
    cand = [c["nombre"] for c in MODELO[origen]["columnas"]
            if c.get("ref") == destino]
    return (cand[0], False) if len(cand) == 1 else (None, False)


def tabla_llamada(txt):
    return next((t for t in MODELO if txt in (t, t + "s", t.rstrip("s"))), None)


ancho = "=" * 78
print(ancho)
print("CABLEADO REAL DE LA APLICACION CONTRA EL MODELO")
print(ancho)
print("Aplicacion: %s" % APP_NOMBRE)
print("Lectura indirecta: se miden las columnas virtuales inversas, no el esquema.")
print("")

real, atribuida, vacias, caidas = {}, set(), [], []
for destino in sorted(MODELO):
    datos, error = filas(destino)
    if error:
        caidas.append((destino, error))
        continue
    if not datos:
        vacias.append(destino)
        continue
    for col in datos[0]:
        if not col.startswith("Related "):
            continue
        resto = col[len("Related "):]
        txt, sufijo = resto.split(" By ", 1) if " By " in resto else (resto, None)
        origen = tabla_llamada(txt)
        if not origen:
            continue
        nombre, directa = columna_de(origen, destino, sufijo)
        if nombre:
            real[(origen, nombre)] = destino
            if directa:
                atribuida.add((origen, nombre))

if caidas:
    # Una tabla que no responde no es una tabla sin referencias. Sin esto, sus
    # inversas no se leen, sus referencias caen en "declaradas y ausentes" y el
    # documento manda PONER una Ref que probablemente ya esta puesta. Una lectura
    # incompleta no produce un encargo incompleto: produce un encargo EQUIVOCADO,
    # y ese se ejecuta con la misma confianza que uno bueno.
    print("LECTURA INCOMPLETA. No se emite nada.")
    print("")
    for t, e in caidas:
        print("   ! %s no respondio: %s" % (t, e))
    print("")
    print("Vuelve a correrlo. Si insiste, mira si esa tabla existe en la aplicacion.")
    print(ancho)
    sys.exit(2)

declarado = {(t, c["nombre"]): c["ref"]
             for t in MODELO for c in MODELO[t]["columnas"] if c.get("ref")}

# Una referencia solo es JUZGABLE si su tabla destino tiene filas: la virtual
# inversa vive alli. Con el destino vacio no hay nada que leer.
juzgable = {k: v for k, v in declarado.items() if v not in vacias}
ciegas = {k: v for k, v in declarado.items() if v in vacias}

bien = [k for k, v in juzgable.items() if real.get(k) == v]
probadas = [k for k in bien if k in atribuida]
compatibles = [k for k in bien if k not in atribuida]
mal = [k for k, v in juzgable.items() if k in real and real[k] != v]
faltan = [k for k in juzgable if k not in real]
sobran = [k for k in real if k not in declarado]

n = 0
print("LAS CORRECCIONES, en el orden en que hay que hacerlas")
print("")

if sobran:
    print("A. Columnas que quedaron como Ref y en el modelo son otra cosa.")
    print("   Van PRIMERO: mientras esten mal, la tabla no deja guardar.")
    print("")
    for t, c in sorted(sobran):
        n += 1
        tipo = next((x["tipo"] for x in MODELO[t]["columnas"] if x["nombre"] == c), "?")
        print("   %d. %s.%s   Ref -> %s   =>   TYPE = %s"
              % (n, t, c, real[(t, c)], tipo))
    print("")

if mal:
    print("B. Referencias que apuntan a la tabla equivocada.")
    print("   La referencia RESUELVE, asi que ningun verificador la ve.")
    print("")
    for t, c in sorted(mal):
        n += 1
        print("   %d. %s.%s   Source table: %s   =>   %s"
              % (n, t, c, real[(t, c)], declarado[(t, c)]))
    print("")

if faltan:
    print("C. Referencias declaradas que la aplicacion no tiene.")
    print("")
    for t, c in sorted(faltan):
        n += 1
        print("   %d. %s.%s   =>   TYPE = Ref, Source table: %s"
              % (n, t, c, declarado[(t, c)]))
    print("")

print(ancho)
print("%d correcciones en el editor" % n)
print("")
print("De las %d referencias declaradas:" % len(declarado))
print("   %3d VERIFICADAS: la aplicacion nombra la columna" % len(probadas))
print("   %3d compatibles, no atribuidas: la aplicacion nombra la tabla" % len(compatibles))
print("       destino pero no la columna. Que sea la que el modelo declara")
print("       lo dice el modelo, no la aplicacion")
print("   %3d apuntan a otra tabla" % len(mal))
print("   %3d declaradas y ausentes" % len(faltan))
print("   %3d convertidas en Ref sin serlo" % len(sobran))
print("   %3d NO SE PUEDEN JUZGAR: su tabla destino esta vacia" % len(ciegas))
if ciegas:
    print("")
    print("   No estan bien ni mal: no son observables por este medio. La virtual")
    print("   inversa vive en el destino y un destino vacio no devuelve columnas.")
    for t, c in sorted(ciegas):
        vista = CONFIRMADAS_A_OJO.get((t, c))
        print("     - %-42s %s" % ("%s.%s -> %s" % (t, c, ciegas[(t, c)]),
              "mirada el %s por %s" % vista if vista else "NADIE LA HA MIRADO"))
    sin_mirar = [k for k in ciegas if k not in CONFIRMADAS_A_OJO]
    print("")
    if sin_mirar:
        print("   %d sin mirar. Abrelas en el editor y confirma su Source table."
              % len(sin_mirar))
    else:
        print("   Las %d se miraron en el editor. Eso NO las vuelve verificadas: una"
              % len(ciegas))
        print("   lectura visual no es una medicion, y por eso se guarda con fecha.")
    print("   Para MEDIRLAS: sembrar una fila en la tabla destino y volver a correr.")
if caidas:
    print("")
    for t, e in caidas:
        print("   ! %s no respondio: %s" % (t, e))
print(ancho)

# ------------------------------------------------- el encargo, para otro agente
#
# Autocontenido y derivado de esta misma lectura, no escrito a mano: si alguien
# corrige la mitad y vuelve a correr, el documento se queda con lo que falta.
M = []
w = M.append
w("# Correcciones de cableado")
w("")
w("**Generado** por `scripts/auditar_cableado.py` contra la aplicacion en vivo. No editar a")
w("mano: vuelve a correr el script y se rehace con lo que quede pendiente.")
w("")
w("---")
w("")
w("En la aplicacion **`%s`**, %d columnas de `ACT_Activos` estan mal. El resto del"
  % (APP_NOMBRE, n))
w("cableado no contradice al modelo, pero conviene leer la cifra con cuidado: de las %d"
  % len(declarado))
w("referencias, **%d estan verificadas** —la aplicacion nombra la columna— y **%d solo son"
  % (len(probadas), len(compatibles)))
w("compatibles**: la aplicacion nombra la tabla destino, y que la referencia este en la columna que")
w("el modelo declara **lo dice el modelo, no la aplicacion**. Sumarlas es la cifra inflada que ya")
w("costo cara una vez.")
w("")
w("## Antes de tocar nada, por que importa")
w("")
w("`ACT_Activos.TipoActivoID` apunta hoy a `SED_Sedes`. Con eso, **cada activo lee el checklist")
w("de una sede**, y la regla del geofencing falla con un mensaje que despista:")
w("")
w("```")
w('Can\'t find column "RadioGeofencingKm" in table "SED_Sedes"')
w("```")
w("")
w("**La expresion esta bien escrita. No la cambies.** El error dice la verdad: navega a")
w("`SED_Sedes` porque la referencia esta mal puesta, y ahi ese radio no existe. Reescribir la")
w("expresion para acomodarla seria romper una regla correcta para tapar un cableado roto.")
w("")
w("Ninguna regla se cablea hasta que estas %d esten hechas." % n)
w("")
w("## Como se llego a esto")
w("")
w("Al cablear `ACT_Activos` salio un aviso rojo. Se corrigieron dos columnas a mano y se guardo.")
w("Pero al guardar quedaron **tres columnas de texto convertidas en `Ref`** y **dos referencias")
w("apuntando a `SED_Sedes`**, que era la tabla que estaba seleccionada. Nada lo detecto: la API")
w("respondio 28/28, `validar_modelo.py` dio APTO y las 368 filas seguian ahi.")
w("")
w("Es la regla **R-04**: *una referencia que resuelve puede apuntar a lo que no es.* Preguntar")
w("«apunta a algo» nunca contesta «apunta a lo correcto».")
w("")
w("## Las %d, en orden" % n)
w("")
w("Todas en **`Data > Columns > ACT_Activos`**.")
w("")
if sobran:
    w("Guarda **una sola vez, al final**. El orden de la tabla importa porque mientras las %d de"
      % len(sobran))
    w("la seccion A esten mal, el editor no deja guardar: hazlas primero dentro de la misma sesion.")
else:
    w("Guarda **una sola vez, al final**. No hay columnas que bloqueen el guardado, asi que dentro")
    w("de la sesion el orden da igual.")
w("")
w("| # | Columna | Esta asi | Debe quedar |")
w("|---|---|---|---|")
i = 0
for t, c in sorted(sobran):
    i += 1
    tipo = next((x["tipo"] for x in MODELO[t]["columnas"] if x["nombre"] == c), "?")
    w("| %d | `%s` | `Ref` -> `%s` | **`%s`**, sin tabla destino |"
      % (i, c, real[(t, c)], tipo))
for t, c in sorted(mal):
    i += 1
    w("| %d | `%s` | `Ref` -> `%s` | `Ref` -> **`%s`** |" % (i, c, real[(t, c)], declarado[(t, c)]))
for t, c in sorted(faltan):
    i += 1
    w("| %d | `%s` | no es `Ref` | `Ref` -> **`%s`** |" % (i, c, declarado[(t, c)]))
w("")
w("> Las tres primeras van antes que las demas. Son las que bloquean el guardado.")
w("")
w("## Como saber que quedo")
w("")
w("El boton `SAVE` pasa de gris a azul al recoger el cambio, y vuelve a gris al guardar. Ese")
w("ciclo es la senal; si sigue gris, el editor no recogio nada y se pierde al recargar.")
w("")
w("Despues, desde el repositorio:")
w("")
w("```bash")
w("python scripts/auditar_cableado.py")
w("```")
w("")
w("Sale con **0 correcciones** cuando esta bien. No te fies del recuento de tablas de la API:")
w("dio 28/28 con estas %d rotas." % n)
w("")
if ciegas:
    w("## Lo que este script NO puede ver")
    w("")
    w("%d referencias no son observables por este medio, porque su tabla destino esta **vacia** y"
      % len(ciegas))
    w("la columna virtual inversa vive en el destino. **No estan bien ni mal: no se sabe.**")
    w("")
    w("| Referencia | Destino | Mirada en el editor |")
    w("|---|---|---|")
    for t, c in sorted(ciegas):
        vista = CONFIRMADAS_A_OJO.get((t, c))
        w("| `%s.%s` | `%s` | %s |" % (t, c, ciegas[(t, c)],
          "el %s por %s" % vista if vista else "**nadie la ha mirado**"))
    w("")
    _sin = [k for k in ciegas if k not in CONFIRMADAS_A_OJO]
    if _sin:
        w("**%d sin mirar.** Abrelas en el editor una por una y confirma su `Source table`."
          % len(_sin))
        w("Dar por buena una referencia que nadie ha mirado es como se llego a un informe de")
        w("«39/39 asignadas» con cinco columnas rotas.")
    else:
        w("Las %d se miraron en el editor. **Eso no las vuelve verificadas:** una lectura visual"
          % len(ciegas))
        w("no es una medicion, y por eso queda con fecha y con quien la hizo. Si alguien vuelve a")
        w("cablear, esa confirmacion habla de un estado anterior.")
    w("")
    w("Para **medirlas**, sembrar una fila en `MAN_Mantenimientos`, `CHK_Checklists` y")
    w("`OT_OrdenesTrabajo` y volver a correr el auditor. De paso deja de haber tablas cuya clave")
    w("AppSheet tipo a ciegas por llegar vacias.")

with open(os.path.join(RAIZ, "docs", "CORRECCIONES_CABLEADO.md"), "w",
          encoding="utf-8") as f:
    f.write("\n".join(M) + "\n")
print("")
print("Generado: docs/CORRECCIONES_CABLEADO.md")

sys.exit(1 if n else 0)
