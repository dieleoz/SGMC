# ROADMAP de implementación — SGMC

**Proyecto:** Sistema de Gestión de Mantenimiento en Campo
**Cliente:** Concesión Transversal del Sisga S.A.S.
**Actualizado:** 11 de agosto de 2026 | **Versión:** 4.4

> ## Para qué sirve este documento, y para qué no
>
> **El estado del proyecto está en [`ESTADO.md`](../ESTADO.md), no aquí.** Este documento es el
> **orden de implementación**: qué va antes que qué, y por qué ese orden y no otro. Es lo que no
> cabe en un tablero de estado y lo que más caro sale improvisar.
>
> **Qué cambió en la 4.4, del 2026-08-11. Es un cambio de ORDEN, que es lo que este documento
> decide:**
>
> - **Hay una ventana que se cierra sola, y por eso pasa delante de todo lo demás.** Está en §2.1.
>   Ocho tablas siguen en cero filas, y esa vacuidad **no es un estado neutro**: es lo único que hace
>   que corregir un tipo o una clave cueste un clic. **El primer registro la cierra para siempre**,
>   porque las ocho son transaccionales. Lo que cabe dentro está reunido y generado en
>   [`ENCARGO_VENTANA.md`](ENCARGO_VENTANA.md), con **lo que deja fuera y por qué**.
> - **`ESPEC-005` está aplicada al modelo, y la hoja de datos NO cambió.** Es contraintuitivo y
>   conviene que quede escrito: se comparó el `.xlsx` antes y después y salen **29 pestañas, las
>   mismas, y cero con contenido distinto**. La razón es que `RG-35` y `RG-36` son **columnas
>   virtuales** y las listas de claves describen el comportamiento del editor, no los datos. Ver §3.1.
> - **`F-11` dejó de disparar sobre dos tablas**, y es una comprobación menos. Ver §3.1.
> - **De los 5 bots, 2 no se pueden dar por funcionando en esta cuenta**, y no por estar mal
>   configurados. Ver §6.
> - **`Vencida` tiene `EsFinal = Y`, así que una orden que se pasa de fecha no puede cerrarse.** Es
>   una decisión de operación pendiente, no un defecto de configuración. Ver §6.
>
> **Qué cambió en la 4.3, del 2026-08-10 por la tarde:**
>
> - **El cableado dejó de estar sin empezar, y dejó de poder afirmarse desde este documento.** Se
>   cablearon las referencias en el editor y el informe dijo «39/39 asignadas». **No era cierto.** Dos
>   apuntaban a `SED_Sedes` en vez de a `CAL_Calzadas` y a `TIP_TiposActivo`, y tres columnas de texto
>   se habían convertido en `Ref`. Ya están corregidas. Lo que queda **no lo sabe este roadmap**: se
>   pregunta con `python scripts/auditar_cableado.py`, que lee la aplicación en vivo. Ver §6.
> - **Las 368 coordenadas se perdieron y se repusieron el mismo día.** Al renombrar `Ubicacion` a
>   `Ubicacion_LatLong` la columna nueva nació vacía y nadie lo vio. Hoy `generar_plantilla.py` las
>   **deriva del `PK`** sobre el trazado en cada pasada en vez de conservarlas, y están las 368 de 368.
> - **Hay un sexto verificador**, `scripts/verificar_datos.py`, y **un auditor de cableado**,
>   `scripts/auditar_cableado.py`. Los dos nacieron de los dos párrafos anteriores.
> - **`RG-21` se renumeró a `RG-34`.** `ESPEC-003` §12.1 ya usaba `RG-21` para `USR_Usuarios.RolID`, y
>   dos reglas con el mismo identificador es exactamente el defecto que este documento persigue.
>
> **Qué cambió en la 4.2, del 2026-08-10:**
>
> - **La aplicación se volvió a reconstruir desde cero, y la vigente es `_SISGA_-323965761`
>   sobre la hoja `Modelo_Datos_10082026`.** Entre el 6 y el 10 de agosto hubo cinco aplicaciones y
>   tres hojas; las superadas están nombradas, con su motivo, en `scripts/sistema.py`. **Vuélquelo
>   con `python scripts/sistema.py`** en vez de copiar el nombre de aquí.
> - **El cableado de la aplicación anterior no sobrevivió, y por eso se repone entero.** La versión
>   4.1 daba las 39 referencias por puestas; la 4.2 dio la aplicación por tener **las 28 tablas y nada
>   más**. Las dos afirmaban un estado del cableado desde un documento. **Ninguna volverá a hacerlo:**
>   ver la 4.3, arriba.
> - **La migración a la hoja limpia ya se ejecutó**, así que dejó de ser una decisión y pasó a ser un
>   hecho. `BD/Modelo_Datos_PLANTILLA.xlsx` sale generada del modelo y es el archivo publicado.
> - **Las referencias son 39, no 15.** Las 15 eran las que faltaban en una aplicación anterior donde
>   otras 23 ya estaban puestas. Sobre una aplicación nueva no sobrevive ninguna.
> - **La Fase 0.5 de reconciliación de modelos está cerrada**, y su lista de tareas —que ocupaba la
>   mitad de este documento— se ha reducido al registro de lo que dejó decidido.
>
> **Y el mismo día cambió el modelo de datos, que es lo que más reordena esta secuencia.** Las
> claves pasaron a alfanuméricas con prefijo —`ACT-0001`, `TIP-001`, `UNF-01`, `SED-001`,
> `USR-001`, `ROL-01`…—, las seis columnas de coordenada llevan `_LatLong` en el nombre, `SED_Sedes`
> volvió con `UnidadFuncionalID`, `PR`, `TramoINVIAS`, `PK` y `Ubicacion_LatLong` como padre de
> ubicación del equipo bajo techo, y `ACT_Activos` ganó `PK` y `TramoINVIAS`. **Eso saca dos
> partidas del paso 1**, que dejan de ser esquema por construir y pasan a ser dato por cargar. El
> motivo de cada regla, y quién la hace cumplir, está en
> [`REGLAS_DEL_MODELO_DE_DATOS.md`](REGLAS_DEL_MODELO_DE_DATOS.md), que se genera del modelo.
>
> El documento funcional que se entrega es [`FUNCIONAL_SGMC.md`](FUNCIONAL_SGMC.md). El contexto
> operativo destilado está en [`CONTEXTO_OPERACION.md`](CONTEXTO_OPERACION.md). El reparto de quién
> hace qué, en [`INDICACIONES_POR_ROL.md`](INDICACIONES_POR_ROL.md).

> **De dónde viene la versión 4.** La 3 declaraba completadas al 100 % la Fase 0 y la Fase 1, y la
> auditoría del 6 de agosto de 2026 verificó contra el archivo que era falso. Ese dictamen,
> `AUDITORIA_PLAN_Y_ROADMAP.md`, se retiró en la limpieza del 2026-08-10; sus hallazgos `B-01` a
> `B-14` son el origen de casi todo lo que se decidió después.
>
> Y la 4.0 amplió el alcance al leer los siete documentos de `contexto/`: la operación real tiene
> varias tareas por tipo de equipo, cuatro clases de mantenimiento, un flujo de correctivo con
> tiempos contractuales y cinco activos que no se visitan. **Ya no cabe todo de una vez**, y por eso
> esto dejó de ser una lista de fases y pasó a ser un orden con criterio explícito.

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
| **0b** | ~~Decidir la migración~~ | **Ejecutada el 2026-08-10.** Las 48 columnas sobrantes ya no existen en el archivo, así que ocultarlas dejó de estar en el plan y con ellas se fueron las tres trampas | Cerrado |
| **1** | **Esquema completo** | `TAR_Tareas` · poblar `ROL_Roles` con los 12 · `ETR_Estructuras`, que es lo que queda de la jerarquía de ubicación · columnas de tiempo en la orden · retirar `ACT.FrecuenciaID` y `TIP.FormularioID`, **que `verificar_documentos.py` avisa como descartadas y vivas con fecha tope 2026-08-31** | `ESPEC-003` y su veredicto |
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

Hoy: **8 tablas · 54 tipos a cotejar · 2 columnas virtuales.**

**Lo que cabe dentro de la ventana está reunido en [`ENCARGO_VENTANA.md`](ENCARGO_VENTANA.md)**,
generado por `scripts/generar_encargo_ventana.py`. Son dos cosas y nada más: las **2 columnas
virtuales `Etiqueta`** que deja pendientes `ESPEC-005`, y el **cotejo de los 54 tipos** de esas ocho
tablas —mirar, no cambiar, y anotar lo que se vea aunque coincida, porque la API devuelve filas y no
esquema, y esa anotación es la única evidencia que va a existir—.

**Y lo que NO cabe, con su motivo, que es la mitad que impide que la lista se reordene sola:**

| Queda fuera | Por qué |
|---|---|
| `UNF_UnidadesFuncionales` y `USR_Usuarios` | **Tienen filas.** Su ventana se cerró hace tiempo, su precio ya está pagado y no vuelve a subir: pueden esperar |
| Los 5 bots | **No dependen de la ventana.** Se configuran igual con las tablas llenas |
| `RG-04` y `RG-05`, los `Security Filter` | Van **los últimos**. Al ponerlos, la API deja de devolver las filas de esa tabla y ni `auditar_cableado.py` ni `instantanea.py` pueden volver a mirarla. Apagan los instrumentos |
| `RG-02`, `RG-19` y `RG-03` | `ESPEC-004` sigue **BLOQUEADA**, y `RG-02` usa una función que no existe en AppSheet |

**La prohibición central del encargo es poblar cualquiera de las ocho**, y no es una precaución
genérica: es **justo el acto** que acaba con el motivo por el que el encargo existe. Quien la cierra
casi nunca cree estar decidiendo nada —siembra un fixture, crea una orden para ver si el bot
dispara—, y ese es exactamente el riesgo. La regla general está en [`CLAUDE.md`](../CLAUDE.md) §7.17.

> **Esto no reordena las fases: se mete delante de todas.** El paso 1 de §2 —esquema completo— sigue
> siendo el que no admite trocearse, y sigue viviendo dentro de esta misma ventana, con el mismo
> motivo: `MAN_Mantenimientos` está vacía y añadir hoy cuesta cero.

---

## 3. Estado por fase

> ### La migración a la hoja limpia, decidida el 2026-08-09 y **ejecutada el 2026-08-10**
>
> **El Excel del repositorio es lo que se entrega, y es la hoja que la aplicación lee.** El funcional
> parte de ese archivo y desde ahí sigue las guías, así que tenía que salir generado y limpio en vez
> de ser una hoja heredada con 48 columnas escondidas encima.
>
> **Lo que cambió al ejecutarla:** ocultar esas 48 salió del plan —ya no existen en el archivo, y con
> ellas se fueron las tres trampas—, y el literal provisional de `1.0` km dejó de aplicar, porque
> `TIP_TiposActivo.RadioGeofencingKm` viene poblado en los 27 tipos de la hoja que la aplicación lee.
>
> **Lo que lo hizo posible:** `scripts/generar_plantilla.py`. La plantilla sale entera de un comando
> y se reproduce celda por celda, con los 27 tipos del catálogo y **cero activos viendo el checklist
> de otro equipo**.

| Fase | Estado | Criterio de cierre |
|---|---|---|
| Sprint 0. Definición funcional | **Cerrado por supuestos.** No se espera respuesta | Los catorce adoptados por escrito en `ALCANCE_Y_SUPUESTOS_SGMC.md`, con su estado de cierre |
| Fase 0.5. Reconciliación de modelos | **CERRADA** el 2026-08-07 | `modelo_objetivo.py` es la fuente única; los documentos se generan de él. Ver 4.5 |
| **Fase A. La hoja** | **CERRADA** | `verificar_faseA.py` en 0 fallos sobre `BD/Modelo_Datos_PLANTILLA.xlsx`. Hoy: **82 conformes y 4 avisos esperados** |
| Reconstrucción de la aplicación | **HECHA** el 2026-08-10 | `_SISGA_-323965761`, con las 28 tablas dadas de alta sobre `Modelo_Datos_10082026` |
| **Fase B. Las 39 referencias** | **HECHA el 2026-08-10.** El auditor sale con **0 correcciones**. De las 39: **4 verificadas** —la aplicación nombra la columna—, **29 compatibles no atribuidas** y **6 no medibles**, estas últimas miradas una a una en el editor y registradas con fecha en `CONFIRMADAS_A_OJO`. El estado **no lo declara este documento**: `python scripts/auditar_cableado.py` | Auditor en 0. Cumplido |
| **Fase C. Las 23 reglas** | **EN CURSO — marcador real: 20 configurables · 9 cotejadas · 3 imposibles.** Eran 21 hasta que `ESPEC-005` añadió `RG-35` y `RG-36`; las 3 imposibles son `RG-02`, `RG-19` y `RG-03`, que espera `ESPEC-004`. En el editor: **las 6 claves con `UNIQUEID()` puestas**, **tipos y etiquetas de 22 de las 28 tablas** —faltan `UNF_UnidadesFuncionales` y `USR_Usuarios`—, **las 2 columnas virtuales `Etiqueta` sin crear** y **los 5 bots sin empezar** —de los cuales **2, `RG-08` y `RG-12`, no se ejecutarán en esta cuenta por ser programados**, ver §6—. **Lo que hay que hacer ANTES de que entre la primera fila está aparte, en [`ENCARGO_VENTANA.md`](ENCARGO_VENTANA.md)**, porque caduca solo (§2.1). El resto, en [`PROMPT_EXPRESIONES.md`](PROMPT_EXPRESIONES.md), que trae para cada regla su tabla, su propiedad y **la cadena de referencias que atraviesa** —una expresión con puntos no falla por estar mal escrita, falla porque un salto no está cableado—, y **dónde está cada control en pantalla** con `python scripts/navegacion_editor.py`, porque `Required_If` se llama `Require?` y no es una casilla. Va en dos tandas: primero las que **no escriben**, después las que **sí** | Las 23 puestas, los dos filtros, las cuatro marcas de tiempo, `Deletes` retirado y `PRUEBA-003` pasada. `RG-16` no debe cambiar ninguna de las 368 celdas |
| Fase 1. Datos maestros | Bloqueada por D-01 y D-09 | Coordenadas reales cargadas, sedes realineadas, bancos de preguntas construidos |
| Fase 2. Configuración de interfaz | Bloqueada por Fase 1 y por declarar vistas | Reportes y pantallas construidos. **Antes hay que declarar la interfaz en el modelo**: hoy no tiene vistas, ni acciones, ni slices |
| Fase 3. Prueba controlada | Bloqueada por Fase 2 | Registros reales en `MAN_Mantenimientos` y en las tablas de evidencia, verificados leyendo el archivo |
| Fase 4. Piloto de campo | Bloqueada por Fase 3 | 10 técnicos operando una semana, con registros sincronizados desde el corredor |
| Fase 5. Producción y evolución | Bloqueada por Fase 4 | Ninguna pregunta marcada como borrador, integraciones y respaldo automático |

**No hay fechas.** El cronograma depende de dos tareas que son trabajo del cliente y cuya duración
solo el equipo de la Concesión puede estimar: el levantamiento de las coordenadas reales (decisión
D-01) y la redacción de los bancos de preguntas (decisión D-09). Las fechas se fijan en el acta de
la mesa de trabajo, no antes.

---

## 3.1 Lo que sí está construido

Verificado el 2026-08-10 contra `scripts/modelo_objetivo.py` y `BD/Modelo_Datos_PLANTILLA.xlsx`.
> ### Lo que falta de la Fase C: una decisión, y una mitad de teclado
>
> - [`ESPEC-005`](sdd/ESPEC-005-clave-otid-planid.md) — **APLICADA AL MODELO, PENDIENTE EN EL
>   EDITOR.** Es el primer dictamen del pipeline que pasa el gate. `OTID` y `PlanID` eran claves
>   legibles que **nadie generaba**, así que los bots `RG-10` y `RG-12` habrían creado filas sin
>   identificador y AppSheet las descarta sin avisar. Ya son `UNIQUEID()`: `CLAVE_LEGIBLE` bajó de
>   22 a 20 tablas y `CLAVE_GENERADA` subió de 6 a 8. En su lugar, la identificación ante el técnico
>   la dan **dos columnas VIRTUALES llamadas `Etiqueta`** —`RG-35` y `RG-36`—, que AppSheet calcula
>   y **no se guardan en la hoja**; por eso no están en `MODELO`, solo en `REGLAS` y en
>   `inferencia.ETIQUETA_VIRTUAL`. **Con esto queda desbloqueado crear órdenes desde la
>   aplicación**, que hoy se hacen en el Sheets saltándose todas las validaciones. **Lo que falta es
>   la mitad del editor**: crear las dos virtuales, marcarles `Show?` y marcarles `Label`. Encargo
>   en [`ENCARGO_VENTANA.md`](ENCARGO_VENTANA.md), paso 1 — y también en
>   [`PROMPT_CABLEADO.md`](PROMPT_CABLEADO.md), paso 5.
>
>   **Y aquí está lo contraintuitivo, que conviene dejar escrito: la hoja de datos NO cambió.** Se
>   comparó el `.xlsx` antes y después de aplicar `ESPEC-005`, y salen **29 pestañas, las mismas, y
>   cero pestañas con contenido distinto**:
>
>   ```bash
>   python -c "import subprocess,io,openpyxl;a=subprocess.run(['git','show','43b0666:BD/Modelo_Datos_PLANTILLA.xlsx'],capture_output=True).stdout;A=openpyxl.load_workbook(io.BytesIO(a),read_only=True,data_only=True);B=openpyxl.load_workbook('BD/Modelo_Datos_PLANTILLA.xlsx',read_only=True,data_only=True);print(len(A.sheetnames),'pestanas | mismos nombres:',A.sheetnames==B.sheetnames,'|',sum(1 for n in A.sheetnames if [tuple(r) for r in A[n].iter_rows(values_only=True)]!=[tuple(r) for r in B[n].iter_rows(values_only=True)]),'con contenido distinto')"
>   ```
>
>   `43b0666` es el commit anterior a `ESPEC-005`. El archivo binario difiere en **un byte** —metadato
>   del `.zip`—, así que `git diff --stat` lo marca como cambiado; **por celda no cambió nada**, y
>   esa es la pregunta que importa.
>
>   **La razón:** `RG-35` y `RG-36` son **columnas virtuales** —no existen en el Sheets—, y
>   `CLAVE_LEGIBLE` y `CLAVE_GENERADA` describen el comportamiento del **editor**, no los datos. **Eso
>   es justamente lo que hacía atractiva la columna virtual frente a la real**, que sí habría tocado
>   producción: una `App formula` sobre una columna real escribe en la hoja, y habría cambiado las 368
>   filas de nadie sabe qué antes de que alguien pudiera revisarlo. Un cambio de modelo que no toca un
>   solo byte de datos es un cambio que se puede deshacer.
>
>   **Y un efecto que resta, no suma: `F-11` dejó de disparar sobre `OT_OrdenesTrabajo` y
>   `PLA_PlanMantenimiento`.** Esa comprobación de `verificar_faseA.py` —que las listas de claves
>   digan la verdad sobre la hoja— **exime a `CLAVE_GENERADA` a propósito**, y las dos acaban de
>   entrar ahí. Es **correcto** —sus claves serán aleatorias en cuanto la aplicación cree la primera
>   fila—, pero son **dos comprobaciones menos**, y el verde de `verificar_faseA.py` ya no dice nada
>   de ellas. Que la clave de esas dos esté bien puesta **solo se ve en el editor**, que es lo que
>   pide el encargo de la ventana.
> - [`ESPEC-004`](sdd/ESPEC-004-cierre-excepcion-manual.md) — **BLOQUEADA.** `RG-02` usa una función
>   que **no existe en AppSheet**, y deja inertes a `RG-19` y `RG-03`. Segunda pasada del
>   arquitecto: **quince hallazgos**. No se aplica.
>
> Nada se aplica hasta que pase por el arquitecto. `ESPEC-005` es la prueba de que ese ciclo termina
> en algo: entró, la tumbaron, se rehizo contra el archivo y pasó.

> ### Una regla puede estar puesta y no hacer nada
>
> Es lo que más veces ha pasado, y siempre en silencio. Tres casos el 2026-08-10, cada uno por un
> motivo distinto:
>
> | | Por qué no hacía nada |
> |---|---|
> | `RG-03` | su columna era `Text` y comparaba contra el booleano `TRUE` |
> | `RG-06` | `EST_Activo.GeneraAlerta` estaba vacía en los cuatro estados |
> | `RG-02` | `USERLOCATIONACCURACY()` **no existe en AppSheet** |
>
> Las tres estaban bien escritas y bien colocadas. Ninguna dio un error.
>
> `verificar_datos.py` caza el segundo caso desde que existe **G-05** —cruza el alcance real de las
> 23 reglas contra los datos—. Los otros dos **solo se ven mirando**: el tipo vive en el editor y la
> función es un hecho de la plataforma.

**Cada cifra se rederiva con los seis verificadores; ninguna está escrita de memoria.** El sexto,
`verificar_datos.py`, se añadió ese mismo día y es **el único que abre el archivo de datos** para
mirar si las columnas obligatorias están pobladas y si las 39 referencias resuelven contra los
valores reales. Los otros cinco leen declaraciones, estructura, prosa, enlaces o dos pasadas del
generador entre sí.

> **Y ninguno de los seis mira la aplicación.** Lo que está cableado en `_SISGA_-323965761` **no lo
> sabe ningún documento generado desde el modelo**, y este es uno de ellos: el modelo declara lo que
> tiene que existir, no lo que existe. Se pregunta, siempre, con
>
> ```bash
> python scripts/auditar_cableado.py
> ```
>
> que lee la aplicación en vivo por la API y reemite [`CORRECCIONES_CABLEADO.md`](CORRECCIONES_CABLEADO.md).
> **Y hay que leer su recuento entero, no la primera línea**, porque separa dos cosas que no son lo
> mismo: las referencias **verificadas** —la aplicación nombra la columna— de las **compatibles no
> atribuidas** —la aplicación nombra la tabla destino, y que sea la columna que el modelo declara lo
> dice el modelo, no la aplicación—. Sumarlas infla la cifra, y ya se infló una vez.

- **Modelo de 28 tablas, 211 columnas, 39 referencias y 23 reglas.** `validar_modelo.py` sale
  `APTO PARA DESPLEGAR` con 0 errores y 3 avisos.
- **La hoja se genera del modelo, y es la que la aplicación lee.** 28 pestañas de datos más `_LEEME`,
  ninguna oculta, sin una sola columna de sobra ni de menos: **las 48 que sobraban ya no existen en el
  archivo**, y el recuento de los 211 encabezados contra el modelo da cero por los dos lados. Las 48
  están hoy **todas en `CAMPOS_RETIRADOS`, y `COLUMNAS_SIN_DECIDIR` quedó vacío**: las cuatro que
  nadie había decidido —`USR_Usuarios.UltimaSincronizacion`, `FOT_Fotografias.Fecha`,
  `FRM_Formularios.Orden` y `FRM_Preguntas.ValorDefecto`— las decidió la regeneración al dejarlas
  fuera, y un aviso que afirma que están sin decidir se repetiría en cada ejecución siendo falso. El
  reparto se vuelca, no se cita:

  ```bash
  python -c "import sys;sys.path.insert(0,'scripts');import modelo_objetivo as M;print(sum(len(v) for v in M.CAMPOS_RETIRADOS.values()),'+',len(M.COLUMNAS_SIN_DECIDIR))"
  ```
- **Todas las claves son alfanuméricas con prefijo.** `ACT-0001`, `TIP-001`, `UNF-01`, `SED-001`,
  `USR-001`, `ROL-01`, `EST-01`, `FRE-01`, `CAL-01`, `SEC-01`, `TPR-01`, más las que ya lo eran
  —`OT-0001`, `MOT-01`, `FAL-01`, `ASG-01`, `PLA-001`, `FRM_SOS`, `SOS001`, `UMBRAL_GPS`—.
- **`SED_Sedes` sabe dónde está**, con `UnidadFuncionalID`, `PR`, `TramoINVIAS`, `PK` y
  `Ubicacion_LatLong`, y `ACT_Activos.SedeID` cuelga de ella para el equipo bajo techo. `RG-34`
  impide que el activo y su sede declaren unidades funcionales distintas. **Eso es la estructura, no
  el dato:** `SED_Sedes.UnidadFuncionalID` está poblada en **1 de 6** y `ACT_Activos.SedeID` en **0 de
  368**, así que hoy `RG-34` no compara nada. Es trabajo de operación y está en §5.
- **`ACT_Activos` distingue `PK` de `PR`**, y lleva `TramoINVIAS` para que el PR identifique un
  punto. `PK` está poblado en las 368; `PR` y `TramoINVIAS`, vacíos en las 368.
- **Aplicación reconstruida el 2026-08-10 con las 28 tablas dadas de alta, y con el cableado de
  referencias empezado.** Las reglas, los dos filtros de seguridad y las cuatro marcas de tiempo
  **siguen sin poner**. Cuántas referencias están puestas, y cuáles, **es lo único de esta lista que
  no se deriva del modelo**: sale de `python scripts/auditar_cableado.py`.
- **Inventario de prueba: 368 filas en `ACT_Activos`.** 334 son sintéticas —códigos del Plan Maestro
  repartidos por los 137 km del corredor, y cada una lo declara en `ACT_Activos.Observaciones`— y 34
  son el juego de arranque. Las familias contables suman los 355 del Plan Maestro; las 13 filas
  restantes son equipos que el Plan no cuenta por unidades.
- **`TIP_TiposActivo.RadioGeofencingKm` poblado en los 27 tipos**, por familia: 0,05 km en 18,
  0,1 km en 8 y 1,5 km en la fibra. **Al leer la aplicación esta hoja, el literal provisional de
  1,0 km dejó de aplicar**, y `PAR_Parametros.RADIO_GEOFENCING_KM` queda como valor histórico que
  `RG-01` no lee.
- Catálogos poblados: 27 tipos de activo con sus 27 formularios, 14 secciones, 10 tipos de respuesta,
  **6 sedes** —las cuatro filas `UF1` a `UF4` que ocupaban esta tabla salieron: viven en
  `UNF_UnidadesFuncionales`—, **4 unidades funcionales con las del contrato, su nombre real y sus dos
  referencias**: `PKInicial`/`PKFinal` de `00+000` a `137+170` y `PRInicial`/`PRFinal` con la ruta
  dentro, de `55CN03 PR0+0+000` a `5608 PR92+048`. Más 4 roles, 11 usuarios, 4 asignaciones de zona,
  5 motivos de pendiente, 5 modos de falla, 7 estados de orden, 3 parámetros y los catálogos viales
  de calzada, sentido, estado y frecuencia.
- **Banco de preguntas: 333 preguntas, los 27 formularios con contenido**, y 108 valores de lista.
  288 preguntas llevan `[BORRADOR: validar con operacion]`; las 45 restantes —SOS, CCTV y PMV fijo,
  15 cada uno— ya estaban acordadas.
- **Sin un solo registro transaccional.** `OT_OrdenesTrabajo`, `MAN_Mantenimientos`, `CHK_Checklists`,
  `CHD_ChecklistDetalle`, `FOT_Fotografias`, `FIR_Firmas`, `NOV_Novedades` y `PLA_PlanMantenimiento`
  están vacías. **El ciclo no se ha recorrido de extremo a extremo ni una vez.** Y eso no es solo una
  carencia: es la **ventana barata** de §2.1, el activo que se gasta la primera vez que alguien cree
  una fila en cualquiera de las ocho.

- **Las 368 coordenadas, perdidas y repuestas el 2026-08-10.** Al renombrar `Ubicacion` a
  `Ubicacion_LatLong` la columna nueva nació vacía y la vieja se retiró, y **no lo vio ninguno de los
  cinco verificadores que había**: `validar_modelo` no abre el `.xlsx`, y `verificar_reproducible`
  comparaba la pasada N con la N+1, las dos derivadas del archivo ya dañado — demostraba que el daño
  se reproducía igual. Era además una pérdida **permanente**, porque el generador lee su propia
  salida y solo completa filas nuevas. **La lección no fue restaurar del git: fue que un dato
  derivable no se conserva, se vuelve a derivar.** Hoy `generar_plantilla.py` saca la coordenada del
  `PK` sobre el trazado en cada pasada, y son **368 de 368, todas distintas**.

**Y lo que está declarado pero no se puede probar:** el geofencing. La columna ya no está vacía, y
por eso **se lee peor que antes, no mejor**: `RG-01` deja de comparar contra blanco y pasa a comparar
contra un punto que está sobre la vía pero **no frente al equipo**. Con 0,05 km de radio en 18 de los
27 tipos, **rechaza el cierre legítimo igual que antes, pero ahora sin que nada se vea vacío**. Es
D-01, y lo que se comprueba en el archivo ya no es que haya dato, sino que el dato **no está medido**:

```bash
python scripts/verificar_datos.py
python -c "import openpyxl;w=openpyxl.load_workbook('BD/Modelo_Datos_PLANTILLA.xlsx',read_only=True,data_only=True)['ACT_Activos'];h=[c.value for c in next(w.iter_rows(max_row=1))];i=h.index('Observaciones');print(sum(1 for r in w.iter_rows(min_row=2,values_only=True) if r[i] and 'SINTETICO' in str(r[i])),'filas se declaran sinteticas de las 368')"
```

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
la salida a producción y ninguna es técnica. **El documento ya no está en el repositorio**: la
carpeta `entregables/` se retiró entera en la limpieza del 2026-08-10 —`git log --diff-filter=D
--name-only -- 'entregables/*'`—, y lo que queda vivo son las tres decisiones, que se piden aquí:

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

## 4.5 Fase 0.5 — Reconciliación de modelos. CERRADA el 2026-08-07

**Qué pasó.** El 6 de agosto de 2026, al leer por primera vez el backend de producción, se encontró
que el Excel local y el Google Sheets **no eran el mismo modelo**: el Excel tenía las columnas de
GPS y no el mapeo de formularios, y producción al revés. Difería además `CHK_Checklists` y
`CHD_ChecklistDetalle`. Dos personas editaban por separado y nadie lo sabía.

**Cómo se cerró.** No eligiendo uno de los dos, que era lo que este documento proponía, sino
**sacando la verdad de los dos archivos**: desde entonces la fuente única es
`scripts/modelo_objetivo.py`, la hoja se genera de él y los documentos también. Un modelo declarado
en código no puede divergir en silencio de otro, porque solo hay uno.

**Lo que dejó decidido, y por eso no se reabre:**

| Decisión | Cómo quedó |
|---|---|
| Columnas de GPS en `MAN_Mantenimientos` | `Coordenadas_Cierre_LatLong` como `LatLong` y `Precision_GPS` como `Number`. AppSheet las había inferido mal y cruzadas |
| `EOT_EstadosOrden` | Sus claves son el nombre del estado, no `1..7`. Un catálogo se diseña mirando los datos que va a resolver |
| `IsPartOf` sobre `MAN_Mantenimientos.OTID` | **Va sin él.** La ejecución es el registro histórico y sobrevive a su orden |
| Borrado del histórico | Se retira `Deletes` en `OT_OrdenesTrabajo` y `MAN_Mantenimientos` (RG-14 y RG-15). Un error se corrige con `Activo = FALSE` |
| Reportes históricos | RG-18: un histórico nunca filtra por el estado actual del activo, o al dar de baja uno desaparecen sus mantenimientos pasados |
| Creación de órdenes desde la app | **Desbloqueada, pendiente de aplicar.** El motivo del aplazamiento era que `OTID` hacía de clave y de etiqueta legible a la vez; `ESPEC-005` lo separa —clave con `UNIQUEID()`, columna `Etiqueta` aparte— y `RG-14` ya declara `Updates, Adds`. Hasta que se aplique, las órdenes se crean en el Sheets, que **se salta todas las validaciones**: aceptable en el piloto por volumen, no como procedimiento |
| Quién edita el Sheets | **Sin resolver.** Sigue sin haber una regla escrita, y hay dos cuentas con permiso |

Las actas que cerraron esta fase, `ACTA-001` a `ACTA-004`, y las especificaciones que las produjeron
—`ESPEC-001`, `001B` y `001C`— **se retiraron en la limpieza del 2026-08-10**: estaban ejecutadas y
cerradas, y describían aplicaciones y hojas superadas. Lo que dejaron decidido es la tabla de arriba,
y eso no se reabre.

**Y lo que esta fase no arregló, porque no era suyo:** la aplicación seguía con el esquema viejo.
Eso se resolvió el 2026-08-09 reconstruyéndola, no reconciliando nada más.

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
- [ ] Situar las cinco sedes que faltan. `SED_Sedes` tiene `UnidadFuncionalID`, `PR`, `TramoINVIAS`,
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
      que arrastraba la heredada desapareció con ella: ninguno de los 211 encabezados lo tiene
- [~] **Código QR: FUERA DE ALCANCE por decisión del 7 de agosto de 2026.** Primero tiene que
      funcionar el ciclo básico. El hallazgo se conserva porque es real: `ACT_Activos.CodigoQR` está
      poblado **solo en 34 de las 368 filas** —las del juego de arranque— y su valor es una copia de
      `CodigoActivo` salvo en una, donde `SERV-001` lleva `SVR-001`; y AppSheet lee códigos pero no
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

**Las reglas están declaradas en el modelo y ninguna está puesta en la aplicación.** La versión 4.1
las daba por configuradas, y describía el cableado de una aplicación que ya no existe. Lo que queda
de esta fase son dos bloques: reponer el comportamiento, y después la **interfaz**, que además tiene
un requisito previo que no es de configuración sino de modelo.

> ### Antes de las reglas van las referencias, y cuántas faltan no se lee aquí
>
> **Diez de las 23 reglas desreferencian** —`RG-01`, `RG-04`, `RG-05`, `RG-06`, `RG-08`, `RG-09`,
> `RG-11`, `RG-16`, `RG-17` y `RG-34`; la lista se saca buscando `].[` en las expresiones del
> modelo—, y cada una **falla o, peor, resuelve contra lo que no es** si la referencia de debajo está
> mal puesta. Y «mal puesta»
> no significa ausente: el 2026-08-10, `ACT_Activos.TipoActivoID` apuntaba a `SED_Sedes`, con lo que
> cada activo leía el checklist de una sede y `RG-01` fallaba con
> `Can't find column "RadioGeofencingKm" in table "SED_Sedes"` — un mensaje que invita a reescribir
> una expresión correcta para acomodarla a un cableado roto.
>
> **Ninguna regla se cablea hasta que el auditor salga con 0 correcciones**, y hay un resto que el
> auditor **no puede juzgar**: la columna virtual inversa vive en la tabla destino, y **seis
> referencias apuntan a tablas que están vacías**, así que de ellas no dice ni bien ni mal. Se abren
> en el editor una a una, o se siembra una fila en el destino y se vuelve a correr. **Confundir «no lo
> puedo ver» con «está bien» es como se llegó a las cuatro de arriba.**
>
> ```bash
> python scripts/auditar_cableado.py
> ```

Declarado en el modelo, con su expresión completa en
[`sdd/RECONSTRUCCION_EXPRESIONES.md`](sdd/RECONSTRUCCION_EXPRESIONES.md), y **sin poner**:

- [ ] **Terminar las referencias de `ACT_Activos`.** Al correr el auditor el 2026-08-10 quedaban
      **cuatro sin poner** —`EstadoActivoID`, `FrecuenciaID`, `SentidoID` y `UnidadFuncionalID`, las
      cuatro `Ref`—, y **la cifra no se copia de aquí**: se vuelve a correr `auditar_cableado.py`,
      que reemite [`CORRECCIONES_CABLEADO.md`](CORRECCIONES_CABLEADO.md) con lo que quede
- [ ] **Mirar en el editor las seis que el auditor no puede juzgar**, una a una, y anotar su
      `Source table`. Son las que apuntan a tablas vacías: `CHD→CHK`, `CHK→MAN`, `FIR→MAN`,
      `FOT→MAN`, `MAN→OT` y la autorreferencia `OT_OrdenesTrabajo.OTOrigenID`
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
- [ ] Bots de notificación y de alerta. **Dos de los cinco no caben en el plan gratuito**: ver el
      recuadro de abajo, que corrige la versión anterior de esta línea
- [ ] **Declarar la interfaz en el modelo** —vistas, acciones y slices—, y generar de ahí el manual
      de pantallas. Mientras no exista, el paso de vistas de cualquier manual dice «se construye
      sola», que es la clase de instrucción que este proyecto tiene prohibida
- [ ] Reportes y tablero, según D-12 y D-13, encima de lo anterior

> ### Los 5 bots: dos de ellos no se pueden contar como funcionando, y no por estar mal puestos
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
