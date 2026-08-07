---
name: verificar-documentos
description: Comprueba que la prosa del repositorio no contradiga al modelo de datos, y decide si una tabla o un mecanismo nuevo hace falta o ya existe. Úsala ANTES de proponer una tabla, una columna o un mecanismo, y siempre después de escribir o tocar un .md.
---

# Verificar documentos contra el modelo

Este proyecto no falla por descuido. Falla porque **los documentos se escriben leyendo otros
documentos** en vez de volcar el modelo. Tres ejemplos reales, ninguno detectado por una persona
leyendo:

- `bd.md` decía «24 hojas» cuando había 32.
- El manual mandaba editar `CHD_ChecklistDetalle` para cambiar preguntas. Esa tabla guarda
  **respuestas**: seguir la instrucción reescribe el histórico de mantenimientos.
- Se propusieron como tablas nuevas `ROL_Roles`, `FRM_Formularios`, `FRM_Secciones` y
  `FRM_Preguntas`. Las cuatro ya estaban en el modelo.

## Antes de proponer cualquier cosa

**Vuelca el modelo. No lo recuerdes.**

```bash
python -c "import sys; sys.path.insert(0,'scripts'); from modelo_objetivo import MODELO, PROPUESTAS; print(sorted(MODELO)); print(sorted(PROPUESTAS))"
```

Tres preguntas, en este orden:

1. **¿La tabla ya existe en `MODELO`?** Si sí, se usa. No se crea otra.
2. **¿Ya está declarada en `PROPUESTAS`?** Si sí, **usa exactamente ese nombre**. Dos nombres para
   la misma tabla en dos documentos es el fallo más caro y el más fácil de cometer: pasó el
   2026-08-07 con `EST_Estructuras`/`ETR_Estructuras` y `PAU_Pausas`/`EVT_EventosOrden`, el mismo
   día, en dos documentos escritos con horas de diferencia.
3. **¿Hay ya un mecanismo para ese propósito en `DECISIONES`?** Si lo hay, se usa el elegido. Si el
   nuevo es mejor, **se retira el viejo en el mismo cambio** y se anota. Nunca conviven los dos.

Si de verdad hace falta algo nuevo, **decláralo en `PROPUESTAS` con su motivo y dónde se
especifica**, antes de escribirlo en ningún `.md`.

## Después de escribir

```bash
python scripts/verificar_documentos.py
```

| Regla | Qué comprueba |
|---|---|
| D-01 | Toda tabla citada existe en `MODELO`, `RETIRADAS` o `PROPUESTAS` |
| D-02 | Ninguna tabla `PROPUESTA` existe ya en `MODELO` |
| D-03 | Toda referencia `Tabla.Columna` apunta a una columna real |
| D-04 | Ningún mecanismo descartado sigue vivo sin fecha de retiro |
| D-05 | Toda tabla del modelo la menciona algún documento |

## Los dos límites, y hay que tenerlos presentes

**No comprueba si la prosa es cierta.** Solo si sus nombres existen. Un documento puede pasar las
cinco reglas y estar equivocado de arriba abajo. Por eso sigue haciendo falta el arquitecto, y por
eso «los scripts pasan» nunca sustituye a un veredicto.

**No ve columnas listadas en celdas separadas de una tabla markdown.** Si una especificación declara
columnas nuevas en una tabla de dos columnas —nombre en una celda, tipo en otra—, D-03 no las
alcanza. Pasar el verificador **no prueba que las columnas nuevas sean correctas**.

## Cuando un documento menciona un nombre para descartarlo

Declara la salida, en el propio documento:

```
<!-- verificar_documentos: ignorar EST_Estructuras -->
```

Es incómoda a propósito y es greppable. **Si aparece en muchos sitios, el problema es el criterio y
no el documento.**

## Qué hacer con cada fallo

- **D-01** — o la tabla hace falta y va a `PROPUESTAS` con su motivo, o el documento está citando
  algo que no existe y hay que corregir el documento. Nunca se calla añadiéndola a la lista de
  excepciones.
- **D-03** — casi siempre es el documento el que se equivoca. Comprueba la columna con un volcado
  antes de tocar nada.
- **D-04** — si un mecanismo descartado sigue vivo, o se retira o se declara en qué paso se retira.
  Dejarlo sin fecha es como no haber decidido.
- **D-05** — una tabla que nadie explica es una tabla que nadie usa. Puede ser que sobre.
