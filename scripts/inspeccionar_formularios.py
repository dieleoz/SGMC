# -*- coding: utf-8 -*-
"""Inspecciona los 27 formularios, secciones, 333 preguntas y 108 valores de lista."""

import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "scripts"))

from verificar_supabase import conectar

def main():
    con, _ = conectar()
    cur = con.cursor()

    cur.execute('SELECT "TipoRespuestaID", "Nombre" FROM public."TPR_TiposRespuesta";')
    print("Tipos de Respuesta disponibles:")
    for row in cur.fetchall():
        print(f"   • {row[0]}: {row[1]}")

    cur.execute('SELECT "FormularioID", "Nombre", "Version" FROM public."FRM_Formularios" ORDER BY "FormularioID" LIMIT 10;')
    print("\nPrimeros 10 Formularios:")
    for row in cur.fetchall():
        print(f"   • {row[0]}: {row[1]} (v{row[2]})")

    cur.execute('''
        SELECT t."TipoActivoID", t."Nombre", t."FormularioID", f."Nombre" as FormNombre, count(p."PreguntaID") as TotalPreguntas
        FROM public."TIP_TiposActivo" t
        JOIN public."FRM_Formularios" f ON t."FormularioID" = f."FormularioID"
        LEFT JOIN public."FRM_Preguntas" p ON f."FormularioID" = p."FormularioID"
        GROUP BY t."TipoActivoID", t."Nombre", t."FormularioID", f."Nombre"
        ORDER BY t."TipoActivoID";
    ''')
    print("\nTipos de Activos vinculados a Formularios y Conteo de Preguntas:")
    for row in cur.fetchall():
        print(f"   • {row[0]} ({row[1]}) -> Form: {row[2]} ({row[3]}) | {row[4]} preguntas")

    cur.execute('''
        SELECT p."PreguntaID", p."Pregunta", p."TipoRespuestaID", s."Nombre" as Seccion, p."Obligatoria", p."Unidad"
        FROM public."FRM_Preguntas" p
        JOIN public."FRM_Secciones" s ON p."SeccionID" = s."SeccionID"
        WHERE p."FormularioID" = 'FRM_SOS'
        ORDER BY p."Orden";
    ''')
    print("\nPreguntas del Formulario FRM_SOS (Poste SOS):")
    for row in cur.fetchall():
        print(f"   • [{row[0]}] ({row[3]}) {row[1]} | Tipo: {row[2]} | Oblig: {row[4]} | Unidad: {row[5]}")

    cur.execute('''
        SELECT v."PreguntaID", p."Pregunta", array_agg(v."Valor" ORDER BY v."Orden") as Opciones
        FROM public."LST_ValoresLista" v
        JOIN public."FRM_Preguntas" p ON v."PreguntaID" = p."PreguntaID"
        GROUP BY v."PreguntaID", p."Pregunta"
        LIMIT 10;
    ''')
    print("\nPreguntas con Valores de Lista (LST_ValoresLista):")
    for row in cur.fetchall():
        print(f"   • [{row[0]}] {row[1]}: {row[2]}")

    cur.close()
    con.close()

if __name__ == "__main__":
    main()
