# Reglas del modelo de datos

**Cualquier cambio en el modelo, en la plantilla o en la aplicación tiene que respetarlas.**

**Generado** por `scripts/generar_reglas_datos.py`. No editar a mano: las listas salen de
`scripts/modelo_objetivo.py`, así que la única forma de que este documento mienta es que mienta
el modelo.

Ninguna de estas reglas es una preferencia de estilo. **Todas salieron de un fallo que llegó a
producción o estuvo a punto**, y cada una lleva escrito cuál, porque el motivo es lo que hace
que alguien la respete en vez de saltársela.

La columna que más importa es la última: **quién la hace cumplir**. Una regla que no comprueba
nadie es una intención, no una regla.

---

## 1. Cómo AppSheet decide el tipo de una columna, y qué se hace al respecto

**AppSheet no lee el tipo de la hoja: lo infiere**, del nombre de la cabecera y del contenido de
las filas. Subir el Excel arregla la hoja, no la aplicación — son dos sitios distintos, y
reimportar no cambia la inferencia porque los datos son los mismos.

Ver `BASE_CONOCIMIENTO_APPSHEET.md` §13, con la cita oficial.

### R-01 · Toda clave es alfanumérica con prefijo

**Por qué.** AppSheet tipa la clave según la mayoría de sus valores. Si son `1`, `2`, `3` la
tipa `Number`, y entonces **una fila con clave alfanumérica se descarta sin avisar**. Pasó el
2026-08-10: `USR_Usuarios` tenía diez claves numéricas y una generada con `UNIQUEID`, y un
técnico no existía para la aplicación. Se vio porque la API devolvía 10 filas y la hoja tenía 11.

**Y no es solo la clave.** `LST_ValoresLista` mezclaba 4 numéricas con 104 de texto: AppSheet
habría descartado las cuatro, que eran los valores del desplegable del único checklist acordado.

Las claves de hoy, derivadas de la plantilla:

```
ACT-0001   TIP-001   UNF-01   SED-001   USR-001   ROL-01
EST-01     FRE-01    CAL-01   SEC-01    TPR-01
OT-0001    MOT-01    FAL-01   ASG-01    PLA-001   FRM_SOS   SOS001   UMBRAL_GPS
```

**Quién la hace cumplir:** `F-20` de `verificar_faseA.py`, que falla si una clave mezcla
numéricas y de texto, y avisa si es enteramente numérica.

### R-02 · Una columna de coordenada lleva `_LatLong` en el nombre

**Por qué.** AppSheet infiere `LatLong` cuando la cabecera contiene `latlong` o `geolocation`.
`Ubicacion` no dispara nada, así que entraba como `Text` — y `DISTANCE()` no funciona sobre
texto. Son nombres feos a cambio de que el tipo entre solo en cada reconstrucción.

Las 6 de hoy:

- `SED_Sedes.Ubicacion_LatLong`
- `ACT_Activos.Ubicacion_LatLong`
- `MAN_Mantenimientos.UbicacionEscaneo_LatLong`
- `MAN_Mantenimientos.Coordenadas_Cierre_LatLong`
- `NOV_Novedades.Ubicacion_LatLong`
- `FOT_Fotografias.Ubicacion_LatLong`

**Quién la hace cumplir:** nadie todavía. Es una regla que hay que recordar al declarar una
columna de coordenada nueva.

### R-03 · Las referencias no se infieren nunca: se ponen a mano

**Por qué.** AppSheet infiere `Ref` cuando el nombre de una columna se parece al de una tabla
existente. Nuestras tablas llevan prefijo —`UNF_UnidadesFuncionales`, no `UnidadFuncional`—, así
que el parecido se rompe. **Es el coste de la convención y a la vez su protección**: impide que
AppSheet invente referencias.

Y explica las tres trampas que costaron un día: `CHK_Checklists.ActivoID`,
`OT_OrdenesTrabajo.FormularioID` y `CHD_ChecklistDetalle.TipoRespuestaID` **sí** se convertían
solas, porque su nombre coincidía con la clave de otra tabla.

Hoy son **39 referencias**, 4 de ellas con `IsPartOf`.

**Quién la hace cumplir:** `V-05` de `validar_modelo.py` comprueba que ninguna quede huérfana en
el modelo. **Que estén puestas en la aplicación no lo comprueba nadie**: es trabajo de editor y
de `PRUEBA-003`.

---

## 2. Cómo se cambia el modelo sin romper lo que ya hay

### R-04 · Una referencia que resuelve puede apuntar a lo que no es

**Por qué.** Es el fallo que más veces se ha repetido, y las tres veces lo encontró una persona:

- El inventario sintético arrancó en `ActivoID 1` y **reescribió los 34 activos reales**. Las
  órdenes pasaron a apuntar a otro equipo, y la referencia seguía resolviendo.
- Nueve familias del Plan Maestro colgaban del tipo de otra cosa: **78 activos con el checklist
  equivocado**, y `TipoActivoID` apuntaba a una fila que existe.
- 107 activos estaban en la unidad funcional equivocada, porque las UF se repartían en cuartos
  iguales y no lo son.

**La comprobación de huérfanos contesta «apunta a algo», nunca «apunta a lo correcto».**

**Quién la hace cumplir:** nadie de forma general. `catalogo_tipos.comprobar()` cubre el caso de
los tipos. Para lo demás, hay que derivarlo del dominio y comprobarlo a propósito.

### R-05 · Cambiar una clave se propaga solo, nunca a mano

**Por qué.** Al resembrar las once claves numéricas, el cambio afectó a **2.502 valores de
referencia** repartidos por diez tablas. Hacerlo a mano sería garantizar el olvido de alguna, y
una referencia olvidada apunta a una clave que ya no existe.

`generar_plantilla.py` lo hace derivando de `MODELO` qué columnas apuntan a la tabla que cambia.

**Quién la hace cumplir:** `verificar_faseA.py`, que detecta huérfanos entre la hoja y sus
tablas destino.

### R-06 · El generador tiene que dar lo mismo dos veces

**Por qué.** Al resembrar las claves, la garantía de catálogo buscaba las filas **por clave**; la
resiembra cambiaba esa clave; en la pasada siguiente las volvía a añadir. `SED_Sedes` acabó con
las seis edificaciones **duplicadas** y cada ejecución habría añadido seis más.

**Pasó los cuatro verificadores que había**, porque todos miran un archivo y el defecto solo
existe entre dos ejecuciones. De ahí la regla derivada: **el catálogo se empareja por la clave
natural —el nombre—, nunca por la clave generada.**

**Quién la hace cumplir:** `verificar_reproducible.py`, que genera dos veces y compara celda a
celda.

### R-07 · El dato y la prosa no comparten campo

**Por qué.** Los valores de un `Enum` vivían dentro de su nota, y el generador del manual partía
la nota por comas: publicó un valor llamado `Baja. Pondera la disponibilidad de D-13` y otro con
un párrafo entero dentro. Ahora `valores=` es el dato y `nota=` es la prosa.

Hoy hay **12 columnas `Enum`**, y 1 sin declarar: `CHD_ChecklistDetalle.RespuestaLista`.

**Quién la hace cumplir:** el generador del manual, que ya no inventa valores: si faltan, lo
dice en vez de deducirlos.

### R-08 · Una columna dice lo que es, no lo que se le parece

**Por qué.** `ACT_Activos.PR` guardaba el kilómetro lineal del proyecto, que es un **PK**. Y
`UNF_UnidadesFuncionales.PRInicial` lo mismo. La columna prometía una referencia de INVÍAS y
contenía otra cosa, y nadie lo veía porque había un valor y parecía correcto.

**El PR y el PK son dos datos distintos y todo elemento tiene ambos**: el PK es lineal y continuo
del proyecto; el PR es de INVÍAS, pertenece a un tramo y reinicia en cada uno. El corredor
atraviesa tres rutas —`55CN03`, `5607`, `5608`— y **tiene dos puntos distintos llamados
`PR 0+000`**, separados por unos 50 km.

**Quién la hace cumplir:** nadie. Es la regla más difícil de mecanizar, porque el defecto es
semántico: la comprobación ve un valor y no sabe si es el que la columna promete.

### R-09 · Un aplazamiento sin fecha no es un aplazamiento

**Por qué.** `USR_Usuarios.SedeID` estuvo cuatro días declarada `Ref` obligatoria mientras la
especificación la daba por descartada. `D-04` lo detectaba **en cada ejecución**, pero la marca
`'paso 1'` degradaba el fallo a aviso y no tenía fecha, así que nunca vencía.

**Quién la hace cumplir:** `D-04` de `verificar_documentos.py`, que ahora exige `AAAA-MM-DD` y
vuelve a fallar el día que pasa.

### R-10 · Los identificadores viven en un solo sitio

**Por qué.** La aplicación y la hoja estaban escritas a mano en 37 documentos y 10 scripts, y el
sistema se reconstruyó tres veces en cuatro días: nunca se perseguían todos. Se llegó a tener
cinco aplicaciones y tres hojas mencionadas por el repositorio, con la portada ofreciendo un
enlace que daba 404.

**Quién la hace cumplir:** nadie automáticamente. `scripts/sistema.py` es la fuente, y su lista
`SUPERADOS` permite reconocer los abandonados.

### R-11 · La clave y la referencia se llaman igual, y eso decide en qué tabla haces clic

**33 de las 39 referencias** llevan un nombre que **además es clave primaria** de otra tabla.
`EstadoActivoID` es la clave de `EST_Activo` y la referencia hacia ella en `ACT_Activos`. Mismo
nombre, papel opuesto.

**Por qué.** El 2026-08-10, cableando, alguien puso `EstadoActivoID` como `Ref` estando **dentro
de `EST_Activo`**. AppSheet lo rechazó: `contains a cyclical table reference`. Se corrigió sin
daño, pero el error no fue un descuido aislado —es el 84% de los clics posibles—, y esta vez
**AppSheet avisó**, que es lo excepcional: casi todo lo demás de esa semana falló en silencio.

**Qué hacer.** Antes de tocar una columna, mirar en qué tabla estás. En la tabla **destino** ese
nombre es la **clave** y va `Text`; en la tabla **origen** es la **referencia** y va `Ref`. Si
AppSheet habla de referencia cíclica, estás en la tabla equivocada: no cambies la expresión ni
busques otro nombre de columna, cambia de tabla.

**Quién la hace cumplir:** nadie. Es la única de estas reglas que se aplica con el ratón. Lo más
cerca que hay es `scripts/auditar_cableado.py`, que lo ve **después** de hecho.

<details><summary>Las 20 expuestas</summary>

| Columna | Es clave en | Es referencia en |
|---|---|---|
| `ActivoID` | `ACT_Activos` | `OT_OrdenesTrabajo`, `NOV_Novedades`, `PLA_PlanMantenimiento` |
| `CalzadaID` | `CAL_Calzadas` | `ACT_Activos` |
| `ChecklistID` | `CHK_Checklists` | `CHD_ChecklistDetalle` |
| `EstadoActivoID` | `EST_Activo` | `ACT_Activos`, `MAN_Mantenimientos` |
| `EstadoOrdenID` | `EOT_EstadosOrden` | `OT_OrdenesTrabajo` |
| `FormularioID` | `FRM_Formularios` | `TIP_TiposActivo`, `CHK_Checklists`, `FRM_Preguntas` |
| `FrecuenciaID` | `FRE_Frecuencias` | `ACT_Activos`, `PLA_PlanMantenimiento` |
| `MantenimientoID` | `MAN_Mantenimientos` | `FOT_Fotografias`, `FIR_Firmas`, `CHK_Checklists` |
| `ModoFallaID` | `FAL_ModosFalla` | `MAN_Mantenimientos` |
| `MotivoPendienteID` | `MOT_MotivosPendiente` | `MAN_Mantenimientos` |
| `OTID` | `OT_OrdenesTrabajo` | `MAN_Mantenimientos` |
| `PreguntaID` | `FRM_Preguntas` | `CHD_ChecklistDetalle`, `LST_ValoresLista` |
| `RolID` | `ROL_Roles` | `USR_Usuarios` |
| `SeccionID` | `FRM_Secciones` | `FRM_Preguntas` |
| `SedeID` | `SED_Sedes` | `ACT_Activos` |
| `SentidoID` | `SEN_Sentidos` | `ACT_Activos` |
| `TipoActivoID` | `TIP_TiposActivo` | `ACT_Activos`, `FAL_ModosFalla` |
| `TipoRespuestaID` | `TPR_TiposRespuesta` | `FRM_Preguntas` |
| `UnidadFuncionalID` | `UNF_UnidadesFuncionales` | `SED_Sedes`, `ASG_AsignacionZona`, `ACT_Activos` |
| `UsuarioID` | `USR_Usuarios` | `ASG_AsignacionZona`, `NOV_Novedades` |

</details>

---

## 3. Lo que ninguna regla evita

Al dar de alta o regenerar una tabla en AppSheet **hay que entrar a `Data > Columns` y recorrer
la columna `TYPE` contra la ficha del anexo de `MANUAL_DESPLIEGUE.md`**. No hay atajo:

| Qué | Cuántos | Por qué no se infiere |
|---|---|---|
| Referencias `Ref` | 39 | El prefijo de la tabla rompe el parecido de nombre |
| `IsPartOf` | 4 | Es una decisión de borrado en cascada, no un tipo |
| Valores de `Enum` | 12 columnas | AppSheet no sabe qué valores son válidos |
| `ChangeTimestamp` | 4 | Nunca se infiere; llega como texto |
| Expresiones | 23 reglas | `Valid_If`, `Editable_If`, `Initial value`, bots |

**Y una trampa propia de las tablas vacías.** Las 8 que llegan sin filas —las de movimiento—
no le dan a AppSheet ningún dato del que inferir la clave, así que la elige a ciegas. Son las
mismas que generan su clave con `UNIQUEID()`, es decir alfanumérica: **si alguna quedó `Number`,
cada fila que cree un técnico se perderá igual que se perdió aquel usuario.**

- `CHD_ChecklistDetalle`
- `CHK_Checklists`
- `FIR_Firmas`
- `FOT_Fotografias`
- `MAN_Mantenimientos`
- `NOV_Novedades`
- `OT_OrdenesTrabajo`
- `PLA_PlanMantenimiento`

**Se puede sondear sin abrir el editor**: insertar por API una fila con clave alfanumerica y
**leerla de vuelta** antes de borrarla. Si regresa literal, la columna es `Text`. Metodo y sus
limites en `BASE_CONOCIMIENTO_APPSHEET.md` seccion 14 — con la advertencia de que la API tiene
mas permisos que la aplicacion: **no ve el `Deletes` retirado**, asi que sobre una tabla con
historico ese sondeo es justo el fallo contra el que el sistema esta disenado.

