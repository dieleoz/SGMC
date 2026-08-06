# 📅 PLAN DE TRABAJO Y HOJA DE RUTA OPERATIVA (SGMC)

**Proyecto:** Sistema de Gestión de Mantenimiento en Campo (SGMC)  
**Cliente:** Concesión Transversal del Sisga S.A.S.  
**Plataforma Cloud:** Google AppSheet + Google Sheets Backend (Producción)  
**URL Google Sheets Producción:** [Google Sheets Backend SGMC](https://docs.google.com/spreadsheets/d/1a4MmZ0u9sNgWmyiR2OPJo9YuUEKJFftbJWMW-KbITRc/edit?gid=1353886072#gid=1353886072)  
**Base de Datos Maestra Única:** `d:\@Proyect\Sisga\BD\Modelo de Datos (2).xlsx` (24 Hojas)  
**Metodología:** **AUDIT-FIRST (Auditar ➡️ Diagnosticar ➡️ Subsanar ➡️ Desplegar Piloto)**  
**Fecha:** Agosto de 2026 | **Versión:** 4.0 (Ajustado al Modelo de 24 Hojas)  

---

## 🛑 1. Directiva de Ejecución para el Agente (Audit-First)

> **[!IMPORTANT] PROTOCOLO DE AUDITORÍA PREVIA Y CONSOLIDACIÓN DE BACKEND:**  
> 1. **Única Fuente de Verdad:** La única base de datos oficial del sistema es el archivo de 24 hojas `BD/Modelo de Datos (2).xlsx` (replicado en Google Sheets). Se desconecta cualquier referencia a archivos viejos de 18 hojas.  
> 2. **Paso 1 Obligatorio (Sin editar nada):** El agente inspeccionará la BD de producción y verificará que las columnas `Coordenadas_Cierre` y `Precision_GPS` ya existen en `MAN_Mantenimientos`, y emite su dictamen.  
> 3. **Paso 2 (Ajustes de Fase 0):** Desduplicación de la columna `Observaciones` en `MAN_Mantenimientos` y configuración de la regla de Geofencing `DISTANCE([Coordenadas_Cierre], [ActivoID].[Ubicacion]) <= 1.0`.

---

## 🗓️ 2. Cronograma de Trabajo Secuencial (Mermaid Gantt)

```mermaid
gantt
    title Plan de Trabajo SGMC: Subsanación 24 Hojas, Piloto y Producción
    dateFormat  YYYY-MM-DD
    section FASE 0: Subsanación & Consolidación Backend
    Audit-01: Verificación de Modelo de 24 Hojas & GPS          :crit, active, a1, 2026-08-07, 2026-08-08
    T-00.1: Desduplicación de columna Observaciones en MAN      :crit, a2, 2026-08-08, 2026-08-08
    T-00.2: Configuración Geofencing DISTANCE(..., Ubicacion)   :a3, 2026-08-08, 2026-08-09
    T-00.3: Configuración Texto Error GPS Sin Emojis          :a4, 2026-08-09, 2026-08-09
    T-00.4: Confirmación Llave Primaria Numero_OT en OT       :a5, 2026-08-09, 2026-08-10
    section FASE 1: Despliegue Móvil & Piloto de Campo
    Instalación AppSheet en 10 Celulares & Login M365          :p1, 2026-08-11, 2026-08-13
    Pruebas Offline en Vía (Túneles, Fotos 600px, Firmas)      :p2, 2026-08-14, 2026-08-18
    Alertas CCO Email PDF & Salida a Producción                :p3, 2026-08-19, 2026-08-25
```

---

## 🛠️ 3. Matriz Detallada de Tareas por Fase

### 🔍 FASE 0 — SUBSANACIÓN Y CONSOLIDACIÓN DE BACKEND (BLOQUEANTE)
- [ ] **Tarea AUDIT-01:** Inspeccionar el archivo `BD/Modelo de Datos (2).xlsx` (24 Hojas) y confirmar que la hoja `MAN_Mantenimientos` contiene físicamente `Coordenadas_Cierre` y `Precision_GPS`.
- [ ] **Tarea T-00.1 [DESDUPLICACIÓN]:** Verificar que la columna `Observaciones` en `MAN_Mantenimientos` no se encuentre duplicada (24 columnas únicas).
- [ ] **Tarea T-00.2 [GEOFENCING GPS]:** Configurar en AppSheet la fórmula de Geofencing evaluando la columna `Ubicacion` de `ACT_Activos`:  
  `DISTANCE([Coordenadas_Cierre], [ActivoID].[Ubicacion]) <= 1.0`
- [ ] **Tarea T-00.3 [TEXTO DE ERROR]:** Establecer en AppSheet el mensaje de error de Geofencing en texto plano sin emojis:  
  `"Ubicación fuera de rango: debe estar a menos de 1.0 km del activo."`
- [ ] **Tarea T-00.4 [LLAVE OT]:** Confirmar en AppSheet que la llave primaria de `OT_OrdenesTrabajo` sea `Numero_OT` para que las referencias `Ref` de `MAN_Mantenimientos` y `CHK_Checklists` mapeen correctamente.
- [ ] **Tarea T-00.5 [EVIDENCIAS ISPART OF]:** Marcar `IsPartOf = TRUE` en `FOT_Fotografias` y `FIR_Firmas` para la captura de hasta 6 fotos comprimidas a 600px por mantenimiento.

---

### 📱 FASE 1 — DESPLIEGUE MÓVIL Y PILOTO EN VÍA
- [ ] **Tarea T-01 / Q-01:** Instalar la app gratuita AppSheet en los 10 móviles del grupo piloto e iniciar sesión con cuentas M365 corporativas (`USEREMAIL()`).
- [ ] **Tarea T-02 / Q-02:** Confirmar que `Security Filter` restrinja el payload por `SedeID` (`Sutatenza`, `Peaje Machetá`, `Peaje SLG`).
- [ ] **Tarea Q-05:** Ejecutar prueba de mantenimiento en Modo Avión (sin señal celular) en túneles: registrar checklist, adjuntar 6 fotos a 600px, capturar firma táctil y verificar sincronización al detectar red.
- [ ] **Tarea T-05 / S-03:** Probar el Automation Bot de correo electrónico con informe PDF adjunto cuando un activo se reporte como *Fuera de servicio*.

---
*Plan de trabajo actualizado para el modelo de 24 hojas.*  
*Referencias Cruzadas:* [README.md](../README.md) | [bd.md](../docs/bd.md) | [MAP.md](../MAP.md) | [especificaciones.md](../docs/especificaciones.md)
