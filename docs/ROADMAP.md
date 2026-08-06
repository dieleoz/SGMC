# ROADMAP de implementación — SGMC

**Proyecto:** Sistema de Gestión de Mantenimiento en Campo
**Cliente:** Concesión Transversal del Sisga S.A.S.
**Actualizado:** 6 de agosto de 2026 | **Versión:** 3.0
**Estado actual:** Sprint 0 enviado, a la espera de respuesta del líder funcional. Frente técnico activo: Fase 0.5

> Esta versión corrige la anterior, que declaraba completadas al 100 % la Fase 0 y la Fase 1.
> La auditoría del 6 de agosto de 2026 verificó contra el archivo que esa declaración era falsa.
> Ver [AUDITORIA_PLAN_Y_ROADMAP.md](AUDITORIA_PLAN_Y_ROADMAP.md).
>
> **Actualización del mismo día:** al leer por primera vez el backend de producción se descubrió
> que el Excel local y el Google Sheets son modelos distintos. Se incorpora la Fase 0.5 de
> reconciliación, y los hallazgos se reexpresan contra producción.

---

## 1. Principio de este roadmap

Ninguna fase se declara cerrada sin un **criterio de cierre verificable**: un hecho que otra
persona pueda comprobar leyendo el archivo o el sistema, no un reporte de avance.

La versión anterior de este documento no tenía criterios de cierre. Por eso pudo marcar como
completadas fases que dejaron cuatro tablas vacías y el control GPS inoperante.

---

## 2. Estado por fase

| Fase | Estado | Criterio de cierre |
|---|---|---|
| Sprint 0. Definición funcional | **Enviado, esperando respuesta** | Respuesta del líder funcional a las 14 decisiones, o supuesto declarado por vencimiento |
| Fase 0.5. Reconciliación de modelos | **En curso, bloqueante** | Un solo modelo declarado como válido, y el otro retirado o alineado por decisión explícita |
| Fase 1. Datos maestros | Bloqueada por Sprint 0 y Fase 0.5 | Coordenadas reales cargadas, columnas de GPS presentes en producción, sedes realineadas, bancos priorizados construidos |
| Fase 2. Configuración | Bloqueada por Fase 1 | Reglas, filtro, formularios, bots y reportes configurados y verificados en la app |
| Fase 3. Prueba controlada | Bloqueada por Fase 2 | Registros reales en `MAN_Mantenimientos` y en las tablas de evidencia, verificados leyendo el archivo |
| Fase 4. Piloto de campo | Bloqueada por Fase 3 | 10 técnicos operando una semana, con registros sincronizados desde el corredor |
| Fase 5. Producción y evolución | Bloqueada por Fase 4 | Los 18 tipos con banco de preguntas, integraciones y respaldo automático |

**No hay fechas.** El cronograma depende de dos tareas que son trabajo del cliente y cuya duración
solo el equipo de la Concesión puede estimar: el levantamiento de las coordenadas reales de los 34
activos (decisión D-01) y la redacción de los bancos de preguntas (decisión D-09). Las fechas se
fijan en el acta de la mesa de trabajo, no antes.

---

## 3. Lo que sí está construido

Verificado el 6 de agosto de 2026 leyendo `BD/Modelo de Datos (2).xlsx` con `openpyxl`.

- Modelo relacional de 24 tablas en ambos entornos. `Coordenadas_Cierre` y `Precision_GPS` ya
  están en los dos: en producción se agregaron el 6 de agosto de 2026, pendientes de que la
  aplicación las reconozca. Ver Fase 0.5.
- En producción, el mapeo de cada tipo de activo a su formulario está completo en los 18 tipos, y
  el detalle de checklist es relacional mediante `PreguntaID`.
- Catálogos poblados: 34 activos con código QR, 18 tipos de activo, 10 sedes, 4 roles,
  11 usuarios, y catálogos viales de calzada, sentido, estado y frecuencia.
- 6 órdenes de trabajo registradas y 1 checklist de inspección SOS con su detalle.
- Banco de preguntas del formulario de postes SOS: 15 preguntas con secciones, tipos de
  respuesta, rangos y unidades.
- Aplicación AppSheet publicada, con vistas móviles y web y autenticación corporativa.

---

## 4. Sprint 0 — Definición funcional (enviado, esperando respuesta)

El documento y su correo ya salieron al líder funcional. **No se reenvía ninguna versión
posterior:** volver a escribir sobre lo mismo confunde y resta credibilidad a la petición. Las
correcciones y afinamientos posteriores se acumulan para un Sprint 2 con el funcional.

- [x] Enviar el documento al líder funcional
- [ ] Recibir respuesta a las 14 decisiones
- [ ] Consolidar las respuestas en un acta de decisiones
- [ ] Sprint 2 con el funcional: lo que quede abierto, más lo aprendido entretanto

**Cierra cuando:** hay respuesta escrita. Toda decisión no resuelta queda con el supuesto que el
documento declaró marcado, y ese supuesto es vinculante.

**Mientras tanto no se está bloqueado.** La Fase 0.5 es trabajo técnico que no depende del líder
funcional y puede avanzar en paralelo.

---

## 4.5 Fase 0.5 — Reconciliación de modelos (nueva, bloqueante)

El 6 de agosto de 2026, al leer por primera vez el backend de producción, se encontró que **el
Excel local y el Google Sheets no son el mismo modelo**. El Excel tiene las columnas de GPS pero
no el mapeo de formularios; producción tenía el mapeo y no las columnas, hasta que estas se
agregaron ese mismo día. Difieren además en `CHK_Checklists` y `CHD_ChecklistDetalle`. Alguien ha
estado editando ambos por separado.

Mientras esto no se resuelva, cualquier trabajo de configuración se hace sobre un blanco móvil.

- [ ] Decidir cuál de los dos modelos es el válido, y dejarlo por escrito
- [x] **Crear las dos columnas de GPS en el Sheets de producción.** Hecho el 6 de agosto de 2026
      en `Z1` y `AA1` de `MAN_Mantenimientos`, verificado celda por celda
- [x] **Hacerlas visibles en la aplicación:** *Regenerate Structure* ejecutado el 6 de agosto de
      2026, la tabla pasó de 26 a 28 columnas; tipadas `LatLong` y `Number`; aplicación guardada
- [ ] **POR AJUSTAR — cablear las referencias del modelo.** `MAN_Mantenimientos.OTID` es `Text` y
      debe ser `Ref` a `OT_OrdenesTrabajo`; confirmar que `OT_OrdenesTrabajo.Activo` sea `Ref` a
      `ACT_Activos`. Sin esto no hay geofencing, ni navegación padre-hijo, ni reportes por activo
- [ ] **POR AJUSTAR — escribir la regla de geofencing** una vez cableadas las referencias:
      `DISTANCE([Coordenadas_Cierre], [OTID].[Activo].[Ubicacion]) <= 1.0`, con su mensaje de error
- [ ] **POR REVISAR — cargar coordenadas reales de la vía de la Concesión**, al menos un subconjunto
      para poder validar el geofencing antes del levantamiento completo de D-01
- [ ] **POR REVISAR — poblar la base con datos de prueba** y ejercitar la aplicación, para
      determinar qué tablas reciben escrituras, cuáles son legacy o quedaron sin relacionar, y
      dónde escriben realmente los disparadores
- [ ] Resolver qué hacer con las columnas que solo tiene producción (`Diagnostico`,
      `Trabajo_Realizado`, `Duracion_Minutos`, `Repuestos_Utilizados`, `Requiere_Repuesto`)
- [ ] Retirar el modelo perdedor o dejarlo marcado como histórico, para que nadie lo siga editando
- [ ] Limpiar los datos de prueba de `CHK_Checklists` (`CHK001` con nombre en vez de identificador
      y `NOW()` como texto)
- [ ] Dejar por escrito quién puede editar el Sheets de producción y bajo qué autorización

**Cierra cuando:** existe un solo modelo declarado válido, con las columnas de GPS presentes **y
visibles en la aplicación**, y una regla escrita de quién lo edita.

### 4.5.1 Especificación del cambio en `MAN_Mantenimientos`

Ejecuta quien tenga permiso de edición sobre el Sheets. El documento es propiedad de
`valentinwebdeveloper@gmail.com`, y la cuenta del cliente también tiene permiso de escritura.
El paso 1 ya está aplicado; los pasos 2 a 4 requieren el editor de AppSheet.

**Paso 1. En el Google Sheets** — **HECHO el 2026-08-06.** Se agregaron dos columnas al final de
la hoja `MAN_Mantenimientos`, que terminaba en `Activo` (columna Y):

| Celda | Encabezado exacto | Contenido |
|---|---|---|
| `Z1` | `Coordenadas_Cierre` | Vacío. Lo llena la aplicación al cerrar |
| `AA1` | `Precision_GPS` | Vacío. Lo llena la aplicación al cerrar |

Verificado leyendo cada celda en la barra de fórmulas. Las mayúsculas y el guion bajo importan:
AppSheet resuelve las columnas por nombre exacto.

**Paso 2. En el editor de AppSheet**, en `Data` sobre la tabla `MAN_Mantenimientos`, ejecutar
**Regenerate Structure**. Sin este paso las columnas existen en la hoja pero la aplicación no las
ve, y todo lo demás falla en silencio.

**Paso 3. Tipar las columnas:** `Coordenadas_Cierre` como `LatLong` y `Precision_GPS` como
`Number`. Si quedan como `Text`, la función de distancia no opera.

**Paso 4. Configurar las reglas** sobre `Coordenadas_Cierre`:

```
Initial value:  HERE()
Valid_If:       DISTANCE([Coordenadas_Cierre], [ActivoID].[Ubicacion]) <= 1.0
Invalid text:   Ubicación fuera de rango: debe estar a menos de 1.0 km del activo.
```

Y sobre `Precision_GPS`, valor inicial `USERLOCATIONACCURACY()`.

**Advertencia sobre el alcance de este cambio.** Los pasos 1 a 3 están hechos. El paso 4 **no se
pudo ejecutar**: al escribir la regla, AppSheet reveló que `MAN_Mantenimientos` no tiene ninguna
columna que apunte al activo, y que `OTID` no es una referencia sino texto. Ver la sección 10 del
dictamen de auditoría. La regla queda pendiente del cableado de referencias.

Aunque se cablee, el geofencing seguirá sin funcionar mientras los 34 activos compartan la
coordenada de Bogotá (D-01) y el radio esté sin confirmar (D-02).

**Criterio de cierre de este punto:** una fila de prueba escrita en `MAN_Mantenimientos` desde la
aplicación, con valor en las dos columnas nuevas, verificada leyendo el Sheets.

---

## 5. Fase 1 — Datos maestros

Es la fase más larga y la que fija el cronograma. Su contenido depende de las decisiones tomadas.

- [ ] **D-01.** Levantamiento en campo de las coordenadas reales de los 34 activos y carga en
      `ACT_Activos.Ubicacion`. Verificar de paso que el QR físico esté instalado y legible
- [ ] **D-09.** Construcción de los bancos de preguntas de los tipos priorizados en
      `FRM_Preguntas`
- [ ] Mapeo de `TIP_TiposActivo.FormularioID` para los 18 tipos
- [ ] Realineación de `SedeID` entre `USR_Usuarios` y `ACT_Activos` según lo decidido en D-03
- [ ] Remediación del checklist huérfano `d02d8a3d`, cuyo `OTID` no corresponde a ninguna orden
- [ ] Corrección de los encabezados con codificación corrupta en el Excel

**Cierra cuando:** las 34 coordenadas son distintas y están sobre el corredor; los tipos
priorizados resuelven su formulario; y un usuario de prueba ve activos al aplicar el filtro.

---

## 6. Fase 2 — Configuración en AppSheet

Solo después de las decisiones de arquitectura A-1 a A-5 del dictamen de auditoría.

- [ ] Regla de geofencing `DISTANCE([Coordenadas_Cierre], [ActivoID].[Ubicacion]) <= 1.0` con el
      radio decidido en D-02, y mensaje de error en texto plano
- [ ] Manejo de excepción por precisión GPS insuficiente, según D-04
- [ ] Security Filter por sede, verificado con una cuenta real de técnico
- [ ] Modelo definitivo de evidencias, según D-10: campos en `MAN` o tablas hijas, nunca ambos
- [ ] Estados de la orden de trabajo y transiciones, según D-06
- [ ] Bot de notificación de asignación y bot de alerta por activo fuera de servicio
- [ ] Reportes y tablero, según D-12 y D-13

**Cierra cuando:** cada regla se demuestra funcionando en la app, no solo configurada.

---

## 7. Fase 3 — Prueba controlada

Etapa que no existía en la versión anterior y cuya ausencia habría llevado el primer error real
directamente a los 10 celulares del piloto.

- [ ] Un mantenimiento completo de extremo a extremo, ejecutado por una persona sobre un activo
      con coordenada real: apertura por QR, checklist, fotografías, firma y cierre con GPS
- [ ] El mismo flujo repetido en modo avión, con verificación de la sincronización posterior
- [ ] Prueba del bloqueo: intentar cerrar lejos del activo y confirmar que el sistema lo impide

**Cierra cuando:** hay filas reales en `MAN_Mantenimientos` y en las tablas de evidencia,
verificadas leyendo el archivo. Hoy esas cuatro tablas están vacías.

---

## 8. Fase 4 — Piloto de campo

- [ ] Instalación en los 10 móviles del grupo piloto y autenticación corporativa
- [ ] Verificación de que cada técnico descarga solo los activos de su zona
- [ ] Operación real durante una semana, con acompañamiento
- [ ] Registro de incidencias y ajuste de formularios según lo observado

**Cierra cuando:** los 10 técnicos completaron mantenimientos sincronizados desde el corredor y
las incidencias críticas están resueltas.

---

## 9. Fase 5 — Producción y evolución

- [ ] Construcción de los bancos de preguntas de los tipos de activo restantes, en tandas
- [ ] Generación automática de órdenes por frecuencia de mantenimiento, si se decide en D-06
- [ ] Integración con Power BI para tableros ejecutivos
- [ ] Integración con mesas de ayuda para tickets de TI
- [ ] Respaldo automático de evidencias y base de datos

---

## 10. Qué cambió frente a la versión anterior

| Afirmación anterior | Realidad verificada |
|---|---|
| "Fase 0 y 1: completado 100 %" | 8 bloqueantes abiertos |
| "Modelo de datos 17 tablas: done" | El modelo vigente tiene 24 hojas |
| "18 formularios dinámicos: done" | 1 de 18 con banco de preguntas, y sin mapeo desde el tipo de activo |
| "Validaciones GPS y Security Filter: done" | GPS inoperante por coordenada única; el filtro dejaría a los técnicos sin activos |
| "Pruebas QA y dictamen: done" | `MAN_Mantenimientos` vacía: el flujo nunca se ejecutó |
| "Estado actual: Fase 1.5, piloto" | El proyecto está en Sprint 0, definición funcional |

---
*Referencias:* [README.md](../README.md) | [AUDITORIA_PLAN_Y_ROADMAP.md](AUDITORIA_PLAN_Y_ROADMAP.md) | [DEFINICION_FUNCIONAL_MESA_DE_TRABAJO.md](DEFINICION_FUNCIONAL_MESA_DE_TRABAJO.md) | [MAP.md](../MAP.md)
