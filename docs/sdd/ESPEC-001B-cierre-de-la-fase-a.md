# ESPEC-001B — Cierre real de la Fase A

La Fase A se reportó como «100% cerrada y validada». **No lo está.** Verificado el 2026-08-07 con
`python scripts/verificar_faseA.py "BD/Modelo de Datos (4).xlsx"`: **27 puntos conformes y 19
fallos**.

Esto no es un reproche al trabajo hecho, que en su mayor parte está bien: los 23 renombrados
llegaron, la limpieza de `CHK_Checklists` se hizo conservando `d02d8a3d`, y `UNF_UnidadesFuncionales`
quedó con las claves 7 a 10, que es justo lo que hacía falta para que los 34 activos siguieran
resolviendo. Lo que falla es lo que quedó a medias.

## 1. El fallo que hay que corregir antes que ningún otro

**F-08. `EOT_EstadosOrden` usa claves numéricas y `OT_OrdenesTrabajo.EstadoOrdenID` guarda texto.**

| `EOT_EstadosOrden` tiene | `OT_OrdenesTrabajo.EstadoOrdenID` guarda |
|---|---|
| `1, 2, 3, 4, 5, 6, 7` | `Asignada`, `Cerrada`, `Suspendida` |

Una referencia de AppSheet guarda **el valor de la clave del destino**. Con esto tal cual, convertir
`EstadoOrdenID` a `Ref` en la Fase B **deja las 6 órdenes huérfanas, y en silencio**. Es exactamente
el defecto que este proyecto lleva meses arrastrando con `OTID`, reproducido en una tabla creada
ayer.

Se ve bien en la hoja. Solo se rompe cuando se cablea.

### Corrección

**Cambiar las 7 claves de `EOT_EstadosOrden` por el nombre del estado**, no los datos de las
órdenes:

| Celda | Valor actual | Valor correcto |
|---|---|---|
| `A2` | `1` | `Programada` |
| `A3` | `2` | `Asignada` |
| `A4` | `3` | `En ejecucion` |
| `A5` | `4` | `En revision` |
| `A6` | `5` | `Cerrada` |
| `A7` | `6` | `Suspendida` |
| `A8` | `7` | `Vencida` |

Se corrige el catálogo y no la transaccional **a propósito**: `EOT_EstadosOrden` se creó ayer y no
tiene todavía ningún dependiente, mientras que tocar `OT_OrdenesTrabajo` sería migrar datos reales.
Ante la duda, se mueve lo que no tiene historia.

Rellenar de paso `QuienCambia`, que quedó vacío: `Sistema` para Programada y Vencida, `Supervisor`
para Asignada, Cerrada y Suspendida, `Tecnico` para las dos de ejecución y revisión.

## 2. Tablas nuevas que quedaron como cáscara

Cuatro se crearon solo con dos columnas y sin filas.

### `ASG_AsignacionZona` — la que más consecuencia tiene

Tiene `AsignacionZonaID | Nombre`. Debe tener:

| Columna | Contenido |
|---|---|
| `AsignacionID` | `ASG-01` a `ASG-04` |
| `UsuarioID` | `3`, `4`, `5`, `6` (los técnicos, RolID 4) |
| `UnidadFuncionalID` | `7`, `8`, `9`, `10` |
| `Activo` | `TRUE` |

**Sin filas aquí, el Security Filter de la Fase B deja a cada técnico con cero activos.** Es el
bloqueante B-03 en su forma nueva: antes los usuarios estaban en una sede y los activos en otra;
ahora simplemente no hay tabla que los una.

### `MOT_MotivosPendiente`

Tiene `MotivoPendienteID | Nombre`. Faltan `GeneraSeguimiento` y `Activo`, y las 5 filas:
`MOT-01` Falta de repuesto, `MOT-02` Clima, `MOT-03` Acceso restringido, `MOT-04` Riesgo para el
técnico, `MOT-05` Requiere especialista. Todas con `GeneraSeguimiento = TRUE` y `Activo = TRUE`.

### `FAL_ModosFalla`, `NOV_Novedades`, `PLA_PlanMantenimiento`

Solo encabezados, y son los que tocan. Van sin filas —se pueblan en otro frente— pero **con sus
columnas completas**, o AppSheet no tendrá qué leer al regenerar:

- `FAL_ModosFalla`: `ModoFallaID`, `TipoActivoID`, `Nombre`, `Componente`, `Criticidad`, `Activo`
- `NOV_Novedades`: `NovedadID`, `UsuarioID`, `Tipo`, `Descripcion`, `Ubicacion`, `Fotografia`,
  `ActivoID`, `Estado`, `FechaHora`
- `PLA_PlanMantenimiento`: `PlanID`, `ActivoID`, `FrecuenciaID`, `UltimaEjecucion`, `ProximaFecha`,
  `ResponsableID`, `Activo`

## 3. Columnas que faltan en tablas existentes

| Tabla | Añadir | Para qué |
|---|---|---|
| `ACT_Activos` | `Criticidad` | Pondera la disponibilidad de D-13 |
| `OT_OrdenesTrabajo` | `Tipo` | Preventivo o Correctivo. Hoy no se distingue |
| `FOT_Fotografias` | `Tipo`, `Ubicacion`, `PrecisionGPS`, `FechaHora` | **Es la cadena de evidencia.** Sin coordenada y hora por fotografía no hay prueba de presencia, que es para lo que existe el sistema |
| `FIR_Firmas` | `FechaHora` | Igual |
| `CAL_Calzadas`, `SEN_Sentidos`, `TPR_TiposRespuesta` | `Activo` | Retirar un valor sin romper el histórico |
| `FRM_Preguntas` | `Version` | Supuesto D-11 |

Las de `FOT_Fotografias` son las únicas de esta lista que no son higiene: sin ellas el sistema no
cumple su propósito.

## 4. Nombres con tilde y una clave mal nombrada

AppSheet resuelve las columnas **por nombre literal**, de modo que una tilde obliga a escribirla en
cada expresión. Renombrar sin tilde:

| Tabla | Actual | Correcto |
|---|---|---|
| `ROL_Roles` | `Descripción` | `Descripcion` |
| `FRM_Formularios` | `Descripción`, `Versión` | `Descripcion`, `Version` |
| `LST_ValoresLista` | `ListaID` | `ValorListaID` |

`LST_ValoresLista.ValorListaID` es un renombrado que no estaba declarado en el modelo. Ya se corrigió en
`scripts/modelo_objetivo.py`.

## 5. Lo que NO es un fallo, aunque lo parezca

**`OT_OrdenesTrabajo` tiene dos columnas relacionadas con `Activo`, y está bien.** La original se
renombró a `ActivoID` y se creó una nueva `Activo` al final, que es la bandera `Yes/No`. Es
exactamente lo que preveía el aviso V-14 del validador, y lo que la especificación pedía.

Mi propia función `verificar()` del Apps Script lo marcaba como error: comprueba «el nombre viejo ya
no existe» y no sabe distinguir una reutilización legítima. **Es un defecto de esa función, no de la
hoja.** `scripts/verificar_faseA.py` ya lo distingue correctamente, consultando si el modelo
objetivo reutiliza ese nombre.

## 6. Lo que sigue pendiente y es correcto que lo esté

- **40 columnas marcadas como retiradas siguen en la hoja** —13 en `MAN`, 15 en `CHK`, 12 en `CHD`,
  3 en `OT`—. La Fase A no borra nada, deliberadamente: borrar es lo único que el respaldo no
  vuelve gratis.
- **14 columnas siguen sin retipar a `Ref`.** Es la Fase B, en el editor de AppSheet.
- **`MAN_Mantenimientos` sigue con 0 filas.** Los datos de prueba no se escribieron. No es
  bloqueante para la Fase B, y mantiene la propiedad de que convertir `OTID` a `Ref` no arrastra
  nada.

## 7. Criterio de cierre

```
python scripts/verificar_faseA.py "BD/Modelo de Datos (N).xlsx"
```

Debe imprimir **`FASE A CERRADA`**, con 0 fallos. Los avisos son esperados y no bloquean.

Para volver a verificar: *Archivo → Descargar → Microsoft Excel*, guardar en `BD/` y correr el
comando. No hace falta Apps Script, que la cuenta bloquea.
