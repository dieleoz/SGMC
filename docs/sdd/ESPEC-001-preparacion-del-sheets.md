# ESPEC-001 — Preparación del Sheets de producción

Primera de las dos especificaciones del cableado. Cubre **todo lo que se puede hacer sobre la hoja
de cálculo**, sin abrir el editor de AppSheet.

| | |
|---|---|
| Fase | Sheets. La barata, reversible y verificable leyendo de vuelta |
| Continúa en | `ESPEC-002` — navegador: Regenerate, tipado, cableado y reglas |
| Estado | **Pendiente de `PRUEBA-001` y del veredicto del arquitecto** |

## 1. Qué se quiere y por qué

Dejar la hoja con la estructura y los datos definitivos **antes** de tocar el editor de AppSheet,
para que el paso caro se reduzca a un solo *Regenerate Structure* por tabla y al tipado.

Hay una razón técnica, no solo económica: **AppSheet deriva su estructura leyendo la hoja e infiere
el tipo a partir de los datos que encuentra.** Una columna vacía se regenera como `Text`; una que ya
trae `4.728512, -74.114531` tiene opción de salir como `LatLong`. Poblar antes de regenerar reduce
el tipado manual.

**Lo que esto NO consigue.** Las referencias no se infieren de forma fiable: AppSheet leerá una
columna de enteros y dirá `Number`, no `Ref` a `ACT_Activos`. El cableado sigue siendo trabajo de
navegador, columna por columna, y es el contenido de `ESPEC-002`.

## 2. Estado actual verificado

**Fuente: Google Sheets de PRODUCCIÓN**, leído el 2026-08-07 con el conector de Google Drive,
`fileId = 1a4MmZ0u9sNgWmyiR2OPJo9YuUEKJFftbJWMW-KbITRc`. No el Excel local.

### 2.1 Corrección de una especificación anterior

`CABLEADO_REFERENCIAS_SGMC.md` se escribió contra el Excel local y **sus nombres de
`MAN_Mantenimientos` son incorrectos para producción**:

| Excel local | Producción | Consecuencia |
|---|---|---|
| `MantenimientoID` | **`MttoID`** | La clave se llama distinto |
| `TécnicoID` | **`Tecnico_Asignado`** | El renombrado declarado no existía |
| `Hora Inicio` / `Hora Fin` | **`Fecha_Hora_Inicio`** / **`Fecha_Hora_Fin`** | Idem |
| `Estado Final` | **no existe** | Hay que crearla, no renombrarla |
| `ActivoID` | **no existe** | Confirma lo que AppSheet reportó |

`scripts/modelo_objetivo.py` ya está corregido contra producción. Manda producción, porque es lo
que corre la aplicación.

### 2.2 Conteo de filas

| Tabla | Filas | Nota |
|---|---|---|
| `ACT_Activos` | 34 | Las 34 con `Ubicacion = 4.728512, -74.114531`, en Bogotá |
| `OT_OrdenesTrabajo` | 6 | `Numero_OT` de `OT-0001` a `OT-0006` |
| `USR_Usuarios` | 11 | Todos con `SedeID = 1` |
| `TIP_TiposActivo` | 18 | `FormularioID` poblado en los 18 |
| `FRM_Formularios` | 18 | |
| `FRM_Preguntas` | 15 | Solo `FRM_SOS` |
| `CHK_Checklists` | 3 | Dos de ellas basura de prueba. Ver 2.4 |
| `MAN_Mantenimientos` | **0** | |
| `CHD_ChecklistDetalle` | **0** | El Excel tiene 2. Divergencia nueva |
| `FOT_Fotografias`, `FIR_Firmas`, `GPS` | **0** | |

### 2.3 Hallazgos nuevos de esta lectura

**H-01. `SED_Sedes` ya mezcla dos conceptos.** Las sedes 7 a 10 se llaman `UF1` a `UF4`, con ciudad
`Unidad Funcional`. Los 34 activos están en 7 a 10 y los 11 usuarios en la sede 1 (`CCO`,
Sutatenza). No es que el `SedeID` esté mal alineado: es que la columna guarda dos cosas distintas.
Confirma la separación `UNF_UnidadesFuncionales` del modelo objetivo.

**H-02. `LST_ValoresLista.PreguntaID` guarda el texto `Estado encontrado`**, no una clave. Las 4
filas lo hacen. Es el defecto de «texto como clave ajena» en su forma pura.

**H-03. `USR_Usuarios` mezcla dos formatos de clave.** Diez usuarios tienen `usuarioID` entero (2 a
11) y uno tiene `3aa202ee`. La clave se llama `usuarioID`, con minúscula inicial.

**H-04. Existen tres bancos de preguntas, no uno.** Las hojas planas `FRM_SOS`, `FRM_CCTV` y
`FRM_PMVF` tienen 15 preguntas cada una. Solo las de SOS se migraron a `FRM_Preguntas`, y quedaron
**duplicadas** en los dos sitios. Hay 30 preguntas ya redactadas, de CCTV y PMVF, que nadie está
usando. Esto mejora el diagnóstico anterior de «falta 17 de 18».

**H-05. `FRM_CCTV` y `FRM_PMVF` usan `FALSO` en lugar de `FALSE`** en la columna `Obligatoria`.
Mezcla de idioma en un valor booleano; AppSheet no lo resolverá.

### 2.4 Datos de prueba en `CHK_Checklists`

| ChecklistID | Problema |
|---|---|
| `CHK001` | `ActivoID = SOS001` (no es un `ActivoID`, los válidos son 1 a 34), `TecnicoID = Santiago Moreno` (un nombre, no una clave), `FechaInicio = NOW()` como texto literal |
| `0356e6d7` | Registro a medio crear: solo `OTID` y contadores |
| `d02d8a3d` | Válido. `OTID = OT-0001`, `ActivoID = 2`, `TecnicoID = 4` |

El huérfano `CHK.OTID = '1'` que documenta `CLAUDE.md` **es del Excel local**. En producción
las tres filas apuntan a `OT-0001`, que existe.

## 3. Qué cambia exactamente

### 3.1 Renombrados

El orden dentro de `OT_OrdenesTrabajo` **no es indiferente**: `Activo` se renombra primero, para
liberar el nombre antes de que se cree la bandera `Yes/No` que lo reutiliza.

| Orden | Tabla | Actual | Nuevo |
|---|---|---|---|
| 1.º | `OT_OrdenesTrabajo` | `Activo` | `ActivoID` |
| 2.º | `OT_OrdenesTrabajo` | `Numero_OT` | `OTID` |
| 3.º | `OT_OrdenesTrabajo` | `Tecnico` | `TecnicoID` |
| 4.º | `OT_OrdenesTrabajo` | `SupervidorID` | `SupervisorID` |
| 5.º | `OT_OrdenesTrabajo` | `Fecha Programada` | `FechaProgramada` |
| 6.º | `OT_OrdenesTrabajo` | `Estado` | `EstadoOrdenID` |
| 7.º | `OT_OrdenesTrabajo` | `Fecha_Cierre` | `FechaCierre` |
| 8.º | `OT_OrdenesTrabajo` | `Cerrada_Por` | `CerradaPor` |
| | `MAN_Mantenimientos` | `MttoID` | `MantenimientoID` |
| | `MAN_Mantenimientos` | `Tecnico_Asignado` | `TecnicoID` |
| | `MAN_Mantenimientos` | `Fecha_Hora_Inicio` | `FechaHoraInicio` |
| | `MAN_Mantenimientos` | `Fecha_Hora_Fin` | `FechaHoraFin` |
| | `MAN_Mantenimientos` | `Requiere_Segunda_Visita` | `RequiereSegundaVisita` |
| | `MAN_Mantenimientos` | `Motivo_Pendiente` | `MotivoPendienteID` |
| | `MAN_Mantenimientos` | `Aprobado_Supervisor` | `AprobadoSupervisor` |
| | `MAN_Mantenimientos` | `Usuario_Registro` | `UsuarioRegistro` |
| | `MAN_Mantenimientos` | `Fecha_Hora_Registro` | `FechaHoraRegistro` |
| | `ACT_Activos` | `EstadoID` | `EstadoActivoID` |
| | `ACT_Activos` | `SedeID` | `UnidadFuncionalID` |
| | `USR_Usuarios` | `usuarioID` | `UsuarioID` |
| | `USR_Usuarios` | `Estado` | `Activo` |
| | `CHK_Checklists` | `OTID` | `MantenimientoID` |
| | `CHD_ChecklistDetalle` | `Observaciones` | `Observacion` |

La lista viva es `RENOMBRADOS` en `scripts/modelo_objetivo.py`. Si difiere de esta tabla, manda el
modelo.

### 3.2 Columnas nuevas

En `MAN_Mantenimientos`: `OrigenApertura`, `UbicacionEscaneo`, `FechaHoraEscaneo`,
`EstadoActivoID`, `CierreConExcepcion`, `MotivoExcepcion`, `ModoFallaID`, `FechaAprobacion`,
`ObservacionRechazo`.

En `TIP_TiposActivo`: `RadioGeofencingKm`. En `CHK_Checklists`: `VersionFormulario`.
En `OT_OrdenesTrabajo`: `OTOrigenID` y la bandera `Activo`, esta **solo después** del renombrado.

### 3.3 Tablas nuevas

`UNF_UnidadesFuncionales`, `ASG_AsignacionZona`, `EOT_EstadosOrden`, `MOT_MotivosPendiente`,
`FAL_ModosFalla`, `NOV_Novedades`, `PLA_PlanMantenimiento`. Definición completa en
`ARQUITECTURA_OBJETIVO_SGMC.md`.

### 3.4 Limpieza, antes de poblar

- Borrar `CHK001` y `0356e6d7` de `CHK_Checklists`.
- Conservar `d02d8a3d`, que es válida.
- Normalizar `FALSO` a `FALSE` en `FRM_CCTV` y `FRM_PMVF` (H-05).

### 3.5 Datos de prueba

**Regla dura: toda fila de prueba lleva el prefijo `TEST-` en su clave, y el paso que la borra se
escribe en esta misma especificación, no en otra.** El motivo está a la vista en 2.4: la basura de
prueba que hoy hay que limpiar entró así, sin marca y sin fecha de caducidad.

| Tabla | Filas | Con qué forma |
|---|---|---|
| `UNF_UnidadesFuncionales` | 4 | UF1 a UF4, tomadas de `SED_Sedes` 7 a 10 |
| `ASG_AsignacionZona` | 4 | Un técnico real a una unidad funcional, para poder probar el filtro |
| `EOT_EstadosOrden` | 7 | Programada, Asignada, En ejecución, En revisión, Cerrada, Suspendida, Vencida |
| `MOT_MotivosPendiente` | 5 | Los del supuesto D-07 |
| `MAN_Mantenimientos` | 2 | `TEST-MTTO-001` y `TEST-MTTO-002` |
| `ACT_Activos` | — | **No se toca.** Las coordenadas reales son D-01 |

Los catálogos nuevos **no son datos de prueba**: son catálogos definitivos y no llevan prefijo.
Solo lo llevan las filas transaccionales.

**Forma obligatoria de las filas de prueba de `MAN_Mantenimientos`:** `OTID` debe valer `OT-0001`
y `OT-0003`, no `1` ni `3`. Escribirlas con la forma final es lo que impide que la conversión a
`Ref` de `ESPEC-002` las deje huérfanas.

## 4. Cómo se declara en el modelo

Ya declarado en `scripts/modelo_objetivo.py`: `RENOMBRADOS`, `RETIPADOS`, `CAMPOS_RETIRADOS` y
`MODELO`. `python scripts/validar_modelo.py` devuelve **0 errores** y 3 avisos, uno de ellos el
V-14 sobre la reutilización del nombre `Activo`, que es intencionado.

## 5. Qué NO cubre esta especificación

- *Regenerate Structure*, tipado, cableado de referencias y reglas. Son `ESPEC-002`.
- Las coordenadas reales de los 34 activos (D-01), que son trabajo de campo.
- Los bancos de preguntas de los 15 tipos sin banco (D-09). Sí cabría migrar los de CCTV y PMVF
  que ya existen (H-04), pero se deja fuera para no mezclar frentes.
- El código QR, fuera de alcance por decisión del 2026-08-07.

## 6. Riesgos

| Riesgo | Mitigación |
|---|---|
| Renombrar `Numero_OT` rompe vistas y fórmulas que la citen | Buscar el nombre viejo en el editor y anotar dónde aparece, **antes** de renombrar. Se corrige en `ESPEC-002` |
| Dos columnas `Activo` en `OT_OrdenesTrabajo` | El renombrado va primero. Es el aviso V-14 |
| Los datos de prueba se quedan para siempre | Prefijo `TEST-` y paso de borrado en esta misma especificación |
| Se escribe sobre producción sin entorno de pruebas | Copia de respaldo antes de empezar. El riesgo real es bajo: 4 tablas vacías y ninguna transacción ejecutada nunca |
| `MAN_Mantenimientos` deja de tener 0 filas | Es deliberado, y por eso los renombrados van **antes** que el poblado |

## 7. Supuestos adoptados

1. **`SedeID` 7 a 10 son unidades funcionales**, no sedes, y migran a `UNF_UnidadesFuncionales`
   conservando su identificador. Las sedes 1 a 6 se quedan en `SED_Sedes`.
2. **Los estados de orden actuales** —Asignada, Cerrada, Suspendida— son subconjunto de los siete
   de `EOT_EstadosOrden`, y las 6 órdenes existentes resuelven contra ellos.
3. **`d02d8a3d` se conserva** como único checklist válido, aunque su `Finalizado` sea `FALSE`.
4. **El identificador `3aa202ee` de `USR_Usuarios` se conserva** tal cual. Homogeneizar claves de
   usuario es otro frente.

## 8. Criterio de cierre

1. `python scripts/validar_modelo.py` devuelve 0 errores.
2. Los encabezados de producción coinciden **uno a uno** con los nombres objetivo, leídos de vuelta
   con el conector de Drive.
3. Las 7 tablas nuevas existen con sus encabezados.
4. `CHK001` y `0356e6d7` ya no están; `d02d8a3d` sí.
5. Las filas de prueba existen, todas con prefijo `TEST-`, y sus `OTID` valen `OT-0001` y `OT-0003`.
6. No se abrió el editor de AppSheet en ningún momento.

El detalle de cómo se comprueba cada punto es `PRUEBA-001`, que todavía no existe. **Sin ella y sin
el veredicto del arquitecto, esta especificación no se ejecuta.**
