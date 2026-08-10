# -*- coding: utf-8 -*-
"""Comprueba que todo enlace relativo entre documentos del repositorio resuelve.

Por que existe
--------------
El 2026-08-09 se retiraron 15 documentos a docs/historico/. Un agente encontro
26 enlaces rotos leyendolos uno a uno. Eso no se sostiene: cada vez que algo se
mueva, los enlaces se rompen en silencio y nadie los ve hasta que alguien pincha.

Un enlace roto no es cosmetico. Manda a quien retoma el proyecto a un documento
que no existe, y la alternativa es que se guie por el que si encuentre, que suele
ser el viejo.

Uso:  python scripts/verificar_enlaces.py
Sale con codigo 1 si hay alguno roto.
"""
import io
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Carpetas que no se recorren: no son documentacion del proyecto.
EXCLUIR = {".git", "node_modules", "__pycache__", "contexto", ".venv"}

# [texto](destino) — solo enlaces relativos. Se ignoran http(s):, mailto: y #ancla.
ENLACE = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")


def es_relativo(destino):
    d = destino.strip()
    if not d or d.startswith("#"):
        return False
    return not re.match(r"^(https?:|mailto:|tel:|data:)", d, re.I)


def documentos():
    for base, dirs, files in os.walk(RAIZ):
        dirs[:] = [d for d in dirs if d not in EXCLUIR]
        for f in files:
            if f.lower().endswith(".md"):
                yield os.path.join(base, f)


def main():
    rotos = []
    revisados = 0
    enlaces = 0

    for ruta in sorted(documentos()):
        revisados += 1
        try:
            texto = io.open(ruta, encoding="utf-8").read()
        except UnicodeDecodeError:
            texto = io.open(ruta, encoding="latin-1").read()

        for n, linea in enumerate(texto.splitlines(), 1):
            for m in ENLACE.finditer(linea):
                destino = m.group(2).strip()
                if not es_relativo(destino):
                    continue
                enlaces += 1
                # Quitar ancla y titulo entre comillas: (archivo.md#seccion "titulo")
                limpio = destino.split("#")[0].split(" ")[0].strip()
                if not limpio:
                    continue
                objetivo = os.path.normpath(
                    os.path.join(os.path.dirname(ruta), limpio))
                if not os.path.exists(objetivo):
                    rotos.append((os.path.relpath(ruta, RAIZ), n,
                                  m.group(1)[:40], destino))

    ancho = "=" * 78
    print(ancho)
    print("VERIFICACION DE ENLACES ENTRE DOCUMENTOS")
    print(ancho)
    print("Documentos revisados: %d | enlaces relativos: %d" % (revisados, enlaces))
    print("")

    if rotos:
        # Agrupados por documento: se arreglan de a un archivo, no de a un enlace.
        actual = None
        for arch, n, texto_enlace, destino in rotos:
            if arch != actual:
                print("  %s" % arch)
                actual = arch
            print("      linea %-5d [%s] -> %s" % (n, texto_enlace, destino))
        print("")
        print(ancho)
        print("ENLACES ROTOS: %d" % len(rotos))
        print(ancho)
        return 1

    print(ancho)
    print("TODOS LOS ENLACES RESUELVEN")
    print(ancho)
    return 0


if __name__ == "__main__":
    sys.exit(main())
