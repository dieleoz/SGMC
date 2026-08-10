# Migración a la hoja limpia

**Qué se hace, qué cuesta y qué se gana.** Es la decisión pendiente para retomar.

| | |
|---|---|
| Estado | Preparado, sin ejecutar |
| Archivo generado | `BD/Modelo_Datos_LIMPIO.xlsx` — 28 pestañas, 202 columnas, 214 filas |
| Lo genera | `python scripts/generar_hoja_limpia.py "BD/<origen>.xlsx"` |

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

**Borrar y volver a dar de alta esas 8 tablas.** De ellas, solo tres llevan reglas encima:

| Tabla | Qué hay que reponer |
|---|---|
| `MAN_Mantenimientos` | Geofencing en `Coordenadas_Cierre` · `CierreConExcepcion` · `MotivoExcepcion` obligatorio · `Editable_If = FALSE` en las cuatro de captura · `Deletes` desmarcado |
| `OT_OrdenesTrabajo` | Security Filter · `Deletes` desmarcado |
| `CHK_Checklists` | `VersionFormulario` con su `Initial value` |

**Ocho cosas.** Las expresiones completas están en
[`sdd/RECONSTRUCCION_EXPRESIONES.md`](sdd/RECONSTRUCCION_EXPRESIONES.md) §2.

## Lo que se gana

```
Las 3 trampas          desaparecen — sin la columna, AppSheet no puede inventar la Ref
Las 43 ocultaciones    no hacen falta nunca más
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

Las columnas a borrar, con su letra y **en orden inverso** —de derecha a izquierda, para que las
posiciones no se muevan—:

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

Son 14 de las 38. La ficha de cada tabla está en el anexo de
[`MANUAL_DESPLIEGUE.md`](MANUAL_DESPLIEGUE.md).

**Y los cuatro `IsPartOf`:** `CHK`, `FOT` y `FIR` hacia el mantenimiento, `CHD` hacia el checklist.
**`MAN_Mantenimientos.OTID` va desmarcado** — con él, borrar una orden se llevaría la evidencia en
cascada.

### 6. Reponer las ocho reglas

Las tres tablas de la tabla de arriba. Expresiones completas en `RECONSTRUCCION_EXPRESIONES.md` §2.

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

**Los 34 activos comparten una sola coordenada, y está en Bogotá.**

Con el radio de un kilómetro, la aplicación rechaza todo cierre hecho en el corredor. **Ninguna hoja
limpia lo soluciona**: hay que salir a levantar coordenadas reales. Es la decisión **D-01** y sigue
siendo el bloqueo del piloto.

## Si se decide no migrar

Es defendible. La aplicación funciona con las 43 columnas ocultas, y ocultarlas ya está casi hecho.

**Lo que se acepta a cambio:** que la hoja y el modelo sigan divergiendo, que las tres trampas haya
que vigilarlas en cada reconstrucción, y que quien retome el proyecto tenga que entender por qué hay
columnas que existen pero no se usan.

**No es deuda técnica grave. Es fricción permanente.**
