# Histórico — documentos que ya no aplican

**Nada de esta carpeta describe el sistema actual.** Son documentos de etapas cerradas, y se
conservan por una razón: explican **por qué** se decidió lo que hay hoy.

Cuando alguien pregunte «¿por qué se reconstruyó la aplicación en vez de repararla?» o «¿por qué el
QR quedó fuera de alcance?», la respuesta está aquí.

**El estado vigente está en [`ESTADO.md`](../../ESTADO.md).**

`verificar_documentos.py` **no revisa esta carpeta**: describe estados superados a propósito, y
corregirla borraría la trazabilidad que justifica conservarla.

## Qué hay

| Documento | De qué etapa es |
|---|---|
| `ENTREGA_TECNICA_SGMC.md` | Reparar la app existente tabla por tabla. Se abandonó al comprobar que AppSheet no admite un cambio de esquema de ese tamaño |
| `CABLEADO_REFERENCIAS_SGMC.md` | Primer análisis del defecto raíz de las referencias |
| `DICTAMEN_AUDITORIA_LOCAL_SGMC.md` | Auditoría del 2026-08-06 |
| `AUDITORIA_PLAN_Y_ROADMAP.md` | Dictamen del 2026-08-06 sobre `plan_de_trabajo.md` y la versión de entonces de `ROADMAP.md`, contra un libro de 24 hojas. **Sus hallazgos `B-01` a `B-14` son el origen de casi todo lo que se decidió después**, y por eso se cita todavía por ese código |
| `INFORME_QA_ISTQB_Y_AUDITORIA_ARQUITECTO.md` | Revisión de calidad de la etapa anterior |
| `PROMPT_AGENTE_HOJA_*.md` | Prompts de la Fase A, ejecutados y cerrados con sus actas |
| `PROMPT_CONSTRUCCION_SGMC.md` | Construcción inicial de la aplicación que se reemplazó |
| `especificaciones*.md`, `plan_de_trabajo.md` | Documentos previos a que `modelo_objetivo.py` fuera la fuente única |
| `DEFINICION_FUNCIONAL_MESA_DE_TRABAJO.md` | Las 14 decisiones enviadas al líder funcional |
| `ESPEC-001-preparacion-del-sheets.md` | Fase A: preparar a mano el Sheets de `SGMC-886843353`. Ejecutada y cerrada. Hoy la hoja se genera del modelo |
| `ESPEC-001B-cierre-de-la-fase-a.md` | Los 19 fallos que faltaban para cerrar la Fase A. Ejecutada y cerrada |
| `ESPEC-001C-baja-de-activos-y-datos-de-prueba.md` | Baja de activos y poblado de prueba sobre esa misma hoja. Ejecutada y cerrada |
| `ORDEN-002-ejecucion-fase-b.md` | Autorizaba convertir 15 columnas en `SGMC-886843353`. Esa aplicación se abandonó y la orden nunca se cerró: no hay `ACTA-005` |
| `MANUAL_DE_USUARIO_ILUSTRADO.md` | Manual con maquetas de pantalla del flujo antiguo con QR. Retirado de `Manuales/` el 2026-08-09. El manual vigente es [`Manuales/MANUAL_DE_USUARIO.md`](../../Manuales/MANUAL_DE_USUARIO.md) |
| `Manual_de_Usuario_SGMC_Con_Diagramas.docx` | El mismo manual en Word, con los mismos diagramas de QR y las tildes corruptas en sus imágenes. Nunca se entregó. Lo genera `scripts/generate_user_manual_docx.py`, que **no debe volver a correrse** hasta rehacer el manual |
| `images_manual/` | Las seis maquetas `img_01` a `img_06` de esos dos manuales. Ilustran el flujo antiguo con QR y la codificación de sus rótulos está rota |

**Las actas `ACTA-001` a `ACTA-004` no están aquí.** Un acta registra un hecho fechado y no caduca:
siguen en [`docs/sdd/`](../sdd/), cada una con una nota de lo que después resultó falso.
