# 🤖 PROMPT Y DIRECTIVA DE INSTRUCCIÓN PARA EL AGENTE DE AUDITORÍA Y SUBSANACIÓN

> **DOCUMENTO SUPERADO — 6 de agosto de 2026.** Su Paso 2 ordena configurar sobre un modelo cuyas referencias no están cableadas.
> Vigentes: [ALCANCE_Y_SUPUESTOS_SGMC.md](../ALCANCE_Y_SUPUESTOS_SGMC.md) y [PROMPT_CONSTRUCCION_SGMC.md](PROMPT_CONSTRUCCION_SGMC.md).

**Copie y pegue el siguiente bloque de texto en la consola de cualquier Agente IA para ejecutar el plan corregido:**

```text
PROMPT PARA EL AGENTE DE INGENIERÍA Y AUDITORÍA DE SOFTWARE:

Actúa como Auditor Principal de Arquitectura de Software y Desarrollador Senior de Google AppSheet para el proyecto SGMC de la Concesión Transversal del Sisga S.A.S.

Tu objetivo es ejecutar la Fase 0 de Subsanación y Consolidación con el modelo oficial de 24 Hojas.

SIGUE ESTAS INSTRUCCIONES EN ORDEN ESTRICTO:

PASO 1: AUDITORÍA PREVIA Y CONFIRMACIÓN DE LA BD MAESTRA (SIN EDITAR NADA INICIALMENTE)
1. Inspecciona la única fuente de verdad: d:\@Proyect\Sisga\BD\Modelo de Datos (2).xlsx (24 Hojas) y el backend de producción en Google Sheets:
   https://docs.google.com/spreadsheets/d/1a4MmZ0u9sNgWmyiR2OPJo9YuUEKJFftbJWMW-KbITRc/edit?gid=1353886072#gid=1353886072
2. Verifica que 'MAN_Mantenimientos' contiene las columnas 'Coordenadas_Cierre' y 'Precision_GPS'.
3. Confirma que la columna 'Observaciones' no esté duplicada en 'MAN_Mantenimientos' (24 columnas únicas).
4. Confirma que 'ACT_Activos' utiliza la columna 'Ubicacion' (LatLong) para las coordenadas.
5. Emite tu Dictamen de Diagnóstico Previo.

PASO 2: CONFIGURACIÓN EN APPSHEET
1. En el editor de AppSheet, configura la regla Valid_If de Geofencing GPS sobre 'MAN_Mantenimientos[Coordenadas_Cierre]':
   DISTANCE([Coordenadas_Cierre], [OTID].[Activo].[Ubicacion]) <= 1.0
2. Establece el texto de error en español sin símbolos decorativos:
   "Ubicación fuera de rango: debe estar a menos de 1.0 km del activo."
3. Marca IsPartOf = TRUE en las tablas de evidencias FOT_Fotografias y FIR_Firmas.
4. Establece calidad de imagen Low (600px) en FOT_Fotografias[Archivo].

PASO 3: RE-AUDITORÍA Y PILOTO DE CAMPO
1. Certifica la Fase 0 en DICTAMEN_AUDITORIA_LOCAL_SGMC.md mediante verificación física.
2. Procede a la Fase 1: Instalación de AppSheet en los 10 celulares del grupo piloto y prueba offline en vía.
```
