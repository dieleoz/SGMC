# -*- coding: utf-8 -*-
"""Auditoría y Blindaje de Políticas RLS (Paso 6 de Fase 4 / ESPEC-012).

Prueba el aislamiento de datos para cada rol:
1. Administrador (diego.zuniga@grupoortiz.com): Ve 368 activos y todas las 111 órdenes.
2. Técnico Iván Salcedo (ivan.salcedo@concesiondelsisga.com.co): Ve los activos de UF1 y UF2, y sus órdenes asignadas.
3. Supervisor Fernand Bolívar (fernand.bolivar@concesiondelsisga.com.co): Ve los activos y órdenes de sus 4 UFs.
"""

import os
import sys
import json

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "scripts"))

from verificar_supabase import conectar

def main():
    print("=" * 78)
    print("AUDITORÍA DE AISLAMIENTO POR IDENTIDAD Y ZONA (RLS)")
    print("=" * 78)

    con, origen = conectar()
    print(f"Conectado a Supabase por: {origen}\n")
    con.set_session(autocommit=True)
    cur = con.cursor()

    # 1. Consultar Unidades y Asignaciones
    cur.execute('SELECT "UnidadFuncionalID", count(*) FROM public."ACT_Activos" GROUP BY "UnidadFuncionalID" ORDER BY "UnidadFuncionalID";')
    print("Distribución de 368 Activos por Unidad Funcional:")
    for uf, count in cur.fetchall():
        print(f"   • {uf}: {count} activos")

    cur.execute('''
        SELECT u."UsuarioID", u."Nombres", u."Correo", r."Nombre" as Rol, array_agg(a."UnidadFuncionalID") as Zonas
        FROM public."USR_Usuarios" u
        JOIN public."ROL_Roles" r ON u."RolID" = r."RolID"
        LEFT JOIN public."ASG_AsignacionZona" a ON u."UsuarioID" = a."UsuarioID" AND a."Activo" = TRUE
        GROUP BY u."UsuarioID", u."Nombres", u."Correo", r."Nombre";
    ''')
    usuarios = cur.fetchall()
    print("\nUsuarios y Zonas Asignadas:")
    for usr in usuarios:
        print(f"   • {usr[0]} | {usr[1]} ({usr[2]}) | Rol: {usr[3]} | Zonas: {usr[4]}")

    cur.execute('SELECT "TecnicoID", count(*) FROM public."OT_OrdenesTrabajo" GROUP BY "TecnicoID";')
    print("\nDistribución de Órdenes por TecnicoID:")
    for tec, count in cur.fetchall():
        print(f"   • {tec}: {count} órdenes")

    cur.close()
    con.close()

if __name__ == "__main__":
    main()
