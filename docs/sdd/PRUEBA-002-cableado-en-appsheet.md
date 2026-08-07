# PRUEBA-002 — Pruebas de aceptación de ESPEC-002

Qué tiene que ocurrir para dar por bueno el cableado de la Fase B. **Escrito antes de ejecutar**,
que es lo único que impide medir el resultado con la vara que convenga después.

No es TDD: AppSheet no tiene framework de pruebas y su API REST exige plan Core. Son pruebas de
aceptación, y se llaman por su nombre.

| | |
|---|---|
| Cubre | `ESPEC-002` |
| Estado de partida | Fase A cerrada y verificada, `ACTA-002`. **43 conformes**, 0 fallos |
| Punto de restauración | AppSheet versión `1.000238`; Sheets `SGMC_backup_2026-08-07_antes_cableado_FaseA` |

## 1. Estado de partida

Verificado el 2026-08-07 sobre **`BD/Modelo de Datos (7).xlsx`**, que es una **descarga del Sheets
de producción** hecha ese mismo día tras aplicar `ESPEC-001C` (*Archivo → Descargar → Microsoft
Excel*). No es el Excel local histórico, que describe otro modelo:

| Tabla | Filas | Relevancia |
|---|---|---|
| `ACT_Activos` | 34 | Las 34 con `Ubicacion = 4.728512, -74.114531`, en Bogotá |
| `OT_OrdenesTrabajo` | 6 | Estados `Asignada`, `Cerrada`, `Suspendida` |
| `MAN_Mantenimientos` | 2 | `TEST-MTTO-001` en rango, `TEST-MTTO-002` a 8,89 km |
| `ASG_AsignacionZona` | 4 | Técnicos 3 a 6 contra unidades 7 a 10 |
| `FOT` / `FIR` / `CHK` / `CHD` | 3 / 1 / 1 / 15 | Cadena de evidencia poblada |

`python scripts/validar_modelo.py` devuelve 0 errores.

---

## 2. Pruebas

### P-01 — La estructura llegó a la aplicación

- **Qué comprueba:** que *Regenerate Structure* leyó la hoja actual y no una versión en caché.
- **Precondición:** paso 1 de `ESPEC-002` ejecutado.
- **Acción:** en *Data > Columns*, contar las columnas de `MAN_Mantenimientos`.
- **Resultado esperado:** **36**.
- **Cómo se distingue el fallo:** 27 significa que no regeneró. **Más de 36 significa definiciones
  de columna fantasma** que sobrevivieron al *Regenerate* —`MttoID`, `Tecnico_Asignado`,
  `EstadoID`, `SedeID`—, que es la causa más probable y hay que retirarlas. Menos de 36 y distinto
  de 27, que la hoja cambió sin que nadie lo registrara.

### P-02 — Las siete tablas nuevas existen en la app

- **Acción:** *Data > Tables*, buscar `UNF_UnidadesFuncionales`, `ASG_AsignacionZona`,
  `EOT_EstadosOrden`, `MOT_MotivosPendiente`, `FAL_ModosFalla`, `NOV_Novedades`,
  `PLA_PlanMantenimiento`.
- **Resultado esperado:** las **siete**, con el número de columnas que tiene cada hoja.
- **Cómo se distingue el fallo:** con seis no se sigue. La que falte rompe una referencia del paso 4.

### P-03 — Las claves son las correctas

- **Acción:** *Data > Columns*, revisar la casilla `KEY` en las **27 tablas** de la sección 4.2 de
  `ESPEC-002`, comprobando nombre **y tipo**. Todas las claves van `Text`.
- **Después de forzar el tipo, contar filas:** `ACT_Activos` 34, `USR_Usuarios` 11,
  `OT_OrdenesTrabajo` 6. Forzar el tipo de una clave es la operación que más silenciosamente pierde
  filas: si el recuento baja, la conversión dejó huérfanas.
- **Resultado esperado:** una sola clave por tabla, y la que dice la especificación.
- **Cómo se distingue el fallo:** dos claves marcadas, la clave en otra columna, o la clave tipada
  `Number`. **Es la prueba más silenciosa de todas:** una referencia contra una tabla con la clave
  mal fijada resuelve contra otra columna sin decirlo. Vigila en particular `USR_Usuarios.UsuarioID`
  —si AppSheet la infiere `Number`, la fila `3aa202ee` queda con clave inválida— y que
  `ACT_Activos.ActivoID` sea `Text`, porque `OT.ActivoID` guarda texto y si no coinciden la
  referencia no resuelve.

### P-04 — El formato de la coordenada, confirmado y no supuesto

- **Qué comprueba:** que lo que escribe `HERE()` coincide con lo que guarda `ACT_Activos.Ubicacion`.
  Hoy es un supuesto: no hay ni una coordenada capturada por la app en todo el sistema.
- **Precondición:** `Coordenadas_Cierre` tipada como `LatLong`.
- **Acción:** crear un registro desde la aplicación dejando que `HERE()` capture, y leer el Sheets
  de vuelta con el conector de Drive.
- **Resultado esperado:** un literal con la misma forma que `4.728512, -74.114531` — separador,
  espaciado y decimales comparables.
- **Cómo se distingue el fallo:** cualquier otra forma. **Si difiere, `DISTANCE()` no da error:
  devuelve un número y la regla parece funcionar sin funcionar.** Hay que reescribir las
  coordenadas de las filas `TEST-` antes de seguir.
- **Plan B, obligatorio si el ejecutor es un agente de navegador:** ese agente **no tiene GPS**.
  `HERE()` sin permiso de ubicación devuelve blanco o una posición por IP, que no confirma nada.
  En ese caso, o la captura la hace una persona desde un móvil, o **se declara el formato como
  supuesto verificado** —`4.728512, -74.114531`, el que ya usan las 34 filas de `ACT_Activos`— se
  anota en el acta y se sigue. Dar el formato por confirmado sin ninguna de las dos no vale.

### P-05 — La cadena de referencias existe

- **Qué comprueba:** el defecto raíz del sistema, el que lleva meses abierto.
- **Acción:** en el Asistente de Expresiones, sobre `MAN_Mantenimientos`, escribir
  `[OTID].[ActivoID].[Ubicacion]`.
- **Resultado esperado:** resuelve sin error.
- **Cómo se distingue el fallo:** `Invalid dereference. Column OTID is not a Ref` significa que la
  conversión no quedó. Es el mensaje exacto que este proyecto lleva meses recibiendo.

### P-06 — Los estados de las órdenes resuelven

- **Acción:** abrir las 6 órdenes en la vista previa.
- **Resultado esperado:** las 6 muestran su estado, ninguna en blanco.
- **Cómo se distingue el fallo:** un estado vacío es una fila huérfana. Con las claves de
  `EOT_EstadosOrden` corregidas en `ESPEC-001B` no debería ocurrir; si ocurre, algo se deshizo.

### P-07 — La navegación padre-hijo funciona

- **Acción:** abrir una orden en la vista previa.
- **Resultado esperado:** el activo se muestra como **enlace navegable**, y al pulsarlo se abre su
  ficha.
- **Cómo se distingue el fallo:** si sigue viéndose el número `2`, la referencia no quedó.

### P-08 — POSITIVA: el cierre en rango se acepta

- **Precondición:** RG-01 configurada.
- **Acción:** abrir `TEST-MTTO-001`, cuyo `Coordenadas_Cierre` es `4.728512, -74.114531`, e
  intentar guardar.
- **Resultado esperado:** se guarda sin error.
- **Cómo se distingue el fallo:** si lo rechaza, la regla está invertida o el radio mal puesto.

### P-09 — NEGATIVA: el cierre fuera de rango se rechaza. **La prueba que importa**

- **Qué comprueba:** que la validación **existe**. Una regla de geofencing que nunca ha rechazado
  un cierre no está probada, solo escrita.
- **Acción:** abrir `TEST-MTTO-002`, cuyo `Coordenadas_Cierre` es `4.650000, -74.100000`, a
  **8,89 km** del activo, e intentar guardar.
- **Resultado esperado:** **rechazado**, con el texto exacto
  `Ubicación fuera de rango: debe estar junto al activo para cerrar.`
- **Cómo se distingue el fallo:** dos formas, y ambas cuentan como fallo:
  1. Lo acepta. La regla no se aplica.
  2. Lo rechaza con un error genérico de AppSheet. La regla existe pero el mensaje no guía al
     técnico, que es medio requisito.

### P-10 — El filtro por zona devuelve algo

- **Precondición:** RG-04 configurada, `ASG_AsignacionZona` con sus 4 filas.
- **Acción:** en *Preview app as*, usar el correo de un técnico —por ejemplo
  `santiago.moreno@concesiondelsisga.com.co`, usuario 4, unidad 8— y abrir la lista de activos.
- **Resultado esperado:** **más de cero** activos, y solo los de su unidad funcional.
- **Cómo se distingue el fallo:** cero activos es el bloqueante B-03 sin resolver. Los 34 significa
  que el filtro no se aplica.

### P-11 — El histórico no se puede borrar

- **Precondición:** RG-14 y RG-15 configuradas.
- **Acción:** abrir una orden y un mantenimiento en la vista previa.
- **Resultado esperado:** **no aparece la acción de borrar** en ninguna de las dos.
- **Cómo se distingue el fallo:** si el botón está, la puerta trasera sigue abierta: un clic
  elimina la prueba de que un técnico estuvo frente a un equipo.

### P-12 — LECTURA DE VUELTA: el dato llegó al Sheets

- **Qué comprueba:** que sincronizó. **La aplicación puede mostrar un registro guardado que no
  llegó al backend**, y sin esta prueba no hay forma de saberlo.
- **Acción:** tras P-08, leer `MAN_Mantenimientos` en producción con el conector de Drive,
  `fileId = 1a4MmZ0u9sNgWmyiR2OPJo9YuUEKJFftbJWMW-KbITRc`.
- **Resultado esperado:** la fila con valor en `Coordenadas_Cierre` y `Precision_GPS`.
- **Cómo se distingue el fallo:** si la app lo muestra y el Sheets no lo tiene, hay un problema de
  sincronización que ninguna otra prueba detecta.

### P-13 — Las vistas rotas quedaron reparadas

- **Acción:** recorrer las vistas de la aplicación y el panel de errores del editor.
- **Resultado esperado:** ninguna referencia a `Numero_OT`, `Activo` como vínculo al activo,
  `Tecnico`, `SupervidorID`, `Estado`, `MttoID`, `Tecnico_Asignado`, `EstadoID` ni `SedeID`. Es la
  misma lista del punto 3.4 y del bloque 5 de `ESPEC-002`: si divergen, el ejecutor repara una cosa
  y el probador mide otra.
- **Cómo se distingue el fallo:** cualquier vista que cite un nombre viejo. La app lleva rota desde
  la Fase A y esto es lo que la devuelve a funcionar.

---

## 3. Pruebas bloqueadas

### P-14 — Geofencing con coordenadas reales · **BLOQUEADA POR D-01**

Los 34 activos comparten `4.728512, -74.114531`, que está en Bogotá y no en el corredor. Cualquier
cierre real en la vía quedará fuera de rango y cualquier cierre en Bogotá quedará dentro.

**No es un fallo de la Fase B.** P-08 y P-09 demuestran que **la regla funciona**; esta demostraría
que **el dato es correcto**, y para eso hace falta el levantamiento de campo.

### P-15 — Bots y procesos programados · **BLOQUEADA POR D-B**

RG-06 a RG-08 y RG-10 a RG-13 son bots. En el plan gratuito los procesos programados no se
ejecutan. Se configuran, no se prueban.

---

## 4. Criterio de cierre

**Deben pasar P-01 a P-13, las trece.** P-14 y P-15 quedan bloqueadas por decisiones ajenas a esta
fase.

Tres son innegociables, y conviene decir por qué antes de que alguien proponga cerrar sin ellas:

- **P-05**, porque es el defecto raíz. Sin la cadena no hay sistema, solo formularios.
- **P-09**, porque una validación que nunca ha rechazado nada no está probada. Es la única prueba
  que distingue «la regla funciona» de «la regla no se aplica».
- **P-12**, porque sin lectura de vuelta no hay constancia de que el dato salió de la pantalla.

Si alguna de las tres falla, la Fase B **no se cierra**, por muchas de las otras que pasen.
