# Indicaciones por rol — qué hace cada quien para que esto llegue a campo

**Todo lo demás del repositorio está organizado por tema. Esto está organizado por persona.**
Si usted acaba de llegar, busque su rol y empiece por ahí.

> **Escrito por rol, no por persona.** Ninguna sección nombra a nadie. Es deliberado: el mismo
> reparto sirve en otro contrato sin reescribirlo.

| | |
|---|---|
| Actualizado | 2026-08-09 |
| Verificado contra | `BD/Modelo_Datos_09082026.xlsx`, `BD/Modelo_Datos_PLANTILLA.xlsx` y `scripts/modelo_objetivo.py` |
| Lo que este documento **no** puede verificar | El estado del editor de AppSheet. No tiene API en el plan actual |

---

## Lo primero, y sin adornos

**Nada sale a campo hasta que existan coordenadas reales.** Los 34 activos de la hoja de producción
comparten la coordenada `4.728512, -74.114531`, que está en Bogotá. La plantilla trae esos 34 más
355 sintéticos con 355 coordenadas distintas repartidas sobre el corredor, y **cada fila dice de sí
misma** lo que es, en `ACT_Activos.Observaciones`:

```
las 34   FIXTURE DE LA FASE A - COORDENADA DE BOGOTA, NO ES UBICACION REAL
las 355  ACTIVO SINTETICO DE PRUEBA - NO ES INVENTARIO REAL
```

Sirven para probar el sistema. No sirven para cerrar una orden con un técnico delante.

**Diecisiete de los dieciocho formularios no tienen ni una pregunta.** `FRM_Formularios` tiene 18
filas. `FRM_Preguntas` tiene 15, y las 15 son del formulario `FRM_SOS`. Un técnico que abra el
checklist de una cámara CCTV verá un formulario vacío. **Eso solo lo puede escribir Operación**: no
es configuración, es el contenido del mantenimiento.

**Sin plan de pago no hay órdenes automáticas ni avisos.** En el plan gratuito los procesos
programados no se ejecutan, y está verificado contra la documentación oficial en
`docs/BASE_CONOCIMIENTO_APPSHEET.md` §6. Las órdenes del año se crean a mano o por carga, y nadie
avisa al supervisor de que tiene trabajo por recibir: tiene que entrar a mirar.

---

## Los cinco roles de un vistazo

| Rol | Lo que solo él puede hacer | Qué se para si no lo hace | Esfuerzo |
|---|---|---|---|
| **Funcional** | Terminar la configuración en el editor y correr `PRUEBA-003` | La aplicación no se puede probar ni publicar | 1 a 2 jornadas |
| **Operación / Mantenimiento** | Coordenadas reales, los 17 bancos de preguntas, y cuatro definiciones de dominio | El campo entero. Es la ruta crítica | Semanas, repartidas |
| **Dirección** | D-A propiedad del backend, D-B plan de licenciamiento | La generación automática y la salida a producción | Dos decisiones, sin trabajo técnico |
| **Propietario de la Aplicación anterior** | Confirmar sobre qué hoja opera producción y despublicar la aplicación vieja | Riesgo de dos aplicaciones escribiendo sobre el mismo backend | Un correo y un clic |
| **Quien mantenga el repositorio** | Que la documentación no vuelva a divergir del archivo | Se repite la avería que costó meses a este proyecto | Continuo, minutos por cambio |

**La ruta crítica es Operación.** El Funcional termina en dos días; Dirección decide en una reunión;
el Propietario contesta un correo. Las coordenadas y los bancos de preguntas se miden en semanas y no
los puede escribir nadie más.

---

## Cifras verificadas, y la que estaba mal

Cada una con el comando que la produce. Si alguna no cuadra dentro de un mes, mande el archivo.

| Hecho | Valor | Cómo se comprueba |
|---|---|---|
| Tablas, columnas, referencias, reglas del modelo | 28 · 202 · 38 · 20 | `python scripts/validar_modelo.py` |
| El modelo consigo mismo | 0 errores, 3 avisos, `APTO PARA DESPLEGAR` | `python scripts/validar_modelo.py` |
| La hoja de producción | `FASE A CERRADA`, **61 conformes**, 0 fallos | `python scripts/verificar_faseA.py "BD/Modelo_Datos_09082026.xlsx"` |
| La plantilla | `FASE A CERRADA`, **60 conformes**, 0 fallos | `python scripts/verificar_faseA.py "BD/Modelo_Datos_PLANTILLA.xlsx"` |
| La prosa contra el modelo | `DOCUMENTOS CONSISTENTES CON EL MODELO`, 0 fallos. **El número de documentos y de avisos se mueve** según se retira material a `historico/` y se declaran columnas sin decidir | `python scripts/verificar_documentos.py` |
| Formularios declarados | 18 | `FRM_Formularios`, hoja de producción |
| Preguntas escritas | **15, todas de `FRM_SOS`** | `FRM_Preguntas`, columna `FormularioID` |
| Activos en producción | 34, **una sola coordenada** | `ACT_Activos`, columna `Ubicacion` |
| Activos en la plantilla | 389: los 34 de fixture y **355 sintéticos** con coordenada propia | `BD/Modelo_Datos_PLANTILLA.xlsx` |
| Radio de geofencing por tipo | **Poblado en los 18**: 0,05 km en 12, 0,1 km en 5, 1,5 km en la fibra | `TIP_TiposActivo.RadioGeofencingKm` en la plantilla |
| Usuarios | 11, de los cuales **2 inactivos** | `USR_Usuarios`, columna `Activo` |
| Asignaciones de zona | **4**, para cuatro técnicos | `ASG_AsignacionZona` |
| Roles poblados | **4** de los 12 oficios del Plan Maestro | `ROL_Roles` |

**Las columnas sobrantes son 47, y ese número ya está corregido en todas partes.** Lo decía mal
`ESTADO.md` §2 —«51»— y lo decía mal el prompt del Funcional —«49», con dos columnas vivas dentro—.
Se deja aquí la derivación porque es la que hay que rehacer si alguien vuelve a escribir otra cifra:

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

Se reproduce así, contra el archivo y no contra un documento:

```bash
python - <<'EOF'
import sys, openpyxl
sys.path.insert(0,'scripts')
import modelo_objetivo as M
wb = openpyxl.load_workbook('BD/Modelo_Datos_09082026.xlsx', read_only=True, data_only=True)
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

**Y las 47 son de la hoja de producción, no de la plantilla.** Sobre
`BD/Modelo_Datos_PLANTILLA.xlsx` el mismo comando devuelve **cero**: esa hoja se generó del modelo y
no arrastra nada. **Si se migra a la hoja limpia, el trabajo de ocultar desaparece entero**, y con
él las tres trampas. Está medido en [`MIGRACION_HOJA_LIMPIA.md`](MIGRACION_HOJA_LIMPIA.md).

**El prompt del Funcional pedía ocultar 49, dos de ellas columnas vivas** —`FRM_Preguntas.RequiereGPS`
y `FRM_Preguntas.RequiereFirma`—, y ocultarlas habría quitado del formulario dos campos que el
sistema usa. **Ya está corregido a 47.** La lista buena sigue siendo la del anexo de
`MANUAL_DESPLIEGUE.md`, que se genera del modelo y por eso no puede desviarse.

**Y las trampas son tres, no siete.** Derivadas del modelo —columna retirada cuyo nombre coincide con
la clave de otra tabla, que es lo que hace que AppSheet la convierta a `Ref` sola— salen exactamente
tres: `CHK_Checklists.ActivoID`, `CHD_ChecklistDetalle.TipoRespuestaID` y
`OT_OrdenesTrabajo.FormularioID`. Es lo que dice el paso 6 del manual generado, y `CLAUDE.md` §7.9
ya está corregido. Se rederiva así:

```bash
python -c "import sys;sys.path.insert(0,'scripts');from modelo_objetivo import MODELO,CAMPOS_RETIRADOS;pk={c['nombre']:t for t,d in MODELO.items() for c in d['columnas'] if c.get('pk')};print([(t,c,pk[c]) for t,f in CAMPOS_RETIRADOS.items() for c in f if c in pk and pk[c]!=t])"
```

---

# 1. El Funcional

**Quién es.** Configura AppSheet. No programa. Es quien tiene ahora mismo el trabajo más concreto y
el que menos depende de nadie.

## Qué tiene que hacer ahora

Todo se hace en el editor de la aplicación `SISGA`. El guion completo está en
`docs/prompts/PROMPT_CONTINUAR_DESPLIEGUE.md`, con dos correcciones que van más abajo.

**1. Deshacer la fórmula que quedó escrita en `MAN_Mantenimientos.Diagnostico`.**
Esa columna quedó con tipo `LatLong` y una `App formula`. Una `App formula` **escribe en la hoja**
cada vez que se guarda la fila: cada mantenimiento nuevo estampa la coordenada del activo encima de
lo que hubiera. Borre la fórmula, ponga tipo `LongText`, desmarque `Show?`. Después abra la hoja y
compruebe que ninguna fila de esa columna tiene una coordenada escrita.
*Verificable: la columna sin fórmula, y las dos filas de la hoja sin coordenada.*

**2. Quitar `Deletes` en `OT_OrdenesTrabajo` y en `MAN_Mantenimientos`.**
*Data → Tables → Are updates allowed*, deje `Updates` y `Adds`, quite `Deletes`. Hay cuatro
referencias con `IsPartOf` puesto, y eso es borrado en cascada: hoy borrar un mantenimiento se lleva
sus fotografías, su firma y su checklist. **La cascada está creada y la protección no.**
*Verificable: la casilla desmarcada en las dos tablas.*

**3. Completar la regla del umbral de GPS.** En `MAN_Mantenimientos.CierreConExcepcion`, la fórmula
tiene que quedar entera, con el `OR(ISBLANK(...))` que trae el prompt en su §2. Sin él, si alguien
borra la fila del parámetro, **todos los cierres salen limpios y nadie se entera**. Con él, si el
umbral no se puede leer, el cierre se marca como excepcional.
*Verificable: pegue la fórmula final en el reporte.*

**4. Comprobar las cuatro marcas de tiempo, no darlas por hechas.**
`MAN_Mantenimientos.FechaHoraRegistro`, `FOT_Fotografias.FechaHora`, `FIR_Firmas.FechaHora` y
`NOV_Novedades.FechaHora` tienen que ser de tipo `ChangeTimestamp`. **`ESTADO.md` §1 las da por
puestas y el prompt las pide.** Ninguno de los dos se puede comprobar desde el repositorio. Ábralas y
anote lo que encuentre.
*Verificable: el tipo de las cuatro, copiado del editor.*

**5. Ocultar las 47 columnas sobrantes, con la lista del manual.**
Use el anexo de `docs/MANUAL_DESPLIEGUE.md`: ficha por tabla, columna por columna. Para cada una:
tipo `Text`, `Show?` desmarcado, sin fórmula. **No se borra ninguna.** Y en las tres trampas hay que
deshacer la referencia que AppSheet puso sola.
*Verificable: cuántas ocultó por tabla, y las tres trampas de vuelta en `Text`.*

> **Pregunte antes de empezar este punto si se va a migrar a la hoja limpia.** Si se migra, las 47
> desaparecen del archivo en vez de esconderse en la aplicación y este punto entero se tira. El
> coste de la migración está medido en [`MIGRACION_HOJA_LIMPIA.md`](MIGRACION_HOJA_LIMPIA.md): 8
> tablas de 28 y 14 reglas a reponer. **Es la única decisión que le puede ahorrar dos horas.**

**6. Las tres expresiones, en el Asistente de Expresiones y no en una columna.**

```
[OTID].[ActivoID].[Ubicacion]              debe salir en verde
[OTID].[TecnicoID].[Correo]                debe salir en verde
REF_ROWS("OT_OrdenesTrabajo", "Activo")    anote literalmente qué dice
```

La tercera apunta a una columna que ya no es la referencia al activo. **Si el Asistente la acepta,
anótelo con su salida literal**: es la prueba de que un despliegue en verde no distingue la expresión
correcta de la trampa. Y el Asistente se cierra **sin dar a `Done`**: escribir una expresión dentro
de una columna la convierte en configuración activa, que es exactamente lo que produjo el punto 1.

**7. Correr `PRUEBA-003`.** Está en `docs/sdd/PRUEBA-003-despliegue.md`. Cinco pruebas son
innegociables: `P-05`, `P-09`, `P-12`, `P-16` y `P-27`. Antes de empezar, lea su sección 2: hay tres
contradicciones entre documentos que, con usted trabajando bien, harían fallar pruebas innegociables.
La más cara es que la lista de reposición manda pegar un geofencing que compara contra una columna
vacía y **rechaza también el cierre legítimo**: el valor vigente es el literal `1.0`.

## Decisiones que dependen de usted y de nadie más

Ninguna. **Es lo bueno de este rol: su trabajo no está bloqueado por ninguna decisión pendiente.**
Puede terminar los siete puntos hoy.

Lo que sí es suyo es un criterio de método: **no cierre nada por su propio reporte.** Este proyecto
tiene tres cierres reportados que no resistieron la comprobación contra el archivo.

## Qué leer

- `docs/MANUAL_DESPLIEGUE.md` — los diez pasos y la ficha de las 28 tablas. Se genera del modelo.
- `docs/sdd/PRUEBA-003-despliegue.md` — cómo se demuestra que funcionó.

## Cuánto le cuesta

| | |
|---|---|
| Puntos 1 a 4 y 6 | Media jornada. Son clics contados |
| Punto 5, las 47 columnas | 1 a 2 horas. Es repetitivo y no tiene dificultad |
| Punto 7, `PRUEBA-003` | Una jornada. `P-27` sola lleva la mitad |

**Entre una y dos jornadas en total.** Es una estimación, no una medición.

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

**2. Escribir los 17 bancos de preguntas que faltan.**
Hay 18 formularios y preguntas escritas para uno solo. El de postes SOS tiene 15 preguntas
repartidas en secciones —estado inicial, limpieza, inspección física, pruebas funcionales, evidencia—
y sirve de molde. **Hay que hacer lo mismo para los otros 17 tipos**: CCTV, PMV fijos y móviles,
gálibos mecánicos y electrónicos, sensores ambientales, generadores, básculas, fibra, video wall,
switch, router, firewall, UPS, servidor, NAS y subestaciones.
Las 14 secciones de `FRM_Secciones` ya están creadas y se comparten entre formularios: no hay que
inventarlas.
*Verificable:* `FRM_Preguntas` *con filas para los 18 valores de* `FormularioID`.

**3. Responder si las unidades funcionales se subdividen.**
Hoy hay cuatro: UF1 a UF4. En otro corredor se subdividen (2,1 · 4,2). **Si aquí también, cambia el
filtro de seguridad y cambia el reparto de los 355 activos**, y cuanto antes se sepa más barato es:
después de cargar el inventario hay que retocar 355 filas.
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
`USR_Usuarios` tiene 11 personas, 9 de ellas activas. **El filtro de seguridad descarga al celular
solo los activos de las unidades funcionales asignadas**: un técnico sin fila en esa tabla abre la
aplicación y no ve nada. Hoy hay al menos un técnico activo en esa situación.
*Verificable: una fila de asignación por cada usuario con rol de técnico.*

## Decisiones que dependen de usted y de nadie más

| Decisión | Qué se para sin ella |
|---|---|
| **D-01, coordenadas reales** | **Todo el campo.** Un técnico no puede cerrar una orden contra una coordenada inventada |
| **Los 17 bancos de preguntas** | El checklist de 17 de los 18 tipos. El técnico abre un formulario vacío |
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
| **Los 17 bancos** | Una a dos horas por tipo con quien hace ese mantenimiento, más transcribirlo. Entre tres y cinco jornadas repartidas. El de SOS son 15 preguntas y sirve de molde |
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
completo de 500 se agota **en 4,1 años, antes de la retención**. Con los 34 de hoy da para décadas:
el problema aparece al crecer, no ahora. Las cuatro cifras salen de `python scripts/capacidad.py`.

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

**Confirmar sobre qué hoja opera la aplicación en producción.** Dos opciones, las dos funcionan: que
la aplicación nueva siga apuntando a su hoja, o que la hoja pase a la Concesión y la suya quede como
respaldo. Es la misma decisión D-A, vista desde su lado.

**Y una cosa que se le debe:** la aplicación original quedó sin poder ejecutarse. Ya venía fallando
—era el problema que se fue a diagnosticar—, pero **dos de sus errores los introdujo este equipo** al
renombrar una tabla durante el diagnóstico. Rodar atrás no sirve: una pestaña cambió de nombre en la
hoja y cualquier versión antigua apunta a una pestaña que no existe.

**Lo razonable es despublicarla, y conviene hacerlo pronto.** Si dos aplicaciones apuntan a la misma
hoja, la vieja sigue pudiendo escribir con permisos que el modelo nuevo ya no concede. El backend es
una hoja de cálculo: no impone unicidad, ni tipos, ni integridad referencial.

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

**1. Correr los tres verificadores antes de dar nada por cerrado.** Ninguno sustituye a otro.

| Script | Mide | Estado hoy |
|---|---|---|
| `python scripts/validar_modelo.py` | El modelo consigo mismo | `APTO PARA DESPLEGAR`, 0 errores |
| `python scripts/verificar_faseA.py "BD/<archivo>.xlsx"` | El modelo contra la hoja descargada | `FASE A CERRADA` sobre `Modelo_Datos_09082026.xlsx` y sobre `Modelo_Datos_PLANTILLA.xlsx` |
| `python scripts/verificar_documentos.py` | La prosa contra el modelo | `DOCUMENTOS CONSISTENTES CON EL MODELO`, 0 fallos |

**`validar_modelo.py` en 0 errores es el único gate objetivo.** Lo que ninguno mide es si algo es
buena idea.

**2. No editar a mano lo que se genera.** Un cambio de diseño se hace en `scripts/modelo_objetivo.py`
y de ahí salen `docs/ARQUITECTURA_OBJETIVO_SGMC.md`, `docs/MANUAL_DESPLIEGUE.md` y `docs/bd.md`.
Editar el documento en vez del modelo garantiza que dentro de dos días diga otra cosa que el archivo.

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

Revisado el 2026-08-09. **Dos de los tres puntos que había aquí ya están cerrados**, y se dejan
anotados con qué los cerró para que nadie los vuelva a abrir.

**1. La plantilla ya pasa la Fase A. CERRADO.** Traía cinco fallos —`F-15` sobre la fila 34 y cuatro
`F-16` de tipo mezclado en las claves— y hoy devuelve `FASE A CERRADA` con **60 conformes y 0
fallos**:

```bash
python scripts/verificar_faseA.py "BD/Modelo_Datos_PLANTILLA.xlsx"
```

Lo que enseñó sigue valiendo: **una conversión de `Text` a `Ref` conserva solo las filas cuyo valor
coincide con la clave del destino**, y AppSheet no anuncia las huérfanas. Por eso se verifica la hoja
**antes** de cablear, no después.

**2. Hay dos descargas con la misma fecha y solo una pasa. ABIERTO.**
`BD/Modelo_Datos_09082026.xlsx` falla la regla `F-18` con ocho pestañas ocultas;
`BD/Modelo_Datos_09082026.xlsx` cierra la Fase A. Son la misma hoja antes y después de
mostrar las pestañas. **AppSheet ignora las pestañas ocultas y no avisa**, así que verificar contra
la primera y desplegar contra la segunda es exactamente el error que costó una semana. Conviene
dejar una sola.

**3. Las cifras de la prosa. CERRADO.** Las tres que no cuadraban ya están corregidas: `ESTADO.md`
dice 47 y 61, y el prompt del Funcional dice 47 sin las dos columnas vivas dentro.

`verificar_documentos.py` no las habría cazado: comprueba que los nombres existan, no que las cifras
sean ciertas. **Esa es su limitación y hay que tenerla presente** — es la razón de que cada cifra de
este documento venga con el comando que la produce.

**4. La plantilla no se reproducía con un comando. CERRADO el 2026-08-10.** Hacían falta dos
scripts y varios pasos a mano —unir los libros, añadir `_LEEME`, poblar
`TIP_TiposActivo.RadioGeofencingKm`— que no estaban escritos en ningún sitio, así que había que
conservarla en vez de regenerarla. Ahora es `python scripts/generar_plantilla.py`, y dos ejecuciones
seguidas dan las 29 pestañas idénticas.

## Qué leer

- `CLAUDE.md` — las reglas de trabajo. Es lo único que no cambia cada semana.
- `docs/SDD_PIPELINE_SGMC.md` — qué pasa por el pipeline de cinco agentes y qué no.

## Cuánto le cuesta

**Minutos por cambio, si se hace en el orden correcto.** Los tres verificadores tardan segundos. Los
tres arreglos de arriba son entre media jornada y una jornada, y el primero —la plantilla— conviene
hacerlo antes de que alguien la suba.

---

## El orden en que se destraba

```
Hoy            Funcional termina los siete puntos y corre PRUEBA-003
               Dirección decide D-A y D-B en una reunión
               Se envía el correo al Propietario, que ya está escrito
               Operación asigna zona a los técnicos que no la tienen

Esta semana    Operación responde: ¿se subdividen las UF? ¿hay iluminación?
               ¿quién avisa una correctiva? ¿hay SLA propios? ¿40 o 50 metros?
               Quien mantiene el repositorio arregla la plantilla

Semanas        Operación escribe los 17 bancos de preguntas
               Operación levanta las coordenadas reales (D-01)

Y entonces     Carga del inventario real, piloto de campo
```

**Las dos últimas líneas de la columna de semanas son la ruta crítica, y las dos son de Operación.**
Todo lo demás cabe en unos días y no espera a nadie.

---

*Este documento se escribe a mano y por eso envejece. Sus cifras se comprueban con los comandos que*
*lleva dentro. Si alguna no cuadra, manda el archivo.*
