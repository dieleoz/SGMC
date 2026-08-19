# -*- coding: utf-8 -*-
import sys, os, uuid
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verificar_supabase import conectar

con, _ = conectar()
con.autocommit = True
cur = con.cursor()

# Verificar o crear dieleoz@gmail.com
cur.execute('SELECT id FROM auth.users WHERE email = %s;', ('dieleoz@gmail.com',))
row = cur.fetchone()

if not row:
    user_id = str(uuid.uuid4())
    cur.execute("""
        INSERT INTO auth.users 
        (id, instance_id, email, encrypted_password, email_confirmed_at, raw_app_meta_data, raw_user_meta_data, created_at, updated_at, aud, role)
        VALUES 
        (%s, '00000000-0000-0000-0000-000000000000', 'dieleoz@gmail.com', crypt('Sisga2026*', gen_salt('bf')), now(), '{"provider":"email","providers":["email"]}', '{"name":"Diego Zuniga"}', now(), now(), 'authenticated', 'authenticated');
    """, (user_id,))
    print("Usuario dieleoz@gmail.com creado en auth.users con ID:", user_id)
else:
    cur.execute("UPDATE auth.users SET encrypted_password = crypt('Sisga2026*', gen_salt('bf')), email_confirmed_at = now() WHERE email = %s;", ('dieleoz@gmail.com',))
    print("Usuario dieleoz@gmail.com actualizado.")

cur.execute('SELECT email, email_confirmed_at FROM auth.users ORDER BY email;')
for r in cur.fetchall():
    print(f"• {r[0]:<45} | Clave: Sisga2026* | Confirmado: {bool(r[1])}")

cur.close()
con.close()
