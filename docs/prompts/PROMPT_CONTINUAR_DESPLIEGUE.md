# Prompt para continuar el despliegue — correcciones y cierre

Autocontenido. Cópialo íntegro desde la línea siguiente.

---

Estás terminando de configurar la aplicación **SISGA** en Google AppSheet.

> ## Quedan dos cosas, no seis
>
> **Revisado el 2026-08-10 contra `ESTADO.md` §2.** Este guion se escribió con seis apartados y hoy
> solo dos siguen vivos:
>
> | Apartado | Estado |
> |---|---|
> | 1. Deshacer `MAN_Mantenimientos.Diagnostico` | **Hecho.** Se conserva como constancia de qué se aplicó y por qué |
> | **2. La regla del umbral de GPS** | **PENDIENTE. Es lo primero** |
> | 3. Retirar el borrado | **Hecho** en las dos tablas |
> | 4. Los cuatro `ChangeTimestamp` | **Hechos** |
> | 5. Ocultar las 47 columnas retiradas | **FUERA DEL PLAN.** No lo haga — ver abajo |
> | **6. Las tres expresiones de prueba** | **PENDIENTE** |
>
> **El apartado 5 salió del plan el 2026-08-09**, cuando se decidió migrar a la hoja limpia: esas
> columnas **desaparecen del archivo**, con las tres trampas dentro. Ocultarlas ahora es una hora de
> trabajo que se tira. La lista se conserva porque sigue valiendo para quien tenga que operar sobre
> `Modelo_Datos_09082026` mientras no se migre.
>
> Los apartados 1, 3 y 4 se conservan sin tocar: describen lo que se aplicó y por qué, que es lo
> que hace falta para no repetir el error que los motivó.

## 1. HECHO — Deshacer `MAN_Mantenimientos.Diagnostico`

Durante las pruebas, esa columna quedó así:

```
Type:         LatLong
App formula:  [OTID].[ActivoID].[Ubicacion]
```

**Hay que revertirlo.** `Diagnostico` es una columna retirada del modelo que sigue existiendo en la
hoja, en la posición 9 de `MAN_Mantenimientos`.

**Por qué corre prisa:** una `App formula` **escribe en la hoja** cada vez que se modifica la fila.
Tal como está, cada mantenimiento que alguien guarde escribirá la coordenada del activo dentro de la
columna `Diagnostico`, machacando lo que hubiera. No da error y no avisa.

**Qué hacer:**

1. `MAN_Mantenimientos` → columna `Diagnostico` → lápiz.
2. **Borrar la `App formula`.** Dejar el campo vacío.
3. **Tipo: `LongText`.**
4. **Desmarcar `Show?`.**
5. `Done`.

**Y comprueba en la hoja** que ninguna fila de `MAN_Mantenimientos` tiene una coordenada escrita en
`Diagnostico`. Si la tiene, bórrala a mano: son dos filas.

> **La lección, para no repetirla:** una expresión se prueba en el **Asistente de Expresiones**, que
> solo la evalúa. Escribirla dentro de una columna la convierte en configuración activa.

## 2. PENDIENTE — Completar la regla del umbral de GPS

En `MAN_Mantenimientos.CierreConExcepcion`, la `App formula` actual está incompleta. Sustitúyela por
esta, entera:

```
OR(ISBLANK(LOOKUP("UMBRAL_GPS", "PAR_Parametros", "ParametroID", "Valor")), [Precision_GPS] > LOOKUP("UMBRAL_GPS", "PAR_Parametros", "ParametroID", "Valor"))
```

**Qué añade el `ISBLANK`:** si alguien borra la fila del parámetro, la versión corta hace que
**todos los cierres salgan limpios y nadie se entere**. Con el `ISBLANK`, si el umbral no se puede
leer, el cierre se marca como excepcional. Falla hacia el lado seguro.

## 3. HECHO — Retirar el borrado

En *Data → Tables → `OT_OrdenesTrabajo` → Are updates allowed*:

```
Updates ✓    Adds ✓    Deletes ✗
```

**Lo mismo en `MAN_Mantenimientos`.**

**Por qué no es opcional.** Se marcó `IsPartOf` en cuatro referencias —`FOT`, `FIR` y `CHK` hacia el
mantenimiento, y `CHD` hacia el checklist—. `IsPartOf` significa **borrado en cascada**: borrar un
mantenimiento se lleva sus fotografías, su firma y su checklist.

Eso solo es seguro **porque el mantenimiento nunca se borra**. Y eso es exactamente lo que hace
quitar `Deletes`.

Tal como está la aplicación ahora mismo, la cascada está creada y la protección no.

## 4. HECHO — Las cuatro marcas de tiempo del servidor

Estas cuatro columnas tienen que ser de tipo **`ChangeTimestamp`**. AppSheet no lo infiere nunca:
llegan como texto.

```
MAN_Mantenimientos.FechaHoraRegistro
FOT_Fotografias.FechaHora
FIR_Firmas.FechaHora
NOV_Novedades.FechaHora
```

**`ChangeTimestamp` la pone el servidor.** Un `Initial value = NOW()` lo pone el teléfono, y el
usuario puede cambiar la hora del teléfono. Sin esto, **la hora de cada fotografía y de cada firma
no prueba nada**, que es justo lo que el sistema existe para sostener.

## 5. FUERA DEL PLAN — Ocultar las columnas retiradas

> **No ejecute este apartado.** Salió del plan el 2026-08-09 al decidirse la migración a la hoja
> limpia: en `BD/Modelo_Datos_PLANTILLA.xlsx` esas 47 columnas **no existen**, así que no hay nada
> que ocultar ni ninguna trampa que deshacer. La lista se conserva para quien tenga que operar
> sobre `Modelo_Datos_09082026` mientras la migración no se ejecute.

### La lista completa, si opera sobre la hoja heredada

Son **47 columnas**. Estan en la hoja, el modelo no las declara, y al dar de alta las tablas
entraron con `Show?` marcado: aparecen en el formulario del tecnico junto a las buenas.

**Para cada una: tipo `Text`, `Show?` desmarcado, sin formula.** No se borran.

**3 son TRAMPA:** su nombre coincide con la clave de otra tabla, asi que **AppSheet las convierte
en `Ref` sola**. Si las ve como `Ref`, hay que deshacerlo.

> **Esta lista se deriva del archivo, no se escribe.** Una version anterior mandaba ocultar
> `FRM_Preguntas.RequiereGPS`, que **si esta viva** y la lee el `show_if` de
> `CHD_ChecklistDetalle.RespuestaGPS`. Ocultarla habria roto esa regla.

### `CHD_ChecklistDetalle` — 12 columnas

```
Activo                
EstadoPregunta        
FechaRespuesta        
Orden                 
PreguntaActual        
RespuestaFecha        
RespuestaFirma        
RespuestaFoto         
RespuestaGPS          
RespuestaHora         
TipoRespuestaID          <-- TRAMPA
TotalPreguntas        
```

### `CHK_Checklists` — 15 columnas

```
Activo                
ActivoID                 <-- TRAMPA
Estado                
FechaCreacion         
FechaEnvioCorreo      
FirmaSupervisor       
FirmaTecnico          
GPSFin                
GPSInicio             
Observaciones         
PDF                   
Porcentaje            
PreguntaActual        
TecnicoID             
TotalPreguntas        
```

### `FOT_Fotografias` — 1 columnas

```
Fecha                 
```

### `FRM_Formularios` — 1 columnas

```
Orden                 
```

### `FRM_Preguntas` — 1 columnas

```
ValorDefecto          
```

### `MAN_Mantenimientos` — 13 columnas

```
Diagnostico           
Duracion_Minutos      
Estado_Intervencion   
Fecha                 
Firma_Supervisor      
Firma_Tecnico         
Imagen_Final          
Imagen_Inicio         
Localizacion          
Repuestos_Utilizados  
Requiere_Repuesto     
Tipo                  
Trabajo_Realizado     
```

### `OT_OrdenesTrabajo` — 3 columnas

```
FormularioID             <-- TRAMPA
Informe_Final         
Motivo_Cierre         
```

### `USR_Usuarios` — 1 columnas

```
UltimaSincronizacion  
```

**Por que importa.** Quedan pares que registran lo mismo en dos sitios: `Requiere_Repuesto` junto a
`MotivoPendienteID`, `Firma_Tecnico` junto a la tabla `FIR_Firmas`, `Imagen_Inicio` e `Imagen_Final`
junto a `FOT_Fotografias`.

## 6. PENDIENTE — Las pruebas, y esta vez en el sitio correcto

**En el Asistente de Expresiones**, que evalúa sin guardar nada. Se abre desde el icono de la
probeta en cualquier campo de fórmula — **y se cierra sin dar a `Done`**.

**Las dos que deben salir verdes:**

```
[OTID].[ActivoID].[Ubicacion]
[OTID].[TecnicoID].[Correo]
```

**Y una que tiene que salir mal, o hay que anotar que no:**

```
REF_ROWS("OT_OrdenesTrabajo", "Activo")
```

`Activo` en `OT_OrdenesTrabajo` **ya no es la referencia al activo**: es la bandera Sí/No. Esa
expresión apunta a la columna equivocada y devuelve lista vacía.

**Si el Asistente la acepta, anótalo con su salida literal.** Es la prueba de que un despliegue
verde no distingue esa expresión de la correcta. Sin verla aceptada, no sabemos si lo demás pasó por
diligencia o por casualidad.

## Cuando termines, reporta

**Solo hay dos cosas que reportar**, porque solo dos estaban pendientes:

1. **La regla del umbral**: pegada entera, con el `ISBLANK`.
2. **Las tres expresiones**, con lo que dijo el Asistente en cada una.

Y si al pasar ves que algo de los apartados 1, 3 o 4 **no** está como dicen, dilo: se dan por
hechos y conviene saber si no lo están.

## Lo que NO debes hacer

- **No borres ninguna columna.** Se ocultan.
- **No pruebes expresiones escribiéndolas en una columna.** Solo en el Asistente.
- **No toques `Precision_GPS` del registro `TEST-MTTO-002`.** Vale `45` y es la fila que prueba el
  rechazo por GPS deficiente.
- **No publiques todavía.** Los 34 activos comparten una sola coordenada, en Bogotá: con el radio de
  1 km, la aplicación rechazaría **todos** los cierres hechos en el corredor.
