> # Documento historico. NO SE APLICA.
>
> **Esta orden autorizaba tocar una aplicación que ya no existe.** Autorizaba ejecutar `ESPEC-002`
> sobre `SGMC-886843353` —convertir 15 columnas de `Text` a `Ref` en el editor— y esa aplicación
> **se abandonó el 2026-08-09**: AppSheet no admite un cambio de esquema de ese tamaño, porque su
> `Regenerate` fusiona en vez de reemplazar (`docs/BASE_CONOCIMIENTO_APPSHEET.md` §11 y §12).
>
> Su §5 exigía un `ACTA-005` de cierre. **No existe y no va a existir:** la orden no llegó a
> cerrarse, se reconstruyó la aplicación en su lugar. La app vigente es `SISGA`, con las **38**
> referencias del modelo, no 15.
>
> Lo que la sustituye: [`docs/MANUAL_DESPLIEGUE.md`](../MANUAL_DESPLIEGUE.md) para construir, y
> [`docs/sdd/PRUEBA-003-despliegue.md`](../sdd/PRUEBA-003-despliegue.md) para medir.
>
> Se conserva por trazabilidad: explica por qué se decidió lo que hay hoy.
> **El estado vigente está en [`ESTADO.md`](../../ESTADO.md).**

# ORDEN-002 — Ejecución de la Fase B

**Queda autorizada la ejecución de `ESPEC-002` en el editor de AppSheet.** Es la primera vez en este
proyecto que se toca producción con las tres firmas del pipeline SDD.

| | |
|---|---|
| Especificación | `ESPEC-002-cableado-en-appsheet.md` |
| Pruebas | `PRUEBA-002-cableado-en-appsheet.md`, 17 casos |
| Gate | Arquitecto, décimo veredicto, tras once rondas |
| Precondición | `verificar_faseA.py` sobre `BD/Modelo de Datos (11).xlsx` → **`FASE A CERRADA`** |
| Autorizado el | 2026-08-07 |

## 1. Por qué se ejecuta ahora y no después de `ESPEC-003`

`ESPEC-003` está **bloqueada** por el arquitecto con cinco hallazgos bloqueantes. Podría parecer que
la Fase B tiene que esperar. **No es así, y está verificado con los comandos en la mano:**

- La Fase B es trabajo en el editor de AppSheet sobre las **28 tablas que ya existen**. No toca
  `scripts/modelo_objetivo.py`.
- El bloqueo que describe `ESPEC-003` §2.4 —`verificar_faseA.py` F-02 falla ante una tabla declarada
  en `MODELO` sin hoja en el libro— **solo se activa al declarar las tablas nuevas**. Mientras no se
  declaren, el modelo valida en 0 errores.
- El único punto de contacto real entre las dos es `TIP_TiposActivo.FormularioID`, y `ESPEC-003`
  §7.4 ya lo resuelve por secuencia: **la Fase B lo cablea como dice `ESPEC-002`, y su retirada
  espera a la Fase C.**

**El bloqueo no es entre las dos fases: es entre la Fase B y el acto de aplicar `ESPEC-003`.**

## 2. La condición que gobierna esta orden

> **Mientras la Fase B esté abierta, nada de `ESPEC-003` se escribe en
> `scripts/modelo_objetivo.py`.**

Ni las tablas propuestas, ni las columnas nuevas, ni las reglas RG-21 a RG-31. `PROPUESTAS` y
`DECISIONES` son declaraciones de intención y no declaran estructura: por eso pueden estar ahí sin
romper nada. **Declarar una tabla en `MODELO` sí rompe**, y rompería el gate objetivo del que
depende esta orden.

## 3. Alcance exacto

Convertir **15 columnas de `Text` a `Ref`** en el editor de AppSheet, en los cinco bloques y el orden
que fija `ESPEC-002`. Nada más.

**Fuera de alcance, explícitamente:**

- Retirar `ACT_Activos.FrecuenciaID` o `TIP_TiposActivo.FormularioID` — es Fase C
- Crear cualquier tabla nueva
- Tocar `MAN_Mantenimientos.Precision_GPS` del registro de prueba: vale `45` y está bien
- Poblar los radios de geofencing
- Relajar F-02, ni ninguna otra comprobación, para que algo pase

Esa última no es una advertencia genérica. **Si una comprobación estorba, se endurece o se
sustituye por la inversa; no se retira.** Es `CLAUDE.md` §3 y es lo único que ha parado tres cierres
falsos en este proyecto.

## 4. Quién ejecuta y quién mide

**Quien aplique el cambio no toca las pruebas ni los verificadores.** Ocurrió el 2026-08-07: el
agente que aplicó `ESPEC-001C` editó `verificar_faseA.py` y después anunció que pasaba. Tenía razón
en el fondo y el bucle seguía estando mal.

Si durante la ejecución aparece que una comprobación está equivocada, **se reporta y se detiene**;
no se corrige sobre la marcha por quien está siendo verificado.

## 5. Criterio de cierre

No se declara cerrada por el reporte de quien la ejecutó. Hacen falta las tres cosas:

1. Las **17 pruebas de `PRUEBA-002`** pasadas, incluidas las cuatro innegociables: `P-05`, `P-09`,
   `P-12` y `P-16`.
2. La hoja descargada a `BD/` y `verificar_faseA.py` en **`FASE A CERRADA`** sobre el archivo nuevo.
3. `validar_modelo.py` y `verificar_documentos.py` **sin errores**.

Y un acta, `ACTA-005`, con **qué comando y qué salida** cerró cada punto. Tres veces se reportó un
cierre que no resistió la comprobación contra el archivo; las tres las paró un script.

## 6. Reversión

**AppSheet no tiene deshacer para un cambio de tipo de columna.** La vuelta atrás es volver la
columna a `Text` en el editor, y solo es limpia **si nadie escribió durante la ventana**.

Por eso, antes del primer bloque:

- Descargar la hoja a `BD/` como punto de retorno del dato.
- Que nadie use la aplicación durante la ejecución. Hoy es viable porque no hay técnicos en campo.

**El riesgo real no es el tipo: es el dato.** Si AppSheet convierte mal un valor de clave, la
referencia queda rota sin avisar. Es lo que `F-16` previno normalizando los formatos, y es la razón
de que esta orden llegue después de `ACTA-004` y no antes.

## 7. Lo que esta orden compra

Con las referencias cableadas se desbloquea lo que hoy no se puede ni escribir:

- El geofencing deja de ser decorativo: `[OTID].[ActivoID].[Ubicacion]` pasa a ser navegable
- El filtro por zona puede desreferenciar la unidad funcional del técnico
- `[OTID].[Tipo]`, que `ESPEC-003` necesita para condicionar el formulario de correctivo
- La navegación padre-hijo y los reportes por activo

**Y es el momento más barato.** `MAN_Mantenimientos` tiene 2 filas: convertir su `OTID` hoy no
arrastra prácticamente nada. Después del piloto es una migración.

---

*Emitida contra `ESPEC-002` y su décimo veredicto. La ejecución la registra `ACTA-005`.*
