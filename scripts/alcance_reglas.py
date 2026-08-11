# -*- coding: utf-8 -*-
"""Que columnas toca de verdad cada regla. Con su tabla, no solo su nombre.

Por que existe
--------------
Los generadores atribuian las reglas a las columnas POR NOMBRE SUELTO. Como
`[Activo]` aparece en RG-04 y en RG-16, las **23 columnas llamadas `Activo`** de
23 tablas distintas salian con esas dos reglas encima. Resultado: 94 columnas
"con regla" donde hay muchas menos.

No es un detalle de presentacion. Esa atribucion es lo que ORDENA el trabajo del
ejecutor -primero las columnas de las que depende una regla, porque una columna
mal tipada con una regla encima rompe la regla en silencio-, asi que inflarla
convierte la prioridad en ruido y entierra las que de verdad importan.

Y era evitable: el propio repositorio ya resolvia bien las cadenas en
generar_prompt_expresiones.py. Estaba escrito, en un solo generador, y no
compartido. Es la misma forma del fallo de la seccion 13: conocimiento correcto
que ningun otro consumidor podia usar.

Como se resuelve
----------------
Una expresion se lee DESDE la tabla de su regla, y los puntos saltan a otra
tabla siguiendo las referencias. Ademas, dentro de un SELECT(Tabla[...], ...) el
contexto cambia: en RG-04 el `[Activo]` es de ASG_AsignacionZona, no de
ACT_Activos.
"""
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "scripts"))

from modelo_objetivo import MODELO, REGLAS

REF = {(t, c["nombre"]): c["ref"]
       for t in MODELO for c in MODELO[t]["columnas"] if c.get("ref")}
FUNCIONES_CON_TABLA = r"\b(?:SELECT|FILTER|ANY|COUNT|MAXROW|MINROW|LOOKUP)\s*\(\s*(\w+)\["


def _ambitos(expresion):
    """Tramos donde manda otra tabla, por un SELECT(Tabla[...]) o similar."""
    tramos = []
    for m in re.finditer(FUNCIONES_CON_TABLA, expresion):
        tabla = m.group(1)
        if tabla not in MODELO:
            continue
        hondo, fin = 0, len(expresion)
        for i in range(m.start(), len(expresion)):
            if expresion[i] == "(":
                hondo += 1
            elif expresion[i] == ")":
                hondo -= 1
                if hondo == 0:
                    fin = i
                    break
        tramos.append((m.start(), fin, tabla))
    return tramos


def columnas_de(regla):
    """Los (tabla, columna) que la regla toca de verdad. Sin repetir."""
    tabla = regla["tabla"]
    expresion = regla.get("expresion") or ""
    tocadas = []
    if regla.get("columna") and regla["columna"] not in ("(tabla)", "(varias)"):
        tocadas.append((tabla, regla["columna"]))
    tramos = _ambitos(expresion)
    for m in re.finditer(r"(?:\[\w+\]\s*\.\s*)*\[\w+\]", expresion):
        nombres = re.findall(r"\[(\w+)\]", m.group(0))
        aqui = next((t for ini, fin, t in tramos if ini <= m.start() <= fin), tabla)
        for i, n in enumerate(nombres):
            if (aqui, n) not in tocadas:
                tocadas.append((aqui, n))
            destino = REF.get((aqui, n))
            if not destino or i == len(nombres) - 1:
                break
            aqui = destino
    return [x for x in tocadas
            if x[0] in MODELO
            and any(c["nombre"] == x[1] for c in MODELO[x[0]]["columnas"])]


def por_columna():
    """{(tabla, columna): {ids de regla}}."""
    salida = {}
    for r in REGLAS:
        for clave in columnas_de(r):
            salida.setdefault(clave, set()).add(r["id"])
    return salida


if __name__ == "__main__":
    m = por_columna()
    total = sum(len(MODELO[t]["columnas"]) for t in MODELO)
    print("Columnas que alguna regla toca DE VERDAD: %d de %d" % (len(m), total))
    print("")
    print("Antes, atribuyendo por nombre suelto, salian 94.")
    print("")
    for (t, c), r in sorted(m.items(), key=lambda x: (-len(x[1]), x[0])):
        print("   %-44s %s" % ("%s.%s" % (t, c), ", ".join(sorted(r))))
