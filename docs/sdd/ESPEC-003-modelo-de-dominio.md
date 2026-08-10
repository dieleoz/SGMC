# ESPEC-003 — Modelo de dominio del SGMC

<!-- verificar_documentos: ignorar EST_Estructuras, ACT_Activos.SedeID -->
<!-- Se menciona en §12.3 solo para explicar por que el nombre elegido es
     ETR_Estructuras: el prefijo EST_ ya lo ocupa EST_Activo. -->

> # BLOQUEADA. No se aplica nada de este documento.
>
> **Bloqueada por el arquitecto el 2026-08-09, con 14 condiciones sin resolver.** El veredicto en sí
> no está versionado en el repositorio: si alguien va a levantar el bloqueo, **pídalo antes de tocar
> `scripts/modelo_objetivo.py`**. El estado vigente del proyecto está en
> [`ESTADO.md`](../../ESTADO.md).
>
> **Qué significa en la práctica.** Nada de aquí —ni las tablas nuevas de §7.1, ni las columnas de
> §7.2, ni las reglas RG-21 en adelante de §12.1— se escribe en `scripts/modelo_objetivo.py`.
> Declarar una tabla en `MODELO` sin su pestaña en el libro **hace fallar `F-02`** de
> `verificar_faseA.py`, que es el gate de datos. Está explicado en §2.4 y **sigue siendo cierto**.
>
> **No es el siguiente paso: es un documento por terminar.** Su pieza principal, `TAR_Tareas`,
> cambia cómo se generan las órdenes —un poste SOS tiene tarea semanal, mensual y trimestral, no
> una— y no se toca con el piloto a punto de arrancar.
>
> ## Lo que caducó de este documento el 2026-08-10, y lo que no
>
> **La secuencia.** La cabecera dice que esto precede a `ESPEC-002` «cerrada con su acta».
> `ESPEC-002` nunca se cerró, describía el cableado de una aplicación abandonada y **se retiró en la
> limpieza del 2026-08-10** junto con `PRUEBA-002` y las cuatro actas. No hay `ACTA-005`. La
> secuencia real es: **cablear entero** el despliegue de la aplicación vigente, probarlo con
> [`PRUEBA-003-despliegue.md`](PRUEBA-003-despliegue.md), y solo después esto. Donde el documento
> dice «Fase C, posterior al cierre de la Fase B», léase «posterior a ese cierre».
>
> **El cuerpo cita `ESPEC-002` unas quince veces.** Léase como el registro de decisiones que aquella
> especificación dejó tomadas —retirar `Adds` de `OT_OrdenesTrabajo`, la cadena de evidencia sin
> atomicidad, el aplazamiento de `RG-11`—, no como un documento consultable. Lo que sobrevive de ella
> está repartido en [`RECONSTRUCCION_EXPRESIONES.md`](RECONSTRUCCION_EXPRESIONES.md), con las 20
> expresiones sin cortar, y en [`../MANUAL_DESPLIEGUE.md`](../MANUAL_DESPLIEGUE.md), con la ficha por
> tabla. **Y una de esas citas ya no vale: el literal `1.0` del geofencing.** La hoja que la
> aplicación lee trae el radio poblado en los 27 tipos, así que se cablea la expresión por tipo.
> Corregido en §9 y en el recuadro de §12.2.
>
> **El punto de partida.** Todo lo que la sección 2 verificó salía de `BD/Modelo de Datos (11).xlsx`,
> **un archivo que ya no está en el repositorio**. La hoja de hoy se genera del modelo y es
> `BD/Modelo_Datos_PLANTILLA.xlsx`. Seis hechos del volcado de §2.2 cambiaron, y están corregidos en
> el recuadro que abre esa sección. **Ninguno tumba el argumento**; el que más muerde es que las
> claves `19` a `23` que §5.3.1 manda usar **ya están ocupadas**.
>
> **Lo que no caduca** es el plano de dominio: las secciones 3 a 6 describen la operación, no la
> plataforma, y sobreviven aunque mañana el backend no sea Google Sheets. Es la mejor descripción
> escrita de lo que el sistema tendría que representar.


Lo que el sistema tiene que representar para que la operación quepa dentro, escrito **antes** de
recortarlo a lo que AppSheet permite. Es la primera especificación del proyecto que no describe una
tarea de configuración sino un dominio.

| | |
|---|---|
| Qué toca | `scripts/modelo_objetivo.py` y, después, la estructura del Sheets |
| Qué **no** toca | El editor de AppSheet. Eso es Fase C, posterior al cierre del cableado |
| Precede | El cierre del cableado de la aplicación y su `PRUEBA-003`. Ver el bloqueo de la sección 2.4: no es una preferencia de orden, es un fallo duro |
| Alcance | Capa de tareas, jerarquía de ubicación, roles, tipos de mantenimiento, correctivo y recepción del trabajo |
| Fuera | Almacén, SAT, flotas, QR, y todo lo que `ESPEC-002` ya decidió |

---

## 1. Qué se quiere y por qué

El modelo vigente se construyó antes de ver el plan de mantenimiento de la Concesión. Asume tres
cosas que la operación desmiente:

1. **Que un tipo de activo tiene una tarea.** El cronograma contractual 2025 del Sisga da dos por
   tipo en los diez tipos que programa.
2. **Que todo activo es un punto con coordenada que se visita.** Cinco de los veinticuatro tipos no
   se visitan nunca: no tienen dónde ir.
3. **Que basta con registrar quién ejecutó.** `EOT_EstadosOrden` ya declara quién puede mover cada
   estado, y **ninguna regla lo impone**: hoy el técnico puede cerrar su propia orden.

La decisión que este modelo permite tomar y hoy no se puede: **decir si el mantenimiento programado
se cumplió**. El indicador que la operación reporta es planeadas contra ejecutadas, y hoy se teclea
a mano porque el sistema no sabe qué era lo planeado — sabe qué órdenes existen, no qué rutinas
debían existir.

### 1.1 El encuadre: dos planos, siempre los dos

> «Todo no podrá ser por las limitaciones de AppSheet, pero ya sabes qué queremos, cómo y para qué.»

Cada pieza de esta especificación se escribe dos veces:

- **Plano de dominio.** Qué se quiere, cómo funciona en la operación y para qué sirve. Se escribe
  completo **aunque AppSheet no lo permita**. Sobrevive a la plataforma: si mañana el backend es
  PostgreSQL, este plano no cambia.
- **Plano de realización.** Qué cabe hoy en AppSheet sobre Google Sheets, y **la limitación con
  nombre** cuando no cabe. Lo que no cabe **no se recorta del plano 1**: se marca
  `NO REALIZABLE HOY` en la tabla de la sección 8, con su causa y con qué haría falta.

Un requisito que no cabe hoy no es un requisito perdido. Es un requisito con fecha.

### 1.2 Procedencia de las fuentes, y qué se puede exigir con cada una

`docs/CONTEXTO_OPERACION.md` etiqueta el origen de los siete documentos de `contexto/`. **Tres son
de otros corredores.** De ellos se copia método, no obligación:

| Fuente | Corredor | Qué se le puede pedir |
|---|---|---|
| `Plan Maestro de Mantenimiento ITS_TI (1).xlsx` | **Sisga** | Requisito. Es el inventario y el reparto de personal confirmados por operación |
| `Plan de actividades … 2025 Componente ITS (3).xls` | **Sisga**, contrato 009 de 2015, supervisor JOYCO S.A.S. | Requisito. Es contra lo que mide la interventoría |
| `PLAN_MANTENIMIENTO_SISGA_2026 (1).docx` | Sisga | Requisito |
| `2-MANTENIMIENTO .pdf` (ETRA) | Neiva–Girardot | **Método, no cifra.** Su forma de medir un SLA sirve; sus horas no son las del Sisga |
| `Informe … enero 2025 v1.1.docx` | Neiva–Girardot | Método |
| `PROPUESTA - PLAN MTTO DC 2016.xlsx` (INDRA) | Doble calzada 444-005-15 | Método |

**Regla que gobierna toda la especificación:** nada procedente de las tres últimas se convierte en
requisito sin que operación lo confirme. Cuando algo sale de ellas y no se ha confirmado, aparece en
la sección 10 como **supuesto abierto**, nunca como carencia del Sisga. Por eso `CRI_Criticidad` se
crea **vacía de plazos** (sección 5.4): la estructura es método copiado; los números son del Sisga y
todavía no se conocen.

---

## 2. Contra qué se verificó

`CLAUDE.md` §2 obliga a declararlo, y el arquitecto ya bloqueó una vez esta serie por afirmar que
existía una columna `FechaCreacion` que no existe. Aquí está lo que se leyó, con qué comando y qué
devolvió.

> ## Qué de esta sección dejó de ser cierto el 2026-08-10
>
> **El archivo contra el que se verificó, `BD/Modelo de Datos (11).xlsx`, ya no está en el
> repositorio.** La hoja se genera hoy del modelo y es `BD/Modelo_Datos_PLANTILLA.xlsx`, la misma que
> está publicada. Lo que sigue se rederivó de ella y de `scripts/modelo_objetivo.py`:
>
> | Lo que dice esta sección | Lo que hay hoy |
> |---|---|
> | «Columnas: 200 · Campos retirados de MAN: 14» (§2.1) | **205 columnas · 13 campos retirados de `MAN_Mantenimientos`.** Tablas, referencias y reglas no cambiaron: 28, 38 y 20 |
> | «`TIP_TiposActivo` tiene 18 filas» (§2.2, §2.2.1, §5.3.1) | **27.** Se añadieron nueve tipos el 2026-08-09 para que cada familia del Plan Maestro tenga checklist propio. `RequiereGPS = FALSE` sigue valiendo solo en `SERVIDOR` y `NAS`, que es lo que sostiene 5.3 |
> | «`TIP_TiposActivo.RadioGeofencingKm` sigue vacío» | **Poblado en los 27**: 0,05 km en 18 tipos, 0,1 en 8 y 1,5 en la fibra |
> | «Los 34 activos comparten una coordenada» | **368 filas.** Las 34 del juego de arranque siguen compartiendo el punto de Bogotá; las otras 334 llevan coordenadas interpoladas sobre el corredor, y **ninguna de las dos clases es real** (D-01) |
> | «`UNF_UnidadesFuncionales.PRInicial` y `PRFinal` están vacías» | **Pobladas en las cuatro filas**, de `00+000` a `137+030`. Lo que sigue faltando es el PK, y el argumento de 4.2 no cambia |
> | «`MAN` 2 filas, `OT` 6, `CHD` 15…» | **Todas las transaccionales están vacías.** La hoja se entrega sin registros de prueba, así que la conversión de `OTID` a `Ref` no arrastra ninguna fila: es aún más barata que cuando se escribió esto |
> | «`FIR_Firmas.TipoFirma` no declara valores» | **Ya los declara**, y con el único valor que §7.6 propone: `Tecnico`. Esa parte de la especificación está aplicada |
>
> **Y el que sí obliga a corregir la especificación: las claves `19` a `23` que §5.3.1 manda usar
> para los cinco tipos sin coordenada están ocupadas.** El catálogo llega hoy a `27`. Ver el recuadro
> de 5.3.1.
>
> Lo que no cambió es el dominio: los conteos del Plan Maestro y del cronograma contractual de §2.5
> salen de `contexto/`, que no se ha tocado.

**Se verificó contra dos fuentes, ninguna de ellas producción:**

| Fuente | Papel |
|---|---|
| `scripts/modelo_objetivo.py` | **El modelo vigente.** Fuente única del diseño. Es lo que esta especificación modifica |
| `BD/Modelo de Datos (11).xlsx` | La hoja con la que se cerró la Fase A (`ACTA-004`). Es de donde salen los conteos y los valores |
| `contexto/*` (3 archivos del Sisga) | El dominio. Leídos directamente, no a través de los `.md` |

**No se leyó el Google Sheets de producción.** Esta especificación no afirma nada sobre el estado de
producción: declara un cambio de diseño sobre `modelo_objetivo.py`. Cuando el ejecutor vaya a
aplicarla, la comprobación contra producción es suya y es obligatoria.

### 2.1 Estado del modelo antes de tocarlo

```
$ python scripts/validar_modelo.py
Tablas: 28  |  Columnas: 200  |  Referencias: 38  |  Reglas: 20
Tablas retiradas: 5  |  Campos retirados de MAN: 14
ERRORES: ninguno
AVISOS (3) - revisar, no bloquean:
  - [V-06] PLA_PlanMantenimiento no es referenciada por nadie. Confirma que es punto de entrada
  - [V-06] LST_ValoresLista no es referenciada por nadie. Confirma que es punto de entrada
  - [V-14] OT_OrdenesTrabajo.Activo se renombra a 'ActivoID', pero 'Activo' sigue siendo una
           columna viva con otro significado.
APTO PARA DESPLEGAR
```

Las veinte reglas existentes son `RG-01` a `RG-20`, sin huecos. **Las nuevas de esta especificación
empiezan en `RG-21`.**

### 2.2 Hechos del modelo, verificados uno a uno

| Afirmación | Cómo se comprobó | Resultado |
|---|---|---|
| `OT_OrdenesTrabajo` **no tiene** ninguna fecha de creación | Volcado de `MODELO['OT_OrdenesTrabajo']` | 12 columnas: `OTID, ActivoID, TecnicoID, SupervisorID, Tipo, FechaProgramada, EstadoOrdenID, OTOrigenID, Observaciones, FechaCierre, CerradaPor, Activo`. **No hay `FechaCreacion`, ni `HoraAviso`, ni `TareaID`, ni `CriticidadID`** |
| Lo mismo en la hoja | Encabezado de `OT_OrdenesTrabajo` en el `.xlsx` | 15 columnas: las 12 más `FormularioID`, `Motivo_Cierre` e `Informe_Final`, las tres ya marcadas como retiradas. **Tampoco hay fecha de creación** |
| `TAR_Tareas` no existe | `'TAR_Tareas' in wb.sheetnames` | `False`. Tampoco existen `ETR_Estructuras`, `CRI_Criticidad`, `EVT_EventosOrden` ni `PAU_Pausas` |
| `EOT_EstadosOrden.QuienCambia` **existe y está poblada** | Volcado completo de la hoja | 6 columnas, 7 filas. Ver 2.3 |
| Ninguna regla usa `QuienCambia` | Búsqueda de `QuienCambia` en las 21 reglas de `REGLAS` | 0 apariciones. **La columna existe, está poblada y no la lee nadie** |
| `FIR_Firmas.TipoFirma` no declara valores | Volcado de la columna en `MODELO` | `{'nombre': 'TipoFirma', 'tipo': 'Enum', 'obligatoria': True, 'nota': 'Tecnico'}`. La nota dice `Tecnico`; **no hay lista declarada**. La hoja tiene 1 fila con valor `Tecnico` |
| `ROL_Roles` tiene 4 filas, no 12 | Volcado de la hoja | `2 Administrador`, `3 Supervisor`, `4 Técnico`, `5 Consulta`. Claves **numéricas** |
| `ACT_Activos` tiene `PR` y **no** `PK` | Encabezado | 17 columnas, `PR` presente, ninguna `PK` |
| `SED_Sedes` no sabe dónde está una edificación | Volcado | 4 columnas: `SedeID, Nombre, Ciudad, Activo`. 10 filas, de las cuales **UF1 a UF4 son las claves 7 a 10** |
| `UNF_UnidadesFuncionales.PRInicial` y `PRFinal` están **vacías** | Volcado de las 4 filas | Las 8 celdas en blanco |
| `TIP_TiposActivo.RequiereGPS` existe **y no está toda a `TRUE`** | Volcado de los 18 valores. Ver 2.2.1 | `FALSE` en `SERVIDOR` y `NAS`; `TRUE` en los otros 16 |
| `TIP_TiposActivo.RadioGeofencingKm` sigue vacío | Valores distintos de la columna | `{None}` en los 18 tipos |
| Los 34 activos comparten una coordenada | Valores distintos de `Ubicacion` | `{'4.728512, -74.114531'}` |
| `OT_OrdenesTrabajo.Tipo` está vacía | Valores de la columna en las 6 filas | `[None, None, None, None, None, None]` |
| Población de las transaccionales | Conteo de filas | `MAN` 2, `FOT` 3, `FIR` 1, `CHK` 1, `CHD` 15, `NOV` 1 |
| `FRE_Frecuencias` no tiene «A demanda» | Volcado de las 8 filas | `Diario 1, Semanal 7, Quincenal 15, Mensual 30, Bimensual 60, Trimestral 90, Semestral 180, Anual 365` |
| `ACT_Activos.FrecuenciaID` está poblada en las 34 | Volcado y contraste | **Round-robin exacto de 1 a 8, sin una sola excepción.** Es relleno, no periodicidad. Demostrado en 7.3 |
| `MAN_Mantenimientos` tiene **2 filas**, no 0 | Conteo | **`CLAUDE.md` §7 dice «0 filas» y está desactualizado.** `ESPEC-002` §1 ya lo había corregido a 2. Sigue siendo el momento más barato para convertir `OTID`, pero no es gratis: son 2 filas que la conversión tiene que resolver |

### 2.2.1 `TIP_TiposActivo`, los 18 tipos completos

> **Volcado histórico: el catálogo tiene hoy 27 tipos y el radio poblado en los 27.** Se deja tal
> como se leyó porque de él cuelga el argumento de 5.3, y ese argumento **no cambia**: `RequiereGPS`
> sigue valiendo `FALSE` solo en `SERVIDOR` y `NAS`. El catálogo vigente se vuelca con
> `python scripts/catalogo_tipos.py`.

El arquitecto lo pidió y tenía razón en pedirlo: **la columna `RequiereGPS` no está vacía ni está
toda a `TRUE`**, y una lectura descuidada habría construido encima una exención silenciosa.

```
TipoActivoID  Nombre        Categoria       TieneQR  RequiereGPS  FormularioID  RadioGeofencingKm
 1            SOS           ITS             TRUE     TRUE         FRM_SOS       (vacio)
 2            CCTV          ITS             TRUE     TRUE         FRM_CCTV      (vacio)
 3            PMVF          ITS             TRUE     TRUE         FRM_PMVF      (vacio)
 4            PMVM          ITS             TRUE     TRUE         FRM_PMVM      (vacio)
 5            SGM           ITS             TRUE     TRUE         FRM_SGM       (vacio)
 6            SGE           ITS             TRUE     TRUE         FRM_SGE       (vacio)
 7            SSA           ITS             TRUE     TRUE         FRM_SSA       (vacio)
 8            GENERADOR     Eléctrico       TRUE     TRUE         FRM_GENE      (vacio)
 9            BASCULA       ITS             TRUE     TRUE         FRM_BASC      (vacio)
10            FO            Comunicaciones  TRUE     TRUE         FRM_FO        (vacio)
11            VW            TI              TRUE     TRUE         FRM_VW        (vacio)
12            SWITCH        TI              TRUE     TRUE         FRM_SWIT      (vacio)
13            ROUTER        TI              TRUE     TRUE         FRM_ROUT      (vacio)
14            FIREWALL      TI              TRUE     TRUE         FRM_FIRE      (vacio)
15            UPS           Eléctrico       TRUE     TRUE         FRM_UPS       (vacio)
16            SERVIDOR      TI              TRUE     FALSE        FRM_SERV      (vacio)
17            NAS           TI              TRUE     FALSE        FRM_NAS       (vacio)
18            SUBESTACIÓN   Eléctrico       TRUE     TRUE         FRM_SUBE      (vacio)
```

**`RequiereGPS = FALSE` vale exactamente en `SERVIDOR` (16) y `NAS` (17). Y esos dos SÍ se visitan:**
son equipos físicos dentro del CCO o de un peaje, y alguien va hasta el rack a mantenerlos.

Luego **`RequiereGPS` no significa «no se visita»**, y una versión anterior de esta especificación lo
usó como si lo significara. Habría eximido del geofencing a los servidores y a los NAS **sin que
nadie lo notara**, que es la forma exacta del defecto de `RG-16`: una condición que no falla, no
avisa, y deja de proteger. Se corrige en 5.3.

**Lo que sí significa `RequiereGPS = FALSE` no está escrito en ninguna parte.** La columna no lleva
nota en `modelo_objetivo.py` y nadie la lee. La hipótesis razonable —bajo techo el GPS no es fiable—
no es una verificación. Va a la sección 10 como **A-13**, y esta especificación **no le da
significado nuevo ni la usa en ninguna regla**.

### 2.3 `EOT_EstadosOrden`, la tabla que ya sabe quién puede cambiar qué

Volcado literal de la hoja, sin normalizar (los valores van sin tilde tal como están):

```
EstadoOrdenID   Nombre          Orden  QuienCambia  EsFinal  Activo
Programada      Programada        1    Sistema      False    True
Asignada        Asignada          2    Supervisor   False    True
En ejecucion    En ejecucion      3    Tecnico      False    True
En revision     En revision       4    Tecnico      False    True
Cerrada         Cerrada           5    Supervisor   True     True
Suspendida      Suspendida        6    Supervisor   False    True
Vencida         Vencida           7    Sistema      True     True
```

Tres lecturas, y las tres importan:

1. **El diseño de la recepción del trabajo ya está escrito.** `Cerrada` la mueve el `Supervisor`,
   `En revision` la mueve el `Tecnico`. Falta la regla que lo imponga, no la decisión.
2. **No existe un estado de rechazo.** El supervisor que revisa y no aprueba no tiene a dónde
   mover la orden.
3. **Dos de los siete estados los mueve el `Sistema`**, y en el plan gratuito no hay sistema que los
   mueva: los procesos programados no se ejecutan. `Vencida` es hoy inalcanzable y `Programada`
   solo puede ponerla quien escriba en la hoja.

### 2.4 Verificado en el código: declarar una tabla nueva **rompe la Fase A**

Esto no es una opinión sobre el orden de trabajo. Es una línea de `scripts/verificar_faseA.py`:

```python
# F-02 toda columna del modelo esta o no
for tabla, d in MODELO.items():
    if tabla not in wb.sheetnames:
        falla("F-02", "%s no existe en el libro" % tabla)
        continue
```

En el momento en que `TAR_Tareas` se declare en `MODELO` sin existir como hoja, `verificar_faseA.py`
devuelve `FASE A INCOMPLETA`. Y `ESPEC-002` §1 exige, como primer paso obligatorio de la Fase B,
que ese mismo verificador diga `FASE A CERRADA`.

**Consecuencia dura: aplicar esta especificación antes de cerrar la Fase B bloquea la Fase B.** Ver
la sección 11.1.

### 2.5 El dominio, verificado contra `contexto/`, no contra los `.md`

`docs/CONTEXTO_OPERACION.md` y `docs/MODELO_EVOLUCION_FASE_2.md` ya contuvieron hechos falsos que un
gate adversarial encontró. Sus afirmaciones de dominio se volvieron a leer del archivo original.

**`contexto/Plan Maestro de Mantenimiento ITS_TI (1).xlsx`** — 1 hoja, 24 filas de datos, 11
columnas. Encabezados: `TIPO DE EQUIPO / ACTIVO, CANT., UNIDAD, ÁREA, TIPO MTTO., TAREA PRINCIPAL,
DESCRIPCIÓN DETALLADA DE LA ACTIVIDAD (PROTOCOLO TÉCNICO), PERIODICIDAD, HERRAMIENTA REQUERIDA,
PERSONAL, COSTO ANUAL (REF. 2026)`.

| Afirmación | Verificado |
|---|---|
| Doce roles en `PERSONAL` | **Sí, exactamente doce**: `Aux. TI, Ayudante, Especialista, Ing. ITS, Ing. Redes, Ing. Soporte, Ing. TI, Proveedor, Técnico Alturas, Técnico Fibra, Técnico ITS, Técnico Peaje` |
| Cuatro tipos de mantenimiento | **Sí**: `Preventivo` 19, `Admin` 3, `Correctivo` 1, `Servicio` 1. Suman 24 |
| 355 activos contables de 508 | **Sí**. Por unidad: `Und` 355, `km` 137, `Glb` 4, `Mes` 12. Total 508. La resta 508 − 355 = 153 = 137 + 4 + 12 |
| Los cinco que no se visitan | **Sí, y con una corrección**: ver el recuadro de abajo |
| «A demanda» aparece como periodicidad | **Sí**, en `Computadores (Portátiles)`, 29 unidades, tipo `Correctivo` |
| `Proveedor` son dos tareas de un tercero | **Sí**: `Impresoras (Sedes)` y `Radios y Comunicaciones` |

> **Corrección a `CONTEXTO_OPERACION.md` §2.** Ese documento agrupa los cinco que no se visitan
> bajo los tipos `Admin`, `Correctivo` y `Servicio`. **No es exacto.** Las seis filas cuya unidad no
> es `Und` son:
>
> ```
> Fibra Óptica (Troncal)               137  km    Preventivo   <- SÍ se visita
> Antivirus Kaspersky                    1  Glb   Admin
> Licencias (Autodesk/Office/Sinco)      1  Glb   Admin
> Radios y Comunicaciones                1  Glb   Preventivo   <- NO se visita, y es Preventivo
> Certificados SSL y Dominios            1  Glb   Admin
> Internet y Enlaces (ISP)              12  Mes   Servicio
> ```
>
> **`Radios y Comunicaciones` es `Preventivo` y aun así no tiene coordenada.** Y la fibra, que sí se
> recorre, tampoco es `Und`. Luego **«se visita» no se puede derivar de `TIPO MTTO.` ni de
> `UNIDAD`**: tiene que ser un atributo propio. Ese atributo ya existe y se llama
> `TIP_TiposActivo.RequiereGPS`. Es la pieza sobre la que se apoya toda la sección 4.4.

**`contexto/Plan de actividades de mantenimiento 2025 Componente ITS (3).xls`** — 6 hojas, leído con
`xlrd`. La hoja `CRONOGRAMA COMPONENTES ITS` declara en su encabezado:

```
CONTRATO CONCESIÓN   CONTRATO DE CONCESIÓN BAJO EL ESQUEMA DE APP, NUMERO 009 DEL
                     10 DE JULIO 2015 - TRANSVERSAL DEL SISGA
SUPERVISOR           JOYCO S.A.S
```

**Es un documento del Sisga, no de otro corredor**, y bajo `ACTIVIDADES DE MANTENIMIENTO RUTINARIO`
lista diez tipos, cada uno con **exactamente dos tareas**:

```
S.O.S. cantidad: 54.                            Inspección en campo   (DURACION CICLO: 1 AÑO)
                                                Ejecución Mantenimiento S.O.S
CIRCUITO CERRADO TELEVISION cantidad camaras: 26   Inspección en campo / Ejecución Mantenimiento
PANEL DE MENSAJERIA VARIABLE FIJO cantidad:11      idem
PANEL DE MENSAJERIA VARIABLE MOVIL cantidad: 19    idem
SISTEMA CONTROL DE GALIBO ELECTRONICO cantidad: 4  idem
SISTEMA DE CONTROL GALIBO MECANICO cantidad: 4     idem
SENSORES AMBIENTALES cantidad:4                    idem
ESTACION TOMA DE DATOS (ETD) cantidad:4            idem
SISTEMA CONTROL DE TRÁFICO cantidad: 2             idem
SEÑALES ORIENTATIVAS PASOS SEGUROS cantidad 16     idem
```

**Esto cambia el peso del argumento y conviene decirlo.** `CONTEXTO_OPERACION.md` §3 apoya «un tipo
tiene varias tareas» en la manta de INDRA, que es de otro corredor y por tanto solo método. **El
cronograma contractual del Sisga lo prueba por su cuenta**: dos tareas por tipo en los diez que
programa. La capa `TAR_Tareas` deja de ser una analogía y pasa a ser un requisito del corredor.

Dos hallazgos más del cruce entre los dos documentos del Sisga:

- **Las cantidades coinciden en los nueve tipos que comparten**: SOS 54, CCTV 26, PMVF 11, PMVM 19,
  gálibo electrónico 4, gálibo mecánico 4, sensores 4, ETD 4, pasos seguros 16. Es la única
  validación cruzada disponible del inventario y sale limpia.
- **El cronograma contiene un tipo que el Plan Maestro no tiene:** `SISTEMA CONTROL DE TRÁFICO,
  cantidad: 2`. No está entre los 24. Va a la sección 10 como supuesto abierto.

### 2.6 Tres hallazgos documentales, y una cosa que **no** es un hallazgo

1. **`docs/PLATAFORMA_APPSHEET_VERIFICADO.md` no existe.** Se pidió como entrada obligatoria y lo
   citan tanto `CLAUDE.md` §3 como `ESPEC-002` §4. El archivo real es
   `docs/BASE_CONOCIMIENTO_APPSHEET.md`, que es contra el que se verificó el comportamiento de la
   plataforma en esta especificación. **Ninguna de las dos citas resuelve.** No se corrige aquí: es
   una corrección de redacción sobre `CLAUDE.md`, fuera del alcance de una especificación.
2. **`CLAUDE.md` R-10 dice «las 15 tablas cuya clave es texto legible».** `CLAVE_LEGIBLE` tiene
   **10** entradas: `ASG_AsignacionZona, EOT_EstadosOrden, FAL_ModosFalla, FRM_Formularios,
   FRM_Preguntas, MOT_MotivosPendiente, OT_OrdenesTrabajo, PAR_Parametros, PLA_PlanMantenimiento,
   SEN_Sentidos`. El comentario dentro de `modelo_objetivo.py` dice «de las nueve». Los tres números
   son distintos y solo uno sale del archivo.
3. **`V-13` clava `TIP_TiposActivo.FormularioID` en el validador.** Ver 6.3: retirar esa columna
   sin tocar `COBERTURA` deja `validar_modelo.py` en error, y ese es el único gate objetivo.

**Y lo que no es un hallazgo:** `CLAUDE.md` §4 manda reportar el mojibake de los encabezados. Se
comprobó por punto de código, no por lo que pinta la consola. `ROL_Roles.Descripcion` contiene
`Configuración general del sistema` con `U+00F3` correcto, y el Plan Maestro contiene `ÁREA` con
`U+00C1` correcto. **No hay mojibake en estos archivos: el `?` era la consola de Windows.** Se deja
escrito para que nadie «arregle» un texto que está bien.

---

## 3. Dominio 1 — La capa de tareas

### 3.1 Plano de dominio

Una **tarea** es una rutina definida sobre un **tipo de activo**, no sobre un activo. «Inspección en
campo de un poste SOS» es una tarea; se le aplica a los 54 postes por igual. De la tarea cuelga todo
lo que hoy está repartido y mal colocado:

```
TIP_TiposActivo  «Poste SOS»
      │
      ├── TAR  «Inspección en campo»       periodicidad · formulario · rol requerido
      └── TAR  «Ejecución de mantenimiento» periodicidad · formulario · rol requerido
                    │
                    │  × cada activo del tipo
                    ▼
              PLA_PlanMantenimiento   (activo × tarea, con su propia próxima fecha)
                    │
                    ▼
              OT_OrdenesTrabajo       la orden dice QUÉ rutina se ejecuta
                    │
                    ▼
              MAN_Mantenimientos      la ejecución real
```

**Por qué la periodicidad no puede vivir en el activo.** Hoy `ACT_Activos.FrecuenciaID` da una sola
frecuencia por poste. El cronograma del Sisga le da al poste una inspección y una ejecución con
ciclos distintos. Con una sola columna hay que elegir cuál de las dos se pierde.

**Por qué el formulario no puede vivir en el tipo.** Hoy `TIP_TiposActivo.FormularioID` da un
checklist por tipo. Si la inspección y la ejecución del mismo poste preguntan cosas distintas —y las
preguntan—, un tipo necesita dos formularios. El formulario es de la tarea.

**Para qué sirve.** Para que el cumplimiento sea una resta y no un dato tecleado. Con la capa de
tareas, «planeadas» es una consulta sobre `PLA_PlanMantenimiento` y «ejecutadas» una consulta sobre
`OT_OrdenesTrabajo`. Hoy ese porcentaje lo escribe una persona en un Excel.

**Y resuelve el correctivo sin duplicar columnas.** `MODELO_EVOLUCION_FASE_2.md` §11 decide que el
correctivo use un formulario propio en lugar de reactivar `Diagnostico` y `Repuestos_Utilizados`.
Con la capa de tareas eso sale gratis: una tarea de tipo `Correctivo` apunta a otro `FormularioID`.

### 3.2 Plano de realización

| Pieza | ¿Cabe hoy? | Cómo, o por qué no |
|---|---|---|
| Tabla `TAR_Tareas` | **Sí** | Hoja nueva más declaración en `MODELO` |
| `PLA_PlanMantenimiento` gana `TareaID` | **Sí** | Columna nueva. `PLA.FrecuenciaID` se retira: la frecuencia es de la tarea |
| `OT_OrdenesTrabajo` gana `TareaID` | **Sí** | Columna nueva |
| Que un plan sea único por (activo, tarea) | **NO** | El Sheets no impone unicidad. Ver N-01 |
| Que la tarea pertenezca al tipo del activo | **Sí, en la app** | `RG-24`. Quien escriba en el Sheets se la salta |
| Generar el plan de los 355 activos × 2 tareas | **NO automáticamente** | Sin bots programados. Se carga por lote sobre el Sheets. Ver N-02 |
| Generar las órdenes de la semana desde el plan | **NO** | `RG-12` es un bot programado. Es la limitación que más duele aquí. Ver N-03 |

**«A demanda» no es una periodicidad: es la ausencia de una.** `FRE_Frecuencias` no la tiene y
**no debe tenerla**. Crear una fila `A demanda` con `Dias = 0` haría que `RG-11` calculase
`ProximaFecha = UltimaEjecucion`, es decir, los 29 portátiles vencidos todos los días desde su
última reparación. Por eso `TAR_Tareas.FrecuenciaID` es **opcional**, y una tarea sin frecuencia
sencillamente no genera fila de plan (`RG-25`).

**El vocabulario de periodicidades no cruza.** Verificado: el Plan Maestro usa siete valores —`A
demanda, Anual, Anual/Mes, Bimestral, Mensual, Semestral, Trimestral`— y `FRE_Frecuencias` tiene
ocho —`Diario, Semanal, Quincenal, Mensual, Bimensual, Trimestral, Semestral, Anual`—. Coinciden
cuatro. De los tres que faltan:

- `Bimestral` (cada dos meses) contra `Bimensual` (60 días). Es el mismo concepto con otro nombre.
  Se resuelve renombrando la fila 5 de `FRE_Frecuencias` a `Bimestral`, que es la palabra que usa el
  contrato. **Es un cambio de dato en la hoja, no de estructura**, y no rompe referencias porque la
  clave es `5` y no el nombre.
- `A demanda` no entra, por lo dicho arriba.
- **`Anual/Mes` no es una periodicidad: son dos tareas.** El antivirus tiene una renovación anual de
  licencia y una gestión mensual de consola. Es el argumento de la sección 3.1 apareciendo solo.

### 3.3 Efecto en volumen, y por qué duele

`MODELO_EVOLUCION_FASE_2.md` §3 estima que con dos tareas por tipo las 1.916 órdenes anuales se
acercan a 3.000-3.500, doce o catorce al día. **No se recalcula aquí**, porque la cifra cuelga de un
inventario que la propia fuente marca como no confirmado (sección 10, supuesto A-01).

Lo que sí es firme: **sin bots programados, cada una de esas órdenes se crea a mano o por lote sobre
el Sheets**, porque `ESPEC-002` retiró `Adds` de `OT_OrdenesTrabajo` y no hay generador de claves
seguro fuera de línea. Doce órdenes al día tecleadas es el punto en el que el sistema deja de
ahorrar trabajo y empieza a costarlo. Es la consecuencia práctica de `N-03` y la razón por la que
esa entrada de la tabla 8 pesa más que las otras.

---

## 4. Dominio 2 — La jerarquía de ubicación

### 4.1 Plano de dominio

Un activo no está «en una unidad funcional **o** en un peaje». Está en un peaje **que está** en una
unidad funcional. Es una cadena, y hoy el modelo la aplana:

```
Unidad Funcional (UNF)              tramo del corredor, con rango de PR y de PK
   ├── Edificación (SED)            CCO, peaje, báscula — con su PR, su PK y su coordenada
   ├── Estructura (ETR)             puente, viaducto — con su PR, su PK y su coordenada
   └── Punto de vía                 el activo directamente sobre el corredor, con su PR y su PK
```

El activo cuelga siempre de una unidad funcional, y **opcionalmente** de un recinto o de una
estructura. Un poste SOS está en el punto de vía; un servidor está dentro del peaje; una caja de
empalme de fibra puede estar sobre un viaducto.

**Lo que arregla.** El filtro de seguridad `RG-04` deja de tener un agujero: con todo colgando de la
UF, el técnico asignado a UF1 ve los postes de su tramo **y** los equipos del peaje que está en ese
tramo. Hoy eso funciona por accidente, porque el relleno de datos metió los servidores en UF4.

**Por qué hoy un servidor tiene punto de referencia vial.** Porque `PR` es la única forma que tiene
el modelo de decir dónde está algo, y a `SVR-001` hubo que ponerle `PR = 01+111`. Verificado: los 34
activos tienen `PR`, incluidos los que están dentro de un edificio.

### 4.2 PR y PK conviven, y el PK no es un lujo

| | Qué es | Para qué sirve |
|---|---|---|
| **PR** | Punto de referencia INVÍAS, marcado físicamente. **No es lineal** | Es lo que usa operación y lo que dice la señal en la vía |
| **PK** | Kilometraje lineal continuo | Aritmética y localización de fallas |

**Con PR no se puede restar.** `PR 12+400` menos `PR 10+200` no son 2,2 km, porque los PR no son
continuos. Y el PK hace falta para una cosa concreta: el OTDR devuelve «pérdida a 37 km» y ese
número solo se convierte en una orden si hay una escala lineal contra la que traducirlo.

```
37 km de fibra  ->  PK 37+000  ->  PR correspondiente  ->  caja más cercana
```

**Los dos se guardan. Ninguno se deriva del otro**, porque la conversión no es una fórmula: es una
tabla de equivalencias que hoy no existe.

### 4.3 Plano de realización

| Pieza | ¿Cabe hoy? | Cómo, o por qué no |
|---|---|---|
| `SED_Sedes` gana `UnidadFuncionalID`, `PR`, `PK`, `Ubicacion` | **Sí** | Cuatro columnas nuevas |
| Tabla `ETR_Estructuras` | **Sí** | Hoja nueva |
| `ACT_Activos` gana `RecintoID` y `EstructuraID`, ambas opcionales | **Sí** | Ver el aviso de nombre reutilizado, abajo |
| `ACT_Activos` gana `PK`; `UNF` gana `PKInicial`/`PKFinal` | **Sí** | `Decimal` |
| Sacar las filas UF1-UF4 de `SED_Sedes` | **Sí** | Son las claves 7 a 10. Los 11 usuarios están en `SedeID = 1`, así que borrarlas no deja a nadie huérfano |
| Que el recinto pertenezca a la misma UF que el activo | **Sí, en la app** | `RG-24`, misma familia de reglas |
| Filtro de seguridad que baje por la jerarquía | **Sí** | `RG-04` no cambia: sigue filtrando por `UnidadFuncionalID` del activo, que ahora es fiable |
| Tabla de equivalencias PR ↔ PK | **NO en este alcance** | No existe el dato. Ver N-04 |

> **Aviso de nombre reutilizado, y es la regla R-7 y la V-12 a la vez.**
> `ACT_Activos.SedeID` **está en `CAMPOS_RETIRADOS`** con el motivo «se sustituye por
> `UnidadFuncionalID`». Volver a declararlo en `MODELO` con el nuevo significado —«el recinto donde
> está el equipo»— **aborta la validación por V-12**, que falla si un campo está a la vez retirado y
> vivo. Y aunque no abortara, sería el defecto exacto que R-7 describe: dos columnas con el mismo
> nombre y significados distintos.
>
> **Por eso la columna se llama `RecintoID`**, no `SedeID`, y necesita `alias_justificado` porque la
> clave de `SED_Sedes` es `SedeID` y V-05 exige que una referencia se llame como su destino.

**La sede de Bogotá.** Está fuera del corredor y aloja 29 portátiles y 3 impresoras. `SED_Sedes`
gana `UnidadFuncionalID` **opcional** por esto: una sede administrativa no está en ningún tramo.
La alternativa —inventar una UF administrativa— mete una fila falsa en el catálogo contra el que
mide la interventoría. Queda como supuesto abierto A-04.

---

## 5. Dominio 3 — Roles, oficios y los tipos que no se visitan

### 5.1 Plano de dominio: dos cosas distintas que se llaman igual

Hay **dos** conceptos y el modelo solo tiene nombre para uno:

- **Perfil de acceso** — qué puede hacer una persona en la aplicación. Son cuatro y están en
  `ROL_Roles`: Administrador, Supervisor, Técnico, Consulta.
- **Oficio** — qué sabe hacer una persona en campo. Son doce y están en la columna `PERSONAL` del
  Plan Maestro: Técnico ITS, Técnico Alturas, Técnico Fibra, Técnico Peaje, Ayudante, Ing. ITS,
  Ing. Redes, Ing. Soporte, Ing. TI, Aux. TI, Especialista, Proveedor.

No son la misma lista ni sirven para lo mismo. El perfil decide qué botones ve; el oficio decide a
quién se le puede asignar la tarea. Un Ing. Redes y un Técnico Alturas tienen los dos el perfil
`Técnico`.

**Y `Proveedor` no es ninguno de los dos.** Verificado: son dos tareas —`Impresoras (Sedes)` en
renting y `Radios y Comunicaciones`— que ejecuta un tercero **que no es usuario de la aplicación**.
Se conserva como oficio para que la tarea pueda decir quién la hace, pero ningún usuario lo lleva.

### 5.2 Plano de realización

Se pidió que los doce vivan en `ROL_Roles`, y ahí van — con un discriminador, porque meter doce
oficios junto a cuatro perfiles sin distinguirlos deja `USR_Usuarios.RolID`, que es **obligatoria**,
pudiendo apuntar a «Técnico Fibra» y cambiando en silencio lo que significa el perfil de acceso.

| Pieza | Cómo |
|---|---|
| `ROL_Roles` gana `Clase` | `Enum`: `Acceso`, `Oficio`. Las 4 filas existentes quedan `Acceso` |
| Los 12 oficios | 12 filas nuevas, `Clase = Oficio` |
| **Claves de los 12** | **Numéricas, 6 a 17**, continuando la serie `2..5` que ya existe |
| `USR_Usuarios.RolID` | `Valid_If` que restringe el desplegable a `Clase = Acceso` (`RG-21`) |
| `TAR_Tareas.RolRequeridoID` | `Ref` a `ROL_Roles`, con `alias_justificado`. Se espera `Clase = Oficio` |

**Por qué claves numéricas y no `ROL-06`.** Dos razones del archivo, no de gusto:

1. `ROL_Roles` **no está** en `CLAVE_LEGIBLE`, y su clave en la hoja es numérica. La comprobación
   `F-11` de `verificar_faseA.py` decide con `_clave_es_legible()`, que exige que **todas** las
   claves sean texto no numérico. Mezclar `2.0` con `ROL-06` da «no legible» igualmente, así que la
   clave mixta no compra nada y ensucia la tabla.
2. Al no ser legible, **`V-17` sigue vigilando**: `[RolRequeridoID] = "Técnico Fibra"` es un error
   que el validador caza, y hay que escribir `[RolRequeridoID].[Nombre]`. Es exactamente la
   protección que hizo falta en `RG-16`. Una clave legible aquí apagaría esa vigilancia sin
   necesidad.

**Lo múltiple sigue en Fase 2**, por decisión de operación del 2026-08-07: que alguien tenga alturas
*y* electricista, que una tarea exija técnico *más* SISO, y las vigencias de certificado. Eso es una
relación de muchos a muchos con fecha de caducidad, y no es esto.

### 5.3 Los cuatro tipos de mantenimiento y los cinco que no se visitan

**Plano de dominio.** El Plan Maestro clasifica las 24 tareas en cuatro tipos, verificados:
`Preventivo` 19, `Admin` 3, `Correctivo` 1, `Servicio` 1. `OT_OrdenesTrabajo.Tipo` hoy solo admite
`Preventivo` y `Correctivo`, así que dos de los cuatro no se pueden ni registrar.

Y cinco tipos de equipo **no son cosas que se visiten**: antivirus, licencias, certificados SSL,
internet ISP y radios. Renovar un certificado es una fecha en un portal; auditar licencias es una
revisión en un navegador; monitorear el SLA del ISP es leer un NMS. **Ninguno tiene coordenada.**

Todo el diseño de prueba de presencia —`RG-01` geofencing, `RG-02` precisión, `RG-19` excepción,
`RG-20` sellado de la captura— asume desplazamiento. **Para esos cinco no aplica, y hay que decidir
qué camino tienen.** Aquí se decide: **tienen orden, ejecución, checklist y firma, y no tienen
cadena de evidencia de ubicación.**

Se elige eso y no sacarlos del alcance por una razón de dominio: son 5 de los 24 tipos del plan
contra el que mide la interventoría. Un sistema que no puede decir si el certificado SSL se renovó
deja fuera del cumplimiento una parte del contrato.

**Plano de realización, y aquí hubo que corregir.** La primera versión de esta especificación
reutilizaba `TIP_TiposActivo.RequiereGPS` para marcar los cinco. **Era un error**, y el volcado de
2.2.1 lo demuestra: esa columna vale `FALSE` en `SERVIDOR` y `NAS`, que **sí se visitan**. El `OR`
sobre `RG-01` habría eximido del geofencing a los servidores y los NAS sin decírselo a nadie.

**Son dos conceptos y llevan dos columnas:**

| Columna | Significa | Estado |
|---|---|---|
| `TIP_TiposActivo.SeVisita` | **Hay un lugar físico al que ir.** `FALSE` = el trabajo se hace desde un navegador o una consola | **Nueva.** Inicial `TRUE`; `FALSE` en los cinco |
| `TIP_TiposActivo.RequiereGPS` | Sin definición escrita. Hoy `FALSE` en `SERVIDOR` y `NAS` | **Existe. No se toca, no se lee y no se le da significado nuevo.** Supuesto A-13 |

| Pieza | Cómo |
|---|---|
| Marcar los tipos sin lugar al que ir | `TIP_TiposActivo.SeVisita = FALSE` en los cinco |
| Que `ACT_Activos.Ubicacion_LatLong` deje de ser obligatoria para ellos | `RG-22`: `Required_If = [TipoActivoID].[SeVisita] = TRUE` |
| Que el geofencing no los rechace | **`RG-01` se modifica**, con `[...].[SeVisita] = FALSE` en el `OR`. Ver 12.2 |
| Los servidores y los NAS | **Siguen con geofencing.** Su problema es de precisión bajo techo, y para eso ya están `RadioGeofencingKm` por tipo y `RG-19`, que marca el cierre como excepcional cuando el error del satélite se dispara. No se les exime |

> **Sin la modificación de `RG-01` esto falla de la peor manera posible.** `DISTANCE()` contra una
> `Ubicacion` en blanco no da error: da un valor que **rechaza el cierre legítimo**. Es el mismo modo
> de fallo que `ESPEC-002` §7 describe para el radio vacío, donde `P-08` y `P-09` fallarían las dos
> y la tanda dejaría de discriminar. Marcar `SeVisita = FALSE` sin tocar `RG-01` deja los cinco
> tipos con órdenes que nadie puede cerrar.

**Lo que se pierde, dicho claro.** Para esos cinco tipos la garantía del sistema baja de «esta
persona estuvo frente al equipo» a «esta persona declaró haberlo hecho, con hora de servidor y
firma». Es menos, y es honesto: no hay equipo frente al que estar.

#### 5.3.1 Los cinco tipos **no existen como filas**, y sin ellas esta sección no se puede aplicar

`TIP_TiposActivo` tenía 18 filas y el Plan Maestro tiene 24 tipos. **No son el mismo conjunto ni uno
contiene al otro**, y ninguno de los cinco sin coordenada está en la hoja. El cruce que se hizo
entonces era este:

| | Cuántos | Cuáles |
|---|---|---|
| Tipos del Plan con fila en `TIP` | **10** | SOS, CCTV, PMVF, PMVM, Gálibos electrónicos (SGE), Gálibos mecánicos (SGM), Sensores ambientales (SSA), Fibra (FO), Servidores, Básculas |
| Tipos del Plan que comparten una sola fila | **2 → 1** | `Switch Capa 3` y `Switch Capa 2` caen los dos en `SWITCH` (12). El Plan los separa; `TIP` no |
| Tipos del Plan **sin fila** en `TIP` | **12** | ETD, Pasos Seguros, Peaje-Carriles, Peaje-Electrónica, OCR de pesaje, **Antivirus, Licencias, Radios, SSL, ISP**, Computadores, Impresoras |
| Filas de `TIP` **sin tipo** en el Plan | **7** | GENERADOR, VW, ROUTER, FIREWALL, UPS, NAS, SUBESTACIÓN |

> ## Corrección del 2026-08-10: siete de esas doce ya tienen fila, y las claves 19 a 23 están tomadas
>
> El 2026-08-09 el catálogo pasó de 18 a 27 tipos, para que **cada familia del Plan Maestro tenga
> checklist propio**: hasta entonces la impresora heredaba el del NAS y el portátil el del servidor,
> y eran 78 activos de 355 con el checklist equivocado. El reparto vive en
> `scripts/catalogo_tipos.py`, que es la fuente única y lo comprueba con `comprobar()`.
>
> **Los nueve tipos añadidos ocupan las claves `19` a `27`**: báscula dinámica, carril de peaje,
> electrónica de peaje, estación de toma de datos, paso seguro, switch de capa 3, computador
> portátil, impresora y cámara OCR de pesaje. Cargar los cinco de la tabla de abajo con las claves
> `19` a `23` **pisaría cinco tipos vivos**, y como `ACT_Activos.TipoActivoID` guarda esos números,
> el efecto sería el de siempre: la referencia sigue resolviendo y apunta a otra cosa.
>
> **El cruce corregido, derivado de `scripts/catalogo_tipos.py`:**
>
> | | Cuántos | Cuáles |
> |---|---|---|
> | Tipos del Plan con fila propia en `TIP` | **19** | Las 18 familias que se cuentan por unidades, cada una con su tipo y su formulario, más la fibra |
> | Tipos del Plan **sin fila** | **5** | **Antivirus, Licencias, SSL, ISP y Radios.** Son exactamente los cinco que no se visitan |
> | Filas de `TIP` **sin tipo** en el Plan | **8** | GENERADOR, BASCULA, VW, ROUTER, FIREWALL, UPS, NAS, SUBESTACIÓN |
>
> **Las claves de las cinco filas nuevas pasan a ser `28` a `32`**, continuando la serie. Todo lo
> demás de esta subsección —que hacen falta cinco filas, que la clave es numérica y no `TIP-28`, y
> que no se pueden cargar sin formulario que apuntar— **sigue valiendo igual**.
>
> Y el 12 → 5 no cierra A-14: **las 8 filas sin tipo del Plan siguen ahí**, y ahora son una más,
> porque `BASCULA` y `BASCULA DINAMICA` son dos tipos distintos desde que la familia contable tiene
> el suyo.

**Para que 5.3 sea aplicable hacen falta cinco filas nuevas en `TIP_TiposActivo`**, con claves que
continúan la serie numérica que la hoja ya usa —no `TIP-28`, que rompería `F-11` mezclando
formatos de clave—:

| Clave | Nombre | Categoria | SeVisita | RequiereGPS | TieneQR | FormularioID |
|---|---|---|---|---|---|---|
| `28` | `ANTIVIRUS` | `TI` | `FALSE` | `FALSE` | `FALSE` | pendiente |
| `29` | `LICENCIAS` | `TI` | `FALSE` | `FALSE` | `FALSE` | pendiente |
| `30` | `SSL` | `TI` | `FALSE` | `FALSE` | `FALSE` | pendiente |
| `31` | `ISP` | `Comunicaciones` | `FALSE` | `FALSE` | `FALSE` | pendiente |
| `32` | `RADIOS` | `Comunicaciones` | `FALSE` | `FALSE` | `FALSE` | pendiente |

`FormularioID` queda pendiente porque el formulario pasa a ser de la tarea (3.1), y las tareas de
estos cinco no existen todavía. **Mientras `TIP_TiposActivo.FormularioID` siga viva —y sigue, hasta
la Fase C por 7.4— es `obligatoria`, así que estas cinco filas no se pueden cargar sin un formulario
que apuntar.** Es una dependencia real y ordena el trabajo: primero `TAR_Tareas` y sus formularios,
después estas cinco filas.

**Y hay una segunda dependencia, que no existía cuando se escribió esto:** las cinco filas nuevas se
cargan editando `scripts/catalogo_tipos.py`, no la hoja. La hoja se genera de ahí con
`scripts/generar_plantilla.py`, y `comprobar()` falla si un tipo se queda sin radio de geofencing.
Para un tipo que no se visita **el radio no significa nada**, así que o `comprobar()` aprende a
eximir a los que llevan `SeVisita = FALSE`, o hay que darles un valor que nadie lee. Eso se decide al
aplicar, y se decide en el script.

**La otra diferencia no se resuelve aquí.** Las 8 filas de `TIP` sin tipo del Plan son una
reconciliación de inventario que necesita a operación, no una decisión de modelo: hay que saber si
`VW`, `ROUTER` o `SUBESTACIÓN` se mantienen y nadie los puso en el Plan Maestro, o si son parte de
otro contrato. Va como **A-14**, y es hermana de A-01.

### 5.4 El oficio necesita dónde leerse, o los doce no compran nada

`USR_Usuarios` tiene hoy `UsuarioID, Nombres, Correo, Cargo, Iniciales, RolID, SedeID, Telefono,
FechaIngreso, Activo`. **Ninguna columna dice qué oficio tiene la persona.**

Así que cargar los doce oficios en `ROL_Roles` y colgarlos de `TAR_Tareas.RolRequeridoID` deja la
mitad de una frase: el sistema sabría que «inspección de fibra la hace un Técnico Fibra» y **no
sabría quién es Técnico Fibra**. Doce filas de catálogo sin un solo consumidor, que es alcance que
crece sin uso — y la instrucción vigente de operación es que funcione primero.

**Se cierra el circuito con una columna: `USR_Usuarios.OficioID`**, `Ref` a `ROL_Roles`, opcional,
con `alias_justificado` porque la clave destino es `RolID`. Con ella:

```
TAR_Tareas.RolRequeridoID  ──┐
                             ├── ¿coinciden?  ->  el supervisor lo ve al asignar
USR_Usuarios.OficioID      ──┘
```

**Y se queda en comprobación de vista, no en regla que bloquea.** Un `Valid_If` sobre
`OT_OrdenesTrabajo.TecnicoID` que exigiera la coincidencia impediría asignar órdenes en cuanto un
usuario tuviera el oficio vacío —y los once lo tienen vacío hoy, porque la columna no existe—. El
sistema quedaría sin poder asignar nada. Se declara como **deuda** y se resuelve cuando los once
usuarios tengan oficio.

Lo que sí es regla es `RG-33`: `OficioID` solo admite filas con `Clase = Oficio`, igual que `RG-21`
restringe `RolID` a `Clase = Acceso`. Sin las dos, el discriminador de 5.2 es decorativo.

**Alternativa considerada y descartada:** no cargar los doce oficios en esta especificación y dejar
`TAR_Tareas.RolRequeridoID` vacío. Se descarta porque el dato ya existe —está en la columna
`PERSONAL` del Plan Maestro, verificado— y porque `TAR_Tareas` sin rol requerido no puede decir
quién debe ejecutar la tarea, que es la mitad de para qué existe la capa.

---

## 6. Dominio 4 — El correctivo y la recepción del trabajo

### 6.1 Plano de dominio: tres relojes, y el modelo no tiene ninguno

Verificado en 2.2: `OT_OrdenesTrabajo` tiene `FechaProgramada` y `FechaCierre`, y **ninguna fecha de
creación**. Su resta no es una duración: es adherencia al cronograma, si se cerró antes o después de
lo previsto. Para una preventiva basta. **Para una correctiva no existe el dato de partida**, porque
una avería no se programa: ocurre.

Lo que un contrato de mantenimiento mide es esto, y hoy no es derivable:

- **Tiempo de respuesta** — desde el aviso hasta que **empiezan** los trabajos.
- **Tiempo de resolución** — desde el aviso hasta que está resuelta **y el cliente informado**.
- **Reloj parado** — el tiempo bloqueado por terceros o fuerza mayor **no cuenta**.

Sin el tercero, cualquier espera de repuesto se lee como incumplimiento, y el indicador deja de
medir al equipo de mantenimiento para medir al proveedor.

La **criticidad** no es opinión: se define por porcentaje de instalación en avería, y de ahí salen
los plazos. La forma se copia de ETRA; **los números no**, porque son de Neiva–Girardot (supuesto
abierto A-05).

El **escalado** N1 → N2 → N3 existe porque una orden que el técnico no resuelve tiene que poder ir a
algún sitio: N1 técnico en campo, N2 especialista, N3 taller o fabricante.

**La recepción del trabajo.** Un trabajo lo recibe quien lo encargó, no quien lo hizo. El diseño ya
está escrito en `EOT_EstadosOrden.QuienCambia` (volcado en 2.3) y **ninguna regla lo impone**. Hoy,
con `Updates` habilitado y el filtro de seguridad `RG-05` mostrándole sus propias órdenes, **el
técnico puede poner su orden en `Cerrada`**. La evidencia entera —geofencing, fotografías con
coordenada, firma— defiende que estuvo allí, y después él mismo se aprueba el trabajo.

Y falta el otro lado: **el supervisor que revisa y no aprueba no tiene estado al que mover la
orden.** `MAN_Mantenimientos.ObservacionRechazo` existe en las 36 columnas de la hoja y nada la
escribe, porque no hay devolución que la provoque.

### 6.2 El patrón que resuelve los tres relojes: eventos, no contadores

**Esto no es preferencia de diseño: es la restricción de la plataforma.**

`BASE_CONOCIMIENTO_APPSHEET.md` lo dice sin rodeos: offline-first, consistencia eventual, sin
transacciones. **Todo contador o acumulado compite consigo mismo.** Es literalmente la razón por la
que `OT_OrdenesTrabajo` perdió `Adds` en `ESPEC-002`. Dos pausas registradas sin señal producen una
pérdida de actualización silenciosa.

Y `RG-20` enseñó la segunda mitad: un `Initial value` **es editable**, y `NOW()` en offline es el
reloj del teléfono. Ninguna de las tres formas obvias de sellar `HoraInicioTrabajos` sirve:

| Forma | Por qué no |
|---|---|
| `Initial value = NOW()` | Editable. El técnico la cambia |
| `DateTime` que teclea el operador | Nada impide rellenarla al cerrar en vez de al empezar |
| `NOW()` en el dispositivo | Reloj del teléfono, no del servidor |

Y hay una cuarta que también falla, y es la que parece buena: **una columna `ChangeTimestamp` no
sirve para «cuándo empezó», porque se reescribe.** Si la orden va `En ejecucion` → `Devuelta` →
`En ejecucion`, la marca se mueve al segundo intento y el tiempo de respuesta se acorta solo.

**Un patrón resuelve los tres: tablas hijas de la orden, y el agregado derivado por consulta en vez
de almacenado.** Son **dos tablas distintas y no intercambiables**, y conviene decirlo porque ya se
confundieron una vez: una registra **transiciones de estado**, la otra registra **bloqueos**.

```
OT_OrdenesTrabajo
   ├── EVT_EventosOrden   una fila por TRANSICIÓN DE ESTADO. Solo se añade
   │        EventoID · EstadoOrdenID · UsuarioID · FechaHora · Observacion
   │
   └── PAU_Pausas         una fila por BLOQUEO. Se añade al pausar, se cierra al reanudar
            PausaID · Inicio · Fin · MotivoPendienteID · MinutosPausa

HoraAviso            = la fila EVT más antigua de la orden
HoraInicioTrabajos   = la fila EVT más antigua con EstadoOrdenID = 'En ejecucion'
Motivo de devolución = EVT.Observacion de la fila con EstadoOrdenID = 'Devuelta'
Reloj parado         = SUM(PAU_Pausas[MinutosPausa]) de esa orden
Tiempo de respuesta  = HoraInicioTrabajos − HoraAviso − reloj parado del tramo
```

**`EVT_EventosOrden` sí es solo-añadir.** Una transición nunca se corrige: si el estado estaba mal,
se hace otra transición. Dos dispositivos sin señal no se pisan porque cada uno añade su fila.

> **`PAU_Pausas` NO es solo-añadir, y decir lo contrario sería falso.** Una versión anterior de esta
> sección lo afirmaba. Con `Inicio` y `Fin` en la misma fila, **reanudar es un `UPDATE`**, no un
> `INSERT`.
>
> Se consideró la alternativa fiel al patrón —dos filas de evento, `Pausa` y `Reanudacion`, emparejadas
> por consulta— y **se descarta**: emparejar eventos consecutivos exige una consulta ordenada por
> tiempo con correlación entre filas, y el lenguaje de expresiones de AppSheet no la tiene. Se
> obtendría pureza sobre el papel y ningún total calculable.
>
> **Se adopta la fila editable**, con la regla `RG-32` que impide abrir una pausa si ya hay otra
> abierta en la misma orden, y **con el fallo residual declarado**: si un técnico pausa en un
> dispositivo y otro reanuda en un segundo dispositivo antes de sincronizar, `RG-32` no ve la fila
> ajena, queda una segunda pausa abierta, `MinutosPausa` no se calcula y **`SUM()` la ignora**. El
> reloj parado sale **por debajo** del real, que es el lado que perjudica a quien ejecuta el
> mantenimiento y favorece a quien lo mide. Es `N-14`, y no se puede cerrar en esta plataforma.

**El motivo de la pausa reutiliza un catálogo que ya existe y está poblado.** `MOT_MotivosPendiente`
tiene las cinco filas verificadas —`Falta de repuesto, Clima, Acceso restringido, Riesgo para el
tecnico, Requiere especialista`— que son exactamente las causas de reloj parado. No hace falta
catálogo nuevo.

**Y el motivo de la devolución tiene un solo sitio: `EVT_EventosOrden.Observacion`.** Ver 6.4.

### 6.3 Plano de realización

| Pieza | ¿Cabe hoy? | Cómo, o por qué no |
|---|---|---|
| `CRI_Criticidad` como catálogo | **Sí**, y **vacía de plazos** | Los números son de otro corredor. La tabla existe para que sean dato y no expresión |
| `OT` gana `CriticidadID`, `HoraAviso`, `CanalAviso`, `NivelAtencion` | **Sí** | Columnas nuevas |
| `EVT_EventosOrden` como tabla | **Sí** | Hoja nueva. Solo-añadir de verdad |
| `PAU_Pausas` con su total por `SUM()` | **Sí, con matiz** | El usuario añade la fila al pausar y la **edita** al reanudar. No es solo-añadir: ver el recuadro de 6.2 y `N-14` |
| `MinutosRelojParado` como **columna virtual** de la orden | **Sí** | **No puede ser `App formula` sobre columna real.** Ver el recuadro de abajo |
| Que `EVT` se escriba **sola** en cada transición | **Supuesto no verificado** | Ver el recuadro. Si falla, ver N-05 |
| Que `HoraInicioTrabajos` sea infalsificable | **NO del todo** | Quien escriba en el Sheets edita la fila de evento. Ver N-06 |
| `Devuelta` como estado de rechazo | **Sí** | Fila nueva en `EOT_EstadosOrden` |
| Que el técnico no cierre su propia orden | **Sí, en la app** | `RG-23` y `RG-24`. Ver el segundo recuadro |
| `Vencida` y `Programada`, que mueve el `Sistema` | **NO** | No hay bot. Ver N-07 |
| Crear una correctiva desde la aplicación | **NO** | `ESPEC-002` retiró `Adds` de `OT`. Ver N-08 |
| Aviso automático al supervisor | **NO** | Bot por evento, plan de pago. Ver N-09 |

> **`MinutosRelojParado` va como columna VIRTUAL, no como `App formula` sobre una columna real.**
>
> Es la corrección que impide que el reloj parado vuelva a ser el acumulado del que huye 6.2.
> `BASE_CONOCIMIENTO_APPSHEET.md` punto 2 lo dice con cita: una `App formula` se recalcula «cuando se
> abre un formulario **o cuando la fila se modifica por otro mecanismo**». **Añadir una pausa modifica
> la fila de `PAU_Pausas`, no la de `OT_OrdenesTrabajo`.** Una `App formula` en la orden no se
> dispararía, el `SUM()` quedaría con el valor del último guardado de la orden, y el total sería un
> acumulado obsoleto escrito en la hoja: exactamente el defecto que se quería evitar, con la agravante
> de que una `App formula` **escribe**.
>
> Una columna virtual se recalcula en cada sincronización y **no se guarda en la hoja**, así que no
> hay nada que pueda quedar desfasado.
>
> **Y por eso no se declara en `MODELO`.** `F-02` de `verificar_faseA.py` exige que toda columna del
> modelo exista en la hoja, y una virtual no existe. Se declara solo como regla `RG-29`, con
> `columna = "(tabla)"`, que es lo que `V-10` admite.
>
> La expresión es `SUM([Related PAU_Pausas][MinutosPausa])` y **no** la forma con `SELECT(...)` y
> `[_THISROW]`: ver el aviso sobre `V-11` en 12.1.

> **Cuatro cosas que NO están verificadas contra la documentación de Google, y hay que verificarlas
> antes de configurar nada.** Se declaran, no se afirman, y se añaden a la tabla del final de
> `BASE_CONOCIMIENTO_APPSHEET.md`:
>
> 1. **Que una acción agrupada pueda añadir una fila a otra tabla** en el plan gratuito, que es como
>    `EVT_EventosOrden` se escribiría sola al pulsar «Iniciar trabajos». Una acción disparada por el
>    usuario no es un bot, pero eso es inferencia, no cita.
> 2. **Que un `ChangeTimestamp` se pueda acotar a los cambios de una columna concreta.** Se ha visto
>    la opción; no se ha encontrado la página que la documente.
> 3. **Que la aritmética de `DateTime` a minutos exista tal como se supone.** El modelo **no tiene
>    tipo `Duration`** —`TIPOS` en `modelo_objetivo.py` no lo incluye—, así que `MinutosPausa` va
>    como `Decimal` calculada. Si la conversión no es directa, hay que añadir `Duration` a `TIPOS`,
>    y eso es un cambio del validador.
> 4. **Que un `ChangeTimestamp` sea la hora del SERVIDOR y no la del dispositivo.** Comprobado con
>    `grep ChangeTimestamp docs/BASE_CONOCIMIENTO_APPSHEET.md`: **cero apariciones.** No hay ni una
>    cita oficial en toda la base de conocimiento. Y de esto cuelga todo: `RG-31`, `HoraAviso`,
>    `HoraInicioTrabajos`, `EVT.FechaHora`, y también `FOT_Fotografias.FechaHora` y
>    `MAN_Mantenimientos.FechaHoraRegistro`, **que ya están en el modelo desde antes de esta
>    especificación**. Si `ChangeTimestamp` resultara ser el reloj del teléfono, la cadena de
>    evidencia entera pierde su marca de tiempo fiable y no solo el correctivo. **Es el supuesto más
>    caro de los cuatro y el que más lleva sin comprobarse.**
>
> Si la primera falla, el respaldo es un botón «Registrar inicio de trabajos» que el técnico pulsa.
> Prueba menos —depende de que se acuerde— pero es real y no bloquea.

> **Cómo se impide que el técnico cierre su propia orden, y dónde sigue el agujero.**
>
> `RG-23` lee `[EstadoOrdenID].[QuienCambia]`, que ya está poblada, y exige que quien mueva el estado
> sea la persona que le corresponde en **esa** orden:
>
> ```
> AND(
>   OR([EstadoOrdenID].[QuienCambia] <> "Supervisor", [SupervisorID].[Correo] = USEREMAIL()),
>   OR([EstadoOrdenID].[QuienCambia] <> "Tecnico",    [TecnicoID].[Correo]    = USEREMAIL())
> )
> ```
>
> Como `Cerrada` tiene `QuienCambia = Supervisor`, el técnico no puede ponerla: su correo no es el de
> `SupervisorID`. **La comparación es contra `.[QuienCambia]`, una columna de texto alcanzada por
> referencia, no contra el `Ref` a secas**, así que `V-17` no tiene nada que objetar. Y
> `[SupervisorID].[Correo]` es un salto que `RG-05` ya usa.
>
> **El agujero:** si la misma persona figura como `TecnicoID` y como `SupervisorID` de la orden, la
> regla se cumple y se cierra a sí misma. Por eso `RG-24` exige `[SupervisorID] <> [TecnicoID]`.
> Sin las dos, la primera parece funcionar y no funciona.
>
> Y el límite de siempre: **esto vive en la capa de aplicación.** Hay dos cuentas con permiso de
> edición sobre el Sheets, y quien escriba ahí pone `Cerrada` sin pasar por ninguna regla.

### 6.4 El motivo de la devolución: un solo sitio, y se retira el otro

Una versión anterior de esta especificación dejaba **dos** sitios donde escribir por qué el
supervisor devuelve el trabajo: la columna `MAN_Mantenimientos.ObservacionRechazo`, que ya existe y
está vacía, y `EVT_EventosOrden.Observacion`, que se crea aquí. Es la falta que
`FUNCIONAL_SGMC.md` §6 existe para impedir: dos sitios que dicen lo mismo acaban diciendo cosas
distintas y no hay forma de saber cuál miente.

**Se usa `EVT_EventosOrden.Observacion`. Se retira `MAN_Mantenimientos.ObservacionRechazo`.**

El argumento no es de gusto, es de quién escribe dónde:

- **La devolución es un acto del supervisor sobre la orden**, y `EVT_EventosOrden` es la tabla donde
  quedan registrados los actos sobre la orden, con su autor y su hora.
- **`MAN_Mantenimientos` es la tabla que edita el técnico.** Poner ahí el motivo del rechazo deja al
  rechazado como dueño del texto que lo justifica. La misma lógica por la que el técnico no cierra
  su propia orden.
- Con una fila de `EVT` por devolución, **una orden devuelta dos veces conserva los dos motivos.**
  Una columna única en `MAN` guarda solo el último.

**Esto retira una columna más de las tres de 7.3, y rompe una segunda entrada de `V-13`.** Está
verificado y medido en 12.4: `COBERTURA` clava `("MAN_Mantenimientos", "ObservacionRechazo")` bajo el
flujo «Devolucion del supervisor». Son **dos** entradas a re-apuntar, no una.

Queda anotado en `docs/FUNCIONAL_SGMC.md` §6 como fila 6.17.

---

## 7. Qué cambia exactamente

### 7.1 Tablas nuevas

Cada una declara **cuál es su clave y si es legible o generada**, como exige `V-17` y comprueba
`F-11`.

**`TAR_Tareas`** — grupo `Catalogos`. Clave `TareaID`, valores `TAR-001`, **legible** → entra en
`CLAVE_LEGIBLE`.

| Columna | Tipo | Destino | Obligatoria | Nota |
|---|---|---|---|---|
| `TareaID` | `Text` | — | clave | `TAR-001` |
| `TipoActivoID` | `Ref` | `TIP_TiposActivo` | Sí | La tarea se define sobre el tipo |
| `Nombre` | `Text` | — | Sí | «Inspección en campo» |
| `TipoMantenimiento` | `Enum` | — | Sí | `Preventivo`, `Correctivo`, `Admin`, `Servicio` |
| `FrecuenciaID` | `Ref` | `FRE_Frecuencias` | **No** | Vacía = «a demanda». Sin fila de plan |
| `FormularioID` | `Ref` | `FRM_Formularios` | Sí | El checklist es de la tarea |
| `RolRequeridoID` | `Ref` | `ROL_Roles` | No | **Necesita `alias_justificado`**: la clave destino es `RolID` |
| `Orden` | `Number` | — | No | Presentación |
| `Activo` | `Yes/No` | — | — | Inicial `TRUE` |

**`CRI_Criticidad`** — grupo `Catalogos`. Clave `CriticidadID`, valores `Total`, `Parcial grave`,
`Parcial leve`, **legible** → entra en `CLAVE_LEGIBLE`. Se crea con las tres filas y **con
`HorasRespuesta` y `HorasResolucion` en blanco**, a la espera de A-05.

| Columna | Tipo | Obligatoria | Nota |
|---|---|---|---|
| `CriticidadID` | `Text` | clave | La palabra es la clave (R-8), como en `EOT_EstadosOrden` |
| `Nombre` | `Text` | Sí | |
| `PorcentajeMin` / `PorcentajeMax` | `Number` | No | Instalación en avería que define el nivel |
| `HorasRespuesta` | `Number` | No | **En blanco hasta A-05.** Obligatoria haría imposible cargar el catálogo |
| `HorasResolucion` | `Number` | No | Idem |
| `Orden` | `Number` | No | |
| `Activo` | `Yes/No` | — | |

**`ETR_Estructuras`** — grupo `Maestras`. Clave `EstructuraID`, valores `ETR-001`, **legible** →
`CLAVE_LEGIBLE`.

> **Se llama `ETR_` y no `EST_`, contra lo que propone `MODELO_EVOLUCION_FASE_2.md` §4.** Ya existe
> `EST_Activo`, verificada como la única tabla con ese prefijo. Dos tablas `EST_` con significados
> distintos es exactamente el tipo de ambigüedad que produjo `SedeID`.

| Columna | Tipo | Destino | Obligatoria |
|---|---|---|---|
| `EstructuraID` | `Text` | — | clave |
| `Nombre` | `Text` | — | Sí |
| `Tipo` | `Enum` | — | Sí (`Puente`, `Viaducto`, `Box culvert`, `Tunel`) |
| `UnidadFuncionalID` | `Ref` | `UNF_UnidadesFuncionales` | Sí |
| `PR` | `Text` | — | No |
| `PK` | `Decimal` | — | No |
| `Ubicacion` | `LatLong` | — | No |
| `Activo` | `Yes/No` | — | — |

**`EVT_EventosOrden`** — grupo `Transaccionales`. Clave `EventoID` por `UNIQUEID()` → **generada**,
entra en `CLAVE_GENERADA`.

| Columna | Tipo | Destino | Nota |
|---|---|---|---|
| `EventoID` | `Text` | — | clave, `Initial value = UNIQUEID()` |
| `OTID` | `Ref` | `OT_OrdenesTrabajo` | **SIN `IsPartOf`**, por R-6b: la traza sobrevive a su orden |
| `EstadoOrdenID` | `Ref` | `EOT_EstadosOrden` | El estado al que se entra |
| `UsuarioID` | `Ref` | `USR_Usuarios` | `LOOKUP(USEREMAIL(), "USR_Usuarios", "Correo", "UsuarioID")` |
| `FechaHora` | `ChangeTimestamp` | — | Marca del servidor. **Supuesto sin cita: punto 4 del recuadro de 6.3** |
| `Observacion` | `LongText` | — | **Único** sitio del motivo de la devolución (6.4) |

**`PAU_Pausas`** — grupo `Transaccionales`. Clave `PausaID` por `UNIQUEID()` → **generada**, entra
en `CLAVE_GENERADA`.

> **`EVT_EventosOrden` y `PAU_Pausas` son dos tablas distintas y no intercambiables.** Una registra
> transiciones de estado; la otra, bloqueos que paran el reloj. Se confundieron una vez al editar
> este documento y el resultado fueron dos tablas con el mismo nombre y claves distintas. Se deja
> escrito para que no vuelva a pasar, y `PROPUESTAS` en `modelo_objetivo.py` las lleva declaradas por
> separado.

| Columna | Tipo | Destino | Nota |
|---|---|---|---|
| `PausaID` | `Text` | — | clave, `Initial value = UNIQUEID()` |
| `OTID` | `Ref` | `OT_OrdenesTrabajo` | Sin `IsPartOf`, misma razón que `EVT` |
| `Inicio` | `DateTime` | — | Obligatoria. Se escribe al abrir la pausa |
| `Fin` | `DateTime` | — | Vacía mientras la pausa sigue abierta. **Es un `UPDATE`**: ver 6.2 |
| `MotivoPendienteID` | `Ref` | `MOT_MotivosPendiente` | Obligatoria. Reutiliza las 5 filas que ya existen |
| `MinutosPausa` | `Decimal` | — | `App formula`, `RG-28`. Ver el supuesto de aritmética en 6.3 |

> **`EVT_EventosOrden` y `PAU_Pausas` van a producir un aviso `V-06`** cada una, del tipo «no es
> referenciada por nadie. Confirma que es punto de entrada». Es correcto y está previsto: son hojas
> que cuelgan de la orden sin `IsPartOf`, y el validador solo exime a las que lo llevan. **Verificado
> en la simulación de 12.4: cinco avisos en total, ninguno error.**

### 7.2 Columnas nuevas sobre tablas existentes

| Tabla | Columna | Tipo | Destino | Nota |
|---|---|---|---|---|
| `OT_OrdenesTrabajo` | `TareaID` | `Ref` | `TAR_Tareas` | Obligatoria si `Tipo = Preventivo` (`RG-26`) |
| `OT_OrdenesTrabajo` | `CriticidadID` | `Ref` | `CRI_Criticidad` | Obligatoria si `Tipo = Correctivo` (`RG-27`) |
| `OT_OrdenesTrabajo` | `HoraAviso` | `DateTime` | — | Cuándo se supo de la avería. No es `FechaProgramada` |
| `OT_OrdenesTrabajo` | `CanalAviso` | `Enum` | — | `Telefono`, `Correo`, `Web`, `SCADA`, `App`. **`SCADA` es del Sisga**, no del PDF de ETRA |
| `OT_OrdenesTrabajo` | `NivelAtencion` | `Enum` | — | `N1`, `N2`, `N3` |
| `ACT_Activos` | `RecintoID` | `Ref` | `SED_Sedes` | Opcional. **`alias_justificado`**; no se llama `SedeID` (R-7 y V-12) |
| `ACT_Activos` | `EstructuraID` | `Ref` | `ETR_Estructuras` | Opcional |
| `ACT_Activos` | `PK` | `Decimal` | — | Kilometraje lineal. Convive con `PR` |
| `SED_Sedes` | `UnidadFuncionalID` | `Ref` | `UNF_UnidadesFuncionales` | **Opcional**: Bogotá está fuera del corredor |
| `SED_Sedes` | `PR` | `Text` | — | |
| `SED_Sedes` | `PK` | `Decimal` | — | |
| `SED_Sedes` | `Ubicacion` | `LatLong` | — | Hoy una edificación no está en ningún sitio |
| `UNF_UnidadesFuncionales` | `PKInicial` | `Decimal` | — | `PRInicial` y `PRFinal` existen y están vacías |
| `UNF_UnidadesFuncionales` | `PKFinal` | `Decimal` | — | |
| `ROL_Roles` | `Clase` | `Enum` | — | `Acceso`, `Oficio`. Sin ella los doce oficios contaminan el perfil |
| `USR_Usuarios` | `OficioID` | `Ref` | `ROL_Roles` | **Opcional.** `alias_justificado`. Sin ella los doce oficios no tienen dónde leerse: ver 5.4 |
| `TIP_TiposActivo` | `SeVisita` | `Yes/No` | — | **No es `RequiereGPS`.** Inicial `TRUE`; `FALSE` solo en los cinco tipos sin lugar al que ir. Ver 5.3 |
| `PLA_PlanMantenimiento` | `TareaID` | `Ref` | `TAR_Tareas` | Obligatoria. El plan es activo × tarea |

**Y una columna que NO se declara aquí:** `MinutosRelojParado` de `OT_OrdenesTrabajo` es una
**columna virtual**, no una columna de la hoja. Va solo como `RG-29`. El motivo, con la cita que lo
sostiene, está en el recuadro de 6.3.

> **Nota de nombre, para que no sorprenda al leer el código.** La columna de dominio se llama `PK`
> (punto kilométrico) y en `modelo_objetivo.py` convive con el atributo `pk=True`, que marca la clave
> primaria. Son cosas distintas y el parecido es desafortunado. Se conserva `PK` porque es el nombre
> que usa operación y el que va a aparecer en los informes; `PKInicial` y `PKFinal` siguen la
> simetría de `PRInicial`/`PRFinal`, que ya existen.

### 7.3 Columnas que se retiran

**Las cuatro van a `CAMPOS_RETIRADOS` y salen de `MODELO` a la vez.** `V-12` aborta si una columna
está en los dos sitios. **Las cuatro se difieren a la Fase C**, por 7.4 y por 11.1.

| Tabla | Columna | Por qué | Efecto colateral |
|---|---|---|---|
| `ACT_Activos` | `FrecuenciaID` | La periodicidad es de la tarea | **Hay que sacarla también de `RETIPADOS['ACT_Activos']`** o `V-16` falla: «figura como retipado pero no existe en el modelo». **No se pierde información**: ver el recuadro |
| `TIP_TiposActivo` | `FormularioID` | El formulario es de la tarea | **Rompe `V-13` y toca la Fase B.** Ver 7.4 |
| `PLA_PlanMantenimiento` | `FrecuenciaID` | Se alcanza por `[TareaID].[FrecuenciaID]` (R-6) | `RG-11` cambia de expresión. `ESPEC-002` **ya la había aplazado** a esta especificación, así que no estaba cableada: retirarla no cuesta nada en la aplicación |
| `MAN_Mantenimientos` | `ObservacionRechazo` | Un solo sitio para el motivo de la devolución, y no en la tabla que edita el técnico (6.4) | **Rompe la segunda entrada de `V-13`**, «Devolucion del supervisor». Está vacía: la tabla tiene 2 filas de prueba y ninguna la usa |

> **Qué se pierde al retirar `ACT_Activos.FrecuenciaID`: nada, y está demostrado.**
>
> La columna está **poblada en las 34 filas**, así que retirarla parece tirar datos. No lo es. Los
> valores son un **round-robin exacto de 1 a 8**, comprobado contra la hoja:
>
> ```
> $ python -c "... [int(r[12]) for r in ACT_Activos] ..."
> FrecuenciaID en orden: [1,2,3,4,5,6,7,8, 1,2,3,4,5,6,7,8, 1,2,3,4,5,6,7,8, 1,2,3,4,5,6,7,8, 1,2]
> round-robin 1..8     : [1,2,3,4,5,6,7,8, 1,2,3,4,5,6,7,8, 1,2,3,4,5,6,7,8, 1,2,3,4,5,6,7,8, 1,2]
> COINCIDE EXACTAMENTE: True
> ```
>
> No hay ni una excepción en 34 filas. **No es la periodicidad de ningún activo: es el relleno que
> alguien escribió para que la columna no quedara vacía.** `SOS-001` sale `Diario` y `SOS-002`
> `Semanal`, cuando el Plan Maestro da `Mensual` a los 54 postes por igual.
>
> Así que no hay mapeo que declarar de las 34 a las tareas: **no hay origen que mapear.** La
> periodicidad real de cada tarea se carga desde el Plan Maestro al crear `TAR_Tareas`, y esos son
> los datos buenos. Se deja escrito porque «poblada en las 34 filas» invita a creer lo contrario, y
> ese es exactamente el error del `CodigoQR` que `CLAUDE.md` documenta: un campo lleno que disfraza
> un vacío.

### 7.4 El caso `TIP_TiposActivo.FormularioID`, que es el único que muerde

Es la única retirada que colisiona con trabajo ya aprobado, y hay que decirlo entero:

1. **`ESPEC-002` §6.1 la cablea como `Ref`** a `FRM_Formularios`. Si la Fase B ya corrió, retirarla
   deshace una referencia que se acaba de crear.
2. **`RETIPADOS['TIP_TiposActivo']['FormularioID']` la declara.** Hay que sacarla o `V-16` falla.
3. **`V-13` la clava en el propio validador**, en un diccionario que no vive en el modelo:

```python
COBERTURA = {
    ...
    "Checklist por tipo de activo": ("TIP_TiposActivo", "FormularioID"),
```

Retirarla sin más deja `validar_modelo.py` en error, y ese es **el único gate objetivo del
pipeline**. La corrección es re-apuntar la entrada a `("TAR_Tareas", "FormularioID")` y renombrar el
flujo a «Checklist por tarea».

> **Y esa corrección la tiene que revisar alguien distinto de quien la aplique.** `CLAUDE.md` §3 lo
> exige por un incidente real del 2026-08-07: el agente que aplicó `ESPEC-001C` editó
> `verificar_faseA.py` y después anunció que pasaba. **Se prefiere endurecer la comprobación a
> retirarla**: la entrada no se borra, se re-apunta, de modo que el flujo sigue exigiendo que exista
> un formulario en algún sitio.

**Recomendación de secuencia:** que la Fase B cablee `TIP_TiposActivo.FormularioID` como manda
`ESPEC-002` —no se toca— y que esta retirada se ejecute en la Fase C, junto con la carga de
`TAR_Tareas`. Retirar antes deja al sistema sin ninguna ruta al formulario.

### 7.5 Filas nuevas en catálogos existentes

| Tabla | Qué | Detalle |
|---|---|---|
| `EOT_EstadosOrden` | 1 fila | `Devuelta` · `Orden = 8` · `QuienCambia = Supervisor` · `EsFinal = FALSE` · `Activo = TRUE`. Sin tilde, como las siete que ya están |
| `ROL_Roles` | 12 filas | Claves 6 a 17, `Clase = Oficio`. Las 4 existentes pasan a `Clase = Acceso` |
| `CRI_Criticidad` | 3 filas | `Total`, `Parcial grave`, `Parcial leve`, **con los plazos vacíos** |
| `FRE_Frecuencias` | 0 filas nuevas | Solo se renombra `Bimensual` a `Bimestral` en la fila de clave `5`. La clave no cambia, así que nada se rompe |

**`Devuelta` con `Orden = 8` no es un descuido.** `Orden` es criterio de presentación, no una máquina
de estados: la devolución es una arista hacia atrás y no tiene sitio en una secuencia. Ponerla en 4,5
o renumerar las siete rompería datos existentes por nada.

**Añadir la octava fila no rompe `F-06`**, que comprueba `n < minimo` con `minimo = 7` para
`EOT_EstadosOrden`.

### 7.6 Valores declarados de `FIR_Firmas.TipoFirma` — APLICADO

> **Esta es la única parte de esta especificación que ya está en el modelo.** `FIR_Firmas.TipoFirma`
> declara hoy la lista con el único valor `Tecnico`, comprobado volcando
> `MODELO['FIR_Firmas']`. No hay nada que aplicar aquí; el razonamiento se conserva porque es lo que
> impide que alguien añada `Supervisor` creyendo que falta.

Cuando se escribió: `Enum`, obligatoria, con la nota `Tecnico` y sin lista.

**Se declara la lista con un solo valor: `Tecnico`.**

Parece pobre y es lo correcto:

- **`Supervisor` no entra.** El supuesto D-10 decidió que el supervisor **aprueba en el portal, no
  firma**, y por eso `MAN_Mantenimientos.Firma_Supervisor` y `CHK_Checklists.FirmaSupervisor` están
  en `CAMPOS_RETIRADOS`. Declararlo aquí contradiría una decisión cerrada.
- **`Tercero` tampoco.** Sale de `PRUEBA MENSUAL CON INTERVENTORÍA`, que es de la manta de INDRA
  —otro corredor—. Va a la sección 10 como A-06.

La columna se mantiene `Enum` y no `Text` precisamente por esto: cuando operación confirme A-06,
añadir `Tercero` es un cambio de configuración, no una migración.

---

## 8. Lo NO REALIZABLE HOY

Nada de esta tabla se recorta del plano de dominio. Todo sigue siendo requisito; lo que tiene es
causa y fecha.

| # | Lo que el dominio pide | Causa, con nombre | Qué haría falta |
|---|---|---|---|
| N-01 | Que no haya dos planes para el mismo (activo, tarea) | **El Sheets no impone unicidad.** No hay índice único, y la clave de AppSheet es de una sola columna | Backend con restricciones, o una comprobación en la app que igualmente se salta quien edite la hoja |
| N-02 | Que el plan de los 355 activos × sus tareas se genere solo | **Plan gratuito: los procesos programados no se ejecutan** | Plan de pago (decisión D-B). Mientras tanto, carga por lote sobre el Sheets |
| N-03 | Que las órdenes de la semana salgan del plan (`RG-12`) | **Ídem.** Es la limitación que más duele de todo este alcance: convierte 3.000 órdenes al año en 3.000 filas tecleadas | Plan de pago. Es el argumento económico de D-B, con número |
| N-04 | Traducir «pérdida a 37 km» del OTDR a una caja concreta | **No existe la tabla de equivalencias PR ↔ PK.** No es una fórmula: los PR no son lineales | Levantar la equivalencia con operación. Es trabajo de campo, no de modelo |
| N-05 | Que `EVT_EventosOrden` se escriba sola en cada transición | **No verificado** que una acción agrupada pueda añadir fila a otra tabla en el plan gratuito | Buscar la página oficial. Respaldo: botón que pulsa el técnico |
| N-06 | Que `HoraInicioTrabajos` sea infalsificable | **Dos cuentas con permiso de edición sobre el Sheets.** Quien escriba ahí edita la fila de evento | Nada dentro de AppSheet. Solo cambia con otro backend o con retirar el acceso |
| N-07 | Que una orden vencida se marque sola (`RG-08`) | **Bot programado.** No corre en el plan gratuito | Plan de pago. Hoy `Vencida` es un estado inalcanzable |
| N-08 | Crear una correctiva desde la aplicación | **`ESPEC-002` retiró `Adds` de `OT_OrdenesTrabajo`**, porque `OTID` sigue la convención legible `OT-0001` y no hay generador seguro fuera de línea | Decidir el generador de `OTID`. Es trabajo propio, y `UNIQUEID()` rompería la convención |
| N-09 | Avisar al supervisor cuando entra una correctiva | **Bot por evento**, mismo plan (`RG-07`, `RG-10`) | Plan de pago |
| N-10 | Atributos propios por tipo de equipo, sin columnas vacías | **Sin esquema dinámico** sobre Sheets. Es lo que GIMAN sí hace | Se paga con columnas vacías o con tablas por familia. Ninguna de las dos es gratis |
| N-11 | Que la cadena de evidencia sea atómica | **No hay transacciones.** Mantenimiento, fotos, firma y checklist son escrituras independientes | Otro backend. Hoy es límite declarado en `ESPEC-002` §6 |
| N-12 | Integración con el SCADA para abrir la correctiva sola | **Sin plan Core no hay API REST** | Plan Core. Hoy el operador transcribe |
| N-13 | Archivar por año antes de degradar la sincronización | **~50.000 filas por tabla.** Con los 355 activos del Plan Maestro, `CHD_ChecklistDetalle` proyecta **76.680 filas/año** y 383.400 a cinco: pasa el umbral en el primer año. Sale de `python scripts/capacidad.py` | Procedimiento de archivo. No es opcional a 5 años |

**Cinco de las trece son la misma causa:** N-02, N-03, N-07, N-09 y, en parte, N-12. Todas dicen
«plan gratuito». Es la decisión D-B y aquí queda con su factura: sin ella, el sistema registra
trabajo pero no lo programa, y el ahorro que justifica el proyecto no llega.

---

## 9. Qué NO cubre esta especificación

- **Almacén y repuestos.** El informe mensual pide «Repuestos y Herramientas». Sigue fuera. Meterlo
  después son dos tablas y una referencia desde el mantenimiento.
- **SAT y flotas de vehículos.** Fuera en GIMAN también.
- **Código QR.** Fuera por decisión del 2026-08-07.
- **El cableado de la aplicación.** No se toca ni una línea de lo que hay que reponer: ni el orden de
  los bloques, ni las 39 referencias, ni las 21 reglas, ni el plan de `PRUEBA-003`. **Con una
  salvedad que cambió el 2026-08-10:** el literal `1.0` de `RG-01` ya no se pega. La hoja que la
  aplicación lee trae `TIP_TiposActivo.RadioGeofencingKm` poblado en los 27 tipos, así que se cablea
  la expresión que desreferencia el radio por tipo.
- **Certificaciones del técnico con vigencia.** Fase 2, por decisión de operación. Lo que muerde ahí
  no son las dos tablas: es que la vigencia se evalúa contra la fecha del trabajo.
- **Brigada o cuadrilla** entre técnico y zona.
- **El subsistema de fibra en detalle** —recorrido por UF, medición de 48 hilos, las ~600 cajas—.
  La jerarquía de ubicación de la sección 4 es su precondición, no su solución.
- **La subdivisión de unidades funcionales** (2,1 · 2,2 · 4,1 · 4,2). Es un patrón visto en el
  informe de Neiva–Girardot. Supuesto A-07.
- **La configuración en AppSheet.** Esta especificación declara el modelo y la estructura de la hoja.
  El cableado es Fase C y necesita su propia especificación y sus pruebas.

---

## 10. Supuestos abiertos que operación debe confirmar

**Ninguno de estos bloquea.** El método vigente es construir bajo supuestos (`CLAUDE.md`). Se
declaran para que nadie los confunda con hechos verificados, y **ninguno se presenta como carencia
del Sisga**: son preguntas.

| # | Pregunta | De dónde sale | Qué cambia según la respuesta |
|---|---|---|---|
| A-01 | **¿Los 355 activos son los del Sisga?** | El Plan Maestro es del Sisga y operación lo confirmó; el dimensionamiento derivado —1.916 órdenes, 4,1 años de cuota— se calculó sobre un maestro descrito como «muy similar» | Todo el volumen. Es el vacío más grande que queda |
| A-02 | **¿Un tipo tiene siempre las mismas tareas, o varían por unidad funcional?** | El cronograma da dos por tipo sin distinguir UF | Si varían, `TAR_Tareas` necesita `UnidadFuncionalID` opcional. Añadirlo después es una columna |
| A-03 | **¿Qué es `SISTEMA CONTROL DE TRÁFICO, cantidad: 2`?** | Está en el cronograma contractual **y no en los 24 tipos del Plan Maestro** | Un tipo de activo más, o una duplicidad. Es una discrepancia entre dos documentos del Sisga |
| A-04 | **La sede de Bogotá: ¿UF vacía o UF administrativa?** | Está fuera del corredor y aloja 29 portátiles y 3 impresoras | Aquí se adopta «UF vacía». Lo contrario mete una fila falsa en el catálogo de la interventoría |
| A-05 | **¿El Sisga tiene SLA contractuales propios?** | Los plazos 2/4, 4/12, 12/48 h son de **ETRA, Neiva–Girardot** | `CRI_Criticidad` se crea con los plazos **en blanco** por esto. Si el Sisga no tiene, hay que decidir si el sistema los mide igual |
| A-06 | **`PRUEBA MENSUAL CON INTERVENTORÍA`: ¿firma el interventor en la app?** | Manta de **INDRA**, otro corredor | Si sí, `FIR_Firmas.TipoFirma` gana `Tercero` y `TAR_Tareas` una bandera. Es configuración, no migración |
| A-07 | **¿Las UF del Sisga se subdividen?** | Informe de **Neiva–Girardot**, donde aparecen 2,1 · 2,2 · 4,1 · 4,2 | `UNF_UnidadesFuncionales` es plana hoy. Si se subdividen, gana autorreferencia |
| A-08 | **¿El Sisga mantiene iluminación?** | Tipo `ILUMINACION` en el informe de **Neiva–Girardot**, ausente de los 24 | Un tipo más, o nada |
| A-09 | **¿Quién puede dar el aviso de una correctiva?** | ETRA lo restringe a operadores autorizados | Decide si `CanalAviso = App` existe y quién ve el formulario |
| A-10 | **¿Los doce oficios son los definitivos?** | Verificados en la columna `PERSONAL`, pero es un reparto de plan, no un organigrama | Filas del catálogo. Barato de corregir |
| A-11 | **¿Hay almacén de repuestos gestionado?** | Pregunta abierta desde `CONTEXTO_OPERACION.md` §6 | Fuera de alcance en cualquier caso; decide si `MotivoPendienteID = Falta de repuesto` basta |
| A-12 | **¿Cuántas estructuras tienen paso de fibra, y están inventariadas?** | Pregunta abierta | Filas de `ETR_Estructuras`. La tabla se crea vacía |

**Adoptados como supuestos en esta especificación, y por tanto vinculantes hasta que el campo los
desmienta:** A-04 (UF vacía), A-05 (catálogo con plazos en blanco), A-06 (`TipoFirma` solo
`Tecnico`).

---

## 11. Riesgos, dependencias y qué se rompe si sale mal

### 11.1 La dependencia dura: esto **bloquea la Fase B** si se aplica antes

Verificado en el código, no supuesto (ver 2.4). En cuanto `TAR_Tareas`, `CRI_Criticidad`,
`ETR_Estructuras`, `EVT_EventosOrden` o `PAU_Pausas` se declaren en `MODELO` sin existir como hoja,
`F-02` da `FASE A INCOMPLETA`, y el cableado de la aplicación exige `FASE A CERRADA` para empezar.

**Dos salidas, y solo dos:**

1. **Preferida: aplicar esta especificación después del acta de cierre de la Fase B.** El frente
   activo sigue siendo `ESPEC-002` y no se interrumpe.
2. Si hay que adelantarla, **crear las cinco hojas en el Sheets en la misma ventana** en que se
   declaran en el modelo. Nunca una cosa sin la otra.

Lo que **no** vale es relajar `F-02` para que deje pasar tablas inexistentes. Sería retirar la
comprobación en lugar de endurecerla, que es justo lo que `CLAUDE.md` §3 prohíbe.

### 11.2 Qué se rompe si sale mal

| Si | Se rompe |
|---|---|
| Se retira `TIP_TiposActivo.FormularioID` sin re-apuntar `V-13` | `validar_modelo.py` en error. **No hay veredicto que valga**: es el único gate objetivo |
| Se retira `ACT_Activos.FrecuenciaID` sin sacarla de `RETIPADOS` | `V-16`: «figura como retipado pero no existe en el modelo» |
| Se declara `ACT_Activos.SedeID` con el significado nuevo | `V-12` aborta. Y si alguien fuerza el paso, dos columnas con el mismo nombre y AppSheet resolviendo una sin decir cuál (R-7) |
| Se retira `TIP.FormularioID` **antes** de cargar `TAR_Tareas` | El sistema se queda **sin ninguna ruta al formulario**. Ningún checklist abre |
| Se marca `RequiereGPS = FALSE` sin modificar `RG-01` | `DISTANCE()` contra `Ubicacion` en blanco **rechaza el cierre legítimo**. Los cinco tipos quedan con órdenes que nadie puede cerrar |
| Se pone `RelojParado` como columna acumulada en vez de `EVT_EventosOrden` | Pérdida de actualización silenciosa en offline. Dos pausas sin señal y el total miente, sin aviso |
| Se sella `HoraInicioTrabajos` con un `ChangeTimestamp` de la orden | Se reescribe en la segunda ida a `En ejecucion`. **El tiempo de respuesta se acorta solo**, y hacia el lado que favorece a quien lo mide |
| Se configura `RG-23` sin `RG-24` | La segregación **parece** funcionar. Quien sea técnico y supervisor de la misma orden se la cierra a sí mismo |
| Se da `TAR_Tareas` clave legible y no se mete en `CLAVE_LEGIBLE` | `F-11` falla: «tiene clave de texto legible y NO está en `CLAVE_LEGIBLE`» |
| Se meten los 12 oficios con clave `ROL-06` | Clave mixta con `2.0`. `F-11` no falla, pero la tabla queda con dos convenciones y `USR_Usuarios.RolID` guardando números y textos |
| Se crea una fila `A demanda` en `FRE_Frecuencias` con `Dias = 0` | `RG-11` deja los 29 portátiles vencidos todos los días desde su última reparación |
| Se aplica esto antes de cerrar la Fase B | La Fase B no puede empezar. Ver 11.1 |

### 11.3 Riesgos de método

- **Es un lote grande.** Cinco tablas, diecisiete columnas, tres retiradas, once reglas. Se
  recomienda partirlo al ejecutar: primero la capa de tareas y la ubicación (secciones 3 y 4), que
  no dependen de nada; después el correctivo y la recepción (sección 6), que dependen de decisiones
  de operación pendientes (A-05, A-09).
- **Tres comportamientos de AppSheet sin verificar** (recuadro de 6.3). Ninguno bloquea el modelo,
  los tres bloquean la configuración. Se verifican **antes** de que el ejecutor abra el editor, no
  durante.
- **`docs/ARQUITECTURA_OBJETIVO_SGMC.md` se regenera**, no se edita. El flujo obligatorio ante
  cualquier cambio de diseño sigue siendo: editar `modelo_objetivo.py`, correr `validar_modelo.py`
  hasta 0 errores, correr `generar_doc_arquitectura.py`.

---

## 12. Cómo se declara en el modelo

Todo se edita **solo** en `scripts/modelo_objetivo.py`. Qué estructura toca cada cosa:

| Cambio | Estructura |
|---|---|
| `TAR_Tareas`, `CRI_Criticidad`, `ETR_Estructuras`, `EVT_EventosOrden`, `PAU_Pausas` | `MODELO`, con `nueva=True` |
| Las 17 columnas de 7.2 | `MODELO`, con `nueva=True` en cada una |
| `ACT_Activos.FrecuenciaID`, `TIP_TiposActivo.FormularioID`, `PLA_PlanMantenimiento.FrecuenciaID` | `CAMPOS_RETIRADOS`, **y salen de `MODELO`** |
| Sacar `FrecuenciaID` y `FormularioID` de los retipados | `RETIPADOS` |
| `TAR_Tareas`, `CRI_Criticidad`, `ETR_Estructuras` | `CLAVE_LEGIBLE` |
| `EVT_EventosOrden`, `PAU_Pausas` | `CLAVE_GENERADA` |
| `RG-21` a `RG-31` | `REGLAS` |
| Modificación de `RG-01` y `RG-11` | `REGLAS`, y `MODELO` en el `valid_if` de `MAN_Mantenimientos.Coordenadas_Cierre_LatLong` |
| Re-apuntar «Checklist por tipo de activo» | **`scripts/validar_modelo.py`, `COBERTURA`.** Fuera del modelo, y con revisión independiente (7.4) |

**Nada de esto se ejecuta hasta que `python scripts/validar_modelo.py` devuelva 0 errores.**

### 12.1 Las reglas nuevas

| # | Tabla | Columna | Tipo | Expresión | Para qué |
|---|---|---|---|---|---|
| `RG-21` | `USR_Usuarios` | `RolID` | `Valid_If` | `IN([RolID], SELECT(ROL_Roles[RolID], [Clase] = "Acceso"))` | El perfil de acceso no puede ser un oficio |
| `RG-22` | `ACT_Activos` | `Ubicacion` | `Required_If` | `[TipoActivoID].[RequiereGPS] = TRUE` | Los cinco tipos sin coordenada dejan de exigirla |
| `RG-23` | `OT_OrdenesTrabajo` | `EstadoOrdenID` | `Valid_If` | `AND(OR([EstadoOrdenID].[QuienCambia] <> "Supervisor", [SupervisorID].[Correo] = USEREMAIL()), OR([EstadoOrdenID].[QuienCambia] <> "Tecnico", [TecnicoID].[Correo] = USEREMAIL()))` | **El técnico no cierra su propia orden.** Da uso a `QuienCambia`, que existe y nadie lee |
| `RG-24` | `OT_OrdenesTrabajo` | `SupervisorID` | `Valid_If` | `[SupervisorID] <> [TecnicoID]` | Cierra el agujero de `RG-23` |
| `RG-25` | `PLA_PlanMantenimiento` | `TareaID` | `Valid_If` | `AND([TareaID].[TipoActivoID] = [ActivoID].[TipoActivoID], ISNOTBLANK([TareaID].[FrecuenciaID]))` | La tarea es del tipo del activo, y una tarea sin frecuencia no genera plan |
| `RG-26` | `OT_OrdenesTrabajo` | `TareaID` | `Required_If` | `[Tipo] = "Preventivo"` | Una preventiva sin rutina no se puede contar contra el plan |
| `RG-27` | `OT_OrdenesTrabajo` | `CriticidadID` | `Required_If` | `[Tipo] = "Correctivo"` | Sin criticidad no hay plazo contra el que medir |
| `RG-28` | `EVT_EventosOrden` | `MinutosPausa` | `App formula` | Diferencia `[Fin] − [Inicio]` en minutos. **Sintaxis pendiente de verificar** (6.3) | El total de reloj parado se deriva, no se acumula |
| `RG-29` | `OT_OrdenesTrabajo` | `MinutosRelojParado` | `App formula` | `SUM(SELECT(EVT_EventosOrden[MinutosPausa], [OTID] = [_THISROW].[OTID]))` | El acumulado que no compite consigo mismo |
| `RG-30` | `MAN_Mantenimientos` | `ObservacionRechazo` | `Required_If` | `[OTID].[EstadoOrdenID] = "Devuelta"` | Devolver sin decir por qué no es devolver. **Comparación legítima**: `EOT_EstadosOrden` está en `CLAVE_LEGIBLE` |
| `RG-31` | `OT_OrdenesTrabajo` | `HoraAviso` | `Editable_If` | `FALSE` | Misma doctrina que `RG-20`. **Solo vale si la escribe la transición**, no un `Initial value` |

**Comprobado a mano contra `V-17` antes de escribirlas:** las comparaciones contra literal de
`RG-21` (`[Clase]`, un `Enum`), `RG-23` (`[EstadoOrdenID].[QuienCambia]`, columna alcanzada por
referencia), `RG-26` y `RG-27` (`[Tipo]`, un `Enum`) **no caen sobre un `Ref` a secas**. La única que
compara un `Ref` contra texto es `RG-30`, y su destino `EOT_EstadosOrden` **sí está** en
`CLAVE_LEGIBLE`, que es la excepción legítima que `V-17` contempla.

### 12.2 Las dos reglas que se modifican

**`RG-01`**, geofencing. La versión definitiva del modelo pasa a:

```
OR(
  [OTID].[ActivoID].[TipoActivoID].[RequiereGPS] = FALSE,
  DISTANCE([Coordenadas_Cierre_LatLong], [OTID].[ActivoID].[Ubicacion_LatLong])
      <= [OTID].[ActivoID].[TipoActivoID].[RadioGeofencingKm]
)
```

> **Esto NO cambia lo que hay que cablear, pero el punto de partida sí cambió.** `ESPEC-002` §7
> mandaba pegar el literal `1.0` porque `RadioGeofencingKm` estaba vacío en los 18 tipos de la hoja
> heredada, y esa hoja quedó superada el 2026-08-10. **La que la aplicación lee trae el radio poblado
> en los 27 tipos**, así que lo que se cablea es la expresión que lo desreferencia y el literal deja
> de tener uso. La divergencia entre el modelo y lo que se pegaba, que allí estaba declarada como
> deuda, se cerró poblando la columna.
>
> Lo que esta especificación añade encima de eso es **solo la exención de los cinco tipos que no se
> visitan**, que sigue sin poder aplicarse porque esos cinco no tienen fila (5.3.1).
>
> El mensaje de error no cambia: `Ubicación fuera de rango: debe estar junto al activo para cerrar.`

**`RG-11`**, próxima fecha del plan. Pasa de `[UltimaEjecucion] + [FrecuenciaID].[Dias]` a:

```
[UltimaEjecucion] + [TareaID].[FrecuenciaID].[Dias]
```

Porque `PLA_PlanMantenimiento.FrecuenciaID` se retira. **`ESPEC-002` §7 ya excluyó `RG-11` de la
Fase B** precisamente porque su referencia estaba aplazada a esta especificación, así que el cambio
no toca nada configurado. La ruta `[TareaID].[FrecuenciaID].[Dias]` es navegable y `V-11` la valida:
`TareaID` → `TAR_Tareas`, `FrecuenciaID` → `FRE_Frecuencias`, `Dias` es `Number`.

### 12.3 Reconciliación con `PROPUESTAS` y `DECISIONES`

**Mientras se escribía esta especificación, otro frente añadió a `modelo_objetivo.py` dos registros
nuevos —`PROPUESTAS` y `DECISIONES`— y el verificador `scripts/verificar_documentos.py`.** Se
comprobó contra ellos, y el resultado hay que dejarlo escrito porque cambia lo que el ejecutor tiene
que tocar.

**Los conteos de la sección 2.1 no cambian:** el modelo sigue en 28 tablas, 200 columnas, 38
referencias y 21 reglas. Los registros nuevos no declaran tablas: declaran intenciones.

**`DECISIONES` corrobora cinco decisiones de esta especificación**, tomadas por separado y desde el
archivo. Conviene decirlo porque es la única confirmación independiente que tiene este documento:

| Decisión de `DECISIONES` | Dónde aparece aquí |
|---|---|
| `TAR_Tareas.FrecuenciaID` se usa, `ACT_Activos.FrecuenciaID` se descarta | 3.1 y 7.3 |
| `TAR_Tareas.FormularioID` se usa, `TIP_TiposActivo.FormularioID` se descarta | 3.1 y 7.4 |
| `EVT_EventosOrden` con `SUM()`, columna acumulada descartada | 6.2 y `RG-29` |
| `ChangeTimestamp` en la transición de estado, `Initial value = NOW()` descartado | 6.2 y `RG-31` |
| `ROL_Roles` ya existe: falta poblarla con los doce del Plan Maestro | 5.2 |

Y `DECISIONES_ABIERTAS` registra como sin resolver «activos sin ubicación física: camino sin
evidencia de coordenada, o fuera del alcance». **Esta especificación la resuelve** en 5.3: tienen
camino, con `RequiereGPS` y la modificación de `RG-01`. Al aplicarla, esa entrada sale de la lista de
abiertas.

**Qué hay que corregir en `PROPUESTAS` al aplicar esto:**

**Aviso de lectura: `PROPUESTAS` es un registro vivo y cambió tres veces mientras se escribía esta
sección.** Lo que sigue se releyó del archivo el 2026-08-10, no de memoria:

```
$ python -c "import sys;sys.path.insert(0,'scripts');import modelo_objetivo as m;print(sorted(m.PROPUESTAS))"
['CER_Certificaciones', 'CRI_Criticidad', 'ETR_Estructuras', 'EVT_EventosOrden',
 'MED_MedicionesHilo', 'PAU_Pausas', 'ROL_Requeridos', 'TAR_Tareas', 'USR_Certificaciones']
```

| Entrada | Estado | Acción |
|---|---|---|
| `TAR_Tareas`, `CRI_Criticidad`, `ETR_Estructuras`, `EVT_EventosOrden` | Registradas y coinciden con esta especificación, **incluido el prefijo `ETR_`** de 7.1 | Salen de `PROPUESTAS` y entran en `MODELO`. `D-02` falla si están en los dos a la vez |
| **`PAU_Pausas`** | **Vuelve a estar registrada.** La regresión que denunciaba este cruce está corregida, y `PROPUESTAS` la lleva declarada por separado de `EVT_EventosOrden`, que es lo que 6.2 exige | Ídem: sale de `PROPUESTAS` y entra en `MODELO` |
| `ROL_Requeridos` | **No se propone aquí.** El rol requerido cabe como columna `TAR_Tareas.RolRequeridoID`; una tabla aparte solo hace falta cuando una tarea exija **varios** roles, que es Fase 2 (5.2) | Retirarla, o dejarla marcada explícitamente como Fase 2 |
| `MED_MedicionesHilo`, `CER_Certificaciones`, `USR_Certificaciones` | Fuera del alcance de esta especificación (sección 9) | Se quedan como están |

**Salida de la comprobación, hoy:**

```
$ python scripts/verificar_documentos.py
DOCUMENTOS CONSISTENTES CON EL MODELO
```

**De los dos `D-01` que este cruce dejaba abiertos no queda ninguno.** El de `PAU_Pausas` se cerró
declarándola en `PROPUESTAS`, no reescribiendo prosa. El de `EST_Estructuras` —esta misma
especificación citándolo para explicar por qué **no** se llama así— se cerró con la línea
`<!-- verificar_documentos: ignorar -->` de la cabecera, que es la salida prevista para un nombre que
se menciona **para descartarlo**. `MODELO_EVOLUCION_FASE_2.md` §4 ya escribe `ETR_Estructuras`, así
que el nombre está reconciliado en los dos sitios.

Y un falso positivo que apareció en la primera pasada y volverá: **`ITS_TI` no es una tabla.** Es
parte del nombre del archivo `contexto/Plan Maestro de Mantenimiento ITS_TI (1).xlsx`, y `RE_TABLA`
—el patrón `[A-Z]{3,4}_[A-Za-z][A-Za-z0-9]*`— no distingue un nombre de tabla de un acrónimo con
guion bajo dentro de un nombre de fichero.

> **El falso positivo se reporta, no se rodea.** Se podría hacer callar al verificador dejando de
> escribir el nombre del archivo, pero entonces esta especificación dejaría de decir contra qué
> archivo exacto se verificó, que es lo que `CLAUDE.md` §2 exige. La corrección correcta es del
> verificador —excluir lo que va dentro de comillas de ruta, o llevar una lista de acrónimos—, y le
> toca a alguien distinto de quien está siendo verificado.

**Hay además un límite de método en `D-03` que conviene conocer antes de fiarse del verde.** La
comprobación de columnas solo mira el patrón `Tabla.Columna`. Las tablas de las secciones 7.1 y 7.2
listan la tabla y la columna en celdas separadas, así que **`D-03` no las ve**: no valida las
diecisiete columnas nuevas ni las tres retiradas. No es un defecto de esta especificación, pero
significa que **pasar `verificar_documentos.py` no prueba que las columnas de aquí sean correctas**.
Eso lo prueba `validar_modelo.py` cuando se declaren, y el arquitecto antes.

---

## 13. Criterio de cierre de esta especificación

No se cierra con una configuración: se cierra con un modelo que valida y una hoja que lo respalda.

1. `python scripts/validar_modelo.py` devuelve **0 errores**. Es el único gate objetivo.
2. `python scripts/verificar_faseA.py "BD/Modelo de Datos (N).xlsx"` vuelve a decir
   `FASE A CERRADA` sobre una descarga posterior a la creación de las cinco hojas.
3. `python scripts/generar_doc_arquitectura.py` regenera
   `docs/ARQUITECTURA_OBJETIVO_SGMC.md` sin editarlo a mano.
4. Los tres comportamientos de AppSheet del recuadro de 6.3 están verificados contra la página
   oficial y añadidos a `docs/BASE_CONOCIMIENTO_APPSHEET.md`, o declarados allí como supuestos.
5. `python scripts/verificar_documentos.py` deja de reportar los `D-01` de este documento, por
   haberse aplicado la reconciliación de 12.3 y no por haber reescrito la prosa.

Y el criterio que no es técnico: **que un lector de operación reconozca su trabajo en la sección 3 a
la 6.** Si no lo reconoce, el modelo está mal aunque valide.
