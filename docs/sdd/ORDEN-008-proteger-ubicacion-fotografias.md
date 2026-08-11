# ORDEN-008 — `ESPEC-008` NO se aplica: falta el veredicto del arquitecto

**Este documento no es un registro de ejecución. Es la constancia de por qué se paró antes de
tocar nada.** `scripts/modelo_objetivo.py` **no** lleva `RG-39` ni `RG-40`, y
`scripts/generar_prompt_cableado.py` **no** lleva el parche del §2.6/§4 de `ESPEC-008`. Ningún
documento derivado se regeneró para esta orden.

## 1. Las tres firmas — dónde fallan

| | |
|---|---|
| Cubre (si se aplicara) | [`ESPEC-008-proteger-ubicacion-fotografias.md`](ESPEC-008-proteger-ubicacion-fotografias.md) y [`PRUEBA-008-proteger-ubicacion-fotografias.md`](PRUEBA-008-proteger-ubicacion-fotografias.md) |
| Contra cuál sistema | Aplicación `_SISGA_-323965761` sobre la hoja `Modelo_Datos_10082026` (`fileId` `1h9kyCYGK6esRL1UiTcPXHlSmDQcPb13fNZ0hBznYOa0`) — no llega a importar, porque no se aplica nada |
| Secuencia | Evaluada **después** de `ORDEN-007`, ya aplicada y verificada (§5 de `ORDEN-007-precision-gps-fotografias.md`), sobre el mismo repositorio |

1. **Especificación.** `ESPEC-008` existe, está bien investigada (§2 verifica el defecto, la
   ausencia de otras columnas en la misma situación, y encuentra un defecto real de generador que
   habría dejado el formulario de fotografías inutilizable si no se hubiera visto — §2.6). **Pero su
   propia §8 dice, textualmente:**

   > **Sin pasar por el arquitecto todavía.** A diferencia de `ESPEC-007` §8 y `ESPEC-006` §8, que
   > cierran registrando una aprobación ya ocurrida, este documento se entrega para esa revisión: no
   > hay fecha ni pasada de arquitecto que anotar aquí, y escribir una sería exactamente la clase de
   > afirmación que este proyecto no se puede permitir.

   Y su lista de riesgos se titula explícitamente *"Riesgos que se proponen como aceptables,
   **pendientes de que el arquitecto lo decida**"* — no *"riesgos aceptados"*.

2. **Pruebas.** `PRUEBA-008` está escrita y es ejecutable (`P-69` a `P-75`), pero probar una
   especificación sin veredicto no la habilita para aplicarse.

3. **Arquitecto.** **No hay veredicto.** No existe ningún archivo de dictamen en `docs/sdd/`
   (`ls docs/sdd/ | grep -i dictamen` no devuelve nada), y el propio documento primario lo confirma
   en el punto 1.

4. **Gate objetivo.** No se corrió como condición de arranque de esta orden, porque el punto 3 ya
   basta para detenerse — no hace falta seguir verificando una vez que una de las tres firmas falta.

## 2. La contradicción encontrada, con la evidencia completa

Antes de concluir que faltaba el veredicto, se revisaron **todas** las fuentes de estado del
repositorio que mencionan `ESPEC-008`, porque dos de ellas dicen lo contrario:

| Fuente | Qué dice | Cuándo |
|---|---|---|
| `docs/sdd/ESPEC-008-proteger-ubicacion-fotografias.md` §8 | *"Sin pasar por el arquitecto todavía"* | Última edición: commit `4ad9d06`, 2026-08-11 15:41 |
| `MAP.md:171` | *"Especificada, **sin pasar todavía por el arquitecto** (§8)"* | Coincide con la fuente primaria |
| `ESTADO.md:31,73` | *"aprobada con riesgos aceptados (2026-08-11), con sus ocho condiciones aplicadas"* | Escrito por el commit `7d1d68e`, 2026-08-11 15:59 |
| `docs/ROADMAP.md:232-233` | *"está aprobada con riesgos aceptados (2026-08-11) [...] no entra en esta tabla porque **todavía no llegó al arquitecto**"* — se contradice en la misma frase | Mismo commit `7d1d68e` |

**Verificado con `git`, no supuesto:**

```
$ git log --all --oneline -- docs/sdd/ESPEC-008-proteger-ubicacion-fotografias.md
4ad9d06 ESPEC-008 aprobada: ocho condiciones, ampliada a NOV, y un sitio para lo que no es spec
3fabf70 ESPEC-008: proteger la coordenada de las fotografias, y el arreglo que habria roto mas que el defecto

$ git show 4ad9d06 -- docs/sdd/ESPEC-008-proteger-ubicacion-fotografias.md | grep -n "^@@"
@@ -2,7 +2,9 @@
@@ -340,12 +342,30 @@ introduce esta especificación...
@@ -399,6 +419,19 @@ le toque:
@@ -440,12 +473,41 @@ Todo en `scripts/modelo_objetivo.py`, dos puntos...
```

Ninguno de esos cuatro *hunks* toca la sección `## 8. Cierre`: pese a que el título del commit dice
"ESPEC-008 aprobada", el propio archivo que se editó ese día **nunca recibió la frase de cierre**
que sí recibió `ESPEC-007` en su commit equivalente (`73c635b`, *"ESPEC-007 aprobada: las siete
condiciones..."*, que sí edita su §8 con fecha, veredicto y lista de condiciones cumplidas —
verificado leyendo `ESPEC-007` §8 en `ORDEN-007-precision-gps-fotografias.md` §1).

El commit `7d1d68e`, que es el que introdujo "aprobada" en `ESTADO.md` y `docs/ROADMAP.md`, tiene
como asunto exactamente **"Los cuatro sitios que indujeron a un lector a reportar mal"**, y su
propio mensaje dice: *"Un agente leyo README, ESTADO y ROADMAP y produjo cuatro afirmaciones falsas.
Ninguna fue culpa suya: los documentos las inducian."* — es decir, el mismo tipo de documento que
ese commit corrige por inducir errores es la única fuente que afirma que `ESPEC-008` está aprobada,
y lo hace sin que el documento primario lo respalde.

**Conclusión: no hay manera de verificar, dentro de este repositorio, que un arquitecto haya
dictaminado sobre `ESPEC-008`.** Lo más parecido que existe es la reescritura sustancial de
`ESPEC-008` en el commit `4ad9d06` — que sí incorpora lenguaje como *"corregido tras el dictamen"* y
*"el arquitecto la señaló"* en tiempo pasado, sugiriendo que hubo alguna forma de retroalimentación
informal — pero sin una fecha, una cita textual de veredicto, ni la actualización de su propia §8 que
todas las demás especificaciones aprobadas de este repositorio sí tienen.

## 3. Qué se aplicó

**Nada.** `scripts/modelo_objetivo.py` no lleva `RG-39` ni `RG-40`, ni `editable=False` en
`FOT_Fotografias.Ubicacion_LatLong` ni en `NOV_Novedades.Ubicacion_LatLong`.
`scripts/generar_prompt_cableado.py` no lleva el parche de las líneas 327-331. Ningún documento
(`docs/ARQUITECTURA_OBJETIVO_SGMC.md`, `docs/MANUAL_DESPLIEGUE.md`, `docs/PROMPT_CABLEADO.md`,
`docs/PROMPT_EXPRESIONES.md`, `docs/sdd/RECONSTRUCCION_EXPRESIONES.md`,
`docs/REGLAS_DEL_MODELO_DE_DATOS.md`) se regeneró para esta orden.

**Confirmado, sobre el estado real del repositorio, después de `ORDEN-007`:**
```
$ python -c "
import sys;sys.path.insert(0,'scripts');from modelo_objetivo import REGLAS
print('RG-39' in [r['id'] for r in REGLAS], 'RG-40' in [r['id'] for r in REGLAS])
"
False False

$ grep -n "RG-39\|RG-40" docs/sdd/RECONSTRUCCION_EXPRESIONES.md
(sin resultado)
```

Las dos filas que este documento tendría que producir en `docs/PROMPT_CABLEADO.md` —

```
| `FOT_Fotografias` | `Ubicacion_LatLong` | `Initial value` | `HERE()` |
| `MAN_Mantenimientos` | `Coordenadas_Cierre_LatLong` | `Initial value` | `HERE()` |
```

— **no aparecen**, porque no se aplicó ningún cambio. La segunda fila en particular sigue sin
existir hoy en `docs/PROMPT_CABLEADO.md` (verificado: `grep -n "Coordenadas_Cierre_LatLong.*Initial
value\|Initial value.*Coordenadas_Cierre_LatLong" docs/PROMPT_CABLEADO.md` sin resultado), que es
justo el defecto preexistente que `ESPEC-008` §2.6 documentó sin corregir: sigue vivo, sin relación
con esta orden.

## 4. Qué NO se aplicó, y por qué

Todo. Por el motivo del §1-§2: no hay veredicto verificable del arquitecto sobre `ESPEC-008`, y el
protocolo de este ejecutor no admite una ruta que lo salte. Ni el modelo, ni el generador de
`generar_prompt_cableado.py`, ni ningún documento derivado, ni el editor de AppSheet, ni el Sheets
de producción se tocaron para esta orden.

## 5. Verificación

No aplica una verificación de cierre de cambios, porque no hubo cambios de esta orden. Los ocho
verificadores de la sesión completa (`validar_modelo.py`, `verificar_faseA.py`,
`verificar_documentos.py`, `verificar_enlaces.py`, `verificar_reproducible.py`,
`verificar_datos.py`, `verificar_sistema.py`, `probar_auditor.py`) están en verde y quedaron
registrados en `ORDEN-007-precision-gps-fotografias.md` §5 — el estado del repositorio al cierre de
esta sesión es exactamente ese, sin ninguna diferencia introducida por este documento.

## 6. Qué queda pendiente — para quien reciba esta cola

**No es una tarea de editor de AppSheet: es una tarea de gate.** Antes de que `ORDEN-008` se pueda
escribir como orden aplicable, alguien con la vara de arquitecto tiene que hacer una de estas dos
cosas, con fecha y por escrito, en el propio `docs/sdd/ESPEC-008-proteger-ubicacion-fotografias.md`
§8:

1. **Dictaminar de verdad** — leer `ESPEC-008` completa (§2 a §7 ya están investigadas y no hace
   falta rehacerlas) y escribir el veredicto con fecha, PASA o PASA CON CONDICIONES, y la lista de
   condiciones si las hay — el mismo molde que `ESPEC-007` §8 ya sigue. O
2. **Si la aprobación citada en `ESTADO.md`/`docs/ROADMAP.md` sí ocurrió** y solo faltó
   transcribirla al documento primario, completar `ESPEC-008` §8 con esa misma fecha y las ocho
   condiciones que esos dos documentos dicen que están aplicadas — nombrándolas una por una, no como
   una cifra suelta.

Solo entonces esta orden se puede reabrir. El trabajo de investigación (§2 de `ESPEC-008`, el
defecto de generador de su §2.6 con el parche ya escrito, `RG-39`/`RG-40` ya redactadas) no hay que
rehacerlo: sigue siendo válido y queda tal como está.

**Nada de lo anterior toca el editor de AppSheet ni el Sheets de producción**, y no hay ninguna cola
de sesión de navegador que abrir para esta orden todavía — abrir el editor para `RG-39`/`RG-40`
antes de que exista el veredicto sería la misma clase de atajo que este documento existe para
impedir.

## 7. Reversión

No aplica: no se aplicó ningún cambio que revertir.
