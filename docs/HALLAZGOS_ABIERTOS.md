# Hallazgos abiertos

**Esto no es una especificación y no pasa por el pipeline.** Es la lista de lo que sabemos que está
mal o sin resolver, **y que no merece un documento propio**.

Existe porque hasta hoy todo hallazgo tenía dos destinos: convertirse en especificación, o perderse.
El primero hace que las especificaciones crezcan sin control; el segundo hace que el trabajo de
mirar se tire a la basura. Esta lista es el tercero.

**Regla de entrada.** Un hallazgo se convierte en especificación **solo si nombra qué se rompe en
producción** —«un técnico hará X y pasará Y»— y además exige una decisión de diseño. Si nombra la
rotura pero el arreglo ya está resuelto en otro sitio, se amplía la especificación que ya lo
resuelve. Si no nombra ninguna rotura, se queda aquí.

**Cada entrada trae su comando.** Sin comando no se puede saber si sigue abierta, y una lista que no
se puede verificar envejece igual que una cifra escrita a mano.

---

## La cascada de borrado de `MAN_Mantenimientos`

`FOT_Fotografias.MantenimientoID` lleva `es_parte_de=True`, así que borrar un mantenimiento borraría
en cascada sus fotografías. Y no es solo esa tabla: son **cuatro hijas** —`FOT_Fotografias`,
`FIR_Firmas`, `CHK_Checklists`, y `CHD_ChecklistDetalle` como nieta—.

```bash
python -c "import sys;sys.path.insert(0,'scripts');from modelo_objetivo import MODELO;print([(t,c['nombre'],c['ref']) for t in MODELO for c in MODELO[t]['columnas'] if c.get('es_parte_de')])"
```

**Por qué no es una especificación, y no es por prioridad.** `RG-15` ya retira `Deletes` de
`MAN_Mantenimientos`, y su propia descripción lo dice: *«Protegido aqui arriba, el IsPartOf de FOT,
FIR y CHK nunca llega a dispararse»*. Dentro de la aplicación **no hay botón que borre** una fila
padre.

El residuo real es otro: **borrado a mano en el Sheets**, que dos cuentas tienen permiso para hacer.
Y ahí retirar `IsPartOf` **no arregla nada**, porque un borrado en la hoja no dispara cascada
ninguna: deja huérfanos. Tendría coste sin beneficio.

Queda aquí porque en un sistema cuyo propósito es que la evidencia sea difícil de falsificar, esto
se decide por escrito aunque la decisión sea «no se toca».

## `docs/PROMPT_CABLEADO.md` no es reproducible byte a byte

Su tabla de etiquetas ordena los empates de forma inestable, así que dos regeneraciones seguidas
producen diffs distintos sin que nada haya cambiado.

```bash
python scripts/generar_prompt_cableado.py && git diff --stat docs/PROMPT_CABLEADO.md
```

**Consecuencia práctica:** cualquier orden que regenere ese documento va a traer líneas de diff
espurias. Hay que avisarlo en la orden, para que no se lean como efecto del cambio.

No rompe nada en producción. Rompe la confianza en el `diff`, que es peor de lo que suena cuando el
método entero se apoya en leer de vuelta.

## Qué pasa si `HERE()` no está disponible

Sin señal, o con la ubicación denegada en el dispositivo, no está fijado si `HERE()` deja el campo
**vacío** o escribe **`0, 0`**. No hay página oficial que lo diga y no lo hemos medido.

Importa porque `ESPEC-008` propone `Editable_If = FALSE` sobre esas columnas, y eso **elimina la
única vía de corrección**: con el campo vacío y obligatorio, el técnico no puede guardar; con `0, 0`,
queda una evidencia falsa e incorregible.

**Es medible barato**, en la misma sesión de editor: abrir el formulario con la ubicación denegada y
mirar. Está en la tabla de supuestos sin verificar de `docs/BASE_CONOCIMIENTO_APPSHEET.md`.

## No hay comando que diga qué tipos quedaron pendientes en el editor

`inferencia.clasificar()` responde *qué columnas necesitan mano*, no *en cuáles ya pasó alguien*. La
API devuelve filas, no esquema.

```bash
python -c "import sys;sys.path.insert(0,'scripts');from inferencia import clasificar;print({k:len(v) for k,v in clasificar().items()})"
```

Por eso `ESTADO.md` dice «unas 24 de 28 tablas» y no las nombra: nombrarlas sería inventar. La única
evidencia de qué se tocó son las actas de `docs/sdd/`.

Es el mismo límite que hace que **11 de los 13 pasos** de `docs/LO_QUE_SE_HACE_A_MANO.md` no tengan
ningún verificador.
