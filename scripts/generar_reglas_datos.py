# -*- coding: utf-8 -*-
"""Genera docs/REGLAS_DEL_MODELO_DE_DATOS.md: las reglas que manda el motor.

Por que se genera y no se escribe
---------------------------------
Estas reglas salieron de fallos reales, uno a uno, entre el 6 y el 10 de agosto,
y estaban repartidas en mensajes de commit y en secciones sueltas de CLAUDE.md.
Quien llegue a cambiar el modelo no va a leer veinte commits.

Y se generan porque cada regla lleva su lista derivada -las claves que hay, las
columnas de coordenada, cuantas referencias- y una lista escrita a mano envejece
en cuanto alguien toca el modelo. Aqui la unica forma de que mienta es que mienta
el modelo.

Uso:  python scripts/generar_reglas_datos.py
"""
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "scripts"))

from modelo_objetivo import MODELO, REGLAS, CLAVE_LEGIBLE, CLAVE_GENERADA
from catalogo_tipos import TIPOS_ACTIVO

SALIDA = os.path.join(RAIZ, "docs", "REGLAS_DEL_MODELO_DE_DATOS.md")

L = []
w = L.append


def columnas_de_tipo(tipo):
    return ["%s.%s" % (t, c["nombre"]) for t in MODELO
            for c in MODELO[t]["columnas"] if c["tipo"] == tipo]


refs = [(t, c["nombre"], c["ref"]) for t in MODELO
        for c in MODELO[t]["columnas"] if c.get("ref")]
partes = [(t, c["nombre"]) for t in MODELO
          for c in MODELO[t]["columnas"] if c.get("es_parte_de")]
enums = columnas_de_tipo("Enum")
latlong = columnas_de_tipo("LatLong")
sin_valores = ["%s.%s" % (t, c["nombre"]) for t in MODELO
               for c in MODELO[t]["columnas"]
               if c["tipo"] == "Enum" and not c.get("valores")]

w("# Reglas del modelo de datos")
w("")
w("**Cualquier cambio en el modelo, en la plantilla o en la aplicación tiene que respetarlas.**")
w("")
w("**Generado** por `scripts/generar_reglas_datos.py`. No editar a mano: las listas salen de")
w("`scripts/modelo_objetivo.py`, así que la única forma de que este documento mienta es que mienta")
w("el modelo.")
w("")
w("Ninguna de estas reglas es una preferencia de estilo. **Todas salieron de un fallo que llegó a")
w("producción o estuvo a punto**, y cada una lleva escrito cuál, porque el motivo es lo que hace")
w("que alguien la respete en vez de saltársela.")
w("")
w("La columna que más importa es la última: **quién la hace cumplir**. Una regla que no comprueba")
w("nadie es una intención, no una regla.")
w("")
w("---")
w("")
w("## 1. Cómo AppSheet decide el tipo de una columna, y qué se hace al respecto")
w("")
w("**AppSheet no lee el tipo de la hoja: lo infiere**, del nombre de la cabecera y del contenido de")
w("las filas. Subir el Excel arregla la hoja, no la aplicación — son dos sitios distintos, y")
w("reimportar no cambia la inferencia porque los datos son los mismos.")
w("")
w("Ver `BASE_CONOCIMIENTO_APPSHEET.md` §13, con la cita oficial.")
w("")

w("### R-01 · Toda clave es alfanumérica con prefijo")
w("")
w("**Por qué.** AppSheet tipa la clave según la mayoría de sus valores. Si son `1`, `2`, `3` la")
w("tipa `Number`, y entonces **una fila con clave alfanumérica se descarta sin avisar**. Pasó el")
w("2026-08-10: `USR_Usuarios` tenía diez claves numéricas y una generada con `UNIQUEID`, y un")
w("técnico no existía para la aplicación. Se vio porque la API devolvía 10 filas y la hoja tenía 11.")
w("")
w("**Y no es solo la clave.** `LST_ValoresLista` mezclaba 4 numéricas con 104 de texto: AppSheet")
w("habría descartado las cuatro, que eran los valores del desplegable del único checklist acordado.")
w("")
w("Las claves de hoy, derivadas de la plantilla:")
w("")
w("```")
w("ACT-0001   TIP-001   UNF-01   SED-001   USR-001   ROL-01")
w("EST-01     FRE-01    CAL-01   SEC-01    TPR-01")
w("OT-0001    MOT-01    FAL-01   ASG-01    PLA-001   FRM_SOS   SOS001   UMBRAL_GPS")
w("```")
w("")
w("**Quién la hace cumplir:** `F-20` de `verificar_faseA.py`, que falla si una clave mezcla")
w("numéricas y de texto, y avisa si es enteramente numérica.")
w("")

w("### R-02 · Una columna de coordenada lleva `_LatLong` en el nombre")
w("")
w("**Por qué.** AppSheet infiere `LatLong` cuando la cabecera contiene `latlong` o `geolocation`.")
w("`Ubicacion` no dispara nada, así que entraba como `Text` — y `DISTANCE()` no funciona sobre")
w("texto. Son nombres feos a cambio de que el tipo entre solo en cada reconstrucción.")
w("")
w("Las %d de hoy:" % len(latlong))
w("")
for c in latlong:
    w("- `%s`" % c)
w("")
w("**Quién la hace cumplir:** nadie todavía. Es una regla que hay que recordar al declarar una")
w("columna de coordenada nueva.")
w("")

w("### R-03 · Las referencias no se infieren nunca: se ponen a mano")
w("")
w("**Por qué.** AppSheet infiere `Ref` cuando el nombre de una columna se parece al de una tabla")
w("existente. Nuestras tablas llevan prefijo —`UNF_UnidadesFuncionales`, no `UnidadFuncional`—, así")
w("que el parecido se rompe. **Es el coste de la convención y a la vez su protección**: impide que")
w("AppSheet invente referencias.")
w("")
w("Y explica las tres trampas que costaron un día: `CHK_Checklists.ActivoID`,")
w("`OT_OrdenesTrabajo.FormularioID` y `CHD_ChecklistDetalle.TipoRespuestaID` **sí** se convertían")
w("solas, porque su nombre coincidía con la clave de otra tabla.")
w("")
w("Hoy son **%d referencias**, %d de ellas con `IsPartOf`." % (len(refs), len(partes)))
w("")
w("**Quién la hace cumplir:** `V-05` de `validar_modelo.py` comprueba que ninguna quede huérfana en")
w("el modelo. **Que estén puestas en la aplicación no lo comprueba nadie**: es trabajo de editor y")
w("de `PRUEBA-003`.")
w("")

w("---")
w("")
w("## 2. Cómo se cambia el modelo sin romper lo que ya hay")
w("")

w("### R-04 · Una referencia que resuelve puede apuntar a lo que no es")
w("")
w("**Por qué.** Es el fallo que más veces se ha repetido, y las tres veces lo encontró una persona:")
w("")
w("- El inventario sintético arrancó en `ActivoID 1` y **reescribió los 34 activos reales**. Las")
w("  órdenes pasaron a apuntar a otro equipo, y la referencia seguía resolviendo.")
w("- Nueve familias del Plan Maestro colgaban del tipo de otra cosa: **78 activos con el checklist")
w("  equivocado**, y `TipoActivoID` apuntaba a una fila que existe.")
w("- 113 activos estaban en la unidad funcional equivocada, porque las UF se repartían en cuartos")
w("  iguales y no lo son.")
w("")
w("**La comprobación de huérfanos contesta «apunta a algo», nunca «apunta a lo correcto».**")
w("")
w("**Quién la hace cumplir:** nadie de forma general. `catalogo_tipos.comprobar()` cubre el caso de")
w("los tipos. Para lo demás, hay que derivarlo del dominio y comprobarlo a propósito.")
w("")

w("### R-05 · Cambiar una clave se propaga solo, nunca a mano")
w("")
w("**Por qué.** Al resembrar las once claves numéricas, el cambio afectó a **2.502 valores de")
w("referencia** repartidos por diez tablas. Hacerlo a mano sería garantizar el olvido de alguna, y")
w("una referencia olvidada apunta a una clave que ya no existe.")
w("")
w("`generar_plantilla.py` lo hace derivando de `MODELO` qué columnas apuntan a la tabla que cambia.")
w("")
w("**Quién la hace cumplir:** `verificar_faseA.py`, que detecta huérfanos entre la hoja y sus")
w("tablas destino.")
w("")

w("### R-06 · El generador tiene que dar lo mismo dos veces")
w("")
w("**Por qué.** Al resembrar las claves, la garantía de catálogo buscaba las filas **por clave**; la")
w("resiembra cambiaba esa clave; en la pasada siguiente las volvía a añadir. `SED_Sedes` acabó con")
w("las seis edificaciones **duplicadas** y cada ejecución habría añadido seis más.")
w("")
w("**Pasó los cuatro verificadores que había**, porque todos miran un archivo y el defecto solo")
w("existe entre dos ejecuciones. De ahí la regla derivada: **el catálogo se empareja por la clave")
w("natural —el nombre—, nunca por la clave generada.**")
w("")
w("**Quién la hace cumplir:** `verificar_reproducible.py`, que genera dos veces y compara celda a")
w("celda.")
w("")

w("### R-07 · El dato y la prosa no comparten campo")
w("")
w("**Por qué.** Los valores de un `Enum` vivían dentro de su nota, y el generador del manual partía")
w("la nota por comas: publicó un valor llamado `Baja. Pondera la disponibilidad de D-13` y otro con")
w("un párrafo entero dentro. Ahora `valores=` es el dato y `nota=` es la prosa.")
w("")
w("Hoy hay **%d columnas `Enum`**%s." % (len(enums),
     ", y todas declaran sus valores" if not sin_valores
     else ", y %d sin declarar: %s" % (len(sin_valores), ", ".join("`%s`" % c for c in sin_valores))))
w("")
w("**Quién la hace cumplir:** el generador del manual, que ya no inventa valores: si faltan, lo")
w("dice en vez de deducirlos.")
w("")

w("### R-08 · Una columna dice lo que es, no lo que se le parece")
w("")
w("**Por qué.** `ACT_Activos.PR` guardaba el kilómetro lineal del proyecto, que es un **PK**. Y")
w("`UNF_UnidadesFuncionales.PRInicial` lo mismo. La columna prometía una referencia de INVÍAS y")
w("contenía otra cosa, y nadie lo veía porque había un valor y parecía correcto.")
w("")
w("**El PR y el PK son dos datos distintos y todo elemento tiene ambos**: el PK es lineal y continuo")
w("del proyecto; el PR es de INVÍAS, pertenece a un tramo y reinicia en cada uno. El corredor")
w("atraviesa tres rutas —`55CN03`, `5607`, `5608`— y **tiene dos puntos distintos llamados")
w("`PR 0+000`**, separados por unos 50 km.")
w("")
w("**Quién la hace cumplir:** nadie. Es la regla más difícil de mecanizar, porque el defecto es")
w("semántico: la comprobación ve un valor y no sabe si es el que la columna promete.")
w("")

w("### R-09 · Un aplazamiento sin fecha no es un aplazamiento")
w("")
w("**Por qué.** `USR_Usuarios.SedeID` estuvo cuatro días declarada `Ref` obligatoria mientras la")
w("especificación la daba por descartada. `D-04` lo detectaba **en cada ejecución**, pero la marca")
w("`'paso 1'` degradaba el fallo a aviso y no tenía fecha, así que nunca vencía.")
w("")
w("**Quién la hace cumplir:** `D-04` de `verificar_documentos.py`, que ahora exige `AAAA-MM-DD` y")
w("vuelve a fallar el día que pasa.")
w("")

w("### R-10 · Los identificadores viven en un solo sitio")
w("")
w("**Por qué.** La aplicación y la hoja estaban escritas a mano en 37 documentos y 10 scripts, y el")
w("sistema se reconstruyó tres veces en cuatro días: nunca se perseguían todos. Se llegó a tener")
w("cinco aplicaciones y tres hojas mencionadas por el repositorio, con la portada ofreciendo un")
w("enlace que daba 404.")
w("")
w("**Quién la hace cumplir:** nadie automáticamente. `scripts/sistema.py` es la fuente, y su lista")
w("`SUPERADOS` permite reconocer los abandonados.")
w("")

w("---")
w("")
w("## 3. Lo que ninguna regla evita")
w("")
w("Al dar de alta o regenerar una tabla en AppSheet **hay que entrar a `Data > Columns` y recorrer")
w("la columna `TYPE` contra la ficha del anexo de `MANUAL_DESPLIEGUE.md`**. No hay atajo:")
w("")
w("| Qué | Cuántos | Por qué no se infiere |")
w("|---|---|---|")
w("| Referencias `Ref` | %d | El prefijo de la tabla rompe el parecido de nombre |" % len(refs))
w("| `IsPartOf` | %d | Es una decisión de borrado en cascada, no un tipo |" % len(partes))
w("| Valores de `Enum` | %d columnas | AppSheet no sabe qué valores son válidos |" % len(enums))
w("| `ChangeTimestamp` | %d | Nunca se infiere; llega como texto |" % len(columnas_de_tipo("ChangeTimestamp")))
w("| Expresiones | %d reglas | `Valid_If`, `Editable_If`, `Initial value`, bots |" % len(REGLAS))
w("")
w("**Y una trampa propia de las tablas vacías.** Las %d que llegan sin filas —las de movimiento—" % len(CLAVE_GENERADA))
w("no le dan a AppSheet ningún dato del que inferir la clave, así que la elige a ciegas. Son las")
w("mismas que generan su clave con `UNIQUEID()`, es decir alfanumérica: **si alguna quedó `Number`,")
w("cada fila que cree un técnico se perderá igual que se perdió aquel usuario.**")
w("")
for t in sorted(CLAVE_GENERADA):
    w("- `%s`" % t)
w("")
w("**Se puede sondear sin abrir el editor**: insertar por API una fila con clave alfanumerica y")
w("**leerla de vuelta** antes de borrarla. Si regresa literal, la columna es `Text`. Metodo y sus")
w("limites en `BASE_CONOCIMIENTO_APPSHEET.md` seccion 14 — con la advertencia de que la API tiene")
w("mas permisos que la aplicacion: **no ve el `Deletes` retirado**, asi que sobre una tabla con")
w("historico ese sondeo es justo el fallo contra el que el sistema esta disenado.")
w("")

with open(SALIDA, "w", encoding="utf-8") as f:
    f.write("\n".join(L) + "\n")

print("Generado:", SALIDA)
print("%d reglas · %d referencias · %d Enum · %d LatLong · %d tablas con clave generada"
      % (10, len(refs), len(enums), len(latlong), len(CLAVE_GENERADA)))
