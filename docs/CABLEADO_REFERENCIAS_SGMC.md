# Cableado de referencias del SGMC

Procedimiento para convertir las referencias del modelo, hoy declaradas como texto, en referencias
reales de AppSheet. Lo ejecuta una persona con permiso de edición sobre el Sheets de producción y
acceso al editor de AppSheet. El agente no puede hacerlo: aquí se especifica, allá se aplica.

El modelo objetivo está en `scripts/modelo_objetivo.py`, y de él salen las tablas de este
documento. Si algo aquí contradice al modelo, manda el modelo.

---

## 1. Qué se está arreglando y por qué importa

`MAN_Mantenimientos.OTID` es de tipo `Text`. Parece una referencia, se llama como una referencia y
en el diccionario de datos figura como una referencia, pero AppSheet responde:

```
Invalid dereference. Column OTID is not a Ref
```

De ese único hecho cuelgan cuatro consecuencias:

| Consecuencia | Por qué |
|---|---|
| No hay geofencing | `DISTANCE()` necesita llegar al activo, y la ruta pasa por `OTID` |
| No hay navegación padre-hijo | El técnico no puede abrir la orden desde la ejecución |
| No hay reportes por activo | No existe forma de agrupar mantenimientos por el equipo intervenido |
| Los huérfanos no se detectan | Un texto acepta cualquier valor; una referencia, no |

El checklist `d02d8a3d` es la demostración: su `OTID` vale `'1'` en el Excel local y `'OT-0001'` en
producción. Con una referencia real, ese valor no se habría podido guardar.

## 2. La regla que gobierna todo el procedimiento

> **Una referencia de AppSheet guarda el valor de la clave de la tabla destino.**

De ahí se derivan las tres reglas de orden que hacen que esto salga bien o mal:

1. **Primero la clave del destino, después quien la apunta.** Convertir `MAN.OTID` a `Ref` antes de
   que `OT_OrdenesTrabajo` tenga su clave definitiva deja las seis órdenes sin resolver.
2. **Renombrar y retipar son la misma tarea.** Si la clave se llama `Numero_OT` y quien la apunta
   se llama `OTID`, no hay contra qué resolver. Por eso el renombrado no es cosmético.
3. **Una conversión `Text` a `Ref` conserva solo las filas cuyo valor coincide con la clave.** Las
   demás quedan huérfanas, y AppSheet no lo anuncia.

## 3. Punto de partida verificado

Leído el 2026-08-07 en `BD/Modelo de Datos (2).xlsx` con `openpyxl`, encabezado por encabezado.

| Tabla | Filas con datos | Observación |
|---|---|---|
| `ACT_Activos` | 34 | `ActivoID` son enteros 1 a 34. Además arrastra 11 columnas sin encabezado |
| `OT_OrdenesTrabajo` | 6 | Clave `Numero_OT` con valores `OT-0001` a `OT-0006` |
| `MAN_Mantenimientos` | **0** | Vacía |
| `CHK_Checklists` | 1 | Dato de prueba: `TecnicoID` trae un nombre y `FechaInicio` el texto `NOW()` |
| `CHD_ChecklistDetalle` | 2 | Referencia la pregunta por su texto |

**`OT_OrdenesTrabajo.Activo` sí es el vínculo al activo.** Guarda los enteros 2, 26, 5, 9, 27 y 3,
que corresponden a `ACT_Activos.ActivoID`. No hay que crear la columna: hay que renombrarla y
retiparla. Los seis valores existen en `ACT_Activos`, de modo que **esa conversión no produce
huérfanos**.

### La consecuencia que decide el calendario

`MAN_Mantenimientos` tiene cero filas. Convertir `OTID` a `Ref` hoy **no arrastra ningún dato**.

Es el momento más barato en que se podrá hacer, y el costo crece con cada mantenimiento que se
registre: después de poblar, la misma conversión obliga a migrar y a reconciliar los valores que no
resuelvan. Esto no argumenta a favor de correr, sino en contra de dejarlo para después del piloto.

### Advertencia sobre la fuente

Lo anterior se verificó contra el **Excel local**. El Sheets de producción es otro modelo: entre
otras diferencias, el Excel tiene `MAN_Mantenimientos.ActivoID` y producción no —AppSheet lo
confirmó al rechazar la fórmula—. **El paso 1 del procedimiento es releer producción**, no dar por
buena esta tabla.

## 4. Procedimiento

### Paso 0 — Respaldo y ventana de congelación

No se toca nada sin esto.

1. En el Sheets: *Archivo > Hacer una copia*, nombrada `SGMC_backup_AAAA-MM-DD_antes_cableado`.
2. En AppSheet: *Manage > Versions > Save a version*, con la nota `antes de cablear referencias`.
3. Avisar a quien tenga permiso de edición que nadie escriba durante la ventana. Son dos personas:
   el propietario del documento y la cuenta del cliente.

### Paso 1 — Releer producción y anotar el punto de partida real

Antes de renombrar nada, leer en el Sheets de producción los encabezados de `ACT_Activos`,
`OT_OrdenesTrabajo`, `MAN_Mantenimientos`, `CHK_Checklists` y `CHD_ChecklistDetalle`, y anotar
cuáles difieren de la sección 3. Cada diferencia cambia el procedimiento.

Comprobar en particular si `MAN_Mantenimientos` tiene o no la columna `ActivoID`, y si conserva
las cinco columnas que solo existen en producción (`Diagnostico`, `Trabajo_Realizado`,
`Duracion_Minutos`, `Repuestos_Utilizados`, `Requiere_Repuesto`).

### Paso 2 — Limpiar los datos de prueba

Se hace **antes** de convertir, no después: un dato de prueba que no resuelve se convierte en un
huérfano silencioso.

- Borrar la fila `CHK001` de `CHK_Checklists`, que trae `TecnicoID = "Santiago Moreno"` y
  `FechaInicio = "NOW()"` como texto literal.
- Borrar sus dos filas hijas en `CHD_ChecklistDetalle`.
- Con `MAN_Mantenimientos` vacía, ningún checklist puede colgar de una ejecución. Esa fila no tiene
  padre posible.

### Paso 3 — Fijar la clave de `ACT_Activos`

En AppSheet, *Data > Columns > `ACT_Activos`*:

- Confirmar que `ActivoID` tiene marcada la casilla **KEY**, y que es la única.
- Anotar su tipo. Todas las referencias que apunten aquí guardarán ese valor.

Si la clave fuera otra columna, detener el procedimiento: el resto de los pasos asume que es
`ActivoID`.

### Paso 4 — Renombrar en `OT_OrdenesTrabajo`

En el Sheets, sobre la fila 1. **El orden dentro de este paso importa.**

| Orden | Nombre actual | Nombre nuevo | Por qué en esta posición |
|---|---|---|---|
| 1.º | `Activo` | `ActivoID` | Libera el nombre `Activo` antes de que nadie lo reutilice |
| 2.º | `Numero_OT` | `OTID` | La clave pasa a llamarse como la referencia que la apunta |
| 3.º | `Tecnico` | `TecnicoID` | Convención |
| 4.º | `SupervidorID` | `SupervisorID` | Corrige el error de escritura del encabezado |
| 5.º | `Fecha Programada` | `FechaProgramada` | Elimina los espacios, que obligan a citar el nombre |

> **La trampa del nombre reutilizado.** En el modelo objetivo `Activo` es la bandera `Yes/No` que
> llevan todas las tablas, no el vínculo al activo. Son dos columnas distintas que se llaman igual
> en momentos distintos. Si se crea la bandera antes de renombrar la vieja, el Sheets queda con dos
> columnas `Activo` y AppSheet resuelve una de las dos sin decir cuál. `validar_modelo.py` emite
> este aviso como **V-14**.

Renombrar `Numero_OT` rompe toda vista, fórmula o acción que la cite. Antes de renombrar, buscar
`Numero_OT` en el editor de AppSheet y anotar dónde aparece; después del paso 5, corregir cada
aparición.

### Paso 5 — Regenerar y tipar `OT_OrdenesTrabajo`

1. *Data > Tables > `OT_OrdenesTrabajo` > Regenerate Structure.* Sin esto la aplicación sigue viendo
   los nombres viejos y todo lo demás falla en silencio.
2. Marcar `OTID` como **KEY**.
3. Tipar:

| Columna | Tipo | Apunta a |
|---|---|---|
| `ActivoID` | `Ref` | `ACT_Activos` |
| `TecnicoID` | `Ref` | `USR_Usuarios` |
| `SupervisorID` | `Ref` | `USR_Usuarios` |

**Verificación del paso:** abrir una orden en la vista previa. El activo debe mostrarse como enlace
navegable, no como el número `2`. Si sigue viéndose el número, la referencia no quedó.

### Paso 6 — El retipado que desbloquea todo

En *Data > Columns > `MAN_Mantenimientos`*:

1. Cambiar `OTID` de `Text` a **`Ref`**, destino `OT_OrdenesTrabajo`.
2. Retirar la columna `ActivoID` si existe. El activo se alcanza por `[OTID].[ActivoID]`; guardarlo
   también aquí permite que la ejecución diga un activo y su orden diga otro, sin forma de saber
   cuál miente. La tabla está vacía, así que no se pierde nada.

**Decisión que hay que tomar aquí, no después:** el modelo objetivo declara `IsPartOf` sobre
`MAN_Mantenimientos.OTID`. Eso significa que **borrar una orden borra su ejecución**, y con ella
—por la misma marca en `FOT_Fotografias` y `FIR_Firmas`— las fotografías y las firmas. En un
sistema cuyo propósito es que la evidencia sea difícil de falsificar, un borrado en cascada de la
evidencia es una decisión deliberada o un agujero. Confirmarla antes de activarla; si se decide que
no, quitar `es_parte_de` en el modelo y regenerar.

**Verificación del paso:** en el Asistente de Expresiones, sobre `MAN_Mantenimientos`, escribir
`[OTID].[ActivoID].[Ubicacion]`. Debe resolver sin error. Es la prueba de que la cadena existe.

### Paso 7 — Escribir la regla de geofencing (RG-01)

Sobre `MAN_Mantenimientos.Coordenadas_Cierre`:

```
Initial value:  HERE()
Valid_If:       DISTANCE([Coordenadas_Cierre], [OTID].[ActivoID].[Ubicacion]) <= [OTID].[ActivoID].[TipoActivoID].[RadioGeofencingKm]
Invalid text:   Ubicación fuera de rango: debe estar junto al activo para cerrar.
```

Y sobre `Precision_GPS`, valor inicial `USERLOCATIONACCURACY()`.

El radio sale del tipo de activo y no es un número fijo: una subestación y un poste SOS no admiten
la misma tolerancia. Mientras `TIP_TiposActivo.RadioGeofencingKm` no exista o esté vacío, usar el
literal `1.0` y dejarlo anotado como provisional.

### Paso 8 — `CHK_Checklists` y `CHD_ChecklistDetalle`

El checklist cambia de padre: cuelga de la ejecución, no de la orden, porque inspeccionar es parte
de ejecutar.

| Tabla | Actual | Objetivo | Tipo |
|---|---|---|---|
| `CHK_Checklists` | `OTID` | `MantenimientoID` | `Ref` a `MAN_Mantenimientos`, `IsPartOf` |
| `CHK_Checklists` | `FormularioID` | `FormularioID` | `Ref` a `FRM_Formularios` |
| `CHD_ChecklistDetalle` | `PreguntaItem` | `PreguntaID` | `Ref` a `FRM_Preguntas` |
| `CHD_ChecklistDetalle` | `ChecklistID` | `ChecklistID` | `Ref` a `CHK_Checklists`, `IsPartOf` |

`PreguntaItem` guardaba el **texto** de la pregunta. Sin la clave no hay comparación histórica: si
alguien corrige una tilde del enunciado, las respuestas anteriores dejan de agruparse con las
nuevas.

## 5. Verificación de cierre

El procedimiento no está cerrado por haberse ejecutado. Está cerrado cuando estas cuatro
comprobaciones pasan, con la salida a la vista:

1. `[OTID].[ActivoID].[Ubicacion]` resuelve en el Asistente de Expresiones sobre
   `MAN_Mantenimientos`.
2. Una fila de prueba escrita **desde la aplicación**, no desde el Sheets, llega a
   `MAN_Mantenimientos` con valor en `Coordenadas_Cierre` y `Precision_GPS`, verificada leyendo el
   Sheets.
3. Desde esa fila se navega a la orden, y desde la orden al activo.
4. Un intento de cierre lejos del activo es rechazado con el mensaje de error escrito, no con un
   error genérico de AppSheet.

**La comprobación 4 no podrá pasar todavía**, y conviene saberlo antes de intentarla: los 34
activos comparten la coordenada `4.728512, -74.114531`, que está en Bogotá y no en el corredor.
Mientras eso siga así, cualquier cierre en la vía queda fuera de rango y cualquier cierre en Bogotá
queda dentro. El cableado es condición necesaria del geofencing; las coordenadas reales (D-01) son
la otra mitad.

## 6. Reversión

Si algo sale mal, no se corrige hacia adelante:

1. En AppSheet, *Manage > Versions*, restaurar la versión guardada en el paso 0.
2. En el Sheets, restaurar desde la copia, o usar *Archivo > Historial de versiones* para volver al
   estado anterior a la ventana.
3. Anotar en qué paso falló y con qué mensaje, antes de reintentar.

La reversión solo es limpia si nadie escribió durante la ventana. De ahí el paso 0.

---

## 7. Cómo se comprueba esto sin abrir AppSheet

Todo lo anterior está codificado en `scripts/modelo_objetivo.py`, en dos estructuras:

- `RETIPADOS` — columnas que conservan el nombre y cambian de tipo. Aquí está `MAN.OTID`.
- `RENOMBRADOS` — columnas que cambian de nombre, con el motivo de cada una.

`python scripts/validar_modelo.py` aplica sobre ellas tres reglas:

| Regla | Comprueba |
|---|---|
| V-14 | Todo renombrado aterriza en una columna que existe, y avisa si reutiliza el nombre viejo |
| V-15 | Toda referencia declara de dónde sale: renombrado, retipado o columna nueva |
| V-16 | Lo retipado coincide en tipo y destino con lo que declara el modelo |

Si alguien cambia el diseño y olvida el mapeo de migración, la validación lo detiene. Es el control
que no existía cuando `bd.md` y el Excel describieron modelos distintos durante meses.
