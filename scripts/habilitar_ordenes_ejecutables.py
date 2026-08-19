# -*- coding: utf-8 -*-
"""Inspecciona y habilita órdenes de trabajo ejecutables ('Asignada') para Iván Salcedo."""

import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "scripts"))

from verificar_supabase import conectar

def main():
    con, _ = conectar()
    con.set_session(autocommit=True)
    cur = con.cursor()

    cur.execute('''
        SELECT ot."OTID", ot."ActivoID", a."Nombre", a."UnidadFuncionalID", a."Ubicacion_LatLong", ot."EstadoOrdenID"
        FROM public."OT_OrdenesTrabajo" ot
        JOIN public."ACT_Activos" a ON ot."ActivoID" = a."ActivoID"
        WHERE ot."TecnicoID" = 'USR-004'
        LIMIT 10;
    ''')
    filas = cur.fetchall()
    print("Órdenes de Iván Salcedo (USR-004):")
    for f in filas:
        print(f)

    # Actualizar las primeras 5 órdenes a 'Asignada'
    cur.execute('''
        UPDATE public."OT_OrdenesTrabajo"
        SET "EstadoOrdenID" = 'Asignada'
        WHERE "OTID" IN (
            SELECT ot."OTID"
            FROM public."OT_OrdenesTrabajo" ot
            WHERE ot."TecnicoID" = 'USR-004'
            LIMIT 5
        );
    ''')
    print("5 órdenes de USR-004 actualizadas a 'Asignada'.")

    cur.execute('''
        SELECT "EstadoOrdenID", count(*) 
        FROM public."OT_OrdenesTrabajo" 
        GROUP BY "EstadoOrdenID";
    ''')
    print("Nueva distribución de estados:", cur.fetchall())

    cur.close()
    con.close()

if __name__ == "__main__":
    main()
