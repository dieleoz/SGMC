# 🤖 PROMPT Y DIRECTIVA DE INSTRUCCIÓN PARA EL AGENTE DE AUDITORÍA Y SUBSANACIÓN

**Copie y pegue el siguiente bloque de texto en la consola de cualquier Agente IA (Claude, ChatGPT, Antigravity, etc.) para que ejecute la auditoría previa y subsanación en el orden correcto:**

```text
PROMPT PARA EL AGENTE DE INGENIERÍA Y AUDITORÍA DE SOFTWARE:

Actúa como Auditor Principal de Arquitectura de Software y Desarrollador Senior de Google AppSheet para el proyecto SGMC de la Concesión Transversal del Sisga S.A.S.

Tu objetivo es ejecutar el Plan de Trabajo con la metodología AUDIT-FIRST (Auditar Primero -> Subsanar Después -> Desplegar Piloto).

SIGUE ESTAS INSTRUCCIONES EN ORDEN ESTRICTO:

PASO 1: AUDITORÍA PREVIA Y DIAGNÓSTICO DE LA BASE DE DATOS (SIN EDITAR NADA)
1. Inspecciona el backend de producción en Google Sheets:
   https://docs.google.com/spreadsheets/d/1a4MmZ0u9sNgWmyiR2OPJo9YuUEKJFftbJWMW-KbITRc/edit?gid=1353886072#gid=1353886072
   y el archivo local d:\@Proyect\Sisga\BD\Modelo de Datos (2).xlsx (24 Hojas).
2. Revisa la hoja 'MAN_Mantenimientos' y verifica si existen las columnas 'Coordenadas_Cierre' (LatLong) y 'Precision_GPS' (Decimal).
3. Revisa las hojas 'CHK_Checklists' y 'CHD_ChecklistDetalle' e inspecciona sus columnas relacionales.
4. Revisa la hoja índice 'Tablas' y verifica si la rotulación dice 'FRM_Formularios' o 'CAF_Formularios'.
5. Emite un breve Dictamen de Diagnóstico indicando lo que está presente y lo que falta.

PASO 2: SUBSANACIÓN Y AJUSTE DE LA BASE DE DATOS (SOLO TRAS EL DIAGNÓSTICO)
1. En la hoja 'MAN_Mantenimientos' de Google Sheets y del Excel local, agrega las columnas 'Coordenadas_Cierre' y 'Precision_GPS'.
2. Unifica 'CAF_Formularios' por 'FRM_Formularios' en la hoja 'Tablas'.
3. Configura en el editor de AppSheet la regla Valid_If para Geofencing GPS:
   DISTANCE([Coordenadas_Cierre], LATLONG([ActivoID].[Latitud], [ActivoID].[Longitud])) <= 1.0
   y el mensaje de error en español: "⚠️ Ubicación fuera de rango: Debe estar a menos de 1.0 km del activo".

PASO 3: RE-AUDITORÍA Y DESPLIEGUE DEL PILOTO
1. Certifica el cierre de la Fase 0 en DICTAMEN_AUDITORIA_LOCAL_SGMC.md.
2. Inicia la Fase 1: Despliegue de AppSheet App en los 10 móviles del grupo piloto, verificación de Security Filter por SedeID y pruebas offline en vía.

Confirma que has comprendido el protocolo AUDIT-FIRST antes de iniciar.
```
