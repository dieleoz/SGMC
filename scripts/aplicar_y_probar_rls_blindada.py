# -*- coding: utf-8 -*-
"""Aplica y prueba el blindaje estricto de RLS (Paso 6 / ESPEC-012).

Prueba el aislamiento de datos para cada sujeto simulando su JWT:
1. Administrador (Diego Zúñiga): 368 activos, 111 órdenes.
2. Supervisor 4 UFs (Fernand Bolívar): 368 activos, 111 órdenes.
3. Técnico UF1 (Iván Salcedo): 146 activos, 23 órdenes.
4. Técnico UF3 (Edinson Morales): 45 activos, 34 órdenes.
"""

import os
import sys
import json

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "scripts"))

from verificar_supabase import conectar

def probar_consulta_como_usuario(cur, email, nombre):
    cur.execute("BEGIN;")
    cur.execute("SET LOCAL role = 'authenticated';")
    claims = json.dumps({"email": email, "role": "authenticated"})
    cur.execute(f"SET LOCAL \"request.jwt.claims\" = '{claims}';")
    
    # Consultar sgmc_rol y sgmc_usuario_id
    cur.execute("SELECT public.sgmc_rol(), public.sgmc_usuario_id();")
    rol, uid = cur.fetchone()
    
    # Consultar UFs asignadas
    cur.execute("SELECT array_agg(\"UnidadFuncionalID\") FROM public.sgmc_unidades();")
    ufs = cur.fetchone()[0]

    # Consultar Activos visibles
    cur.execute('SELECT count(*) FROM public."ACT_Activos";')
    count_activos = cur.fetchone()[0]

    # Consultar Órdenes visibles
    cur.execute('SELECT count(*) FROM public."OT_OrdenesTrabajo";')
    count_ots = cur.fetchone()[0]

    # Consultar Mantenimientos visibles
    cur.execute('SELECT count(*) FROM public."MAN_Mantenimientos";')
    count_mans = cur.fetchone()[0]

    cur.execute("ROLLBACK;")

    print(f"\n--- Probando como: {nombre} ({email}) ---")
    print(f"   • Rol detectado: {rol} | UsuarioID: {uid} | UFs: {ufs}")
    print(f"   • Activos visibles: {count_activos} (de 368)")
    print(f"   • Órdenes visibles: {count_ots} (de 111)")
    print(f"   • Mantenimientos visibles: {count_mans} (de 113)")

    return {
        "email": email,
        "rol": rol,
        "uid": uid,
        "activos": count_activos,
        "ots": count_ots,
        "mans": count_mans
    }

def main():
    print("=" * 78)
    print("APLICANDO Y VERIFICANDO BLINDAJE ESTRICTO DE POLÍTICAS RLS (PASO 6)")
    print("=" * 78)

    con, origen = conectar()
    print(f"Conectado a Supabase por: {origen}\n")
    con.set_session(autocommit=True)
    cur = con.cursor()

    # 1. Aplicar nuevo script RLS
    print("1. Aplicando BD/supabase_rls_politicas.sql...")
    sql_path = os.path.join(RAIZ, "BD", "supabase_rls_politicas.sql")
    with open(sql_path, "r", encoding="utf-8") as f:
        rls_sql = f.read()
    cur.execute(rls_sql)
    print("   -> OK: Políticas RLS aplicadas.")

    # 2. Probar como Administrador (Diego Zúñiga)
    res_admin = probar_consulta_como_usuario(cur, "diego.zuniga@grupoortiz.com", "Diego Zúñiga (Administrador)")
    assert res_admin["activos"] == 368, f"Admin debió ver 368 activos, vio {res_admin['activos']}"
    assert res_admin["ots"] == 111, f"Admin debió ver 111 órdenes, vio {res_admin['ots']}"

    # 3. Probar como Supervisor 4 UFs (Fernand Bolívar)
    res_sup = probar_consulta_como_usuario(cur, "fernand.bolivar@concesiondelsisga.com.co", "Fernand Bolívar (Supervisor 4 UFs)")
    assert res_sup["activos"] == 368, f"Supervisor debió ver 368 activos, vio {res_sup['activos']}"
    assert res_sup["ots"] == 111, f"Supervisor debió ver 111 órdenes, vio {res_sup['ots']}"

    # 4. Probar como Técnico UF1 (Iván Salcedo)
    res_ivan = probar_consulta_como_usuario(cur, "ivan.salcedo@concesiondelsisga.com.co", "Iván Salcedo (Técnico UF1)")
    assert res_ivan["activos"] == 146, f"Iván debió ver 146 activos (UF1), vio {res_ivan['activos']}"
    assert res_ivan["ots"] == 23, f"Iván debió ver 23 órdenes, vio {res_ivan['ots']}"

    # 5. Probar como Técnico UF3 (Edinson Morales)
    res_edinson = probar_consulta_como_usuario(cur, "edinson.morales@concesiondelsisga.com.co", "Edinson Morales (Técnico UF3)")
    assert res_edinson["activos"] == 45, f"Edinson debió ver 45 activos (UF3), vio {res_edinson['activos']}"
    assert res_edinson["ots"] == 34, f"Edinson debió ver 34 órdenes, vio {res_edinson['ots']}"

    cur.close()
    con.close()

    print("\n" + "=" * 78)
    print("TODAS LAS PRUEBAS DE BLINDAJE RLS PASARON CON ÉXITO: 0 FALLOS")
    print("=" * 78)

if __name__ == "__main__":
    main()
