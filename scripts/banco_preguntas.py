# -*- coding: utf-8 -*-
"""Borrador de checklist para los tipos que no tienen banco de preguntas.

Que es y que NO es
------------------
NO es el checklist definitivo. Las preguntas de verdad las escribe quien sabe
que se le revisa a un paso seguro o a un carril de peaje: es la decision D-09 y
sigue abierta.

Lo que esto hace es que el funcional NO parta de una hoja en blanco. Recibe una
estructura completa y plausible -sus secciones, sus tipos de respuesta, sus
rangos, sus fotografias obligatorias- y trabaja corrigiendo, que es mucho mas
barato que inventar el formato desde cero.

**Toda pregunta generada aqui lleva MARCA al final de su ayuda.** Mientras esa
marca este, la pregunta esta sin validar. Buscar la marca en la hoja dice
exactamente que queda por revisar, y el dia que no aparezca ninguna, el banco
esta cerrado.

De donde sale la forma
----------------------
De los tres bancos reales que ya existian -SOS, CCTV y PMVF, 15 preguntas cada
uno-. Los tres comparten el mismo esqueleto, y es ese esqueleto el que se
replica:

  estado encontrado -> limpieza -> inspeccion -> pruebas -> medicion ->
  novedad critica -> observaciones -> tres fotografias

Esos tres NO se generan: se copian tal cual de la hoja, porque estan acordados.
"""

MARCA = "[BORRADOR: validar con operacion]"

# Sin tocar: son los IDs de FRM_Secciones y TPR_TiposRespuesta de la hoja.
SEC_ESTADO, SEC_LIMPIEZA, SEC_FISICA, SEC_PRUEBAS = 1, 2, 3, 4
SEC_ELECTRICO, SEC_COMUNICACIONES, SEC_SOLAR = 5, 6, 7
SEC_VISUAL, SEC_VENTILACION, SEC_GABINETE = 8, 9, 10
SEC_SEGURIDAD, SEC_SENSORES, SEC_NOVEDADES, SEC_EVIDENCIA = 11, 12, 13, 14

SI_NO, LISTA, NUMERO, TEXTO_CORTO, TEXTO_LARGO = 1, 2, 3, 4, 5
FECHA, HORA, FOTO, FIRMA, GPS = 6, 7, 8, 9, 10

# Los cuatro valores de "Estado encontrado". Salen de LST_ValoresLista, donde
# hoy solo los tiene la pregunta de SOS. Una pregunta de tipo Lista sin valores
# le muestra al tecnico un desplegable vacio, y eso no da error en ninguna parte.
VALORES_ESTADO = ["Operativo", "Operativo con observaciones",
                  "Fuera de servicio", "No aplica"]

# (seccion, pregunta, tipo, obligatoria, minimo, maximo, unidad, ayuda)

# Abre igual en los tres bancos reales.
APERTURA = [
    (SEC_ESTADO, "Estado encontrado", LISTA, True, "", "", "",
     "Seleccione el estado en que encontro el activo"),
    ]

# Cierra igual en los tres bancos reales: la novedad, el texto libre y las
# tres fotografias. La de novedades es la unica no obligatoria.
CIERRE = [
    (SEC_NOVEDADES, "¿Se detecto una novedad critica?", SI_NO, True, "", "", "",
     "Si responde Si, describala en la pregunta siguiente"),
    (SEC_NOVEDADES, "Observaciones tecnicas", TEXTO_LARGO, False, "", "", "",
     "Describa hallazgos y recomendaciones"),
    (SEC_EVIDENCIA, "Fotografia panoramica del activo", FOTO, True, "", "", "",
     "Fotografia general que situe el equipo en su entorno"),
    (SEC_EVIDENCIA, "Fotografia de detalle del equipo", FOTO, True, "", "", "",
     "Fotografia cercana del equipo intervenido"),
    (SEC_EVIDENCIA, "Fotografia de novedades", FOTO, False, "", "", "",
     "Solo si existen novedades"),
    ]

# El cuerpo, por categoria. Es lo que cambia entre un poste en la via y un
# servidor en un rack, y por eso no puede ser uno solo.
CUERPO = {
    "ITS": [
        (SEC_LIMPIEZA, "¿Se realizo limpieza externa del equipo?", SI_NO, True, "", "", "",
         "Retire polvo, barro y vegetacion"),
        (SEC_LIMPIEZA, "¿Se realizo limpieza interna del gabinete?", SI_NO, True, "", "", "",
         "Verifique ausencia de polvo y humedad"),
        (SEC_FISICA, "¿La estructura y los anclajes estan en buen estado?", SI_NO, True, "", "", "",
         "Revise corrosion, tornilleria y fijaciones"),
        (SEC_PRUEBAS, "¿El equipo responde correctamente a la prueba funcional?", SI_NO, True, "", "", "",
         "Ejecute la prueba propia del equipo"),
        (SEC_ELECTRICO, "Voltaje de alimentacion", NUMERO, True, 100, 240, "VAC",
         "Registre el voltaje medido con multimetro"),
        (SEC_COMUNICACIONES, "¿Existe comunicacion con el CCO?", SI_NO, True, "", "", "",
         "Verifique el enlace desde el sitio"),
        (SEC_GABINETE, "¿El gabinete esta libre de humedad y corrosion?", SI_NO, True, "", "", "",
         "Inspeccione sellos, prensaestopas y drenajes"),
        ],
    "Electrico": [
        (SEC_LIMPIEZA, "¿Se realizo limpieza del equipo y su recinto?", SI_NO, True, "", "", "",
         "Sin energizar, segun el procedimiento de seguridad"),
        (SEC_FISICA, "¿Hay senales de sobrecalentamiento o corrosion?", SI_NO, True, "", "", "",
         "Revise bornes, cables y conexiones"),
        (SEC_ELECTRICO, "Voltaje de salida", NUMERO, True, 100, 480, "VAC",
         "Registre el voltaje medido"),
        (SEC_ELECTRICO, "Resistencia de puesta a tierra", NUMERO, True, 0, 25, "ohm",
         "Debe estar por debajo de 25 ohm"),
        (SEC_PRUEBAS, "¿La prueba de transferencia o respaldo fue exitosa?", SI_NO, True, "", "", "",
         "Simule el corte y verifique la respuesta"),
        (SEC_VENTILACION, "¿La ventilacion del recinto funciona?", SI_NO, True, "", "", "",
         "Verifique rejillas, extractores y filtros"),
        ],
    "TI": [
        (SEC_LIMPIEZA, "¿Se realizo limpieza del equipo y del rack?", SI_NO, True, "", "", "",
         "Incluye filtros de aire si el equipo los tiene"),
        (SEC_FISICA, "¿El equipo presenta alarmas o indicadores en rojo?", SI_NO, True, "", "", "",
         "Revise el panel frontal y los indicadores de fuente"),
        (SEC_PRUEBAS, "¿El equipo responde a la prueba de conectividad?", SI_NO, True, "", "", "",
         "Prueba de alcance desde la red de gestion"),
        (SEC_VENTILACION, "Temperatura del recinto", NUMERO, True, 15, 30, "C",
         "Medir a la altura del equipo"),
        (SEC_COMUNICACIONES, "¿Los enlaces estan operativos?", SI_NO, True, "", "", "",
         "Verifique puertos activos y sin errores"),
        ],
    "Comunicaciones": [
        (SEC_FISICA, "¿El tramo recorrido presenta danos o intervenciones?", SI_NO, True, "", "", "",
         "Revise postes, camaras de paso y empalmes"),
        (SEC_FISICA, "¿La senalizacion del trazado esta completa?", SI_NO, True, "", "", "",
         "Hitos y placas de identificacion"),
        (SEC_PRUEBAS, "Atenuacion medida en el tramo", NUMERO, True, 0, 30, "dB",
         "Registre la medicion del OTDR"),
        (SEC_COMUNICACIONES, "¿El enlace quedo operativo al terminar?", SI_NO, True, "", "", "",
         "Confirme con el CCO antes de retirarse"),
        ],
    }


def preguntas_de(categoria):
    """El borrador de checklist para un tipo de activo de esa categoria."""
    cuerpo = CUERPO.get(categoria)
    if cuerpo is None:
        raise KeyError("No hay cuerpo de checklist para la categoria '%s'. "
                       "Anadela a CUERPO o corrige el catalogo" % categoria)
    return APERTURA + cuerpo + CIERRE


def comprobar():
    """Invariantes del borrador."""
    fallos = []
    for categoria in CUERPO:
        p = preguntas_de(categoria)
        if not any(t == LISTA for _, _, t, _, _, _, _, _ in p):
            fallos.append("%s no abre con una pregunta de estado" % categoria)
        fotos = sum(1 for _, _, t, _, _, _, _, _ in p if t == FOTO)
        if fotos < 2:
            fallos.append("%s tiene %d fotografias. La evidencia fotografica es "
                          "lo unico que prueba que se estuvo trabajando" % (categoria, fotos))
        for sec, texto, tipo, _obl, mini, maxi, unidad, _ayuda in p:
            if tipo == NUMERO and (mini == "" or maxi == "" or not unidad):
                fallos.append("%s: '%s' es numerica y le falta rango o unidad. "
                              "Sin rango, cualquier cifra pasa" % (categoria, texto))
    return fallos


if __name__ == "__main__":
    fallos = comprobar()
    for categoria in sorted(CUERPO):
        p = preguntas_de(categoria)
        print("== %s : %d preguntas ==" % (categoria, len(p)))
        for i, (sec, texto, tipo, obl, mini, maxi, unidad, _a) in enumerate(p, 1):
            rango = " [%s-%s %s]" % (mini, maxi, unidad) if tipo == NUMERO else ""
            print("   %2d  s%-3d t%-3d %-5s %s%s"
                  % (i, sec, tipo, "oblig" if obl else "", texto, rango))
        print()
    if fallos:
        for f in fallos:
            print("  x", f)
        raise SystemExit(1)
    print("Borrador coherente. Toda pregunta generada lleva:", MARCA)
