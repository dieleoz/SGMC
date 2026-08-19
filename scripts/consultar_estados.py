# -*- coding: utf-8 -*-
from verificar_supabase import conectar

con, _ = conectar()
cur = con.cursor()
cur.execute('SELECT "EstadoOrdenID", "Nombre" FROM public."EOT_EstadosOrden";')
print("EOT_EstadosOrden:", cur.fetchall())
cur.execute('SELECT "EstadoActivoID", "Nombre" FROM public."EST_Activo";')
print("EST_Activo:", cur.fetchall())
cur.execute('SELECT "EstadoOrdenID", count(*) FROM public."OT_OrdenesTrabajo" GROUP BY "EstadoOrdenID";')
print("Distribución OT_OrdenesTrabajo:", cur.fetchall())
cur.execute('SELECT "UsuarioID", "Nombre", "Correo", "RolID" FROM public."USR_Usuarios";')
print("Usuarios:", cur.fetchall())
cur.close()
con.close()
