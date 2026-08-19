# -*- coding: utf-8 -*-
"""Aplica y verifica el bucket y políticas de Supabase Storage para evidencias-sgmc (Paso 8 / ESPEC-013)."""

import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "scripts"))

from verificar_supabase import conectar

def main():
    print("=" * 78)
    print("CONFIGURANDO Y AUDITANDO SUPABASE STORAGE (EVIDENCIAS-SGMC)")
    print("=" * 78)

    con, origen = conectar()
    print(f"Conectado a Supabase por: {origen}\n")
    con.set_session(autocommit=True)
    cur = con.cursor()

    # 1. Leer y aplicar BD/supabase_storage.sql
    storage_sql_path = os.path.join(RAIZ, "BD", "supabase_storage.sql")
    with open(storage_sql_path, "r", encoding="utf-8") as f:
        sql_storage = f.read()

    print("1. Aplicando configuración de bucket y políticas RLS para storage.objects...")
    cur.execute(sql_storage)
    print("   -> OK: Bucket 'evidencias-sgmc' y políticas RLS configuradas.")

    # 2. Verificar existencia del bucket en storage.buckets
    cur.execute("SELECT id, name, public, file_size_limit, allowed_mime_types FROM storage.buckets WHERE id = 'evidencias-sgmc';")
    bucket = cur.fetchone()
    print(f"\n2. Detalle del Bucket en Supabase Storage:")
    print(f"   • ID: {bucket[0]}")
    print(f"   • Nombre: {bucket[1]}")
    print(f"   • Público: {bucket[2]}")
    print(f"   • Límite tamaño archivo: {bucket[3] / (1024*1024):.1f} MB")
    print(f"   • Tipos MIME permitidos: {bucket[4]}")
    assert bucket is not None, "El bucket evidencias-sgmc no fue encontrado!"

    # 3. Verificar políticas RLS en storage.objects
    cur.execute("SELECT policyname, permissive, roles, cmd FROM pg_policies WHERE schemaname = 'storage' AND tablename = 'objects';")
    policies = cur.fetchall()
    print(f"\n3. Políticas RLS en storage.objects ({len(policies)} encontradas):")
    for pol in policies:
        print(f"   • [{pol[3]}] {pol[0]} (Roles: {pol[2]})")

    cur.close()
    con.close()

    print("\n" + "=" * 78)
    print("CONFIGURACIÓN DE SUPABASE STORAGE COMPLETADA CON ÉXITO: 0 FALLOS")
    print("=" * 78)

if __name__ == "__main__":
    main()
