# CLAUDE.md — SGMC (Concesión Transversal del Sisga S.A.S.)

Instrucciones de trabajo para agentes en este repositorio. Léelo antes de tocar cualquier archivo.

## 1. Qué es este proyecto

SGMC (Sistema de Gestión de Mantenimiento en Campo) digitaliza la inspección y el mantenimiento
preventivo/correctivo de la infraestructura ITS, eléctrica y de TI del corredor de la Concesión
Transversal del Sisga.

No es un repositorio de código de aplicación. Es un repositorio **documental y de modelo de datos**
de un sistema construido sobre **Google AppSheet** (no-code) con backend en **Google Sheets**.
El entregable de este repo es el As-Built: especificaciones, diccionario de datos, manuales,
dictámenes de auditoría y el archivo Excel maestro.

- Aplicación: AppSheet `SGMC-886843353` (app en vivo, enlaces en `README.md`)
- Backend de producción: Google Sheets `1a4MmZ0u9sNgWmyiR2OPJo9YuUEKJFftbJWMW-KbITRc`
- Repositorio remoto: `github.com/dieleoz/SGMC`

## 2. Dónde está la verdad: hay dos modelos y no coinciden

**Verificado el 2026-08-06: el Excel local y el Google Sheets de producción son modelos
distintos.** No es deriva menor: difieren en las tablas que más importan. Cualquier afirmación
sobre "el modelo" es ambigua hasta que declares cuál de los dos leíste.

| Tabla | `BD/Modelo de Datos (2).xlsx` (local) | Google Sheets (producción) |
|---|---|---|
| `TIP_TiposActivo.FormularioID` | Vacío en los 18 tipos | **Poblado en los 18** |
| `MAN_Mantenimientos` | 24 col, **con** `Coordenadas_Cierre` y `Precision_GPS` | 25 col, **sin** esas dos. Tiene `Diagnostico`, `Trabajo_Realizado`, `Duracion_Minutos`, `Repuestos_Utilizados`, `Requiere_Repuesto` |
| `CHK_Checklists` | 9 col, 1 fila | 21 col, 3 filas |
| `CHD_ChecklistDetalle` | 6 col, pregunta en texto libre | 21 col, **con `PreguntaID`** |
| `CHK.OTID` del registro `d02d8a3d` | `'1'`, huérfano | `'OT-0001'`, válido |

Consecuencia que manda sobre todo lo demás: **en producción no existen las columnas de GPS**, así
que la regla de geofencing no está mal configurada, es que no se puede configurar. El campo sobre
el que se evalúa no existe en el backend que corre la app.

Reglas mientras esto no se reconcilie:
- El **Sheets es el que corre la app**. El Excel es un registro paralelo que alguien ha estado
  editando por separado. Ante una discrepancia, manda producción.
- **Antes de afirmar cualquier cosa sobre el modelo, lee producción**, no el Excel. Se lee con el
  conector de Google Drive: `fileId = 1a4MmZ0u9sNgWmyiR2OPJo9YuUEKJFftbJWMW-KbITRc`.
- Al reportar un hallazgo, escribe siempre contra cuál de los dos lo verificaste.
- No "sincronices" uno con otro sin decisión explícita: ninguno es superconjunto del otro y
  copiar en cualquier dirección destruye trabajo.
- `entregables/Modelo_Datos_SGMC_AsBuilt.xlsx` es copia byte a byte del Excel local
  (sha256 verificado). Artefacto de publicación, no una tercera fuente.

## 2.1 Gobierno del backend

El Sheets de producción es propiedad de `valentinwebdeveloper@gmail.com`, una cuenta personal de
Gmail, no del dominio corporativo. La Concesión no controla su propio backend. Es un riesgo que
entra en la decisión D-14 y que conviene resolver antes de la salida a producción.

## 3. Regla de verificación (no negociable)

Este proyecto arrastra un historial de subsanaciones reportadas como cerradas que no lo estaban.

- **No declares nada conforme por reporte. Verifícalo contra el archivo.**
- Para el Excel, usa `openpyxl` (disponible, 3.1.5) y muestra el dato leído, no un resumen.
- Distingue siempre **estructura** de **población**: que exista la columna no significa que el
  campo tenga datos, y que la tabla exista no significa que el flujo se haya ejercitado.
  Cuatro tablas del modelo están hoy vacías (`MAN_Mantenimientos`, `FOT_Fotografias`,
  `FIR_Firmas`, `GPS`).
- Al cerrar un hallazgo, deja constancia de con qué comando y qué salida lo cerraste.

## 4. Convenciones de entregables

- **Sin emojis ni iconos decorativos** en documentos, mensajes de error de la app y textos de
  interfaz. Los documentos heredados los tienen; al reescribir uno, quítalos.
- Español, con las tildes correctas. Ojo: varias hojas del Excel tienen encabezados con
  mojibake (`Descripci�n`, `T�cnicoID`, `Secci�n`) por codificación; al leer, no los normalices
  silenciosamente — repórtalos como hallazgo.
- No hagas commit ni push salvo petición explícita.

## 5. Nomenclatura del modelo

Prefijos de tabla por dominio: `USR_` usuarios, `ROL_` roles, `SED_` sedes, `TIP_` tipos de
activo, `ACT_` activos, `OT_` órdenes de trabajo, `MAN_` mantenimientos, `CHK_`/`CHD_` checklist
encabezado y detalle, `FOT_`/`FIR_` evidencias, `FRM_` formularios y preguntas, `TPR_` tipos de
respuesta, `LST_` listas de valores, `EST_`/`FRE_`/`CAL_`/`SEN_` catálogos.

Advertencia sobre claves: la nomenclatura **no** es uniforme. `OT_OrdenesTrabajo` no tiene columna
`OTID`; su primera columna es `Numero_OT` con valores `OT-0001`. Otras tablas referencian `OTID`.
Verifica la clave real antes de asumirla.

## 6. Fórmulas y reglas de la app

Geofencing de cierre (RF-012). `ACT_Activos` guarda un único campo `Ubicacion` de tipo LatLong;
no existen columnas `Latitud`/`Longitud` separadas. La fórmula correcta es:

```
DISTANCE([Coordenadas_Cierre], [ActivoID].[Ubicacion]) <= 1.0
```

Mensaje de error, en texto plano:

```
Ubicación fuera de rango: debe estar a menos de 1.0 km del activo.
```

Toda variante con `LATLONG([ActivoID].[Latitud], [ActivoID].[Longitud])` es incorrecta contra este
modelo y falla en ejecución.

Security Filter por sede (RF-004): filtra `ACT_Activos` por el `SedeID` del usuario resuelto vía
`USEREMAIL()` contra `USR_Usuarios`.

## 7. Estado real (verificado 2026-08-06)

La Fase 0 **no está cerrada**. `docs/ROADMAP.md` ya fue corregido; `docs/DICTAMEN_AUDITORIA_LOCAL_SGMC.md` sigue afirmando lo contrario.

**Confirmados en producción** (leídos en el Sheets, no en el Excel):

1. Los 34 activos de `ACT_Activos` comparten una sola coordenada, `4.728512, -74.114531`, que está
   en Bogotá y no en el corredor.
2. `MAN_Mantenimientos` **no tiene `Coordenadas_Cierre` ni `Precision_GPS`**: el geofencing
   (RF-012) y la captura de precisión (RF-011) no pueden ni configurarse.
3. Solo `FRM_SOS` tiene banco de preguntas en `FRM_Preguntas` (15). Faltan 17 de 18.
4. Todos los usuarios están en `SedeID = 1`; todos los activos en `SedeID` 7 a 10. El Security
   Filter dejaría a cada técnico con cero activos.
5. `MAN_Mantenimientos`, `FOT_Fotografias`, `FIR_Firmas` y `GPS` están vacías: el ciclo nunca se
   ha ejecutado.
6. Evidencias modeladas por duplicado (campos en `MAN` + tablas hijas vacías).
7. Datos de prueba sin limpiar en `CHK_Checklists`: el registro `CHK001` trae
   `TecnicoID = "Santiago Moreno"` en lugar de un identificador y `FechaInicio = "NOW()"` como
   texto literal.

**Resueltos en producción, pendientes solo en el Excel local:** el mapeo
`TIP_TiposActivo.FormularioID`, la trazabilidad de `CHD_ChecklistDetalle` mediante `PreguntaID`, y
el checklist huérfano.

Detalle, evidencia y remediación en `docs/AUDITORIA_PLAN_Y_ROADMAP.md`.

El documento de las 14 decisiones **ya se envió** al líder funcional y se está a la espera de su
respuesta. No generes ni propongas reenviarle una versión corregida: insistir sobre lo mismo resta
credibilidad a la petición. Lo que se aprenda entretanto se acumula para un **Sprint 2** con el
funcional.

No configures ni construyas sobre un punto que dependa de una decisión abierta en
`docs/DEFINICION_FUNCIONAL_MESA_DE_TRABAJO.md`. La ruta crítica es D-01 (coordenadas reales de los
34 activos) y D-09 (bancos de preguntas), ambas trabajo del cliente.

**El frente que sí puede avanzar sin el funcional es la Fase 0.5**: reconciliar los dos modelos,
agregar las columnas de GPS en producción y limpiar los datos de prueba. Ver `docs/ROADMAP.md`.

Lo que sí está verificado como resuelto: `Coordenadas_Cierre` y `Precision_GPS` existen en
`MAN_Mantenimientos`; la columna `Observaciones` ya no está duplicada (24 columnas únicas).

## 8. Deriva documental conocida

Estos documentos contienen afirmaciones que no corresponden al archivo real. No los uses como
fuente sin contrastar:

- `docs/bd.md` — **corrección**: una revisión anterior marcó su sección 3.1 como inventada por
  describir un `MAN_Mantenimientos` de 25 columnas con `MttoID`, `Diagnostico`,
  `Trabajo_Realizado` y `Duracion_Minutos`. Estaba describiendo **producción**, y es correcta.
  Lo mismo su conteo de 21 columnas para `CHK`/`CHD`. Lo desactualizado es el Excel local.
  `bd.md` sigue sin declarar contra cuál de los dos modelos está escrito, y eso hay que corregirlo.
- `docs/DICTAMEN_AUDITORIA_LOCAL_SGMC.md` e `docs/INFORME_QA_ISTQB_Y_AUDITORIA_ARQUITECTO.md` — dictaminan
  100% conforme sobre un modelo anterior y describen un mantenimiento ejecutado en vivo que no
  existe en `MAN_Mantenimientos` (0 filas).

## 9. Estructura del repositorio

```
README.md          Entrada: qué es el proyecto, cómo funciona, estado real
CLAUDE.md          Este archivo
MAP.md             Índice maestro y referencias cruzadas

BD/                FUENTE DE VERDAD: Modelo de Datos (2).xlsx, 24 hojas
docs/              Documentación técnica y funcional (.md)
  images/          Figuras de los documentos (fig_01 a fig_05)
  prompts/         Directivas para agentes de auditoría
Manuales/          Manuales de usuario
  images/          Maquetas del manual (img_01 a img_06)
entregables/       Word y Excel listos para enviar al cliente
scripts/           Generadores de figuras y documentos
archivo/           Material de origen. No versionado (en .gitignore)
```

Reglas de ubicación al crear archivos:

- Un `.md` de documentación va en `docs/`. Solo README, CLAUDE y MAP viven en la raíz.
- Un `.py` va en `scripts/` y resuelve sus rutas desde la raíz del repositorio con
  `os.path.dirname(os.path.dirname(os.path.abspath(__file__)))`. Nunca rutas absolutas `D:\`.
- Un `.docx` o `.xlsx` destinado al cliente va en `entregables/`. Los manuales van en `Manuales/`.
- Las figuras de un documento van en `docs/images/`; las del manual, en `Manuales/images/`.
- Todo documento nuevo se enlaza en `MAP.md` y en la tabla de `README.md`.

## 10. Alcance

El agente no tiene acceso al editor de AppSheet ni al Google Sheets de producción. Puede auditar
y corregir el Excel maestro y la documentación; las configuraciones en AppSheet se **especifican**
aquí para que un operador humano las aplique, y se marcan como pendientes de verificación hasta
que alguien confirme la aplicación con evidencia.
