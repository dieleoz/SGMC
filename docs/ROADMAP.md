# ROADMAP de implementación — SGMC

**Proyecto:** Sistema de Gestión de Mantenimiento en Campo
**Cliente:** Concesión Transversal del Sisga S.A.S.

> ## Para qué sirve este documento, y para qué no
>
> **Este documento decide el ORDEN de implementación**: qué va antes que qué, y por qué ese orden y
> no otro. Es lo que no cabe en un tablero de estado y lo que más caro sale improvisar.
>
> | No busque aquí | Búsquelo en |
> |---|---|
> | En qué punto va cada frente y qué lo bloquea | [`ESTADO.md`](../ESTADO.md) |
> | Qué es el sistema hoy: modelo, decisiones de diseño, límites | [`SISTEMA.md`](SISTEMA.md) |
> | Qué está cableado en la aplicación | `python scripts/auditar_cableado.py`. **Ningún documento lo sabe** |
> | Qué hacer a mano en el editor, paso a paso | [`LO_QUE_SE_HACE_A_MANO.md`](LO_QUE_SE_HACE_A_MANO.md) |
> | Qué hace el sistema y para quién | [`FUNCIONAL_SGMC.md`](FUNCIONAL_SGMC.md) |
> | Cómo se mantiene el corredor de verdad | [`CONTEXTO_OPERACION.md`](CONTEXTO_OPERACION.md) |
> | Quién hace qué | [`INDICACIONES_POR_ROL.md`](INDICACIONES_POR_ROL.md) |
>
> **Cómo cambió este documento lo dice `git log -- docs/ROADMAP.md`.** Cada afirmación de estado que
> este roadmap llegó a hacer sobre el cableado resultó falsa el día siguiente, y por eso ya no hace
> ninguna: lo que aquí se decide es la secuencia. La factura de haberlo hecho al revés está en §10.

---

## 1. Principio de este roadmap

**Hay dos archivos contra los que verificar, no uno.** Los datos, en `BD/*.xlsx` y en el Sheets de
producción. Y el comportamiento de la plataforma, en la documentación oficial de AppSheet, recogido
en `BASE_CONOCIMIENTO_APPSHEET.md` con su cita y su URL. Durante cinco rondas de revisión solo se
verificaba lo primero.

Ninguna fase se declara cerrada sin un **criterio de cierre verificable**: un hecho que otra
persona pueda comprobar leyendo el archivo o el sistema, no un reporte de avance.

La versión anterior de este documento no tenía criterios de cierre. Por eso pudo marcar como
completadas fases que dejaron cuatro tablas vacías y el control GPS inoperante.

---

## 2. Orden de implementación

**No se ordena por importancia: se ordena por lo que cuesta hacerlo tarde.**

Es el riesgo que fijó operación — «que no falten campos, o cambiar la base y la aplicación después
de salir a producción, es un problema». Una implementación progresiva **agrava** ese riesgo si se
ordena mal: si el piloto sale con medio esquema, la otra mitad deja de ser una columna y pasa a ser
una migración.

De ahí salen tres clases, y el orden entre ellas no es negociable:

| Clase | Cuándo | Por qué |
|---|---|---|
| **Esquema** — tablas y columnas | **Antes del piloto, todo junto** | `MAN_Mantenimientos` está **vacía**, y con ella las demás transaccionales. Añadir hoy cuesta cero; después cuesta migración |
| **Datos** — inventario, coordenadas | En medio, con las referencias ya tipadas | Así AppSheet valida cada fila al cargarla, gratis |
| **Comportamiento** — reglas, permisos | Después, en cualquier orden | No tocan datos. Se endurece con el sistema andando |

### La secuencia

| # | Paso | Contenido | Depende de |
|---|---|---|---|
| **0** | **Cablear la aplicación entera** | **Las 39 referencias**, con `IsPartOf` en las cuatro que lo llevan; **las 23 reglas**; los dos filtros de seguridad; las cuatro marcas de tiempo como `ChangeTimestamp`; retirar `Deletes` en `OT_OrdenesTrabajo` y `MAN_Mantenimientos`; y correr `PRUEBA-003` | **En curso, y su estado no se lee aquí:** `python scripts/auditar_cableado.py`. Ficha por tabla en [`MANUAL_DESPLIEGUE.md`](MANUAL_DESPLIEGUE.md); expresión completa en [`sdd/RECONSTRUCCION_EXPRESIONES.md`](sdd/RECONSTRUCCION_EXPRESIONES.md) |
| **1** | **Esquema completo** | `TAR_Tareas` · poblar `ROL_Roles` con los 12 · `ETR_Estructuras`, que es lo que queda de la jerarquía de ubicación · columnas de tiempo en la orden · retirar `ACT.FrecuenciaID` y `TIP.FormularioID`, **que `verificar_documentos.py` avisa como descartadas y vivas con fecha tope 2026-08-31** | `ESPEC-003`, **bloqueada** desde el 2026-08-09 por decisiones de operación y de plan de licenciamiento, no del editor (§3.2) |
| **2** | **Carga del inventario real** | Los 355 con identidad, serie y ubicación. **Los que hay hoy son sintéticos** y lo dicen de sí mismos. Aquí entran también las cuatro columnas que existen y están vacías en las 368: `Ubicacion_LatLong`, `PR`, `TramoINVIAS` y `SedeID` | Paso 1, y que operación confirme que 355 son los de este corredor |
| **3** | **Reglas de integridad** | Imponer `QuienCambia` · estado de rechazo · valores de `TipoFirma` | Paso 1 |
| **4** | **Piloto de campo** | El levantamiento de coordenadas **como primera orden de trabajo** | Pasos 2 y 3 |
| **5** | **Correctivo** | Criticidad · pausas · escalado N1/N2/N3 | Decisión de alcance |
| **6** | **Fase 2 de modelo** | Certificaciones múltiples · mediciones de hilo · estructuras · **tramos en túnel** · almacén | Piloto en marcha |

**El paso 1 es el único que no admite trocearse.** Los demás sí.

### Lo que NO está en esta secuencia

No es «más adelante»: es **no en el plan actual**. Ponerlo en una fase futura daría la impresión de
que llega solo con tiempo, y no llega — llega con la decisión de licenciamiento **D-B**.

- Generación automática de las órdenes del mes
- Aviso al supervisor de que hay trabajo por recibir
- Integración con el SCADA para abrir correctivas
- Cualquier prueba automatizada, por falta de API REST

---

## 2.1 La ventana barata, y por qué es lo más urgente que hay

**Este documento ordena por lo que cuesta hacerlo tarde. Esto es lo único que ahora mismo cuesta
más cada día que pasa, sin que nada lo anuncie.**

**Ocho tablas están hoy en CERO filas.** Y esa vacuidad no es un estado neutro, aunque se lea como
«todavía no empezado»: es lo único que hace que corregir un tipo o una clave cueste **un clic**. Con
una sola fila dentro, cada corrección pasa a ser una **migración**. Entre los dos precios no hay
ningún evento: ni un error, ni un aviso. **El precio sube solo.**

**Y sube en un solo sentido.** Las ocho son **transaccionales**, así que el primer registro cierra la
ventana **para siempre**: una vez que entren órdenes y mantenimientos no vuelven a estar vacías
nunca. No es una ventana que se estreche; es una que desaparece.

Las ocho son `VOLCADO_CIEGO_A` en `scripts/lectura_de_vuelta.py`, y coinciden exactamente con
`CLAVE_GENERADA`. La cuenta no se cita, se vuelca:

```bash
python -c "import sys;sys.path.insert(0,'scripts');from inferencia import clasificar;from lectura_de_vuelta import VOLCADO_CIEGO_A;from modelo_objetivo import REGLAS;print(len(VOLCADO_CIEGO_A),'tablas |',sum(1 for t,c,m in clasificar()['a mano'] if t in VOLCADO_CIEGO_A),'tipos a cotejar |',sum(1 for r in REGLAS if r['tipo']=='App formula' and r.get('columna')=='(tabla)'),'columnas virtuales')"
```

Hoy: **8 tablas · 53 tipos · 3 columnas virtuales** (de las tres, solo dos son `Etiqueta`
— la tercera es `EstaVencida`, `RG-37`, que no es `Label` y no entra en `ENCARGO_VENTANA.md` Paso 1;
ver `ESPEC-006`/`ORDEN-006`).

**Lo que cabe dentro de la ventana está reunido en [`ENCARGO_VENTANA.md`](ENCARGO_VENTANA.md)**,
generado por `scripts/generar_encargo_ventana.py`. Son dos cosas y nada más: las **2 columnas
virtuales `Etiqueta`** que deja pendientes `ESPEC-005`, y el **cotejo de los 53 tipos** de esas ocho
tablas —mirar, no cambiar, y anotar lo que se vea aunque coincida, porque la API devuelve filas y no
esquema, y esa anotación es la única evidencia que va a existir—.

> **Ese `53` es el TAMAÑO del trabajo, no lo que queda.** Sale de `inferencia.clasificar()`, que
> responde *«qué columnas necesitan mano»* y **no** *«en cuáles ya pasó alguien»*: la API devuelve
> filas, no esquema, así que **no existe comando que reste lo hecho**. Y se hizo mucho: el
> 2026-08-11 una sesión de editor recorrió las ocho tablas corrigiendo tipos (`docs/sdd/ACTA-004`,
> `ACTA-006`). Leer este número como pendiente ya indujo un informe erróneo. La única evidencia de
> qué se tocó son las actas.

**Las 2 columnas virtuales ya están creadas**, con `Show?` y `Label` puestos, verificado a ojo el
2026-08-11. Lo que sigue abierto de la ventana es el cotejo de tipos: el guion paso a paso está en
[`LO_QUE_SE_HACE_A_MANO.md`](LO_QUE_SE_HACE_A_MANO.md).

**Y lo que NO cabe, con su motivo, que es la mitad que impide que la lista se reordene sola:**

| Queda fuera | Por qué |
|---|---|
| `UNF_UnidadesFuncionales` y `USR_Usuarios` | **Tienen filas.** Su ventana se cerró hace tiempo, su precio ya está pagado y no vuelve a subir: pueden esperar |
| Los 3 bots (`RG-06`, `RG-07`, `RG-10`) más `RG-38` (acción) | **No dependen de la ventana.** Se configuran igual con las tablas llenas. `RG-08`/`RG-12` se retiraron (`ESPEC-006`/`ORDEN-006`); `RG-37` es columna virtual, ya cubierta en la fila de arriba |
| `RG-04` y `RG-05`, los `Security Filter` | Van **los últimos**. Al ponerlos, la API deja de devolver las filas de esa tabla y ni `auditar_cableado.py` ni `instantanea.py` pueden volver a mirarla. Apagan los instrumentos |
| `RG-03` | Ya **entra**: `ESPEC-004`/`ORDEN-004` la desbloqueó (2026-08-11). `RG-02` y `RG-19` se retiraron del modelo (`RG-02` usaba una función que no existe en AppSheet) |

**La prohibición central del encargo es poblar cualquiera de las ocho**, y no es una precaución
genérica: es **justo el acto** que acaba con el motivo por el que el encargo existe. Quien la cierra
casi nunca cree estar decidiendo nada —siembra un fixture, crea una orden para ver si el bot
dispara—, y ese es exactamente el riesgo. La regla general está en [`CLAUDE.md`](../CLAUDE.md) §7.17.

> **Esto no reordena las fases: se mete delante de todas.** El paso 1 de §2 —esquema completo— sigue
> siendo el que no admite trocearse, y sigue viviendo dentro de esta misma ventana, con el mismo
> motivo: `MAN_Mantenimientos` está vacía y añadir hoy cuesta cero.

---

## 3. Las fases y su criterio de cierre

**Una fase no se cierra por reporte de avance: se cierra por un hecho que otra persona puede
comprobar leyendo un archivo o el sistema.** Eso es lo que fija esta tabla. **En qué punto va cada
fase lo dice [`ESTADO.md`](../ESTADO.md)**, y ninguna casilla de aquí lo afirma.

| Fase | Depende de | Criterio de cierre |
|---|---|---|
| Sprint 0. Definición funcional | — | Los catorce supuestos adoptados por escrito en [`ALCANCE_Y_SUPUESTOS_SGMC.md`](ALCANCE_Y_SUPUESTOS_SGMC.md), con su estado de cierre. **Se cierra por supuestos: no se espera respuesta del funcional** |
| Fase 0.5. Reconciliación de modelos | — | `scripts/modelo_objetivo.py` es la fuente única y los documentos se generan de él. Lo que dejó decidido, en §4.5 |
| **Fase A. La hoja** | Fase 0.5 | `python scripts/verificar_faseA.py "BD/Modelo_Datos_PLANTILLA.xlsx"` en 0 fallos |
| Reconstrucción de la aplicación | Fase A | Las 28 tablas dadas de alta sobre la hoja vigente, y ninguna de más. `python scripts/verificar_app.py` |
| **Fase B. Las referencias** | Reconstrucción | `python scripts/auditar_cableado.py` en **0 correcciones**, leyendo su recuento entero y no la primera línea. Las que apuntan a una tabla vacía **el auditor no las puede juzgar**: se miran en el editor una a una y se registran en `CONFIRMADAS_A_OJO` |
| **Fase C. Las reglas** | Fase B | Todas las reglas puestas, los dos `Security Filter`, las cuatro marcas de tiempo, `Deletes` retirado y `PRUEBA-003` pasada. **`RG-16` no debe cambiar ninguna celda de `ACT_Activos`** |
| Fase 1. Datos maestros | D-01 y D-09 | Coordenadas **medidas en campo**, sedes realineadas, bancos de preguntas cerrados. Detalle en §5 |
| Fase 2. Configuración de interfaz | Fase 1, y declarar vistas | Reportes y pantallas construidos. **Antes hay que declarar la interfaz en el modelo**: hoy no tiene vistas, ni acciones, ni slices |
| Fase 3. Prueba controlada | Fase 2 | Registros reales en `MAN_Mantenimientos` y en las tablas de evidencia, verificados leyendo el archivo |
| Fase 4. Piloto de campo | Fase 3 | 10 técnicos operando una semana, con registros sincronizados desde el corredor |
| Fase 5. Producción y evolución | Fase 4 | Ninguna pregunta marcada como borrador, integraciones y respaldo automático |

**La Fase C va en dos tandas: primero las reglas que no escriben, después las que sí.** Una `App
formula` o un bot escriben en la hoja, y eso no se revierte cambiando un desplegable — la red es
`python scripts/instantanea.py`, que compara dos fotografías celda a celda. La expresión de cada
regla está en [`sdd/RECONSTRUCCION_EXPRESIONES.md`](sdd/RECONSTRUCCION_EXPRESIONES.md); su tabla, su
propiedad y **la cadena de referencias que atraviesa** en
[`PROMPT_EXPRESIONES.md`](PROMPT_EXPRESIONES.md) —una expresión con puntos no falla por estar mal
escrita, falla porque un salto no está cableado—; y **dónde está cada control en pantalla**, en
`python scripts/navegacion_editor.py`, porque `Required_If` se llama `Require?` y no es una casilla.

**No hay fechas.** El cronograma depende de dos tareas que son trabajo del cliente y cuya duración
solo el equipo de la Concesión puede estimar: el levantamiento de las coordenadas reales (decisión
D-01) y la redacción de los bancos de preguntas (decisión D-09). Las fechas se fijan en el acta de
la mesa de trabajo, no antes.

---

## 3.1 Dos consecuencias de orden que no salen en ningún tablero

**Qué está construido lo dice [`ESTADO.md`](../ESTADO.md) §1; qué es el sistema,
[`SISTEMA.md`](SISTEMA.md).** Lo que sigue está aquí
porque cambia **el orden**, y en un tablero de estado no cabe.

### Un cambio que no toca un byte de datos es un cambio que se puede deshacer

Una columna **virtual** no existe en el Sheets: AppSheet la calcula en cada sincronización y no la
escribe. Una `App formula` sobre una columna **real** sí escribe, y lo hace sobre todas las filas
antes de que nadie pueda revisarlo. Por eso, cuando las dos formas resuelven el mismo problema,
**va primero la virtual**: se prueba sin arriesgar producción, y deshacerla es borrarla.

Se comprueba comparando el `.xlsx` antes y después del cambio, pestaña por pestaña y celda por
celda —el binario difiere en un byte de metadato del `.zip`, así que `git diff --stat` lo marca
como cambiado y no responde la pregunta que importa—:

```bash
python -c "import subprocess,io,openpyxl,sys;ref=sys.argv[1];a=subprocess.run(['git','show',ref+':BD/Modelo_Datos_PLANTILLA.xlsx'],capture_output=True).stdout;A=openpyxl.load_workbook(io.BytesIO(a),read_only=True,data_only=True);B=openpyxl.load_workbook('BD/Modelo_Datos_PLANTILLA.xlsx',read_only=True,data_only=True);print(len(A.sheetnames),'pestanas | mismos nombres:',A.sheetnames==B.sheetnames,'|',sum(1 for n in A.sheetnames if [tuple(r) for r in A[n].iter_rows(values_only=True)]!=[tuple(r) for r in B[n].iter_rows(values_only=True)]),'con contenido distinto')" <commit-anterior>
```

### Meter una tabla en `CLAVE_GENERADA` le quita una comprobación

`F-11` de `verificar_faseA.py` contrasta las listas de claves contra la hoja, y **exime a
`CLAVE_GENERADA` a propósito**: su clave será una cadena aleatoria en cuanto la aplicación cree la
primera fila, así que mirarla en el `.xlsx` no dice nada. La consecuencia es que **el verde de
`verificar_faseA.py` no dice nada de esas tablas**, y que su clave esté bien puesta **solo se ve en
el editor**. Es correcto, y es una comprobación menos: por eso el cotejo en el editor no es opcional
sino la única evidencia que va a existir, y por eso está en el encargo de la ventana (§2.1).

---

## 3.2 Lo que espera dictamen del arquitecto

**Nada se aplica hasta que el arquitecto lo tumbe o lo deje pasar**, y ese ciclo termina en algo:
una especificación entra, la tumban, se rehace contra el archivo y pasa. **El estado de cada una,
con su motivo, está en [`../MAP.md`](../MAP.md) §3 y en [`ESTADO.md`](../ESTADO.md) §0.** Lo que el
orden necesita saber es qué queda inerte mientras tanto:

**El 2026-08-11 fue el día que más de estas se movieron.** Cinco pasaron el gate ese día; de las
cuatro que quedaron aplicadas al modelo, tres se cablearon además en el editor la misma sesión
([`ACTA-009`](sdd/ACTA-009-cableado-editor.md), [`ACTA-011`](sdd/ACTA-011-bloqueo-vivo-y-here-sin-senal.md)).
Una sigue bloqueada desde antes y una está escrita, sin pasar todavía por el arquitecto —el molde
sigue vivo para la próxima especificación que quede en espera—:

| Espera | Deja sin poder ponerse | Estado |
|---|---|---|
| [`ESPEC-003`](sdd/ESPEC-003-modelo-de-dominio.md) · modelo de dominio (`TAR_Tareas`, `ETR_Estructuras`…) | El paso 1, esquema completo (§2) | **BLOQUEADA** por el arquitecto desde el 2026-08-09, con 14 condiciones sin resolver. Revisado el 2026-08-11: sus condiciones son de **operación o de plan de licenciamiento**, no de lo que un ejecutor pueda decidir en el editor, así que no se destraba sin esas decisiones |
| [`ESPEC-004`](sdd/ESPEC-004-cierre-excepcion-manual.md) · cierre con excepción manual | `RG-02`, `RG-19` y `RG-03`. `RG-02` dependía de una función que **no existe en AppSheet** | **Aplicada y cableada** (`ORDEN-004`; `ACTA-009` el 2026-08-11): `RG-02`/`RG-19` retiradas del modelo, y la `App formula` que `RG-19` había dejado físicamente en la columna `CierreConExcepcion` —el defecto real que bloqueaba la casilla— ya está borrada en el editor |
| [`ESPEC-005`](sdd/ESPEC-005-clave-otid-planid.md) · separar clave de etiqueta legible | Creación de órdenes desde la app (§4.5) | **Aplicada al modelo y al editor**: `RG-35`/`RG-36`, las columnas virtuales `Etiqueta` de `OT_OrdenesTrabajo` y `PLA_PlanMantenimiento`, con `Show?` y `Label` puestos, confirmado a ojo en [`ACTA-010`](sdd/ACTA-010-cotejo-ocho-tablas.md) |
| [`ESPEC-006`](sdd/ESPEC-006-reemplazo-bots-programados.md) · reemplazo de los bots programados | `RG-08` y `RG-12`, que no corren en esta cuenta (§6) | **Aplicada y cableada** (`ORDEN-006`; `ACTA-009` el 2026-08-11): retiradas del modelo, sustituidas por `RG-37`/`RG-38`, las dos cableadas en el editor |
| [`ESPEC-007`](sdd/ESPEC-007-precision-gps-fotografias.md) · retirar `FOT_Fotografias.PrecisionGPS` | Nada del cableado la necesita: ninguna regla del modelo lee esa columna | **Aplicada** (`ORDEN-007`, 2026-08-11). Confirmada en el editor: `Initial value` vacío en `PrecisionGPS` — Rama A, la retirada fue limpia ([`ACTA-011`](sdd/ACTA-011-bloqueo-vivo-y-here-sin-senal.md)) |
| [`ESPEC-008`](sdd/ESPEC-008-proteger-ubicacion-fotografias.md) · proteger `Ubicacion_LatLong` de `FOT_Fotografias`/`NOV_Novedades` | El pin arrastrable sobre esas dos tablas | **Aplicada y cableada** (`ORDEN-008`, 2026-08-11: `RG-39`/`RG-40`) — **pero en revisión**: `HERE()` no mide y puede haber quitado también la captura manual, no solo el arrastre del pin; sin señal escribe `0,0`, medido. No se decide todavía; ver `ACTA-011` §2 y [`HALLAZGOS_ABIERTOS.md`](HALLAZGOS_ABIERTOS.md) |
| [`ESPEC-009`](sdd/ESPEC-009-proteger-identidad.md) · proteger la identidad (`USEREMAIL()` en cuatro columnas, dos `Ref`) | — | **Escrita** (2026-08-11), **pendiente del arquitecto**: no ha pasado dictamen todavía |

> ### Una regla puede estar puesta y no hacer nada
>
> Es lo que más veces ha fallado en este proyecto, y siempre en silencio: configurada, bien escrita,
> sin un solo error, y sin efecto. **Los tres motivos y cómo se caza cada uno están en
> [`CLAUDE.md`](../CLAUDE.md) §7.13.** Para el orden, lo que importa es la consecuencia: **«la puse»
> no es «hace algo»**, así que ninguna fase se cierra contando reglas configuradas.

---

## 4. Sprint 0 — Definición funcional (cerrado por supuestos)

El documento y su correo salieron al líder funcional y **no se reenvían**. Pero el proyecto dejó de
esperar su respuesta: las catorce decisiones se adoptaron como supuestos en
`ALCANCE_Y_SUPUESTOS_SGMC.md` y son vinculantes hasta que el campo las desmienta.

- [x] Enviar el documento al líder funcional
- [x] Adoptar los catorce supuestos y declararlos por escrito
- [ ] Contrastar la respuesta del funcional, cuando llegue, contra los supuestos adoptados

**Por qué cambió.** Un cuestionario en abstracto a quien no tiene todavía el modelo mental produce
silencio, y el sistema actual no permite formarse criterio: no hay nada que mirar. Es más rápido
construir completo, poblar con datos, entregar con manual, y corregir con lo que diga el campo.

---

## 4.4 Decisiones pendientes de Dirección

La propuesta de arquitectura enviada a Dirección pide tres decisiones. Las dos primeras condicionan
la salida a producción y ninguna es técnica. **El documento no está en el repositorio** —se recupera
con `git log --diff-filter=D --name-only -- 'entregables/*'`—, y lo que queda vivo son las tres
decisiones, que se piden aquí:

- **D-A. Propiedad del backend.** El documento y las fotografías pertenecen a una cuenta personal
  de Gmail. Las imágenes consumen su cuota de 15 GB, que con los 355 activos del Plan Maestro da
  **5,7 años** frente a los 5 de retención, y con el corredor completo de 500 se agota **en 4,1**.
  Sale de `python scripts/capacidad.py`.
- **D-B. Plan de licenciamiento.** En el plan gratuito los procesos programados no se ejecutan. Sin
  plan pagado no hay generación automática de órdenes ni notificaciones, que es lo que convierte el
  sistema en gestión y no en registro.
- **D-C. Definición contractual de disponibilidad.** Si el contrato o interventoría la definen de
  otra forma, esa prima sobre la propuesta.

---

## 4.5 Fase 0.5 — Reconciliación de modelos. CERRADA

**El Excel local y el Google Sheets llegaron a ser modelos distintos** —el Excel con las columnas de
GPS y sin el mapeo de formularios, producción al revés, y `CHK_Checklists` y `CHD_ChecklistDetalle`
divergentes—, porque dos personas editaban por separado y nadie lo sabía.

**No se cerró eligiendo uno de los dos**, que era lo que este documento proponía, sino **sacando la
verdad de los dos archivos**: la fuente única es `scripts/modelo_objetivo.py`, la hoja se genera de
él y los documentos también. **Un modelo declarado en código no puede divergir en silencio de otro,
porque solo hay uno** — y por eso esta fase no se reabre.

**Lo que dejó decidido:**

| Decisión | Cómo quedó |
|---|---|
| Columnas de GPS en `MAN_Mantenimientos` | `Coordenadas_Cierre_LatLong` como `LatLong` y `Precision_GPS` como `Number`. AppSheet las había inferido mal y cruzadas |
| `EOT_EstadosOrden` | Sus claves son el nombre del estado, no `1..7`. Un catálogo se diseña mirando los datos que va a resolver |
| `IsPartOf` sobre `MAN_Mantenimientos.OTID` | **Va sin él.** La ejecución es el registro histórico y sobrevive a su orden |
| Borrado del histórico | Se retira `Deletes` en `OT_OrdenesTrabajo` y `MAN_Mantenimientos` (RG-14 y RG-15). Un error se corrige con `Activo = FALSE` |
| Reportes históricos | RG-18: un histórico nunca filtra por el estado actual del activo, o al dar de baja uno desaparecen sus mantenimientos pasados |
| Creación de órdenes desde la app | **Aplicada al modelo y al editor** (2026-08-11, ver §3.2). El motivo del aplazamiento era que `OTID` hacía de clave y de etiqueta legible a la vez; `ESPEC-005` lo separó —clave con `UNIQUEID()`, columna `Etiqueta` aparte— y `RG-14` ya declara `Updates, Adds`. Mientras las órdenes reales se sigan creando en el Sheets en vez de en la app, siguen **saltándose todas las validaciones**: aceptable en el piloto por volumen, no como procedimiento |
| Quién edita el Sheets | **Sin resolver.** Sigue sin haber una regla escrita, y hay dos cuentas con permiso |

Las actas y especificaciones que produjeron esa tabla no están en el árbol de trabajo: describían
aplicaciones y hojas superadas, y **lo que dejaron decidido es la tabla de arriba**. El resto lo
guarda `git`, con la etiqueta `antes-de-la-limpieza-2026-08-10`.

**Y lo que esta fase no arregló, porque no era suyo:** el esquema de la aplicación. Reconciliar dos
modelos no repara una aplicación construida sobre el viejo — eso se resuelve reconstruyéndola.

---

## 5. Fase 1 — Datos maestros

Es la fase más larga y la que fija el cronograma. **Todo su contenido es trabajo de operación**,
y por eso no hay forma de adelantarlo desde el repositorio.

- [ ] **D-01.** Levantamiento en campo de las coordenadas reales y carga en `ACT_Activos.Ubicacion_LatLong`.
      **La columna está poblada en las 368 filas, con 368 valores distintos, y aun así D-01 sigue
      abierta**: cada punto se **deriva del `PK`** sobre el trazado en cada pasada del generador, y
      ninguno se midió en campo. `DISTANCE()` no da error ni compara contra blanco: compara contra un
      punto de la carretera que no es el equipo, y **rechaza el cierre legítimo** con 0,05 km de
      radio. **Que la celda tenga algo no es que el dato exista**, y esta es la partida donde más
      barato sale confundirlo
- [ ] Cargar `ACT_Activos.PR` y `ACT_Activos.TramoINVIAS`, vacías en las 368. **No se deducen del
      `PK`**: la conversión PK↔PR no es una fórmula sino una tabla de equivalencias que no existe, y
      el corredor tiene dos puntos distintos llamados `PR 0+000`
- [ ] Situar **las seis** sedes. Ojo con el reparto, porque no es el mismo número para cada columna:
      **`PK` y `Ubicacion_LatLong` faltan en las seis**; `UnidadFuncionalID`, `PR` y `TramoINVIAS`
      faltan en **cinco**, porque solo el peaje de Machetá los trae. Decir «cinco sedes» a secas ya
      indujo a un lector a reportar que a cinco les faltaba la coordenada. `SED_Sedes` tiene
      `UnidadFuncionalID`, `PR`, `TramoINVIAS`,
      `PK` y `Ubicacion_LatLong`, y solo el peaje de Machetá trae `UnidadFuncionalID`, `PR` y
      `TramoINVIAS`; **`PK` y `Ubicacion_LatLong` están vacías en las seis**. Y el de San Luis de
      Gaceno figura en el contrato como peaje nuevo, sin abscisa: está proyectado, no construido.
      **`verificar_datos.py` lo saca como aviso, no como fallo, y con fecha tope: el 2026-08-31 pasa
      a fallo.** Un aviso que no caduca deja de leerse
- [ ] Colgar de su sede el equipo bajo techo. `ACT_Activos.SedeID` existe, es opcional y **está
      vacía en las 368 filas**, así que los 7 servidores, los 29 portátiles, las 3 impresoras y el
      resto del equipo de interior no dicen dentro de qué edificación están. Mientras esté vacía
      `RG-34` no compara nada, y un servidor sigue localizándose por un punto de la carretera
- [ ] **D-09.** Validación de las **288 preguntas en borrador** de `FRM_Preguntas`, repartidas en 24
      de los 27 formularios. No están por escribir: están escritas y marcadas
      `[BORRADOR: validar con operacion]` en su ayuda, y el día que no aparezca ninguna el banco
      está cerrado. Las 45 de SOS, CCTV y PMV fijo ya estaban acordadas
- [ ] Poblar `ROL_Roles` con los doce oficios del Plan Maestro. **Es lo más barato que hay
      pendiente:** doce filas en una tabla que ya existe, sin tocar ninguna regla. Ojo: para que
      compren algo hace falta `USR_Usuarios.OficioID`, que no existe — ver `ESPEC-003` §5.4
- [ ] Asignar zona en `ASG_AsignacionZona` a los técnicos que no la tienen. Hay 4 asignaciones y 11
      usuarios: quien no tenga fila abre la aplicación y no ve nada
- [ ] Confirmar el umbral de GPS. La hoja dice 40 m en `PAR_Parametros`; la propuesta enviada decía
      50. Hay que quedarse con uno
- [x] **Encabezados sin codificación corrupta.** La hoja se genera del modelo, así que el mojibake
      que arrastraba la heredada desapareció con ella: ninguno de los 210 encabezados lo tiene
- [~] **Código QR: FUERA DE ALCANCE.** Primero tiene que funcionar el ciclo básico. El hallazgo se
      conserva porque es real: `ACT_Activos.CodigoQR` está poblado **solo en las filas del juego de
      arranque** y su valor es una copia de `CodigoActivo` salvo en una, donde `SERV-001` lleva
      `SVR-001`; y AppSheet lee códigos pero no
      los genera ni los imprime. **Consecuencia que se asume:** el activo se abre por lista y
      `MAN_Mantenimientos.OrigenApertura = Lista` deja de ser excepción. Si se retoma, falta decidir
      qué se codifica, quién genera las imágenes, en qué material se imprime, quién las instala y
      cómo se verifica que cada etiqueta quedó en su equipo
- [x] **Diccionario de datos regenerado.** `docs/bd.md` ya no se escribe: sale de
      `generar_diccionario_bd.py` leyendo la hoja
- [x] **`TIP_TiposActivo.FormularioID` mapeado en los 27 tipos**, sin una fila sin formulario. Y el
      modelo lo declara descartado: el formulario es de la tarea, no del tipo. Se retira en el paso 1
      del orden de implementación
- [x] **Checklist huérfano remediado.** `CHK_Checklists` cuelga hoy de `MantenimientoID`, no de la
      orden

**Cierra cuando:** ninguna fila de `ACT_Activos` se declara sintética en `Observaciones` —hoy lo
hacen **334 de las 368**— y su coordenada quedó **medida en campo**, no derivada del `PK`; las 288
preguntas en borrador están validadas; y un usuario de prueba ve activos al aplicar el filtro.

> **El criterio anterior de esta fase era «no tiene ninguna celda vacía y sus valores son todos
> distintos y están sobre el corredor», y hoy se cumple entero sin que la fase esté cerrada.** Es
> exactamente el defecto que este documento persigue: un criterio que un generador puede satisfacer
> solo. Una coordenada derivada del `PK` es no vacía, distinta de las demás y está sobre el corredor
> **por construcción**. Lo que hay que exigir es la procedencia del dato, no su forma.

---

## 6. Fase 2 — Configuración en AppSheet

Esta fase son dos bloques en este orden: reponer el **comportamiento** —las reglas, los filtros, las
marcas de tiempo—, y después la **interfaz**, que tiene un requisito previo que no es de
configuración sino de modelo. **Cuánto está puesto no lo declara este documento**, y ninguna versión
suya volverá a hacerlo: se pregunta con `python scripts/auditar_cableado.py`.

> ### Antes de las reglas van las referencias, y cuántas faltan no se lee aquí
>
> **Doce de las 23 reglas desreferencian** —`RG-01`, `RG-04`, `RG-05`, `RG-06`, `RG-09`,
> `RG-11`, `RG-16`, `RG-17`, `RG-34`, `RG-35`, `RG-36` y `RG-37`; la lista se saca buscando `].[` en
> las expresiones del modelo—, y cada una **falla o, peor, resuelve contra lo que no es** si la
> referencia de debajo está mal puesta. Y «mal puesta» no significa ausente: ha pasado que `ACT_Activos.TipoActivoID` apuntara
> a `SED_Sedes`, con lo que cada activo leía el checklist de una sede y `RG-01` fallaba con
> `Can't find column "RadioGeofencingKm" in table "SED_Sedes"` — un mensaje que invita a reescribir
> una expresión correcta para acomodarla a un cableado roto.
>
> **Ninguna regla se cablea hasta que el auditor salga con 0 correcciones**, y hay un resto que el
> auditor **no puede juzgar**: la columna virtual inversa vive en la tabla destino, y **seis
> referencias apuntan a tablas que están vacías**, así que de ellas no dice ni bien ni mal. Se abren
> en el editor una a una, o se siembra una fila en el destino y se vuelve a correr. **Confundir «no lo
> puedo ver» con «está bien» es como se llegó a las cuatro de arriba.**
>
> **Las seis, y las ocho tablas de movimiento enteras, ya se miraron una a una el 2026-08-11**
> ([`ACTA-010`](sdd/ACTA-010-cotejo-ocho-tablas.md)): las ocho salieron conformes, y de paso se
> confirmó que `MAN_Mantenimientos.OTID` es `Ref` y va **sin** `Is a part of`. **Mirado no es
> medido**: sigue sin haber comando que lo compruebe, y esa lectura visual se guarda con fecha
> porque caduca. Medirlas de verdad sigue costando lo mismo que cerrar la ventana barata: sembrar
> una fila en el destino.
>
> ```bash
> python scripts/auditar_cableado.py
> ```

Declarado en el modelo, con su expresión completa en
[`sdd/RECONSTRUCCION_EXPRESIONES.md`](sdd/RECONSTRUCCION_EXPRESIONES.md), y **sin poner**:

- [ ] **Terminar las referencias de `ACT_Activos`.** Cuáles faltan **no se copia de aquí**: se corre
      `python scripts/auditar_cableado.py`, que reemite
      [`CORRECCIONES_CABLEADO.md`](CORRECCIONES_CABLEADO.md) con lo que quede
- [x] **Mirar en el editor las seis que el auditor no puede juzgar**, una a una, y anotar su
      `Source table`. Son las que apuntan a tablas vacías: `CHD→CHK`, `CHK→MAN`, `FIR→MAN`,
      `FOT→MAN`, `MAN→OT` y la autorreferencia `OT_OrdenesTrabajo.OTOrigenID`. Hecho el 2026-08-11
      ([`ACTA-010`](sdd/ACTA-010-cotejo-ocho-tablas.md)) — mirado, no medido: sigue sin haber comando
      que lo compruebe
- [ ] **Y al cablear `ACT_Activos.EstadoActivoID` se despierta `RG-16`**, que es una `App formula` y
      por tanto **escribe en la hoja**. Hoy `Activo` está poblada a mano en las 368 y hay **un solo
      activo con `EST-04` (Retirado)**, que ya trae `Activo = FALSE`: la regla no debería cambiar
      ninguna celda, y si cambia alguna, el dato y la regla no dicen lo mismo. Con ella viva,
      `RG-18` —el histórico no filtra por el estado actual del activo— deja de estar dormida, porque
      por primera vez hay una fila donde la prohibición se nota. Tiene prueba: `P-33` en
      [`sdd/PRUEBA-003-despliegue.md`](sdd/PRUEBA-003-despliegue.md), y `RG-34` tiene la suya en
      `P-32`, que hasta hoy no existía
- [ ] Geofencing, con la expresión que atraviesa la orden y el activo:
      `DISTANCE([Coordenadas_Cierre_LatLong], [OTID].[ActivoID].[Ubicacion_LatLong]) <= [OTID].[ActivoID].[TipoActivoID].[RadioGeofencingKm]`
      y mensaje de error en texto plano. **El literal `1.0` ya no se usa**: la hoja que la aplicación
      lee trae el radio poblado en los 27 tipos
- [ ] `Editable_If = FALSE` en las cuatro columnas de captura de `MAN_Mantenimientos` (`RG-20`). **Sin
      esto el geofencing es decorativo**: el pin del mapa se arrastra encima del activo y la regla
      valida sin protestar
- [ ] Los dos filtros de seguridad: activos por unidad funcional, órdenes por técnico o supervisor
- [ ] Las cuatro marcas de tiempo como `ChangeTimestamp` del servidor
- [ ] Evidencia en tablas hijas, con `IsPartOf` en las cuatro que lo llevan, **y `Deletes` retirado
      antes** en `OT_OrdenesTrabajo` y `MAN_Mantenimientos`. El orden no es opcional: `IsPartOf` es
      borrado en cascada, y solo es seguro porque el mantenimiento nunca se borra
- [ ] La regla del umbral de GPS **entera**, con su `OR(ISBLANK(...))`. Sin él, si alguien borra la
      fila del parámetro todos los cierres salen limpios y nadie se entera

Pendiente, y además no declarado todavía en el modelo:

- [ ] Imponer `QuienCambia`: la columna está poblada en las siete filas y **ninguna de las 23 reglas
      la lee**, así que hoy nada impide que un técnico ponga «Cerrada» él mismo
- [ ] Estado de rechazo. `MAN_Mantenimientos.ObservacionRechazo` existe y la orden no tiene a dónde
      volver: falta una fila `Devuelta` en `EOT_EstadosOrden`, que es dato y no esquema
- [x] Bots de notificación y de alerta. **Resuelto por `ESPEC-006`/`ORDEN-006`**: los dos que no
      cabían en el plan gratuito (`RG-08`, `RG-12`) se retiraron y se reemplazaron por `RG-37`
      (columna virtual) y `RG-38` (vista + acción). Ver el recuadro de abajo
- [ ] **Declarar la interfaz en el modelo** —vistas, acciones y slices—, y generar de ahí el manual
      de pantallas. Mientras no exista, el paso de vistas de cualquier manual dice «se construye
      sola», que es la clase de instrucción que este proyecto tiene prohibida
- [ ] Reportes y tablero, según D-12 y D-13, encima de lo anterior

> **Resuelto por `ESPEC-006`/`ORDEN-006` (2026-08-11): `RG-08` y `RG-12` se retiraron del modelo.**
> No se reemplazó "bot que no corre" por "bot que sí corre" — se reemplazó el mecanismo entero.
> `RG-37` (columna virtual `EstaVencida` sobre `OT_OrdenesTrabajo`) sustituye a `RG-08`: informa,
> no mueve el estado. `RG-38` (vista + acción sobre `PLA_PlanMantenimiento`, invocada por el
> supervisor) sustituye a `RG-12`. Lo que sigue debajo describe el problema tal como se encontró y
> por qué había que decidir antes de configurar nada; se conserva como historia, no como estado
> vigente. El análisis por debajo queda como registro de tres bots por evento, no cinco.
>
> ### Los 3 bots por evento, y los dos programados que se retiraron
>
> La lista se vuelca, no se cita:
>
> ```bash
> python -c "import sys;sys.path.insert(0,'scripts');from modelo_objetivo import REGLAS;[print(r['id'],'|',r['tipo'],'|',r['tabla']) for r in REGLAS if 'Bot' in r['tipo']]"
> ```
>
> | Bot | Tipo | Se ejecuta en esta cuenta |
> |---|---|---|
> | `RG-06` · alerta de activo fuera de servicio | `Bot` por evento | Sí |
> | `RG-07` · aviso al técnico al asignarle una orden | `Bot` por evento | Sí — **y manda correo real**, ver abajo |
> | `RG-10` · orden de seguimiento por segunda visita | `Bot` por evento | Sí |
> | **`RG-08`** · marcar `Vencida` la orden pasada de fecha | **`Bot programado`** | **No** |
> | **`RG-12`** · generar las órdenes de la semana desde el plan | **`Bot programado`** | **No** |
>
> **`RG-08` y `RG-12` son bots PROGRAMADOS, y esta cuenta es gratuita.**
> [`BASE_CONOCIMIENTO_APPSHEET.md`](BASE_CONOCIMIENTO_APPSHEET.md) §6 lo documenta con cita oficial:
> *«puedes configurar estas funciones, pero no se ejecutarán como esperas»*, y añade dos matices que
> importan: depende también de que la app esté **desplegada**, y en cuenta gratuita **los correos de
> un bot programado van solo al propietario de la app**, no al destinatario que la regla nombra.
>
> **Se configuran igual** —hay que dejarlos puestos, y se pueden **ejercitar a mano con `Test`**—,
> pero **contarlos como funcionando sería falso.** Es la forma de `CLAUDE.md` §7.13: una regla puesta,
> bien escrita, sin un solo error, que no hace nada. Aquí el motivo no es el tipo ni el dato ni una
> función inexistente: es el **plan de licenciamiento**, y por eso depende de **D-B** y de nadie del
> equipo técnico.
>
> **Esto corrige la línea anterior de esta fase**, que metía los cinco en el mismo saco. Los tres por
> evento sí se ejecutan en el plan gratuito, y hay evidencia dura de ello: `PRUEBA-005` tuvo que
> **desactivar `RG-07` antes de sembrar su fixture** para no disparar tres correos reales.
>
> ### `RG-07` manda correos de verdad, a una persona de verdad
>
> `RG-07` dispara con **cualquier** fila nueva en `OT_OrdenesTrabajo` —la cree un técnico con el
> botón `+` o el bot `RG-10`— y notifica por correo al técnico asignado. Hoy eso es
> **`ivan.salcedo@concesiondelsisga.com.co`**, una dirección corporativa. **Cualquier tanda que cree
> órdenes le escribe**, incluidas las de prueba, y ya pasó: `PRUEBA-005` habría mandado tres correos
> sobre órdenes marcadas `TEST`.
>
> Se desactiva en `Automation > Bots` → `RG-07` → `Disable`, y se reactiva al terminar. **Pero es una
> decisión abierta, no un paso de fixture:** hay que decidir si en el piloto el técnico debe recibir
> ese correo, o si el aviso vive solo dentro de la aplicación. Afecta a toda tanda futura que cree
> órdenes.
>
> ### `Vencida` es un estado FINAL, así que una orden que se pasa de fecha no puede cerrarse
>
> `RG-08` marca la orden como `Vencida` cuando su fecha programada pasa sin cerrarse. Y `Vencida`
> tiene **`EsFinal = Y`**. Es dato, y se comprueba en las dos fuentes:
>
> ```bash
> python -c "import json,io;d=json.load(io.open('BD/instantaneas/antes-de-fase-c.json',encoding='utf-8'));[print(r['EstadoOrdenID'],'EsFinal=',r['EsFinal']) for r in d['EOT_EstadosOrden']]"
> ```
>
> De los 7 estados hay **2 finales**: `Cerrada` y `Vencida`.
>
> **La consecuencia es operativa, no técnica: el técnico que llega tarde no puede registrar el
> mantenimiento que sí hizo.** La orden entra en un estado terminal por el paso del tiempo, y el
> trabajo real que se ejecutó después no tiene dónde asentarse. **Probablemente no es lo que
> operación quiere**, y hay al menos tres salidas —que `Vencida` deje de ser final, que exista una
> transición de reapertura, o que el vencimiento sea una marca y no un estado—. **Está pendiente de
> decidir con operación, y la decisión va antes de poner `RG-08`**: ponerlo primero significa
> descubrirlo con la primera orden real encima.
>
> Hoy no ha hecho daño porque `RG-08` es de los que no se ejecutan (arriba) y porque
> `OT_OrdenesTrabajo` está vacía. **Las dos cosas dejan de ser ciertas el mismo día.**
>
> **Decidido por `ESPEC-006`/`ORDEN-006`: la tercera salida.** `Vencida` deja de ser una
> consecuencia automática y pasa a ser una decisión del supervisor de que la orden no se va a
> ejecutar — se queda `EsFinal = Y`, correcto para una disposición final tomada por una persona.
> `RG-37` (columna virtual `EstaVencida`) es la marca informativa; no bloquea el cierre, verificado
> como el punto que más pesaba de la especificación (`PRUEBA-006` `P-55`).

**Cierra cuando:** cada regla se demuestra funcionando en la app, no solo configurada — **y las que
no puedan demostrarse en esta cuenta se cierran diciendo que no se demostraron, no dándolas por
buenas.**

---

## 7. Fase 3 — Prueba controlada

Etapa que no existía en la versión anterior y cuya ausencia habría llevado el primer error real
directamente a los 10 celulares del piloto.

- [ ] Un mantenimiento completo de extremo a extremo, ejecutado por una persona sobre un activo
      con coordenada real: apertura por lista, checklist, fotografías, firma y cierre con GPS
- [ ] El mismo flujo repetido en modo avión, con verificación de la sincronización posterior
- [ ] Prueba del bloqueo: intentar cerrar lejos del activo y confirmar que el sistema lo impide

> **El par de pruebas del geofencing sigue sin discriminar, y ahora es más difícil de ver.** Mientras
> `ACT_Activos.Ubicacion_LatLong` estuvo vacía en las 368, `DISTANCE()` comparaba contra blanco y
> **fallaban las dos**, la que debe aceptarse y la que debe rechazarse. Hoy la columna trae las 368
> pobladas y **el resultado no cambia**: el punto derivado del `PK` está sobre la vía pero no frente
> al equipo, así que con 0,05 km de radio el cierre legítimo se sigue rechazando. **Lo que cambió es
> que ya no hay una celda vacía que lo delate.** La tanda sigue sin distinguir una regla correcta de
> una rota, y **solo D-01 lo arregla.**

**Cierra cuando:** hay filas reales en `MAN_Mantenimientos` y en las tablas de evidencia,
verificadas leyendo el archivo. **Hoy no hay ninguna, ni de prueba**: la hoja se entrega sin
registros a propósito, para que el primer ciclo que se recorra sea real.

---

## 8. Fase 4 — Piloto de campo

- [ ] Instalación en los 10 móviles del grupo piloto y autenticación corporativa
- [ ] Verificación de que cada técnico descarga solo los activos de su zona
- [ ] Operación real durante una semana, con acompañamiento
- [ ] Registro de incidencias y ajuste de formularios según lo observado

> **Lo que el piloto va a encontrar y conviene anticipar: los túneles.** Bajo tierra el GPS no fija
> posición, así que `RG-01` falla **siempre** para el equipo de dentro, por diseño y no por avería.
> Son quince túneles y 7.224 metros, y **6.000 de los 17.800 de la UF3** van bajo tierra. Sin los
> tramos declarados, el supervisor verá a un técnico acumulando cierres con excepción sin poder
> distinguir el túnel del técnico. La tabla `TUN_Tuneles` está en `PROPUESTAS`, sin especificar.

**Cierra cuando:** los 10 técnicos completaron mantenimientos sincronizados desde el corredor y
las incidencias críticas están resueltas.

---

## 9. Fase 5 — Producción y evolución

- [ ] Cierre del banco de preguntas: que no quede ninguna marcada `[BORRADOR: validar con operacion]`
- [ ] Generación automática de órdenes por frecuencia. **No es cuestión de tiempo: depende de D-B**,
      porque en el plan gratuito los procesos programados no se ejecutan
- [ ] Integración con Power BI para tableros ejecutivos
- [ ] Integración con mesas de ayuda para tickets de TI
- [ ] Respaldo automático de evidencias y base de datos

---

## 10. Lo que la versión 3 daba por hecho y no lo estaba

Se conserva porque explica por qué este documento exige un criterio de cierre por fase. **Cada línea
es un hito marcado como completado sin nada que lo demostrara.**

| Afirmación de la versión 3 | Realidad verificada el 2026-08-06 |
|---|---|
| "Fase 0 y 1: completado 100 %" | 8 bloqueantes abiertos |
| "Modelo de datos 17 tablas: done" | El libro de entonces tenía 24 hojas |
| "18 formularios dinámicos: done" | 1 de 18 con banco de preguntas, y sin mapeo desde el tipo de activo |
| "Validaciones GPS y Security Filter: done" | GPS inoperante por coordenada única; el filtro dejaría a los técnicos sin activos |
| "Pruebas QA y dictamen: done" | `MAN_Mantenimientos` vacía: el flujo nunca se ejecutó |
| "Estado actual: Fase 1.5, piloto" | El proyecto estaba en definición funcional |

**El problema de fondo no era la desactualización: era marcar hitos sin criterio de cierre.** Por eso
cada fase de este documento lleva el suyo, y por eso son hechos que otra persona puede comprobar
leyendo un archivo, no reportes de avance.

---
*Referencias:* [ESTADO.md](../ESTADO.md) | [FUNCIONAL_SGMC.md](FUNCIONAL_SGMC.md) | [INDICACIONES_POR_ROL.md](INDICACIONES_POR_ROL.md) | [MAP.md](../MAP.md)
