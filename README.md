# SGMC — Sistema de Gestión de Mantenimiento en Campo

Aplicación de campo para la inspección y el mantenimiento de la infraestructura tecnológica,
eléctrica y de TI del corredor vial de la **Concesión Transversal del Sisga S.A.S.**

Construida sobre **Google AppSheet** con backend en **Google Sheets**. Sin servidores propios,
sin compilación de APK, sin Play Console: los técnicos instalan la app de AppSheet e inician
sesión con su cuenta corporativa.

> **Estado del proyecto: Sprint 0 — definición funcional en validación.**
> El modelo de datos y la app existen y están operativos como prototipo, pero la Fase 0 no está
> cerrada, la definición funcional no ha sido validada con el líder funcional, y el 6 de agosto de
> 2026 se detectó que **el Excel local y el backend de producción son modelos distintos**. Ver [Estado real](#estado-real-verificado) y
> [AUDITORIA_PLAN_Y_ROADMAP.md](docs/AUDITORIA_PLAN_Y_ROADMAP.md).
> La arquitectura objetivo está definida y validada automáticamente. La propuesta se envió a
> Dirección y al líder funcional, a la espera de tres decisiones: propiedad del backend, plan de
> licenciamiento y definición contractual de disponibilidad. Ver
> [ARQUITECTURA_OBJETIVO_SGMC.md](docs/ARQUITECTURA_OBJETIVO_SGMC.md) y
> [ALCANCE_Y_SUPUESTOS_SGMC.md](docs/ALCANCE_Y_SUPUESTOS_SGMC.md).
> No desplegar a campo hasta cerrar
> [DEFINICION_FUNCIONAL_MESA_DE_TRABAJO.md](docs/DEFINICION_FUNCIONAL_MESA_DE_TRABAJO.md).

---

## 1. El problema que resuelve

El mantenimiento del corredor se registraba en papel y hojas sueltas. Eso produce cuatro
problemas que el SGMC ataca directamente:

| Problema | Cómo lo resuelve el SGMC |
|---|---|
| No hay evidencia verificable de que el técnico estuvo en el activo | Geofencing GPS: el cierre solo se permite dentro del radio definido para ese tipo de activo, con registro de precisión satelital |
| Buena parte del corredor no tiene señal celular (montaña, túneles) | Operación offline nativa: se diligencia sin red y sincroniza al recuperar conexión |
| Cada tipo de activo requiere una inspección distinta | Checklist dinámico: la app abre el formulario que corresponde al tipo de activo escaneado |
| El CCO se entera tarde de una falla | Bot de automatización: correo con informe PDF cuando un activo queda fuera de servicio |

## 2. Qué gestiona

34 activos catalogados sobre 18 tipos, en cuatro categorías:

- **ITS** — Postes SOS, CCTV, paneles de mensaje variable fijo y móvil (PMVF/PMVM), sensores
  meteorológicos y ambientales (SGM/SGE/SSA), básculas de pesaje
- **Eléctrico** — Generadores, UPS, subestaciones
- **Comunicaciones** — Fibra óptica
- **TI** — Servidores, NAS, switches, routers, firewalls, videowall

## 3. Actores

| Rol | Dónde trabaja | Qué hace |
|---|---|---|
| **Técnico** | App móvil, mayoritariamente offline | Recibe OT, escanea QR, diligencia checklist, toma fotos, firma, cierra con GPS |
| **Supervisor** | Portal web | Programa y asigna OT, revisa evidencias, aprueba, consulta el tablero |
| **Administrador** | Portal web | Gestiona usuarios, catálogos, activos y formularios de inspección |
| **Consulta** | Portal web | Solo lectura y reportes |

## 4. Cómo funciona

```mermaid
graph TD
    subgraph C1[Capa 1: Cliente]
        M[App movil AppSheet - cache offline]
        W[Portal web CCO - supervisores y admin]
    end
    subgraph C2[Capa 2: Logica en la nube]
        E[AppSheet Cloud Engine]
        S[SSO Microsoft 365 / Google]
        F[Security Filter por SedeID]
        G[Geofencing DISTANCE menor o igual a 1.0 km]
        B[Bot de correo con informe PDF]
    end
    subgraph C3[Capa 3: Datos]
        GS[Google Sheets - 24 tablas de produccion]
        X[Excel maestro As-Built - BD/Modelo de Datos 2.xlsx]
        OD[Almacenamiento de evidencias fotograficas]
    end
    M -->|sync offline| E
    W -->|https| E
    E --> S
    E --> F
    E --> G
    E --> B
    E -->|API| GS
    GS <-->|respaldo As-Built| X
    E -->|fotos 600px| OD
```

**Ciclo del técnico:** iniciar sesión y sincronizar, descargar las OT de su sede, seleccionar la
OT o escanear el QR del activo, abrir el checklist que corresponde al tipo, responder, adjuntar
fotografías, firmar, cerrar validando la posición GPS. Si no hay red, todo queda en cola local y
sube solo al recuperar señal.

**Ciclo del supervisor:** programar la OT en el portal, asignarla a un técnico (el bot le avisa
por correo), revisar la evidencia sincronizada y aprobar, con el tablero de indicadores al lado.

## 5. Modelo de datos

Fuente de verdad: **`BD/Modelo de Datos (2).xlsx`**, 24 hojas. `entregables/Modelo_Datos_SGMC_AsBuilt.xlsx`
es una copia idéntica publicada, para enviar; no se edita. Diccionario completo en [bd.md](docs/bd.md).

```mermaid
erDiagram
    SED_Sedes ||--o{ USR_Usuarios : "asigna sede"
    ROL_Roles ||--o{ USR_Usuarios : "define permisos"
    SED_Sedes ||--o{ ACT_Activos : "ubica"
    TIP_TiposActivo ||--o{ ACT_Activos : "clasifica"
    TIP_TiposActivo ||--o{ FRM_Formularios : "determina checklist"
    EST_Activo ||--o{ ACT_Activos : "estado"
    FRE_Frecuencias ||--o{ ACT_Activos : "periodicidad"
    CAL_Calzadas ||--o{ ACT_Activos : "calzada"
    SEN_Sentidos ||--o{ ACT_Activos : "sentido"

    ACT_Activos ||--o{ OT_OrdenesTrabajo : "objeto de la orden"
    USR_Usuarios ||--o{ OT_OrdenesTrabajo : "tecnico asignado"
    OT_OrdenesTrabajo ||--o{ MAN_Mantenimientos : "ejecucion"
    OT_OrdenesTrabajo ||--o{ CHK_Checklists : "inspeccion"

    MAN_Mantenimientos ||--o{ FOT_Fotografias : "evidencia fotografica"
    MAN_Mantenimientos ||--o{ FIR_Firmas : "firmas"
    MAN_Mantenimientos ||--o{ GPS : "traza de posicion"
    CHK_Checklists ||--o{ CHD_ChecklistDetalle : "respuesta por item"

    FRM_Formularios ||--o{ FRM_Preguntas : "banco de preguntas"
    FRM_Secciones ||--o{ FRM_Preguntas : "agrupa"
    TPR_TiposRespuesta ||--o{ FRM_Preguntas : "tipo de respuesta"
    FRM_Preguntas ||--o{ LST_ValoresLista : "opciones de lista"
```

### Las 24 tablas

| Grupo | Tablas | Función |
|---|---|---|
| **Catálogos (9)** | `USR_Usuarios`, `ROL_Roles`, `SED_Sedes`, `TIP_TiposActivo`, `EST_Activo`, `FRE_Frecuencias`, `CAL_Calzadas`, `SEN_Sentidos`, `FRM_Formularios` | Usuarios y roles RBAC, sedes, taxonomía de activos y catálogos viales |
| **Maestras (3)** | `ACT_Activos`, `CHK_Checklists`, `CHD_ChecklistDetalle` | Inventario de activos con PR, QR y `Ubicacion` (LatLong); inspecciones ejecutadas y su detalle |
| **Transaccionales (5)** | `OT_OrdenesTrabajo`, `MAN_Mantenimientos`, `FOT_Fotografias`, `FIR_Firmas`, `GPS` | Orden programada, ejecución con `Coordenadas_Cierre` y `Precision_GPS`, y evidencias |
| **Motor de formularios (7)** | `FRM_Preguntas`, `FRM_Secciones`, `TPR_TiposRespuesta`, `LST_ValoresLista`, `FRM_SOS`, `FRM_CCTV`, `FRM_PMVF` | Checklists dinámicos por tipo de activo |

### Regla de geofencing

`ACT_Activos` guarda un único campo `Ubicacion` de tipo LatLong. No hay columnas `Latitud` y
`Longitud` separadas. La expresión válida contra el modelo objetivo, con el radio tomado del tipo
de activo porque una subestación y un poste SOS no admiten la misma tolerancia:

```
DISTANCE([Coordenadas_Cierre], [OTID].[ActivoID].[Ubicacion]) <= [OTID].[ActivoID].[TipoActivoID].[RadioGeofencingKm]
```

**No es aplicable todavía.** La ruta atraviesa dos referencias que hoy son texto. El procedimiento
para cablearlas está en [ESPEC-002](docs/sdd/ESPEC-002-cableado-en-appsheet.md), con sus pruebas de
aceptación en [PRUEBA-002](docs/sdd/PRUEBA-002-cableado-en-appsheet.md).

## 6. Estado real (verificado)

Verificado el 6 de agosto de 2026 leyendo el Excel maestro directamente en disco.

**Construido y funcionando**
- Modelo de 24 tablas, con `Coordenadas_Cierre` y `Precision_GPS` en `MAN_Mantenimientos`
- Catálogos poblados: 34 activos, 18 tipos, 10 sedes, 4 roles, 11 usuarios. El campo `CodigoQR`
  está lleno, pero repite el `CodigoActivo`: no hay etiqueta física detrás (B-10)
- 6 órdenes de trabajo registradas y 1 checklist de inspección SOS con su detalle
- Banco de preguntas del formulario de postes SOS (15 preguntas)
- App AppSheet publicada, con vistas móviles y web

**Divergencia entre los dos modelos**

El Excel local y el Google Sheets de producción no coinciden. Ninguno es superconjunto del otro.
Lo que corre la app es el Sheets.

| Tabla | Excel local | Producción |
|---|---|---|
| `TIP_TiposActivo.FormularioID` | Vacío en los 18 tipos | Poblado en los 18 |
| `MAN_Mantenimientos` | 24 columnas | 27 columnas. Las de GPS se agregaron el 6 de agosto de 2026 |
| `CHK_Checklists` | 9 columnas | 21 columnas |
| `CHD_ChecklistDetalle` | Pregunta en texto libre | Relacional, con `PreguntaID` |

**Abierto y bloqueante** (verificado en producción)

| # | Hallazgo |
|---|---|
| B-01 | Los 34 activos comparten una sola coordenada, situada en Bogotá y no en el corredor. El geofencing es inoperante hasta levantar las coordenadas reales |
| B-02 | La cadena relacional del modelo **no existe en la aplicación**: `OTID` es texto y no referencia. Sin eso no hay geofencing, ni navegación padre-hijo, ni reportes por activo. Corrección especificada y probada en [ESPEC-002](docs/sdd/ESPEC-002-cableado-en-appsheet.md); pendiente de ejecutar |
| B-03 | Todos los usuarios están en la sede 1 y todos los activos en las sedes 7 a 10. El Security Filter dejaría a cada técnico sin activos |
| B-04 | Solo 1 de 18 formularios tiene banco de preguntas |
| B-09 | La fórmula de geofencing documentada durante meses, con `[ActivoID].[Ubicacion]`, no funciona: esa columna no existe en `MAN_Mantenimientos` |
| B-10 | **El código QR no existe como objeto físico.** `ACT_Activos.CodigoQR` está poblado en los 34 activos, pero su valor es una copia literal de `CodigoActivo` (`SOS-001`, `CCTV-001`). Nada genera, imprime ni asigna una etiqueta, y AppSheet lee códigos pero no los produce. **Fuera de alcance por decisión del 7 de agosto de 2026:** el activo se abre por lista. La propuesta enviada a Dirección lo marca «Incluido», discrepancia abierta |
| B-05 | La entrega del backend de Valentín a la Concesión está pendiente de fecha |
| B-06 | Fotografías, firmas y GPS están modelados dos veces: campos en `MAN_Mantenimientos` y tablas hijas vacías |
| B-07 | `MAN_Mantenimientos` está vacía: ningún mantenimiento se ha ejecutado nunca de extremo a extremo |
| B-08 | Datos de prueba sin limpiar en `CHK_Checklists`: un registro trae el nombre del técnico en lugar de su identificador y `NOW()` como texto literal |

Detalle, evidencia y plan de remediación en [AUDITORIA_PLAN_Y_ROADMAP.md](docs/AUDITORIA_PLAN_Y_ROADMAP.md).

## 7. Por qué el proyecto vuelve a la definición funcional

El SGMC nació como un MVP de 8 días sobre una ERS v1.0 y un formulario de levantamiento
diligenciado el 25 de julio de 2026 (ver `legacy/Plan_Implementacion_SGMC_AppSheet.docx`). Desde
entonces mutó: el modelo pasó de 17 a 24 tablas, aparecieron dos arquitecturas de formularios en
paralelo y las evidencias quedaron modeladas por duplicado.

Esa mutación ocurrió sin una validación funcional intermedia. Varios bloqueantes de la lista
anterior no son errores de implementación sino **decisiones de negocio que nadie tomó**: qué
gobierna la sede de un activo, cuántas fotos exige realmente una inspección, qué reportes debe
entregar el sistema.

Por eso el paso siguiente no es configurar sino definir. El documento
[DEFINICION_FUNCIONAL_MESA_DE_TRABAJO.md](docs/DEFINICION_FUNCIONAL_MESA_DE_TRABAJO.md) presenta los
flujos funcionales por actor y las decisiones pendientes al líder funcional. Sus respuestas
producen el roadmap de implementación.

## 8. Organización del repositorio

```
BD/            Fuente de verdad: Modelo de Datos (2).xlsx, 24 hojas
docs/          Documentación técnica y funcional
docs/images/   Figuras de los documentos
docs/prompts/  Directivas para agentes de auditoría
Manuales/      Manuales de usuario y sus imágenes
entregables/   Documentos Word y Excel listos para enviar al cliente
scripts/       Generadores de figuras y documentos
.claude/skills/ Skills: auditar-modelo, generar-entregables, revisar-arquitectura
               y cablear-referencias
.claude/agents/ Agentes del pipeline SDD: especificador, verificador, arquitecto,
               ejecutor y probador
docs/sdd/      Artefactos del pipeline: ESPEC, PRUEBA, ORDEN y ACTA
archivo/       Material de origen, no versionado
```

| Documento | Para qué sirve |
|---|---|
| [ARQUITECTURA_OBJETIVO_SGMC.md](docs/ARQUITECTURA_OBJETIVO_SGMC.md) | **Frente activo.** Modelo objetivo: 27 tablas, 192 columnas, 38 referencias, 13 reglas. Generado desde `scripts/modelo_objetivo.py` y validado automáticamente |
| [historico/](docs/historico/) | **Documentos retirados el 2026-08-07.** Describen estados superados; seguirlos induce a deshacer trabajo correcto. No usar como fuente |
| [BASE_CONOCIMIENTO_APPSHEET.md](docs/BASE_CONOCIMIENTO_APPSHEET.md) | **Base de conocimiento propia.** Cómo se comporta AppSheet, con cita textual y URL oficial, y qué regla del SGMC sostiene cada una |
| [SDD_PIPELINE_SGMC.md](docs/SDD_PIPELINE_SGMC.md) | **Método vigente.** Cómo se construye cualquier cambio: especificado y probado antes de tocar producción. Los cinco agentes, las dos fases y el gate |
| [sdd/ESPEC-001-preparacion-del-sheets.md](docs/sdd/ESPEC-001-preparacion-del-sheets.md) | **Frente activo.** Fase A del cableado, verificada contra producción |
| [scripts/faseA_sheets.gs](scripts/faseA_sheets.gs) | La Fase A como Apps Script. La cuenta de Google bloqueó su ejecución |
| [sdd/ESPEC-001B-cierre-de-la-fase-a.md](docs/sdd/ESPEC-001B-cierre-de-la-fase-a.md) | Los 23 fallos que faltaban para cerrar la Fase A. Aplicados |
| [sdd/ACTA-001-cierre-de-la-fase-a.md](docs/sdd/ACTA-001-cierre-de-la-fase-a.md) | Acta de cierre de la Fase A, con la verificación y las lecciones de método |
| [sdd/ESPEC-001C-baja-de-activos-y-datos-de-prueba.md](docs/sdd/ESPEC-001C-baja-de-activos-y-datos-de-prueba.md) | Baja de activos, huérfanos y poblado de prueba. Aplicado y verificado |
| [sdd/ACTA-002-cierre-definitivo-de-la-fase-a.md](docs/sdd/ACTA-002-cierre-definitivo-de-la-fase-a.md) | Cierre definitivo de la Fase A, con la integridad referencial comprobada relación por relación |
| [prompts/PROMPT_AGENTE_HOJA_ESPEC_001C.md](docs/prompts/PROMPT_AGENTE_HOJA_ESPEC_001C.md) | Prompt autocontenido para el agente que aplica los cambios sobre la hoja |
| [prompts/PROMPT_AGENTE_HOJA_PAR_PARAMETROS.md](docs/prompts/PROMPT_AGENTE_HOJA_PAR_PARAMETROS.md) | **Frente activo.** Crear la pestaña de parámetros calibrables por el administrador |
| [sdd/ESPEC-002-cableado-en-appsheet.md](docs/sdd/ESPEC-002-cableado-en-appsheet.md) | **Frente activo.** Fase B: el cableado en AppSheet, paso a paso |
| [scripts/verificar_faseA.py](scripts/verificar_faseA.py) | Verifica un `.xlsx` exportado contra el modelo objetivo, encabezado por encabezado. No cierra nada por reporte |
| [ALCANCE_Y_SUPUESTOS_SGMC.md](docs/ALCANCE_Y_SUPUESTOS_SGMC.md) | Alcance del sistema completo y los 14 supuestos adoptados |
| [prompts/PROMPT_CONSTRUCCION_SGMC.md](docs/prompts/PROMPT_CONSTRUCCION_SGMC.md) | Directiva de construcción en 7 pasos con criterios de aceptación |
| [DEFINICION_FUNCIONAL_MESA_DE_TRABAJO.md](docs/DEFINICION_FUNCIONAL_MESA_DE_TRABAJO.md) | Flujos funcionales por actor y las 14 decisiones, ya enviadas al funcional |
| [AUDITORIA_PLAN_Y_ROADMAP.md](docs/AUDITORIA_PLAN_Y_ROADMAP.md) | Dictamen vigente: hallazgos, evidencia y Fase 0 corregida |
| [bd.md](docs/bd.md) | Diccionario de datos de las 24 tablas |
| [especificaciones.md](docs/especificaciones.md) | Requerimientos funcionales RF-001 a RF-016 |
| [especificaciones_visuales.md](docs/especificaciones_visuales.md) | Pantallas, vistas y elementos de interfaz |
| [plan_de_trabajo.md](docs/plan_de_trabajo.md) | Plan operativo, supeditado a la mesa de trabajo |
| [ROADMAP.md](docs/ROADMAP.md) | Fases y criterios de cierre |
| [GUIA_SVG_BOTONES_DINAMICOS_APPSHEET.md](docs/GUIA_SVG_BOTONES_DINAMICOS_APPSHEET.md) | Diseño de botones e iconos dinámicos en AppSheet |
| [MAP.md](MAP.md) | Índice maestro y referencias cruzadas |
| [CLAUDE.md](CLAUDE.md) | Reglas de trabajo para agentes sobre este repositorio |
| [Manuales/](Manuales/) | Manual de usuario, versión ilustrada y documento Word |
| [entregables/](entregables/) | Mesa de trabajo, especificaciones técnicas y modelo de datos publicado |

**Entregables al cliente**

| Archivo | Estado |
|---|---|
| `entregables/Propuesta_Arquitectura_SGMC.docx` | **Enviado a Dirección y al funcional.** Qué se va a construir, validado desde 6 roles, con 3 decisiones que pide |
| `entregables/Definicion_Funcional_SGMC_Mesa_de_Trabajo.docx` | Enviado. 14 decisiones con propuesta marcada |
| `entregables/CORREO_ENVIO_MESA_DE_TRABAJO.md` | Texto del correo de envío, listo para copiar |
| `entregables/Especificaciones_Tecnicas_SGMC_AsBuilt.docx` | v2.0. Qué hace, qué ofrece y cómo funciona, con el modelo real de 24 tablas y el estado verificado de los 16 requerimientos |
| `entregables/Modelo_Datos_SGMC_AsBuilt.xlsx` | Copia publicada del maestro. No editar: se edita `BD/` y se replica |
| `Manuales/Manual_de_Usuario_SGMC_Con_Diagramas.docx` | No es entregable ahora: el manual sirve cuando la app esté lista para usarse. Además sus imágenes tienen las tildes corruptas |

## 9. Enlaces

- Aplicación AppSheet: `SGMC-886843353` — [abrir](https://www.appsheet.com/start/060b99df-2037-4049-b94d-03c1eefc3219?platform=desktop#appName=SGMC-886843353&view=Usuarios)
- Backend Google Sheets: [abrir](https://docs.google.com/spreadsheets/d/1a4MmZ0u9sNgWmyiR2OPJo9YuUEKJFftbJWMW-KbITRc/edit)
- Repositorio: [github.com/dieleoz/SGMC](https://github.com/dieleoz/SGMC)

---
Concesión Transversal del Sisga S.A.S. | Agosto de 2026
