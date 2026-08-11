# Contexto de operación — qué dicen los documentos reales

Lo que aportan al modelo de datos del SGMC los documentos de `contexto/`. No es un resumen de cada
uno: es **lo que sirve** para decidir tablas, columnas y flujos, con la cita de dónde sale.

> **Son ocho archivos y aquí se destilan siete.** El que falta es
> `MATRIZ_MANTENIMIENTO_SISGA_2026 (1).xlsx`, **que no se ha abierto**: no está en la tabla de
> procedencia de más abajo ni ha alimentado ninguna decisión. Se deja dicho para que nadie lo lea
> como que ya se revisó y no aportaba nada.

> **Nota del 2026-08-09.** El contenido de este documento no ha cambiado: destila documentos de
> operación, y esos documentos no se han movido. Lo que se corrigió son **dos cifras de capacidad
> mal atribuidas** —los 4,1 años de cuota son del escenario de 500 activos, no de los 355— y la
> lectura de `OT_OrdenesTrabajo`, que no tiene fecha de creación sino fecha programada. Nada de lo
> que aquí se pregunta a operación se ha respondido todavía.

> **Nota del 2026-08-10: el modelo de datos cambió, y lo que aquí destilamos no.** Los documentos de
> operación siguen diciendo lo mismo; lo que se movió es el modelo contra el que se leen. Cuatro
> cambios afectan a cómo se cita este documento:
>
> - **Toda clave es alfanumérica con prefijo** —`ACT-0001`, `TIP-001`, `UNF-01`, `SED-001`,
>   `USR-001`—, porque AppSheet tipaba la clave `Number` y descartaba en silencio la fila con clave
>   de texto.
> - **Las seis columnas de coordenada llevan `_LatLong` en el nombre**, para que AppSheet infiera el
>   tipo. La del activo es `ACT_Activos.Ubicacion_LatLong`.
> - **`USR_Usuarios.SedeID` se retiró** —la zona de trabajo del técnico vive en `ASG_AsignacionZona`
>   y solo ahí— y **`SED_Sedes` volvió** como padre de ubicación del equipo bajo techo, con cinco
>   columnas nuevas: `UnidadFuncionalID`, `PR`, `TramoINVIAS`, `PK` y `Ubicacion_LatLong`.
> - **`ACT_Activos` tiene ahora `PK`, `TramoINVIAS` y `SedeID`** además del `PR` que ya tenía. Es la
>   corrección de la sección 2 de `REGLAS_DEL_MODELO_DE_DATOS.md`: un PR no identifica un punto
>   porque el corredor atraviesa tres rutas de INVÍAS y tiene dos sitios distintos llamados
>   `PR 0+000`.
>
> Las diez reglas que manda el motor están en
> [`REGLAS_DEL_MODELO_DE_DATOS.md`](REGLAS_DEL_MODELO_DE_DATOS.md), generado del modelo.

| | |
|---|---|
| Origen | `contexto/`, aportado el 2026-08-07. Cifras revisadas el 2026-08-09 |
| Documentos | `contexto/` tiene **8**; este documento destila **7**. El octavo, `MATRIZ_MANTENIMIENTO_SISGA_2026 (1).xlsx`, **no se ha abierto** y no aporta nada aquí todavía |
| Para qué sirve | Alimentar `MODELO_EVOLUCION_FASE_2.md` con dominio verificado, no supuesto |
| Qué **no** es | Una especificación. Nada de aquí se ejecuta sin pasar por `ESPEC-00N` y su veredicto |

## Procedencia de cada fuente

**Son documentos de ejemplo que dan contexto. No son la vara con la que se mide el Sisga.** Se citan
para copiar método, no para exigir cumplimiento. Aun así hay que saber de dónde viene cada uno, para
no atribuirle al Sisga una estructura que es de otro corredor:

| Documento | Corredor | Autor · año |
|---|---|---|
| `2-MANTENIMIENTO.pdf` | Neiva – Aipe – Castilla – Espinal – Girardot | ETRA · Consorcio Constructor ANG · 2017 |
| `Informe … enero 2025 v1.1.docx` | **Neiva – Girardot**, el mismo de ETRA | — · 2025 |
| `PROPUESTA - PLAN MTTO DC 2016.xlsx` | Doble calzada, contrato 444-005-15 | INDRA Colombia · 2016 |
| `Plan Maestro de Mantenimiento ITS_TI.xlsx` | **Sisga** — cantidades confirmadas por operación | 2026 |
| `PLAN_MANTENIMIENTO_SISGA_2026.docx` | Sisga | 2026 |
| `Plan de actividades … 2025 Componente ITS.xls` | Sisga · supervisado por JOYCO S.A.S. | 2025 |

**Regla de uso:** cuando este documento diga «la práctica del sector», sale de los tres primeros.
Cuando diga «el Sisga», sale de los tres últimos. Nada de los tres primeros se convierte en
requisito sin que operación lo confirme.

> **Y hay una fuente que sí es la vara, y no está en esa tabla: el contrato.** Junto a los ocho
> archivos, `contexto/` tiene la carpeta **`SISGA Contrato`** con cinco PDF —`acta de inicio`,
> `apendice_1_y_2`, `apendices_3_al_9`, `contrato_parte_general_y_especial` y `otrosies 1 a 11`—.
> **No es material de ejemplo: obliga.** De ahí salen las cuatro filas de
> `UNF_UnidadesFuncionales` —nombre real y tramo, no cuartos iguales—, y el único dato de
> `SED_Sedes` anclado en fuente: el peaje de Machetá, `SED-003`, con `PR = 27+240` y
> `TramoINVIAS = 5607`. **Es la única fila de las seis que tiene unidad funcional, PR y tramo**; las
> otras cinco los tienen vacíos. Lo que el contrato diga manda sobre lo que digan los seis
> documentos de arriba, y `ESTADO.md` §3 lleva la lectura completa.

Verificado contra el archivo el 2026-08-07. El informe de enero figuraba aquí como del Sisga y no lo
es: su encabezado dice `NEIVA – GIRARDOT` y sus tablas nombran CCO Neiva, PC Peaje Flandes y PC
Peaje Pata.

## Contra qué se verificó

`CLAUDE.md` §2 exige declararlo. **Las cifras del modelo de este documento se leyeron en su día de
`BD/Modelo de Datos (11).xlsx`**, el archivo con el que se cerró la Fase A, no de producción ni de
memoria.

**Ese libro ya no está en el repositorio.** Con la limpieza del 2026-08-10, `BD/` quedó con **un
solo archivo**, `BD/Modelo_Datos_PLANTILLA.xlsx`, que es a la vez el entregable y la hoja publicada;
tener dos descargas de la misma hoja fue lo que permitió verificar contra una y desplegar contra
otra. **Toda comprobación de este documento se rehace contra ese archivo**, y las cifras que hablan
del modelo se rederivan, no se copian de aquí:

```bash
ls BD/
python scripts/verificar_faseA.py "BD/Modelo_Datos_PLANTILLA.xlsx"
```

---

## 1. El inventario de documentos

| Documento | Qué aporta que no teníamos |
|---|---|
| `Plan Maestro de Mantenimiento ITS_TI.xlsx` | 24 tipos, 355 activos, tarea, periodicidad, herramienta y **personal por tarea** |
| `PLAN_MANTENIMIENTO_SISGA_2026.docx` | El plan vigente por subsistema |
| `Plan de actividades … 2025 Componente ITS.xls` | **Cronograma contractual**, supervisado por JOYCO S.A.S. |
| `Informe … enero 2025 v1.1.docx` | La **salida** exigida: qué secciones tiene el informe mensual |
| `PROPUESTA - PLAN MTTO DC 2016.xlsx` | **La manta**: la rejilla semanal y el indicador de cumplimiento |
| `2-MANTENIMIENTO.pdf` | El **flujo de correctivo**, los SLA y la arquitectura de un GMAO real |
| `PPT 2026 Operación de Vías.xlsx` | Presupuesto de operación. Sin uso para el modelo |

---

## 2. El inventario del Sisga: tenemos el censo, no el registro

`Plan Maestro de Mantenimiento ITS_TI.xlsx`, 24 filas × 11 columnas. Lo que da: tipo, cantidad,
unidad, área, tipo de mantenimiento, tarea, periodicidad, herramienta, personal y costo.

**Y aquí hay una media verdad que conviene deshacer.** Este apartado lo daba por confirmado el
2026-08-07 como el inventario real del Sisga, y la pregunta 6 del apartado 6 dice a la vez que
operación lo describió como «muy similar» al del Sisga, no como el del Sisga. **Las dos cosas no
pueden ser ciertas.** Vale la segunda, que es la cauta: hasta que operación lo confirme por escrito,
estas cantidades son un maestro parecido y no el censo de este corredor.

Lo que **no** da: **las propiedades de cada equipo**. Sabemos que hay 54 postes SOS; no sabemos cuál
es cada uno, dónde está, ni qué serie tiene. `ACT_Activos` necesita 355 filas con identidad y
ubicación, y lo que hay son 18 cifras agregadas.

> **Los «24 tipos» de este maestro no son los tipos de `TIP_TiposActivo`, y confundirlos costó un
> día.** Son dos vocabularios distintos: el maestro cuenta equipos —24 filas, de las que **18** son
> familias contables en `Und`— y el catálogo decide **qué checklist ve el técnico**. Hasta el
> 2026-08-09 los dos números eran 18 y parecía la misma lista; no lo era, y nueve familias colgaban
> del tipo de otra cosa. Hoy el catálogo tiene **27 tipos**, con **27 formularios**, uno por tipo.
> La correspondencia entre las 18 familias y los 27 tipos **está escrita y se comprueba**, no se
> supone: vive en `scripts/catalogo_tipos.py`, con `comprobar()`, que falla si dos familias
> comparten tipo o si un tipo se queda sin radio de geofencing.
>
> ```bash
> python -c "import sys;sys.path.insert(0,'scripts');import catalogo_tipos as C;print(len(C.FAMILIAS),'familias |',len(C.TIPOS_ACTIVO),'tipos')"
> ```

### De dónde salen los 355, escrito

La columna `CANT.` suma **508** sobre los 24 tipos. Los 355 son **solo las filas cuya unidad es
`Und`**:

```
54 + 26 + 11 + 19 + 4 + 4 + 4 + 4 + 16 + 4 + 142 + 12 + 12 + 7 + 2 + 2 + 29 + 3  =  355
```

Fuera quedan, y no son activos contables: fibra troncal (137 **km**), antivirus, licencias, radios y
certificados SSL (1 **Glb** cada uno) e internet (12 **Mes**). **508 − 355 = 153**, que es la suma
de esos seis.

De los 355 cuelgan las 1.916 órdenes anuales y la cuota de Drive. Ahora la aritmética está escrita y
es verificable.

**La cifra de cuota que circulaba estaba mal atribuida.** `scripts/capacidad.py` calcula cuatro
escenarios —34, 150, 355 y 500 activos— y los **4,1 años** son los del corredor completo de 500. Con
los 355 de este maestro la cuota da **5,7 años**, frente a los 5 de retención exigida: alcanza y no
sobra nada.

### Cuatro tipos de mantenimiento, no uno

| `TIPO MTTO.` | Tipos | Ejemplos |
|---|---|---|
| Preventivo | 19 | SOS, CCTV, fibra, peajes, básculas |
| **Admin** | 3 | Antivirus, licencias, certificados SSL |
| **Correctivo** | 1 | Computadores — periodicidad «A demanda» |
| **Servicio** | 1 | Internet ISP — monitoreo de SLA |

**Cinco de los 24 tipos no son cosas que se visitan.** Renovar un certificado SSL es una fecha en un
portal; auditar licencias es una revisión en un navegador; monitorear el SLA del ISP es leer un NMS.
Ninguno tiene coordenada.

Todo el diseño —RG-01 geofencing, cadena de evidencia, la excepción manual por GPS deficiente, firma
en sitio— asume desplazamiento. **Para esos cinco no aplica**, y hay que decidir si se les da un
camino sin evidencia de ubicación o si salen del alcance.

**Y «A demanda» no es una periodicidad: es la ausencia de una.** `PLA_PlanMantenimiento` no puede
programar los 29 portátiles: solo existen cuando se rompen.

### Doce roles, ya escritos

La columna `PERSONAL` asigna un rol a cada una de las 24 tareas:

```
Técnico ITS · Técnico Alturas · Técnico Fibra · Técnico Peaje · Ayudante
Ing. ITS · Ing. Redes · Ing. Soporte · Ing. TI · Aux. TI · Especialista · Proveedor
```

**Esto pesa más que el dato de GIMAN de la sección 4.** Que la herramienta de referencia no modelara
certificaciones sugería aplazarlo; que el plan del Sisga **ya asigne un rol por tarea** lo vuelve un
dato existente, no una idea.

Y abarata la solución: `ROL_Roles` más `TAR_Tareas.RolRequeridoID` y `USR_Usuarios.RolID`. Una tabla
y dos referencias, porque el dato ya está en la columna. Lo que sigue siendo Fase 2 es lo
**múltiple** —alguien con alturas *y* electricista, una tarea que exija técnico *más* SISO, y las
vigencias—, que sí es una relación de muchos a muchos.

**`Proveedor` no es un rol:** son dos tareas —impresoras en renting y radios— que ejecuta un tercero
que no es usuario de la aplicación.

---

## 3. La manta, que hasta ahora era una palabra

`PROPUESTA - PLAN MTTO DC 2016.xlsx`, hoja `SEMANA 1 AL 5 DE FEBRERO`.

```
                                 BQ   QB   BV    V
PRUEBA SEMANAL POSTES SOS         X         X    X
PRUEBA SEMANAL RADIO-COMUNICAC.   X    X    X
VERIFICACIÓN SEMANAL MÁSCARAS     X         X
MANTENIMIENTO TRIMESTRAL …             X
PRUEBA MENSUAL CON INTERVENTORÍA  X         X    X
───────────────────────────────────────────────────
TAREAS EJECUTADAS                 5   10    5    2   = 22
TAREAS NO EJECUTADAS              1    1    0    0   =  2
                                83%  91%  100% 100%
```

**Tareas en filas, sectores en columnas, y abajo planeadas contra ejecutadas.** Eso es la manta, y
ese porcentaje es el indicador que se reporta.

### Tres cosas que cambian el modelo

**Un tipo de equipo tiene varias tareas, y ahora está probado.** En la hoja `MANTENIMIENTO FEBRERO`,
C78:C80, el poste SOS aparece con prueba **semanal**, prueba **mensual con interventoría** y
mantenimiento **trimestral**. `PMG 2016` C83 añade una cuarta, «prueba mensual antes de
interventoría». El maestro ITS listaba una sola tarea por tipo, y sobre esa simplificación se
construyó `ACT_Activos.FrecuenciaID`. Confirma la sección 3 de `MODELO_EVOLUCION_FASE_2.md`: la
periodicidad es de la tarea, no del activo.

*La rejilla de arriba es de `SEMANA 1 AL 5 DE FEBRERO`, donde el SOS solo aparece con dos de sus
tareas. Las tres juntas están en `MANTENIMIENTO FEBRERO`.*

**Hay tareas con la interventoría dentro.** `PRUEBA MENSUAL CON INTERVENTORÍA` no es una tarea
normal: alguien externo asiste y firma. El modelo tiene `FIR_Firmas`, pero no sabe que una tarea
pueda exigir una firma de tercero.

**El cumplimiento es una resta, no un dato.** Planeadas menos ejecutadas. Con
`PLA_PlanMantenimiento` y `OT_OrdenesTrabajo` esa cifra **sale sola**, sin que nadie la teclee — y
hoy se teclea. Es el argumento de venta más fuerte que tiene este sistema y no estaba escrito en
ninguna parte.

---

## 3. El flujo de correctivo, que el modelo no tiene

`2-MANTENIMIENTO.pdf` §6. Es la parte más útil de los siete documentos, porque el correctivo es
justo donde nuestro modelo está en blanco.

### La cadena completa

```
Aviso            teléfono · web · correo          ← los tres literales del PDF §6.1.3
   ↓
Ticket           número que se entrega a quien reporta, y le sirve para consultar estado
   ↓
Tipología        Incidencia · Consulta · Petición
Criticidad       Total/Crítica · Parcial grave · Parcial leve
   ↓
Nivel            N1 técnico en campo · N2 especialista · N3 taller o fabricante
   ↓
Reparación       cambiar el elemento, nunca repararlo en sitio
   ↓
Parte de trabajo elemento reparado · hora de puesta en marcha · observaciones
```

### La criticidad se define por porcentaje de servicio, no por opinión

| Nivel | Definición | Respuesta | Resolución |
|---|---|---|---|
| Total / Crítica | 75–100 % de la instalación en avería | **2 h** | **4 h** |
| Parcial grave | 25–75 % | **4 h** | **12 h** |
| Parcial leve | 25 % o menos | **12 h** | **48 h** |

Y las dos definiciones que hacen medible el SLA:

- **Tiempo de respuesta:** desde que se notifica hasta que **empiezan a trabajar** en la resolución.
- **Tiempo de resolución:** desde que se informa hasta que está resuelta **y el cliente informado**.
- **Reloj parado:** el tiempo bloqueado por terceros o fuerza mayor no cuenta.

Esa última es la que nadie modela y siempre hace falta. Sin ella, cualquier SLA se incumple por
esperar un repuesto.

### Qué le falta al modelo para esto

`OT_OrdenesTrabajo` no tiene criticidad, ni hora de aviso, ni hora de inicio de trabajos, ni reloj
parado. Lo que tiene es `FechaProgramada` y `FechaCierre`, y **eso no es ni siquiera una duración**:
es adherencia al cronograma, si se cerró antes o después de lo previsto. **No existe fecha de
creación.** Para una preventiva basta; para una correctiva falta el dato de partida, porque una
avería no se programa: ocurre.

**Lo que describe operación encaja, con un canal más que el PDF no nombra:** el operador del centro
de control recibe la llamada —«no funciona el poste 3»—, **lo valida contra el SCADA** y lanza la
correctiva. El PDF habla de «la herramienta de monitorización» y **no menciona SCADA en sus 82
páginas**: ese canal es del Sisga, no de la fuente. Lo que sí es literal es que **solo operadores
autorizados** pueden dar el aviso, «para evitar notificar incidencias a través de terceras
personas».

---

## 4. GIMAN: el sistema que estamos replicando

`2-MANTENIMIENTO.pdf` §11. ETRA describe su herramienta **GIMAN**, un GMAO con interfaz **web y
Android**. Conviene mirarlo de frente: **el SGMC es un GIMAN pobre montado sobre AppSheet.**

Eso no es malo. Es útil, porque da un mapa de qué falta y en qué orden.

| Módulo GIMAN | En el SGMC |
|---|---|
| Mapa con código de colores por estado | Parcial. AppSheet lo da |
| Gestión de inventario | **Sí** — `ACT_Activos`, `TIP_TiposActivo` |
| Gestión de recursos | Parcial — `USR_Usuarios`, `ASG_AsignacionZona` |
| Mantenimiento preventivo | Parcial — falta la capa de tareas |
| Mantenimiento correctivo | **No** — sin criticidad, sin niveles, sin SLA |
| Almacén y existencias | **No** |
| SAT | **No** |
| Gestión documental | Parcial — `FOT_Fotografias` |
| Flotas de vehículos | No, y es opcional también en GIMAN |

### Lo que GIMAN hace y confirma decisiones nuestras

**Atributos por tipo de elemento.** GIMAN deja definir atributos adicionales por tipo —código,
dimensiones, color— sin tocar el esquema. Es el patrón que resuelve el problema de que un poste SOS
y un servidor no comparten propiedades. **En AppSheet sobre Sheets no se puede hacer**: no hay
esquema dinámico. Se paga con columnas vacías o con tablas por familia. Merece estar escrito como
limitación, no descubrirse en producción.

**Generación programada de tareas.** Se configura fecha de inicio y periodicidad, el sistema genera
las tareas solas, **y hay que activarlas antes de que sean ejecutables**. Ese paso intermedio es
inteligente: separa lo generado de lo comprometido, y deja reprogramar sin borrar.

Y aquí está la limitación de fondo, que ya conocíamos y ahora tiene consecuencia: **AppSheet gratuito
no ejecuta bots programados**. La generación automática que GIMAN da por sentada, nosotros no la
tenemos. Por eso las órdenes se crean a mano o por carga, y por eso la creación masiva es el
problema de usabilidad que usted señaló.

**Jerarquía de recursos.** Técnico → Supervisor/Capataz → Cuadrilla. Nuestro `ASG_AsignacionZona`
asigna técnico a zona, sin brigada intermedia.

### Y una cosa que GIMAN **no** tiene

El técnico en GIMAN se registra con **nombre, identificador y empresa**. Nada más. **No hay
certificaciones, ni especialidades, ni vigencias.**

Es un dato en contra de la propuesta de perfiles —electricista, alturas, electrónico, ayudante,
SISO— que usted planteó. No la invalida: un GMAO genérico de 2017 no es la vara. Pero conviene
saber que la herramienta de referencia resolvió la asignación **por zona y por brigada**, no por
certificación, y aun así funcionó.

Refuerza dejarlo en Fase 2.

---

## 5. Qué confirma y qué contradice nuestro modelo

### Confirma

| Decisión nuestra | Qué la respalda |
|---|---|
| Capa `TAR_Tareas` entre tipo y trabajo | GIMAN §11.1.5.1: el tipo de tarea se define **sobre el tipo de elemento** |
| Retirar `ACT_Activos.FrecuenciaID` | La manta: el SOS tiene tarea semanal, mensual y trimestral |
| Estado de alta/baja en el activo | GIMAN §11.1.3.1 lo lleva como campo del elemento |
| Fotografías con coordenada como evidencia | Cliente Android de GIMAN, para «introducir información en tiempo real» |
| Histórico que no se borra | «Seguimiento y tratamiento estadístico de averías» |

### Contradice o deja corto

| Hueco | Dónde duele |
|---|---|
| Sin criticidad ni SLA en la orden | Es lo que mide la interventoría por disponibilidad |
| Sin niveles N1/N2/N3 ni escalado | Una orden que el técnico no resuelve no tiene a dónde ir |
| Sin reloj parado | Cualquier espera de repuesto cuenta como incumplimiento |
| Sin almacén ni repuestos | El informe mensual pide «Repuestos y Herramientas» |
| Sin firma de tercero en la tarea | `PRUEBA MENSUAL CON INTERVENTORÍA` la exige |
| Sin brigada entre técnico y zona | GIMAN §11.1.4.3 |

**Ninguno de los seis bloquea la Fase B.** Todos son de correctivo o de recurso, y la Fase B es
cableado de referencias sobre el preventivo. Pero los seis son columnas, y **añadir columnas después
de producción es el problema que usted pidió evitar**.

---

## 6. Lo que sigue faltando, y no está en ningún documento

Estas no salen de leer más. Salen de preguntar en operación:

1. **¿El Sisga tiene SLA contractuales propios?** Los de ETRA son de otro corredor. Si el Sisga
   tiene los suyos, son otros números; si no tiene, hay que decidir si el sistema los mide igual.
2. **¿Quién puede dar el aviso de una correctiva?** ETRA restringe a operadores autorizados. En el
   Sisga, ¿el operador de turno, el supervisor, cualquiera con la app?
3. **¿Existe almacén de repuestos gestionado**, o los repuestos se anotan en texto libre?
4. **Las 600 cajas de fibra**: ¿hay inventario o hay que levantarlo?
5. **¿Cuántas estructuras** —puentes, viaductos— tienen paso de fibra?
6. **El inventario real del Sisga.** Trabajamos con 355 activos de un maestro que usted describió
   como «muy similar» al del Sisga, no el del Sisga. **Es el vacío más grande que queda.**

La 6 es la que más pesa: todo el dimensionamiento —1.916 órdenes al año, la cuota de 15 GB que da
5,7— está calculado sobre un inventario que no es el de este corredor.

**Y la plantilla no responde la pregunta 6.** `ACT_Activos` tiene **368 filas**, de las que **334
son sintéticas** y lo dicen de sí mismas —`ACTIVO SINTETICO DE PRUEBA - NO ES INVENTARIO REAL` en
`Observaciones`—; las otras 34 son el juego de arranque. Llevan los códigos de este maestro y sirven
para ejercitar el sistema; no para saber cuántos equipos hay ni dónde están.

**Y ya no llevan ni siquiera una coordenada aproximada.** `ACT_Activos.Ubicacion_LatLong` está
**vacía en las 368**: las coordenadas interpoladas sobre el corredor que hubo hasta el 2026-08-10 se
perdieron al renombrar la columna, y tampoco servían, porque ninguna era el sitio real del equipo.
Lo mismo con la referencia vial: `PK` está poblado en las 368 y **`PR` y `TramoINVIAS` están vacíos
en las 368**. Las tres cosas se cuentan contra el archivo:

```bash
python - <<'EOF'
import openpyxl
ws = openpyxl.load_workbook('BD/Modelo_Datos_PLANTILLA.xlsx', data_only=True)['ACT_Activos']
h = [c.value for c in ws[1]]
f = [dict(zip(h, r)) for r in ws.iter_rows(min_row=2, values_only=True)]
print('filas', len(f))
print('sinteticos', sum(1 for r in f if 'SINTETICO' in str(r['Observaciones'] or '')))
for c in ('Ubicacion_LatLong', 'PK', 'PR', 'TramoINVIAS'):
    print(c, 'con valor:', sum(1 for r in f if r[c] not in (None, '')))
EOF
```

---

*Alimenta `MODELO_EVOLUCION_FASE_2.md`. Ninguna pieza de aquí es ejecutable hasta que tenga su*
*`ESPEC`, su `PRUEBA` y el veredicto del arquitecto.*
