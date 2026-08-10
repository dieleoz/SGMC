# MAP.md — Índice maestro del proyecto

**Proyecto:** Sistema de Gestión de Mantenimiento en Campo (SGMC)
**Cliente:** Concesión Transversal del Sisga S.A.S.
**Actualizado:** 9 de agosto de 2026
**Propósito:** Mapa de navegación del repositorio. Dónde está cada cosa y qué contiene.

> **Este archivo dice dónde está cada cosa, no en qué punto va el proyecto.**
> Para el estado, [`ESTADO.md`](ESTADO.md).

---

## 1. Por dónde empezar

| Si necesitas | Abre |
|---|---|
| Saber en qué punto va el proyecto y qué falta | [ESTADO.md](ESTADO.md) |
| Entender qué es el proyecto | [README.md](README.md) |
| Saber qué te toca a ti, según tu rol | [docs/INDICACIONES_POR_ROL.md](docs/INDICACIONES_POR_ROL.md) |
| Entender qué hace el sistema y para quién | [docs/FUNCIONAL_SGMC.md](docs/FUNCIONAL_SGMC.md) |
| Ver la arquitectura que se va a construir | [docs/ARQUITECTURA_OBJETIVO_SGMC.md](docs/ARQUITECTURA_OBJETIVO_SGMC.md) |
| Construir o configurar la aplicación | [docs/MANUAL_DESPLIEGUE.md](docs/MANUAL_DESPLIEGUE.md) |
| Terminar lo que falta hoy en el editor | [docs/prompts/PROMPT_CONTINUAR_DESPLIEGUE.md](docs/prompts/PROMPT_CONTINUAR_DESPLIEGUE.md) |
| Saber qué expresión va en cada sitio | [docs/sdd/RECONSTRUCCION_EXPRESIONES.md](docs/sdd/RECONSTRUCCION_EXPRESIONES.md) |
| Probar que el despliegue funciona | [docs/sdd/PRUEBA-003-despliegue.md](docs/sdd/PRUEBA-003-despliegue.md) |
| Saber cómo se comporta AppSheet, con la cita oficial | [docs/BASE_CONOCIMIENTO_APPSHEET.md](docs/BASE_CONOCIMIENTO_APPSHEET.md) |
| Consultar la estructura de datos real | [docs/bd.md](docs/bd.md), generado del `.xlsx` |
| Saber con qué supuestos se construye | [docs/ALCANCE_Y_SUPUESTOS_SGMC.md](docs/ALCANCE_Y_SUPUESTOS_SGMC.md) |
| Saber hasta dónde aguanta el sistema | `python scripts/capacidad.py` |
| Trabajar sobre el repositorio como agente | [CLAUDE.md](CLAUDE.md) y las skills de `.claude/skills/` |

---

## 2. Estructura de carpetas

```
D:\@Proyect\Sisga\
├── ESTADO.md                     Dónde vamos y qué falta. Se lee primero
├── README.md                     Entrada del proyecto: qué es y cómo funciona
├── CLAUDE.md                     Reglas de trabajo para agentes
├── MAP.md                        Este archivo
│
├── BD/                           Hojas de datos
│   ├── Modelo_Datos_PLANTILLA.xlsx     Generada del modelo. Es el entregable de datos
│   ├── Modelo_Datos_09082026.xlsx      Descarga del Sheets de producción, 32 pestañas
│                                       0 ocultas, como Drive. De aquí sale bd.md
│   ├── Modelo_Datos_LIMPIO.xlsx        Paso intermedio de la migración
│   ├── ACT_Activos_355_SINTETICO.xlsx  Los 355 activos sintéticos del corredor
│   └── historico/                      Descargas anteriores. No usar como fuente
│
├── docs/                         Documentación técnica y funcional
│   ├── historico/                 Documentos retirados. No usar como fuente
│   ├── sdd/                       Artefactos del pipeline: ESPEC, PRUEBA y ACTA
│   ├── prompts/                   Directivas para agentes
│   └── images/                    fig_01 a fig_07, figuras de los documentos
│
├── Manuales/                     Manual de usuario
│   └── MANUAL_DE_USUARIO.md
│
├── entregables/                  Listos para enviar al cliente
│
├── scripts/                      Fuente del modelo, validadores y generadores
│   ├── modelo_objetivo.py         FUENTE ÚNICA. De aquí sale todo lo demás
│   ├── validar_modelo.py          Gate objetivo del pipeline
│   ├── verificar_faseA.py         El modelo contra la hoja descargada
│   ├── verificar_documentos.py    La prosa contra el modelo
│   ├── verificar_enlaces.py       Que todo enlace relativo entre documentos resuelve
│   └── generar_*.py               Generadores de documentos y de la plantilla
│
├── contexto/                     Material de contexto operativo. No es la vara
└── archivo/                      Material de origen. No versionado
```

---

## 3. Índice de documentos

### Estado y método

| Documento | Contenido | Vigencia |
|---|---|---|
| [ESTADO.md](ESTADO.md) | Qué está hecho, qué falta, qué está bloqueado y por quién | **Vigente. Es la verdad del estado** |
| [docs/SDD_PIPELINE_SGMC.md](docs/SDD_PIPELINE_SGMC.md) | Método de construcción: cinco agentes, dos fases y el gate antes del paso caro | **Vigente. Es el método** |
| [docs/INDICACIONES_POR_ROL.md](docs/INDICACIONES_POR_ROL.md) | El reparto por rol: qué hacer, qué decidir, qué leer y cuánto cuesta | Vigente |
| [docs/ALCANCE_Y_SUPUESTOS_SGMC.md](docs/ALCANCE_Y_SUPUESTOS_SGMC.md) | Alcance del sistema y los 14 supuestos adoptados, vinculantes hasta que el campo los desmienta | Vigente |
| [docs/ROADMAP.md](docs/ROADMAP.md) | Fases con criterio de cierre verificable | Vigente |

### Definición funcional y de dominio

| Documento | Contenido | Vigencia |
|---|---|---|
| [docs/FUNCIONAL_SGMC.md](docs/FUNCIONAL_SGMC.md) | Qué hace el sistema, para quién, cómo y para qué. Su §6 es el registro de una sola forma por propósito | **Vigente. Es la fuente funcional** |
| [docs/CONTEXTO_OPERACION.md](docs/CONTEXTO_OPERACION.md) | Cómo se mantiene el corredor de verdad, y la procedencia de cada documento de contexto | Vigente |
| [docs/GUIA_IMPLEMENTACION_FUNCIONAL.md](docs/GUIA_IMPLEMENTACION_FUNCIONAL.md) | La implementación vista desde la operación. Generada | Vigente |
| [docs/MODELO_EVOLUCION_FASE_2.md](docs/MODELO_EVOLUCION_FASE_2.md) | Lo que viene después del piloto | Propuesta |
| [docs/sdd/ESPEC-003-modelo-de-dominio.md](docs/sdd/ESPEC-003-modelo-de-dominio.md) | Capa de tareas, jerarquía de ubicación, oficios y correctivo | **Bloqueada.** 14 condiciones del arquitecto sin resolver |

### Modelo de datos y despliegue

| Documento | Contenido | Vigencia |
|---|---|---|
| [docs/ARQUITECTURA_OBJETIVO_SGMC.md](docs/ARQUITECTURA_OBJETIVO_SGMC.md) | Modelo objetivo, generado desde `scripts/modelo_objetivo.py` y validado | Vigente. **Se regenera, no se edita** |
| [docs/bd.md](docs/bd.md) | Diccionario As-Built: lo que la hoja tiene hoy, columna a columna | Vigente. **Se regenera, no se edita** |
| [docs/MANUAL_DESPLIEGUE.md](docs/MANUAL_DESPLIEGUE.md) | De cero a app desplegada, con la ficha de las 28 tablas columna por columna | Vigente. Generado |
| [docs/MIGRACION_HOJA_LIMPIA.md](docs/MIGRACION_HOJA_LIMPIA.md) | El procedimiento de migración a la hoja limpia, con su coste medido | Vigente. **Decisión cerrada el 2026-08-09: se migra.** Falta ejecutarla |
| [docs/sdd/RECONSTRUCCION_EXPRESIONES.md](docs/sdd/RECONSTRUCCION_EXPRESIONES.md) | Los nombres renombrados y las 20 reglas a reponer, sin cortar | Vigente |
| [docs/prompts/PROMPT_CONTINUAR_DESPLIEGUE.md](docs/prompts/PROMPT_CONTINUAR_DESPLIEGUE.md) | Las correcciones pendientes para el agente que está en el editor | Vigente |
| [docs/sdd/PRUEBA-003-despliegue.md](docs/sdd/PRUEBA-003-despliegue.md) | Las pruebas del despliegue | Vigente |
| [docs/sdd/ESPEC-002-cableado-en-appsheet.md](docs/sdd/ESPEC-002-cableado-en-appsheet.md) | El cableado de referencias, paso a paso | Aplicado sobre la app reconstruida. **Su lista de 15 columnas valía para la app anterior: son 38** |
| [docs/sdd/PRUEBA-002-cableado-en-appsheet.md](docs/sdd/PRUEBA-002-cableado-en-appsheet.md) | Las pruebas del cableado | **Vigente en 9 de sus 19.** Medía la app anterior; `PRUEBA-003` §1 dice cuál sobrevive |

### Plataforma

| Documento | Contenido | Vigencia |
|---|---|---|
| [docs/BASE_CONOCIMIENTO_APPSHEET.md](docs/BASE_CONOCIMIENTO_APPSHEET.md) | Cómo se comporta AppSheet, con cita textual y URL oficial. §11 y §12 explican por qué se reconstruyó | Vigente |
| [docs/COMUNICACION_PROPIETARIO_APP.md](docs/COMUNICACION_PROPIETARIO_APP.md) | Qué decirle al dueño de la aplicación anterior, con borrador del mensaje | Vigente |

### Actas del pipeline

Un acta registra un hecho fechado y no caduca. Siguen en `docs/sdd/` aunque su especificación
se haya retirado.

| Documento | Contenido |
|---|---|
| [docs/sdd/ACTA-001-cierre-de-la-fase-a.md](docs/sdd/ACTA-001-cierre-de-la-fase-a.md) | Cierre de la Fase A: qué se aplicó y qué quedó pendiente a propósito |
| [docs/sdd/ACTA-002-cierre-definitivo-de-la-fase-a.md](docs/sdd/ACTA-002-cierre-definitivo-de-la-fase-a.md) | Cierre de la Fase A y el incidente de método del verificador editado |
| [docs/sdd/ACTA-003-cierre-de-la-hoja.md](docs/sdd/ACTA-003-cierre-de-la-hoja.md) | Cierre de la hoja, y las dos alucinaciones que paró el verificador |
| [docs/sdd/ACTA-004-cierre-de-formatos.md](docs/sdd/ACTA-004-cierre-de-formatos.md) | Cierre de formatos, y el defecto de leer fórmulas en vez de valores |

### Manuales

| Documento | Contenido |
|---|---|
| [Manuales/MANUAL_DE_USUARIO.md](Manuales/MANUAL_DE_USUARIO.md) | Guía de operación por rol: técnico, supervisor, administrador. **No se entrega todavía**, y su cabecera dice por qué |

La versión ilustrada, el Word con diagramas y las seis maquetas **se retiraron a
[`docs/historico/`](docs/historico/) el 2026-08-09**: retratan el flujo antiguo con QR.

### Histórico

**Nada de [`docs/historico/`](docs/historico/) describe el sistema actual.** Se conserva porque
explica por qué se decidió lo que hay hoy. Su [README](docs/historico/README.md) lista qué hay y de
qué etapa es cada cosa. `verificar_documentos.py` no revisa esa carpeta.

---

## 4. Matriz de referencias cruzadas

| Concepto | Dónde está documentado | Dónde está el dato real |
|---|---|---|
| Estado del proyecto | [ESTADO.md](ESTADO.md) | — |
| Arquitectura de 3 capas | [README.md](README.md) sección 4 | Aplicación AppSheet `SISGA` |
| El modelo de 28 tablas | [docs/ARQUITECTURA_OBJETIVO_SGMC.md](docs/ARQUITECTURA_OBJETIVO_SGMC.md) | `scripts/modelo_objetivo.py` |
| Lo que la hoja tiene hoy | [docs/bd.md](docs/bd.md) | `python scripts/generar_diccionario_bd.py` |
| Regla de geofencing | [CLAUDE.md](CLAUDE.md) sección 6 | `MAN_Mantenimientos.Coordenadas_Cierre` en AppSheet |
| Radio por tipo de activo | [README.md](README.md) sección 5 | `TIP_TiposActivo.RadioGeofencingKm` en `BD/Modelo_Datos_PLANTILLA.xlsx` |
| Flujos por actor | [docs/FUNCIONAL_SGMC.md](docs/FUNCIONAL_SGMC.md) | — |
| Una sola forma por propósito | [docs/FUNCIONAL_SGMC.md](docs/FUNCIONAL_SGMC.md) §6 | `DECISIONES` en `scripts/modelo_objetivo.py` |
| Cableado de referencias | [docs/sdd/ESPEC-002-cableado-en-appsheet.md](docs/sdd/ESPEC-002-cableado-en-appsheet.md) | `python scripts/validar_modelo.py`, reglas V-14 a V-17 |
| Comportamiento de la plataforma | [docs/BASE_CONOCIMIENTO_APPSHEET.md](docs/BASE_CONOCIMIENTO_APPSHEET.md) | Cita textual y URL oficial por cada afirmación |
| Deriva documental | [CLAUDE.md](CLAUDE.md) sección 8 | `python scripts/verificar_documentos.py` |
| Capacidad y crecimiento | — | `python scripts/capacidad.py` |

---

## 5. Enlaces externos

- Aplicación AppSheet `SISGA`: se entra por el listado de [appsheet.com](https://www.appsheet.com). **El enlace directo con `appId=9e947fce-…` no resuelve** — ver [`ESTADO.md`](ESTADO.md)
- Backend Google Sheets `Modelo_Datos_09082026`: [abrir](https://docs.google.com/spreadsheets/d/1LGabjn1iNDKiJNP7CUD4_LwCH2BGXC8oTBfXmuuAkFs)
- Repositorio: [github.com/dieleoz/SGMC](https://github.com/dieleoz/SGMC)

---
*SGMC | Concesión Transversal del Sisga S.A.S.*
