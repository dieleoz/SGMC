# -*- coding: utf-8 -*-
"""Quien comprueba cada cosa que se hace en el editor. Y quien no.

Por que existe
--------------
El 2026-08-10 se reporto tres veces que algo estaba hecho, y las tres veces no
lo estaba:

    "39/39 referencias asignadas"   ->  5 mal, 4 sin poner
    "11 reglas puestas"             ->  6 bien, 1 mal, 2 sin poner
    "tipos y Label listos"          ->  escribio en 2 celdas, 1 mal

No fue mala fe ni descuido: **quien ejecuta no puede verificarse a si mismo**.
Cierra el dialogo, ve el boton en gris, y para el la cosa quedo. Lo que faltaba
es la LECTURA DE VUELTA -mirar el resultado desde fuera, con otro instrumento-
y solo dos cosas la tenian: auditar_cableado.py e instantanea.py. Todo lo que
paso por ellas se cazo el mismo dia. Todo lo demas sobrevivio a tres informes.

De ahi el bucle de arreglar el arreglo: cada tanda descubre a mano lo que la
anterior dio por hecho.

La regla
--------
**Ningun paso del encargo se da por cerrado sin decir quien lo lee de vuelta.**
Si hay comando, va el comando. Si no lo hay, se dice EN VOZ ALTA que no lo hay
y se pide el cotejo a ojo copiando el texto literal, que es la unica evidencia
posible.

Lo segundo importa mas que lo primero. Un paso sin comprobacion declarada se
lee como comprobado.
"""

# Cada entrada: como se lee de vuelta, y si es mecanica o humana.
COMPROBACIONES = {
    "referencias": (
        "python scripts/auditar_cableado.py",
        "mecanica",
        "Lee las columnas virtuales inversas de la tabla destino. Con ' By ' "
        "prueba la columna; sin ' By ' solo prueba que hay una referencia a esa "
        "tabla. Y no ve nada si el destino esta vacio"),
    "datos": (
        "python scripts/instantanea.py comparar <antes> <despues>",
        "mecanica",
        "Compara celda a celda contra una foto previa. Cazo que convertir "
        "MotivoBaja a Enum reescribio el dato con un espacio al final"),
    "estructura": (
        "python scripts/verificar_app.py",
        "mecanica",
        "Compara el numero de filas de las 28 tablas. No mira contenido"),
    "tipos": (
        None, "humana",
        "**No hay comando.** La API v2 devuelve filas, no esquema: no hay forma "
        "de preguntarle de que tipo es una columna. Se cotejan contra "
        "TIPOS_ESPERADOS.md, y lo que quede escrito es la unica evidencia"),
    "expresiones": (
        None, "humana",
        "**No hay comando.** Valid_If, App formula, Initial value, Editable_If y "
        "los Security Filter no viajan por la API. Se copian del editor "
        "LITERALMENTE, sin resumir ni corregir: un espacio al final o una tilde "
        "de mas rompen la comparacion y no dan error"),
    "permisos": (
        None, "humana",
        "**No hay comando.** Are updates allowed no viaja por la API, y la API "
        "ademas tiene MAS permisos que la aplicacion -se salta el Deletes "
        "retirado-, asi que probar por ahi diria que se puede borrar cuando la "
        "app no deja"),
    "etiqueta": (
        None, "humana",
        "**No hay comando.** El Label es lo que el tecnico ve en los "
        "desplegables. Se mira en Data > Columns, una por tabla"),
    }


def bloque(clave, sangria=""):
    """El texto de comprobacion para un paso, listo para meter en un encargo."""
    comando, clase, motivo = COMPROBACIONES[clave]
    L = []
    if clase == "mecanica":
        L.append("%s**Cómo se lee de vuelta:**" % sangria)
        L.append("")
        L.append("%s```bash" % sangria)
        L.append("%s%s" % (sangria, comando))
        L.append("%s```" % sangria)
        L.append("")
        L.append("%s%s." % (sangria, motivo))
    else:
        L.append("%s**Cómo se lee de vuelta: NADIE, salvo tú.**" % sangria)
        L.append("")
        L.append("%s%s." % (sangria, motivo))
        L.append("")
        L.append("%sPor eso este paso se cierra **copiando literalmente lo que ves**, incluso"
                 % sangria)
        L.append("%scuando coincida. «Coincide» no es evidencia; el texto sí." % sangria)
    return "\n".join(L)


if __name__ == "__main__":
    mec = [k for k, v in COMPROBACIONES.items() if v[1] == "mecanica"]
    hum = [k for k, v in COMPROBACIONES.items() if v[1] == "humana"]
    print("QUIEN LEE DE VUELTA CADA COSA")
    print("")
    print("  con comando   %s" % " · ".join(mec))
    print("  a ojo         %s" % " · ".join(hum))
    print("")
    print("Las de la segunda fila son las que sobrevivieron a tres informes de")
    print("'hecho' el 2026-08-10. No porque nadie mirara: porque no habia con que.")


# ------------------------------------- lo que apaga los instrumentos: el orden
#
# **Los filtros de seguridad van AL FINAL, y no es preferencia.**
#
# El 2026-08-10, al poner RG-04 sobre ACT_Activos, la API paso de devolver 368
# filas a devolver CERO. No se perdio nada -un Security Filter filtra lecturas,
# no borra- pero la API llama SIN USUARIO, asi que USEREMAIL() esta en blanco y
# el filtro no deja pasar nada.
#
# El efecto es que los dos unicos instrumentos mecanicos se quedan ciegos justo
# en la tabla mas grande:
#
#   instantanea.py       deja de poder comparar los 368 activos
#   auditar_cableado.py  ACT_Activos pasa a "tabla vacia", y con ella las tres
#                        referencias que la apuntan dejan de ser juzgables: de 6
#                        no observables se paso a 9
#
# Es la version instrumental de la trampa de siempre: no es que este mal, es que
# **deja de poderse ver**, y eso se lee igual que "esta bien" si nadie lo dice.
FILTROS_AL_FINAL = (
    "Los Security Filter -RG-04 y RG-05- se ponen DESPUES de haber comprobado "
    "referencias, tipos y datos. Una vez puestos, la API deja de devolver las "
    "filas de esas tablas y ni instantanea.py ni auditar_cableado.py pueden "
    "volver a mirarlas: no porque fallen, sino porque el filtro hace su trabajo "
    "tambien con ellos.")

