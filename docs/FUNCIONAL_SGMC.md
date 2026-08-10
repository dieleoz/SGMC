# SGMC — Documento funcional

Qué hace el sistema, para quién, cómo y para qué. **Este es el documento que se entrega al
funcional.** Todo lo demás —especificaciones, actas, base de conocimiento— es material de trabajo.

| | |
|---|---|
| Sistema | Gestión de Mantenimiento en Campo · Concesión Transversal del Sisga S.A.S. |
| Plataforma | Google AppSheet `SISGA_-323965761-26-08-10` sobre la hoja `Modelo_Datos_10082026` |
| Verificado contra | `scripts/modelo_objetivo.py` y `BD/Modelo_Datos_PLANTILLA.xlsx` |
| Fecha | 2026-08-10 |

> **Hay una sola aplicación y una sola hoja, y son las de la tabla de arriba.** Entre el 6 y el 10 de
> agosto de 2026 hubo cinco aplicaciones y tres hojas; las superadas están nombradas, con su motivo,
> en `scripts/sistema.py`. Si un documento menciona otra, describe algo que ya no existe.
>
> **Nada de lo funcional cambió por las reconstrucciones** —el modelo de datos es el mismo—, pero sí
> cambió lo que está montado: la aplicación de hoy **tiene las 28 tablas dadas de alta y nada más.**
> Las referencias, las reglas y los filtros están sin poner. Este documento describe qué hace el
> sistema; qué falta para que lo haga está en [`../ESTADO.md`](../ESTADO.md).

**Regla de este documento: una sola forma por propósito.** Si dos mecanismos pueden resolver lo
mismo, aquí se elige uno y se dice cuál se descarta. La sección 6 es el registro de esas decisiones,
y existe porque con tanto material acumulado el riesgo real es proponer dos cosas para lo mismo y
que el funcional implemente las dos.

---

## 1. Para qué existe el sistema

**Para responder una pregunta que hoy se responde a mano: cuánto de lo planeado se ejecutó.**

Así se lleva hoy el mantenimiento —rejilla semanal, tareas en filas, sectores en columnas, y al pie
la cuenta—:

```
                              BQ   QB   BV    V
PRUEBA SEMANAL POSTES SOS      X         X    X
VERIFICACIÓN SEMANAL MÁSCARAS  X         X
...
TAREAS EJECUTADAS              5   10    5    2   = 22
TAREAS NO EJECUTADAS           1    1    0    0   =  2      → 91,7 %
```

Ese 91,7 % se teclea. Alguien recoge partes en papel, cuenta y transcribe. **Con el sistema, esa
cifra es una resta entre lo programado y lo cerrado, y sale sola.**

Todo lo demás —evidencia fotográfica, geolocalización, firmas, histórico— existe para que esa cifra
sea **defendible ante la interventoría**, no solo cierta.

## 2. Qué se mantiene

**El Plan Maestro lista 24 tipos de equipo.** De esos, **18 se cuentan por unidades y son los que
se visitan: suman los 355 activos contables**, y son los 18 que aparecen en el bloque de abajo. Los
seis restantes no se cuentan en unidades: la fibra troncal va en kilómetros, e internet, antivirus,
licencias, radios y certificados SSL no se visitan porque no tienen coordenada.

> **Y `TIP_TiposActivo` tiene 27, que es otra lista.** No es el catálogo del inventario sino **el de
> checklists**: un tipo por cada formulario. Son los 18 de arriba más nueve equipos que existen en el
> corredor y el Plan Maestro no cuenta por unidades —fibra óptica, generador, video wall, router,
> firewall, UPS, NAS, subestación y báscula estática—, que hasta el 2026-08-09 colgaban del checklist
> de otro equipo. **Dos listas del mismo dominio no son la misma lista**: la correspondencia vive en
> `scripts/catalogo_tipos.py` y la comprueba `comprobar()`.

```
Vía          postes SOS 54 · CCTV 26 · PMV fijos 11 · PMV móviles 19
             gálibos 8 · sensores meteo 4 · ETD 4 · pasos seguros 16
Comunicac.   switches capa 2  142 · capa 3  4 · fibra troncal 137 km
Peajes       carriles 12 · electrónica 12
Pesajes      básculas 2 · OCR 2
TI           servidores 7 · portátiles 29 · impresoras 3
```

**Y cinco cosas que no se visitan:** antivirus, licencias, certificados SSL, radios e internet. No
tienen coordenada. Todo el mecanismo de evidencia de ubicación no les aplica — ver 6.11. **Ninguna de
las cinco tiene fila en `TIP_TiposActivo`**, así que hoy no se pueden ni registrar.

> **Cuidado al contar activos: 355 y 368 son cifras de cosas distintas.** 355 son los que el Plan
> Maestro cuenta por unidades. `ACT_Activos` en `BD/Modelo_Datos_PLANTILLA.xlsx` tiene **368 filas**:
> esos 355 más **13 equipos que solo existen en el juego de datos de arranque** —generador, báscula
> estática, fibra, video wall, router, cortafuegos, UPS, NAS y subestación— y que el Plan Maestro no
> cuenta por unidades. Las 368 se derivan leyendo la hoja, no se citan de memoria.

## 3. Quién lo usa

| Perfil | Dispositivo | Qué hace |
|---|---|---|
| **Técnico de campo** | Móvil, con trabajo sin cobertura | Ejecuta la orden, responde el checklist, toma fotografías, firma. **No cierra la orden** |
| **Supervisor** | Web o tableta | Programa, asigna, **revisa y cierra**. Suspende |
| **Consulta / interventoría** | Web | Audita y exporta. No escribe |
| **Administrador** | Web | Usuarios, activos, catálogos, plantillas de checklist |

## 4. El ciclo de una orden, y por qué el técnico no la cierra

`EOT_EstadosOrden` lleva una columna `QuienCambia` que define quién mueve cada estado:

```
Programada   → Sistema
Asignada     → Supervisor
En ejecución → Técnico
En revisión  → Técnico      ← aquí el técnico termina y suelta
Cerrada      → Supervisor   ← quien ejecuta no certifica
Suspendida   → Supervisor
Vencida      → Sistema
```

**El técnico deja la orden «En revisión»; el supervisor la recibe y la cierra.** Quien hace el
trabajo no certifica que se hizo. Es la misma doctrina por la que en este proyecto quien aplica un
cambio no toca la comprobación que lo mide.

> **Estado real:** `QuienCambia` está escrita en la tabla, **pero ninguna regla la impone**. Hoy nada
> impide que un técnico ponga «Cerrada» él mismo. El modelo describe la separación y no la aplica.
> Es una de las piezas pendientes — ver sección 8.

Falta además una cosa para que la recepción esté completa: **no hay estado de rechazo.**
`MAN_Mantenimientos.ObservacionRechazo` existe y la orden no tiene a dónde volver, porque
`EOT_EstadosOrden` tiene siete filas —`Programada`, `Asignada`, `En ejecucion`, `En revision`,
`Cerrada`, `Suspendida`, `Vencida`— y ninguna es una devolución. **Eso no cuesta una columna: cuesta
una fila** en un catálogo que ya existe, más la regla que la escriba.

> **Lo que sí está resuelto, y algún documento anterior daba por pendiente:**
> `FIR_Firmas.TipoFirma` **tiene sus valores declarados** en el modelo —la lista es `Tecnico`, y solo
> ese—. Es deliberado: por el supuesto D-10 el supervisor aprueba en el portal y no firma en campo, y
> por eso `MAN_Mantenimientos.Firma_Supervisor` está retirada. La columna sigue siendo `Enum` y no
> `Text` precisamente para que añadir `Tercero`, si operación lo pide, sea configuración y no
> migración.

## 5. Qué prueba el sistema, y qué no

Esto hay que decirlo entero, porque es lo que se defiende ante un tercero.

**Prueba:**

- Que alguien registró una ejecución en una fecha, con una coordenada y una precisión declarada
- Qué se respondió en cada pregunta del checklist
- Qué fotografías se tomaron, con su coordenada y su hora
- Que un supervisor la recibió

**No prueba:**

- **Que el técnico estuviera trabajando.** El geofencing confirma proximidad, no actividad. En un
  tramo de fibra con radio de kilómetro y medio, confirma que estaba en ese tramo del corredor
- **Nada frente a quien escriba directamente en el Google Sheets.** Todas las validaciones viven en
  la capa de aplicación. Hoy hay dos cuentas con permiso de edición sobre la hoja. **Esto no es
  gobierno, es arquitectura**: la hoja no impone unicidad, ni tipos, ni integridad referencial

## 5.1 Cómo se encadenan las tablas

**Derivado de `scripts/modelo_objetivo.py`**, que declara 28 tablas y 39 referencias. Se pone aquí
porque tres decisiones de la sección 6 solo se entienden mirando la cadena, y porque varios
documentos la habían dibujado a mano y de más de una forma.

```
USR_Usuarios ──> ROL_Roles                ASG_AsignacionZona ──> USR_Usuarios
             ──> SED_Sedes                                   ──> UNF_UnidadesFuncionales

ACT_Activos  ──> TIP_TiposActivo ──> FRM_Formularios
             ──> UNF_UnidadesFuncionales     · CAL_Calzadas · SEN_Sentidos
             ──> EST_Activo                  · FRE_Frecuencias

OT_OrdenesTrabajo ──> ACT_Activos · EOT_EstadosOrden · OT_OrdenesTrabajo (OTOrigenID)
                  ──> USR_Usuarios, tres veces: TecnicoID, SupervisorID, CerradaPor
      │
      └──< MAN_Mantenimientos   SIN IsPartOf
                  ──> USR_Usuarios · EST_Activo · MOT_MotivosPendiente · FAL_ModosFalla
             │
             ├──< FOT_Fotografias        IsPartOf
             ├──< FIR_Firmas             IsPartOf
             └──< CHK_Checklists         IsPartOf  ──> FRM_Formularios
                        └──< CHD_ChecklistDetalle  IsPartOf  ──> FRM_Preguntas

FRM_Preguntas ──> FRM_Formularios · FRM_Secciones · TPR_TiposRespuesta
LST_ValoresLista ──> FRM_Preguntas
NOV_Novedades ──> USR_Usuarios · ACT_Activos        PLA_PlanMantenimiento ──> ACT_Activos ·
FAL_ModosFalla ──> TIP_TiposActivo                                            FRE_Frecuencias ·
                                                                              USR_Usuarios
```

Cuatro cosas que hay que leer bien, porque cada una nació de un error real:

- **`IsPartOf` está en cuatro referencias y solo en cuatro:** las tres que cuelgan del mantenimiento
  y la de `CHD_ChecklistDetalle` contra su checklist. Significa borrado en cascada, no protección: la
  protección es que `OT_OrdenesTrabajo` y `MAN_Mantenimientos` **van sin `Deletes`**. Se corrige con
  `Activo = FALSE`.
- **`MAN_Mantenimientos.OTID` va deliberadamente sin `IsPartOf`.** La ejecución es el registro
  histórico y sobrevive a su orden. Marcarlo haría que borrar una orden se llevara las fotografías,
  la firma y el checklist.
- **`MAN_Mantenimientos` no tiene `ActivoID`.** El activo se alcanza por `[OTID].[ActivoID]`, y esa
  cadena de dos saltos es la que usa el geofencing. Guardarlo también permitiría que la ejecución
  diga un activo y su orden diga otro.
- **`CHK_Checklists` cuelga del mantenimiento, no de la orden.** La inspección es parte de ejecutar.
  La columna se llamó `OTID` y guardaba números de orden; ese desajuste produjo un checklist huérfano.

**Y una que el diagrama enseña por lo que le falta:** `PLA_PlanMantenimiento` apunta a otras tablas y
**nadie apunta a ella**. Por eso «planeadas contra ejecutadas» no es hoy una consulta — ver 8.1.

---

## 6. Una sola forma por propósito

**Registro de decisiones.** Cada fila es un propósito donde había dos caminos posibles. Se eligió
uno. El descartado no se implementa, aunque aparezca mencionado en documentos anteriores o en el
manual de usuario.

| # | Propósito | Se usa | Se descarta | Por qué |
|---|---|---|---|---|
| 6.1 | Periodicidad de un trabajo | `TAR_Tareas.FrecuenciaID` | `ACT_Activos.FrecuenciaID` | Un poste SOS tiene tarea semanal, mensual y trimestral. La periodicidad es de la tarea |
| 6.2 | Qué checklist se abre | `TAR_Tareas.FormularioID` | `TIP_TiposActivo.FormularioID` | El formulario es de la tarea. La columna vieja llevaba 18 fórmulas de hoja de cálculo |
| 6.3 | Dónde trabaja un usuario | `ASG_AsignacionZona` por unidad funcional | `USR_Usuarios.SedeID` | La sede es un edificio; la asignación es un tramo. El filtro de seguridad es por UF |
| 6.4 | Cierre sin GPS válido | `CierreConExcepcion` + `MotivoExcepcion`, con umbral en `PAR_Parametros` | Nota libre en `Observaciones` | Una excepción tiene que ser contable y auditable, no un texto |
| 6.5 | Que hizo falta un repuesto | `MotivoPendienteID` = Falta de repuesto | `Requiere_Repuesto` | Dos sitios que dicen lo mismo permiten decir cosas distintas |
| 6.6 | Qué se hizo en una preventiva | El checklist respondido | `Trabajo_Realizado` en texto libre | El checklist **es** la descripción, ítem por ítem |
| 6.7 | Qué se reparó en una correctiva | Formulario propio de correctivo | Reactivar `Diagnostico` y `Repuestos_Utilizados` | Un formulario no duplica columnas y encaja en la capa de tareas |
| 6.8 | Cuánto duró | Derivar de `FechaHoraInicio` y `FechaHoraFin` | `Duracion_Minutos` almacenada | Un dato derivable no se guarda |
| 6.9 | Coordenada de un activo | `Ubicacion`, tipo LatLong | `Latitud` y `Longitud` separadas | AppSheet trata LatLong como un tipo, y `DISTANCE()` lo exige |
| 6.10 | Preguntas de inspección | `FRM_Preguntas`, que apunta a `FRM_Formularios` **y** a `FRM_Secciones` | Editar `CHD_ChecklistDetalle` | `CHD` guarda **respuestas**. Editarlo para cambiar preguntas corrompe el histórico. Y la sección **no cuelga del formulario**: las 14 son un catálogo plano que comparten los 27 |
| 6.11 | Activos sin ubicación física | Camino sin evidencia de coordenada | Forzarles geofencing | Un certificado SSL no tiene dónde estar. **Decisión pendiente**: camino propio o fuera de alcance |
| 6.12 | Tiempo de reloj parado | Tabla hija de eventos, total por `SUM()` | Columna acumulada | Un acumulado compite consigo mismo sin señal. Es lo que le costó el `Adds` a las órdenes |
| 6.13 | Marca de tiempo que sirve de prueba | `ChangeTimestamp` en la transición de estado, con `Editable_If = FALSE` | `Initial value = NOW()` | Un `Initial value` **es editable**, y `NOW()` es el reloj del teléfono |
| 6.14 | Catálogo de roles | **`ROL_Roles`, que ya existe** | Crear una tabla nueva | Ya está en el modelo. Falta poblarla con los doce roles del Plan Maestro |

**Sin resolver, y hay que resolverlo:**

| # | Propósito | Camino A | Camino B |
|---|---|---|---|
| 6.16 | Que hace falta volver | `MAN.RequiereSegundaVisita` | `OT.OTOrigenID`, orden nueva encadenada | Sin resolver. Los dos existen |

### 6.15 — La recepción del trabajo: no se elige, se relaciona

Parecía una duplicación y no lo es. `MAN_Mantenimientos.OTID` es una referencia, de modo que **una
orden puede tener varias ejecuciones**: el técnico va, no puede terminar, vuelve otro día.

| Acto | Dónde vive | Qué afirma |
|---|---|---|
| `AprobadoSupervisor` · `FechaAprobacion` | En la **ejecución** | «Acepto esta visita como evidencia válida» |
| `EstadoOrdenID = Cerrada` · `CerradaPor` | En la **orden** | «El trabajo terminó, no hacen falta más visitas» |

Son dos niveles distintos y los dos hacen falta. **Lo que falta es la regla que los une: una orden
no se puede cerrar mientras alguna de sus ejecuciones esté sin aprobar.** Hoy nada lo impide, y por
eso los dos campos parecían decir lo mismo.

Queda como requisito para `ESPEC-003`, con su prueba negativa: intentar cerrar una orden con una
ejecución no aprobada tiene que fallar.

---

## 7. Lo que no cabe en la plataforma

No es «más adelante». Es **no en el plan actual**, y solo cambia con la decisión de licenciamiento.

| Lo que se querría | Por qué no |
|---|---|
| **Generación automática de las órdenes del mes** | El plan gratuito no ejecuta procesos programados. Las órdenes se crean a mano o por carga |
| **Aviso al supervisor de que hay algo por recibir** | Lo mismo. El supervisor tiene que entrar a mirar |
| **Integración con el SCADA para abrir correctivas** | Sin plan Core no hay API REST |
| **Atributos distintos por tipo de equipo** | El backend es una hoja: no hay esquema dinámico. Se paga con columnas vacías |
| **Garantía de unicidad de un consecutivo** | Offline-first: dos técnicos sin señal generan el mismo número |
| **Que una escritura directa en la hoja respete las validaciones** | Imposible por diseño de la plataforma |

**Volumen.** Las cifras salen de `python scripts/capacidad.py`, que tiene cuatro escenarios. Con los
**355 activos** del Plan Maestro:

```
CHD_ChecklistDetalle   76.680 filas/año  ->  383.400 a 5 años   (AppSheet degrada sobre ~50.000)
Almacenamiento          2,62 GB/año      ->  13,10 GB a 5 años  (87% de los 15 GB)
La cuota se agota en    5,7 años
```

**Archivar por año no es opcional:** la tabla de detalle pasa el umbral de sincronización en el
primer año. Y **la cuota de 15 GB de la cuenta que hoy posee el backend dura 5,7 años frente a los 5
de retención exigida**, es decir, no sobra nada. Si el corredor crece a 500 activos, el escenario que
también calcula el script, la cuota se agota **en 4,1 años, antes de la retención**.

---

## 8. Estado: qué existe, qué está especificado, qué es futuro

**Tres columnas, porque hay tres cosas distintas.** Que el modelo lo declare no significa que la hoja
lo traiga, y que la hoja lo traiga no significa que la aplicación lo tenga montado. Confundir las
tres es lo que hizo que este documento dijera durante un día que las referencias estaban puestas.

| | En el modelo | En la hoja | En la aplicación |
|---|---|---|---|
| Modelo de datos, 28 tablas | **Sí.** 205 columnas, 39 referencias, 21 reglas | **Sí.** 28 pestañas más `_LEEME`, ninguna columna de sobra. `FASE A CERRADA` con 52 conformes | **Las 28 tablas dadas de alta, y nada más** |
| Referencias entre tablas | **Sí.** Las 38, con `IsPartOf` en cuatro: `FOT`, `FIR` y `CHK` contra el mantenimiento, y `CHD` contra su checklist | No aplica: la hoja no tiene integridad referencial | **No. Sin poner** |
| Geofencing y filtros de seguridad | **Sí.** `RG-01`, `RG-04` y `RG-05` con su expresión completa | El radio por tipo está poblado en los 27 | **No. Sin poner** |
| Plantillas de checklist | **Sí** — `FRM_Formularios`, `FRM_Secciones`, `FRM_Preguntas`, `TPR_TiposRespuesta` | **27 formularios**, uno por tipo de activo, y 14 secciones | Tablas de alta, sin vistas |
| Banco de preguntas | — | **333 preguntas, los 27 formularios con contenido.** 288 llevan `[BORRADOR: validar con operacion]`; las 45 acordadas son SOS, CCTV y PMV fijo, 15 cada uno | — |
| Catálogo de roles | `ROL_Roles` existe | **4 filas**: Administrador, Supervisor, Técnico, Consulta. Faltan los doce oficios del Plan Maestro | — |
| Inventario | — | **368 filas** en `ACT_Activos`: 334 sintéticas, marcadas como tales en `Observaciones`, y 34 del juego de arranque. **No es el registro real** | — |
| Coordenadas de los activos | `ACT_Activos.Ubicacion`, `LatLong`, obligatoria | **Ninguna es real.** Las 34 comparten un punto de Bogotá; las 334 están interpoladas sobre el corredor | — |
| Registros de prueba | — | **Ninguno.** `OT`, `MAN`, `CHK`, `CHD`, `FOT`, `FIR`, `NOV` y `PLA` están vacías | El ciclo no se ha recorrido |
| Capa de tareas `TAR_Tareas` | **No.** Declarada en `PROPUESTAS` | — | — |
| Jerarquía de ubicación | **No.** Declarada en `PROPUESTAS` como `ETR_Estructuras` | — | — |
| Correctivo con criticidad y SLA | **No.** `CRI_Criticidad`, `EVT_EventosOrden` y `PAU_Pausas` en `PROPUESTAS` | — | — |
| Imponer `QuienCambia` y el rechazo | **No.** Ninguna de las 21 reglas lee `QuienCambia` | Falta la fila `Devuelta` en `EOT_EstadosOrden` | — |
| Vistas, acciones y slices | **No están en el modelo.** Mientras no se declaren, la interfaz no se puede generar ni auditar | — | — |
| Certificaciones múltiples, vigencias | `CER_Certificaciones` y `USR_Certificaciones` en `PROPUESTAS` — Fase 2 | — | — |
| Almacén, SAT, flotas | Fuera de alcance | — | — |

### 8.1 Lo que este documento promete y el modelo no puede sostener

**Cada carencia va con el nombre de lo que faltaría**, para que nadie la resuelva inventándose una
columna. Todas están declaradas en `PROPUESTAS` o en `COLUMNAS_PROPUESTAS` de
`scripts/modelo_objetivo.py`, así que no hay que proponerlas otra vez.

| Lo que promete este documento | Qué falta, con nombre |
|---|---|
| §1 — que el porcentaje de cumplimiento **salga solo** | El puente entre lo planeado y lo ejecutado. `PLA_PlanMantenimiento` no la referencia nadie —es el aviso `V-06` de `validar_modelo.py`— y `OT_OrdenesTrabajo` no tiene ninguna columna que diga qué fila del plan satisface. La orden tendría que ganar una referencia a la tarea, y antes hace falta **`TAR_Tareas`** |
| §6.1 — periodicidad por tarea | **`TAR_Tareas`**, con `FrecuenciaID`. Hoy la periodicidad cuelga de `ACT_Activos.FrecuenciaID`, una sola por activo, y un poste SOS tiene inspección y ejecución con ciclos distintos |
| §6.2 — el checklist lo decide la tarea | **`TAR_Tareas.FormularioID`**. Hoy lo decide `TIP_TiposActivo.FormularioID`, uno por tipo |
| §2 — los cinco tipos que no se visitan | **Cinco filas en `TIP_TiposActivo`** y la columna **`TIP_TiposActivo.SeVisita`**. Sin ella `ACT_Activos.Ubicacion` es obligatoria para todos y `RG-01` compara contra una coordenada en blanco, que **rechaza el cierre legítimo** |
| §5 — **el punto kilométrico** | La columna **`ACT_Activos.PK`**. Hoy solo existe `PR`, y operación usa los dos: un panel está «en el PR 34+500 y el PK 25+00». Son dos sistemas de referencia distintos y el modelo solo guarda uno, así que el otro se pierde o se mete a mano en `Observaciones` |
| §5 — **el equipo compuesto** | Una referencia de `ACT_Activos` a sí misma, **`ACT_Activos.ActivoPadreID`**. Un panel de mensaje variable tiene pórtico, fuentes y cámaras, y hoy cada pieza sería un activo suelto sin nada que diga de quién cuelga. Sin eso no se puede responder «qué se le hizo al panel», solo «qué se le hizo a esta fuente» |
| El Plan Maestro clasifica en cuatro clases de mantenimiento | `OT_OrdenesTrabajo.Tipo` solo admite `Preventivo` y `Correctivo`. `Admin` y `Servicio` no se pueden registrar |
| §7 — medir tiempos de respuesta y resolución de un correctivo | `OT_OrdenesTrabajo` no tiene **ninguna fecha de creación**. Faltarían `HoraAviso`, `CriticidadID` y **`CRI_Criticidad`**, más **`EVT_EventosOrden`** y **`PAU_Pausas`** para el reloj parado, que no puede ser una columna acumulada |
| §3 — el oficio decide a quién se asigna | `ROL_Roles` existe y sirve; falta **`USR_Usuarios.OficioID`** y un discriminador de clase en `ROL_Roles` que separe los cuatro perfiles de acceso de los doce oficios, o los doce no tienen dónde leerse |
| Que el equipo de un peaje herede la unidad funcional del peaje | `SED_Sedes` tiene cuatro columnas y **no sabe dónde está**: sin `UnidadFuncionalID`, sin `PR` y sin `Ubicacion`. Y `ACT_Activos` no tiene recinto ni estructura |

**Y dos cosas que el modelo ya sostiene, y que conviene no volver a construir:** la segunda visita
encadenada tiene `OT_OrdenesTrabajo.OTOrigenID`; la baja de un activo tiene `FechaBaja`, `MotivoBaja`
y las reglas `RG-16` y `RG-17`, con `RG-18` protegiendo el histórico.

## 9. Lo que operación tiene que confirmar

Nada de esto se puede resolver leyendo documentos:

1. **Las propiedades de los 355 activos**: identidad, ubicación, serie. Tenemos las cantidades
2. **¿Las unidades funcionales del Sisga se subdividen?** En otro corredor sí (2,1 · 4,2)
3. **¿El Sisga mantiene iluminación?** No está en el Plan Maestro y sí en el informe de otro corredor
4. **¿Hay SLA contractuales propios?** Los plazos conocidos son de otro contrato
5. **¿Quién puede dar el aviso de una correctiva?**
6. **¿La prueba mensual con interventoría exige firma del interventor en la aplicación?**
7. **Los cinco activos sin ubicación**: ¿entran al sistema o se llevan aparte?
8. **6.15**: ¿cerrar la orden o aprobar la ejecución es el acto de recepción?

---

*El `Manual de Usuario` describe una versión anterior del sistema y contradice varias decisiones de*
*la sección 6. No se entrega hasta reescribirse contra este documento.*
