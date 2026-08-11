# El sistema, tal como es

**No es una especificación.** Una `ESPEC` propone un cambio, y por eso pasa por verificador,
arquitecto y ejecutor. Esto no propone nada: describe qué es el SGMC hoy, en presente, y es la línea
de partida contra la que se leen las demás.

Y por eso tampoco tiene un documento de pruebas. **Su comprobación es mecánica:**

```bash
python scripts/verificar_sistema.py
```

Cada afirmación de aquí sale de un comando, y ese verificador los corre y compara. Un documento que
se desmiente solo cuando envejece es lo contrario de lo que ha pasado seis veces en este proyecto
con cifras que nadie volvió a mirar. Lo que falta o está a medias vive en [`ESTADO.md`](../ESTADO.md);
cómo se llegó hasta aquí vive en `git log` y en las actas. Nada de eso está aquí.

| | |
|---|---|
| Aplicación | AppSheet [`_SISGA_-323965761`](https://www.appsheet.com/template/appdef?appId=aca92ac5-a6eb-4c73-be81-471a5b3fe04e) |
| Datos | Google Sheets [`Modelo_Datos_10082026`](https://docs.google.com/spreadsheets/d/1h9kyCYGK6esRL1UiTcPXHlSmDQcPb13fNZ0hBznYOa0) |

Ambos identificadores salen de `python scripts/sistema.py`, que también lista, con su motivo, las
aplicaciones y hojas superadas. Un identificador que no aparezca ahí como vigente no es este sistema.

## 1. Qué resuelve

El SGMC lleva el mantenimiento en campo de la infraestructura tecnológica, eléctrica y de TI del
corredor de la **Concesión Transversal del Sisga S.A.S.**: un técnico llega a un activo, ejecuta el
checklist de su tipo, deja evidencia fotográfica y firmada, y esa ejecución queda probada ante un
tercero — la interventoría.

Responde una pregunta que hoy se responde a mano, sumando partes de papel: cuánto de lo planeado se
ejecutó. Con el sistema esa cifra es una resta entre lo programado y lo cerrado, y sale sola. Todo lo
demás — geolocalización, fotografías, firma, histórico — existe para que esa cifra sea defendible, no
solo cierta. El desarrollo completo, con el ciclo de la orden y qué prueba y qué no prueba el
sistema, está en [`docs/FUNCIONAL_SGMC.md`](FUNCIONAL_SGMC.md); qué se mantiene y de dónde sale
cada cifra de dominio, en [`docs/CONTEXTO_OPERACION.md`](CONTEXTO_OPERACION.md).

## 2. De qué se compone

Tres piezas, sin solapar:

| Pieza | Qué es | Quién la gobierna |
|---|---|---|
| **La hoja de Google** (`Modelo_Datos_10082026`) | El backend de datos: 29 pestañas, una por tabla más `Enums`. Es exactamente `BD/Modelo_Datos_PLANTILLA.xlsx` mientras nadie la edite a mano en el Sheets | Se genera con `python scripts/generar_plantilla.py`. No se edita a mano |
| **La aplicación de AppSheet** (`_SISGA_-323965761`) | El cliente: móvil offline-first para el técnico, portal web para supervisor y administrador. Lee la hoja de arriba | Se configura a mano en el editor de AppSheet; el repositorio la describe y audita, no la crea |
| **El repositorio** | Genera la hoja y describe la aplicación. La fuente única del diseño es `scripts/modelo_objetivo.py`; todo lo demás —validador, diccionario, manual, plantilla— se deriva de ahí | Nada se documenta a mano: se cambia el modelo y se regenera |

El repositorio no toca producción directamente salvo por lectura: `verificar_app.py` y
`auditar_cableado.py` leen la aplicación en vivo por API con la acción `Find` únicamente; escribir en
el editor —tipos, claves, `Label`, reglas, bots— es trabajo manual de quien tiene acceso a AppSheet.

## 3. El modelo

28 tablas, 210 columnas, 39 referencias, 21 reglas — la cifra la imprime `python
scripts/validar_modelo.py` en su primera línea, no se cita de memoria. Vive entera en
`scripts/modelo_objetivo.py`; se lee formateada en
[`docs/ARQUITECTURA_OBJETIVO_SGMC.md`](ARQUITECTURA_OBJETIVO_SGMC.md) (generado, no editar) y se
compara contra la hoja real en [`docs/bd.md`](bd.md) (generado del `.xlsx`).

Seis grupos: catálogos (14 tablas), la tabla maestra `ACT_Activos` (1), transaccionales (4:
`OT_OrdenesTrabajo`, `MAN_Mantenimientos`, `NOV_Novedades`, `PLA_PlanMantenimiento`), evidencias (2:
`FOT_Fotografias`, `FIR_Firmas`), checklist (2: `CHK_Checklists`, `CHD_ChecklistDetalle`) y motor de
formularios (5: `FRM_Formularios`, `FRM_Secciones`, `FRM_Preguntas`, `TPR_TiposRespuesta`,
`LST_ValoresLista`). El diagrama de referencias completo está en `README.md` §5, generado del mismo
modelo.

Cinco tablas se declaran retiradas y no cuentan en las 28 — `GPS` (duplicaba las columnas de captura
de `MAN_Mantenimientos` y nunca recibió un registro), `FRM_SOS`, `FRM_CCTV`, `FRM_PMVF` (hojas planas
que el motor `FRM_Preguntas` reemplaza) y `SEC_Secciones` (duplicada con `FRM_Secciones`). Viven en
`RETIRADAS` de `scripts/modelo_objetivo.py`, no en `MODELO`: si un documento las cita como vigentes,
está desactualizado.

## 4. Las decisiones que gobiernan el diseño

**La evidencia no se borra.** `OT_OrdenesTrabajo` (`RG-14`) y `MAN_Mantenimientos` (`RG-15`) declaran
`Are updates allowed: Updates, Adds`, sin `Deletes`: un error se corrige con `Activo = FALSE`, que
deja traza de que existió. Por eso `MAN_Mantenimientos.OTID` es la única referencia de una tabla hija
hacia su padre transaccional que **no** lleva `IsPartOf` — marcarlo encadenaría el borrado de una
orden con el de su ejecución, sus fotografías, sus firmas y su checklist. `FOT_Fotografias`,
`FIR_Firmas`, `CHK_Checklists` y `CHD_ChecklistDetalle` sí llevan `IsPartOf` hacia
`MAN_Mantenimientos` o `CHK_Checklists`, y es inofensivo porque ese padre nunca se borra: `IsPartOf`
describe composición, no protege por sí solo, la protección es retirar `Deletes` más arriba en la
cadena. Esta garantía es de la capa de aplicación: quien escribe directamente en el Sheets —hoy dos
cuentas tienen permiso de edición— se la salta.

**El geofencing compara contra un radio por tipo de activo, no uno global.** `RG-01` valida
`DISTANCE([Coordenadas_Cierre_LatLong], [OTID].[ActivoID].[Ubicacion_LatLong]) <=
[OTID].[ActivoID].[TipoActivoID].[RadioGeofencingKm]`, y `TIP_TiposActivo.RadioGeofencingKm` trae
valor en las 27 filas de `scripts/catalogo_tipos.py`: 0,05 km para equipo puntual, 0,1 km para
instalaciones con recinto y 1,5 km para el tramo de fibra, que es lineal y no tiene un "delante". Un
radio único no distingue una subestación de un poste SOS.

**Las claves son alfanuméricas con prefijo, y las de movimiento se generan con `UNIQUEID()`.** Toda
tabla tiene una clave primaria de tipo texto (`ACT-0001`, `TIP-001`); un `Number` hace que AppSheet
descarte en silencio la fila cuya clave llega como texto. Ocho tablas —las que reciben filas creadas
por la aplicación en movimiento, no por el generador— resuelven su clave con `Initial value =
UNIQUEID()` en vez de una clave legible: `MAN_Mantenimientos`, `CHK_Checklists`,
`CHD_ChecklistDetalle`, `FOT_Fotografias`, `FIR_Firmas`, `NOV_Novedades`, `OT_OrdenesTrabajo` y
`PLA_PlanMantenimiento` (`CLAVE_GENERADA` en `scripts/modelo_objetivo.py`). Una fórmula compuesta
—prefijo más consecutivo— se descarta: AppSheet es offline-first con consistencia eventual, y un
contador calculado en el dispositivo no tiene forma de coordinarse entre dos técnicos sin señal.

**Las etiquetas de `OT_OrdenesTrabajo` y `PLA_PlanMantenimiento` son columnas virtuales, no columnas
de la hoja.** Con la clave resuelta por `UNIQUEID()`, ninguna de las dos identifica nada ante un
humano. `RG-35` y `RG-36` declaran una columna `Etiqueta` calculada con `CONCATENATE()` —marcada
`Label` en el editor—, que AppSheet recalcula en cada sincronización y nunca escribe en el Sheets:
`scripts/inferencia.py` la resuelve por `ETIQUETA_VIRTUAL`, no por `MODELO`, porque una columna
virtual no vive en la hoja y `python scripts/verificar_faseA.py` no la exige ahí.

**Lo que la plataforma decide y el repositorio solo declara: tipo, clave y `Label`.** Un `col(...)`
en `scripts/modelo_objetivo.py` dice qué tipo, qué clave y qué etiqueta *debería* tener cada columna;
que AppSheet lo tenga puesto así es un hecho del editor, no del repositorio, y ningún archivo lo
puede afirmar sin decir cómo se comprobó. `scripts/lectura_de_vuelta.py` declara, para cada clase de
cambio, quién lo lee de vuelta y con qué instrumento — ver §5.

## 5. Qué se puede comprobar y qué no

Siete scripts verifican el repositorio contra sí mismo o contra un archivo, y ninguno sustituye a
otro:

| Script | Mide |
|---|---|
| `python scripts/validar_modelo.py` | El modelo consigo mismo: tipos, claves, rutas de desreferencia, reglas |
| `python scripts/verificar_faseA.py <xlsx>` | El modelo contra la hoja descargada: estructura, tipos, pestañas |
| `python scripts/verificar_datos.py` | Los datos de esa misma hoja: obligatorias vacías, referencias huérfanas, homogeneidad de tipo |
| `python scripts/verificar_documentos.py` | La prosa de los `.md` contra el modelo |
| `python scripts/verificar_enlaces.py` | Que todo enlace relativo entre documentos resuelve |
| `python scripts/verificar_reproducible.py` | Que generar la plantilla dos veces dé el mismo archivo |
| `python scripts/verificar_app.py` | Que la aplicación en vivo vea lo que el repositorio declara —estructura de filas, por API, solo lectura |

Aparte hay un **auditor**, `python scripts/auditar_cableado.py`, que no mide el repositorio sino el
cableado real de la aplicación contra el modelo, leyendo por API; y una **instantánea**, `python
scripts/instantanea.py`, que fotografía los datos vivos y compara dos fotografías celda a celda —
necesaria porque una `App formula` o un bot escriben en la hoja y ese cambio no se revierte
cambiando un desplegable.

**Y cuatro cosas que ningún comando puede mirar**, declaradas así en `scripts/lectura_de_vuelta.py`
para que un paso sin comprobación no se lea como comprobado:

| Qué | Por qué no hay comando |
|---|---|
| **Tipos** de columna | La API v2 devuelve filas, no esquema |
| **Expresiones** (`Valid_If`, `App formula`, `Initial value`, `Editable_If`, `Security Filter`) | No viajan por la API |
| **Permisos** (`Are updates allowed`) | No viajan por la API, y además la API tiene más permisos que la aplicación: se salta el `Deletes` retirado |
| **Etiqueta** (`Label`) | Es lo que ve el técnico en los desplegables; solo se mira en `Data > Columns` |

Estas cuatro se cierran copiando el texto literal que se ve en el editor, no afirmando que
"coincide": coincidir no es evidencia, el texto sí.

## 6. Los límites que hoy tiene

- **La cuenta es gratuita.** Los bots con evento programado no se ejecutan en el horario indicado
  —solo se pueden invocar a mano con `Test`—, y en cuenta gratuita el correo de un bot programado
  llega únicamente al propietario de la aplicación. Sin plan Core no hay API REST para integración ni
  para pruebas automatizadas.
- **Las coordenadas de `ACT_Activos` están derivadas, ninguna medida en campo.** Cada punto sale del
  `PK` del activo proyectado sobre el trazado, no de un GPS en sitio.
- **288 de las 333 preguntas del banco de checklists son borrador**, marcadas `[BORRADOR: validar con
  operacion]` en su ayuda; 45 —`FRM_SOS`, `FRM_CCTV`, `FRM_PMVF`, 15 cada uno— están acordadas.
- **Las imágenes se guardan en el Drive del propietario de la hoja**, hoy una cuenta personal con 15
  GB compartidos entre documento y fotografías.
- **La sincronización se degrada por encima de ~50.000 filas por tabla.** `python
  scripts/capacidad.py` deriva el crecimiento año a año a partir de `ACT_Activos`, no a ojo.
- **Ninguna garantía de integridad vive en la hoja.** Ni unicidad, ni tipos, ni referencial: todas las
  reglas —`Valid_If`, `Required_If`, referencias— viven en la capa de aplicación, y hoy hay dos
  cuentas con permiso de edición directa sobre el Sheets.
