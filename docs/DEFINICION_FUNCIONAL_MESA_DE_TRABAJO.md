# Definición funcional y mesa de trabajo — SGMC

**Proyecto:** Sistema de Gestión de Mantenimiento en Campo
**Cliente:** Concesión Transversal del Sisga S.A.S.
**Dirigido a:** Líder funcional y equipo de Operaciones / ITS
**Fecha:** 6 de agosto de 2026
**Estado:** Documento de validación. No es un informe de avance: es un cuestionario estructurado.

---

## Cómo usar este documento

Este documento no pide aprobación. Pide **decisiones**.

Está organizado en tres partes:

- **Parte I y II** describen cómo entendemos hoy que debe funcionar el sistema, expresado como
  flujos de uso verificables. Léelas para confirmar o corregir.
- **Parte III** es el cuestionario. Cada decisión llega con nuestra propuesta ya marcada `[X]`:
  si estás de acuerdo no escribes nada, y si no, marcas otra opción.
- **Parte IV** muestra cómo cada respuesta se convierte en trabajo y en fecha. El roadmap no
  existe todavía porque depende de lo que respondas aquí.

Sugerencia de mesa: dos sesiones de dos horas. La primera recorre las Partes I y II y valida los
flujos. La segunda resuelve el cuestionario decisión por decisión. Lo que no se decida queda con
el supuesto por defecto que está declarado en cada punto, y ese supuesto se vuelve vinculante.

---

## Contexto: por qué volvemos a la definición

El SGMC se planteó en julio de 2026 como un producto mínimo viable de 8 días sobre Google
AppSheet, a partir de una ERS v1.0 y un formulario de levantamiento diligenciado el 25 de julio.
Se construyó, y hoy existe una aplicación publicada con un modelo de datos de 24 tablas, 34
activos catalogados y órdenes de trabajo registradas.

En el camino el alcance mutó. El modelo pasó de 17 a 24 tablas, aparecieron dos maneras distintas
de definir los formularios de inspección, y las fotografías y firmas quedaron modeladas por
duplicado. Ninguna de esas mutaciones pasó por una validación funcional.

Una auditoría del 6 de agosto de 2026 verificó ocho bloqueantes contra el archivo real. Al
revisarlos uno a uno aparece un patrón: **la mayoría no son errores de programación, son
preguntas de negocio que nadie respondió.** No se puede configurar el filtro de seguridad sin
saber si la sede de un activo es la unidad funcional o el peaje. No se puede cerrar el
requerimiento de evidencia fotográfica sin saber cuántas fotos exige realmente una inspección.

Por eso el paso siguiente no es seguir construyendo. Es definir, validar contigo, y recién
entonces ejecutar.

---

# PARTE I — Alcance funcional propuesto

## 1. Qué hace el sistema

El SGMC reemplaza el registro en papel del mantenimiento del corredor por un registro digital
con evidencia verificable de que el trabajo se hizo, dónde se hizo y en qué estado quedó el activo.

## 2. Actores

| Actor | Dónde trabaja | Responsabilidad |
|---|---|---|
| **Técnico** | Celular, con o sin señal | Ejecuta la inspección o reparación en el activo y registra la evidencia |
| **Supervisor** | Navegador | Programa y asigna el trabajo, revisa la evidencia y aprueba |
| **Administrador** | Navegador | Mantiene usuarios, catálogos, inventario de activos y formularios de inspección |
| **Consulta** | Navegador | Lee y exporta reportes, sin modificar |

Pendiente de confirmar si **Interventoría / ANI** es un actor con acceso al sistema o un
destinatario de reportes exportados. Ver decisión D-13.

## 3. Alcance propuesto para el primer sprint productivo

**Entra:** mantenimiento preventivo programado, sobre los tipos de activo que se prioricen,
ejecutado por técnico con evidencia fotográfica, firma y validación GPS, con asignación y
aprobación por parte del supervisor, y un tablero básico de cumplimiento.

**No entra por ahora, y se confirma en la mesa:** mantenimiento correctivo iniciado desde el
campo sin OT previa, generación automática de OT por frecuencia, integración con Power BI o GLPI,
gestión de repuestos e inventario, y firma de interventoría.

Este corte es una propuesta. Las decisiones D-01, D-03 y D-09 lo redefinen.

---

# PARTE II — Flujos funcionales

Cada flujo se expresa con precondiciones, pasos, excepciones y criterios de aceptación
verificables, de modo que sirva a la vez como definición funcional y como base de las pruebas de
aceptación de usuario.

---

## CU-01 — El técnico ejecuta un mantenimiento preventivo en campo

**Actor:** Técnico
**Cubre:** RF-002 offline, RF-006 escaneo QR, RF-007 y RF-008 checklist dinámico, RF-010 fotos,
RF-012 geofencing, RF-013 firma
**Criticidad:** Máxima. Es el flujo que justifica el sistema.

**Precondiciones**
1. El técnico tiene la app instalada y sesión iniciada con su cuenta corporativa.
2. Sincronizó al menos una vez con señal, y su celular tiene los activos de su zona descargados.
3. Existe una orden de trabajo asignada a él, o el activo admite intervención directa (D-06).
4. El activo tiene su coordenada real registrada en el sistema.

**Flujo principal**

| # | Paso | Qué hace el sistema |
|---|---|---|
| 1 | El técnico abre la app al inicio de la jornada, con señal | Sincroniza y descarga solo los activos y OT de su zona |
| 2 | Se desplaza al activo, ya sin señal | Opera contra la caché local |
| 3 | Abre "Mis OT" y elige la orden, o escanea el código QR del equipo | Abre la ficha del activo |
| 4 | Presiona "Iniciar mantenimiento" | Registra hora de inicio y precarga técnico, activo y OT |
| 5 | El sistema abre el checklist | Selecciona el formulario que corresponde al tipo de activo |
| 6 | El técnico responde el checklist | Valida obligatorias, rangos numéricos y unidades |
| 7 | Toma las fotografías requeridas | Comprime a 600 px para no agotar los datos móviles |
| 8 | Registra el estado final del activo | Operativo, en mantenimiento o fuera de servicio |
| 9 | Firma | Captura la firma manuscrita |
| 10 | Presiona guardar | Captura posición y precisión GPS y valida la distancia al activo |
| 11 | Guardado local | Queda en cola de sincronización con indicador visible |
| 12 | Al recuperar señal | Sube en segundo plano sin intervención del técnico |

**Excepciones**

| Código | Situación | Comportamiento propuesto | Decisión |
|---|---|---|---|
| E-01 | El técnico está a más de 1 km de la coordenada del activo | Bloquea el guardado con mensaje en texto plano | D-02 |
| E-02 | El GPS no fija posición o su precisión es mala (túnel, cañón) | Pendiente de definir. Hoy bloquearía y el técnico perdería el trabajo | **D-04** |
| E-03 | La batería se agota o la app se cierra a mitad del formulario | Debe conservar el borrador local | D-05 |
| E-04 | El activo no puede intervenirse (acceso cerrado, riesgo, falta repuesto) | Se registra como pendiente con motivo y se marca segunda visita | **D-07** |
| E-05 | El técnico llega a un activo que no está en el inventario | Pendiente de definir | **D-08** |
| E-06 | Dos técnicos registran sobre la misma OT | Pendiente de definir | D-06 |

**Postcondición.** Existe un registro de mantenimiento con: fecha y horas, checklist respondido,
fotografías, firma, coordenada de cierre, precisión GPS y estado final del activo.

**Criterios de aceptación**
- CA-01.1 El registro se completa de principio a fin sin señal celular en ningún momento.
- CA-01.2 Al recuperar señal, el registro aparece en el backend sin acción del técnico.
- CA-01.3 Estando a más de 1 km del activo, el sistema impide guardar.
- CA-01.4 Estando junto al activo, el sistema permite guardar.
- CA-01.5 El checklist que abre corresponde al tipo del activo escaneado.
- CA-01.6 Las fotografías quedan asociadas al mantenimiento y comprimidas.
- CA-01.7 Un mantenimiento sin firma no puede cerrarse.

> **Advertencia sobre el estado actual.** Este flujo nunca se ha ejecutado completo. La tabla de
> mantenimientos está vacía. Las coordenadas de los 34 activos son todas iguales y apuntan a
> Bogotá, de modo que CA-01.3 y CA-01.4 hoy fallan ambos. Ver D-01.

---

## CU-02 — El supervisor programa y asigna una orden de trabajo

**Actor:** Supervisor | **Cubre:** RF-014

**Precondiciones.** El activo existe en el inventario y hay un técnico activo en la zona.

**Flujo principal**
1. El supervisor entra al portal web y abre Órdenes de Trabajo.
2. Crea una orden: selecciona activo, técnico responsable, fecha programada y tipo de trabajo.
3. El sistema asigna el número de orden y la deja en estado inicial.
4. Un bot envía correo al técnico con el detalle de la asignación.
5. El técnico sincroniza y la orden aparece en su celular.

**Criterios de aceptación**
- CA-02.1 El número de orden es único y se genera solo.
- CA-02.2 El técnico recibe el correo dentro de los 5 minutos siguientes.
- CA-02.3 La orden aparece en el celular del técnico asignado y no en el de otros.

**Sin resolver.** Los estados de la orden que hoy existen en los datos son Asignada, Cerrada y
Suspendida, pero no hay definición de quién puede pasar de uno a otro ni bajo qué condición. Ver
**D-06**.

---

## CU-03 — El supervisor revisa y aprueba

**Actor:** Supervisor | **Cubre:** RF-014, RF-015

1. Al sincronizar el técnico, el mantenimiento aparece en el portal.
2. El supervisor revisa checklist, fotografías, firma y coordenada de cierre.
3. Aprueba, o lo devuelve al técnico con observación.
4. Al aprobar, la orden se cierra y el indicador de cumplimiento se actualiza.

**Criterios de aceptación**
- CA-03.1 El supervisor ve la coordenada de cierre y su precisión, no solo el resultado.
- CA-03.2 Una orden no puede cerrarse sin mantenimiento aprobado.

**Sin resolver.** El modelo tiene un campo de aprobación del supervisor, pero no existe el flujo
de rechazo: qué pasa con un mantenimiento devuelto, si el técnico lo corrige sobre el mismo
registro o crea uno nuevo, y si el rechazo notifica. Ver **D-07**.

---

## CU-04 — Alerta automática por activo fuera de servicio

**Actor:** Sistema | **Cubre:** RF-016

1. El técnico cierra un mantenimiento con estado final "Fuera de servicio".
2. Al sincronizar, se dispara el bot.
3. El bot genera un informe en PDF con los datos de la falla, la ubicación y las fotografías.
4. Envía correo prioritario al CCO y al supervisor de la zona.

**Criterios de aceptación**
- CA-04.1 El correo llega dentro de los 10 minutos posteriores a la sincronización.
- CA-04.2 El PDF incluye fotografías y coordenada.
- CA-04.3 No se envían alertas por mantenimientos con estado operativo.

**Sin resolver.** A quién exactamente se notifica, si hay escalamiento cuando nadie responde, y
si un activo fuera de servicio debe generar automáticamente una orden correctiva. Ver **D-08**.

---

## CU-05 — El administrador mantiene el inventario y los formularios

**Actor:** Administrador | **Cubre:** RF-005, RF-007

1. Da de alta un activo con su código, tipo, sede, PR, calzada, sentido, coordenada real,
   frecuencia de mantenimiento y código QR.
2. Define o ajusta el formulario de inspección de un tipo de activo: secciones, preguntas, tipo
   de respuesta, obligatoriedad, rangos y si la pregunta exige fotografía.
3. Publica el cambio y los técnicos lo reciben en la siguiente sincronización.

**Criterios de aceptación**
- CA-05.1 Un activo nuevo queda disponible en el celular del técnico de su zona tras sincronizar.
- CA-05.2 Modificar una pregunta no altera las respuestas ya registradas históricamente.

**Sin resolver.** CA-05.2 hoy no se cumple: el detalle de checklist guarda el texto de la
pregunta, no su identificador, así que un cambio de redacción rompe la comparación histórica.
Ver **D-11**. Y si el administrador puede editar formularios en producción sin control de
versión. Ver **D-12**.

---

## CU-06 — Reportes y tablero

**Actor:** Supervisor, Consulta, Dirección | **Cubre:** RF-015

Este caso de uso **no está definido**. Es el vacío más grande del proyecto: el sistema captura
datos desde julio pero nadie ha especificado qué debe producir con ellos.

Lo que hoy se menciona en documentos previos, sin definición operativa:
cumplimiento de mantenimientos ejecutados contra programados, tiempo promedio de atención,
disponibilidad de activos por zona, y mapa de activos fuera de servicio.

Ninguno tiene fórmula, periodicidad, destinatario ni formato acordado. Ver **D-09 y D-10**.

---

# PARTE III — Las catorce decisiones

Cada decisión llega con nuestra propuesta ya marcada `[X]`. El líder funcional confirma no
escribiendo nada, o corrige marcando otra opción. Solo se pide redacción libre donde no cabe
una opción: nombres, fechas y listas propias.

Las cuatro marcadas como **ruta crítica** son las que fijan el cronograma.

---

## Bloque A. Datos maestros

### D-01. Coordenadas reales de los activos  **RUTA CRÍTICA**

**Qué encontramos.** Los 34 activos del inventario tienen exactamente la misma coordenada: 4.728512, -74.114531. Ese punto está en Bogotá, no en el corredor.

**Por qué importa.** Toda la promesa de evidencia verificable del sistema descansa en el control GPS, y ese control compara la posición del técnico contra esa coordenada. Con el dato actual, un técnico parado frente a un poste SOS en Machetá no podrá cerrar nunca su mantenimiento, y en cambio cualquiera ubicado en ese punto de Bogotá validaría los 34 activos. La regla está bien programada; el dato la vuelve inútil.

**Nuestra propuesta. Confirme o corrija.**

*¿De dónde tomamos las coordenadas reales?*

- `[X]` Recorrido de campo, capturando con el mismo celular que usará el técnico
- `[ ]` De un levantamiento topográfico o inventario georreferenciado que ya existe
- `[ ]` Otra fuente

*¿Los 34 activos cargados son todo el inventario?*

- `[X]` Sí, son todos los activos que gestionará el sistema
- `[ ]` No, faltan activos por cargar

- Responsable del levantamiento: `______________________________`
- Fecha comprometida: `______________________________`
- Si existe inventario georreferenciado, ¿dónde está?: `______________________________`
- Si faltan activos, ¿cuántos y de qué tipo?: `______________________________`

> Si desea matizar o agregar algo (opcional):
>

**Desbloquea:** El control GPS, el piloto de campo y los criterios de aceptación CA-01.3 y CA-01.4.

### D-02. Radio de tolerancia del control GPS

**Qué encontramos.** El radio definido es 1,0 km, heredado de la especificación original.

**Por qué importa.** Un kilómetro es mucho para un poste SOS en vía abierta, donde 100 metros bastarían para probar presencia. Y puede ser poco para un activo lineal como un tramo de fibra óptica, donde el técnico puede intervenir legítimamente a varios kilómetros del punto registrado. Un radio único para 18 tipos de activo muy distintos es una simplificación que conviene revisar.

**Nuestra propuesta. Confirme o corrija.**

*¿Qué radio aplicamos?*

- `[X]` Diferenciado: 200 m en activos puntuales (SOS, CCTV, paneles, básculas) y tratamiento aparte para fibra óptica
- `[ ]` Único de 1,0 km para todos los tipos, como está hoy
- `[ ]` Otro esquema

*¿El kilómetro viene de alguna obligación?*

- `[ ]` Sí, está en el contrato o lo exige interventoría
- `[X]` No, fue un valor elegido por el equipo y se puede cambiar

- Si es otro esquema, ¿cuál?: `______________________________`
- Si es contractual, ¿qué cláusula o documento?: `______________________________`

> Si desea matizar o agregar algo (opcional):
>

**Desbloquea:** La configuración definitiva de la regla de validación.

### D-03. Qué significa la sede de un activo  **RUTA CRÍTICA**

**Qué encontramos.** Los 11 usuarios están registrados en la sede 1, que es el CCO. Los 34 activos están repartidos entre las sedes 7 a 10, que son las unidades funcionales UF1 a UF4. La intersección es vacía.

**Por qué importa.** El filtro de seguridad descarga al celular del técnico solo los activos de su sede. Con los datos actuales, cada técnico descargaría cero activos y la aplicación quedaría vacía en sus manos el primer día de piloto. El problema de fondo es que la misma columna se usa con dos significados: para los usuarios es el sitio físico donde trabajan (CCO, peaje, báscula) y para los activos es el tramo del corredor donde están (UF1 a UF4).

**Nuestra propuesta. Confirme o corrija.**

*¿Qué activos debe descargar un técnico en su celular?*

- `[X]` Los de las unidades funcionales que tenga asignadas, y puede tener varias
- `[ ]` Los de una sola unidad funcional
- `[ ]` Todos los del corredor, sin filtro

*¿Qué debe ver un supervisor?*

- `[X]` Todo el corredor
- `[ ]` Solo su zona

*¿Un técnico del CCO puede intervenir activos de cualquier unidad funcional?*

- `[X]` Sí
- `[ ]` No

- Si aplica, ¿qué unidades funcionales atiende cada técnico?: `______________________________`

> Si desea matizar o agregar algo (opcional):
>

**Desbloquea:** El filtro de seguridad y, con él, la descarga de datos al celular. Sin esto el piloto no arranca.

---

## Bloque B. Operación en campo

### D-04. Qué hacer cuando el GPS falla

**Qué encontramos.** El sistema captura la precisión del GPS pero no define qué hacer cuando esa precisión es mala. El plan original ya señalaba el riesgo de falsos negativos y proponía un mecanismo de excepción supervisada, que nunca se especificó.

**Por qué importa.** En túnel, en cañón o bajo copa densa, el celular puede reportar una posición con error de cientos de metros o no fijar nada. Si el sistema bloquea sin salida, el técnico pierde el trabajo de una hora y el sistema pierde su confianza el primer día. Si el sistema deja pasar todo, el control no sirve para nada. Este es el punto donde el control se gana o se pierde.

**Nuestra propuesta. Confirme o corrija.**

*¿Qué hace el sistema cuando la precisión del GPS es insuficiente?*

- `[X]` Permite cerrar con excepción: exige motivo escrito y fotografía, marca el registro y avisa al supervisor
- `[ ]` Bloquea siempre: el técnico debe regresar cuando haya señal
- `[ ]` Permite cerrar solo con autorización previa por llamada al CCO

*¿A partir de qué error del GPS se activa la excepción?*

- `[X]` Cuando la precisión reportada es peor que 50 metros
- `[ ]` Otro umbral

*¿Las excepciones se reportan al supervisor?*

- `[X]` Sí, en un reporte semanal de excepciones
- `[ ]` No, basta con que queden registradas

- Si es otro umbral, ¿cuál?: `______________________________`
- ¿Qué porcentaje de excepciones consideraría un problema?: `______________________________`

> Si desea matizar o agregar algo (opcional):
>

**Desbloquea:** La excepción E-02 del flujo de campo y buena parte de la aceptación del sistema por los técnicos.

### D-05. Interrupción a mitad de formulario

**Qué encontramos.** No hay definición de qué ocurre si el técnico cierra la aplicación, se le agota la batería o lo interrumpen a mitad del checklist.

**Por qué importa.** Una inspección de poste SOS son 15 preguntas más fotografías. Perder eso por una llamada entrante es la clase de fricción que hace que un técnico vuelva al papel.

**Nuestra propuesta. Confirme o corrija.**

*¿Se conserva el trabajo a medio hacer?*

- `[X]` Sí, queda como borrador local y la inspección aparece en curso hasta cerrarse
- `[ ]` No, se descarta y el técnico reinicia

*¿Hasta cuándo puede quedar abierta una inspección?*

- `[X]` Debe cerrarse dentro de la misma jornada
- `[ ]` Puede quedar abierta de un día para otro
- `[ ]` Otro plazo

*¿Una inspección iniciada y no cerrada cuenta como incumplimiento?*

- `[ ]` Sí, cuenta como incumplida
- `[X]` No, pero se reporta aparte para seguimiento

- Si es otro plazo, ¿cuál?: `______________________________`

> Si desea matizar o agregar algo (opcional):
>

**Desbloquea:** La excepción E-03 y la definición del indicador de cumplimiento.

### D-06. Ciclo de vida de la orden de trabajo

**Qué encontramos.** Las órdenes registradas tienen estados Asignada, Cerrada y Suspendida, pero no hay regla que diga quién cambia cada estado ni bajo qué condición. Además, el único checklist existente apunta a una orden que no existe, señal de que hoy se puede registrar trabajo sin orden válida.

**Por qué importa.** Sin ciclo de vida definido no hay indicador de cumplimiento confiable: no se puede medir ejecutado contra programado si no está claro cuándo una orden cuenta como vencida, quién la suspende y si un trabajo puede existir sin orden.

**Nuestra propuesta. Confirme o corrija.**

*¿Adoptamos los siete estados de la figura 4?*

- `[X]` Sí: Programada, Asignada, En ejecución, En revisión, Cerrada, Suspendida y Vencida
- `[ ]` No, preferimos otro conjunto de estados

*¿Un técnico puede ejecutar un mantenimiento sin orden previa?*

- `[X]` Sí, lo levanta como novedad y el supervisor la convierte en orden
- `[ ]` No, siempre debe existir una orden asignada antes

*¿Cuándo se considera vencida una orden?*

- `[X]` Al día siguiente de la fecha programada
- `[ ]` Al cierre de la semana
- `[ ]` Al cierre del mes

*¿Se permite reasignar una orden a otro técnico?*

- `[X]` Sí, y queda traza de quién la reasignó
- `[ ]` No

- Si prefiere otros estados, ¿cuáles?: `______________________________`
- ¿Quién puede suspender una orden?: `______________________________`
- Motivos válidos de suspensión: `______________________________`

> Si desea matizar o agregar algo (opcional):
>

**Desbloquea:** El indicador de cumplimiento, el flujo de asignación y la excepción E-06.

### D-07. Trabajo incompleto, segunda visita y devoluciones

**Qué encontramos.** El modelo prevé marcar que se requiere una segunda visita con su motivo, y la aprobación del supervisor, pero ninguno de los dos flujos está definido.

**Por qué importa.** El caso real más común no es el mantenimiento perfecto: es el técnico que llega y no puede terminar por falta de repuesto, por lluvia o por acceso cerrado. Si el sistema no modela ese caso, el técnico va a forzar un cierre falso o no va a registrar nada.

**Nuestra propuesta. Confirme o corrija.**

*¿Qué pasa cuando el técnico no puede terminar?*

- `[X]` Cierre parcial con motivo tipificado, que genera una orden de seguimiento asociada a la original
- `[ ]` Se deja la orden abierta sin registrar nada
- `[ ]` Se suspende la orden y el supervisor decide

*Motivos de trabajo incompleto que debe ofrecer el desplegable (marque los que apliquen)*

- `[X]` Falta de repuesto o material
- `[X]` Condiciones climáticas
- `[X]` Acceso restringido o activo inaccesible
- `[X]` Riesgo para la seguridad del técnico
- `[X]` Requiere personal o equipo especializado

*Cuando el supervisor devuelve un mantenimiento, ¿qué ocurre?*

- `[X]` Se reabre el mismo registro al técnico, conservando la traza del rechazo
- `[ ]` El técnico crea un registro nuevo

*¿La devolución notifica por correo al técnico?*

- `[X]` Sí
- `[ ]` No

- Otros motivos a incluir: `______________________________`

> Si desea matizar o agregar algo (opcional):
>

**Desbloquea:** La excepción E-04, el flujo de aprobación y el cálculo real de cumplimiento.

### D-08. Activos no inventariados y correctivo desde campo

**Qué encontramos.** No hay ruta para un activo que el técnico encuentra en vía y que no está en el sistema, ni para una falla detectada fuera de programación.

**Por qué importa.** Sin esa ruta, los hallazgos de campo se pierden o se gestionan por WhatsApp, que es exactamente lo que el sistema viene a reemplazar.

**Nuestra propuesta. Confirme o corrija.**

*¿Puede el técnico reportar un activo que no está en el inventario?*

- `[X]` Sí, levanta una novedad con foto y coordenada; el supervisor decide si lo da de alta
- `[ ]` No, el inventario solo lo modifica el administrador

*Cuando un activo queda fuera de servicio, ¿qué debe pasar?*

- `[X]` El sistema genera automáticamente una orden correctiva
- `[ ]` El supervisor la crea manualmente si lo considera
- `[ ]` El correctivo se gestiona por fuera del sistema

> Si desea matizar o agregar algo (opcional):
>

**Desbloquea:** La excepción E-05 y el alcance de la alerta automática.

---

## Bloque C. Alcance de los formularios

### D-09. Cuántos tipos de activo entran al primer sprint  **RUTA CRÍTICA**

**Qué encontramos.** Hay 18 tipos de activo y 18 formularios declarados, pero solo el de postes SOS tiene sus preguntas construidas: 15 preguntas. Los otros 17 están vacíos. Además, la columna que conecta cada tipo de activo con su formulario está vacía en los 18 tipos, de modo que hoy la aplicación no sabría qué checklist abrir ni siquiera para el SOS.

**Por qué importa.** Construir los 17 bancos restantes son del orden de 250 preguntas que alguien con criterio técnico debe redactar, con sus rangos, unidades y obligatoriedad. Es la tarea más grande que queda y es trabajo del equipo de la Concesión, no de configuración. Intentar construir los 18 a la vez es lo que hará que el proyecto se estanque otro mes.

**Nuestra propuesta. Confirme o corrija.**

*¿Con qué tipos de activo arrancamos?*

- `[X]` Tres tipos: postes SOS, CCTV y paneles de mensaje variable
- `[ ]` Otros tres tipos
- `[ ]` Los 18 tipos a la vez

*¿De dónde salen las preguntas de cada checklist?*

- `[X]` Se transcriben los formatos de inspección en papel que ya se usan
- `[ ]` Se redactan desde cero con el equipo técnico

*¿Hay una exigencia contractual sobre qué debe contener una inspección?*

- `[ ]` Sí, existe un requisito de interventoría o del contrato
- `[X]` No, el contenido lo define el criterio técnico de la Concesión

- Si son otros tres tipos, ¿cuáles?: `______________________________`
- Quién redacta y valida las preguntas: `______________________________`
- Disponibilidad semanal de esa persona: `______________________________`
- Si es contractual, ¿qué documento lo exige?: `______________________________`

> Si desea matizar o agregar algo (opcional):
>

**Desbloquea:** El alcance real del primer sprint y su fecha. Es la decisión que más mueve el cronograma.

### D-10. Evidencia fotográfica y firmas

**Qué encontramos.** El requerimiento habla de hasta 6 fotografías. El modelo de datos las soporta de dos maneras a la vez, incompatibles entre sí: dos campos fijos dentro del registro de mantenimiento y una tabla separada sin límite. Lo mismo ocurre con las firmas. Las tablas separadas están vacías.

**Por qué importa.** Si no se decide, el técnico terminará firmando dos veces y adjuntando fotos en dos lugares distintos, o peor, la evidencia quedará repartida y los reportes no la encontrarán completa.

**Nuestra propuesta. Confirme o corrija.**

*¿Cuántas fotografías exige una inspección?*

- `[X]` Mínimo 3 obligatorias y hasta 6 en total
- `[ ]` Solo 2: una de inicio y una final
- `[ ]` Otra cantidad

*¿Las fotografías son tipificadas o libres?*

- `[X]` Tipificadas: antes, después y novedad
- `[ ]` Libres, el técnico decide qué fotografía

*¿Quién firma y dónde?*

- `[X]` El técnico firma en campo; el supervisor valida aprobando en el portal, sin firmar
- `[ ]` Firman ambos en campo, uno junto al otro

*¿Qué valor tiene la firma?*

- `[ ]` Contractual: es soporte frente a interventoría
- `[X]` Control interno de la Concesión

- Si es otra cantidad, ¿cuál?: `______________________________`

> Si desea matizar o agregar algo (opcional):
>

**Desbloquea:** El diseño definitivo del formulario y el cumplimiento verificable de los requerimientos de evidencia.

### D-11. Trazabilidad histórica de las respuestas

**Qué encontramos.** El detalle de las inspecciones guarda el texto de la pregunta, no su identificador. Si alguien reformula una pregunta, los registros anteriores dejan de ser comparables con los nuevos.

**Por qué importa.** Si el sistema debe mostrar la evolución de un activo en el tiempo, o demostrar ante interventoría que se aplicó el mismo criterio durante un periodo, esta trazabilidad es indispensable. Si el sistema solo debe dejar constancia de cada visita por separado, no lo es.

**Nuestra propuesta. Confirme o corrija.**

*¿Necesita comparar la misma pregunta a lo largo del tiempo para un activo?*

- `[X]` Sí, es necesario ver la evolución del activo
- `[ ]` No, basta la constancia de cada visita por separado

*¿El sistema debe poder reconstruir cómo era un formulario en una fecha pasada?*

- `[X]` Sí, se versionan los formularios al cambiarlos
- `[ ]` No hace falta

> Si desea matizar o agregar algo (opcional):
>

**Desbloquea:** La comparabilidad histórica y los reportes de evolución.

---

## Bloque D. Reportes

### D-12. Qué reportes debe entregar el sistema  **RUTA CRÍTICA**

**Qué encontramos.** Ningún reporte está definido. Se mencionan indicadores en documentos previos pero ninguno tiene fórmula, periodicidad ni destinatario.

**Por qué importa.** Este es el vacío más costoso del proyecto. Todo lo que el técnico captura en campo existe para producir algo, y ese algo nunca se especificó. Definir el reporte al final obliga casi siempre a volver atrás y capturar datos que no se pidieron. Definirlo ahora es lo que garantiza que el formulario pida lo correcto.

**Nuestra propuesta. Confirme o corrija.**

*Marque los reportes que el sistema debe entregar. Los marcados son nuestra propuesta.*

- `[X]` Cumplimiento del plan de mantenimiento — mensual, a Supervisión y Dirección
- `[X]` Activos fuera de servicio — diario, al CCO
- `[X]` Hoja de vida del activo — a demanda, a Supervisión e Interventoría
- `[X]` Certificado de mantenimiento por intervención — a Interventoría
- `[ ]` Productividad del técnico — semanal, a Supervisión
- `[X]` Excepciones de GPS — semanal, a Supervisión

*¿En qué formato deben entregarse?*

- `[X]` En pantalla, con exportación a Excel y PDF cuando se necesite enviar
- `[ ]` Solo en pantalla
- `[ ]` PDF automático por correo

*¿Alguno se entrega a un tercero con formato obligatorio?*

- `[ ]` Sí, hay un formato exigido por interventoría o la ANI
- `[X]` No, el formato lo definimos nosotros

- Otros reportes que necesite: `______________________________`
- Si hay formato obligatorio, ¿cuál y quién lo exige?: `______________________________`

> Si desea matizar o agregar algo (opcional):
>

**Desbloquea:** El tablero y los entregables, y hacia atrás, la validación de que los formularios capturan lo necesario.

### D-13. Definición de los indicadores

**Qué encontramos.** Se habla de cumplimiento, disponibilidad y tiempo de atención sin fórmula acordada.

**Por qué importa.** La disponibilidad de activos puede significar tres cosas distintas según se mida por tiempo, por cantidad o ponderada por criticidad, y cada una da un número diferente ante la misma realidad. Si ese número va a un informe de interventoría, la definición debe estar acordada antes y no después.

**Nuestra propuesta. Confirme o corrija.**

*¿Cómo se calcula el cumplimiento?*

- `[X]` Órdenes cerradas dentro de la fecha programada, sobre órdenes programadas
- `[ ]` Órdenes ejecutadas sobre programadas, sin importar la fecha

*Una orden cerrada con excepción de GPS, ¿cuenta como cumplida?*

- `[X]` Sí, pero se reporta aparte en el informe de excepciones
- `[ ]` No cuenta como cumplida

*¿Cómo se mide la disponibilidad de activos?*

- `[X]` Por tiempo: horas fuera de servicio sobre horas totales del periodo
- `[ ]` Por cantidad: activos operativos sobre activos totales
- `[ ]` Ponderada por criticidad del activo

*¿Existe una meta contractual frente a la ANI que el sistema deba reportar?*

- `[ ]` Sí, hay meta de disponibilidad o de tiempo de atención
- `[ ]` No
- `[X]` Por confirmar con el área contractual

- Si existe meta contractual, ¿cuál es y de qué documento sale?: `______________________________`

> Si desea matizar o agregar algo (opcional):
>

**Desbloquea:** El tablero de indicadores y cualquier reporte a terceros.

---

## Bloque E. Gobierno

### D-14. Usuarios, licenciamiento y gobierno del cambio

**Qué encontramos.** Hay 11 usuarios registrados, dos de ellos inactivos. El presupuesto declarado en el plan original fue de 100 USD mensuales, y la plataforma se cobra por usuario activo. No hay definición de quién puede modificar la aplicación en producción.

**Por qué importa.** El costo escala con el número de usuarios, y sin un responsable de cambios cualquiera puede alterar un formulario en producción y romper la comparabilidad de los datos.

**Nuestra propuesta. Confirme o corrija.**

*¿Interventoría o la ANI tendrán acceso al sistema?*

- `[ ]` Sí, con perfil de consulta
- `[X]` No, solo reciben reportes exportados

*¿Quién puede modificar formularios y reglas en producción?*

- `[X]` Solo el administrador, con autorización escrita del responsable funcional
- `[ ]` El administrador, sin autorización previa

*¿Cuánto tiempo se conserva la evidencia fotográfica?*

- `[X]` Cinco años
- `[ ]` Lo que dure la concesión
- `[ ]` Otro plazo

- Número de técnicos que usarán el sistema en régimen: `______________________________`
- Responsable funcional que autoriza cambios: `______________________________`
- Si es otro plazo de retención, ¿cuál?: `______________________________`

> Si desea matizar o agregar algo (opcional):
>

**Desbloquea:** El dimensionamiento de licencias y el procedimiento de control de cambios.

# PARTE IV — De las respuestas al roadmap

El roadmap no está escrito porque depende de esta mesa. Este es el mapa de dependencias: qué
habilita cada decisión.

| Decisión | Trabajo que habilita | Quién ejecuta | Bloquea |
|---|---|---|---|
| D-01 | Levantamiento y carga de coordenadas reales | Operaciones, recorrido de corredor | Todo el campo |
| D-03 | Realineación de sedes y configuración del filtro | Configuración | Descarga de datos al celular |
| D-09 | Construcción de los bancos de preguntas | Líder técnico y equipo ITS | Alcance del sprint |
| D-10 | Rediseño del formulario y limpieza de evidencia duplicada | Configuración | Diseño del formulario |
| D-12, D-13 | Construcción de reportes y tablero | Configuración | Entregables a Dirección e Interventoría |
| D-02, D-04, D-05 | Reglas de validación y excepción | Configuración | Aceptación en campo |
| D-06, D-07, D-08 | Estados, notificaciones y flujos de excepción | Configuración | Indicador de cumplimiento |
| D-11 | Versionado de formularios | Configuración | Reportes históricos |
| D-14 | Licencias y procedimiento de cambios | Dirección | Salida a producción |

**La ruta crítica son D-01 y D-09.** Ambas son trabajo de tu equipo, no de configuración, y ambas
se miden en semanas, no en días. El cronograma del proyecto lo fijan esas dos y no las demás.

Una vez cerrada la mesa, el orden de ejecución es:

1. **Definición** — esta mesa y sus respuestas.
2. **Datos** — coordenadas reales, mapeo de formularios por tipo, realineación de sedes,
   construcción de los bancos de preguntas priorizados.
3. **Configuración** — reglas de validación, filtro de seguridad, formularios, bots y reportes.
4. **Prueba controlada** — un mantenimiento completo de extremo a extremo ejecutado por una
   persona, primero con señal y luego en modo avión. El criterio de cierre es que existan
   registros reales en la base, verificados leyendo el archivo.
5. **Piloto** — los 10 celulares, solo después de que el paso 4 haya funcionado.
6. **Producción y evolución** — resto de tipos de activo, integraciones y respaldo automático.

---

# PARTE V — Acta de la mesa

| Campo | |
|---|---|
| Fecha de la sesión | |
| Participantes | |
| Decisiones cerradas | |
| Decisiones aplazadas y hasta cuándo | |
| Supuestos que quedan vinculantes | |
| Responsable de D-01 (coordenadas) y fecha comprometida | |
| Responsable de D-09 (preguntas) y fecha comprometida | |
| Próxima sesión | |

Firma del líder funcional: ______________________  Fecha: ____________

---
*Documento de validación funcional. Las decisiones aquí registradas son la base del roadmap de
implementación y del alcance contractual del sprint.*
