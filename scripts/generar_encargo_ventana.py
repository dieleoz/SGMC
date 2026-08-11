# -*- coding: utf-8 -*-
"""Genera docs/ENCARGO_VENTANA.md: lo que hay que cerrar ANTES de poblar.

Por que existe
--------------
Ocho tablas estan hoy en CERO filas, y esa vacuidad no es un estado neutro: es
lo que hace que corregir un tipo o una clave cueste un clic. Con una sola fila
dentro, cada correccion pasa a ser una migracion.

El primer registro de prueba la cierra. Y la cierra **para siempre**, porque
esas tablas son transaccionales: una vez que entran ordenes y mantenimientos, no
vuelven a estar vacias nunca.

Este encargo reune lo unico que tiene sentido hacer en esa ventana, y deja fuera
todo lo demas a proposito.

Lo que NO va aqui, y por que
----------------------------
  UNF_UnidadesFuncionales y USR_Usuarios  tienen filas: su ventana ya se cerro
                                          hace tiempo y pueden esperar
  los bots                                no dependen de la ventana
  RG-04 y RG-05, los filtros              van los ULTIMOS: al ponerlos la API
                                          deja de ver esas tablas y ni el
                                          auditor ni las instantaneas pueden
                                          volver a mirarlas

Uso:  python scripts/generar_encargo_ventana.py
"""
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "scripts"))

from modelo_objetivo import MODELO, REGLAS
from inferencia import clasificar, etiquetas_virtuales
from sistema import APP_NOMBRE, APP_URL
from navegacion_editor import mapa_markdown

SALIDA = os.path.join(RAIZ, "docs", "ENCARGO_VENTANA.md")

VACIAS = ("OT_OrdenesTrabajo", "MAN_Mantenimientos", "PLA_PlanMantenimiento",
          "CHK_Checklists", "CHD_ChecklistDetalle", "FOT_Fotografias",
          "FIR_Firmas", "NOV_Novedades")

# Solo las que hacen de Label: no toda columna virtual lo es. Se pregunta a
# inferencia.py en vez de deducirlo de la forma, que es lo que hacia que
# EstaVencida saliera aqui llamandose «Etiqueta».
virtuales = [(r["tabla"], n, r["expresion"]) for r, n in etiquetas_virtuales(REGLAS)]
clases = clasificar()
pendientes = {}
for t, c, motivo in clases["a mano"]:
    if t in VACIAS:
        pendientes.setdefault(t, []).append(c)

L = []
w = L.append

w("# Encargo: cerrar la ventana barata")
w("")
w("**Autocontenido. Cópialo íntegro desde la línea siguiente.**")
w("")
w("**Generado** por `scripts/generar_encargo_ventana.py`. No editar a mano.")
w("")
w("---")
w("")
w("Trabajas en el editor de AppSheet de **`%s`**." % APP_NOMBRE)
w("")
w("```")
w("%s" % APP_URL)
w("```")
w("")

w("## Por qué esto es urgente y lo demás no")
w("")
w("**%d tablas están hoy en CERO filas**, y esa vacuidad no es un estado neutro: es lo que hace que"
  % len(VACIAS))
w("corregir un tipo o una clave cueste **un clic**. Con una sola fila dentro, cada corrección pasa a")
w("ser una migración.")
w("")
w("Y el primer registro la cierra **para siempre**: son tablas transaccionales, así que una vez que")
w("entren órdenes y mantenimientos no vuelven a estar vacías nunca.")
w("")
w("Todo lo que sigue vive dentro de esa ventana. Lo que no está aquí es porque no.")
w("")

w("## Paso 1 — Las %d columnas virtuales `Etiqueta`" % len(virtuales))
w("")
w("**No son columnas de la hoja.** Son columnas **virtuales**: las calcula AppSheet y no se guardan")
w("en el Sheets. Es lo que Google documenta para una etiqueta compuesta de varias columnas.")
w("")
w("Existen porque `OTID` y `PlanID` pasaron a `UNIQUEID()`: una orden ya no se llama `OT-0042` sino")
w("`a3f9c2e1`, y sin etiqueta el técnico vería eso en cada desplegable.")
w("")
w("En *Data > Columns > la tabla*, botón **`Add virtual column`**:")
w("")
w("| Tabla | Nombre | `App formula` |")
w("|---|---|---|")
for t, n, e in sorted(virtuales):
    w("| `%s` | **`%s`** | `%s` |" % (t, n, e))
w("")
w("Y en esa misma columna virtual, dos cosas que la documentación de Google prescribe y que es fácil")
w("saltarse:")
w("")
w("- **`Show?` activo.** Sin eso AppSheet no acepta que sea etiqueta.")
w("- **`Label` marcado** — y si la tabla ya tenía otra columna con `Label`, **desmárcala primero**.")
w("  Solo puede haber una por tabla.")
w("")

total = sum(len(v) for v in pendientes.values())
w("## Paso 2 — Cotejar %d tipos, y dejar constancia" % total)
w("")
w("**Esto no es para cambiarlos: es para mirarlos.** Lo más probable es que ya estén, porque una")
w("sesión anterior recorrió estas tablas. Pero *reportado* no es *verificado*, y de eso este")
w("proyecto lleva cuatro informes de «hecho» que no lo estaban.")
w("")
w("**Anota lo que veas aunque coincida.** No hay comando que lo recupere después: la API de AppSheet")
w("devuelve filas, no esquema. Tu anotación es la única evidencia que va a existir.")
w("")
for t in sorted(pendientes):
    w("### `%s` — %d columnas" % (t, len(pendientes[t])))
    w("")
    w("| Columna | Debe ser |")
    w("|---|---|")
    for c in sorted(pendientes[t], key=lambda x: x["nombre"]):
        extra = ""
        if c.get("ref"):
            extra = " → `%s`" % c["ref"]
        elif c.get("valores"):
            extra = " · valores: %s" % " · ".join("`%s`" % v for v in c["valores"])
        w("| `%s` | **`%s`**%s |" % (c["nombre"], c["tipo"], extra))
    w("")

w("## Lo que NO entra, y por qué")
w("")
w("| | Por qué queda fuera |")
w("|---|---|")
w("| `UNF_UnidadesFuncionales` y `USR_Usuarios` | Tienen filas. Su ventana se cerró hace tiempo, así que pueden esperar |")
w("| Los bots | No dependen de la ventana |")
w("| `RG-04` y `RG-05`, los `Security Filter` | Van **los últimos**. Al ponerlos, la API deja de devolver las filas de esa tabla y ni `auditar_cableado.py` ni `instantanea.py` pueden volver a mirarla |")
w("| `RG-02`, `RG-19`, `RG-03` | `ESPEC-004` está bloqueada. `RG-02` usa una función que no existe en AppSheet |")
w("")

w(mapa_markdown())
w("")

w("## Antes de empezar y al terminar")
w("")
w("```bash")
w("python scripts/instantanea.py guardar antes-de-la-ventana")
w("```")
w("")
w("Un cambio de tipo **puede escribir en los datos**. Ya pasó: convertir una columna a `Enum`")
w("reescribió una celda añadiéndole un espacio al final. Sin foto previa no hay vuelta atrás.")
w("")
w("Al terminar:")
w("")
w("```bash")
w("python scripts/instantanea.py guardar despues-de-la-ventana")
w("python scripts/instantanea.py comparar antes-de-la-ventana despues-de-la-ventana")
w("python scripts/auditar_cableado.py")
w("```")
w("")
w("La comparación debe decir **NINGUNA CELDA CAMBIO**, y el auditor **0 correcciones**. Si dicen")
w("otra cosa, para y reporta la salida entera.")
w("")

w("## Lo que no puedes hacer")
w("")
w("- **No pobles ninguna de las %d tablas.** Es justo lo que cerraría la ventana." % len(VACIAS))
w("- **No toques ninguna referencia.** Están puestas: el auditor sale con 0 correcciones. Pero")
w("  «puestas» no es «auditadas» —de las %d, solo unas pocas están **verificadas** y el resto son"
  % len([1 for t in MODELO for c in MODELO[t]["columnas"] if c.get("ref")]))
w("  **compatibles no atribuidas**—, así que si ves algo raro, repórtalo en vez de corregirlo.")
w("- **No pongas los `Security Filter`.** Apagan los instrumentos sobre esa tabla.")
w("- **No pulses `Regenerate Structure`.** Fusiona, no reemplaza, y no se deshace.")
w("- **No ejecutes ningún `.js` de `scripts/`.** Son experimentos abandonados que hacen clic a")
w("  ciegas, y son la causa de que cinco columnas acabaran apuntando a la tabla equivocada.")
w("- **No publiques.**")
w("- Si AppSheet muestra un error, **ese error describe algo real**. Reporta el texto exacto y para.")
w("")

w("## Qué reportar")
w("")
w("1. Las %d columnas virtuales: si se crearon, con qué `App formula`, y el estado de `Show?` y"
  % len(virtuales))
w("   `Label` en cada una.")
w("2. Tabla por tabla, **qué tipo tenía cada columna antes** — aunque no lo cambies.")
w("3. La salida entera de los tres comandos del cierre.")
w("")
w("No des una tabla por cerrada sin su comparación.")

with open(SALIDA, "w", encoding="utf-8") as f:
    f.write("\n".join(L) + "\n")

print("Generado:", SALIDA)
print("%d columnas virtuales · %d tipos por cotejar en %d tablas"
      % (len(virtuales), total, len(pendientes)))
