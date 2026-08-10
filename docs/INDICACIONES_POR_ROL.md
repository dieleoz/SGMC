# Indicaciones por rol — qué hace cada quien para que esto llegue a campo

**Todo lo demás del repositorio está organizado por tema. Esto está organizado por persona.**
Si usted acaba de llegar, busque su rol y empiece por ahí.

> **Escrito por rol, no por persona.** Ninguna sección nombra a nadie. Es deliberado: el mismo
> reparto sirve en otro contrato sin reescribirlo.

| | |
|---|---|
| Actualizado | 2026-08-10 |
| Verificado contra | `BD/Modelo_Datos_PLANTILLA.xlsx` y `scripts/modelo_objetivo.py` |
| El sistema | Aplicación `SISGA_-323965761-26-08-10` sobre la hoja `Modelo_Datos_10082026`. Vuélquelo con `python scripts/sistema.py` |
| Lo que este documento **no** puede verificar | El estado del editor de AppSheet. No tiene API en el plan actual |

> **Un solo sistema, y una sola hoja.** El 2026-08-10 se fijó un punto de partida: la aplicación se
> reconstruyó desde cero sobre una hoja generada del modelo, y todo lo anterior quedó superado.
> `BD/Modelo_Datos_PLANTILLA.xlsx` **es** esa hoja, la misma que está publicada como
> `Modelo_Datos_10082026`. Si un documento habla de «la hoja de producción» como algo distinto de la
> plantilla, describe el estado anterior.

---

## Lo primero, y sin adornos

**La aplicación tiene las 28 tablas dadas de alta y nada más.** Las 39 referencias, las 21 reglas,
los dos filtros de seguridad y las cuatro marcas de tiempo del servidor **están sin poner**. No es
una lista de retoques: el cableado se repone entero, y es el trabajo del Funcional.

**Nada sale a campo hasta que existan coordenadas reales.** De los **368 activos** de la hoja, 34
comparten la coordenada `4.728512, -74.114531`, que está en Bogotá, y los **334** restantes llevan
coordenada propia pero calculada sobre el trazado del corredor. Los 334 lo dicen de sí mismos en
`ACT_Activos.Observaciones`:

```
los 334  ACTIVO SINTETICO DE PRUEBA - NO ES INVENTARIO REAL
los 34   (Observaciones vacío — no llevan marca, y por eso hay que saberlo de aquí)
```

Sirven para probar el sistema. No sirven para cerrar una orden con un técnico delante.

**Los 27 formularios ya tienen banco de preguntas, pero 24 están en borrador.** `FRM_Formularios`
tiene 27 filas —eran 18 hasta el 2026-08-09, antes de separar las nueve familias que colgaban del
tipo de otra cosa—. `FRM_Preguntas` tiene **333 filas que cubren los 27**: 45 acordadas —`FRM_SOS`,
`FRM_CCTV` y `FRM_PMVF`, 15 cada uno— y **288 marcadas `[BORRADOR: validar con operacion]`** en los
otros 24.

**El borrador no es contenido acordado.** Un técnico que abra el checklist de una cámara ya no ve un
formulario vacío, pero ve preguntas que nadie de Operación ha validado, y eso puede ser peor: parece
acordado. **Validarlas solo lo puede hacer Operación**; no es configuración, es el contenido del
mantenimiento.

**Sin plan de pago no hay órdenes automáticas ni avisos.** En el plan gratuito los procesos
programados no se ejecutan, y está verificado contra la documentación oficial en
`docs/BASE_CONOCIMIENTO_APPSHEET.md` §6. Las órdenes del año se crean a mano o por carga, y nadie
avisa al supervisor de que tiene trabajo por recibir: tiene que entrar a mirar.

---

## Los cinco roles de un vistazo

| Rol | Lo que solo él puede hacer | Qué se para si no lo hace | Esfuerzo |
|---|---|---|---|
| **Funcional** | Cablear la aplicación entera —referencias, reglas, filtros, marcas de tiempo— y correr `PRUEBA-003` | La aplicación no se puede probar ni publicar | 2 a 3 jornadas |
| **Operación / Mantenimiento** | Coordenadas reales, validar los 24 bancos en borrador, y cuatro definiciones de dominio | El campo entero. Es la ruta crítica | Semanas, repartidas |
| **Dirección** | D-A propiedad del backend, D-B plan de licenciamiento | La generación automática y la salida a producción | Dos decisiones, sin trabajo técnico |
| **Propietario de la Aplicación anterior** | Confirmar sobre qué hoja opera producción y despublicar la aplicación vieja | Riesgo de dos aplicaciones escribiendo sobre el mismo backend | Un correo y un clic |
| **Quien mantenga el repositorio** | Que la documentación no vuelva a divergir del archivo | Se repite la avería que costó meses a este proyecto | Continuo, minutos por cambio |

**La ruta crítica es Operación.** El Funcional termina en unos días; Dirección decide en una reunión;
el Propietario contesta un correo. Las coordenadas y la validación de los bancos de preguntas se
miden en semanas y no las puede hacer nadie más.

---

## Cifras verificadas, y la que estaba mal

Cada una con el comando que la produce. Si alguna no cuadra dentro de un mes, mande el archivo.

| Hecho | Valor | Cómo se comprueba |
|---|---|---|
| Tablas, columnas, referencias, reglas del modelo | 28 · 202 · 38 · 20 | `python scripts/validar_modelo.py` |
| El modelo consigo mismo | 0 errores, 3 avisos, `APTO PARA DESPLEGAR` | `python scripts/validar_modelo.py` |
| La hoja contra el modelo | `FASE A CERRADA`, **52 conformes**, 0 fallos. Son menos que los 61 de las descargas antiguas y está bien: esta hoja va sin registros de prueba, así que las comprobaciones que necesitan filas se saltan | `python scripts/verificar_faseA.py "BD/Modelo_Datos_PLANTILLA.xlsx"` |
| La prosa contra el modelo | `DOCUMENTOS CONSISTENTES CON EL MODELO`, 0 fallos. **El número de documentos y de avisos se mueve** según se retira material y se declaran columnas sin decidir | `python scripts/verificar_documentos.py` |
| Pestañas | **29**: 28 de datos más `_LEEME`, que no se da de alta. **Ninguna oculta** | `python scripts/verificar_faseA.py`, reglas `F-18` y `F-19` |
| Tipos de activo y formularios | **27 y 27**, uno por tipo | `TIP_TiposActivo` y `FRM_Formularios` |
| Preguntas escritas | **333 que cubren los 27 formularios**: 45 acordadas —`FRM_SOS`, `FRM_CCTV`, `FRM_PMVF`— y **288 en borrador** | `FRM_Preguntas`; el borrador se reconoce por `[BORRADOR: validar con operacion]` en `Ayuda` |
| Activos | **368**: los 34 de fixture, con una sola coordenada en Bogotá, y **334 generados** con coordenada propia | `ACT_Activos`, columna `Ubicacion` |
| Registros de prueba | **Ninguno.** `OT`, `MAN`, `CHK`, `CHD`, `FOT`, `FIR` y `NOV` están vacías | Contar filas de esas pestañas |
| Radio de geofencing por tipo | **Poblado en los 27**: 0,05 km en 18 tipos, 0,1 km en 8, 1,5 km en la fibra | `TIP_TiposActivo.RadioGeofencingKm` |
| Umbral de GPS | **40 m** en `PAR_Parametros.UMBRAL_GPS` | `PAR_Parametros`, columna `Valor` |
| Usuarios | 11, de los cuales **2 inactivos**. Cinco tienen rol de técnico | `USR_Usuarios`, columnas `Activo` y `RolID` |
| Asignaciones de zona | **4**, para cuatro técnicos. **Son cinco los técnicos** | `ASG_AsignacionZona` contra `USR_Usuarios` |
| Roles poblados | **4** de los 12 oficios del Plan Maestro | `ROL_Roles` |

**Las 47 columnas sobrantes ya no existen: son historia.** Venían del libro heredado, y la hoja
vigente se genera del modelo. **Ocultarlas no es trabajo de nadie**, y la regla `F-19` lo comprueba
en cada verificación. Se deja aquí la derivación porque es la que hay que rehacer si alguien vuelve
a hablar de esa cifra:

```
43  columnas declaradas en CAMPOS_RETIRADOS   MAN 13 · CHK 15 · CHD 12 · OT 3
 4  columnas que están en la hoja y el modelo no declara de ninguna forma
--
47  columnas que aparecen en el formulario del técnico y no deberían
```

Las cuatro sin declarar son `USR_Usuarios.UltimaSincronizacion`, `FOT_Fotografias.Fecha`, y las
columnas `Orden` de `FRM_Formularios` y `ValorDefecto` de `FRM_Preguntas`. **Las cuatro están hoy en
`COLUMNAS_SIN_DECIDIR` y las avisa la regla D-06**, con el motivo de cada una: existen en la hoja,
nadie ha decidido si sobran, y hasta entonces no se ocultan a ciegas.

**Sobre la hoja vigente el recuento da cero**, y esa es la comprobación que importa. Se corre contra
el archivo, no contra un documento:

```bash
python - <<'EOF'
import sys, openpyxl
sys.path.insert(0,'scripts')
import modelo_objetivo as M
wb = openpyxl.load_workbook('BD/Modelo_Datos_PLANTILLA.xlsx', read_only=True, data_only=True)
total = 0
for t, d in M.MODELO.items():
    hdr = [c.value for c in next(wb[t].iter_rows(min_row=1, max_row=1)) if c.value]
    sobra = [h for h in hdr if h not in {c['nombre'] for c in d['columnas']}]
    if sobra:
        total += len(sobra)
        print(t, len(sobra), sobra)
print('TOTAL', total)
EOF
```

**Por qué se deja escrito lo que ya no existe.** Circuló una instrucción de ocultar **49**, dos de
ellas columnas vivas —`FRM_Preguntas.RequiereGPS` y `FRM_Preguntas.RequiereFirma`—, y ocultarlas
habría quitado del formulario dos campos que el sistema usa. El patrón vuelve: **una lista escrita a
mano se desvía del modelo**. La lista buena es siempre la del anexo de `MANUAL_DESPLIEGUE.md`, que
se genera y por eso no puede desviarse.

**Y las trampas eran tres, no siete.** Derivadas del modelo —columna retirada cuyo nombre coincide
con la clave de otra tabla, que es lo que hace que AppSheet la convierta a `Ref` sola— salen
exactamente tres: `CHK_Checklists.ActivoID`, `CHD_ChecklistDetalle.TipoRespuestaID` y
`OT_OrdenesTrabajo.FormularioID`. **Sobre la hoja vigente ninguna de las tres existe**, así que no
hay nada que deshacer; las marcas `TRAMPA` del manual generado lo dicen en su cabecera. Se rederiva
así:

```bash
python -c "import sys;sys.path.insert(0,'scripts');from modelo_objetivo import MODELO,CAMPOS_RETIRADOS;pk={c['nombre']:t for t,d in MODELO.items() for c in d['columnas'] if c.get('pk')};print([(t,c,pk[c]) for t,f in CAMPOS_RETIRADOS.items() for c in f if c in pk and pk[c]!=t])"
```

---

# 1. El Funcional

**Quién es.** Configura AppSheet. No programa. Es quien tiene ahora mismo el trabajo más concreto y
el que menos depende de nadie.

## Qué tiene que hacer ahora

Todo se hace en el editor de `SISGA_-323965761-26-08-10`. **La aplicación tiene las 28 tablas dadas
de alta y nada más: el cableado se repone entero.** Dos documentos, y no se solapan:

- `docs/MANUAL_DESPLIEGUE.md` dice **qué** poner, con la ficha de cada tabla columna por columna.
- `docs/GUIA_IMPLEMENTACION_FUNCIONAL.md` dice **cómo** se procede y **cómo se comprueba** cada
  etapa antes de pasar a la siguiente.
- `docs/sdd/RECONSTRUCCION_EXPRESIONES.md` §2 trae las 20 expresiones enteras, sin truncar.

**0. Antes de nada, dos comprobaciones que solo salen baratas ahora.** Recién dadas de alta las
tablas, y carísimas después:

- **Ninguna clave compuesta.** AppSheet combina dos columnas cuando no encuentra una única, y contra
  una clave compuesta **no resuelve ninguna referencia**. Deben ser 28 claves simples, todas `Text`.
- **Ninguna tabla dos veces.** Si aparece `OT_OrdenesTrabajo_1` o `Copy of…`, hay dos tablas sobre la
  misma pestaña: **las referencias se reparten y la mitad de las filas parece desaparecer, sin
  error**.

*Verificable: 28 tablas en* Data → Tables*, ningún nombre repetido, una sola casilla* `KEY` *por
tabla.*

**1. Las 39 referencias, con `IsPartOf` en las cuatro que lo llevan.**
La lista completa y en orden está en el paso 5 del manual. El orden no es alfabético: primero la
clave del destino, después quien la apunta. **`MAN_Mantenimientos.OTID` va desmarcado**, y es
deliberado.
*Verificable: cuente las columnas de tipo* `Ref`*. Tienen que ser 38.*

**2. Quitar `Deletes` en `OT_OrdenesTrabajo` y en `MAN_Mantenimientos`.**
*Data → Tables → Are updates allowed*, deje `Updates` y `Adds`, quite `Deletes`. **No es opcional y
va con el punto 1:** las cuatro referencias con `IsPartOf` crean borrado en cascada, y eso solo es
seguro porque el mantenimiento nunca se borra.
*Verificable: la casilla desmarcada en las dos tablas.*

**3. Las 21 reglas.** Las cuatro que no pueden faltar:

- **El geofencing de cierre**, en `MAN_Mantenimientos.Coordenadas_Cierre_LatLong`, comparando contra
  `[OTID].[ActivoID].[TipoActivoID].[RadioGeofencingKm]`. **El radio va por tipo y está poblado en
  los 27**; el literal `1.0` describe el sistema anterior y no se usa.
- **`Editable_If = FALSE`** en las cuatro columnas de captura —`Coordenadas_Cierre_LatLong`,
  `Precision_GPS`, `UbicacionEscaneo` y `FechaHoraEscaneo`—. **Sin esto el geofencing es
  decorativo:** el técnico arrastra el pin del mapa y cierra desde donde quiera.
- **El umbral de GPS** en `CierreConExcepcion`, con el `OR(ISBLANK(...))` entero. Sin él, borrar la
  fila del parámetro hace que **todos los cierres salgan limpios y nadie se entere**.
- **Los dos filtros de seguridad**: activos por unidad funcional, órdenes por técnico. No son solo
  control de acceso: sin ellos cada técnico se descarga el inventario entero al teléfono.

*Verificable: pegue en el reporte la expresión final de cada una, leída del editor.*

**4. Las cuatro marcas de tiempo como `ChangeTimestamp` del servidor.**
`MAN_Mantenimientos.FechaHoraRegistro`, `FOT_Fotografias.FechaHora`, `FIR_Firmas.FechaHora` y
`NOV_Novedades.FechaHora`. Un `Initial value = NOW()` lo pone el teléfono, y el usuario puede
cambiar la hora del teléfono. **Sin esto, la hora de cada fotografía y de cada firma no prueba
nada** — que es justo lo que el sistema existe para sostener.
*Verificable: el tipo de las cuatro, copiado del editor.*

**5. Las tres expresiones, en el Asistente de Expresiones y no en una columna.**

```
[OTID].[ActivoID].[Ubicacion_LatLong]              debe salir en verde
[OTID].[TecnicoID].[Correo]                debe salir en verde
REF_ROWS("OT_OrdenesTrabajo", "Activo")    anote literalmente qué dice
```

La tercera apunta a una columna que ya no es la referencia al activo. **Si el Asistente la acepta,
anótelo con su salida literal**: es la prueba de que un despliegue en verde no distingue la expresión
correcta de la trampa. Y el Asistente se cierra **sin dar a `Done`**: escribir una expresión dentro
de una columna la convierte en configuración activa, y una `App formula` **escribe en la hoja** cada
vez que se guarda la fila. Ya pasó una vez, sobre `MAN_Mantenimientos.Diagnostico`.

**6. Correr `PRUEBA-003`.** Está en `docs/sdd/PRUEBA-003-despliegue.md`. Cinco pruebas son
innegociables: `P-05`, `P-09`, `P-12`, `P-16` y `P-27`.

> **Lo que ya no tiene que hacer.** Ocultar columnas sobrantes y deshacer las tres trampas **salió
> del plan**: venían del libro heredado y la hoja vigente se genera del modelo. La etapa 6 de la
> guía funcional está marcada como retirada y trae el comando que lo comprueba. Si alguien le pasa
> una lista de 47 columnas por ocultar, es del sistema anterior.

## Decisiones que dependen de usted y de nadie más

Ninguna. **Es lo bueno de este rol: su trabajo no está bloqueado por ninguna decisión pendiente.**

Lo que sí es suyo es un criterio de método: **no cierre nada por su propio reporte.** Este proyecto
tiene tres cierres reportados que no resistieron la comprobación contra el archivo.

## Qué leer

- `docs/MANUAL_DESPLIEGUE.md` — los diez pasos y la ficha de las 28 tablas. Se genera del modelo.
- `docs/GUIA_IMPLEMENTACION_FUNCIONAL.md` — cómo se procede y cómo se comprueba cada etapa.
- `docs/sdd/RECONSTRUCCION_EXPRESIONES.md` — las 20 expresiones sin cortar.
- `docs/sdd/PRUEBA-003-despliegue.md` — cómo se demuestra que funcionó.

## Cuánto le cuesta

| | |
|---|---|
| Punto 0 y punto 1, las claves y las 39 referencias | Una jornada. Es lo más repetitivo y lo que más cuesta rehacer si sale mal |
| Puntos 2 a 5 | Media jornada. Son clics contados y expresiones que se pegan |
| Punto 6, `PRUEBA-003` | Una jornada. `P-27` sola lleva la mitad |

**Entre dos y tres jornadas en total.** Es una estimación, no una medición: la anterior decía «una a
dos» y estaba hecha sobre una aplicación que ya venía cableada.

---

# 2. Operación / Mantenimiento

**Quién es.** Quien conoce el corredor. **De este rol salen todas las decisiones que nadie más puede
tomar**, porque ninguna se resuelve leyendo documentos.

## Qué tiene que hacer ahora

**1. Levantar las coordenadas reales — decisión D-01.**
Es el bloqueo de la salida a campo, y no hay forma de rodearlo. La propuesta de la mesa de trabajo es
capturarlas en un recorrido de campo **con el mismo celular que usará el técnico**, no de un
levantamiento topográfico previo. El `ROADMAP.md` propone hacerlo como la primera orden de trabajo
del propio sistema, que es la forma barata: se prueba la aplicación y se levanta el dato en el mismo
viaje.
*Verificable: ninguna fila de* `ACT_Activos.Observaciones` *dice ya* `ACTIVO SINTETICO DE PRUEBA`
*ni* `FIXTURE DE LA FASE A`*, y las coordenadas de* `Ubicacion` *son todas distintas y están sobre
el corredor.*

**2. Validar los 24 bancos de preguntas que están en borrador.**
La hoja trae 27 formularios y **333 preguntas que cubren los 27**. Tres están acordados —`FRM_SOS`,
`FRM_CCTV` y `FRM_PMVF`, 15 preguntas cada uno— y **los otros 24 llevan sus 288 preguntas marcadas
`[BORRADOR: validar con operacion]` en la columna `Ayuda`**.

**Escritas no es acordadas, y aquí eso importa más que en otro sitio.** El técnico ya no abre un
formulario vacío: abre uno que parece acordado. Hay que leerlas, corregirlas o descartarlas, y
quitar la marca. **El día que no quede ninguna, el banco de preguntas está cerrado.** Esta es la
lista de los 24, sin nada que deducir:

```
PMV movil             Galibo mecanico       Galibo electronico    Sensor ambiental
Generador             Bascula               Fibra optica          Video wall
Switch                Router                Firewall              UPS
Servidor              NAS                   Subestacion           Bascula dinamica
Peaje carril          Peaje electronica     Estacion toma datos   Paso seguro
Switch capa 3         Computador portatil   Impresora             Camara OCR pesaje
```

**Los nueve últimos son de familias nuevas**: hasta el 2026-08-09 colgaban del tipo de otra cosa
—la impresora veía el checklist del NAS, el portátil el del servidor, el carril de peaje el de la
báscula—. Las 14 secciones de `FRM_Secciones` ya están creadas y se comparten entre formularios: no
hay que inventarlas.

*Verificable: el recuento de la marca baja de 288 a cero.* Se cuenta así, contra el archivo:

```bash
python -c "import openpyxl;s=openpyxl.load_workbook('BD/Modelo_Datos_PLANTILLA.xlsx',read_only=True,data_only=True)['FRM_Preguntas'];h=[c.value for c in next(s.iter_rows(max_row=1))];i=h.index('Ayuda');print(sum(1 for r in s.iter_rows(min_row=2,values_only=True) if '[BORRADOR' in str(r[i] or '')))"
```

**3. Responder si las unidades funcionales se subdividen.**
Hoy hay cuatro: UF1 a UF4. En otro corredor se subdividen (2,1 · 4,2). **Si aquí también, cambia el
filtro de seguridad y cambia el reparto de los 368 activos**, y cuanto antes se sepa más barato es:
después de cargar el inventario hay que retocar el inventario entero.
*Verificable: sí o no, por escrito, en el acta de la mesa.*

**4. Responder si el Sisga mantiene iluminación.**
No está en el Plan Maestro del Sisga y sí aparece en el informe de otro corredor. Si la mantiene,
falta un tipo de activo, su formulario y su cantidad. Si no, se cierra el punto y no se vuelve sobre
él.
*Verificable: sí o no. Si es que sí, la cantidad y dónde están.*

**5. Cerrar cuatro definiciones más, que ya están escritas como preguntas.**
Están en `docs/FUNCIONAL_SGMC.md` §9 y en `docs/CONTEXTO_OPERACION.md` §6. Las que más pesan:

- **¿Quién puede dar el aviso de una correctiva?** En el corredor de referencia solo pueden
  operadores autorizados, «para evitar notificar incidencias a través de terceras personas».
- **¿Hay SLA contractuales propios?** Los plazos que tenemos —2 h de respuesta y 4 h de resolución
  en criticidad total— son de otro contrato. Si el Sisga tiene los suyos, son otros números.
- **¿La prueba mensual con interventoría exige firma del interventor en la aplicación?** Hoy
  `FIR_Firmas` solo contempla la firma del técnico.
- **Los cinco activos sin ubicación física** —antivirus, licencias, certificados SSL, radios e
  internet— ¿entran al sistema por un camino sin evidencia de coordenada, o quedan fuera de alcance?

**6. Confirmar el umbral de GPS.** La hoja tiene `UMBRAL_GPS = 40` metros en `PAR_Parametros`. La
propuesta que se envió a la mesa decía 50. Son dos números distintos y hay que quedarse con uno.
*Verificable: el valor en la hoja coincide con lo que diga el acta.*

**7. Asignar zona a los técnicos que no la tienen.** `ASG_AsignacionZona` tiene 4 filas y
`USR_Usuarios` tiene 11 personas, 9 activas y **cinco con rol de técnico**. **El filtro de seguridad
descarga al celular solo los activos de las unidades funcionales asignadas**: un técnico sin fila en
esa tabla abre la aplicación y no ve nada. Falta al menos una asignación.
*Verificable: una fila de asignación por cada usuario con rol de técnico.*

## Decisiones que dependen de usted y de nadie más

| Decisión | Qué se para sin ella |
|---|---|
| **D-01, coordenadas reales** | **Todo el campo.** Un técnico no puede cerrar una orden contra una coordenada inventada |
| **Los 24 bancos en borrador** | El checklist de 24 de los 27 tipos. El técnico no ve un formulario vacío: ve uno que parece acordado y no lo está |
| **¿Se subdividen las UF?** | El filtro de seguridad y el reparto del inventario |
| **¿Hay iluminación?** | Un tipo de activo entero, con su formulario y su cantidad |
| **¿Quién avisa una correctiva?** | El flujo de correctivo, que hoy no existe en el modelo |
| **¿SLA propios?** | Toda la medición de disponibilidad |

**Y una que es de fondo.** Todo el dimensionamiento del sistema —las 1.916 órdenes preventivas al
año, los años que dura la cuota de Drive— está calculado sobre un maestro de 355 activos que se
describió como «muy similar» al del Sisga, no como el del Sisga. Es el vacío más grande que queda, y
está escrito así en `docs/CONTEXTO_OPERACION.md` §6. **Confirmar que esos 355 son los de este
corredor, o dar los que son.**

## Qué leer

- `docs/FUNCIONAL_SGMC.md` — qué hace el sistema y para quién. Su §9 es su lista de pendientes.
- `docs/CONTEXTO_OPERACION.md` — qué dicen los documentos reales, y qué falta que no está en ninguno.

## Cuánto le cuesta

| | |
|---|---|
| **D-01, coordenadas** | Un recorrido del corredor. **El repositorio no tiene una estimación verificada**: la fecha la fija usted, y el `ROADMAP` dice explícitamente que sin ella no hay cronograma |
| **Los 24 bancos en borrador** | Menos que escribirlos de cero, porque ya hay texto que corregir: una hora por tipo con quien hace ese mantenimiento, más transcribir. Entre tres y cinco jornadas repartidas. Los de SOS, CCTV y PMVF ya están acordados y sirven de molde |
| **Los puntos 3 a 6** | Una reunión. Son respuestas que usted ya tiene en la cabeza |
| **Punto 7, asignaciones** | Minutos. Son filas en una hoja |

Los puntos 3 a 7 se pueden cerrar esta semana. Los dos primeros son los que fijan el calendario.

---

# 3. Dirección

**Quién es.** Quien decide lo que no es técnico. **Dos decisiones, y ninguna requiere entender
AppSheet.**

## Qué tiene que hacer ahora

**1. D-A — decidir de quién es el backend.**
El documento de Google Sheets y las fotografías que el sistema genera pertenecen hoy a la cuenta de
un tercero. **Las imágenes consumen la cuota de Drive del propietario del documento**, no la de la
Concesión. Con los 355 activos del Plan Maestro esa cuota da **5,7 años** frente a los cinco de
retención de evidencia que el propio proyecto adoptó —alcanza y no sobra nada—, y con el corredor
completo de 500 se agota **en 4,1 años, antes de la retención**. Con los 34 activos reales de hoy
—los otros 334 de la hoja son sintéticos— da para décadas: el problema aparece al crecer, no ahora.
Las cuatro cifras salen de `python scripts/capacidad.py`, y el escenario de hoy sigue escrito sobre
34 activos porque son los reales, no los 368 de la hoja.

Las dos opciones funcionan y las dos están escritas en `docs/COMUNICACION_PROPIETARIO_APP.md` §3:
seguir sobre la hoja del tercero, o que pase a una cuenta de la Concesión.
*Verificable: una respuesta, y el correo al Propietario saliendo.*

**2. D-B — decidir el plan de licenciamiento.**
Esto no es una mejora que llegue sola con el tiempo. **En el plan gratuito los procesos programados
no se ejecutan.** Sin plan pagado:

- **Las órdenes del año se crean a mano o por carga.** El plan estima 1.916 preventivas anuales, unas
  ocho por día hábil. Alguien las teclea o alguien prepara la carga.
- **Nadie avisa al supervisor** de que tiene trabajo por recibir. Tiene que entrar a mirar.
- **No hay integración con el SCADA** para abrir correctivas: la API REST exige plan Core o superior.
- **No hay prueba automatizada** de la aplicación, por la misma razón.

Lo que cambia no es una función: **cambia cómo se opera.** Con plan de pago el sistema gestiona; sin
él, registra.

El presupuesto declarado en el plan original fue de 100 USD mensuales y la plataforma se cobra por
usuario activo. Hoy hay 11 usuarios y 9 activos. **El precio unitario vigente lo fija Google y no
está verificado en este repositorio**: hay que consultarlo antes de comprometer la cifra.
*Verificable: plan elegido y número de licencias.*

**3. Cerrar D-C, si aplica.** Si el contrato o la interventoría definen la disponibilidad de otra
forma que la propuesta, esa definición manda sobre la nuestra. Es una comprobación documental, no una
decisión.

## Decisiones que dependen de usted y de nadie más

| Decisión | Qué se para sin ella |
|---|---|
| **D-A, propiedad del backend** | Nada de inmediato. **Pero se decide antes de que haya técnicos en campo, no después**: mover el backend con evidencia dentro es mucho más caro |
| **D-B, plan de licenciamiento** | La generación automática de órdenes, los avisos al supervisor, el SCADA y la API. Y con ellos, el modo de operar |

## Qué leer

- `ESTADO.md` — dónde va el proyecto, en dos páginas.
- `docs/FUNCIONAL_SGMC.md` §7 — la lista exacta de lo que no cabe en el plan gratuito.

## Cuánto le cuesta

**Una reunión de una hora, y ningún trabajo técnico.** Lo que cuesta es el dinero de la licencia y el
trámite de mover un documento entre cuentas. Para dimensionar cualquiera de las dos:
`python scripts/capacidad.py` da las cifras de crecimiento, y no se calculan a ojo.

---

# 4. El Propietario de la Aplicación anterior

**Quién es.** Un tercero: figura como *owner* de la aplicación original y del documento de Google
Sheets que le servía de backend. **Hay una entrega a la Concesión ya prevista.**

**Ya no bloquea nada.** Lo que hacía falta de él se resolvió por otro camino. Lo que queda es avisar y
cerrar un punto.

## Qué se le pide

**Confirmar de quién es el backend a partir de ahora.** La aplicación vigente ya lee una hoja
generada del modelo, `Modelo_Datos_10082026`, así que la suya queda como respaldo. Lo que falta es
dejarlo por escrito. Es la misma decisión D-A, vista desde su lado.

**Y una cosa que se le debe:** la aplicación original quedó sin poder ejecutarse. Ya venía fallando
—era el problema que se fue a diagnosticar—, pero **dos de sus errores los introdujo este equipo** al
renombrar una tabla durante el diagnóstico. Rodar atrás no sirve: una pestaña cambió de nombre en la
hoja y cualquier versión antigua apunta a una pestaña que no existe.

**Lo razonable es despublicarla, y conviene hacerlo pronto.** Entre el 6 y el 10 de agosto quedaron
**cinco aplicaciones** en pie —las cuatro superadas están nombradas en `scripts/sistema.py` con su
motivo—. Mientras una aplicación vieja apunte a una hoja viva, sigue pudiendo escribir con permisos
que el modelo nuevo ya no concede. El backend es una hoja de cálculo: no impone unicidad, ni tipos,
ni integridad referencial.

**El documento completo, con el borrador del mensaje ya escrito, es
[`docs/COMUNICACION_PROPIETARIO_APP.md`](COMUNICACION_PROPIETARIO_APP.md).** No hay que redactar
nada: está listo para enviar.

## Cuánto cuesta

**Un correo y un clic.** Enviarlo es de Dirección o de quien lleve la relación; contestarlo, de él.

---

# 5. Quien mantenga el repositorio

**Quién es.** Quien escribe documentos, edita el modelo o genera entregables. **Su trabajo es que la
documentación no vuelva a divergir del archivo**, que es la avería que costó meses a este proyecto.

## Qué tiene que hacer, cada vez

**1. Correr los cuatro verificadores antes de dar nada por cerrado.** Ninguno sustituye a otro.

| Script | Mide | Estado hoy |
|---|---|---|
| `python scripts/validar_modelo.py` | El modelo consigo mismo | `APTO PARA DESPLEGAR`, 0 errores |
| `python scripts/verificar_faseA.py "BD/Modelo_Datos_PLANTILLA.xlsx"` | El modelo contra la hoja | `FASE A CERRADA`, 52 conformes, 0 fallos |
| `python scripts/verificar_documentos.py` | La prosa contra el modelo | `DOCUMENTOS CONSISTENTES CON EL MODELO`, 0 fallos |
| `python scripts/verificar_enlaces.py` | Que todo enlace entre documentos resuelve | Se corre al mover, renombrar o retirar cualquier documento |

**`validar_modelo.py` en 0 errores es el único gate objetivo.** Lo que ninguno mide es si algo es
buena idea.

**2. No editar a mano lo que se genera.** Un cambio de diseño se hace en `scripts/modelo_objetivo.py`
y de ahí salen `docs/ARQUITECTURA_OBJETIVO_SGMC.md`, `docs/MANUAL_DESPLIEGUE.md`,
`docs/GUIA_IMPLEMENTACION_FUNCIONAL.md` y `docs/bd.md`. Editar el documento en vez del generador
garantiza que dentro de dos días diga otra cosa que el archivo.

```
1. editar  scripts/modelo_objetivo.py
2. correr  python scripts/validar_modelo.py          -> 0 errores
3. correr  python scripts/generar_doc_arquitectura.py
```

**3. Escribir listas completas, nunca instrucciones que exijan criterio.** «Oculte las columnas
retiradas» produjo que se cableara una trampa como referencia y que alguien se inventara los valores
de un `Enum`. **Ninguno de los dos errores fue del ejecutor: fueron del documento.** Si una
instrucción dice «las retiradas» o «los valores correspondientes», está mal escrita.

**4. Al leer un `.xlsx` con `openpyxl`, `data_only=True`.** Sin él se leen fórmulas en vez de valores,
y ese fallo exacto produjo 18 huérfanos que ninguna regla veía y un diccionario generado con esa
basura. Y al revés para detectar fórmulas: hacen falta dos libros abiertos del mismo archivo.

**5. Probar una regla nueva reintroduciendo el defecto.** Si no la ve fallar, no sabe si funciona. La
regla V-17 se escribió para cazar un defecto real y **su primera versión daba falso positivo** sobre
una regla correcta.

**6. Quien aplica un cambio no toca la comprobación que lo mide.** Un cambio en `verificar_faseA.py` o
en `validar_modelo.py` propuesto por quien está siendo verificado se revisa antes de aceptarlo, y **se
prefiere endurecer la comprobación a retirarla**.

## Lo que hay que arreglar en el repositorio

Revisado el 2026-08-10. **Los cuatro puntos que había aquí están cerrados**, y se dejan anotados con
qué los cerró para que nadie los vuelva a abrir.

**1. La plantilla ya pasa la Fase A. CERRADO.** Traía cinco fallos —`F-15` sobre la fila 34 y cuatro
`F-16` de tipo mezclado en las claves— y hoy devuelve `FASE A CERRADA` con **52 conformes y 0
fallos**:

```bash
python scripts/verificar_faseA.py "BD/Modelo_Datos_PLANTILLA.xlsx"
```

Lo que enseñó sigue valiendo: **una conversión de `Text` a `Ref` conserva solo las filas cuyo valor
coincide con la clave del destino**, y AppSheet no anuncia las huérfanas. Por eso se verifica la hoja
**antes** de cablear, no después.

**2. Había dos descargas de la misma hoja y solo una pasaba. CERRADO el 2026-08-10.** Una fallaba
`F-18` con ocho pestañas ocultas y la otra no: eran el mismo libro antes y después de mostrarlas.
**AppSheet ignora las pestañas ocultas y no avisa**, así que verificar contra una y desplegar contra
la otra es exactamente el error que costó una semana. Hoy **`BD/` tiene un solo archivo**, y esa es
la forma de que el problema no vuelva.

**3. Las cifras de la prosa. CERRADO.** `verificar_documentos.py` no las habría cazado: comprueba
que los nombres existan, no que las cifras sean ciertas. **Esa es su limitación y hay que tenerla
presente** — es la razón de que cada cifra de este documento venga con el comando que la produce.

**4. La plantilla no se reproducía con un comando. CERRADO el 2026-08-10.** Hacían falta dos
scripts y varios pasos a mano —unir los libros, añadir `_LEEME`, poblar
`TIP_TiposActivo.RadioGeofencingKm`— que no estaban escritos en ningún sitio, así que había que
conservarla en vez de regenerarla. Ahora es `python scripts/generar_plantilla.py`, y dos ejecuciones
seguidas dan las 29 pestañas idénticas.

## Qué leer

- `CLAUDE.md` — las reglas de trabajo. Es lo único que no cambia cada semana.
- `docs/SDD_PIPELINE_SGMC.md` — qué pasa por el pipeline de cinco agentes y qué no.

## Cuánto le cuesta

**Minutos por cambio, si se hace en el orden correcto.** Los cuatro verificadores tardan segundos.
Los arreglos de arriba están cerrados; lo que queda es no volver a abrirlos.

---

## El orden en que se destraba

```
Esta semana    Funcional cablea la aplicación entera y corre PRUEBA-003
               Dirección decide D-A y D-B en una reunión
               Se envía el correo al Propietario, que ya está escrito
               Operación asigna zona a los técnicos que no la tienen
               Operación responde: ¿se subdividen las UF? ¿hay iluminación?
               ¿quién avisa una correctiva? ¿hay SLA propios? ¿40 o 50 metros?

Semanas        Operación valida los 24 bancos de preguntas en borrador
               Operación levanta las coordenadas reales (D-01)

Y entonces     Carga del inventario real, piloto de campo
```

**Las dos últimas líneas de la columna de semanas son la ruta crítica, y las dos son de Operación.**
Todo lo demás cabe en unos días y no espera a nadie.

---

*Este documento se escribe a mano y por eso envejece. Sus cifras se comprueban con los comandos que*
*lleva dentro. Si alguna no cuadra, manda el archivo.*
