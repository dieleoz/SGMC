# -*- coding: utf-8 -*-
"""Genera docs/PROMPT_CABLEADO.md: el encargo para quien cablee la aplicacion.

Autocontenido y DERIVADO. Las listas salen de scripts/modelo_objetivo.py, asi
que no pueden envejecer ni contradecir al modelo. Es la leccion de CLAUDE.md
7.9: una instruccion que exige criterio se ejecuta mal, de modo que aqui no hay
nada que deducir -cada referencia lleva su tabla, su columna, su destino y si
lleva IsPartOf-.

Uso:  python scripts/generar_prompt_cableado.py
"""
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "scripts"))

from modelo_objetivo import MODELO, REGLAS, CLAVE_GENERADA
from sistema import APP_NOMBRE, APP_ID, APP_URL, HOJA_NOMBRE

SALIDA = os.path.join(RAIZ, "docs", "PROMPT_CABLEADO.md")

L = []
w = L.append

refs = [(t, c["nombre"], c["ref"], bool(c.get("es_parte_de")))
        for t in MODELO for c in MODELO[t]["columnas"] if c.get("ref")]
partes = [r for r in refs if r[3]]
enums = [(t, c["nombre"], c.get("valores"))
         for t in MODELO for c in MODELO[t]["columnas"] if c["tipo"] == "Enum"]
stamps = [(t, c["nombre"]) for t in MODELO for c in MODELO[t]["columnas"]
          if c["tipo"] == "ChangeTimestamp"]
latlong = [(t, c["nombre"]) for t in MODELO for c in MODELO[t]["columnas"]
           if c["tipo"] == "LatLong"]

w("# Encargo de cableado de la aplicación")
w("")
w("**Autocontenido. Cópialo íntegro desde la línea siguiente.**")
w("")
w("**Generado** por `scripts/generar_prompt_cableado.py`. No editar a mano: las listas salen de")
w("`scripts/modelo_objetivo.py`.")
w("")
w("---")
w("")
w("Vas a cablear la aplicación **`%s`** de Google AppSheet. Las %d tablas ya están dadas de alta"
  % (APP_NOMBRE, len(MODELO)))
w("sobre la hoja `%s`, y los datos ya están cargados. **No hay que subir ningún Excel ni tocar la"
  % HOJA_NOMBRE)
w("hoja**: todo lo que sigue vive dentro del editor.")
w("")
w("```")
w("%s" % APP_URL)
w("```")
w("")
w("> Si ese enlace da 404, entra por el listado de `https://www.appsheet.com` y abre `%s`."
  % APP_NOMBRE)
w("")

w("## Cómo cambiar un tipo sin morir a base de clics")
w("")
w("Los desplegables de la columna `TYPE` en *Data > Columns* son **`<select>` nativos del")
w("navegador**, no widgets propios de AppSheet. Se pueden asignar de forma determinista.")
w("")
w("**Y la parte que no es obvia: cambiar el valor del control NO basta.** Hay que confirmar que la")
w("aplicación lo recogió, y la señal es que **el botón `SAVE` de la cabecera pasa de gris a azul**.")
w("Si sigue gris, el cambio no llegó al modelo interno del editor y se pierde al recargar. Después")
w("de guardar vuelve a gris: ese ciclo —gris, azul, gris— es lo que hay que ver en cada tabla.")
w("")
w("**Guarda al terminar cada tabla, no al final.** La interfaz deja de protegerte cuando la")
w("automatizas: un valor equivocado aplicado en serie se aplica en serie.")
w("")

w("## Paso 1 — Retirar el borrado. ANTES que las referencias")
w("")
w("En *Data > Tables*, para `OT_OrdenesTrabajo` y `MAN_Mantenimientos`, en **Are updates allowed**:")
w("")
w("```")
w("Updates  si        Adds  si        Deletes  NO")
w("```")
w("")
w("**Por qué va primero y no después.** El paso 2 marca `IsPartOf` en %d referencias, y eso es"
  % len(partes))
w("**borrado en cascada**: borrar un mantenimiento se lleva sus fotografías, su firma y su")
w("checklist. Eso solo es seguro porque el mantenimiento nunca se borra. **La cascada existe desde")
w("el momento en que se marca la primera; la protección tiene que estar puesta ya.**")
w("")

w("## Paso 2 — Las %d referencias" % len(refs))
w("")
w("Para cada una: *Data > Columns > la tabla > la columna > `TYPE` = `Ref`*, y en las propiedades de")
w("la columna, **`Source table`** = la tabla destino.")
w("")
w("**Ninguna se crea sola.** AppSheet infiere `Ref` por parecido entre el nombre de la columna y el")
w("de una tabla, y las nuestras llevan prefijo —`UNF_UnidadesFuncionales`, no `UnidadFuncional`—,")
w("así que el parecido se rompe. Hay que ponerlas las %d." % len(refs))
w("")
w("> **Cuántas faltan hoy, este documento no lo sabe.** Sale del modelo, así que describe el destino")
w("> y no el estado: seguirá diciendo %d el día que estén las %d puestas. Antes de empezar, pregúntaselo"
  % (len(refs), len(refs)))
w("> a la aplicación:")
w(">")
w("> ```bash")
w("> python scripts/auditar_cableado.py")
w("> ```")
w(">")
w("> Emite [`CORRECCIONES_CABLEADO.md`](CORRECCIONES_CABLEADO.md) con **lo que quede pendiente**, y")
w("> distingue tres cosas que es fácil confundir: la que está mal, la que falta, y la que **no se")
w("> puede ver** porque su tabla destino está vacía. Dar por buena una referencia que nadie ha")
w("> mirado es como se llegó a tener `TipoActivoID` apuntando a la tabla de sedes.")
w("")
w("| Tabla | Columna | `Source table` | `IsPartOf` |")
w("|---|---|---|---|")
for t, col, destino, parte in refs:
    w("| `%s` | `%s` | `%s` | %s |"
      % (t, col, destino, "**SÍ**" if parte else "no"))
w("")
w("> **Las %d de `IsPartOf` y la que NO lo lleva.**" % len(partes))
w(">")
for t, col, destino, _p in partes:
    w("> - `%s.%s` hacia `%s`" % (t, col, destino))
w(">")
w("> **`MAN_Mantenimientos.OTID` va DESMARCADO.** Es la trampa de este paso: parece que debería")
w("> llevarlo por simetría con las otras, y no. Con `IsPartOf`, borrar una orden se llevaría el")
w("> mantenimiento entero y con él toda su evidencia.")
w("")

w("## Paso 3 — Los tipos que no se infieren")
w("")
w("### Las %d marcas de tiempo del servidor" % len(stamps))
w("")
w("Tipo **`ChangeTimestamp`**. AppSheet no lo infiere nunca: llegan como texto.")
w("")
for t, col in stamps:
    w("- `%s.%s`" % (t, col))
w("")
w("**Por qué importa.** `ChangeTimestamp` la escribe el servidor. Un `Initial value = NOW()` lo pone")
w("el teléfono, y el usuario puede cambiar la hora del teléfono. Sin esto, **la hora de cada")
w("fotografía y de cada firma no prueba nada**, que es justo lo que el sistema existe para sostener.")
w("")
w("### Los %d desplegables" % len(enums))
w("")
w("Tipo `Enum`, y **los valores exactos**. No los deduzcas ni los traduzcas: son estos.")
w("")
w("| Tabla | Columna | Valores |")
w("|---|---|---|")
for t, col, valores in enums:
    w("| `%s` | `%s` | %s |"
      % (t, col, " · ".join("`%s`" % v for v in valores) if valores
         else "**sin declarar en el modelo. Pregunta antes de inventarlos**"))
w("")
w("### Las %d coordenadas" % len(latlong))
w("")
w("Deberían haber entrado ya como `LatLong`, porque su nombre lleva la palabra que AppSheet")
w("reconoce. **Compruébalas igual**, y si alguna salió `Text`, cámbiala: `DISTANCE()` no funciona")
w("sobre texto.")
w("")
for t, col in latlong:
    w("- `%s.%s`" % (t, col))
w("")

w("## Paso 4 — Las %d reglas" % len(REGLAS))
w("")
w("Están **enteras y sin cortar** en [`sdd/RECONSTRUCCION_EXPRESIONES.md`](sdd/RECONSTRUCCION_EXPRESIONES.md),")
w("con su tabla, su columna y su tipo —`Valid_If`, `Initial value`, `App formula`, bot—. Cópialas de")
w("ahí. **No las escribas de memoria ni las adaptes.**")
w("")
w("La que más se olvida es **RG-19**, el umbral de GPS con su `OR(ISBLANK(...))`: sin ese `ISBLANK`,")
w("si alguien borra la fila del parámetro **todos los cierres salen limpios y nadie se entera**.")
w("")

w("## Paso 5 — Comprobar, y aquí está lo que solo se puede ver ahora")
w("")
w("**Las %d tablas que llegaron vacías eligieron su clave a ciegas**, porque AppSheet la infiere de"
  % len(CLAVE_GENERADA))
w("los datos y no había. Y son justo las que generan clave con `UNIQUEID()`, es decir alfanumérica:")
w("**si alguna quedó `Number`, cada fila que cree un técnico se perderá sin aviso.**")
w("")
for t in sorted(CLAVE_GENERADA):
    w("- `%s`" % t)
w("")
w("Abre cada una y confirma que su clave es **`Text`**.")
w("")
w("Después, las pruebas de [`sdd/PRUEBA-003-despliegue.md`](sdd/PRUEBA-003-despliegue.md).")
w("")

w("## Qué reportar al terminar")
w("")
w("1. **Cuántas referencias pusiste**, y si alguna no te dejó.")
w("2. **Las %d de `IsPartOf`**, y confirmación de que `MAN_Mantenimientos.OTID` quedó DESMARCADA."
  % len(partes))
w("3. **`Deletes` retirado** en las dos tablas.")
w("4. **Las claves de las %d tablas vacías**: qué tipo tenía cada una." % len(CLAVE_GENERADA))
w("5. **Cualquier tipo que encontraras distinto** del que dice este documento. Eso es un hallazgo,")
w("   no un estorbo: significa que la inferencia hizo algo que no esperábamos.")
w("")

w("## Lo que NO debes hacer")
w("")
w("- **No subas ningún Excel ni toques la hoja.** El dato está bien; lo que falta es configuración.")
w("- **No pruebes expresiones escribiéndolas dentro de una columna.** Se prueban en el Asistente de")
w("  Expresiones, que solo evalúa, y se cierra **sin dar a `Done`**. Escribir una expresión dentro de")
w("  una columna la convierte en configuración activa: ya ocurrió una vez y dejó una `App formula`")
w("  escribiendo coordenadas dentro de una columna retirada.")
w("- **No borres ninguna columna.**")
w("- **No publiques.** Ninguna de las coordenadas de los activos es real, así que en campo la")
w("  comprobación de distancia no significa nada todavía.")

with open(SALIDA, "w", encoding="utf-8") as f:
    f.write("\n".join(L) + "\n")

print("Generado:", SALIDA)
print("%d referencias · %d IsPartOf · %d Enum · %d ChangeTimestamp · %d LatLong · %d reglas"
      % (len(refs), len(partes), len(enums), len(stamps), len(latlong), len(REGLAS)))
