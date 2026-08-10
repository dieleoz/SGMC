# Manual de usuario y guía de operación — SGMC

**Sistema de Gestión de Mantenimiento en Campo**
Concesión Transversal del Sisga S.A.S. · Google AppSheet **`SISGA_-323965761-26-08-10`**

Reescrito el 2026-08-07 contra [`docs/FUNCIONAL_SGMC.md`](../docs/FUNCIONAL_SGMC.md) y verificado
sobre `scripts/modelo_objetivo.py`. **La versión anterior describía un sistema que no existe** —
incluía escáner QR, que se retiró del alcance, e indicaba editar la tabla de respuestas para cambiar
las preguntas, lo que corrompe el histórico.

**Cabecera y recuadro de estado actualizados el 2026-08-10** contra [`ESTADO.md`](../ESTADO.md), que
es el estado vigente. Ese día se fijó un punto de partida: la aplicación se reconstruyó desde cero
sobre una hoja generada del modelo, `Modelo_Datos_10082026`. **Entre el 6 y el 10 de agosto hubo
cinco aplicaciones y tres hojas.** Los nombres de las superadas están en `scripts/sistema.py`, con
el motivo de cada una; para verlos, `python scripts/sistema.py`. Si alguien le pasa un enlace que no
sea el de arriba, no es este sistema.

> ## Antes de usar este manual
>
> **El sistema está en construcción, y está menos avanzado de lo que decían las versiones anteriores
> de este manual.** Lo que sigue describe cómo se opera; buena parte todavía no está montada. Cada
> apartado afectado lo dice en su sitio, y el resumen es este:
>
> | Función | Estado |
> |---|---|
> | Órdenes, checklist, fotografías, firmas, histórico | **Solo las tablas.** Las 28 dadas de alta sobre la hoja limpia, y nada más |
> | Referencias entre tablas | **Sin poner.** Las 38 del modelo se reponen enteras: la aplicación se reconstruyó desde cero |
> | Radio de cierre por tipo de activo | **Poblado en los 27 tipos** de la hoja vigente: 0,05 km en 18, 0,1 km en 8 y 1,5 km en la fibra. **Falta cablear la regla que lo lee** |
> | Que la coordenada de cierre no se pueda mover a mano | **Pendiente.** `Editable_If = FALSE` está especificado y no puesto |
> | Que no se pueda borrar una orden ni una ejecución | **Pendiente.** Falta retirar `Deletes` en las dos tablas |
> | Que cada técnico solo descargue lo de sus zonas | **Pendiente.** Los dos filtros de seguridad —activos por unidad funcional, órdenes por técnico— están especificados y no puestos |
> | Que el técnico no pueda cerrar su propia orden | **Pendiente.** Está definido en el catálogo de estados, no impuesto como regla |
> | Coordenadas de los activos | **No son las reales.** De los **368** de la hoja vigente, 34 comparten una coordenada en Bogotá y **334** llevan coordenada propia, pero calculada sobre el trazado y no medida. **Ninguna sirve para operar** |
> | Creación automática de las órdenes del mes | **No cabe en el plan actual** |
>
> **Y aunque se cableara todo mañana, faltarían las coordenadas.** Con las de hoy, cualquier cierre
> en la vía queda fuera de rango y cualquier cierre en Bogotá queda dentro.

---

## 1. Para qué sirve

Para saber **cuánto de lo planeado se ejecutó**, y poder demostrarlo.

Hoy esa cifra se lleva a mano: alguien recoge los partes, cuenta las tareas hechas contra las
programadas y transcribe el porcentaje. Con el SGMC esa cuenta es una resta entre lo programado y
lo cerrado, y sale del sistema.

Todo lo demás —fotografías, coordenadas, firmas, histórico— existe para que esa cifra sea
**defendible ante la interventoría**, no solo cierta.

## 2. Quién usa el sistema

| Perfil | Dispositivo | Qué hace |
|---|---|---|
| **Técnico de campo** | Móvil, funciona sin cobertura | Ejecuta la orden, responde el checklist, toma fotografías, firma. **No cierra la orden** |
| **Supervisor** | Web o tableta | Programa, asigna, revisa, **cierra** y suspende |
| **Consulta / interventoría** | Web | Audita y exporta. No escribe |
| **Administrador** | Web | Usuarios, activos, catálogos y plantillas de checklist |

El Plan Maestro distingue además **doce especialidades** —técnico ITS, técnico de alturas, técnico
de fibra, técnico de peaje, ayudante, ingenieros de ITS, redes, soporte y TI, auxiliar de TI,
especialista y proveedor—. Hoy el sistema **no las usa para decidir quién puede hacer qué**: eso
está previsto y no construido.

## 3. Guía del técnico de campo

### 3.1 Primer ingreso

1. Instale la aplicación **AppSheet** desde Google Play o App Store.
2. Inicie sesión con su **cuenta corporativa**, la misma que figura en su ficha de usuario.
3. El sistema descarga a su teléfono **solo los activos y las órdenes de las unidades funcionales
   que tiene asignadas**. Si no ve un activo que espera ver, el problema está en su asignación de
   zona, no en la aplicación — ver 6.2.

> **Estado:** ese recorte todavía no está puesto. Hasta que se cablee, la aplicación descarga el
> inventario entero a todos los teléfonos.

### 3.2 El día de trabajo

```
1. Abrir "Mis órdenes"
2. Elegir la orden del día              → la orden pasa a "En ejecución"
3. Responder el checklist               → las preguntas dependen de la tarea
4. Tomar fotografías                    → cada una guarda su coordenada y su hora
5. Firmar
6. Cerrar en sitio                      → se comprueba la distancia al activo
7. La orden queda "En revisión"         → el supervisor la recibe
```

**Usted no cierra la orden.** Al terminar, la deja **En revisión** y el supervisor decide si la
acepta. Quien hace el trabajo no certifica que se hizo: es lo que da valor a la evidencia frente a
un tercero.

> **Estado:** hoy la aplicación **no impide** que un técnico ponga la orden en «Cerrada». La
> separación está definida en el catálogo de estados pero todavía no se aplica como regla.

### 3.3 Trabajo sin cobertura

Buena parte del corredor no tiene señal. La aplicación guarda **todo** —respuestas, fotografías,
firmas— en el teléfono, sin red.

- Al recuperar cobertura o conectarse al wifi del peaje o del CCO, envía lo pendiente en segundo
  plano.
- Para forzarlo, use el icono de sincronización en la esquina superior derecha.
- **No desinstale la aplicación ni borre sus datos con trabajo sin sincronizar.** No hay copia en
  ningún otro sitio hasta que suba.

### 3.4 Cierre con excepción, cuando el GPS no alcanza

En túnel, corte de montaña o bajo vegetación densa, el teléfono puede no fijar posición con
precisión suficiente.

1. Espere unos segundos a que la antena busque posición.
2. Si la precisión sigue siendo insuficiente, marque **`Cierre con excepción`**.
3. **Escriba el motivo** en `Motivo de excepción`. Es obligatorio.

La excepción **no es un rodeo: queda registrada y es auditable**. El supervisor ve cuántos cierres
con excepción tiene cada técnico y cada activo. Un activo que siempre se cierra con excepción
señala que su coordenada está mal o que el sitio no tiene cobertura satelital, y eso se corrige.

El umbral de precisión no está escondido en el código: lo ajusta el administrador en la tabla de
parámetros.

> **No use** el campo de observaciones para justificar un problema de GPS. Ese texto no se puede
> contar ni auditar. Para eso está el cierre con excepción.

### 3.5 Distancia al activo

Al cerrar se comprueba que usted esté cerca del activo. El radio **depende del tipo**: un poste SOS
o una cámara admiten decenas de metros; un tramo de fibra, que es lineal, necesita kilómetros.

Conviene saber qué prueba y qué no: **confirma que usted estaba cerca, no que estuviera
trabajando**. Lo que sí aporta valor son las fotografías, porque cada una lleva su propia
coordenada y su hora.

Los radios están puestos por familia en la hoja vigente, en `TIP_TiposActivo.RadioGeofencingKm`:

```
0,05 km   18 tipos   poste SOS, cámaras, sensores, paso seguro y equipos de TI
0,1  km    8 tipos   paneles de mensaje variable, básculas, peajes, generador y subestación
1,5  km    1 tipo    el tramo de fibra, que es lineal
```

> **Estado: el radio está en la hoja, pero la regla que lo lee todavía no está puesta.** Los 27
> tipos lo traen poblado —se comprueba sobre `BD/Modelo_Datos_PLANTILLA.xlsx`, que es el mismo
> archivo publicado como `Modelo_Datos_10082026`—, y lo que falta es cablear el cierre en la
> aplicación. **El radio no se ajusta en la tabla de parámetros:** ver 5.4.
>
> Y aunque estuviera cableado, **la coordenada del activo tampoco es la real**: ninguna de las 368
> lo es. Hasta cargarlas, la comprobación de distancia no significa nada en campo.

## 4. Guía del supervisor

### 4.1 Programar y asignar

1. Entre a **Órdenes de trabajo** desde el navegador.
2. Cree la orden indicando **activo**, **tarea**, **técnico** y **fecha programada**.
3. Al asignarla, la orden pasa a **Asignada**.

La **periodicidad no se elige aquí**: viene de la tarea. Un poste SOS tiene prueba semanal, prueba
mensual con interventoría y mantenimiento trimestral, y cada una es una tarea distinta con su propia
frecuencia y su propio checklist.

> **Estado:** las órdenes se crean **una a una o por carga en la hoja**. La generación automática
> del mes no está disponible en el plan actual del servicio, y no es cuestión de tiempo: depende de
> la decisión de licenciamiento.

### 4.2 Recibir el trabajo

Cuando el técnico termina, la orden queda **En revisión**. Usted:

- Revisa el checklist, las fotografías y la firma.
- Si está conforme, **aprueba la ejecución** y **cierra la orden**.
- Si no, deja la **observación de rechazo**.

> **Estado:** nadie le avisa de que hay trabajo por recibir. Tiene que entrar a mirar — las
> notificaciones automáticas dependen de la misma decisión de licenciamiento.
>
> **Y falta el camino de vuelta:** existe el campo de observación de rechazo, pero la orden **no
> tiene un estado de rechazo** al que volver. Está pendiente de definir.

### 4.3 Los estados de una orden

| Estado | Quién lo pone |
|---|---|
| Programada | Sistema |
| Asignada | Supervisor |
| En ejecución | Técnico |
| En revisión | Técnico |
| Cerrada | **Supervisor** |
| Suspendida | Supervisor |
| Vencida | Sistema |

## 5. Guía del administrador

### 5.1 Usuarios

Al crear un usuario diligencie nombres, correo —**exactamente el de su cuenta corporativa**—, cargo,
rol y sede, y márquelo como activo.

**El correo es lo que conecta la persona con la aplicación.** Si no coincide con la cuenta con la
que inicia sesión, el usuario entra pero no ve nada.

Después, **asígnele sus unidades funcionales** en la tabla de asignación de zona. Eso es lo que
determina qué descarga a su teléfono, no la sede.

### 5.2 Activos

Diligencie código, nombre, tipo, unidad funcional, punto de referencia, calzada, sentido, ubicación
y estado.

- **La ubicación es un solo campo de coordenada**, no dos columnas de latitud y longitud.
- **El código del activo no es su identificador interno.** Puede renombrarlo sin romper nada: las
  órdenes y el histórico apuntan al identificador, no al código.
- Para dar de baja un activo, marque la fecha y el motivo de baja y desmárquelo como activo. **No lo
  borre**: su histórico de mantenimientos tiene que seguir consultable.

### 5.3 Cambiar las preguntas de una inspección

Las preguntas viven en la estructura de plantillas:

```
Formulario  →  Sección  →  Pregunta  →  Tipo de respuesta
```

Para añadir o cambiar una pregunta, edite **la plantilla**. No hace falta tocar la configuración de
la aplicación.

> **Nunca edite la tabla de detalle del checklist para cambiar preguntas.** Esa tabla guarda las
> **respuestas ya dadas** por los técnicos. Modificarla reescribe el histórico de mantenimientos
> ejecutados. El manual anterior daba esta instrucción y era incorrecta.

### 5.4 Parámetros

El umbral de precisión de GPS se ajusta **en la tabla de parámetros**, sin abrir el editor de la
aplicación. Hoy vale **40 metros**.

**El radio de cierre no está ahí: va por tipo de activo**, en el campo `RadioGeofencingKm` de la
tabla de tipos, y está poblado en los 27 —los valores están en 3.5—. La tabla de parámetros
conserva un `RADIO_GEOFENCING_KM` de 1 km, pero es un **valor provisional histórico que la regla de
cierre no lee**. Cambiarlo ahí no cambia nada: si alguien le dice lo contrario, está describiendo
el sistema anterior.

## 6. Problemas frecuentes

| Problema | Causa | Qué hacer |
|---|---|---|
| «Fuera de rango» al cerrar | Está lejos de la coordenada registrada, **o la coordenada del activo está mal** | Acérquese. Si está junto al activo y sigue fallando, ciérrelo con excepción y avise: la coordenada hay que corregirla |
| No veo activos de otra zona | Es correcto: solo descarga los de sus unidades funcionales asignadas | El administrador revisa su asignación de zona |
| No aparece una orden que me asignaron | Falta sincronizar, o la orden no está en una de sus zonas | Sincronice. Si persiste, avise al supervisor |
| Las fotografías tardan en subir | Conexión lenta en montaña | No apague el teléfono. Suben en segundo plano |
| Cambié una pregunta y desaparecieron respuestas anteriores | Se editó la tabla de respuestas en vez de la plantilla | Ver 5.3. Avise de inmediato: hay histórico afectado |

## 7. Lo que el sistema no hace

Conviene decirlo, porque de otro modo se descubre en campo:

- **No prueba que usted estuviera trabajando**, solo que estaba cerca.
- **No avisa a nadie automáticamente** de que hay trabajo por recibir.
- **No genera las órdenes del mes solo.**
- **No protege contra quien edite la hoja de cálculo directamente.** Todas las validaciones viven en
  la aplicación; quien escriba en la hoja se las salta.

---

*Documento derivado de [`docs/FUNCIONAL_SGMC.md`](../docs/FUNCIONAL_SGMC.md), que es la fuente. Si*
*ambos discrepan, manda el funcional.*
