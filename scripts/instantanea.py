# -*- coding: utf-8 -*-
"""Fotografia los datos vivos de la aplicacion, y compara dos fotografias.

Por que existe
--------------
Diez de las 21 reglas -App formula, Initial value y los bots- **escriben en la
hoja**. A diferencia de un tipo de columna, lo que escriben NO se revierte
cambiando un desplegable: hay que saber que habia antes.

Y no basta con mirar la fila que se espera que cambie. RG-16 deberia tocar 1
activo de 368 -el retirado, que ya tiene Activo = N, de modo que el valor no
deberia moverse-, pero una App formula se evalua sobre las 368. Si la
expresion esta mal, escribe en todas y no da error: da datos.

Por eso el criterio de cierre de P-33 no es "el activo EST-04 sigue igual",
es **"no cambio ninguna de las 368 celdas"**. Eso exige una fotografia previa,
y hasta hoy no habia forma de tomarla.

Contra la aplicacion, no contra la plantilla
--------------------------------------------
Se lee por API, que es lo que ve la aplicacion. BD/Modelo_Datos_PLANTILLA.xlsx
no sirve para esto: se regenera del modelo y NUNCA recibe lo que la aplicacion
escribe, asi que compararse contra ella diria que no cambio nada siempre.

Solo lee: usa la accion Find.

Uso:
    python scripts/instantanea.py guardar antes-de-rg16
    ... se cablean las reglas ...
    python scripts/instantanea.py guardar despues-de-rg16
    python scripts/instantanea.py comparar antes-de-rg16 despues-de-rg16

Sale con codigo 1 si la comparacion encuentra alguna celda distinta.
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

CARPETA = os.path.join(RAIZ, "BD", "instantaneas")

_env = os.path.join(RAIZ, ".env")
if os.path.exists(_env):
    for _l in open(_env, encoding="utf-8"):
        if "=" in _l and not _l.strip().startswith("#"):
            _k, _v = _l.split("=", 1)
            os.environ.setdefault(_k.strip(), _v.strip())

API_KEY = os.environ.get("APPSHEET_API_KEY", "")
URL = "https://api.appsheet.com/api/v2/apps/%s/tables/%s/Action"


def leer(tabla):
    pet = urllib.request.Request(
        URL % (APP_ID, tabla),
        json.dumps({"Action": "Find", "Properties": {}, "Rows": []}).encode(),
        {"ApplicationAccessKey": API_KEY, "Content-Type": "application/json"})
    cuerpo = urllib.request.urlopen(pet, timeout=40).read().decode()
    return json.loads(cuerpo or "[]")


def ruta(nombre):
    return os.path.join(CARPETA, "%s.json" % nombre)


def guardar(nombre):
    if not API_KEY:
        print("Falta APPSHEET_API_KEY en .env."); sys.exit(2)
    if not os.path.isdir(CARPETA):
        os.makedirs(CARPETA)
    foto, caidas = {}, []
    for t in sorted(MODELO):
        try:
            filas = leer(t)
        except urllib.error.URLError as e:
            caidas.append((t, str(e)))
            continue
        # Las virtuales inversas -Related ...- no son dato: las calcula AppSheet
        # y cambian al cablear una referencia. Si entraran, cualquier cambio de
        # cableado se leeria como si se hubiera tocado el dato.
        foto[t] = [{k: v for k, v in f.items() if not k.startswith("Related ")}
                   for f in filas]
    if caidas:
        # Una tabla que no responde daria una foto con menos filas de las que
        # hay, y la comparacion siguiente la leeria como filas BORRADAS.
        print("LECTURA INCOMPLETA. No se guarda nada.")
        for t, e in caidas:
            print("   ! %s: %s" % (t, e))
        sys.exit(2)
    with open(ruta(nombre), "w", encoding="utf-8") as f:
        json.dump(foto, f, ensure_ascii=False, indent=1, sort_keys=True)
    print("Guardada: BD/instantaneas/%s.json" % nombre)
    print("%d tablas · %d filas en total"
          % (len(foto), sum(len(v) for v in foto.values())))


def clave_de(tabla, fila):
    pk = next((c["nombre"] for c in MODELO[tabla]["columnas"] if c.get("pk")), None)
    return str(fila.get(pk, "")) if pk else str(fila.get("_RowNumber", ""))


def comparar(a, b):
    for n in (a, b):
        if not os.path.exists(ruta(n)):
            print("No existe BD/instantaneas/%s.json" % n); sys.exit(2)
    A = json.load(open(ruta(a), encoding="utf-8"))
    B = json.load(open(ruta(b), encoding="utf-8"))
    ancho = "=" * 78
    print(ancho)
    print("QUE CAMBIO EN LA APLICACION")
    print(ancho)
    print("%s  ->  %s" % (a, b))
    print("")

    cambios = []
    for t in sorted(set(A) | set(B)):
        fa = {clave_de(t, f): f for f in A.get(t, [])}
        fb = {clave_de(t, f): f for f in B.get(t, [])}
        for k in sorted(set(fa) - set(fb)):
            cambios.append("%s: desaparecio la fila %s" % (t, k))
        for k in sorted(set(fb) - set(fa)):
            cambios.append("%s: aparecio la fila %s" % (t, k))
        for k in sorted(set(fa) & set(fb)):
            for col in sorted(set(fa[k]) | set(fb[k])):
                if col == "_RowNumber":
                    continue
                va, vb = str(fa[k].get(col, "")), str(fb[k].get(col, ""))
                if va != vb:
                    cambios.append("%s[%s].%s: %r -> %r" % (t, k, col, va, vb))

    if not cambios:
        print("NINGUNA CELDA CAMBIO.")
        print("")
        print("Es el criterio de cierre de P-33: una App formula se evalua sobre")
        print("TODAS las filas, no solo sobre la que se espera que cambie.")
        print(ancho)
        return 0

    print("%d cambios:" % len(cambios))
    print("")
    for c in cambios[:60]:
        print("   %s" % c)
    if len(cambios) > 60:
        print("   ... y %d mas" % (len(cambios) - 60))
    print("")
    print(ancho)
    print("LA APLICACION ESCRIBIO EN LOS DATOS")
    print("Si no esperabas esto, la expresion que acabas de poner escribe donde")
    print("no debe. Se corrige la expresion; el dato se repone desde el modelo.")
    print(ancho)
    return 1


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "guardar":
        guardar(sys.argv[2])
    elif len(sys.argv) >= 4 and sys.argv[1] == "comparar":
        sys.exit(comparar(sys.argv[2], sys.argv[3]))
    else:
        print(__doc__)
        print("Aplicacion: %s" % APP_NOMBRE)
        if os.path.isdir(CARPETA):
            fotos = sorted(x[:-5] for x in os.listdir(CARPETA) if x.endswith(".json"))
            print("Instantaneas guardadas: %s" % (" · ".join(fotos) or "ninguna"))
        sys.exit(2)
