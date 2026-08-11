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
from inferencia import clasificar, etiquetas_pendientes
import json as _json

# Las tablas que llegaron VACIAS: AppSheet eligio su clave sin un solo dato.
_foto = os.path.join(RAIZ, "BD", "instantaneas", "antes-de-fase-c.json")
_vacias = []
if os.path.exists(_foto):
    _d = _json.load(open(_foto, encoding="utf-8"))
    _entra = {}
    for _t in MODELO:
        for _c in MODELO[_t]["columnas"]:
            if _c.get("ref"):
                _entra[_c["ref"]] = _entra.get(_c["ref"], 0) + 1
    _vacias = [(t, next(c["nombre"] for c in MODELO[t]["columnas"] if c.get("pk")),
                _entra.get(t, 0))
               for t in sorted(MODELO) if not _d.get(t)]
from lectura_de_vuelta import bloque
from alcance_reglas import por_columna

clases = clasificar()

# La atribucion va por (tabla, columna), no por nombre suelto. Hacerlo por
# nombre daba las 23 columnas `Activo` de 23 tablas con RG-04 y RG-16 encima
# -94 columnas "con regla" donde hay 36-, y esta lista ORDENA el trabajo: una
# columna mal tipada con una regla encima rompe la regla en silencio, asi que
# inflarla entierra las que de verdad importan.
reglas_de = por_columna()

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
w(bloque("permisos"))
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

if _vacias:
    w("## Paso 2 — Las claves de las %d tablas que llegaron vacías" % len(_vacias))
    w("")
    w("**Sin un solo dato, AppSheet elige la clave a ciegas — y elige `_RowNumber`.** Contra una")
    w("clave que no es la declarada, ninguna referencia resuelve de forma estable, y el error que")
    w("acaba dando es este:")
    w("")
    w("```")
    w("That Table or Slice uses RowNumber as a key which is not a stable key.")
    w("```")
    w("")
    w("En *Data > Columns*, marca **`Key`** en la columna que dice la tabla y **desmarca `_RowNumber`**:")
    w("")
    w("| Tabla | `Key` | ¿AppSheet avisará? |")
    w("|---|---|---|")
    for _t, _pk, _n in _vacias:
        w("| `%s` | **`%s`** | %s |" % (_t, _pk,
          "sí, %d referencias la apuntan" % _n if _n
          else "**no. Nadie la referencia, así que falla en silencio**"))
    w("")
    w("> **Solo %d de las %d avisan.** AppSheet protesta cuando una tabla referenciada tiene clave"
      % (sum(1 for _, _, n in _vacias if n), len(_vacias)))
    w("> inestable; de las que nadie referencia no dice nada. Hazlas las %d de una vez, o las cinco"
      % len(_vacias))
    w("> restantes se descubrirán de una en una, cuando alguien intente usarlas.")
    w("")

w("## Paso 2 — Las %d referencias" % len(refs))
w("")
w(bloque("referencias"))
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

w("## Paso 3bis — Los tipos. **Las %d, no una lista de excepciones**" % sum(len(MODELO[t]["columnas"]) for t in MODELO))
w("")
w("**Este paso se llamaba «los tipos que no se infieren» y enumeraba 61 columnas.** Era una lista")
w("blanca de excepciones sobre un default que se presumía bueno: las otras 150 se daban por")
w("correctas por omisión. La plataforma garantiza lo contrario, y el precio fue `RG-03` —bien")
w("escrita, bien colocada— sobre una columna que AppSheet tipó `Text` cuando el modelo dice")
w("`Yes/No`. Comparar texto contra el booleano `TRUE` es **siempre falso y no da error**: el motivo")
w("de excepción no se pide nunca. La regla existe y es decorativa.")
w("")
w("Y el «qué reportar» cerraba el bucle en falso —«cualquier tipo distinto del que dice este")
w("documento»—: **nadie puede reportar una diferencia contra un valor que nunca se le dio.**")
w("")
w("### Las %d que NADIE pone si no las pones tú" % len(clases["a mano"]))
w("")
w("Ningún contenido de la hoja las produce, o su propio nombre empuja a AppSheet al tipo")
w("equivocado. **Están ordenadas por las reglas que dependen de cada una**, que es lo que ordena el")
w("trabajo: una columna mal tipada sin regla encima molesta al usuario; con una regla encima")
w("**rompe la regla en silencio**.")
w("")
w("| Tabla | Columna | `TYPE` | Reglas | Por qué no se consigue sola |")
w("|---|---|---|---|---|")
for t, c, motivo in sorted(clases["a mano"],
                           key=lambda x: (-len(reglas_de.get((x[0], x[1]["nombre"]), ())), x[0], x[1]["nombre"])):
    rr = reglas_de.get((t, c["nombre"]), set())
    detalle = ""
    if c.get("ref"):
        detalle = " → `%s`" % c["ref"]
    elif c.get("valores"):
        detalle = " · valores: %s" % " · ".join("`%s`" % v for v in c["valores"])
    w("| `%s` | `%s` | **`%s`**%s | %s | %s |"
      % (t, c["nombre"], c["tipo"], detalle,
         ", ".join("`%s`" % x for x in sorted(rr)) if rr else "—", motivo))
w("")

w("### Las %d que el NOMBRE consigue" % len(clases["nombre"]))
w("")
w("Deberían haber entrado bien porque su nombre lleva la palabra que AppSheet reconoce.")
w("**Compruébalas igual**: es una heurística, no una garantía.")
w("")
for t, c, motivo in sorted(clases["nombre"], key=lambda x: (x[0], x[1]["nombre"])):
    w("- `%s.%s` → **`%s`**  ·  %s" % (t, c["nombre"], c["tipo"], motivo))
w("")

w(bloque("tipos"))
w("")
w("### Las %d que dependen del contenido" % len(clases["contenido"]))
w("")
w("AppSheet debería acertar leyendo los valores — **cuando los hay**. Las de una tabla vacía no")
w("tienen contenido que leer, así que estas también hay que mirarlas ahí. La lista completa, tabla")
w("por tabla, está en [`TIPOS_ESPERADOS.md`](TIPOS_ESPERADOS.md).")
w("")
w("> **El caso que desarma la confianza en el contenido:** `SED_Sedes.TramoINVIAS` tenía un valor")
w("> real y representativo, `5607`, y AppSheet la tipó **`Number`**. El modelo dice `Text`, y el día")
w("> que operación escriba `55CN03` no cabrá. Tener el dato correcto no basta.")
w("")

w("## Paso 4 — La etiqueta de cada tabla, que no la declaraba nadie")
w("")
w(bloque("etiqueta"))
w("")
w("`Label` es la columna que **representa una fila en las listas y en los desplegables**. No estaba")
w("en el modelo ni en ningún documento: la elegía AppSheet, y elige la primera columna de texto, que")
w("casi siempre es la clave.")
w("")
w("No rompe nada, y por eso nadie lo miraba. Lo que pasa es que el técnico abre el desplegable para")
w("asignar una orden y ve **`USR-001`, `USR-004`** en vez de los nombres.")
w("")
w("En *Data > Columns*, marca la casilla **`Label`** de estas columnas:")
w("")
w("| Tabla | Referencias que la apuntan | `Label` |")
w("|---|---|---|")
for _t, _e, _n in etiquetas_pendientes():
    w("| `%s` | %d | %s |" % (_t, _n,
      "**`%s`**" % _e if _e else "*ninguna: la clave la identifica, y está decidido así*"))
w("")
w("> Las tres sin etiqueta **no son un hueco**: una orden se identifica por su número y su fecha,")
w("> una ejecución por su orden y su hora. Está decidido, no olvidado.")
w("")

w("## Paso 5 — Las %d reglas" % len(REGLAS))
w("")
w("Están **enteras y sin cortar** en [`sdd/RECONSTRUCCION_EXPRESIONES.md`](sdd/RECONSTRUCCION_EXPRESIONES.md),")
w("con su tabla, su columna y su tipo —`Valid_If`, `Initial value`, `App formula`, bot—. Cópialas de")
w("ahí. **No las escribas de memoria ni las adaptes.**")
w("")
w("La que más se olvida es **RG-19**, el umbral de GPS con su `OR(ISBLANK(...))`: sin ese `ISBLANK`,")
w("si alguien borra la fila del parámetro **todos los cierres salen limpios y nadie se entera**.")
w("")

w("## Paso 6 — Comprobar, y aquí está lo que solo se puede ver ahora")
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
