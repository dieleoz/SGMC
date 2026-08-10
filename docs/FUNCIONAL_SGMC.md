# SGMC — Documento funcional

Qué hace el sistema, para quién, cómo y para qué. **Este es el documento que se entrega al
funcional.** Todo lo demás —especificaciones, actas, base de conocimiento— es material de trabajo.

| | |
|---|---|
| Sistema | Gestión de Mantenimiento en Campo · Concesión Transversal del Sisga S.A.S. |
| Plataforma | Google AppSheet `SISGA` sobre Google Sheets |
| Verificado contra | `scripts/modelo_objetivo.py`, `BD/Modelo_Datos_PLANTILLA.xlsx` y `BD/Modelo_Datos_09082026_VISIBLE.xlsx` |
| Fecha | 2026-08-09 |

> **La aplicación es nueva.** `SGMC-886843353` se abandonó el 2026-08-09: su esquema había divergido
> tanto del modelo que *Regenerate* no podía converger, porque fusiona en vez de reemplazar. Se
> reconstruyó desde cero sobre la misma estructura de datos. **Nada de lo funcional cambió por eso**
> —el modelo es el mismo—, pero cualquier documento que hable de la aplicación anterior describe algo
> que ya no existe.

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

24 tipos de equipo. **355 activos contables**, más lo que no se cuenta por unidades:

```
Vía          postes SOS 54 · CCTV 26 · PMV fijos 11 · PMV móviles 19
             gálibos 8 · sensores meteo 4 · ETD 4 · pasos seguros 16
Comunicac.   switches capa 2  142 · capa 3  4 · fibra troncal 137 km
Peajes       carriles 12 · electrónica 12
Pesajes      básculas 2 · OCR 2
TI           servidores 7 · portátiles 29 · impresoras 3
```

**Y cinco cosas que no se visitan:** antivirus, licencias, certificados SSL, radios e internet. No
tienen coordenada. Todo el mecanismo de evidencia de ubicación no les aplica — ver 6.11.

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

Faltan además dos cosas para que la recepción esté completa: **no hay estado de rechazo** —existe
`ObservacionRechazo` pero la orden no tiene a dónde volver— y `FIR_Firmas.TipoFirma` **no tiene
valores declarados**: la única firma que existe es la del técnico.

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
| 6.10 | Preguntas de inspección | `FRM_Formularios` → `FRM_Secciones` → `FRM_Preguntas` | Editar `CHD_ChecklistDetalle` | `CHD` guarda **respuestas**. Editarlo para cambiar preguntas corrompe el histórico |
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

| | Estado |
|---|---|
| Modelo de datos, 28 tablas | **Existe.** 202 columnas y 20 reglas. `FASE A CERRADA` con 61 conformes sobre la hoja de producción y 60 sobre la plantilla |
| Plantillas de checklist | **Existe** — `FRM_Formularios`, `FRM_Secciones`, `FRM_Preguntas`. 18 formularios, 14 secciones |
| Banco de preguntas | **1 de 18.** Las 15 filas de `FRM_Preguntas` son todas del formulario de postes SOS |
| Catálogo de roles | **Existe** — `ROL_Roles`, con 4 filas. Faltan los doce oficios del Plan Maestro |
| Referencias entre tablas | **Puestas.** Las **38** del modelo, sobre la aplicación reconstruida, con `IsPartOf` en las cuatro que lo llevan |
| Geofencing y filtros de seguridad | **Puestos.** No probados en campo: falta la coordenada real |
| Capa de tareas `TAR_Tareas` | **En especificación**, y `ESPEC-003` está bloqueada por el arquitecto |
| Jerarquía de ubicación | **En especificación**, dentro de `ESPEC-003` |
| Correctivo con criticidad y SLA | **En especificación**, dentro de `ESPEC-003` |
| Imponer `QuienCambia` y el rechazo | **Pendiente** |
| Inventario de 355 activos | **En la plantilla como sintético.** 34 de fixture y 355 de prueba, cada uno marcado como tal en `ACT_Activos.Observaciones`. **No es el registro real** |
| Coordenadas de los activos | **No existen.** Los 34 comparten una de Bogotá y las 355 sintéticas están interpoladas sobre el corredor. Se levantan en campo |
| Vistas, acciones y slices | **No están en el modelo.** Mientras no se declaren, la interfaz no se puede generar ni auditar |
| Certificaciones múltiples, vigencias | Fase 2 |
| Almacén, SAT, flotas | Fuera de alcance |

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
