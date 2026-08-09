# Lo que hay que pedirle a Valentín

**Estamos parados por un permiso, no por una dificultad técnica.** Este documento dice exactamente
qué hace falta, por qué, y qué dos caminos hay para desbloquearlo.

| | |
|---|---|
| Bloqueado desde | 2026-08-09 |
| Quién decide | Dirección, con Valentín Ceballos |
| Aplicación | `SGMC-886843353`, propiedad de `valentinwebdeveloper@gmail.com` |
| Nuestra cuenta | `dieleoz@gmail.com`, **coautora** |

## 1. El bloqueo, en una frase

**Una cuenta coautora no puede dar de alta tablas en AppSheet**, y todo el trabajo pendiente consiste
precisamente en eso.

```
+ → Add data
"As a co-author you don't have the permission to add new data.
 Please ask the app owner to add new data."
```

## 2. Por qué el trabajo pendiente es exactamente eso

La aplicación se construyó sobre un modelo de datos que después se corrigió **en la hoja de cálculo**:
se renombraron 27 columnas, se crearon 8 tablas nuevas y se retiraron 45 campos. **AppSheet no se
enteró de nada de eso.**

Y no basta con pedirle que relea la hoja. Su documentación oficial lo dice:

> Al regenerar, AppSheet **combina la información nueva con la que ya exista** e intenta mantener el
> nombre y el tipo de las columnas existentes.

Es decir: **`Regenerate` fusiona, no reemplaza.** Las columnas viejas sobreviven. Lo comprobamos: la
tabla de órdenes de trabajo aguantó varios *Regenerate* conservando `Numero_OT`, `Tecnico`, `Estado`
y `SupervidorID`, mientras la hoja ya tenía `OTID`, `TecnicoID`, `EstadoOrdenID` y `SupervisorID`.

**Y las columnas reales no se pueden borrar una a una.** El propio AppSheet indica la salida:

> «Delete and re-add the table to create the column structure.»

**Borrar y volver a dar de alta cada tabla. Que es justo lo que un coautor no puede hacer.**

## 3. Dos caminos, y hay que elegir uno

### Opción A — Transferir la propiedad de la aplicación

Valentín transfiere `SGMC-886843353` a la cuenta de la Concesión.

**A favor:** se conserva la aplicación, su URL, sus vistas y su historial de versiones. No hay
ruptura para nadie.

**En contra:** el trabajo sigue siendo reconstruir 24 tablas una a una dentro de una app que arrastra
expresiones rotas. Es más lento, y quien lo haga va a ir encontrando restos durante días.

### Opción B — Construir la aplicación de nuevo desde la hoja

Se crea una aplicación nueva apuntando a la misma hoja de producción. AppSheet lee las 32 pestañas
con el esquema actual e infiere claves y referencias desde cero.

**A favor:** cero restos del modelo viejo. Es más rápido que reparar. Y **la propiedad queda desde el
primer minuto en la cuenta de la Concesión**, que es donde tiene que estar.

**En contra:** se pierden las vistas y acciones de la aplicación actual, y hay que rehacer la
interfaz.

**Y conviene medir lo que se pierde:** hoy la navegación padre-hijo está rota, el geofencing no
discrimina —el radio está vacío en los 24 tipos—, media capa de expresiones apunta a columnas que no
existen y el manual de usuario contiene nueve afirmaciones que contradicen el sistema. **No es
trabajo bueno que se tira: es trabajo roto que se deja de arrastrar.**

### Por qué el momento es ahora

**No hay usuarios en producción.** `MAN_Mantenimientos` tiene dos filas de prueba, las órdenes son
seis de ejemplo y ningún técnico ha usado la aplicación en campo. **Cambiar de aplicación hoy cuesta
cero. Dentro de dos meses es una migración.**

**Recomendamos la opción B**, y que la decisión la tome Dirección y no el equipo técnico: no es una
cuestión de arquitectura, es de a quién pertenece el sistema.

## 4. Aparte de la decisión, dos cosas concretas

**Dejar la aplicación original limpia.** Durante el diagnóstico del 2026-08-08 se renombró una tabla
—`SEC_Secciones` a `FRM_Secciones`— y eso dejó dos referencias colgando. La aplicación quedó en la
versión **1.000245**, no ejecutable.

> **Se arregla rodando atrás a la versión 1.000240** desde *Manage → Versions*.

Conviene decirlo tal cual: la aplicación **ya no cargaba antes** de ese cambio —ese era justamente el
problema que fuimos a diagnosticar—, pero esos dos errores concretos los introdujimos nosotros.

**Confirmar quién opera el despliegue.** Los cambios de esquema exigen volver a desplegar, y el plan
gratuito no ejecuta procesos programados. Haga falta o no cambiar de plan, tiene que estar claro
quién pulsa ese botón cuando la aplicación salga a campo.

## 5. Borrador del mensaje

> Hola Valentín,
>
> Estamos preparando el SGMC para salir a campo y nos hemos topado con un tope de permisos.
>
> El modelo de datos de la hoja se corrigió: se renombraron columnas, se crearon ocho tablas nuevas y
> se retiraron campos que ya no se usan. Para que la aplicación lo recoja hay que borrar y volver a
> dar de alta cada tabla —lo indica el propio AppSheet, porque *Regenerate* conserva las columnas
> viejas en lugar de sustituirlas—. Y **dar de alta tablas solo lo puede hacer el propietario de la
> aplicación**.
>
> Vemos dos caminos y preferimos que lo decidas tú con Dirección:
>
> **A.** Nos transfieres la propiedad de `SGMC-886843353` y seguimos sobre la aplicación actual.
>
> **B.** Levantamos una aplicación nueva desde la misma hoja de producción. Es más rápido, porque no
> arrastra el modelo viejo, y adelanta la entrega que ya estaba prevista.
>
> Sea cual sea, hay algo que conviene hacer ya: la aplicación quedó en la versión **1.000245** sin
> poder ejecutarse. Rodando atrás a la **1.000240** vuelve a su estado anterior. Dos de esos errores
> los provocamos nosotros al diagnosticar, y te pedimos disculpas por el ruido.
>
> Nada de esto corre prisa hoy: no hay técnicos usando la aplicación todavía. Pero sí queremos
> cerrarlo antes de cargar el inventario real, porque después sale mucho más caro.
>
> Cuéntanos qué prefieres y lo montamos.

---

*Mientras tanto, el trabajo continúa sobre una copia de ensayo —`SGMC2-323965761`— que apunta a un*
*duplicado de la hoja. Sirve para descubrir el procedimiento sin tocar producción, y ya ha destapado*
*media docena de defectos que no se veían desde la hoja.*
