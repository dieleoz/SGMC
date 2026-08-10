# Correcciones de cableado

**Generado** por `scripts/auditar_cableado.py` contra la aplicacion en vivo. No editar a
mano: vuelve a correr el script y se rehace con lo que quede pendiente.

---

En la aplicacion **`_SISGA_-323965761`**, 9 columnas de `ACT_Activos` estan mal. El resto del
cableado esta bien: **27 de las 39 referencias son correctas**.

## Antes de tocar nada, por que importa

`ACT_Activos.TipoActivoID` apunta hoy a `SED_Sedes`. Con eso, **cada activo lee el checklist
de una sede**, y la regla del geofencing falla con un mensaje que despista:

```
Can't find column "RadioGeofencingKm" in table "SED_Sedes"
```

**La expresion esta bien escrita. No la cambies.** El error dice la verdad: navega a
`SED_Sedes` porque la referencia esta mal puesta, y ahi ese radio no existe. Reescribir la
expresion para acomodarla seria romper una regla correcta para tapar un cableado roto.

Ninguna regla se cablea hasta que estas 9 esten hechas.

## Como se llego a esto

Al cablear `ACT_Activos` salio un aviso rojo. Se corrigieron dos columnas a mano y se guardo.
Pero al guardar quedaron **tres columnas de texto convertidas en `Ref`** y **dos referencias
apuntando a `SED_Sedes`**, que era la tabla que estaba seleccionada. Nada lo detecto: la API
respondio 28/28, `validar_modelo.py` dio APTO y las 368 filas seguian ahi.

Es la regla **R-04**: *una referencia que resuelve puede apuntar a lo que no es.* Preguntar
«apunta a algo» nunca contesta «apunta a lo correcto».

## Las 9, en orden

Todas en **`Data > Columns > ACT_Activos`**. Guarda **una vez al final**, no columna a columna:
mientras las tres primeras esten mal, la tabla no deja guardar.

| # | Columna | Esta asi | Debe quedar |
|---|---|---|---|
| 1 | `CodigoQR` | `Ref` -> `SED_Sedes` | **`Text`**, sin tabla destino |
| 2 | `Nombre` | `Ref` -> `SED_Sedes` | **`Text`**, sin tabla destino |
| 3 | `PR` | `Ref` -> `SED_Sedes` | **`Text`**, sin tabla destino |
| 4 | `CalzadaID` | `Ref` -> `SED_Sedes` | `Ref` -> **`CAL_Calzadas`** |
| 5 | `TipoActivoID` | `Ref` -> `SED_Sedes` | `Ref` -> **`TIP_TiposActivo`** |
| 6 | `EstadoActivoID` | no es `Ref` | `Ref` -> **`EST_Activo`** |
| 7 | `FrecuenciaID` | no es `Ref` | `Ref` -> **`FRE_Frecuencias`** |
| 8 | `SentidoID` | no es `Ref` | `Ref` -> **`SEN_Sentidos`** |
| 9 | `UnidadFuncionalID` | no es `Ref` | `Ref` -> **`UNF_UnidadesFuncionales`** |

> Las tres primeras van antes que las demas. Son las que bloquean el guardado.

## Como saber que quedo

El boton `SAVE` pasa de gris a azul al recoger el cambio, y vuelve a gris al guardar. Ese
ciclo es la senal; si sigue gris, el editor no recogio nada y se pierde al recargar.

Despues, desde el repositorio:

```bash
python scripts/auditar_cableado.py
```

Sale con **0 correcciones** cuando esta bien. No te fies del recuento de tablas de la API:
dio 28/28 con estas 9 rotas.

## Lo que este script NO puede ver

6 referencias no son observables por este medio, porque su tabla destino esta **vacia** y
la columna virtual inversa vive en el destino. **No estan bien ni mal: no se sabe.**

- `CHD_ChecklistDetalle.ChecklistID` -> `CHK_Checklists`
- `CHK_Checklists.MantenimientoID` -> `MAN_Mantenimientos`
- `FIR_Firmas.MantenimientoID` -> `MAN_Mantenimientos`
- `FOT_Fotografias.MantenimientoID` -> `MAN_Mantenimientos`
- `MAN_Mantenimientos.OTID` -> `OT_OrdenesTrabajo`
- `OT_OrdenesTrabajo.OTOrigenID` -> `OT_OrdenesTrabajo`

Abrelas en el editor una por una y confirma su `Source table`. Dar por buena una
referencia que no se ha mirado es exactamente como se llego a las 9 de arriba.
