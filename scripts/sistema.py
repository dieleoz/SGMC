# -*- coding: utf-8 -*-
"""Cual es la aplicacion y cual es la hoja. Un solo sitio.

Por que existe
--------------
Estos dos identificadores estaban escritos a mano en 37 documentos y 10 scripts.
Cada vez que el sistema se reconstruia -y se reconstruyo tres veces en cuatro
dias- habia que perseguirlos uno por uno, y nunca se perseguian todos. El
resultado, el 2026-08-10: cinco aplicaciones y tres hojas mencionadas por el
repositorio, con documentos vigentes apuntando a las abandonadas y un enlace de
la portada que daba 404.

Quien llega no puede distinguir cual es el sistema. Eso no se arregla revisando
mejor: se arregla teniendo un solo sitio del que salga el dato.

Regla
-----
**Ningun documento generado escribe un identificador a mano.** Lo pide aqui.
Si un .md vigente nombra una aplicacion o una hoja que no sea la de este
archivo, esta desactualizado o habla del pasado, y en el segundo caso tiene que
decirlo.
"""

# ------------------------------------------------------------- lo que ES hoy
APP_NOMBRE = "SISGA_-323965761-26-08-10"
APP_ID = "d180a1b5-19ca-448e-a44c-f985396dce12"
APP_URL = "https://www.appsheet.com/template/appdef?appId=" + APP_ID

HOJA_NOMBRE = "Modelo_Datos_10082026"
HOJA_ID = "1h9kyCYGK6esRL1UiTcPXHlSmDQcPb13fNZ0hBznYOa0"
HOJA_URL = "https://docs.google.com/spreadsheets/d/" + HOJA_ID

# El volcado local de esa hoja, contra el que corren los verificadores.
# Mientras la hoja publicada sea exactamente la plantilla generada, son el mismo
# archivo. En cuanto operacion empiece a completarla, se descarga a BD/ con su
# fecha y se pasa por argumento.
VOLCADO = "BD/Modelo_Datos_PLANTILLA.xlsx"

# ------------------------------------------------------- lo que YA NO es
#
# No se borran de aqui: son lo que hay que reconocer para poder descartarlo.
# Si alguien abre un enlace de esta tabla, tiene que saber en un vistazo que no
# es el sistema y por que dejo de serlo.
SUPERADOS = [
    ("aplicacion", "SISGA_-323965761", "7cc0b0eb-8c28-4cfb-9916-1e80367b43bc",
     "Intento previo del 2026-08-10. La vigente es su copia"),
    ("aplicacion", "SISGA", "",
     "Leia Modelo_Datos_09082026. Respaldo del estado anterior a la hoja limpia"),
    ("aplicacion", "SGMC2", "",
     "Con aviso de error. Abandonada"),
    ("aplicacion", "SGMC-886843353", "",
     "De la cuenta del Propietario anterior. Abandonada el 2026-08-09 porque "
     "Regenerate fusiona y con un esquema tan divergente no converge"),
    ("hoja", "Modelo_Datos_09082026", "1LGabjn1iNDKiJNP7CUD4_LwCH2BGXC8oTBfXmuuAkFs",
     "La hoja heredada, con 47 columnas que el modelo no declara. Respaldo"),
    ("hoja", "Modelo de Datos", "1a4MmZ0u9sNgWmyiR2OPJo9YuUEKJFftbJWMW-KbITRc",
     "Backend de la aplicacion abandonada, propiedad del Propietario anterior"),
    ]

# Los identificadores que NO deben aparecer en un documento vigente sin decir
# que estan superados. Lo comprueba verificar_documentos.py.
IDENTIFICADORES_SUPERADOS = [x[2] for x in SUPERADOS if x[2]] + \
                            [x[1] for x in SUPERADOS if x[1] != "Modelo de Datos"]


def cabecera_markdown():
    """El bloque de enlaces, para que ningun generador lo escriba a mano."""
    return (
        "| | |\n"
        "|---|---|\n"
        "| Aplicacion | AppSheet [`%s`](%s) |\n"
        "| Datos | Google Sheets [`%s`](%s) |\n"
        % (APP_NOMBRE, APP_URL, HOJA_NOMBRE, HOJA_URL))


if __name__ == "__main__":
    print("EL SISTEMA, hoy")
    print("  Aplicacion  %s" % APP_NOMBRE)
    print("              %s" % APP_URL)
    print("  Datos       %s" % HOJA_NOMBRE)
    print("              %s" % HOJA_URL)
    print("  Volcado     %s" % VOLCADO)
    print()
    print("SUPERADOS -- si un documento vigente los nombra sin decir que lo estan,")
    print("            esta desactualizado")
    for clase, nombre, ident, motivo in SUPERADOS:
        print("  %-11s %-26s %s" % (clase, nombre, motivo))
