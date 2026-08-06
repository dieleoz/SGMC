---
name: generar-entregables
description: Regenera las figuras y los documentos Word del SGMC desde sus generadores en scripts/. Úsala cuando cambie el contenido de un entregable, cuando haya que corregir una figura, o antes de enviar algo al cliente.
---

# Regenerar los entregables del SGMC

Los documentos Word y las figuras **no se editan a mano**: se generan desde `scripts/`. Editar el
`.docx` directamente hace que el generador y el archivo diverjan, que es exactamente el problema
que este proyecto ya tiene con el modelo de datos.

## Cadena de generación

```
scripts/generate_figuras.py              -> docs/images/fig_01..07.png
scripts/generate_especificaciones_docx.py -> entregables/Especificaciones_Tecnicas_SGMC_AsBuilt.docx
scripts/generate_mesa_trabajo_docx.py     -> entregables/Definicion_Funcional_SGMC_Mesa_de_Trabajo.docx
scripts/generate_user_manual_docx.py      -> Manuales/Manual_de_Usuario_SGMC_Con_Diagramas.docx
```

Las figuras van primero: los dos primeros documentos las incrustan.

```bash
python scripts/generate_figuras.py
python scripts/generate_especificaciones_docx.py
python scripts/generate_mesa_trabajo_docx.py
```

`scripts/_helpers_docx.py` tiene las utilidades de composición compartidas. Asigna
`H.IMG` antes de llamar a `figura()`.

## Reglas

- **Sin emojis ni iconos** en documentos, mensajes de error y textos de interfaz.
- Español con tildes correctas. Verifica después de generar: las maquetas viejas de
  `Manuales/images/` tienen la codificación rota (`M?VIL`, `DIN?MICO`) y no deben usarse.
- Rutas relativas a la raíz del repositorio, nunca `D:\...`:
  `RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))`.
- Si un contenido vive a la vez en un `.md` y en un `.docx`, **genera el `.md` desde los mismos
  datos del script**. No los mantengas a mano en paralelo.

## Antes de dar por bueno un documento

```bash
python -c "
from docx import Document; import os, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
f = 'entregables/NOMBRE.docx'
d = Document(f)
print('Parrafos:', len(d.paragraphs), '| Tablas:', len(d.tables),
      '| Imagenes:', len(d.inline_shapes), '|', round(os.path.getsize(f)/1024), 'KB')
"
```

Comprueba que el número de imágenes sea el esperado: si una figura falta, `figura()` lo avisa por
consola pero el documento se genera igual, sin ella.

Revisa también las figuras nuevas abriéndolas: los solapamientos y los textos que se salen del
lienzo solo se ven mirando. El generador no los detecta.

## Errores conocidos

- **Word bloquea el archivo.** Si el `.docx` está abierto, la escritura falla con
  `PermissionError` y aparece un `~$...` en la carpeta. Ciérralo y repite.
- **Escapes en heredoc.** No edites estos scripts con `bash <<EOF`: los `\n` dentro de literales se
  convierten en saltos reales y rompen el archivo. Usa las herramientas de edición.

## Coherencia final

Si cambia la estructura de carpetas o se agrega un documento, actualiza `MAP.md` y la tabla de
`README.md`, y comprueba que no queden enlaces rotos:

```bash
python -c "
import io, os, re, glob
rotos = []
for f in glob.glob('**/*.md', recursive=True):
    if f.startswith('archivo'): continue
    base = os.path.dirname(f)
    for m in re.findall(r'\]\(([^)#]+?)\)', io.open(f, encoding='utf-8').read()):
        if m.startswith(('http', 'mailto', '#')): continue
        if not os.path.exists(os.path.normpath(os.path.join(base, m))): rotos.append((f, m))
print('Enlaces rotos:', rotos if rotos else 'ninguno')
"
```
