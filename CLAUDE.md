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

## 2. Única fuente de verdad

`BD/Modelo de Datos (2).xlsx` — 24 hojas. Es el único modelo de datos válido.

`entregables/Modelo_Datos_SGMC_AsBuilt.xlsx` es una **copia byte a byte idéntica** del anterior
(sha256 verificado el 2026-08-06). Es un artefacto de publicación, no una segunda fuente.

Reglas:
- Nunca edites los dos archivos. Edita `BD/Modelo de Datos (2).xlsx` y replica.
- El modelo viejo de 17/18 hojas está retirado. Si un documento lo menciona, es deriva documental
  y debe corregirse, no seguirse.
- El Excel local y el Google Sheets de producción deben mantenerse alineados. Si divergen, el
  Sheets es el que corre en la app; el Excel es el registro As-Built. Declara cuál verificaste.

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
Bloqueantes vigentes, en orden:

1. Los 34 activos de `ACT_Activos` comparten una sola coordenada, `4.728512, -74.114531`, que está
   en Bogotá y no en el corredor. El geofencing es inoperante.
2. `TIP_TiposActivo.FormularioID` está vacío en los 18 tipos: la asignación automática de checklist
   (RF-007/RF-008) no tiene mapeo.
3. Solo `FRM_SOS` tiene banco de preguntas en `FRM_Preguntas` (15). Faltan 17 de 18.
4. Todos los usuarios están en `SedeID = 1`; todos los activos en `SedeID` 7 a 10. El Security
   Filter dejaría a cada técnico con cero activos.
5. `CHK_Checklists.OTID = '1'` es huérfano frente a las claves `OT-0001..OT-0006`.
6. Evidencias y GPS modelados por duplicado (campos en `MAN` + tablas hijas vacías).

Detalle, evidencia y remediación en `docs/AUDITORIA_PLAN_Y_ROADMAP.md`.

El proyecto está en **Sprint 0: definición funcional**. La mayoría de los bloqueantes no son
errores de implementación sino decisiones de negocio sin tomar. No configures ni construyas sobre
un punto que dependa de una decisión abierta en `docs/DEFINICION_FUNCIONAL_MESA_DE_TRABAJO.md`: primero
se cierra la mesa con el líder funcional, y de ahí sale el roadmap. La ruta crítica es D-01
(coordenadas reales de los 34 activos) y D-09 (bancos de preguntas), ambas trabajo del cliente.

Lo que sí está verificado como resuelto: `Coordenadas_Cierre` y `Precision_GPS` existen en
`MAN_Mantenimientos`; la columna `Observaciones` ya no está duplicada (24 columnas únicas).

## 8. Deriva documental conocida

Estos documentos contienen afirmaciones que no corresponden al archivo real. No los uses como
fuente sin contrastar:

- `docs/bd.md` — la sección 3.1 lista un `MAN_Mantenimientos` de 25 columnas con nombres que no existen
  (`MttoID`, `Diagnostico`, `Trabajo_Realizado`, `Duracion_Minutos`); el real tiene 24 con otros
  nombres. Declara `CHK`/`CHD` con 21 columnas; tienen 9 y 6.
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
