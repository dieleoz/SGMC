# Prompt para el agente de AppSheet — Fase B, cableado de referencias

Autocontenido. Cópialo íntegro desde la línea siguiente.

---

Vas a trabajar en el **editor de Google AppSheet**, en la aplicación `SGMC-886843353` de la Concesión
Transversal del Sisga. El trabajo es convertir **15 columnas de texto o número en referencias entre
tablas**. Nada más: ni crear tablas, ni borrar columnas, ni cambiar datos.

Está autorizado por escrito y verificado antes de llegar a ti. **Lo que no está autorizado es
ampliarlo.**

## Lo único que tienes que entender antes de empezar

> **Una referencia de AppSheet guarda el valor de la clave de la tabla destino.**

De ahí salen las tres reglas que gobiernan todo lo que sigue:

1. **Primero la clave del destino, después quien la apunta.** Si conviertes la columna que apunta
   antes de fijar la clave a la que apunta, apuntará a lo que AppSheet decidiera por su cuenta.
2. **Convertir `Text` a `Ref` conserva solo las filas cuyo valor coincide con la clave del destino.
   Las demás quedan huérfanas, y AppSheet no avisa.** No hay mensaje de error: simplemente esa fila
   deja de resolver.
3. **Se valida en el Asistente de Expresiones, no ejercitando la aplicación.** Si escribes
   `[OTID].[ActivoID].[Ubicacion]` y el asistente lo acepta en verde, la cadena es navegable. Si da
   error, la referencia no está bien aunque la columna diga `Ref`.

## Antes de tocar absolutamente nada

**Estos cuatro pasos no son burocracia. AppSheet no tiene deshacer para un cambio de tipo de
columna.**

1. **Respaldo del Google Sheets.** Nómbralo `SGMC_backup_ANTES_FASE_B` con la fecha.
2. **Anota la versión actual de la app**, que aparece en el editor. AppSheet versiona solo; ese
   número es tu punto de restauración.
3. **Confirma que nadie va a usar la aplicación ni a editar la hoja mientras trabajas.** Hay dos
   cuentas con permiso de edición. **La reversión solo es limpia si nadie escribe durante la
   ventana.** Si no puedes confirmarlo, no empieces.
4. **Inventaría los nombres viejos.** Busca en el editor cualquier vista, fórmula o acción que cite:
   `Numero_OT`, `Tecnico`, `SupervidorID`, `Estado`, `MttoID`, `Tecnico_Asignado`, `EstadoID`,
   `SedeID`, y `Activo` usado como vínculo al activo. Apunta dónde aparece cada una: hay que
   repararlas al final, y si no las inventarías ahora no las encontrarás después.

## La trampa que ya mordió a este proyecto

Cuando das de alta una tabla o usas ***Regenerate Structure***, **AppSheet elige una clave por su
cuenta y crea referencias contra ella**. Puede incluso construir una clave compuesta de varias
columnas.

Eso ya pasó aquí: las acciones `View Ref (CalzadaID)`, `View Ref (EstadoID)` y `View Ref (SedeID)`
sobre `ACT_Activos` existen porque AppSheet las creó solo, sin que nadie las pidiera.

**Por eso no puedes hacer *Regenerate* y parar ahí.** Si regeneras, tienes que terminar de fijar las
claves en la misma sesión. Dejarlo a medias produce exactamente el estado que hay que evitar: tablas
con la clave adivinada y referencias automáticas colgando de ella.

## Las 15 columnas

Hazlas **en este orden**, que no es arbitrario: primero las que apuntan a catálogos, cuyas claves ya
están fijas, y al final las que dependen de otras conversiones.

### Primero, los catálogos

| Tabla | Columna | Hoy | Pasa a `Ref` a |
|---|---|---|---|
| `USR_Usuarios` | `RolID` | Number | `ROL_Roles` |
| `USR_Usuarios` | `SedeID` | Number | `SED_Sedes` |
| `ACT_Activos` | `TipoActivoID` | Number | `TIP_TiposActivo` |
| `ACT_Activos` | `CalzadaID` | Number | `CAL_Calzadas` |
| `ACT_Activos` | `SentidoID` | Number | `SEN_Sentidos` |
| `ACT_Activos` | `FrecuenciaID` | Number | `FRE_Frecuencias` |
| `TIP_TiposActivo` | `FormularioID` | Text | `FRM_Formularios` |

### Después, el motor de formularios

| Tabla | Columna | Hoy | Pasa a `Ref` a |
|---|---|---|---|
| `FRM_Preguntas` | `FormularioID` | Text | `FRM_Formularios` |
| `FRM_Preguntas` | `SeccionID` | Number | `FRM_Secciones` |
| `FRM_Preguntas` | `TipoRespuestaID` | Number | `TPR_TiposRespuesta` |
| `LST_ValoresLista` | `PreguntaID` | Text | `FRM_Preguntas` |

### Y al final, la cadena de ejecución

| Tabla | Columna | Hoy | Pasa a `Ref` a |
|---|---|---|---|
| `CHK_Checklists` | `FormularioID` | Text | `FRM_Formularios` |
| `CHD_ChecklistDetalle` | `ChecklistID` | Text | `CHK_Checklists` |
| `CHD_ChecklistDetalle` | `PreguntaID` | Text | `FRM_Preguntas` |
| `MAN_Mantenimientos` | `OTID` | Text | `OT_OrdenesTrabajo` |

**`MAN_Mantenimientos.OTID` es la más importante de las quince.** De ella cuelga el geofencing, el
filtro por zona y los reportes por activo. Déjala para el final y compruébala con más cuidado que
ninguna.

## Después de cada conversión, comprueba

No pases a la siguiente sin esto:

1. **Que la columna diga `Ref` y apunte a la tabla correcta.**
2. **Que las filas siguen resolviendo.** Abre la vista de esa tabla y mira que los valores se ven
   como el nombre del registro destino, no en blanco. **Una columna en blanco donde antes había un
   número es una referencia rota.**
3. **Que la cadena navega.** En el Asistente de Expresiones, escribe una desreferencia que pase por
   la columna nueva y comprueba que la acepta. Para `MAN_Mantenimientos.OTID`, esta:

```
[OTID].[ActivoID].[Ubicacion]
```

Si esa expresión da error, **para y repórtalo**. Es la que sostiene el geofencing.

## Varias pueden estar ya hechas

Algunas columnas quizá ya sean `Ref` con el nombre viejo, de conversiones anteriores o de algo que
AppSheet hizo solo. **Comprueba antes de crear.** Si ya está bien, no la toques y anótalo.

## Lo que NO debes hacer

- **No crees ninguna tabla.** Si algo parece necesitar una tabla nueva, para y repórtalo.
- **No borres ninguna columna**, ni siquiera las que parezcan duplicadas o sobrantes.
- **No cambies ningún dato.** Esto es un cambio de tipo, no de contenido.
- **No toques `MAN_Mantenimientos.Precision_GPS` del registro `TEST-MTTO-002`.** Vale `45` y está
  bien. Es un valor que asistentes anteriores han intentado «corregir» dos veces.
- **No pongas radios de geofencing.** Van en otra fase.
- **No modifiques ninguna comprobación ni ningún script** para que algo pase. Si una validación
  estorba, se reporta; no se retira.

## Cuándo pararte

Párate y reporta, sin seguir adelante, si ocurre cualquiera de estas:

- Una conversión deja filas en blanco que antes tenían valor.
- El Asistente de Expresiones rechaza una desreferencia que debería funcionar.
- AppSheet crea una clave compuesta o una referencia que nadie pidió.
- Aparece una columna duplicada con dos nombres parecidos.
- Cualquier cosa que te obligue a salirte de la lista de quince.

**Parar a mitad no es un fracaso.** Terminar con referencias rotas en silencio, sí.

## Cuando termines

**No lo des por cerrado tú.** En este proyecto se ha reportado un cierre tres veces y las tres veces
la comprobación contra el archivo encontró que no lo estaba.

Haz esto y entrega:

1. **Descarga el libro:** *Archivo → Descargar → Microsoft Excel*, y guárdalo en la carpeta `BD/`.
2. **Reporta, columna por columna**, cuál convertiste, cuál ya estaba hecha y cuál no pudiste.
3. **Pega el resultado de la expresión** `[OTID].[ActivoID].[Ubicacion]` en el asistente.
4. **Anota cualquier vista, fórmula o acción que se rompiera** al convertir, con su nombre.

El cierre lo declara la verificación automática sobre el archivo que descargaste, no tu informe.
