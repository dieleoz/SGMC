# 📅 PLAN DE TRABAJO: AUDITORÍA PREVIA, SUBSANACIÓN Y PILOTO (SGMC)

**Proyecto:** Sistema de Gestión de Mantenimiento en Campo (SGMC)  
**Cliente:** Concesión Transversal del Sisga S.A.S.  
**Plataforma de Producción:** Google AppSheet + Google Sheets Backend  
**URL Google Sheets Producción:** [Backend Google Sheets SGMC](https://docs.google.com/spreadsheets/d/1a4MmZ0u9sNgWmyiR2OPJo9YuUEKJFftbJWMW-KbITRc/edit?gid=1353886072#gid=1353886072)  
**Base de Datos Maestra Local:** `d:\@Proyect\Sisga\BD\Modelo de Datos (2).xlsx` (24 Hojas)  
**Metodología de Ejecución:** **AUDITAR PRIMERO ➡️ SUBSANAR DESPUÉS ➡️ DESPLEGAR PILOTO**  
**Fecha:** Agosto de 2026 | **Versión:** 3.0 Audit-First Protocol  

---

## 🛑 1. Directiva de Ejecución para el Agente (Audit-First)

> **[!IMPORTANT] PROTOCOLO DE AUDITORÍA PREVIA BLOQUEANTE:**  
> El agente que reciba este plan **NO MODIFICARÁ NINGÚN ARCHIVO NI HOJA DE CÁLCULO DE INICIALMENTE**.  
> **Paso 1 Obligatorio:** El agente debe auditar la BD de producción en Google Sheets y el Excel local (`BD/Modelo de Datos (2).xlsx`), inspeccionar la presencia real de cada columna y emitir un **Dictamen de Diagnóstico**.  
> **Paso 2:** Solo si el dictamen identifica columnas faltantes, procederá a aplicar los ajustes de la **Fase 0.B**.

---

## 🗓️ 2. Cronograma de Trabajo Secuencial (Mermaid Gantt)

```mermaid
gantt
    title Plan de Trabajo SGMC: Auditoría Previa, Subsanación y Piloto
    dateFormat  YYYY-MM-DD
    section FASE 0.A: Auditoría Previa & Diagnóstico
    Audit-01: Inspección de Hojas y Columna Coordenadas_Cierre :crit, active, a1, 2026-08-07, 2026-08-08
    Audit-02: Diagnóstico de CHK_Checklists y CHD_ChecklistDetalle :crit, a2, 2026-08-08, 2026-08-08
    Audit-03: Verificación Rótulo FRM_Formularios & Catálogo OT   :a3, 2026-08-08, 2026-08-09
    section FASE 0.B: Ajuste de BD (Google Sheets / Excel)
    T-00.1: Adición física Coordenadas_Cierre y Precision_GPS     :f0_1, 2026-08-09, 2026-08-10
    T-00.2: Definir columnas relacionales CHK y CHD (21 cols)      :f0_2, 2026-08-10, 2026-08-10
    T-00.3: Unificar FRM_Formularios y Valid_If GPS en AppSheet    :f0_3, 2026-08-10, 2026-08-11
    section FASE 1: Despliegue Móvil & Piloto de Campo
    Instalación AppSheet en 10 Celulares & Login M365             :p1, 2026-08-12, 2026-08-14
    Pruebas Offline en Vía (Túneles, Fotos 600px, Firmas)         :p2, 2026-08-15, 2026-08-18
    Alertas CCO Email PDF & Salida a Producción                   :p3, 2026-08-19, 2026-08-25
```

---

## 📋 3. Matriz de Tareas Detallada por Fases

### 🔍 FASE 0.A — AUDITORÍA PREVIA Y DIAGNÓSTICO FÍSICO (LEER Y DIAGNOSTICAR)
- [ ] **Tarea AUDIT-01:** Abrir la base de datos de producción ([Google Sheets](https://docs.google.com/spreadsheets/d/1a4MmZ0u9sNgWmyiR2OPJo9YuUEKJFftbJWMW-KbITRc/edit?gid=1353886072#gid=1353886072)) y el archivo local `BD/Modelo de Datos (2).xlsx`. Contar las columnas de la hoja `MAN_Mantenimientos` y verificar si existen las columnas `Coordenadas_Cierre` y `Precision_GPS`.
- [ ] **Tarea AUDIT-02:** Inspeccionar las hojas `CHK_Checklists` y `CHD_ChecklistDetalle`. Verificar si poseen los encabezados de inspección relacionales o si son placeholders.
- [ ] **Tarea AUDIT-03:** Revisar la hoja índice `Tablas` y confirmar si rotula `FRM_Formularios` o `CAF_Formularios`.
- [ ] **Tarea AUDIT-04:** Generar un documento de **Dictamen de Diagnóstico Previo** indicando la lista exacta de vacíos encontrados antes de realizar cualquier edición.

---

### 🛠️ FASE 0.B — SUBSANACIÓN Y AJUSTE DE BASE DE DATOS (SOLO TRAS DIAGNÓSTICO)
- [ ] **Tarea T-00.1 [SUBSANACIÓN GPS]:** En la hoja `MAN_Mantenimientos` del Google Sheet de producción y del Excel local, agregar físicamente las columnas `Coordenadas_Cierre` (`LatLong`, `HERE()`) y `Precision_GPS` (`Decimal`, `USERLOCATIONACCURACY()`).
- [ ] **Tarea T-00.2 [SUBSANACIÓN CHECKLISTS]:** Asegurar los encabezados relacionales en `CHK_Checklists` (21 columnas) y `CHD_ChecklistDetalle` (21 columnas) para dar soporte a los 18 formularios dinámicos.
- [ ] **Tarea T-00.3 [NOMENCLATURA]:** Unificar la rotulación a `FRM_Formularios` en la hoja índice `Tablas`.
- [ ] **Tarea T-00.4 [REGLAS APPSHEET]:** En el editor web de AppSheet, configurar el campo `Valid_If` de `Coordenadas_Cierre`:  
  `DISTANCE([Coordenadas_Cierre], LATLONG([ActivoID].[Latitud], [ActivoID].[Longitud])) <= 1.0`  
  Y establecer el texto de error en español: *"⚠️ Ubicación fuera de rango: Debe estar a menos de 1.0 km del activo y tener el GPS activo"*.
- [ ] **Tarea T-00.5 [RE-AUDITORÍA]:** Re-ejecutar la prueba de verificación física y certificar que la BD de producción quedó 100% Conforme.

---

### 📱 FASE 1 — DESPLIEGUE MÓVIL Y PILOTO EN VÍA
- [ ] **Tarea T-01 / Q-01:** Instalar la app gratuita AppSheet en los 10 celulares del grupo piloto e iniciar sesión con cuentas M365 corporativas (`USEREMAIL()`).
- [ ] **Tarea T-02 / Q-02:** Confirmar que `Security Filter` restrinja el payload por `SedeID` (`Sutatenza`, `Peaje Machetá`, `Peaje SLG`).
- [ ] **Tarea Q-05:** Ejecutar prueba de mantenimiento en Modo Avión (sin señal celular) en túneles: registrar checklist, adjuntar 6 fotos comprimidas a 600px, capturar firma táctil y verificar sincronización al detectar red.
- [ ] **Tarea T-05 / S-03:** Probar el Automation Bot de correo electrónico con informe PDF adjunto cuando un activo se reporte como *Fuera de servicio*.

---

## 🎯 4. Hitos de Entrega

| Hito | Nombre del Hito | Criterio de Aceptación | Estado |
|---|---|---|---|
| **HITO-00.A** | Diagnóstico Previo Emitido | Informe emitido indicando el estado real de columnas antes de editar | 🔲 **Paso 1 (Auditoría)** |
| **HITO-00.B** | Subsanación de BD Certificada | Google Sheets y Excel actualizados con columnas GPS y Checklists | 🔲 **Paso 2 (Ajuste)** |
| **HITO-01** | Despliegue Móvil Piloto | 10 técnicos autenticados con SSO M365 y filtro por sede operativo | 🔲 Pendiente |
| **HITO-02** | Registro Offline en Túneles | Mantenimiento guardado offline sin red y sincronizado en segundo plano | 🔲 Pendiente |
| **HITO-03** | Alerta CCO PDF Operativa | Email con informe PDF recibido en CCO ante fallas de activos | 🔲 Pendiente |

---
*Plan de trabajo protocolo Audit-First listo para asignación.*  
*Referencias Cruzadas:* [README.md](./README.md) | [bd.md](./bd.md) | [MAP.md](./MAP.md) | [DICTAMEN_AUDITORIA_LOCAL_SGMC.md](./DICTAMEN_AUDITORIA_LOCAL_SGMC.md)
