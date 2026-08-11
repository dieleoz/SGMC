# -*- coding: utf-8 -*-
"""Caza documentos que afirman un estado que otro documento ya desmintio.

Por que existe
--------------
La queja es literal: *"siempre que entro al repo, la documentacion es legacy
ya"*. Y es cierta. El 2026-08-11 se barrieron los documentos principales TRES
veces, y las tres volvieron a envejecer en horas:

  - ESTADO decia "RG-37/RG-38 por cablear" cuando ACTA-009 los habia cableado
  - ESTADO y ROADMAP decian "ESPEC-008 en curso" cuando ya estaba aprobada
  - README decia "ningun bot creado" cuando ya habia dos
  - ESPEC-008 decia "sin pasar por el arquitecto" DESPUES de aprobarse

Ese ultimo caso es el que mas duele: un ejecutor se nego a aplicar la orden por
esa contradiccion, y **acerto**. Le creyo al documento y no al resumen, que es
la regla de este proyecto. Pero costo una vuelta entera.

Barrer a mano no escala. Este script hace lo que `verificar_sistema.py` hace
con `SISTEMA.md`: comprobar que lo escrito sigue siendo verdad, salvo que aqui
la verdad no sale de un comando sino de OTRO DOCUMENTO.

Que comprueba
-------------
  F-01  El veredicto de cada ESPEC contra lo que dicen de ella los documentos
        principales. Una ESPEC aprobada de la que README dice "pendiente de
        dictamen" es la contradiccion que ya costo una vuelta.

  F-02  Que ninguna acta quede huerfana. Un acta es la UNICA evidencia que
        existe de lo que hay en el editor -la API devuelve filas, no esquema-,
        asi que una que no se cita desde ningun documento principal es trabajo
        que nadie va a encontrar.

  F-03  Que ninguna regla retirada del modelo se siga citando como algo
        pendiente de poner.

  F-04  Las cifras del modelo -tablas, columnas, referencias, reglas- en
        los cuatro documentos principales. Este control faltaba, y lo
        destapo un lector en frio: ESTADO.md decia 210 columnas y 21
        reglas con el modelo en 209 y 23, siendo ESTADO.md el documento
        al que README manda creer por encima de todos los demas.

Que NO comprueba
----------------
Lo que dice el editor. Ningun script puede: la API v2 devuelve filas, no
esquema. Para eso estan las actas, y por eso F-02 vigila que no se pierdan.

Uso:  python scripts/verificar_frescura.py
Sale con codigo 1 si un documento afirma algo que otro ya desmintio.
"""
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "scripts"))

SDD = os.path.join(RAIZ, "docs", "sdd")
PRINCIPALES = ["README.md", "ESTADO.md", "MAP.md",
               os.path.join("docs", "ROADMAP.md")]

# Que veredicto declara una ESPEC sobre si misma, y que frases quedan
# PROHIBIDAS en los documentos principales cuando lo declara.
#
# El orden importa: "APROBADA CON RIESGOS ACEPTADOS" contiene "APROBADA", asi
# que la variante larga va primero o la corta se la come.
VEREDICTOS = [
    ("APROBADA CON RIESGOS ACEPTADOS", "aprobada con riesgos aceptados"),
    ("CERRADA", "cerrada"),
    ("APROBADA", "aprobada"),
    ("BLOQUEADA", "bloqueada"),
]

# Frases que contradicen un veredicto ya emitido. Se buscan SOLO en la linea
# que menciona esa ESPEC: buscarlas en todo el documento daria falsos
# positivos cada vez que otra ESPEC distinta si esta pendiente.
# Lo que convierte la mencion de una regla retirada en un fallo: que se hable
# de ella como algo que queda por hacer.
PENDIENTE = [
    "pendiente", "falta", "faltan", "por poner", "por cablear",
    "sin cablear", "sin poner", "hay que poner", "queda por",
]

DESMENTIDAS_POR_APROBACION = [
    "pendiente de nuevo dictamen",
    "pendiente de dictamen",
    "espera dictamen",
    "sin pasar por el arquitecto",
    "en curso",
    "se esta escribiendo",
    "sin aprobar",
]


def lee(ruta):
    p = os.path.join(RAIZ, ruta)
    if not os.path.exists(p):
        return None
    return open(p, encoding="utf-8").read()


def sin_tildes(s):
    """Los documentos mezclan 'esta' y 'está'. Comparar sin tildes evita que
    una contradiccion real se escape por un acento."""
    for a, b in (("á", "a"), ("é", "e"), ("í", "i"), ("ó", "o"), ("ú", "u")):
        s = s.replace(a, b)
    return s


fallos, avisos, comprobadas = [], [], 0

ancho = "=" * 78
print(ancho)
print("LA DOCUMENTACION SE CONTRADICE A SI MISMA?")
print(ancho)
print("")

# ------------------------------------------------------- F-01  el veredicto
especs = sorted(f for f in os.listdir(SDD) if f.startswith("ESPEC-"))
for nombre in especs:
    texto = lee(os.path.join("docs", "sdd", nombre))
    ident = "-".join(nombre.split("-")[:2])

    veredicto = None
    for marca, legible in VEREDICTOS:
        if re.search(r"\*\*%s" % re.escape(marca), texto):
            veredicto = legible
            break
    if veredicto is None:
        continue  # sin veredicto propio: no hay contra que contrastar

    aprobada = veredicto in ("aprobada", "aprobada con riesgos aceptados",
                             "cerrada")
    if not aprobada:
        continue

    for doc in PRINCIPALES:
        contenido = lee(doc)
        if contenido is None:
            continue
        for n, linea in enumerate(contenido.split("\n"), 1):
            if ident not in linea:
                continue
            comprobadas += 1
            plano = sin_tildes(linea.lower())
            for frase in DESMENTIDAS_POR_APROBACION:
                if frase in plano:
                    fallos.append(
                        "[F-01] %s:%d dice «%s» sobre %s, y %s declara "
                        "en su cierre que esta **%s**. Le creera al resumen "
                        "quien lea el resumen, y al documento quien lea el "
                        "documento"
                        % (doc, n, frase, ident, nombre, veredicto))

# ------------------------------------------------------ F-02  actas huerfanas
actas = sorted(f for f in os.listdir(SDD) if f.startswith("ACTA-"))
for nombre in actas:
    base = nombre[:-3]
    comprobadas += 1
    citada = any(base in (lee(d) or "") for d in PRINCIPALES)
    if not citada:
        fallos.append(
            "[F-02] %s no se cita desde ninguno de los 4 documentos "
            "principales. Un acta es la UNICA evidencia que existe de lo que "
            "hay en el editor: si no se enlaza, nadie la va a encontrar"
            % nombre)

# --------------------------------------------- F-03  reglas retiradas vivas
try:
    from modelo_objetivo import REGLAS
    vivas = {r["id"] for r in REGLAS}
    todas = set()
    for d in PRINCIPALES:
        todas |= set(re.findall(r"RG-\d\d", lee(d) or ""))
    # Una regla que una ESPEC PROPONE todavia no esta en el modelo, y eso no
    # la convierte en retirada: es lo contrario, esta por venir. Sin esto,
    # RG-41 a RG-44 de ESPEC-009 salian como si se hubieran quitado.
    propuestas = set()
    for f in os.listdir(SDD):
        if f.startswith("ESPEC-"):
            propuestas |= set(re.findall(r"RG-\d\d",
                                         lee(os.path.join("docs", "sdd", f)) or ""))
    for rid in sorted(todas - vivas - (propuestas - vivas)):
        comprobadas += 1
        for doc in PRINCIPALES:
            for n, linea in enumerate((lee(doc) or "").split("\n"), 1):
                if rid not in linea:
                    continue
                plano = sin_tildes(linea.lower())
                # Mencionar una regla retirada es CORRECTO y frecuente: es
                # registro historico, y borrarlo seria perder por que se
                # decidio lo que se decidio.
                #
                # Lo que si es un fallo es hablar de ella como TRABAJO
                # PENDIENTE. Ese es el modo de fallo real: un lector va a
                # ponerla, y ya no existe.
                #
                # La primera version de este bloque marcaba toda mencion sin
                # la palabra "retirada" al lado, y daba 31 avisos de los que
                # casi ninguno era un fallo. Un verificador ruidoso es un
                # verificador que se ignora, asi que ocupa el sitio del que
                # si serviria -el mismo defecto que ya se cazo en P-66-.
                if not any(p in plano for p in PENDIENTE):
                    continue
                avisos.append(
                    "[F-03] %s:%d habla de %s como pendiente, y esa regla ya "
                    "no esta en el modelo. Quien lo lea va a ir a ponerla"
                    % (doc, n, rid))
except ImportError:
    pass

# ------------------------------------------- F-04  las cifras del modelo
#
# El agujero que este script tenia y que cazó un lector en frio, no el script:
# F-01 compara VEREDICTOS, y nadie comprobaba las CIFRAS fuera de SISTEMA.md.
# ESTADO.md llego a decir "210 columnas / 21 reglas" con el modelo en 209/23,
# y ESTADO.md es el documento al que README manda creer por encima del resto.
#
# `verificar_sistema.py` ya hace esto para SISTEMA.md. Aqui se extiende a los
# cuatro principales, con la misma leccion aprendida: se busca el numero PEGADO
# a su sustantivo. Comprobar si el numero aparece "en algun sitio" no caza nada,
# porque el viejo suele seguir estando en otra frase.
try:
    from modelo_objetivo import MODELO, REGLAS
    CIFRAS = [
        ("columnas", sum(len(MODELO[x]["columnas"]) for x in MODELO)),
        ("reglas", len(REGLAS)),
        ("referencias", sum(1 for x in MODELO for c in MODELO[x]["columnas"]
                            if c.get("ref"))),
    ]
    # `tablas` NO entra, y es una renuncia deliberada. Los documentos hablan
    # constantemente de subconjuntos grandes y todos son ciertos: 20 tablas con
    # clave legible, 24 con los tipos corregidos, 23 con una columna Activo, 8
    # de movimiento. Ninguna heuristica los separa del total de 28 sin acertar
    # a veces y fallar otras.
    #
    # Un control que no sabe distinguir se calla en esa dimension. Es preferible
    # a inundar de avisos que nadie va a leer -y este script ya nacio con ese
    # defecto en F-03, corregido el mismo dia-.
    for doc in PRINCIPALES:
        contenido = lee(doc)
        if contenido is None:
            continue
        for n, linea in enumerate(contenido.split(chr(10)), 1):
            plano = sin_tildes(linea.lower())
            for palabra, hoy in CIFRAS:
                for viejo in re.findall(r"(\d+)\s+%s" % palabra, plano):
                    comprobadas += 1
                    if int(viejo) == hoy:
                        continue
                    # Un SUBCONJUNTO no pretende ser el total: «2 columnas
                    # virtuales», «8 tablas de movimiento», «14 tablas con el
                    # Label movido». Todas son ciertas y no tienen por que
                    # coincidir con la cifra del modelo.
                    #
                    # La primera version las marcaba todas y daba mas ruido que
                    # senal, que es como muere un verificador: la gente deja de
                    # leerlo y entonces ocupa el sitio del que si serviria.
                    #
                    # Se distinguen por tamano: una cifra que PRETENDE ser el
                    # total esta cerca del total -210 contra 209, 21 contra 23-.
                    # Un subconjunto esta lejos.
                    if int(viejo) < hoy * 0.5:
                        continue
                    # Una cifra fechada es registro, no error: borrarla seria
                    # perder por que se decidio lo que se decidio.
                    if re.search(r"20\d\d-\d\d-\d\d", linea):
                        continue
                    fallos.append(
                        "[F-04] %s:%d dice «%s %s» y hoy son **%d**. Sale de "
                        "validar_modelo.py, no de la memoria de nadie"
                        % (doc, n, viejo, palabra, hoy))
except ImportError:
    pass

for f in fallos:
    print("  x %s" % f)
for a in avisos:
    print("  ! %s" % a)

print("")
print(ancho)
if fallos:
    print("LA DOCUMENTACION SE CONTRADICE: %d casos" % len(fallos))
    print("")
    print("No lo arregles solo donde salta. Mira cual de los dos documentos")
    print("tiene razon: si el resumen esta viejo, se actualiza; si el que esta")
    print("viejo es el cierre de la ESPEC, es peor, porque el gate solo")
    print("funciona si el propio documento lleva su veredicto.")
    print(ancho)
    sys.exit(1)

print("SIN CONTRADICCIONES: %d comprobaciones%s"
      % (comprobadas, " (%d avisos)" % len(avisos) if avisos else ""))
print("")
print("Lo que este script NO puede ver es el editor. Ningun script puede: la")
print("API v2 devuelve filas, no esquema. Por eso F-02 vigila que las actas no")
print("queden huerfanas: son la unica evidencia que va a existir.")
print(ancho)
