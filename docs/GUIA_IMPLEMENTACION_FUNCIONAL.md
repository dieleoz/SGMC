# Guia de implementacion — el Funcional, paso a paso

**Como se procede en cada etapa y como se comprueba antes de pasar a la siguiente.**

> **Escrita por rol.** El **Funcional** es quien configura AppSheet sin programar. Esta guia se
> replica en otro contrato cambiando solo los nombres de tablas.

| | |
|---|---|
| Que dice esta guia | **Como** se hace cada etapa y **como se verifica** |
| Que dice `MANUAL_DESPLIEGUE.md` | **Que** hay que poner: la ficha de las 28 tablas, columna por columna |
| Fuente | `scripts/modelo_objetivo.py`. Esta guia se genera de ahi |

## Como usar esta guia

**Cada etapa termina con una comprobacion.** Si no pasa, no siga: el error se multiplica en la
siguiente y despues cuesta el triple encontrarlo.

**Anote lo que va comprobando.** Al final hay un acta que rellenar. Este proyecto tiene tres
cierres reportados que no resistieron la comprobacion contra el archivo, y las tres veces lo paro
un script, no una persona.

**Si algo no sale como dice esta guia, pare y reportelo.** Eso es informacion, no un fallo suyo:
cada cosa rara que ha aparecido en este proyecto acabo siendo un comportamiento de AppSheet que
nadie habia documentado.

---

# Etapa 0 — Antes de abrir AppSheet

**Duracion:** 15 minutos. **Sin esto, todo lo demas hereda el error.**

### 0.1 Copia de seguridad de la hoja

En Google Sheets: *Archivo -> Hacer una copia*. Nombrela con la fecha.

**Es lo unico que no se recupera.** Todo lo demas vive en el repositorio y se regenera.

### 0.2 Comprobar que ninguna pestana este oculta

En Google Sheets, abajo a la izquierda: el icono de las cuatro lineas, *Todas las hojas*. Las
ocultas salen en gris.

**AppSheet ignora las pestanas ocultas y no avisa.** Ocho catalogos estaban ocultos y la
aplicacion cargaba 24 tablas de 32 sin un solo mensaje. Se perdieron dos dias en eso.

### 0.3 Verificar el archivo

Descargue el libro —*Archivo -> Descargar -> Microsoft Excel*—, guardelo en `BD/` y ejecute:

```bash
python scripts/verificar_faseA.py "BD/<su archivo>.xlsx"
```

### COMPROBACION de la etapa 0

| Que | Como se ve que esta bien |
|---|---|
| Copia hecha | Existe en el Drive, con la fecha en el nombre |
| Pestanas visibles | El menu *Todas las hojas* no muestra ninguna en gris |
| Archivo verificado | El script imprime **`FASE A CERRADA`** |

> **Si dice `FASE A INCOMPLETA`, pare.** El mensaje dice exactamente que falta. `F-18` avisa de
> pestanas ocultas y `F-19` de columnas declaradas que ya no existen.

# Etapa 1 — Crear la aplicacion

**Duracion:** 5 minutos.

### 1.1

En AppSheet: **Create -> App -> Start with existing data**. Elija el documento de **Google
Sheets**.

> **No suba un `.xlsx`.** Si la aplicacion lee un archivo subido, queda mirando una foto fija y
> nada se sincroniza. Tiene que apuntar al documento vivo.

### 1.2 Quien la crea, la posee

**Un coautor no puede dar de alta tablas**, y toda esta guia consiste en eso. Cree la aplicacion
con la cuenta que va a operarla.

### COMPROBACION de la etapa 1

| Que | Como se ve |
|---|---|
| La fuente es el Sheets vivo | *Data -> [tabla] -> Source Type* dice `Sheets` |
| Usted es propietario | *Data -> `+` -> Add data* **no** dice «As a co-author...» |

# Etapa 2 — Dar de alta las 28 tablas

**Duracion:** 45 minutos. Es lo mas repetitivo de todo.

### 2.1 Una por una, y en orden

*Data -> `+` -> Add data -> el Sheets -> la pestana*.

**El orden importa y no es alfabetico.** Determina que referencias infiere AppSheet solo al dar
de alta cada tabla. La lista esta en `MANUAL_DESPLIEGUE.md` paso 2.

### 2.2 Las 5 que el modelo retira

```
`FRM_CCTV` · `FRM_PMVF` · `FRM_SOS` · `GPS` · `SEC_Secciones`
```

**Sobre la hoja vigente ya no existen**, porque la hoja se genera del modelo: no van a aparecer en
el desplegable. La lista sirve para reconocerlas si algun dia trabaja sobre una copia antigua del
libro. **No lo de por hecho, compruebelo:**

```bash
python -c "import openpyxl;n=openpyxl.load_workbook('BD/Modelo_Datos_PLANTILLA.xlsx',read_only=True).sheetnames;print([t for t in ['FRM_CCTV', 'FRM_PMVF', 'FRM_SOS', 'GPS', 'SEC_Secciones'] if t in n])"
```

Tiene que devolver `[]`. Y los bancos de preguntas que tres de ellas guardaban **ya estan dentro
de `FRM_Preguntas`**, que es el motor unico.

### COMPROBACION de la etapa 2

| Que | Como se ve |
|---|---|
| Son exactamente 28 | Cuentelas en *Data -> Tables* |
| Ninguna duplicada | Ningun nombre acaba en `_1`, `(2)` ni empieza por `Copy of` |
| Cada una a su pestana | Abra la ficha de cada una y lea el *Qualifier* |
| Las 5 retiradas no estan | `FRM_CCTV`, `FRM_PMVF`, `FRM_SOS`, `GPS`, `SEC_Secciones` no aparecen |

> **La duplicada es el fallo tipico de esta etapa.** Si el borrado no se confirma y el alta si,
> AppSheet crea una segunda tabla sobre la misma pestana. **Las referencias se reparten entre las
> dos y la mitad de las filas parece desaparecer, sin error.**

# Etapa 3 — Las claves

**Duracion:** 30 minutos. **Es lo unico que no se recupera despues.**

### 3.1 Por que importa tanto

Al dar de alta una tabla, AppSheet elige clave por su cuenta: examina las columnas de izquierda a
derecha buscando valores unicos y, **si ninguna le sirve, combina dos en una clave compuesta**.

**Contra una clave compuesta no resuelve ninguna referencia.** Y el sintoma no es un mensaje: es
que la etapa 5 entera falla sin decir por que.

### 3.2 Que hacer en cada tabla

*Data -> Columns*. Una sola casilla `KEY` marcada, sobre la columna correcta, **tipo `Text`**.

La lista de las 28 claves esta en `MANUAL_DESPLIEGUE.md` paso 3.

### 3.3 Por que todas `Text` y no `Number`

`USR_Usuarios.UsuarioID` tiene un valor alfanumerico entre otros numericos. **Si AppSheet infiere
`Number`, esa fila se queda sin clave valida y ese usuario deja de existir para el sistema.**

### 3.4 Clave automatica para filas nuevas

Estas 8 tablas crean filas desde la aplicacion. Sin `Initial value = UNIQUEID()` no sabe que
identificador poner:

```
CHD_ChecklistDetalle     DetalleID
CHK_Checklists           ChecklistID
FIR_Firmas               FirmaID
FOT_Fotografias          FotoID
MAN_Mantenimientos       MantenimientoID
NOV_Novedades            NovedadID
OT_OrdenesTrabajo        OTID
PLA_PlanMantenimiento    PlanID
```

### COMPROBACION de la etapa 3

| Que | Como se ve |
|---|---|
| Una sola `KEY` por tabla | Recorra las 28. Si hay dos marcadas, quite la sobrante |
| Ninguna compuesta | Si el editor muestra la clave como combinacion de columnas, corrijala |
| Todas `Text` | Ninguna en `Number` |
| Las 8 con `UNIQUEID()` | Compruebe el `Initial value` de cada una |

# Etapa 4 — Los tipos que AppSheet no adivina

**Duracion:** 20 minutos.

Todo llega de una hoja de calculo, asi que entra como texto o numero. La lista completa esta en
`MANUAL_DESPLIEGUE.md` paso 4.

### La que no se puede fallar

```
MAN_Mantenimientos.Coordenadas_Cierre_LatLong  ->  LatLong
```

**Sobre ella se monta el geofencing, y `DISTANCE()` no funciona sobre texto.** Si esta columna
queda como `Text`, la regla de la etapa 7 no se puede ni escribir.

### Las cuatro marcas de tiempo

```
MAN_Mantenimientos.FechaHoraRegistro   ->  ChangeTimestamp
FOT_Fotografias.FechaHora              ->  ChangeTimestamp
FIR_Firmas.FechaHora                   ->  ChangeTimestamp
NOV_Novedades.FechaHora                ->  ChangeTimestamp
```

**`ChangeTimestamp` la pone el servidor.** Un `Initial value = NOW()` lo pone el telefono, y el
usuario puede cambiar la hora del telefono. **Sin esto, la hora de cada fotografia y de cada firma
no prueba nada** — que es justo lo que el sistema existe para sostener.

### COMPROBACION de la etapa 4

| Que | Como se ve |
|---|---|
| `Coordenadas_Cierre_LatLong` | Tipo `LatLong` |
| Las cuatro marcas | Tipo `ChangeTimestamp` |
| Las imagenes y la firma | `Image` y `Signature`, no `Text` |
| Los `Enum` | Con sus valores declarados, no vacios |

# Etapa 5 — Las 39 referencias

**Duracion:** 1 hora. Es el corazon del sistema.

### 5.1 La regla de la que sale todo

> **Una referencia guarda el valor de la clave de la tabla destino.**

De ahi que el orden importe: **primero la clave del destino, despues quien la apunta**. La lista
en orden esta en `MANUAL_DESPLIEGUE.md` paso 5.

### 5.2 Cuidado con las listas de otros documentos

Circulo una lista de **15** referencias por convertir, y era correcta para lo que normaba: una
aplicacion existente donde otras 23 ya estaban puestas. Ese documento esta retirado.
**Construyendo desde cero son 39.** Si al terminar cuenta 15, siguio la lista equivocada.

### 5.3 `IsPartOf` va en 4, y en ninguna mas

```
FOT_Fotografias.MantenimientoID    -> MAN_Mantenimientos
FIR_Firmas.MantenimientoID         -> MAN_Mantenimientos
CHK_Checklists.MantenimientoID     -> MAN_Mantenimientos
CHD_ChecklistDetalle.ChecklistID   -> CHK_Checklists
```

**`MAN_Mantenimientos.OTID` va DESMARCADO, y es deliberado.** Con `IsPartOf`, borrar una orden
borraria su ejecucion, sus fotografias y su firma **en cascada**.

### 5.4 Despues de cada conversion, mire la tabla

**Convertir a `Ref` conserva solo las filas cuyo valor coincide con la clave del destino. Las
demas quedan huerfanas sin mensaje de error**: la celda se queda en blanco.

### COMPROBACION de la etapa 5

| Que | Como se ve |
|---|---|
| Son 39 | Cuente las columnas de tipo `Ref` en todas las tablas |
| Ninguna rota | El indicador `!` de referencia rota. **Hay que ir a mirarlo: no se anuncia** |
| Sin blancos nuevos | Ninguna celda vacia donde antes habia un valor |
| `IsPartOf` en 4 | Y desmarcado en `MAN_Mantenimientos.OTID` |

**Y la prueba de la cadena**, en el Asistente de Expresiones sobre `MAN_Mantenimientos`:

```
[OTID].[ActivoID].[Ubicacion_LatLong]
[OTID].[TecnicoID].[Correo]
```

Las dos en verde. **Se cierra sin dar a `Done`.**

> **Nunca pruebe una expresion escribiendola dentro de una columna.** Ya ocurrio: quedo una
> `App formula` escribiendo la coordenada del activo dentro de una columna retirada, y una
> `App formula` **escribe en la hoja** cada vez que se modifica la fila.

# Etapa 6 — RETIRADA. No la haga

**Duracion: 0.** Se conserva numerada para que quien tenga una copia antigua de esta guia sepa que
este trabajo salio del plan, y no crea que se le olvido.

Esta etapa mandaba ocultar, una por una, las 50 columnas que el modelo no declara, mas las tres que
AppSheet convertia en `Ref` sola por coincidencia de nombre. **Todas ellas venian de un libro
heredado. La hoja vigente se genera del modelo y no trae ninguna**, asi que no hay nada que
esconder ni ninguna referencia que deshacer.

**Compruebelo usted, no lo de por bueno:**

```bash
python scripts/verificar_faseA.py "BD/Modelo_Datos_PLANTILLA.xlsx"
```

Entre los conformes tiene que salir esta linea, que es la regla `F-19`:

```
ok Hoja limpia: ninguna de las 50 columnas retiradas existe ya. No hay nada que ocultar
```

> **Si no sale, no oculte nada todavia: pare y reportelo.** Significa que la hoja contra la que
> esta trabajando no es la que se genera del modelo, y entonces el problema no es esta etapa sino
> de que archivo salio la aplicacion.

# Etapa 7 — Las reglas

**Duracion:** 45 minutos. **Aqui esta el valor del sistema.**

Son 23. Las expresiones completas, sin truncar, en
`docs/sdd/RECONSTRUCCION_EXPRESIONES.md` §2.

### 7.1 El geofencing, y por que sin `Editable_If` no vale nada

En `MAN_Mantenimientos.Coordenadas_Cierre_LatLong`:

```
Initial value:  HERE()
Valid_If:       DISTANCE([Coordenadas_Cierre_LatLong], [OTID].[ActivoID].[Ubicacion_LatLong])
                  <= [OTID].[ActivoID].[TipoActivoID].[RadioGeofencingKm]
Invalid text:   Ubicacion fuera de rango: debe estar junto al activo para cerrar.
Editable_If:    FALSE
```

**El radio va por tipo, no como literal**, porque una subestacion y un poste SOS no admiten la
misma tolerancia. En la hoja vigente esa columna esta poblada en los 27 tipos; contra celdas en
blanco esta expresion **rechazaria tambien los cierres legitimos**, asi que compruebelo antes de
pegarla:

```bash
python -c "import openpyxl;s=openpyxl.load_workbook('BD/Modelo_Datos_PLANTILLA.xlsx',read_only=True,data_only=True)['TIP_TiposActivo'];h=[c.value for c in next(s.iter_rows(max_row=1))];i=h.index('RadioGeofencingKm');v=[r[i] for r in s.iter_rows(min_row=2,values_only=True)];print(len(v),'tipos,',sum(1 for x in v if x not in (None,'')),'con radio')"
```

**`PAR_Parametros.RADIO_GEOFENCING_KM` no lo lee esta regla.** Es un valor provisional historico
que sigue en la tabla; si alguien le dice que el radio se cambia ahi, esta describiendo el sistema
anterior.

**El `Editable_If = FALSE` no es un detalle.** Sin el, el tecnico arrastra el pin del mapa y
cierra desde su casa. La regla existiria, se veria, y no probaria nada.

Lo mismo en `UbicacionEscaneo_LatLong` y `FechaHoraEscaneo` (tres columnas, no cuatro: desde
ESPEC-004/ORDEN-004 `Precision_GPS` se retiro del modelo).

> **Y un supuesto que sigue sin verificar, el peor del sistema.** No hay pagina oficial que
> confirme si AppSheet evalua un `Valid_If` sobre una columna con `Editable_If = FALSE`. **Si no lo
> evalua, la regla parece funcionar por no ejercitarse nunca.** Se detecta en la etapa 9.

### 7.2 La excepcion por GPS deficiente, marcada por el tecnico

`RG-19` (el `App formula` que calculaba `CierreConExcepcion` con `Precision_GPS`) se retiro con
ESPEC-004/ORDEN-004: `USERLOCATIONACCURACY()` no existe en AppSheet, la columna nunca se
poblaba, y la comparacion daba siempre falso. Hoy `CierreConExcepcion` es una casilla `Yes/No`
**libre**, sin `App formula`, que marca el propio tecnico. Dos cosas a cablear en su lugar:

```
Type:          Yes/No (confirmar en Data > Columns; si sale Text, retipar antes de seguir -
               S-30, ESPEC-004 2.7)
Description:   "¿La app no alcanzó buena precisión al capturar la posición de cierre? Marque
               si es así." (no viaja por ningun generador, se escribe a mano - ESPEC-004 2.13)
```

`PAR_Parametros.UMBRAL_GPS` se conserva sin lector: es la cifra de referencia para el juicio
del tecnico, no una comparacion automatica.

### 7.3 Retirar el borrado

*Data -> Tables -> [tabla] -> Are updates allowed*:

```
OT_OrdenesTrabajo    Updates si · Adds si · Deletes NO
MAN_Mantenimientos   Updates si · Adds si · Deletes NO
```

**Es la otra mitad del `IsPartOf` de la etapa 5.** La cascada solo es segura porque el
mantenimiento no se puede borrar. Configurar una sin la otra deja la puerta abierta.

### 7.4 Los filtros de seguridad

*Data -> Tables -> [tabla] -> Security Filter*. Las dos expresiones estan en la lista de reglas.

**No son solo control de acceso: son rendimiento.** Sin ellos cada tecnico se descarga el
inventario entero al telefono.

### COMPROBACION de la etapa 7

| Que | Como se ve |
|---|---|
| Ninguna en rojo | El panel de errores del editor, vacio |
| `Deletes` quitado | En las dos tablas |
| Las no editables | `Editable_If = FALSE`. Hoy son 5, en 3 tablas: `FOT_Fotografias`, `MAN_Mantenimientos`, `NOV_Novedades` |
| El umbral con `ISBLANK` | Leala entera, no de por hecho que se pego bien |

# Etapa 8 — Las vistas

**Duracion:** 30 minutos.

**Esta guia no especifica las vistas, y conviene saberlo antes de abrir la etapa.** El modelo
declara datos, no interfaz: `VISTAS`, `ACCIONES` y `SLICES` **no existen** en
`scripts/modelo_objetivo.py` —comprobado al generar esta guia, no de memoria—. De las etapas
anteriores puede fiarse porque salen del modelo; de esta no, porque no hay de donde sacarla.

**Lo unico que AppSheet crea solo son las columnas virtuales `Related ...`**, que aparecen al poner
las referencias de la etapa 5 y traen con ellas la navegacion padre-hijo: al abrir un mantenimiento
se ven sus fotografias y su firma; al abrir un activo, sus ordenes. **Eso es todo lo que se
construye solo.** Las pantallas no.

**Y las pantallas no se configuran a ojo.** Las tres de abajo van con el tipo y la tabla que dice
la tabla; si algo no encaja, **no lo improvise: anotelo como pendiente y siga**. Una vista
inventada aqui es configuracion activa que nadie declaro, y quien reconstruya la aplicacion no
podra reproducirla.

### El caso que engana

**`USR_Usuarios` recibe tres referencias desde `OT_OrdenesTrabajo`** —tecnico, supervisor y quien
cerro— y AppSheet crea tres columnas virtuales con nombres casi iguales. Hay que abrirlas y leer el
segundo argumento del `REF_ROWS` para saber cual es cual.

**Si solo aparece una, faltan dos y el supervisor no vera sus ordenes.**

### Las tres pantallas principales

| Vista | Tipo | Sobre | Nota |
|---|---|---|---|
| Mapa de activos | `Map` | `ACT_Activos` | Columna de mapa: `Ubicacion` |
| Mis ordenes | `Deck` | `OT_OrdenesTrabajo` | Es la pantalla de trabajo del tecnico |
| Mantenimientos | `Table` | `MAN_Mantenimientos` | |

> **Esta etapa es la menos especificada de todas.** El modelo describe datos, no pantallas: no hay
> declaracion de vistas, acciones ni slices. Lo que haga aqui, **anotelo**, porque es la unica
> constancia que va a quedar.

# Etapa 9 — Probar

**Duracion:** 1 hora. **No se salte esta etapa: es la que dice si algo de lo anterior sirve.**

La tanda completa esta en `docs/sdd/PRUEBA-003-despliegue.md`. Aqui las cinco que no se negocian.

### 9.1 La cadena navega

En el Asistente, las dos expresiones de la etapa 5. **En verde las dos.**

### 9.2 El cierre legitimo se acepta, y el lejano se rechaza

Abra un mantenimiento cuyo cierre este junto a su activo: **debe guardar**. Abra otro que este
lejos: **debe rechazarlo** con el mensaje.

> **Si los dos salen aceptados, no celebre: sospeche.** La causa mas probable es que el `Valid_If`
> no se evalua sobre una columna con `Editable_If = FALSE`, y entonces el geofencing es decorativo.
> Reportelo antes de seguir.

> **Y con el inventario completo, el radio por tipo es lo que hace la prueba significativa.** Sobre
> los 334 activos repartidos por el corredor, un literal de 1 km mete **7,4 activos de media dentro
> de cada geofence** —la prueba pasaria estando frente al equipo equivocado—; con el radio por tipo
> de la etapa 7 baja a **1,2**. Por eso el literal no se usa.

### 9.3 El dato llega a la hoja

Cree un registro desde la aplicacion y **abra la hoja**. Si no esta ahi, no existe.

### 9.4 El historico no se puede borrar

Intente borrar un mantenimiento desde la aplicacion. **El boton no debe aparecer.**

### 9.5 El barrido de fallos silenciosos

En el Asistente, escriba esto:

```
REF_ROWS("OT_OrdenesTrabajo", "Activo")
```

`Activo` en esa tabla **ya no es la referencia al activo**: es la bandera Si/No. La expresion
apunta a la columna equivocada y devuelve lista vacia.

**Si el Asistente la ACEPTA, anotelo con su texto literal.** Es la prueba de que un despliegue
verde no distingue esa expresion de la correcta. **Sin verla aceptada, no sabemos si el resto paso
por diligencia o por casualidad.**

# Etapa 10 — Publicar

*Manage -> Deploy -> Run deployment check*, y despues **Move app to Deployed state**.

> ## No publique todavia
>
> **Las coordenadas de los activos no son reales.** Las **368** se derivan del PK sobre el
> trazado del corredor en cada pasada del generador: son todas distintas y todas estan sobre la
> via, pero **ninguna esta medida en campo**.
>
> Con radios de 0,05 km en la mayoria de los tipos, **el primer tecnico en via no podra cerrar ni
> una orden**. Y se descubre con el tecnico delante.
>
> Es la decision **D-01** y es trabajo de campo. Hasta que llegue, la aplicacion se prueba pero no
> se despliega.

**Y si existe una aplicacion anterior sobre la misma hoja, despubliquela antes.** Dos aplicaciones
sobre un backend sin integridad referencial corrompen en silencio: la vieja conserva permisos que
el modelo nuevo ya no concede.

> **El paso 10 es el punto de no retorno.** Todo lo anterior se abandona sin coste. Compruebe la
> etapa 9 entera **antes** de despublicar nada.

---

# Acta — para rellenar al terminar

**No lo de por cerrado usted.** Este proyecto tiene tres cierres reportados que no resistieron la
comprobacion contra el archivo.

```
Etapa 0   copia hecha ............................ [  ]   nombre del archivo:
          pestanas ocultas ....................... [  ]   cuantas: 
          verificar_faseA.py ..................... [  ]   salida:

Etapa 2   tablas dadas de alta ................... [  ]   cuantas de 28:
          duplicadas ............................. [  ]   cuales:

Etapa 3   claves simples y Text .................. [  ]   cuantas de 28:
          alguna compuesta ....................... [  ]   cual:

Etapa 5   referencias puestas .................... [  ]   cuantas de 39:
          IsPartOf ............................... [  ]   cuantas de 4:
          MAN.OTID desmarcado .................... [  ]
          [OTID].[ActivoID].[Ubicacion_LatLong] .......... [  ]   salida:
          [OTID].[TecnicoID].[Correo] ............ [  ]   salida:

Etapa 6   RETIRADA. No se ejecuta: la hoja vigente no trae columnas que ocultar
          F-19 en verde .......................... [  ]   salida:

Etapa 7   reglas puestas ......................... [  ]   cuantas de 23:
          Deletes quitado en OT y MAN ............ [  ]
          umbral con ISBLANK ..................... [  ]

Etapa 9   cierre cercano aceptado ................ [  ]
          cierre lejano rechazado ................ [  ]
          dato leido en la hoja .................. [  ]
          borrado no disponible .................. [  ]
          REF_ROWS(...,"Activo") ................. [  ]   que dijo:

Errores en rojo que aparecieron, con su texto literal:


Cosas que no salieron como dice esta guia:

```

---
*Generado de `scripts/modelo_objetivo.py` por `scripts/generar_guia_funcional.py`.*
