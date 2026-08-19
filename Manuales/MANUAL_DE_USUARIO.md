# Manual Funcional y Guía de Operación por Rol — SGMC v2

**Sistema de Gestión de Mantenimiento en Campo**  
**Cliente:** Concesión Transversal del Sisga S.A.S. (137 km)  
**Versión:** 2.0 (PostgreSQL 16 + PostGIS + Next.js 14 PWA)  
**Acceso en Producción:** [https://sisga-2.vercel.app/](https://sisga-2.vercel.app/)  
**Fecha de Emisión:** Agosto 2026

---

## 1. Propósito y Alcance del SGMC v2

El **Sistema de Gestión de Mantenimiento en Campo (SGMC v2)** es la plataforma oficial de la Concesión Transversal del Sisga para la administración, planificación, ejecución técnica y certificación pericial del mantenimiento preventivo y correctivo sobre los **368 activos de infraestructura** distribuidos a lo largo de las cuatro Unidades Funcionales (`UF1` a `UF4`):

1. **UF1 — Sisga / Guateque (PK 00+000 al PK 49+000):** 146 activos (Postes SOS, Cámaras CCTV, Paneles PMV, Subestaciones).
2. **UF2 — Guateque / Macanal (PK 49+000 al PK 72+000):** 53 activos (Túneles, Estaciones de Peaje, Cámaras de Monitoreo).
3. **UF3 — Macanal / Santa María (PK 72+000 al PK 105+000):** 45 activos (Postes SOS, Radares de Velocidad, Luminarias).
4. **UF4 — Santa María / Aguaclara (PK 105+000 al PK 137+000):** 124 activos (Sistemas de Comunicación, Estaciones Meteorológicas).

El sistema garantiza **trazabilidad jurídica e inmutabilidad pericial** ante la **Agencia Nacional de Infraestructura (ANI)** y la **Interventoría**, mediante validación satelital fail-closed, almacenamiento de evidencias fotográficas WebP en S3, firma digital manuscrita y cálculo automatizado de la Disponibilidad Contractual ($D_i \ge 98.5\%$).

---

## 2. Matriz de Roles y Responsabilidades

| Rol | Perfil / Usuarios | Interfaz de Acceso | Responsabilidades Funcionales |
|:---:|---|:---:|---|
| **`ROL-03` Técnico de Campo** | Iván Salcedo / Luis Gacha | [`/tecnico`](https://sisga-2.vercel.app/tecnico) | • Ejecutar inspecciones en modo 100% offline.<br>• Responder checklists dinámicos por tipo de equipo.<br>• Tomar fotos WebP georreferenciadas y firma digital.<br>• Reportar novedades de vía (`/novedades`). |
| **`ROL-02` Supervisor de Zona** | Fernand Bolívar | [`/supervisor`](https://sisga-2.vercel.app/supervisor)<br>[`/planes`](https://sisga-2.vercel.app/planes) | • Auditar órdenes ejecutadas y coordenadas GPS.<br>• Aprobar o rechazar mantenimientos con observaciones.<br>• Generar Fichas Técnicas Periciales en PDF.<br>• Programar planes preventivos mensuales por UF. |
| **`ROL-01` Director Técnico / CCO** | Diego Zúñiga / Operadores CCO | [`/`](https://sisga-2.vercel.app/)<br>[`/activos`](https://sisga-2.vercel.app/activos) | • Monitorear el estado general del corredor (137 km).<br>• Administrar el catálogo de 368 activos.<br>• Supervisar la asignación de técnicos por zona (`ASG_AsignacionZona`). |
| **`ROL-04` Interventoría / ANI** | Consorcio Interventoría Sisga | [`/reportes`](https://sisga-2.vercel.app/reportes) | • Auditar la Disponibilidad Contractual ($D_i \ge 98.5\%$).<br>• Consultar el Parte Diario de Operaciones del CCO.<br>• Descargar el **Informe Oficial en PDF para la ANI**. |

---

## 3. Manual Funcional: Rol Técnico de Campo (`/tecnico`)

### 3.1. Instalación de la Aplicación en Celular o Tablet (PWA)
1. Abra el navegador Chrome (Android) o Safari (iOS) en su dispositivo móvil.
2. Ingrese a la URL: `https://sisga-2.vercel.app/tecnico`.
3. Presione el botón **"Instalar App"** en el banner superior (o en el menú del navegador: *Instalar aplicación* / *Agregar a pantalla de inicio*).
4. La aplicación se ejecutará a pantalla completa con rendimiento nativo y caché sin conexión.

### 3.2. Operación Offline en Túneles y Zonas de Montaña
* La PWA almacena automáticamente el censo de órdenes y formularios en la base de datos local (IndexedDB).
* Si pierde la señal celular (túneles o cañones de montaña), el indicador superior pasará a **"Modo Offline Activo (Túneles/Vía)"**.
* **Contador de Cola Outbox:** Si tiene mantenimientos pendientes por sincronizar, verá un badge ámbar (ej. `⚠️ 2 pendientes`).
* Al recuperar señal 4G o WiFi, el motor de sincronización subirá automáticamente los registros sin que deba reingresar información.

### 3.3. Ciclo de Ejecución de una Orden de Trabajo:
1. **Selección:** En la lista de órdenes asignadas, seleccione el equipo a intervenir (ej. *Poste SOS PK 14+200*).
2. **Validación Satelital (GPS):**
   * Presione **"Capturar Coordenadas GPS"**.
   * Si está dentro de la tolerancia del activo (ej. 50 metros), el sistema mostrará: `¡Validación Conforme!`.
   * **Cierre con Excepción (Túneles):** Si se encuentra en un túnel o recinto cerrado sin señal satelital, active la casilla **"Activar Cierre con Excepción Manual"** y seleccione el motivo (ej. *Túnel o zona sin cobertura satelital GPS*). El sistema no inventará coordenadas ficticias.
3. **Diligenciamiento de Checklist Dinámico:**
   * Responda las preguntas agrupadas por secciones según el tipo de activo (Conforme/No conforme, valores de lista, mediciones de voltaje en voltios, etc.).
4. **Captura Fotográfica WebP:**
   * Tome las fotografías de evidencia requeridas. La cámara estampará las coordenadas y la hora en el pie de foto, comprimiéndola a formato ligero WebP (<150 KB).
5. **Firma Digital Manuscrita:**
   * Dibuje su firma en el recuadro táctil del celular.
6. **Guardar Mantenimiento:**
   * Presione **"Guardar y Cerrar Mantenimiento"**. El botón se bloqueará contra doble clic y asentará la orden para revisión de supervisión.

### 3.4. Reporte de Novedades en Ruta (`/novedades`)
Si durante el recorrido en carretera detecta una falla imprevista o un daño por terceros:
1. Presione el botón **"Reportar Novedad en Ruta"** en la cabecera.
2. Ingrese la descripción del daño, adjunte la fotografía de evidencia y tome la ubicación GPS.
3. Al enviar, el sistema genera automáticamente una **Orden de Trabajo Correctiva (`OT-CORR`)** en Supabase para su atención inmediata.

---

## 4. Manual Funcional: Rol Supervisor de Mantenimiento (`/supervisor` y `/planes`)

### 4.1. Bandeja de Supervisión y Auditoría Pericial
1. Ingrese a `https://sisga-2.vercel.app/supervisor`.
2. Filtre las órdenes por Unidad Funcional (`UF1` a `UF4`), Estado (`En revision` o `Cerrada`) o técnico asignado.
3. Presione **"Auditar Evidencias"** sobre la orden a certificar.

### 4.2. Modal de Auditoría Pericial
* **Auditoría GPS:** Contraste en el mapa la ubicación reportada por el técnico vs el punto kilométrico (PK) oficial del activo.
* **Inspección de Evidencias:** Revise las fotos WebP almacenadas en Supabase Storage y verifique la firma digital manuscrita.
* **Aprobación / Rechazo:**
  * **Aprobar:** Presione **"Aprobar y Certificar"**. La orden pasa a estado `Cerrada`.
  * **Rechazar:** Presione **"Rechazar / Solicitar Corrección"**, indicando el motivo para que el técnico reejecute la labor.
* **Descarga de Ficha PDF:** Presione **"📄 Descargar Ficha PDF (Interventoría)"** para emitir el documento individual pericial con membrete oficial.

### 4.3. Programación Masiva en el Generador de Planes (`/planes`)
1. Ingrese a `https://sisga-2.vercel.app/planes`.
2. Seleccione el mes de ejecución (ej. *Septiembre 2026*) y la Unidad Funcional (o *Todas las UFs*).
3. Presione **"Generar OTs del Mes"**.
4. El sistema ejecuta el procedimiento RPC `sgmc_generar_plan_mensual`, programa los 368 activos en `PLA_PlanMantenimiento` y genera las órdenes en `OT_OrdenesTrabajo` para cada técnico de zona.

---

## 5. Manual Funcional: Rol Director Técnico y CCO (`/` y `/activos`)

### 5.1. Cuadro de Mando del Corredor Vial (`/`)
* Monitoreo en tiempo real del porcentaje de avance preventivo y correctivo en los 137 km de vía.
* Visualización rápida del estado de las cuadrillas técnicas y volumen de órdenes activas.

### 5.2. Catálogo Maestro de Activos (`/activos`)
* Búsqueda y filtrado del censo completo de **368 activos** por código (`ACT-0001`), PK (`PK 14+200`), Unidad Funcional y tipo de equipo.
* Inspección de coordenadas geográficas, radio de tolerancia y formulario asignado.

---

## 6. Manual Funcional: Rol Interventoría y Auditoría ANI (`/reportes`)

### 6.1. Tablero de Disponibilidad Contractual ($D_i$)
1. Ingrese a `https://sisga-2.vercel.app/reportes`.
2. Seleccione el mes y año a auditar.
3. El sistema calcula en vivo la fórmula contractual del Apéndice Técnico 1 de la ANI:
   $$D_i = \left[ 1 - \left( \frac{\text{Horas Indisponibles Totales}}{\text{Horas Programadas Totales}} \right) \right] \times 100\%$$
4. **Semáforo de Conformidad ANI:**
   * $\ge 98.5\% \longrightarrow$ 🟢 **CONFORME** (Cumplimiento de indicadores contractuales).
   * $< 98.5\% \longrightarrow$ 🔴 **NO CONFORME** (Afecta retribución mensual).

### 6.2. Parte Diario de Operaciones del CCO
* Muestra el balance diario de órdenes programadas, mantenimientos ejecutados, cierres con excepción satelital y novedades atendidas.

### 6.3. 📄 Emisión del Informe Oficial en PDF para Radicación ante la ANI
1. En la vista `/reportes`, presione el botón verde **"Descargar Informe PDF (ANI)"**.
2. El sistema compila automáticamente:
   * Membrete institucional de la Concesión Transversal del Sisga.
   * Código de documento `INF-DISP-YYYYMM` y versión PostGIS.
   * Matriz detallada de los 27 subsistemas y 4 Unidades Funcionales.
   * Resumen de operaciones del CCO.
   * Bloques oficiales de firma para el **Director Técnico de la Concesión** y el **Ingeniero Residente de Interventoría**.
3. Se abre el diálogo de impresión / guardado en PDF listo para radicación contractual.

---

## 7. Diccionario de Códigos y Módulos del Sistema

| Módulo | Ruta URL | Roles Autorizados | Función Principal |
|---|---|---|---|
| **Centro de Control** | `/` | Todos | Resumen general del corredor (137 km). |
| **App Técnico** | `/tecnico` | Técnico de Campo | Ejecución offline, checklists, fotos WebP, firmas. |
| **Bandeja Supervisión** | `/supervisor` | Supervisor / Interventoría | Auditoría pericial, aprobación y fichas técnicas PDF. |
| **Novedades de Ruta** | `/novedades` | Técnico / Supervisor | Reporte de imprevistos y OTs correctivas automáticas. |
| **Planes Preventivos** | `/planes` | Supervisor / CCO | Generación masiva mensual de OTs preventivas por UF. |
| **Disponibilidad ($D_i$)** | `/reportes` | Interventoría / Dirección | Cálculo de $D_i \ge 98.5\%$, Parte Diario e informe PDF ANI. |
| **Inventario de Activos** | `/activos` | Todos | Consulta del censo georreferenciado de 368 activos. |

---
**Concesión Transversal del Sisga S.A.S.** — Sistema de Gestión de Mantenimiento en Campo (SGMC v2)
