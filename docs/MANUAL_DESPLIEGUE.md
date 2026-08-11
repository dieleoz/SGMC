# Manual de despliegue — SGMC sobre AppSheet

**Para quien construye la aplicacion.** De cero a desplegada.

> **Manual por rol, no por persona.** Quien lo ejecuta es el **Funcional**: perfil que configura
> AppSheet, sin necesidad de programar. Escrito para poder replicarlo en otro contrato.

| | |
|---|---|
| Sistema | Gestion de Mantenimiento en Campo |
| Plataforma | Google AppSheet sobre Google Sheets |
| Fuente del modelo | `scripts/modelo_objetivo.py`. Este manual se genera de ahi |
| Tablas | **28** |
| Columnas | **209** |
| Referencias | **39** |
| Reglas | **23** |

## Los cinco documentos, y cual se usa cuando

**Este es el unico que hay que leer entero.** Los otros cuatro no son capitulos que falten
aqui: son **extractos que se le pasan a un ejecutor** -una persona o un agente- para que haga
una parte sin leer el resto. Si el que despliega es usted, le basta con este.

| Documento | Que es | Cuando se usa | Describe |
|---|---|---|---|
| `MANUAL_DESPLIEGUE.md` | Este. La ruta completa, de cero a aplicacion funcionando | Siempre. Es el camino | el **destino** |
| [`PROMPT_CABLEADO.md`](PROMPT_CABLEADO.md) | Encargo autocontenido de las 39 referencias y de los tipos | Se copia integro a quien cablee | el **destino** |
| [`PROMPT_EXPRESIONES.md`](PROMPT_EXPRESIONES.md) | Idem para las 23 reglas, con la **cadena de referencias** que atraviesa cada una | Se copia integro despues del cableado | el **destino** |
| [`TIPOS_ESPERADOS.md`](TIPOS_ESPERADOS.md) | La lista larga, tabla por tabla | Abierto al lado mientras se recorre *Data > Columns* | el **destino** |
| [`CORRECCIONES_CABLEADO.md`](CORRECCIONES_CABLEADO.md) | **Generado contra la aplicacion viva** | Antes de empezar, y despues de cada tanda | el **estado de HOY** |

**Cuatro describen el destino y uno el estado, y confundirlos es de lo que mas se paga.** Un
documento generado del modelo seguira diciendo que hay 39 referencias el dia que las 39 esten
puestas: no mira la aplicacion. **Solo `CORRECCIONES_CABLEADO.md` la mira.**

## Por que este manual existe

La primera version de esta aplicacion se construyo, y despues el modelo de datos se corrigio **en
la hoja**: columnas renombradas, tablas nuevas, campos retirados. **No hubo forma de que AppSheet
lo recogiera.**

Dos limites de la plataforma, los dos verificados, explican por que:

**`Regenerate` fusiona, no reemplaza.** Su documentacion dice que combina la informacion nueva con
la existente e intenta mantener las columnas que ya estan. Sirve para anadir una columna; con un
esquema muy divergente **impide converger**. El propio AppSheet indica la salida: *Delete and
re-add the table*.

**AppSheet ignora las pestanas ocultas, y no avisa.** Ocho pestanas del libro estaban ocultas y
cargaban 24 tablas de 32, sin un solo mensaje.

**Por debajo de cierto umbral se repara; por encima se reconstruye.** Este manual es el camino de
reconstruir, que resulto ser mas rapido y mas limpio.

---

## Lo que este manual no puede saber

**Todo lo que sigue sale del modelo, asi que describe el DESTINO: como tiene que quedar.** No
sabe -ni puede saber- cuanto esta hecho ya. Si esta reconstruyendo de cero da igual; si esta
retomando una aplicacion a medias, esa diferencia lo es todo.

Al estado se le pregunta con dos comandos, y no estan aqui de adorno:

```bash
python scripts/auditar_cableado.py    # que referencias estan puestas HOY
python scripts/instantanea.py         # que datos tiene la app HOY
```

**El auditor tiene un limite contraintuitivo, y conviene entenderlo antes de fiarse de el: es
mas fuerte cuando el cableado esta MAL y mas debil cuando esta bien.** No lee el esquema -la
API v2 devuelve filas, no esquema-: lee las columnas virtuales `Related ...` que AppSheet anade
en la tabla DESTINO al crear una referencia. Si hay varias referencias entre el mismo par de
tablas, AppSheet tiene que desambiguar y las llama `Related X By Columna`: ahi nombra la
columna, y la lectura es prueba. Si hay una sola, solo nombra la tabla, y para saber que
columna la produjo hay que preguntarselo al modelo, que es justo lo que se estaba verificando.

> **De ahi la consecuencia practica: no sirve para confirmar una correccion recien hecha.** Si
> alguien pone la referencia correcta en la columna equivocada, la virtual inversa se llama
> igual y el auditor dice que esta bien. Lo explica entero el docstring de
> `scripts/auditar_cableado.py`.

**Y hay un tercer estado que no es ni bien ni mal: lo que no se puede ver.** La columna virtual
vive en el destino, asi que de una referencia cuya tabla destino esta vacia el auditor no puede
decir nada. No la da por buena: la separa.

La ultima instantanea guardada -`BD/instantaneas/despues-de-la-ventana.json`- trae **953 filas** repartidas en las
28 tablas, y **8 de ellas estan vacias**:

```
  CHD_ChecklistDetalle     CHK_Checklists           FIR_Firmas
  FOT_Fotografias          MAN_Mantenimientos       NOV_Novedades
  OT_OrdenesTrabajo        PLA_PlanMantenimiento
```

**De esas 8 salen dos cosas a la vez:** sus referencias no son medibles, y sus columnas se
tiparon a ciegas -sin contenido que leer, AppSheet cae en `Text`-. Las dos vuelven en el
paso 4.

## Antes de nada: quien comprueba cada cosa

**Quien ejecuta no puede verificarse a sí mismo.** Cierra el diálogo, ve el botón en gris, y
para él la cosa quedó. El 2026-08-10 se reportó tres veces que algo estaba hecho:

```
«39/39 referencias asignadas»   ->  5 mal, 4 sin poner
«11 reglas puestas»             ->  6 bien, 1 mal, 2 sin poner
«tipos y Label listos»          ->  escribio en 2 celdas, 1 mal
```

Las tres se descubrieron después, una a una, y de ahí sale el bucle de arreglar el arreglo: cada
tanda encuentra a mano lo que la anterior dio por hecho.

Lo que las cazó no fue mirar más: fue **leer de vuelta con otro instrumento**.

| Qué se toca | Quién lo lee de vuelta |
|---|---|
| Referencias | `python scripts/auditar_cableado.py` |
| Datos | `python scripts/instantanea.py comparar <antes> <despues>` |
| Estructura | `python scripts/verificar_app.py` |
| **Tipos de columna** | **nadie: la API devuelve filas, no esquema** |
| **Expresiones y filtros** | **nadie** |
| **`Are updates allowed`** | **nadie**, y la API tiene más permisos que la app |
| **`Label`** | **nadie** |

### Y un orden que no es preferencia: los filtros de seguridad, al final

**Poner un `Security Filter` apaga los instrumentos sobre esa tabla.** La API llama sin usuario,
así que `USEREMAIL()` queda en blanco y el filtro no deja pasar nada:

```
ACT_Activos    368 filas  ->  0 por la API, en cuanto entra RG-04
auditor        6 referencias no juzgables  ->  9
```

**No se pierde ni un dato** —un filtro filtra lecturas, no borra— pero `instantanea.py` deja de
poder comparar los activos y `auditar_cableado.py` cuenta `ACT_Activos` como tabla vacía, con lo
que las tres referencias que la apuntan dejan de ser juzgables.

Así que `RG-04` y `RG-05` van **después** de haber comprobado referencias, tipos y datos. Es la
versión instrumental de la trampa de siempre: no es que esté mal, es que **deja de poderse ver**,
y eso se lee igual que «está bien» si nadie lo dice.

> **Las cuatro de abajo son las que sobrevivieron a los tres informes.** No porque nadie mirara:
> porque no había con qué. Se cierran copiando **literalmente** lo que muestra el editor, incluso
> cuando coincide. «Coincide» no es evidencia; el texto sí.

## Paso 0 — Antes de abrir AppSheet

**Comprobar la hoja.** Si algo esta mal aqui, todo lo demas hereda el error.

```bash
python scripts/verificar_faseA.py "BD/<archivo>.xlsx"
```

Tiene que decir **`FASE A CERRADA`**. Si dice otra cosa, no siga.

**Y mirar las pestanas ocultas**, que es lo que mas cuesta descubrir despues:

```bash
python -c "import openpyxl;wb=openpyxl.load_workbook('BD/<archivo>.xlsx',read_only=True);print([n for n in wb.sheetnames if wb[n].sheet_state!='visible'])"
```

Tiene que devolver **una lista vacia**. Si hay pestanas ocultas, mostrarlas en Google Sheets —
*Ver → Hojas ocultas*— antes de continuar. **`F-18` de la verificacion tambien lo detecta.**

## Paso 1 — Crear la aplicacion

En AppSheet: **Create → App → Start with existing data**, y elegir el Google Sheets.

**Fuente: el documento de Google Sheets, no un archivo subido.** Si se sube un `.xlsx`, la
aplicacion queda leyendo una foto fija y nada se sincroniza.

**Quien crea la aplicacion es su propietario.** Conviene que sea la cuenta que va a operarla: un
coautor no puede dar de alta tablas, y todo este manual consiste en eso.

## Paso 2 — Dar de alta las 28 tablas

*Data → `+` → Add data*, una por una. **En este orden**, que no es alfabetico: cada nivel apunta a
tablas cuyas claves quedaron fijadas antes.

**1. Catalogos**

```
  ROL_Roles                · SED_Sedes                · UNF_UnidadesFuncionales
  CAL_Calzadas             · SEN_Sentidos             · FRE_Frecuencias
  EST_Activo               · EOT_EstadosOrden         · MOT_MotivosPendiente
  TPR_TiposRespuesta       · PAR_Parametros
```

**2. Formularios**

```
  FRM_Formularios          · FRM_Secciones            · FRM_Preguntas
  LST_ValoresLista
```

**3. Maestras**

```
  TIP_TiposActivo          · USR_Usuarios             · ASG_AsignacionZona
  FAL_ModosFalla
```

**4. Activos**

```
  ACT_Activos
```

**5. Ordenes**

```
  OT_OrdenesTrabajo        · PLA_PlanMantenimiento    · NOV_Novedades
```

**6. Ejecucion**

```
  MAN_Mantenimientos       · CHK_Checklists           · CHD_ChecklistDetalle
  FOT_Fotografias          · FIR_Firmas
```

### Las 5 que el modelo retira

**Sobre la hoja vigente estas pestanas ya no existen.** La hoja se genera del modelo, asi que no
aparecen en el desplegable y no hay nada que evitar. La lista se conserva para reconocerlas si
alguien trabaja sobre una copia antigua:

| Pestana | Por que se retiro |
|---|---|
| `FRM_CCTV` | Hoja plana en paralelo al motor FRM_Preguntas. Se migra y se retira. |
| `FRM_PMVF` | Hoja plana en paralelo al motor FRM_Preguntas. Se migra y se retira. |
| `FRM_SOS` | Hoja plana en paralelo al motor FRM_Preguntas. Se migra y se retira. |
| `GPS` | Duplica Coordenadas_Cierre y Precision_GPS de MAN_Mantenimientos. Nunca recibio un registro. |
| `SEC_Secciones` | Duplicada con FRM_Secciones. Se consolida en una sola. |

**No lo de por hecho: compruebelo contra el archivo.** Tiene que devolver una lista vacia.

```bash
python -c "import openpyxl;n=openpyxl.load_workbook('BD/Modelo_Datos_PLANTILLA.xlsx',read_only=True).sheetnames;print([t for t in ['FRM_CCTV', 'FRM_PMVF', 'FRM_SOS', 'GPS', 'SEC_Secciones'] if t in n])"
```

**Y los bancos de preguntas que guardaban tres de ellas ya estan migrados** a `FRM_Preguntas`, que
es el motor unico. Se comprueba contando cuantos formularios distintos tienen preguntas:

```bash
python -c "import openpyxl;s=openpyxl.load_workbook('BD/Modelo_Datos_PLANTILLA.xlsx',read_only=True,data_only=True)['FRM_Preguntas'];f=[r[1] for r in s.iter_rows(min_row=2,values_only=True)];print(len(f),'preguntas en',len(set(f)),'formularios')"
```

## Paso 3 — Las claves, todas `Text`

*Data → Columns* de cada tabla. **Una sola casilla `KEY`**, sobre la columna correcta, tipo
**`Text`**.

| Tabla | Clave |
|---|---|
| `ACT_Activos` | `ActivoID` |
| `ASG_AsignacionZona` | `AsignacionID` |
| `CAL_Calzadas` | `CalzadaID` |
| `CHD_ChecklistDetalle` | `DetalleID` |
| `CHK_Checklists` | `ChecklistID` |
| `EOT_EstadosOrden` | `EstadoOrdenID` |
| `EST_Activo` | `EstadoActivoID` |
| `FAL_ModosFalla` | `ModoFallaID` |
| `FIR_Firmas` | `FirmaID` |
| `FOT_Fotografias` | `FotoID` |
| `FRE_Frecuencias` | `FrecuenciaID` |
| `FRM_Formularios` | `FormularioID` |
| `FRM_Preguntas` | `PreguntaID` |
| `FRM_Secciones` | `SeccionID` |
| `LST_ValoresLista` | `ValorListaID` |
| `MAN_Mantenimientos` | `MantenimientoID` |
| `MOT_MotivosPendiente` | `MotivoPendienteID` |
| `NOV_Novedades` | `NovedadID` |
| `OT_OrdenesTrabajo` | `OTID` |
| `PAR_Parametros` | `ParametroID` |
| `PLA_PlanMantenimiento` | `PlanID` |
| `ROL_Roles` | `RolID` |
| `SED_Sedes` | `SedeID` |
| `SEN_Sentidos` | `SentidoID` |
| `TIP_TiposActivo` | `TipoActivoID` |
| `TPR_TiposRespuesta` | `TipoRespuestaID` |
| `UNF_UnidadesFuncionales` | `UnidadFuncionalID` |
| `USR_Usuarios` | `UsuarioID` |

**`Text` sin excepcion, y hay un caso que lo justifica.** `USR_Usuarios.UsuarioID` tiene un valor
alfanumerico entre otros numericos. Si AppSheet infiere `Number`, esa fila se queda sin clave
valida y ese usuario **deja de existir para el sistema**.

**Si ve dos casillas `KEY` marcadas, o la clave aparece como combinacion de dos columnas,
corrijalo antes de seguir.** Contra una clave compuesta no resuelve ninguna referencia, y el
sintoma es que falla todo el paso 5 sin decir por que.

### Clave automatica para las filas nuevas

Estas 8 tablas crean filas desde la aplicacion. Sin esto, no sabe que identificador poner:

| Tabla | Columna | `Initial value` |
|---|---|---|
| `CHD_ChecklistDetalle` | `DetalleID` | `UNIQUEID()` |
| `CHK_Checklists` | `ChecklistID` | `UNIQUEID()` |
| `FIR_Firmas` | `FirmaID` | `UNIQUEID()` |
| `FOT_Fotografias` | `FotoID` | `UNIQUEID()` |
| `MAN_Mantenimientos` | `MantenimientoID` | `UNIQUEID()` |
| `NOV_Novedades` | `NovedadID` | `UNIQUEID()` |
| `OT_OrdenesTrabajo` | `OTID` | `UNIQUEID()` |
| `PLA_PlanMantenimiento` | `PlanID` | `UNIQUEID()` |

## Paso 4 — El tipo de las 209 columnas

**Subir el Excel arregla la hoja, no la aplicacion.** Son dos sitios distintos. El Excel fija
que columnas hay y que datos tienen; **el tipo de cada columna vive en el esquema de
AppSheet**, y ese se infiere. Reimportar no lo corrige: la inferencia vuelve a ser la misma
sobre los mismos datos.

### Este paso era una lista de excepciones, y por eso fallo

Se titulaba «los tipos que AppSheet no adivina» y enumeraba unas pocas. Eso es una **lista
blanca de excepciones sobre un default que se presume bueno**: lo que no salia en la lista se
daba por correcto por omision, sin que nadie lo hubiera decidido. La plataforma garantiza lo
contrario.

**Lo que costo.** `RG-03` se puso bien escrita y bien colocada -`[CierreConExcepcion] = TRUE`
en `Required_If`, sobre `MAN_Mantenimientos.MotivoExcepcion`- encima de una columna que
AppSheet tipo `Text`. **Comparar texto contra el booleano `TRUE` es siempre falso y no da
error:** el motivo de excepcion no se pide nunca, el tecnico cierra con excepcion sin
justificar, y la regla figura como puesta. **Existe, esta bien redactada, y es decorativa.**

Y el «que reportar» cerraba el bucle en falso -«cualquier tipo distinto del que dice este
documento»-: **nadie puede reportar una diferencia contra un valor que nunca se le dio.**

### Quien consigue el tipo de cada columna

La pregunta util no es que tipos son raros, es **quien consigue este tipo**. Lo reparte
`scripts/inferencia.py` y se comprueba en un comando:

```bash
python scripts/inferencia.py
```

| Quien lo consigue | Cuantas | Que significa |
|---|---|---|
| **Nadie: a mano** | **105** | ningun contenido de la hoja las produce, o su propio nombre empuja a AppSheet al tipo equivocado |
| El **nombre** | 17 | la cabecera lleva una palabra que AppSheet reconoce |
| El **contenido** | 87 | AppSheet deberia acertar leyendo los valores, **cuando los hay** |

**De donde sale la inferencia**, segun la documentacion oficial: AppSheet mira **el nombre de la
cabecera Y el contenido de las filas**. Las palabras que disparan un tipo son concretas
-`latlong` y `geolocation` para una coordenada, `birthday` o `day` para una fecha, una cabecera
acabada en `?` para un Yes/No-. Ver `BASE_CONOCIMIENTO_APPSHEET.md` seccion 13.

### Las 105 que no consigue nadie si no las pone usted

Por tipo: **39** `Ref` · **38** `Yes/No` · **12** `Enum` · **9** `LongText` · **4** `ChangeTimestamp` · **2** `Image` · **1** `Signature`.

**Estan ordenadas por cuantas reglas dependen de cada una**, que es lo que ordena el trabajo:
una columna mal tipada **sin** regla encima molesta al usuario; **con** una regla encima
**rompe la regla en silencio**, que es lo que paso con `RG-03`. Las 24 primeras llevan regla.

| Tabla | Columna | `TYPE` | Reglas | Por que no se consigue sola |
|---|---|---|---|---|
| `ACT_Activos` | `EstadoActivoID` | **`Ref`** → `EST_Activo` | `RG-16`, `RG-17` | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `ACT_Activos` | `UnidadFuncionalID` | **`Ref`** → `UNF_UnidadesFuncionales` | `RG-04`, `RG-34` | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `OT_OrdenesTrabajo` | `ActivoID` | **`Ref`** → `ACT_Activos` | `RG-01`, `RG-35` | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `PLA_PlanMantenimiento` | `FrecuenciaID` | **`Ref`** → `FRE_Frecuencias` | `RG-11`, `RG-36` | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `ACT_Activos` | `Activo` | **`Yes/No`** | `RG-16` | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `ACT_Activos` | `SedeID` | **`Ref`** → `SED_Sedes` | `RG-34` | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `ACT_Activos` | `TipoActivoID` | **`Ref`** → `TIP_TiposActivo` | `RG-01` | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `ASG_AsignacionZona` | `Activo` | **`Yes/No`** | `RG-04` | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `ASG_AsignacionZona` | `UnidadFuncionalID` | **`Ref`** → `UNF_UnidadesFuncionales` | `RG-04` | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `ASG_AsignacionZona` | `UsuarioID` | **`Ref`** → `USR_Usuarios` | `RG-04` | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `CHK_Checklists` | `FormularioID` | **`Ref`** → `FRM_Formularios` | `RG-09` | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `EOT_EstadosOrden` | `EsFinal` | **`Yes/No`** | `RG-37` | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `EST_Activo` | `GeneraAlerta` | **`Yes/No`** | `RG-06` | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `MAN_Mantenimientos` | `CierreConExcepcion` | **`Yes/No`** | `RG-03` | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `MAN_Mantenimientos` | `EstadoActivoID` | **`Ref`** → `EST_Activo` | `RG-06` | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `MAN_Mantenimientos` | `MotivoExcepcion` | **`LongText`** | `RG-03` | indistinguible de Text por contenido |
| `MAN_Mantenimientos` | `OTID` | **`Ref`** → `OT_OrdenesTrabajo` | `RG-01` | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `MAN_Mantenimientos` | `RequiereSegundaVisita` | **`Yes/No`** | `RG-10` | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `OT_OrdenesTrabajo` | `EstadoOrdenID` | **`Ref`** → `EOT_EstadosOrden` | `RG-37` | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `OT_OrdenesTrabajo` | `SupervisorID` | **`Ref`** → `USR_Usuarios` | `RG-05` | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `OT_OrdenesTrabajo` | `TecnicoID` | **`Ref`** → `USR_Usuarios` | `RG-05` | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `PLA_PlanMantenimiento` | `Activo` | **`Yes/No`** | `RG-38` | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `PLA_PlanMantenimiento` | `ActivoID` | **`Ref`** → `ACT_Activos` | `RG-36` | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `SED_Sedes` | `UnidadFuncionalID` | **`Ref`** → `UNF_UnidadesFuncionales` | `RG-34` | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `ACT_Activos` | `CalzadaID` | **`Ref`** → `CAL_Calzadas` | — | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `ACT_Activos` | `Criticidad` | **`Enum`** · `Alta` · `Media` · `Baja` | — | el contenido no declara el conjunto de valores permitidos |
| `ACT_Activos` | `FrecuenciaID` | **`Ref`** → `FRE_Frecuencias` | — | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `ACT_Activos` | `MotivoBaja` | **`Enum`** · `Obsolescencia` · `Dano irreparable` · `Robo o vandalismo` · `Reemplazo` · `Retiro por obra` | — | el contenido no declara el conjunto de valores permitidos |
| `ACT_Activos` | `Observaciones` | **`LongText`** | — | indistinguible de Text por contenido |
| `ACT_Activos` | `SentidoID` | **`Ref`** → `SEN_Sentidos` | — | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `CAL_Calzadas` | `Activo` | **`Yes/No`** | — | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `CHD_ChecklistDetalle` | `ChecklistID` | **`Ref`** → `CHK_Checklists` | — | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `CHD_ChecklistDetalle` | `Contestada` | **`Yes/No`** | — | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `CHD_ChecklistDetalle` | `Observacion` | **`LongText`** | — | indistinguible de Text por contenido |
| `CHD_ChecklistDetalle` | `PreguntaID` | **`Ref`** → `FRM_Preguntas` | — | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `CHD_ChecklistDetalle` | `RespuestaBoolean` | **`Yes/No`** | — | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `CHD_ChecklistDetalle` | `RespuestaLista` | **`Enum`** | — | el contenido no declara el conjunto de valores permitidos |
| `CHD_ChecklistDetalle` | `RespuestaTexto` | **`LongText`** | — | indistinguible de Text por contenido |
| `CHK_Checklists` | `Finalizado` | **`Yes/No`** | — | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `CHK_Checklists` | `MantenimientoID` | **`Ref`** → `MAN_Mantenimientos` | — | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `EOT_EstadosOrden` | `Activo` | **`Yes/No`** | — | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `EOT_EstadosOrden` | `QuienCambia` | **`Enum`** · `Sistema` · `Tecnico` · `Supervisor` | — | el contenido no declara el conjunto de valores permitidos |
| `EST_Activo` | `Activo` | **`Yes/No`** | — | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `FAL_ModosFalla` | `Activo` | **`Yes/No`** | — | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `FAL_ModosFalla` | `Criticidad` | **`Enum`** · `Alta` · `Media` · `Baja` | — | el contenido no declara el conjunto de valores permitidos |
| `FAL_ModosFalla` | `TipoActivoID` | **`Ref`** → `TIP_TiposActivo` | — | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `FIR_Firmas` | `FechaHora` | **`ChangeTimestamp`** | — | lo escribe el servidor; por contenido no se distingue de una fecha cualquiera |
| `FIR_Firmas` | `Imagen` | **`Signature`** | — | igual que Image |
| `FIR_Firmas` | `MantenimientoID` | **`Ref`** → `MAN_Mantenimientos` | — | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `FIR_Firmas` | `TipoFirma` | **`Enum`** · `Tecnico` | — | el contenido no declara el conjunto de valores permitidos |
| `FOT_Fotografias` | `Archivo` | **`Image`** | — | la celda solo lleva un nombre de archivo |
| `FOT_Fotografias` | `FechaHora` | **`ChangeTimestamp`** | — | lo escribe el servidor; por contenido no se distingue de una fecha cualquiera |
| `FOT_Fotografias` | `MantenimientoID` | **`Ref`** → `MAN_Mantenimientos` | — | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `FOT_Fotografias` | `Tipo` | **`Enum`** · `Antes` · `Despues` · `Novedad` | — | el contenido no declara el conjunto de valores permitidos |
| `FRE_Frecuencias` | `Activo` | **`Yes/No`** | — | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `FRM_Formularios` | `Activo` | **`Yes/No`** | — | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `FRM_Preguntas` | `Activo` | **`Yes/No`** | — | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `FRM_Preguntas` | `FormularioID` | **`Ref`** → `FRM_Formularios` | — | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `FRM_Preguntas` | `Obligatoria` | **`Yes/No`** | — | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `FRM_Preguntas` | `RequiereFirma` | **`Yes/No`** | — | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `FRM_Preguntas` | `RequiereFoto` | **`Yes/No`** | — | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `FRM_Preguntas` | `RequiereGPS` | **`Yes/No`** | — | su nombre dispara la inferencia a LatLong y NO lo es (observado: Precision_GPS salio LatLong el 2026-08-10 estando su tabla VACIA: no pudo ser el contenido) |
| `FRM_Preguntas` | `SeccionID` | **`Ref`** → `FRM_Secciones` | — | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `FRM_Preguntas` | `TipoRespuestaID` | **`Ref`** → `TPR_TiposRespuesta` | — | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `FRM_Secciones` | `Activo` | **`Yes/No`** | — | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `LST_ValoresLista` | `Activo` | **`Yes/No`** | — | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `LST_ValoresLista` | `PreguntaID` | **`Ref`** → `FRM_Preguntas` | — | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `MAN_Mantenimientos` | `Activo` | **`Yes/No`** | — | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `MAN_Mantenimientos` | `AprobadoSupervisor` | **`Yes/No`** | — | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `MAN_Mantenimientos` | `FechaHoraRegistro` | **`ChangeTimestamp`** | — | lo escribe el servidor; por contenido no se distingue de una fecha cualquiera |
| `MAN_Mantenimientos` | `ModoFallaID` | **`Ref`** → `FAL_ModosFalla` | — | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `MAN_Mantenimientos` | `MotivoPendienteID` | **`Ref`** → `MOT_MotivosPendiente` | — | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `MAN_Mantenimientos` | `ObservacionRechazo` | **`LongText`** | — | indistinguible de Text por contenido |
| `MAN_Mantenimientos` | `Observaciones` | **`LongText`** | — | indistinguible de Text por contenido |
| `MAN_Mantenimientos` | `OrigenApertura` | **`Enum`** · `QR` · `Lista` | — | el contenido no declara el conjunto de valores permitidos |
| `MAN_Mantenimientos` | `TecnicoID` | **`Ref`** → `USR_Usuarios` | — | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `MOT_MotivosPendiente` | `Activo` | **`Yes/No`** | — | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `MOT_MotivosPendiente` | `GeneraSeguimiento` | **`Yes/No`** | — | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `NOV_Novedades` | `ActivoID` | **`Ref`** → `ACT_Activos` | — | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `NOV_Novedades` | `Descripcion` | **`LongText`** | — | indistinguible de Text por contenido |
| `NOV_Novedades` | `Estado` | **`Enum`** · `Reportada` · `Aceptada` · `Descartada` | — | el contenido no declara el conjunto de valores permitidos |
| `NOV_Novedades` | `FechaHora` | **`ChangeTimestamp`** | — | lo escribe el servidor; por contenido no se distingue de una fecha cualquiera |
| `NOV_Novedades` | `Fotografia` | **`Image`** | — | la celda solo lleva un nombre de archivo |
| `NOV_Novedades` | `Tipo` | **`Enum`** · `Activo no inventariado` · `Falla detectada` | — | el contenido no declara el conjunto de valores permitidos |
| `NOV_Novedades` | `UsuarioID` | **`Ref`** → `USR_Usuarios` | — | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `OT_OrdenesTrabajo` | `Activo` | **`Yes/No`** | — | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `OT_OrdenesTrabajo` | `CerradaPor` | **`Ref`** → `USR_Usuarios` | — | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `OT_OrdenesTrabajo` | `OTOrigenID` | **`Ref`** → `OT_OrdenesTrabajo` | — | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `OT_OrdenesTrabajo` | `Observaciones` | **`LongText`** | — | indistinguible de Text por contenido |
| `OT_OrdenesTrabajo` | `Tipo` | **`Enum`** · `Preventivo` · `Correctivo` | — | el contenido no declara el conjunto de valores permitidos |
| `PAR_Parametros` | `Activo` | **`Yes/No`** | — | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `PAR_Parametros` | `Descripcion` | **`LongText`** | — | indistinguible de Text por contenido |
| `PLA_PlanMantenimiento` | `ResponsableID` | **`Ref`** → `USR_Usuarios` | — | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `ROL_Roles` | `Activo` | **`Yes/No`** | — | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `SED_Sedes` | `Activo` | **`Yes/No`** | — | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `SEN_Sentidos` | `Activo` | **`Yes/No`** | — | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `TIP_TiposActivo` | `Activo` | **`Yes/No`** | — | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `TIP_TiposActivo` | `Categoria` | **`Enum`** · `ITS` · `Electrico` · `Comunicaciones` · `TI` | — | el contenido no declara el conjunto de valores permitidos |
| `TIP_TiposActivo` | `FormularioID` | **`Ref`** → `FRM_Formularios` | — | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |
| `TIP_TiposActivo` | `RequiereGPS` | **`Yes/No`** | — | su nombre dispara la inferencia a LatLong y NO lo es (observado: Precision_GPS salio LatLong el 2026-08-10 estando su tabla VACIA: no pudo ser el contenido) |
| `TIP_TiposActivo` | `TieneQR` | **`Yes/No`** | — | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `TPR_TiposRespuesta` | `Activo` | **`Yes/No`** | — | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `UNF_UnidadesFuncionales` | `Activo` | **`Yes/No`** | — | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `USR_Usuarios` | `Activo` | **`Yes/No`** | — | no hay gatillo de nombre: depende de que AppSheet lea TRUE/FALSE en el contenido. VERIFICADO en 28 columnas con datos -la API devuelve Y/N, que es lo que devuelve una Yes/No y no una Text- y ABIERTO en las de tablas vacias, que es donde ya fallo: CierreConExcepcion salio Text y dejo RG-03 sin efecto (S-30) |
| `USR_Usuarios` | `RolID` | **`Ref`** → `ROL_Roles` | — | ningun contenido produce una referencia, y el prefijo de tabla rompe el parecido de nombre a proposito |

> **Ninguna de las 39 referencias se creara sola, y es deliberado.** AppSheet infiere `Ref`
> cuando el nombre de una columna se parece al de una tabla, y las nuestras llevan prefijo:
> `UNF_UnidadesFuncionales` no se parece a `UnidadFuncional`, asi que el parecido se rompe. Es
> el precio de la convencion y a la vez su proteccion: impide que AppSheet invente referencias.
> Como ponerlas es el paso 5.

### Las 17 que consigue el nombre

Deberian entrar bien porque su cabecera lleva la palabra que AppSheet reconoce. **Compruebelas
igual: es una heuristica, no una garantia.**

- `ACT_Activos.FechaBaja` → **`Date`**  ·  su nombre lo dispara (observado: ACT_Activos.FechaBaja salio DateTime estando vacia en las 368)
- `ACT_Activos.Ubicacion_LatLong` → **`LatLong`**  ·  su nombre lo dispara (documentado: 13, tabla de palabras reconocidas)
- `CHK_Checklists.FechaFin` → **`DateTime`**  ·  su nombre lo dispara (observado: ACT_Activos.FechaBaja salio DateTime estando vacia en las 368)
- `CHK_Checklists.FechaInicio` → **`DateTime`**  ·  su nombre lo dispara (observado: ACT_Activos.FechaBaja salio DateTime estando vacia en las 368)
- `FOT_Fotografias.Ubicacion_LatLong` → **`LatLong`**  ·  su nombre lo dispara (documentado: 13, tabla de palabras reconocidas)
- `MAN_Mantenimientos.Coordenadas_Cierre_LatLong` → **`LatLong`**  ·  su nombre lo dispara (documentado: 13, tabla de palabras reconocidas)
- `MAN_Mantenimientos.FechaAprobacion` → **`DateTime`**  ·  su nombre lo dispara (observado: ACT_Activos.FechaBaja salio DateTime estando vacia en las 368)
- `MAN_Mantenimientos.FechaHoraEscaneo` → **`DateTime`**  ·  su nombre lo dispara (observado: ACT_Activos.FechaBaja salio DateTime estando vacia en las 368)
- `MAN_Mantenimientos.FechaHoraFin` → **`DateTime`**  ·  su nombre lo dispara (observado: ACT_Activos.FechaBaja salio DateTime estando vacia en las 368)
- `MAN_Mantenimientos.FechaHoraInicio` → **`DateTime`**  ·  su nombre lo dispara (observado: ACT_Activos.FechaBaja salio DateTime estando vacia en las 368)
- `MAN_Mantenimientos.UbicacionEscaneo_LatLong` → **`LatLong`**  ·  su nombre lo dispara (documentado: 13, tabla de palabras reconocidas)
- `NOV_Novedades.Ubicacion_LatLong` → **`LatLong`**  ·  su nombre lo dispara (documentado: 13, tabla de palabras reconocidas)
- `OT_OrdenesTrabajo.FechaCierre` → **`DateTime`**  ·  su nombre lo dispara (observado: ACT_Activos.FechaBaja salio DateTime estando vacia en las 368)
- `OT_OrdenesTrabajo.FechaProgramada` → **`DateTime`**  ·  su nombre lo dispara (observado: ACT_Activos.FechaBaja salio DateTime estando vacia en las 368)
- `PLA_PlanMantenimiento.ProximaFecha` → **`Date`**  ·  su nombre lo dispara (observado: ACT_Activos.FechaBaja salio DateTime estando vacia en las 368)
- `SED_Sedes.Ubicacion_LatLong` → **`LatLong`**  ·  su nombre lo dispara (documentado: 13, tabla de palabras reconocidas)
- `USR_Usuarios.FechaIngreso` → **`Date`**  ·  su nombre lo dispara (observado: ACT_Activos.FechaBaja salio DateTime estando vacia en las 368)

### Las 87 que dependen del contenido

AppSheet deberia acertar leyendo los valores. La lista completa, tabla por tabla, esta en
**[`TIPOS_ESPERADOS.md`](TIPOS_ESPERADOS.md)**, que es la que se tiene abierta al recorrer el
editor. Aqui van las dos unicas cosas que hay que saber antes de mirarla:

**Una columna vacia no tiene contenido que leer, y cae en `Text`.**
Son 8 tablas enteras -las de la instantanea- mas cada columna vacia de las pobladas.

> **Y el caso que desarma la confianza en el contenido.** Una columna de texto cuyos valores
> parecen numeros se tipa `Number`. Paso el 2026-08-10 con `SED_Sedes.TramoINVIAS`: el unico
> valor cargado era `5607`, asi que salio `Number` — y los otros tramos del corredor son
> `55CN03`, que no cabe en un numero. **Tener el dato correcto no basta.**

### Como se comprueba, tabla por tabla

Al terminar de dar de alta o de regenerar una tabla, abrala en *Data > Columns* y **recorra la
columna TYPE de arriba abajo contra la ficha del anexo**. No es opcional ni es paranoia: el
defecto no se ve en la hoja ni en los datos, solo en esta pantalla. Lo que se corrige aqui
sobrevive a un `Regenerate` posterior, porque AppSheet conserva el tipo de las columnas que ya
existen.

> **Si va a automatizarlo:** los desplegables de `TYPE` son `<select>` nativos del navegador, no
> widgets propios, asi que se pueden asignar de forma determinista en vez de a base de clics.
> **La senal de que la aplicacion recogio el cambio es que el boton `SAVE` pasa de gris a
> azul**; si sigue gris, el cambio se perdera al recargar. Metodo y riesgos en
> `BASE_CONOCIMIENTO_APPSHEET.md` seccion 15. No sustituye a comprobar: quita los clics, no la
> verificacion.

## Paso 5 — Las 39 referencias

> **Cuidado con las listas de otros documentos.** Circulo una lista de **15** referencias por
> convertir, y era correcta para lo que normaba: una aplicacion existente donde otras 23 ya estaban
> puestas. Ese documento esta retirado. **Construyendo desde cero no sobrevive ninguna: son 39.**
> Si al terminar cuenta 15, siguio la lista equivocada.

Una referencia de AppSheet **guarda el valor de la clave de la tabla destino**. De ahi que el orden
importe: primero la clave del destino, despues quien la apunta.

**1. Catalogos**

```
 1  SED_Sedes.UnidadFuncionalID        -> UNF_UnidadesFuncionales
```

**2. Formularios**

```
 2  FRM_Preguntas.FormularioID         -> FRM_Formularios
 3  FRM_Preguntas.SeccionID            -> FRM_Secciones
 4  FRM_Preguntas.TipoRespuestaID      -> TPR_TiposRespuesta
 5  LST_ValoresLista.PreguntaID        -> FRM_Preguntas
```

**3. Maestras**

```
 6  TIP_TiposActivo.FormularioID       -> FRM_Formularios
 7  USR_Usuarios.RolID                 -> ROL_Roles
 8  ASG_AsignacionZona.UsuarioID       -> USR_Usuarios
 9  ASG_AsignacionZona.UnidadFuncionalID -> UNF_UnidadesFuncionales
10  FAL_ModosFalla.TipoActivoID        -> TIP_TiposActivo
```

**4. Activos**

```
11  ACT_Activos.TipoActivoID           -> TIP_TiposActivo
12  ACT_Activos.UnidadFuncionalID      -> UNF_UnidadesFuncionales
13  ACT_Activos.CalzadaID              -> CAL_Calzadas
14  ACT_Activos.SentidoID              -> SEN_Sentidos
15  ACT_Activos.SedeID                 -> SED_Sedes
16  ACT_Activos.EstadoActivoID         -> EST_Activo
17  ACT_Activos.FrecuenciaID           -> FRE_Frecuencias
```

**5. Ordenes**

```
18  OT_OrdenesTrabajo.ActivoID         -> ACT_Activos
19  OT_OrdenesTrabajo.TecnicoID        -> USR_Usuarios
20  OT_OrdenesTrabajo.SupervisorID     -> USR_Usuarios
21  OT_OrdenesTrabajo.EstadoOrdenID    -> EOT_EstadosOrden
22  OT_OrdenesTrabajo.OTOrigenID       -> OT_OrdenesTrabajo
23  OT_OrdenesTrabajo.CerradaPor       -> USR_Usuarios
24  PLA_PlanMantenimiento.ActivoID     -> ACT_Activos
25  PLA_PlanMantenimiento.FrecuenciaID -> FRE_Frecuencias
26  PLA_PlanMantenimiento.ResponsableID -> USR_Usuarios
27  NOV_Novedades.UsuarioID            -> USR_Usuarios
28  NOV_Novedades.ActivoID             -> ACT_Activos
```

**6. Ejecucion**

```
29  MAN_Mantenimientos.OTID            -> OT_OrdenesTrabajo
30  MAN_Mantenimientos.TecnicoID       -> USR_Usuarios
31  MAN_Mantenimientos.EstadoActivoID  -> EST_Activo
32  MAN_Mantenimientos.MotivoPendienteID -> MOT_MotivosPendiente
33  MAN_Mantenimientos.ModoFallaID     -> FAL_ModosFalla
34  CHK_Checklists.MantenimientoID     -> MAN_Mantenimientos   IsPartOf = TRUE
35  CHK_Checklists.FormularioID        -> FRM_Formularios
36  CHD_ChecklistDetalle.ChecklistID   -> CHK_Checklists   IsPartOf = TRUE
37  CHD_ChecklistDetalle.PreguntaID    -> FRM_Preguntas
38  FOT_Fotografias.MantenimientoID    -> MAN_Mantenimientos   IsPartOf = TRUE
39  FIR_Firmas.MantenimientoID         -> MAN_Mantenimientos   IsPartOf = TRUE
```

**Nota sobre `OT_OrdenesTrabajo.OTOrigenID`**, que sale en el nivel 5: apunta a su propia tabla,
para encadenar una orden derivada con la que la origino. **Dejela para el final del nivel.**

### `IsPartOf` va marcado en cuatro, y en ninguna mas

```
FOT_Fotografias.MantenimientoID    -> MAN_Mantenimientos
FIR_Firmas.MantenimientoID         -> MAN_Mantenimientos
CHK_Checklists.MantenimientoID     -> MAN_Mantenimientos
CHD_ChecklistDetalle.ChecklistID   -> CHK_Checklists
```

**`MAN_Mantenimientos.OTID` va DESMARCADO, y es deliberado.** Con `IsPartOf`, borrar una orden
borraria su ejecucion, sus fotografias y su firma **en cascada**. En un sistema cuyo proposito es
que la evidencia sea dificil de falsificar, eso se decide, no se hereda de un ejemplo.

### Despues de cada conversion

**Mire si aparecieron celdas en blanco donde habia valores.** Convertir a `Ref` conserva solo las
filas cuyo valor coincide con la clave del destino; las demas quedan huerfanas **sin mensaje de
error**.

### El error que AppSheet SI avisa: `cyclical table reference`

`EstadoActivoID` es la **clave** de `EST_Activo` y a la vez el nombre de la **referencia** hacia
ella en `ACT_Activos`. Son la misma palabra en dos tablas y no son la misma cosa. Si abre la
columna en la tabla equivocada y la convierte alli, AppSheet lo rechaza:

```
Column Name 'EstadoActivoID' in Schema 'EST_Activo_Schema'
contains a cyclical table reference to 'EST_Activo'.
```

Ya paso el 2026-08-10. **Y no es un caso raro: es el caso normal.** 33 de las 39 referencias
-el 85%- llevan un nombre que ademas es clave primaria en otra tabla, porque es justo lo que
produce la convencion `<Tabla>ID`.

**Antes de tocar una columna, compruebe en que tabla esta.** De los tres fallos que persigue
este manual, este es el unico que AppSheet le va a decir: el tipo mal inferido y la referencia
bien puesta hacia el destino equivocado **no avisan**.

## Paso 6 — RETIRADO. Sobre la hoja vigente no hay nada que deshacer

> **No ejecute este paso.** Se conserva numerado para que quien tenga una copia antigua del manual
> sepa que salio del plan, y para poder reconocer el problema si algun dia se trabaja sobre una
> hoja heredada.
>
> Estas columnas **no existen en la hoja vigente**, que se genera del modelo, asi que AppSheet no
> tiene nada que convertir solo. **Compruebelo usted, con la regla `F-19`:**
>
> ```bash
> python scripts/verificar_faseA.py "BD/Modelo_Datos_PLANTILLA.xlsx"
> ```
>
> ```
> ok Hoja limpia: ninguna de las 50 columnas retiradas existe ya. No hay nada que ocultar
> ```
>
> **Lo mismo vale para las marcas `OCULTAR` y `TRAMPA` del anexo:** describen una hoja que ya no se
> usa y no aplican a la vigente.

El problema que este paso resolvia: son columnas muertas que **se llaman igual que la clave de otra
tabla**. Donde existan, AppSheet infiere la referencia por coincidencia de nombre y las convierte
sin que nadie se lo pida.

| Tabla | Columna | Adonde apunta sola | Por que esta mal |
|---|---|---|---|
| `CHD_ChecklistDetalle` | `TipoRespuestaID` | `TPR_TiposRespuesta` | Se alcanza por [PreguntaID].[TipoRespuestaID]. |
| `CHK_Checklists` | `ActivoID` | `ACT_Activos` | Se alcanza por [MantenimientoID].[OTID].[ActivoID]. |
| `OT_OrdenesTrabajo` | `FormularioID` | `FRM_Formularios` | El formulario lo determina el tipo del activo, no la orden. |
| `USR_Usuarios` | `SedeID` | `SED_Sedes` | Retirada el 2026-08-10 para que el modelo diga lo que dice la especificacion. FUNCIONAL_SGMC 6.3 la declara descartada frente a ASG_AsignacionZona: la sede es un edificio y la asignacion es un tramo, y un tecnico puede atender varias unidades funcionales, asi que la relacion es de muchos a muchos y no cabe como columna. RG-04, el filtro de seguridad que decide que activos ve cada tecnico, lee la asignacion y no menciona la sede. El modelo la declaraba Ref obligatoria mientras la spec la daba por descartada: se contradecian, y cablearla habria dejado dos formas de decir donde trabaja alguien. |

**Son 4, derivadas del archivo y no escritas a mano.** Estan tambien en la ficha de cada tabla,
marcadas como TRAMPA, **y esas marcas tampoco aplican a la hoja vigente**.

Si alguna vez aparecen —trabajando sobre una copia antigua del libro—, lo que habria que hacer es
dejarlas en `Text` y desmarcar `Show?`. Como `Ref` dibujan rutas de navegacion que el modelo
prohibe y aparecen en la aplicacion como si fueran buenas.

## Paso 7 — Las 23 reglas

Las expresiones enteras, con la **cadena de referencias que atraviesa cada una**, estan en
[`PROMPT_EXPRESIONES.md`](PROMPT_EXPRESIONES.md) —que es lo que se le pasa a quien las ponga— y
con su historia en [`sdd/RECONSTRUCCION_EXPRESIONES.md`](sdd/RECONSTRUCCION_EXPRESIONES.md) §2.
**Copielas de ahi. No las escriba de memoria ni las adapte.**

### Lo primero, porque ya salio mal tres veces

**Una expresion con puntos no falla por estar mal escrita: falla porque un salto de su cadena
no esta cableado.** El error de AppSheet lo dice literalmente. Cuando `RG-01` daba esto:

```
Can't find column "RadioGeofencingKm" in table "SED_Sedes"
```

...no habia que buscar otro nombre de columna: habia que ver **por que la cadena aterrizaba en
`SED_Sedes`**. Y era que `ACT_Activos.TipoActivoID` apuntaba a la tabla de sedes.

Cuando una falle: mire la tabla que nombra el error y busquela en la columna «atraviesa» de
[`PROMPT_EXPRESIONES.md`](PROMPT_EXPRESIONES.md), que trae la cadena de cada regla desglosada
salto a salto. **Ahi esta el salto roto**, y se arregla en el paso 5, no aqui.

> **NO reescriba una expresion para que el error desaparezca.** Se propusieron dos veces dos
> arreglos que parecian razonables: sustituir el radio por un `LOOKUP` global a
> `PAR_Parametros`, y quitar un salto de la cadena.
> **El primero habria colapsado en un solo numero los 3 radios distintos** que hoy declara
> `TIP_TiposActivo`: 1,5 km (`FO`) · 0,1 km en 8 tipos · 0,05 km en 18 tipos.
> El segundo apunta a una columna que no existe.
> **Ninguno de los dos da error:** dejan el cierre en campo **aceptando lo que debe rechazar**.

### Como se prueba una expresion

En el **Asistente de Expresiones**, que solo evalua, y se cierra **sin dar a `Done`**. Escribir
una expresion dentro de una columna para probarla la convierte en **configuracion activa**: ya
ocurrio una vez, y dejo una `App formula` escribiendo coordenadas dentro de una columna
retirada.

**Y compruebe en que tabla esta antes de abrir la columna**, por lo que dice el paso 5: el
mismo nombre es clave en una tabla y referencia en otra.

### Las 23, y las 9 que van al final

| # | Regla | Tabla | Columna | Propiedad | Escribe |
|---|---|---|---|---|---|
| 1 | RG-01 | `MAN_Mantenimientos` | `Coordenadas_Cierre_LatLong` | Valid_If | no |
| 2 | RG-03 | `MAN_Mantenimientos` | `MotivoExcepcion` | Required_If | no |
| 3 | RG-04 | `ACT_Activos` | `(tabla)` | Security Filter | no |
| 4 | RG-05 | `OT_OrdenesTrabajo` | `(tabla)` | Security Filter | no |
| 5 | RG-13 | `MAN_Mantenimientos` | `(tabla)` | Verificacion de evidencia | no |
| 6 | RG-14 | `OT_OrdenesTrabajo` | `(tabla)` | Are updates allowed | no |
| 7 | RG-15 | `MAN_Mantenimientos` | `(tabla)` | Are updates allowed | no |
| 8 | RG-17 | `ACT_Activos` | `FechaBaja` | Required_If | no |
| 9 | RG-18 | `ACT_Activos` | `(tabla)` | Doctrina de reportes | no |
| 10 | RG-20 | `MAN_Mantenimientos` | `(varias)` | Editable_If | no |
| 11 | RG-34 | `ACT_Activos` | `UnidadFuncionalID` | Valid_If | no |
| 12 | RG-38 | `PLA_PlanMantenimiento` | `(tabla)` | Accion | no |
| 13 | RG-39 | `FOT_Fotografias` | `Ubicacion_LatLong` | Editable_If | no |
| 14 | RG-40 | `NOV_Novedades` | `Ubicacion_LatLong` | Editable_If | no |
| 15 | RG-06 | `MAN_Mantenimientos` | `(tabla)` | Bot | **SI** |
| 16 | RG-07 | `OT_OrdenesTrabajo` | `(tabla)` | Bot | **SI** |
| 17 | RG-09 | `CHK_Checklists` | `VersionFormulario` | Initial value | **SI** |
| 18 | RG-10 | `MAN_Mantenimientos` | `(tabla)` | Bot | **SI** |
| 19 | RG-11 | `PLA_PlanMantenimiento` | `ProximaFecha` | App formula | **SI** |
| 20 | RG-16 | `ACT_Activos` | `Activo` | App formula | **SI** |
| 21 | RG-35 | `OT_OrdenesTrabajo` | `(tabla)` | App formula | **SI** |
| 22 | RG-36 | `PLA_PlanMantenimiento` | `(tabla)` | App formula | **SI** |
| 23 | RG-37 | `OT_OrdenesTrabajo` | `(tabla)` | App formula | **SI** |

### Las 9 que escriben en la hoja van al final, y antes se toma una instantanea

Las de `App formula`, `Initial value` y las de tipo bot **escriben en la hoja**. A diferencia de
un tipo de columna, **lo que escriben no se revierte cambiando un desplegable**: hay que saber
que habia antes. Por eso van las ultimas, cuando ya se puede comprobar que escribieron.

```bash
python scripts/instantanea.py guardar antes-de-las-que-escriben
#   ... se ponen las 9 ...
python scripts/instantanea.py guardar despues
python scripts/instantanea.py comparar antes-de-las-que-escriben despues
```

**Y no basta con mirar la fila que se espera que cambie.** Una `App formula` se evalua sobre
**todas** las filas de su tabla: `RG-16` sola se evalua sobre los **368** activos, no sobre el
unico que deberia cambiar. Si la expresion esta mal, escribe en todos y **no da error: da
datos**. Por eso el criterio de cierre no es «la fila esperada quedo bien», es **«no cambio
ninguna celda»** — y eso exige la fotografia previa.

### Las cuatro que no pueden faltar

**Geofencing** — en `MAN_Mantenimientos.Coordenadas_Cierre_LatLong`:

```
Initial value:  HERE()
Valid_If:       DISTANCE([Coordenadas_Cierre_LatLong], [OTID].[ActivoID].[Ubicacion_LatLong])
                  <= [OTID].[ActivoID].[TipoActivoID].[RadioGeofencingKm]
Invalid text:   Ubicacion fuera de rango: debe estar junto al activo para cerrar.
Editable_If:    FALSE
```

**El radio va por tipo de activo, no como literal.** Una subestacion y un poste SOS no admiten
la misma tolerancia, y un tramo de fibra es lineal. `PAR_Parametros.RADIO_GEOFENCING_KM` queda
como valor provisional historico: **la regla no lo lee.**

**Antes de pegarla, compruebe que la columna esta poblada**, porque contra celdas en blanco esta
expresion **rechaza tambien los cierres legitimos**:

```bash
python -c "import openpyxl;s=openpyxl.load_workbook('BD/Modelo_Datos_PLANTILLA.xlsx',read_only=True,data_only=True)['TIP_TiposActivo'];h=[c.value for c in next(s.iter_rows(max_row=1))];i=h.index('RadioGeofencingKm');v=[r[i] for r in s.iter_rows(min_row=2,values_only=True)];print(len(v),'tipos,',sum(1 for x in v if x not in (None,'')),'con radio')"
```

Sobre la hoja vigente devuelve **27 tipos, 27 con radio**. Si devuelve alguno sin radio, pare:
ese tipo de activo no se podra cerrar en campo.

**No editables** — en `MAN_Mantenimientos`, `Editable_If = FALSE` en las tres columnas de
captura (no cuatro: desde ESPEC-004/ORDEN-004 `Precision_GPS` se retiro del modelo):

```
Coordenadas_Cierre_LatLong · UbicacionEscaneo_LatLong · FechaHoraEscaneo
```

**Sin esto el geofencing es decorativo:** el tecnico arrastra el pin del mapa y cierra desde
donde quiera. La regla parece funcionar y no prueba nada.

> **Supuesto sin verificar, y es el peor modo de fallo del sistema.** No hay pagina oficial que
> confirme si AppSheet evalua un `Valid_If` sobre una columna con `Editable_If = FALSE`. **Si no
> lo evalua, la regla parece funcionar por no ejercitarse nunca.** Se detecta asi: pruebe un
> cierre cercano y uno lejano. **Si los dos salen aceptados, sospeche de esto antes que del
> radio.**

**Excepcion por GPS deficiente** — en `MAN_Mantenimientos.CierreConExcepcion`:

`RG-19`, el `App formula` que calculaba esta columna con `Precision_GPS`, se retiro con
ESPEC-004/ORDEN-004 (`USERLOCATIONACCURACY()` no existe en AppSheet, la columna nunca se
poblaba). Hoy `CierreConExcepcion` es una casilla `Yes/No` **libre**, sin `App formula`, que
marca el propio tecnico:

```
Type:          Yes/No
App formula:   (vacio)
Description:   "¿La app no alcanzó buena precisión al capturar la posición de cierre? Marque
               si es así." (a mano; ningun generador emite Description — ESPEC-004 2.13)
```

**Confirme el `Type` antes de dar por buena esta tabla.** Si `CierreConExcepcion` quedo `Text`
(el escenario que documenta `S-30`), `RG-03` —que compara contra el booleano `TRUE`— deja de
pedir el motivo aunque la casilla se marque, sin ningun mensaje de error (`ESPEC-004` §2.7).

`PAR_Parametros.UMBRAL_GPS` se conserva sin lector automatico: es la referencia que el tecnico
consulta para decidir si marca la casilla, no una comparacion que corra sola.

**Filtros de seguridad** — *Data → Tables → [tabla] → Security Filter*:

```
ACT_Activos:
IN([UnidadFuncionalID], SELECT(ASG_AsignacionZona[UnidadFuncionalID],
   AND([UsuarioID].[Correo] = USEREMAIL(), [Activo] = TRUE)))

OT_OrdenesTrabajo:
OR([TecnicoID].[Correo] = USEREMAIL(), [SupervisorID].[Correo] = USEREMAIL())
```

**No son solo control de acceso: son rendimiento.** Sin ellos, cada tecnico se descarga el
inventario entero al telefono.

### Retirar el borrado — sin esto el `IsPartOf` es peligroso

*Data → Tables → [tabla] → Are updates allowed*:

```
OT_OrdenesTrabajo    Updates si · Adds si · Deletes NO
MAN_Mantenimientos   Updates si · Adds si · Deletes NO
```

**Es la otra mitad del paso 5.** Marcar `IsPartOf` en cuatro referencias crea **borrado en
cascada**: borrar un mantenimiento se lleva sus fotografias, su firma y su checklist.

Eso solo es seguro **porque el mantenimiento nunca se borra**, y eso es exactamente lo que hace
quitar `Deletes`. Configurar el `IsPartOf` sin esto deja la cascada abierta.

## Paso 8 — Las vistas

**Este manual no especifica las vistas, y hay que saberlo antes de empezar el paso.** El modelo
declara datos, no interfaz: `VISTAS`, `ACCIONES` y `SLICES` **no existen** en
`scripts/modelo_objetivo.py` —comprobado al generar este manual, no de memoria—. Por eso aqui no
hay ficha columna por columna como en los pasos anteriores, y por eso lo que decida en este paso
es lo unico que no queda escrito en ninguna parte.

**Lo unico que AppSheet crea solo son las columnas virtuales `Related ...`**, que aparecen al poner
las referencias del paso 5 y traen con ellas la navegacion padre-hijo: al abrir un mantenimiento se
ven sus fotografias y su firma; al abrir un activo, sus ordenes. **Eso es todo lo que se construye
solo.** Las pantallas no.

**Y no se configuran a ojo.** Las tres de abajo van con el tipo y la tabla que dice la ficha; si
una no encaja, no la improvise: **anote que falta y siga**. Una vista inventada aqui es
configuracion activa que nadie declaro y que el siguiente que reconstruya la aplicacion no podra
reproducir.

| Vista | Tipo | Sobre | Nota |
|---|---|---|---|
| Mapa de activos | `Map` | `ACT_Activos` | Columna de mapa: `Ubicacion_LatLong` |
| Mis ordenes | `Deck` | `OT_OrdenesTrabajo` | Es la pantalla de trabajo del tecnico |
| Mantenimientos | `Table` | `MAN_Mantenimientos` | |

**Anote lo que haga.** Es la unica constancia que va a quedar de este paso.

## Paso 9 — Verificar antes de publicar

**No lo de por cerrado usted.** Este proyecto tiene tres cierres reportados que no resistieron la
comprobacion contra el archivo, y las tres veces lo paro un script.

**La cadena navega** — en el Asistente de Expresiones, sobre `MAN_Mantenimientos`:

```
[OTID].[ActivoID].[Ubicacion_LatLong]
[OTID].[TecnicoID].[Correo]
```

Las dos en verde. Si la primera falla, casi siempre es `OT_OrdenesTrabajo.ActivoID`, que la lista
antigua de 15 no incluia.

**Cuente las referencias.** Las columnas de tipo `Ref` deben sumar **39**.

**Y los seis verificadores del repositorio:**

```bash
python scripts/validar_modelo.py          # el modelo consigo mismo
python scripts/verificar_faseA.py "..."   # el modelo contra la hoja
python scripts/verificar_documentos.py    # la prosa contra el modelo
python scripts/verificar_enlaces.py       # que todo enlace entre documentos resuelve
python scripts/verificar_reproducible.py  # que generar dos veces da el mismo archivo
python scripts/verificar_datos.py         # que los DATOS sostienen lo que el modelo declara
```

**Ninguno de los seis mira la aplicacion:** todos comparan el modelo, la hoja y la prosa entre
si. Los dos que si la miran son los del principio —`auditar_cableado.py` e `instantanea.py`—, y
ninguno de los dos lee el esquema, porque la API devuelve filas. **De lo que hay configurado en
el editor, la unica prueba es haberlo mirado ahi.** Para lo demas estan las pruebas de
aceptacion de [`sdd/PRUEBA-003-despliegue.md`](sdd/PRUEBA-003-despliegue.md).

## Paso 10 — Publicar

> **Antes de publicar, lea esto.** Ninguna de las coordenadas de `ACT_Activos` se levanto en campo.
> Las **368** se **derivan del PK sobre el trazado del corredor** en cada pasada del generador:
> son todas distintas y todas estan sobre la via, pero **ninguna esta medida**. Con los radios
> por tipo —0,05 km en 18 de los 27 tipos— la aplicacion
> **rechaza todo cierre hecho en via y acepta todo cierre hecho en Bogota**.
>
> **No es un defecto de la configuracion: faltan las coordenadas reales**, que es la decision
> D-01. Publicar antes de cargarlas entrega un sistema donde ningun tecnico puede cerrar una
> orden, y se descubre con el tecnico delante.

*Manage → Deploy → Run deployment check*, y despues **Move app to Deployed state**.

**Antes de publicar, si existe una aplicacion anterior sobre la misma hoja, despubliquela.** Dos
aplicaciones sobre un backend sin integridad referencial es una fuente de corrupcion silenciosa:
la vieja conserva permisos de anadir y borrar que el modelo nuevo ya no concede.

## Reversion — hasta donde se puede volver atras

**Todo lo anterior al paso 10 se puede abandonar sin coste.** La aplicacion no esta publicada y
nadie la usa: se borra y se empieza de nuevo. La hoja no se toca en ningun paso salvo el 0.

**El paso 0 SI escribe en la hoja** al mostrar las pestanas ocultas. Antes de empezar, haga una
copia fechada del documento. Es el unico punto de restauracion del dato.

**El punto de no retorno es el paso 10**, y no por publicar: por **despublicar la aplicacion
anterior**. Si el *deployment check* falla despues, la vieja ya no esta en servicio. Compruebe
todo el paso 9 **antes** de despublicar nada.

### Lo que no se puede deshacer con un comando

**Antes de cambiar un tipo o una referencia, anote el valor que tenia.** Suena a burocracia y
no lo es: **no hay ningun comando en este repositorio que lo recupere despues.** La API v2 de
AppSheet devuelve **filas, no esquema**, asi que no se le puede preguntar de que tipo era una
columna ni adonde apuntaba una referencia. Es el mismo limite por el que
`auditar_cableado.py` tiene que leer de rebote las columnas virtuales `Related ...`.

Una linea por cambio basta, y es lo unico que hay:

```
ACT_Activos.TipoActivoID    estaba: Ref -> SED_Sedes     lo dejo: Ref -> TIP_TiposActivo
SED_Sedes.TramoINVIAS       estaba: Number               lo dejo: Text
```

**Y para las 9 reglas que escriben en la hoja, la anotacion no sirve: hace falta la
instantanea.** Lo que escriben no vive en el esquema, vive en el dato, y hay que haberlo
fotografiado **antes**:

```bash
python scripts/instantanea.py guardar antes-de-las-que-escriben
```

Sin esa foto, la comparacion posterior no tiene contra que compararse, y una `App formula`
equivocada no deja rastro de error: deja datos.

## Lo que NO cabe en el plan gratuito

No es *mas adelante*: es **no en este plan**. Solo cambia con la decision de licenciamiento.

| Lo que se querria | Por que no |
|---|---|
| Generacion automatica de las ordenes del mes | Los procesos programados no se ejecutan |
| Aviso al supervisor de que hay trabajo por recibir | Lo mismo |
| Integracion con sistemas externos | Sin plan Core no hay API REST |
| Atributos distintos por tipo de equipo | El backend es una hoja: no hay esquema dinamico |
| Que una escritura directa en la hoja respete las validaciones | Imposible por diseno |

**Ese ultimo importa mas de lo que parece.** Todas las garantias del sistema viven en la capa de
aplicacion. Quien escriba en la hoja se las salta todas. Lo que el sistema puede ofrecer es que
falsificar cueste mas que hacer el trabajo, no que sea imposible.

---
*Generado de `scripts/modelo_objetivo.py` por `scripts/generar_manual_despliegue.py`.*
*Para actualizarlo, cambie el modelo y vuelva a generar.*
---

# Anexo — Ficha de cada tabla

**Columna por columna, sin nada que deducir.** Esta es la referencia contra la que se configura y
contra la que se valida. Si una columna no aparece aqui, no deberia estar visible en la app.

> ## Las marcas `OCULTAR` y `TRAMPA` NO aplican a la hoja vigente
>
> **Describen una hoja que ya no se usa:** el libro heredado que arrastraba columnas que el modelo
> no declara. **La hoja vigente se genera del modelo y no trae ninguna**, asi que no hay nada que
> ocultar ni ninguna referencia que deshacer. Ignore las dos marcas.
>
> Se conservan por una sola razon: son la lista por nombre que permite reconocer esas columnas si
> algun dia aparece una copia antigua del libro. **No son trabajo de nadie.**
>
> **Compruebelo, con la regla `F-19`:**
>
> ```bash
> python scripts/verificar_faseA.py "BD/Modelo_Datos_PLANTILLA.xlsx"
> ```
>
> ```
> ok Hoja limpia: ninguna de las 50 columnas retiradas existe ya. No hay nada que ocultar
> ```
>
> La plantilla se rehace entera con `python scripts/generar_plantilla.py` y sale con las columnas
> que el modelo declara, ni una mas.

Leyenda:

- **CLAVE** — casilla `KEY` marcada, tipo `Text`
- **`Ref` -> Tabla** — tipo `Ref` con esa tabla como *Source table*
- **IsPartOf** — ademas, casilla `Is a part of` marcada
- **OCULTAR** — **no aplica a la hoja vigente.** Columna retirada del modelo que el libro heredado
  arrastraba. Si apareciera: tipo `Text`, `Show?` desmarcado, sin formula
- **TRAMPA** — **no aplica a la hoja vigente.** Donde exista, AppSheet la convierte a `Ref` sola
  por coincidencia de nombre
- **SIN DECIDIR** — esta en la hoja y el modelo no la declara

## `ACT_Activos`

Inventario de los activos del corredor. Es el eje del sistema.

| Columna | Tipo | Que hacer |
|---|---|---|
| `ActivoID` | `Text` | **CLAVE** |
| `CodigoActivo` | `Text` |  |
| `Nombre` | `Text` |  |
| `TipoActivoID` | `Ref` | `Ref` -> `TIP_TiposActivo` · IsPartOf desmarcado |
| `UnidadFuncionalID` | `Ref` | `Ref` -> `UNF_UnidadesFuncionales` · IsPartOf desmarcado |
| `PR` | `Text` |  |
| `CalzadaID` | `Ref` | `Ref` -> `CAL_Calzadas` · IsPartOf desmarcado |
| `SentidoID` | `Ref` | `Ref` -> `SEN_Sentidos` · IsPartOf desmarcado |
| `Ubicacion_LatLong` | `LatLong` |  |
| `PK` | `Text` |  |
| `TramoINVIAS` | `Text` |  |
| `SedeID` | `Ref` | `Ref` -> `SED_Sedes` · IsPartOf desmarcado |
| `EstadoActivoID` | `Ref` | `Ref` -> `EST_Activo` · IsPartOf desmarcado |
| `CodigoQR` | `Text` |  |
| `FrecuenciaID` | `Ref` | `Ref` -> `FRE_Frecuencias` · IsPartOf desmarcado |
| `Criticidad` | `Enum` | Valores: `Alta` · `Media` · `Baja` |
| `FechaBaja` | `Date` |  |
| `MotivoBaja` | `Enum` | Valores: `Obsolescencia` · `Dano irreparable` · `Robo o vandalismo` · `Reemplazo` · `Retiro por obra` |
| `Activo` | `Yes/No` |  |
| `Observaciones` | `LongText` |  |

## `ASG_AsignacionZona`

Que unidades funcionales atiende cada tecnico. Resuelve el supuesto D-03: un tecnico puede tener varias, de modo que la relacion es de muchos a muchos y no cabe como columna en USR_Usuarios.

| Columna | Tipo | Que hacer |
|---|---|---|
| `AsignacionID` | `Text` | **CLAVE** |
| `UsuarioID` | `Ref` | `Ref` -> `USR_Usuarios` · IsPartOf desmarcado |
| `UnidadFuncionalID` | `Ref` | `Ref` -> `UNF_UnidadesFuncionales` · IsPartOf desmarcado |
| `Activo` | `Yes/No` | `Initial value` = `TRUE` |

## `CAL_Calzadas`

Calzadas del corredor.

| Columna | Tipo | Que hacer |
|---|---|---|
| `CalzadaID` | `Text` | **CLAVE** |
| `Nombre` | `Text` |  |
| `Activo` | `Yes/No` | `Initial value` = `TRUE` |

## `CHD_ChecklistDetalle`

Respuesta a cada pregunta. Referencia la pregunta por su clave, no por su texto: sin eso no hay comparacion historica posible.

| Columna | Tipo | Que hacer |
|---|---|---|
| `DetalleID` | `Text` | **CLAVE** |
| `ChecklistID` | `Ref` | `Ref` -> `CHK_Checklists` · **IsPartOf** |
| `PreguntaID` | `Ref` | `Ref` -> `FRM_Preguntas` · IsPartOf desmarcado |
| `RespuestaTexto` | `LongText` |  |
| `RespuestaNumero` | `Decimal` |  |
| `RespuestaBoolean` | `Yes/No` |  |
| `RespuestaLista` | `Enum` | **Valores sin declarar en el modelo.** No los invente: pregunte antes de crear la columna |
| `Contestada` | `Yes/No` | `Initial value` = `FALSE` |
| `Observacion` | `LongText` |  |

**Y estas, que estan en la hoja y NO se usan:**

| Columna | Que hacer | Por que |
|---|---|---|
| `Activo` | **OCULTAR** | El detalle es parte de su checklist: no se desactiva por separado. |
| `EstadoPregunta` | **OCULTAR** | Redundante con Contestada. |
| `FechaRespuesta` | **OCULTAR** | Se deriva del ChangeTimestamp del mantenimiento. |
| `Orden` | **OCULTAR** | Se alcanza por [PreguntaID].[Orden]. |
| `PreguntaActual` | **OCULTAR** | Estado de la interfaz, no dato. |
| `RespuestaFecha` | **OCULTAR** | Fuera de alcance: ninguna pregunta usa tipo fecha. |
| `RespuestaFirma` | **OCULTAR** | Sustituido por FIR_Firmas. |
| `RespuestaFoto` | **OCULTAR** | Sustituido por FOT_Fotografias. |
| `RespuestaGPS` | **OCULTAR** | La coordenada es del mantenimiento y de cada fotografia. |
| `RespuestaHora` | **OCULTAR** | Fuera de alcance: ninguna pregunta usa tipo hora. |
| `TipoRespuestaID` | **OCULTAR** · **TRAMPA: AppSheet la pone `Ref` sola hacia `TPR_TiposRespuesta`** | Se alcanza por [PreguntaID].[TipoRespuestaID]. |
| `TotalPreguntas` | **OCULTAR** | No es del detalle sino del encabezado, y ademas se cuenta. |

## `CHK_Checklists`

Encabezado de la inspeccion. Cuelga del mantenimiento, no de la orden: la inspeccion es parte de la ejecucion.

| Columna | Tipo | Que hacer |
|---|---|---|
| `ChecklistID` | `Text` | **CLAVE** |
| `MantenimientoID` | `Ref` | `Ref` -> `MAN_Mantenimientos` · **IsPartOf** |
| `FormularioID` | `Ref` | `Ref` -> `FRM_Formularios` · IsPartOf desmarcado |
| `VersionFormulario` | `Number` |  |
| `FechaInicio` | `DateTime` | `Initial value` = `NOW()` |
| `FechaFin` | `DateTime` |  |
| `Finalizado` | `Yes/No` | `Initial value` = `FALSE` |

**Y estas, que estan en la hoja y NO se usan:**

| Columna | Que hacer | Por que |
|---|---|---|
| `Activo` | **OCULTAR** | El checklist es parte de su mantenimiento: no se desactiva por separado. |
| `ActivoID` | **OCULTAR** · **TRAMPA: AppSheet la pone `Ref` sola hacia `ACT_Activos`** | Se alcanza por [MantenimientoID].[OTID].[ActivoID]. |
| `Estado` | **OCULTAR** | Sustituido por Finalizado, que produccion ya tiene. |
| `FechaCreacion` | **OCULTAR** | Redundante con FechaInicio. |
| `FechaEnvioCorreo` | **OCULTAR** | Es traza del bot, no del checklist. |
| `FirmaSupervisor` | **OCULTAR** | El supervisor aprueba en el portal, no firma. Supuesto D-10. |
| `FirmaTecnico` | **OCULTAR** | Sustituido por FIR_Firmas. |
| `GPSFin` | **OCULTAR** | Idem. |
| `GPSInicio` | **OCULTAR** | La coordenada es del mantenimiento y de cada fotografia, no del checklist. |
| `Observaciones` | **OCULTAR** | La observacion es de la ejecucion o de la respuesta, no del encabezado. |
| `PDF` | **OCULTAR** | El informe se genera al enviarlo, no se almacena en la fila. |
| `Porcentaje` | **OCULTAR** | Se calcula. Guardarlo permite que contradiga al detalle. |
| `PreguntaActual` | **OCULTAR** | Estado de la interfaz, no dato. Se deriva de las respuestas. |
| `TecnicoID` | **OCULTAR** | Se alcanza por [MantenimientoID].[TecnicoID]. Es el campo donde el dato de prueba dejo 'Santiago Moreno' en lugar de un identificador. |
| `TotalPreguntas` | **OCULTAR** | Se cuenta de FRM_Preguntas. |

## `EOT_EstadosOrden`

Ciclo de vida de la orden segun el supuesto D-06. Declararlo como catalogo, y no como texto libre, es lo que permite medir cumplimiento.

| Columna | Tipo | Que hacer |
|---|---|---|
| `EstadoOrdenID` | `Text` | **CLAVE** |
| `Nombre` | `Text` |  |
| `Orden` | `Number` |  |
| `QuienCambia` | `Enum` | Valores: `Sistema` · `Tecnico` · `Supervisor` |
| `EsFinal` | `Yes/No` | `Initial value` = `FALSE` |
| `Activo` | `Yes/No` | `Initial value` = `TRUE` |

## `EST_Activo`

Estados del activo: Operativo, En mantenimiento, Fuera de servicio, Retirado.

| Columna | Tipo | Que hacer |
|---|---|---|
| `EstadoActivoID` | `Text` | **CLAVE** |
| `Nombre` | `Text` |  |
| `GeneraAlerta` | `Yes/No` | `Initial value` = `FALSE` |
| `Activo` | `Yes/No` | `Initial value` = `TRUE` |

## `FAL_ModosFalla`

Taxonomia de fallas por tipo de activo. Sin clasificar la falla no hay ingenieria de mantenimiento posible: no se puede calcular tiempo medio entre fallas, ni saber que componente falla mas, ni pasar de correctivo a predictivo.

| Columna | Tipo | Que hacer |
|---|---|---|
| `ModoFallaID` | `Text` | **CLAVE** |
| `TipoActivoID` | `Ref` | `Ref` -> `TIP_TiposActivo` · IsPartOf desmarcado |
| `Nombre` | `Text` |  |
| `Componente` | `Text` |  |
| `Criticidad` | `Enum` | Valores: `Alta` · `Media` · `Baja` |
| `Activo` | `Yes/No` | `Initial value` = `TRUE` |

## `FIR_Firmas`

Firma manuscrita. Supuesto D-10: firma el tecnico en campo; el supervisor valida aprobando en el portal, no firmando.

| Columna | Tipo | Que hacer |
|---|---|---|
| `FirmaID` | `Text` | **CLAVE** |
| `MantenimientoID` | `Ref` | `Ref` -> `MAN_Mantenimientos` · **IsPartOf** |
| `TipoFirma` | `Enum` | Valores: `Tecnico` |
| `Imagen` | `Signature` |  |
| `FechaHora` | `ChangeTimestamp` |  |

## `FOT_Fotografias`

Fotografias del mantenimiento. Supuesto D-10: minimo 3, maximo 6, tipificadas. Se elige tabla hija y se retiran los campos de imagen embebidos en MAN.

| Columna | Tipo | Que hacer |
|---|---|---|
| `FotoID` | `Text` | **CLAVE** |
| `MantenimientoID` | `Ref` | `Ref` -> `MAN_Mantenimientos` · **IsPartOf** |
| `Tipo` | `Enum` | Valores: `Antes` · `Despues` · `Novedad` |
| `Archivo` | `Image` |  |
| `Ubicacion_LatLong` | `LatLong` | `Initial value` = `HERE()` |
| `FechaHora` | `ChangeTimestamp` |  |
| `Usuario` | `Text` | `Initial value` = `USEREMAIL()` |

**Y estas, que estan en la hoja y NO se usan:**

| Columna | Que hacer | Por que |
|---|---|---|
| `Fecha` | **OCULTAR** | Duplicaba a FechaHora, que es la que vale como evidencia porque la escribe el servidor. Dos fechas para el mismo hecho invitan a discutir cual manda justo cuando hay que probar algo. Retirada el 2026-08-10. |
| `PrecisionGPS` | **OCULTAR** | USERLOCATIONACCURACY() no existe en AppSheet (ESPEC-004 2.1, mismo hallazgo que Precision_GPS de MAN_Mantenimientos). Ninguna regla la leia (ESPEC-007 2.2): a diferencia de MAN, no habia cadena que romper. Retirada por ESPEC-007. Si FOT_Fotografias ya tenia esta columna con Initial value puesto en el editor, hace falta Delete and re-add de la tabla completa (mismo procedimiento de ESPEC-004 2.10); si quedo huerfana sin usar, no hace falta nada (ESPEC-007 2.7, sin confirmar cual rama aplica). |

## `FRE_Frecuencias`

Periodicidad del mantenimiento preventivo.

| Columna | Tipo | Que hacer |
|---|---|---|
| `FrecuenciaID` | `Text` | **CLAVE** |
| `Nombre` | `Text` |  |
| `Dias` | `Number` |  |
| `Activo` | `Yes/No` | `Initial value` = `TRUE` |

## `FRM_Formularios`

Registro maestro de los checklists, uno por tipo de activo: 27 en BD/Modelo_Datos_PLANTILLA.xlsx, 18 en la hoja de produccion.

| Columna | Tipo | Que hacer |
|---|---|---|
| `FormularioID` | `Text` | **CLAVE** |
| `Nombre` | `Text` |  |
| `Descripcion` | `Text` |  |
| `Version` | `Number` | `Initial value` = `1` |
| `Activo` | `Yes/No` | `Initial value` = `TRUE` |

**Y estas, que estan en la hoja y NO se usan:**

| Columna | Que hacer | Por que |
|---|---|---|
| `Orden` | **OCULTAR** | Ordenaria los formularios en una lista y ninguna vista los ordena. Estaba vacia. Si algun dia se ordenan, se declara entonces con su proposito escrito. Retirada el 2026-08-10. |

## `FRM_Preguntas`

Banco unico de preguntas. Es el motor: se retiran las hojas planas FRM_SOS, FRM_CCTV y FRM_PMVF, que eran una arquitectura paralela con otro esquema.

| Columna | Tipo | Que hacer |
|---|---|---|
| `PreguntaID` | `Text` | **CLAVE** |
| `FormularioID` | `Ref` | `Ref` -> `FRM_Formularios` · IsPartOf desmarcado |
| `SeccionID` | `Ref` | `Ref` -> `FRM_Secciones` · IsPartOf desmarcado |
| `Orden` | `Number` |  |
| `Pregunta` | `Text` |  |
| `TipoRespuestaID` | `Ref` | `Ref` -> `TPR_TiposRespuesta` · IsPartOf desmarcado |
| `Obligatoria` | `Yes/No` | `Initial value` = `TRUE` |
| `ValorMinimo` | `Decimal` |  |
| `ValorMaximo` | `Decimal` |  |
| `Unidad` | `Text` |  |
| `Ayuda` | `Text` |  |
| `VisibleSi` | `Text` |  |
| `RequiereFoto` | `Yes/No` | `Initial value` = `FALSE` |
| `Version` | `Number` | `Initial value` = `1` |
| `RequiereGPS` | `Yes/No` | `Initial value` = `FALSE` |
| `RequiereFirma` | `Yes/No` | `Initial value` = `FALSE` |
| `Activo` | `Yes/No` | `Initial value` = `TRUE` |

**Y estas, que estan en la hoja y NO se usan:**

| Columna | Que hacer | Por que |
|---|---|---|
| `ValorDefecto` | **OCULTAR** | Precargaria la respuesta antes de que el tecnico conteste. En una evidencia eso es peligroso: una respuesta por defecto que nadie toca parece contestada. Retirada el 2026-08-10. |

## `FRM_Secciones`

Agrupacion de preguntas dentro del formulario.

| Columna | Tipo | Que hacer |
|---|---|---|
| `SeccionID` | `Text` | **CLAVE** |
| `Nombre` | `Text` |  |
| `Orden` | `Number` |  |
| `Activo` | `Yes/No` | `Initial value` = `TRUE` |

## `LST_ValoresLista`

Opciones de las preguntas de tipo lista.

| Columna | Tipo | Que hacer |
|---|---|---|
| `ValorListaID` | `Text` | **CLAVE** |
| `PreguntaID` | `Ref` | `Ref` -> `FRM_Preguntas` · IsPartOf desmarcado |
| `Valor` | `Text` |  |
| `Orden` | `Number` |  |
| `Activo` | `Yes/No` | `Initial value` = `TRUE` |

## `MAN_Mantenimientos`

Ejecucion real en campo. Cuelga de la orden y es padre de la evidencia.

| Columna | Tipo | Que hacer |
|---|---|---|
| `MantenimientoID` | `Text` | **CLAVE** |
| `OTID` | `Ref` | `Ref` -> `OT_OrdenesTrabajo` · IsPartOf desmarcado |
| `TecnicoID` | `Ref` | `Ref` -> `USR_Usuarios` · IsPartOf desmarcado · `Initial value` = `LOOKUP(USEREMAIL(), "USR_Usuarios", "Correo", "UsuarioID")` |
| `FechaHoraInicio` | `DateTime` | `Initial value` = `NOW()` |
| `FechaHoraFin` | `DateTime` |  |
| `OrigenApertura` | `Enum` | Valores: `QR` · `Lista` · `Initial value` = `Lista` |
| `UbicacionEscaneo_LatLong` | `LatLong` |  |
| `FechaHoraEscaneo` | `DateTime` |  |
| `EstadoActivoID` | `Ref` | `Ref` -> `EST_Activo` · IsPartOf desmarcado |
| `Coordenadas_Cierre_LatLong` | `LatLong` | `Initial value` = `HERE()` |
| `CierreConExcepcion` | `Yes/No` |  |
| `MotivoExcepcion` | `LongText` |  |
| `RequiereSegundaVisita` | `Yes/No` | `Initial value` = `FALSE` |
| `MotivoPendienteID` | `Ref` | `Ref` -> `MOT_MotivosPendiente` · IsPartOf desmarcado |
| `ModoFallaID` | `Ref` | `Ref` -> `FAL_ModosFalla` · IsPartOf desmarcado |
| `Observaciones` | `LongText` |  |
| `AprobadoSupervisor` | `Yes/No` | `Initial value` = `FALSE` |
| `FechaAprobacion` | `DateTime` |  |
| `ObservacionRechazo` | `LongText` |  |
| `UsuarioRegistro` | `Text` | `Initial value` = `USEREMAIL()` |
| `FechaHoraRegistro` | `ChangeTimestamp` |  |
| `Activo` | `Yes/No` | `Initial value` = `TRUE` |

**Y estas, que estan en la hoja y NO se usan:**

| Columna | Que hacer | Por que |
|---|---|---|
| `Diagnostico` | **OCULTAR** | Se responde en el checklist, no en campo libre. |
| `Duracion_Minutos` | **OCULTAR** | Se calcula de FechaHoraInicio y FechaHoraFin. |
| `Estado_Intervencion` | **OCULTAR** | Redundante con el estado de la orden. |
| `Fecha` | **OCULTAR** | Redundante con FechaHoraInicio. |
| `Firma_Supervisor` | **OCULTAR** | El supervisor aprueba en el portal, no firma. Supuesto D-10. |
| `Firma_Tecnico` | **OCULTAR** | Sustituido por FIR_Firmas. |
| `Imagen_Final` | **OCULTAR** | Sustituido por FOT_Fotografias con Tipo=Despues. |
| `Imagen_Inicio` | **OCULTAR** | Sustituido por FOT_Fotografias con Tipo=Antes. |
| `Localizacion` | **OCULTAR** | Ambiguo y redundante con Coordenadas_Cierre. |
| `Precision_GPS` | **OCULTAR** | USERLOCATIONACCURACY() no existe en AppSheet (ESPEC-004 2.1): la columna nunca se poblaba, RG-19 comparaba siempre numero > blanco y RG-03 no pedia MotivoExcepcion nunca. Retirada por ESPEC-004/ORDEN-004. Si MAN_Mantenimientos ya estaba dada de alta en el editor con esta columna sin usar (Rama A, ESPEC-004 2.10), retirarla del modelo no la borra de la hoja: queda huerfana, sin Initial value y sin uso, y eso no es un fallo (ACTA-004; PRUEBA-004 P-45). Si ya estaba cableada con Initial value puesto (Rama B), hace falta Delete and re-add de la tabla completa (ESPEC-004 2.10). |
| `Repuestos_Utilizados` | **OCULTAR** | Gestion de repuestos esta fuera de alcance. |
| `Requiere_Repuesto` | **OCULTAR** | Se cubre con MotivoPendienteID = Falta de repuesto. |
| `Tipo` | **OCULTAR** | El tipo es de la orden, no de la ejecucion. |
| `Trabajo_Realizado` | **OCULTAR** | Se responde en el checklist. |

## `MOT_MotivosPendiente`

Motivos tipificados de trabajo incompleto, supuesto D-07. Si el tecnico no tiene donde declarar por que no pudo terminar, fuerza un cierre falso.

| Columna | Tipo | Que hacer |
|---|---|---|
| `MotivoPendienteID` | `Text` | **CLAVE** |
| `Nombre` | `Text` |  |
| `GeneraSeguimiento` | `Yes/No` | `Initial value` = `TRUE` |
| `Activo` | `Yes/No` | `Initial value` = `TRUE` |

## `NOV_Novedades`

Hallazgos del tecnico en ruta: activos no inventariados o fallas fuera de programacion. Supuesto D-08. Sin esta via los hallazgos se pierden o acaban en WhatsApp, que es lo que el sistema viene a reemplazar.

| Columna | Tipo | Que hacer |
|---|---|---|
| `NovedadID` | `Text` | **CLAVE** |
| `UsuarioID` | `Ref` | `Ref` -> `USR_Usuarios` · IsPartOf desmarcado · `Initial value` = `LOOKUP(USEREMAIL(), "USR_Usuarios", "Correo", "UsuarioID")` |
| `Tipo` | `Enum` | Valores: `Activo no inventariado` · `Falla detectada` |
| `Descripcion` | `LongText` |  |
| `Ubicacion_LatLong` | `LatLong` | `Initial value` = `HERE()` |
| `Fotografia` | `Image` |  |
| `ActivoID` | `Ref` | `Ref` -> `ACT_Activos` · IsPartOf desmarcado |
| `Estado` | `Enum` | Valores: `Reportada` · `Aceptada` · `Descartada` · `Initial value` = `Reportada` |
| `FechaHora` | `ChangeTimestamp` |  |

## `OT_OrdenesTrabajo`

Trabajo programado o levantado sobre un activo.

| Columna | Tipo | Que hacer |
|---|---|---|
| `OTID` | `Text` | **CLAVE** |
| `ActivoID` | `Ref` | `Ref` -> `ACT_Activos` · IsPartOf desmarcado |
| `TecnicoID` | `Ref` | `Ref` -> `USR_Usuarios` · IsPartOf desmarcado |
| `SupervisorID` | `Ref` | `Ref` -> `USR_Usuarios` · IsPartOf desmarcado |
| `Tipo` | `Enum` | Valores: `Preventivo` · `Correctivo` |
| `FechaProgramada` | `DateTime` |  |
| `EstadoOrdenID` | `Ref` | `Ref` -> `EOT_EstadosOrden` · IsPartOf desmarcado |
| `OTOrigenID` | `Ref` | `Ref` -> `OT_OrdenesTrabajo` · IsPartOf desmarcado |
| `Observaciones` | `LongText` |  |
| `FechaCierre` | `DateTime` |  |
| `CerradaPor` | `Ref` | `Ref` -> `USR_Usuarios` · IsPartOf desmarcado |
| `Activo` | `Yes/No` | `Initial value` = `TRUE` |

**Y estas, que estan en la hoja y NO se usan:**

| Columna | Que hacer | Por que |
|---|---|---|
| `FormularioID` | **OCULTAR** · **TRAMPA: AppSheet la pone `Ref` sola hacia `FRM_Formularios`** | El formulario lo determina el tipo del activo, no la orden. |
| `Informe_Final` | **OCULTAR** | Se genera del mantenimiento y su checklist, no se transcribe. |
| `Motivo_Cierre` | **OCULTAR** | Se tipifica en MOT_MotivosPendiente desde la ejecucion. |

## `PAR_Parametros`

Umbrales que el administrador ajusta con las pruebas de campo, sin tocar la configuracion de la aplicacion. Existe porque un numero magico escondido en una expresion no se puede calibrar: hay que abrir el editor, encontrarlo y arriesgarse a romper la regla. Aqui es una celda.

| Columna | Tipo | Que hacer |
|---|---|---|
| `ParametroID` | `Text` | **CLAVE** |
| `Nombre` | `Text` |  |
| `Valor` | `Decimal` |  |
| `Unidad` | `Text` |  |
| `Descripcion` | `LongText` |  |
| `Activo` | `Yes/No` | `Initial value` = `TRUE` |

## `PLA_PlanMantenimiento`

Que tarea preventiva toca a cada activo y cada cuanto. Es lo que convierte al sistema en gestion de mantenimiento y no en un registro de formularios: de aqui salen las ordenes, en lugar de crearlas a mano una por una.

| Columna | Tipo | Que hacer |
|---|---|---|
| `PlanID` | `Text` | **CLAVE** |
| `ActivoID` | `Ref` | `Ref` -> `ACT_Activos` · IsPartOf desmarcado |
| `FrecuenciaID` | `Ref` | `Ref` -> `FRE_Frecuencias` · IsPartOf desmarcado |
| `UltimaEjecucion` | `Date` |  |
| `ProximaFecha` | `Date` |  |
| `ResponsableID` | `Ref` | `Ref` -> `USR_Usuarios` · IsPartOf desmarcado |
| `Activo` | `Yes/No` | `Initial value` = `TRUE` |

## `ROL_Roles`

Perfiles de acceso: Administrador, Supervisor, Tecnico y Consulta.

| Columna | Tipo | Que hacer |
|---|---|---|
| `RolID` | `Text` | **CLAVE** |
| `Nombre` | `Text` |  |
| `Descripcion` | `Text` |  |
| `Activo` | `Yes/No` | `Initial value` = `TRUE` |

## `SED_Sedes`

Edificaciones del corredor: CCO, peajes y basculas. Cada una esta al lado de la via, en un PR concreto, y por tanto dentro de una unidad funcional. Es el PADRE DE UBICACION del equipo bajo techo: un servidor, un NAS o una impresora no estan en un punto de la via, estan DENTRO de un edificio, y de el heredan donde estan.

| Columna | Tipo | Que hacer |
|---|---|---|
| `SedeID` | `Text` | **CLAVE** |
| `Nombre` | `Text` |  |
| `Ciudad` | `Text` |  |
| `UnidadFuncionalID` | `Ref` | `Ref` -> `UNF_UnidadesFuncionales` · IsPartOf desmarcado |
| `PR` | `Text` |  |
| `TramoINVIAS` | `Text` |  |
| `PK` | `Text` |  |
| `Ubicacion_LatLong` | `LatLong` |  |
| `Activo` | `Yes/No` | `Initial value` = `TRUE` |

## `SEN_Sentidos`

Sentidos de circulacion.

| Columna | Tipo | Que hacer |
|---|---|---|
| `SentidoID` | `Text` | **CLAVE** |
| `Nombre` | `Text` |  |
| `Activo` | `Yes/No` | `Initial value` = `TRUE` |

## `TIP_TiposActivo`

Taxonomia de activos. Determina que checklist abre la aplicacion.

| Columna | Tipo | Que hacer |
|---|---|---|
| `TipoActivoID` | `Text` | **CLAVE** |
| `Nombre` | `Text` |  |
| `Categoria` | `Enum` | Valores: `ITS` · `Electrico` · `Comunicaciones` · `TI` |
| `FormularioID` | `Ref` | `Ref` -> `FRM_Formularios` · IsPartOf desmarcado |
| `TieneQR` | `Yes/No` | `Initial value` = `TRUE` |
| `RequiereGPS` | `Yes/No` | `Initial value` = `TRUE` |
| `RadioGeofencingKm` | `Decimal` | `Initial value` = `0.2` |
| `Activo` | `Yes/No` | `Initial value` = `TRUE` |

## `TPR_TiposRespuesta`

Tipo de dato esperado en cada respuesta.

| Columna | Tipo | Que hacer |
|---|---|---|
| `TipoRespuestaID` | `Text` | **CLAVE** |
| `Nombre` | `Text` |  |
| `Activo` | `Yes/No` | `Initial value` = `TRUE` |

## `UNF_UnidadesFuncionales`

Tramos del corredor donde estan los activos. Se separa de SED_Sedes porque son dos conceptos distintos que el modelo anterior mezclaba en una sola columna, dejando usuarios y activos en conjuntos disjuntos.

| Columna | Tipo | Que hacer |
|---|---|---|
| `UnidadFuncionalID` | `Text` | **CLAVE** |
| `Nombre` | `Text` |  |
| `PKInicial` | `Text` |  |
| `PKFinal` | `Text` |  |
| `PRInicial` | `Text` |  |
| `PRFinal` | `Text` |  |
| `Activo` | `Yes/No` | `Initial value` = `TRUE` |

## `USR_Usuarios`

Personas del sistema. El correo resuelve la sesion contra USEREMAIL().

| Columna | Tipo | Que hacer |
|---|---|---|
| `UsuarioID` | `Text` | **CLAVE** |
| `Nombres` | `Text` |  |
| `Correo` | `Email` |  |
| `Cargo` | `Text` |  |
| `Iniciales` | `Text` |  |
| `RolID` | `Ref` | `Ref` -> `ROL_Roles` · IsPartOf desmarcado |
| `Telefono` | `Phone` |  |
| `FechaIngreso` | `Date` |  |
| `Activo` | `Yes/No` | `Initial value` = `TRUE` |

**Y estas, que estan en la hoja y NO se usan:**

| Columna | Que hacer | Por que |
|---|---|---|
| `SedeID` | **OCULTAR** · **TRAMPA: AppSheet la pone `Ref` sola hacia `SED_Sedes`** | Retirada el 2026-08-10 para que el modelo diga lo que dice la especificacion. FUNCIONAL_SGMC 6.3 la declara descartada frente a ASG_AsignacionZona: la sede es un edificio y la asignacion es un tramo, y un tecnico puede atender varias unidades funcionales, asi que la relacion es de muchos a muchos y no cabe como columna. RG-04, el filtro de seguridad que decide que activos ve cada tecnico, lee la asignacion y no menciona la sede. El modelo la declaraba Ref obligatoria mientras la spec la daba por descartada: se contradecian, y cablearla habria dejado dos formas de decir donde trabaja alguien. |
| `UltimaSincronizacion` | **OCULTAR** | Venia de una version anterior y el modelo nunca la uso. La regeneracion del 2026-08-10 la dejo fuera y no se echo en falta. Retirada el 2026-08-10. |

