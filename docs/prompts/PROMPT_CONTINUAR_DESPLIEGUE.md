# Prompt para continuar el despliegue — correcciones y cierre

Autocontenido. Cópialo íntegro desde la línea siguiente.

---

Estás terminando de configurar la aplicación **SISGA** en Google AppSheet. Las 38 referencias ya
están puestas y los filtros de seguridad también. Quedan **seis cosas**, y la primera hay que
hacerla antes que ninguna otra.

## 1. URGENTE — Deshacer `MAN_Mantenimientos.Diagnostico`

Durante las pruebas, esa columna quedó así:

```
Type:         LatLong
App formula:  [OTID].[ActivoID].[Ubicacion]
```

**Hay que revertirlo.** `Diagnostico` es una columna retirada del modelo que sigue existiendo en la
hoja, en la posición 9 de `MAN_Mantenimientos`.

**Por qué corre prisa:** una `App formula` **escribe en la hoja** cada vez que se modifica la fila.
Tal como está, cada mantenimiento que alguien guarde escribirá la coordenada del activo dentro de la
columna `Diagnostico`, machacando lo que hubiera. No da error y no avisa.

**Qué hacer:**

1. `MAN_Mantenimientos` → columna `Diagnostico` → lápiz.
2. **Borrar la `App formula`.** Dejar el campo vacío.
3. **Tipo: `LongText`.**
4. **Desmarcar `Show?`.**
5. `Done`.

**Y comprueba en la hoja** que ninguna fila de `MAN_Mantenimientos` tiene una coordenada escrita en
`Diagnostico`. Si la tiene, bórrala a mano: son dos filas.

> **La lección, para no repetirla:** una expresión se prueba en el **Asistente de Expresiones**, que
> solo la evalúa. Escribirla dentro de una columna la convierte en configuración activa.

## 2. Completar la regla del umbral de GPS

En `MAN_Mantenimientos.CierreConExcepcion`, la `App formula` actual está incompleta. Sustitúyela por
esta, entera:

```
OR(ISBLANK(LOOKUP("UMBRAL_GPS", "PAR_Parametros", "ParametroID", "Valor")), [Precision_GPS] > LOOKUP("UMBRAL_GPS", "PAR_Parametros", "ParametroID", "Valor"))
```

**Qué añade el `ISBLANK`:** si alguien borra la fila del parámetro, la versión corta hace que
**todos los cierres salgan limpios y nadie se entere**. Con el `ISBLANK`, si el umbral no se puede
leer, el cierre se marca como excepcional. Falla hacia el lado seguro.

## 3. Retirar el borrado — esto faltaba y es lo más importante

En *Data → Tables → `OT_OrdenesTrabajo` → Are updates allowed*:

```
Updates ✓    Adds ✓    Deletes ✗
```

**Lo mismo en `MAN_Mantenimientos`.**

**Por qué no es opcional.** Se marcó `IsPartOf` en cuatro referencias —`FOT`, `FIR` y `CHK` hacia el
mantenimiento, y `CHD` hacia el checklist—. `IsPartOf` significa **borrado en cascada**: borrar un
mantenimiento se lleva sus fotografías, su firma y su checklist.

Eso solo es seguro **porque el mantenimiento nunca se borra**. Y eso es exactamente lo que hace
quitar `Deletes`.

Tal como está la aplicación ahora mismo, la cascada está creada y la protección no.

## 4. Las cuatro marcas de tiempo del servidor

Estas cuatro columnas tienen que ser de tipo **`ChangeTimestamp`**. AppSheet no lo infiere nunca:
llegan como texto.

```
MAN_Mantenimientos.FechaHoraRegistro
FOT_Fotografias.FechaHora
FIR_Firmas.FechaHora
NOV_Novedades.FechaHora
```

**`ChangeTimestamp` la pone el servidor.** Un `Initial value = NOW()` lo pone el teléfono, y el
usuario puede cambiar la hora del teléfono. Sin esto, **la hora de cada fotografía y de cada firma
no prueba nada**, que es justo lo que el sistema existe para sostener.

## 5. Ocultar las columnas retiradas

La hoja arrastra **49 columnas que el modelo no usa**, y al dar de alta las tablas entraron todas
con `Show? = TRUE`. Aparecen en el formulario del técnico junto a las que sí valen.

**El problema no es estético.** Quedan pares que registran lo mismo en dos sitios:

```
Requiere_Repuesto        junto a  MotivoPendienteID
Firma_Tecnico            junto a  FIR_Firmas
Imagen_Inicio/Final      junto a  FOT_Fotografias
Diagnostico              junto al checklist
Trabajo_Realizado        junto al checklist
```

**Desmarca `Show?` en todas las columnas retiradas.** La lista completa, tabla por tabla, está en
`docs/sdd/RECONSTRUCCION_EXPRESIONES.md` §5. Las que más filas tienen:

```
MAN_Mantenimientos     13 columnas
CHK_Checklists         15
CHD_ChecklistDetalle   12
OT_OrdenesTrabajo       3
```

**No las borres.** Se ocultan, no se eliminan: la Fase A no borra nada, y borrar es lo único que un
respaldo no devuelve gratis.

## 6. Las pruebas, y esta vez en el sitio correcto

**En el Asistente de Expresiones**, que evalúa sin guardar nada. Se abre desde el icono de la
probeta en cualquier campo de fórmula — **y se cierra sin dar a `Done`**.

**Las dos que deben salir verdes:**

```
[OTID].[ActivoID].[Ubicacion]
[OTID].[TecnicoID].[Correo]
```

**Y una que tiene que salir mal, o hay que anotar que no:**

```
REF_ROWS("OT_OrdenesTrabajo", "Activo")
```

`Activo` en `OT_OrdenesTrabajo` **ya no es la referencia al activo**: es la bandera Sí/No. Esa
expresión apunta a la columna equivocada y devuelve lista vacía.

**Si el Asistente la acepta, anótalo con su salida literal.** Es la prueba de que un despliegue
verde no distingue esa expresión de la correcta. Sin verla aceptada, no sabemos si lo demás pasó por
diligencia o por casualidad.

## Cuando termines, reporta

1. **`Diagnostico`**: tipo final, si tenía fórmula, y si había coordenadas escritas en la hoja.
2. **La regla del umbral**: pegada entera, con el `ISBLANK`.
3. **`Deletes`**: desmarcado en las dos tablas.
4. **Los cuatro `ChangeTimestamp`**: puestos.
5. **Cuántas columnas ocultaste** por tabla.
6. **Las tres expresiones**, con lo que dijo el Asistente en cada una.

## Lo que NO debes hacer

- **No borres ninguna columna.** Se ocultan.
- **No pruebes expresiones escribiéndolas en una columna.** Solo en el Asistente.
- **No toques `Precision_GPS` del registro `TEST-MTTO-002`.** Vale `45` y es la fila que prueba el
  rechazo por GPS deficiente.
- **No publiques todavía.** Los 34 activos comparten una sola coordenada, en Bogotá: con el radio de
  1 km, la aplicación rechazaría **todos** los cierres hechos en el corredor.
