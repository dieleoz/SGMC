# Migración a la hoja limpia

**Qué se hace, qué cuesta y qué se gana.** Es la decisión pendiente para retomar.

| | |
|---|---|
| Estado | Preparado, sin ejecutar |
| **El entregable** | `BD/Modelo_Datos_PLANTILLA.xlsx` — 28 pestañas de datos más `_LEEME`, con los 34 activos de fixture y 355 sintéticos |
| Intermedio | `BD/Modelo_Datos_LIMPIO.xlsx` — la estructura sin inventario. **No se entrega** |
| Lo genera | `python scripts/generar_plantilla.py` — la plantilla entera, en un comando |

> **Cerrado el 2026-08-10.** Antes hacían falta dos scripts y varios pasos a mano —unir los dos
> libros, añadir `_LEEME`, poblar `TIP_TiposActivo.RadioGeofencingKm`— que no estaban escritos en
> ninguna parte, así que la plantilla no se reproducía y había que conservarla.
>
> **Ahora sale de un comando y se reproduce:** dos ejecuciones seguidas dan las 29 pestañas
> idénticas, celda por celda. `generar_hoja_limpia.py` y `generar_inventario.py` siguen existiendo
> y producen sus piezas por separado, pero **el entregable es el del comando de arriba**.

## Por qué existe esta migración

**El modelo se definió y después se heredó la hoja vieja tal cual.** En vez de generar la hoja
*desde* el modelo, se tomó como venía —con 47 columnas que el modelo no usa— y se escribió
documentación para gestionar la basura: anexos de ocultación, listas de trampas, un registro de
columnas sin decidir.

**Todo eso existe porque no se hizo lo obvio.** La hoja limpia lo borra de un golpe.

## Lo que cambia: 8 tablas de 28

```
CHD_ChecklistDetalle    -12 columnas
CHK_Checklists          -15
MAN_Mantenimientos      -13
OT_OrdenesTrabajo        -3
FOT_Fotografias          -1
FRM_Formularios          -1
FRM_Preguntas            -1
USR_Usuarios             -1
```

**Las otras 20 no se tocan.** Conservan claves, tipos, referencias y columnas virtuales.

## Lo que cuesta

**Borrar y volver a dar de alta esas 8 tablas**, y reponer **14 reglas** —esta tabla se deriva del
modelo, no se escribe a mano—:

| Tabla | Regla | Columna | Tipo |
|---|---|---|---|
| `CHK_Checklists` | RG-09 | `VersionFormulario` | Initial value |
| `MAN_Mantenimientos` | RG-01 | `Coordenadas_Cierre` | Valid_If |
| `MAN_Mantenimientos` | RG-02 | `Precision_GPS` | Initial value |
| `MAN_Mantenimientos` | RG-03 | `MotivoExcepcion` | Required_If |
| `MAN_Mantenimientos` | RG-06 | `(tabla)` | Bot |
| `MAN_Mantenimientos` | RG-10 | `(tabla)` | Bot |
| `MAN_Mantenimientos` | RG-13 | `(tabla)` | Verificacion de evidencia |
| `MAN_Mantenimientos` | RG-15 | `(tabla)` | Are updates allowed |
| `MAN_Mantenimientos` | RG-19 | `CierreConExcepcion` | App formula |
| `MAN_Mantenimientos` | RG-20 | `(varias)` | Editable_If |
| `OT_OrdenesTrabajo` | RG-05 | `(tabla)` | Security Filter |
| `OT_OrdenesTrabajo` | RG-07 | `(tabla)` | Bot |
| `OT_OrdenesTrabajo` | RG-08 | `EstadoOrdenID` | Bot programado |
| `OT_OrdenesTrabajo` | RG-14 | `(tabla)` | Are updates allowed |

**Y 27 referencias**: 21 que salen de esas 8 tablas, más 6 que apuntan **hacia** ellas desde tablas
que no se tocan. Esas últimas se rompen aunque su tabla no cambie, porque su destino desaparece un
momento.

Las expresiones completas están en
[`sdd/RECONSTRUCCION_EXPRESIONES.md`](sdd/RECONSTRUCCION_EXPRESIONES.md) §2.

## Lo que se gana

```
Las 3 trampas          desaparecen — sin la columna, AppSheet no puede inventar la Ref
Las 47 ocultaciones    no hacen falta nunca más
El anexo de ocultar    sobra
COLUMNAS_SIN_DECIDIR   se vacía
```

**La aplicación pasa a leer el modelo y punto.** Y en la próxima reconstrucción —que la habrá—
nadie tiene que acordarse de esconder nada.

---

## Paso a paso

### 1. Respaldo

*Archivo → Hacer una copia* del Google Sheets, con la fecha en el nombre.

**Es lo único que no se recupera.** Todo lo demás vive en el repositorio.

### 2. Llevar el contenido limpio a la hoja

Dos caminos, y el segundo conserva el enlace de la aplicación:

**a) Subir el archivo nuevo.** Suba `BD/Modelo_Datos_LIMPIO.xlsx` a Drive, ábralo como Google
Sheets, y **reapunte la aplicación a ese archivo**. Requiere tocar la fuente de cada tabla.

**b) Limpiar la hoja actual** borrando las 47 columnas. La aplicación sigue apuntando al mismo
archivo y no hay que reapuntar nada. **Es el camino recomendado.**

**Borre por NOMBRE de encabezado, no por letra de columna.** Una letra exige que el encabezado no
haya cambiado desde que se generó esta lista, y si alguien las borra en orden ascendente destruye
**13 columnas vivas** —entre ellas `Coordenadas_Cierre` y `MotivoExcepcion`— dejando 35 retiradas en
pie. **La aplicación seguiría abriendo: el daño no se ve hasta el primer cierre.**

La lista por nombre está en el anexo de [`MANUAL_DESPLIEGUE.md`](MANUAL_DESPLIEGUE.md), ficha por
ficha. Si aun así usa las letras, van en orden inverso —de derecha a izquierda—:

```
CHD_ChecklistDetalle   U · S · Q · P · O · N · M · H · G · F · E · D
CHK_Checklists         T · S · R · Q · P · O · N · M · L · K · J · I · F · E · D
MAN_Mantenimientos     U · T · R · Q · P · O · L · K · J · I · H · G · D
OT_OrdenesTrabajo      L · K · G
FOT_Fotografias        D
FRM_Formularios        D
FRM_Preguntas          Q
USR_Usuarios           K
```

> **Compruebe la letra contra el encabezado antes de borrar cada una.** Si alguien añadió o quitó
> una columna desde que se generó esta lista, las posiciones cambian.

### 3. Verificar la hoja antes de tocar la aplicación

Descargue el libro a `BD/` y:

```bash
python scripts/verificar_faseA.py "BD/<archivo>.xlsx"
```

Tiene que decir **`FASE A CERRADA`**. `F-18` comprueba que no haya pestañas ocultas y `F-19` que no
queden columnas declaradas como retiradas que ya no existan.

### 4. Rehacer las 8 tablas en AppSheet

**Borrar y volver a dar de alta**, una por una. `Regenerate` no sirve: fusiona en vez de reemplazar
y conservaría las columnas viejas — ver `BASE_CONOCIMIENTO_APPSHEET.md` §11.

**En este orden**, para que cada una encuentre puestas las claves de las que depende:

```
1.  FRM_Formularios · FRM_Preguntas · USR_Usuarios
2.  OT_OrdenesTrabajo
3.  MAN_Mantenimientos
4.  CHK_Checklists · CHD_ChecklistDetalle · FOT_Fotografias
```

Y en cada una, antes de pasar a la siguiente: **la casilla `KEY` en la columna correcta, tipo
`Text`**.

### 5. Reponer las referencias de esas 8

Son 27: 21 desde esas tablas y 6 hacia ellas. La ficha de cada tabla está en el anexo de
[`MANUAL_DESPLIEGUE.md`](MANUAL_DESPLIEGUE.md).

**Y los cuatro `IsPartOf`:** `CHK`, `FOT` y `FIR` hacia el mantenimiento, `CHD` hacia el checklist.
**`MAN_Mantenimientos.OTID` va desmarcado** — con él, borrar una orden se llevaría la evidencia en
cascada.

### 6. Reponer las 14 reglas

Las de la tabla de arriba. **`RG-19` está entre ellas** —el umbral de GPS con su `ISBLANK`— y es
la que `ESTADO.md` llama la más peligrosa de olvidar. Expresiones completas en `RECONSTRUCCION_EXPRESIONES.md` §2.

### 7. Verificar

```
[OTID].[ActivoID].[Ubicacion]              debe salir en verde
[OTID].[TecnicoID].[Correo]                debe salir en verde
REF_ROWS("OT_OrdenesTrabajo", "Activo")    anote literalmente qué dice
```

**En el Asistente de Expresiones, y se cierra sin dar a `Done`.** Escribir una expresión dentro de
una columna la convierte en configuración activa: ya ocurrió una vez y dejó una `App formula`
escribiendo coordenadas en una columna retirada.

Y las pruebas de [`sdd/PRUEBA-003-despliegue.md`](sdd/PRUEBA-003-despliegue.md).

---

## Lo que esta migración NO arregla

**Las coordenadas reales.** Los 34 activos reales comparten una sola, en Bogotá; los 355 sintéticos
tienen coordenadas del corredor pero inventadas. **Ninguna hoja limpia lo soluciona**: hay que salir
a levantar. Es la decisión **D-01** y sigue siendo el bloqueo del piloto.

**Y el radio del geofencing, a medias.** Con 355 activos a 386 metros de separación media, un radio
de 1 km mete **8 activos dentro de cada geofence**. El sistema probaría «estás en el corredor», no
«estás frente al equipo».

`TIP_TiposActivo.RadioGeofencingKm` **ya no está vacía**: la plantilla la trae poblada por familia
—0,05 km en 12 tipos, 0,1 km en 5 y 1,5 km en la fibra—. **Lo que falta es la expresión**: mientras
la regla del editor use el literal `1.0` en vez de desreferenciar esa columna, la plantilla no
cambia nada. La expresión buena está en `RECONSTRUCCION_EXPRESIONES.md`.

## Si se decide no migrar

Es defendible. La aplicación funciona con las 47 columnas ocultas, y ocultarlas ya está casi hecho.

**Lo que se acepta a cambio:** que la hoja y el modelo sigan divergiendo, que las tres trampas haya
que vigilarlas en cada reconstrucción, y que quien retome el proyecto tenga que entender por qué hay
columnas que existen pero no se usan.

**No es deuda técnica grave. Es fricción permanente.**
