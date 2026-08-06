# -*- coding: utf-8 -*-
"""Genera los esquemas del documento de mesa de trabajo SGMC.
Supersampling x2 + LANCZOS para bordes y texto limpios."""
import os
from PIL import Image, ImageDraw, ImageFont

OUT = r"D:\@Proyect\Sisga\Manuales\images"
S = 2  # factor de supersampling

FONTS = r"C:\Windows\Fonts"
def F(name, size):
    for f in (name, "segoeui.ttf", "arial.ttf"):
        p = os.path.join(FONTS, f)
        if os.path.exists(p):
            return ImageFont.truetype(p, size * S)
    return ImageFont.load_default()

REG = lambda s: F("segoeui.ttf", s)
BOLD = lambda s: F("segoeuib.ttf", s)
SEMI = lambda s: F("seguisb.ttf", s)

# Paleta
TINTA   = (28, 37, 48)
GRIS    = (110, 122, 134)
LINEA   = (203, 211, 219)
FONDO   = (255, 255, 255)
SUAVE   = (244, 246, 248)
AZUL    = (31, 91, 153)
AZUL_S  = (226, 236, 246)
AMBAR   = (176, 112, 12)
AMBAR_S = (253, 243, 222)
ROJO    = (168, 45, 45)
ROJO_S  = (251, 233, 233)
VERDE   = (32, 116, 84)
VERDE_S = (228, 243, 237)


class Lienzo:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.img = Image.new("RGB", (w * S, h * S), FONDO)
        self.d = ImageDraw.Draw(self.img)

    def caja(self, x, y, w, h, relleno=SUAVE, borde=LINEA, r=6, grosor=1):
        self.d.rounded_rectangle([x*S, y*S, (x+w)*S, (y+h)*S], radius=r*S,
                                 fill=relleno, outline=borde, width=grosor*S)

    def txt(self, x, y, s, font, color=TINTA, anchor="la"):
        self.d.text((x*S, y*S), s, font=font, fill=color, anchor=anchor)

    def parrafo(self, x, y, s, font, color=TINTA, ancho=40, interlinea=14):
        import textwrap
        for i, ln in enumerate(textwrap.wrap(s, ancho)):
            self.txt(x, y + i*interlinea, ln, font, color)
        return y + len(textwrap.wrap(s, ancho)) * interlinea

    def flecha(self, x1, y1, x2, y2, color=GRIS, grosor=2, cabeza=7):
        self.d.line([x1*S, y1*S, x2*S, y2*S], fill=color, width=grosor*S)
        import math
        a = math.atan2(y2-y1, x2-x1)
        for s_ in (-1, 1):
            self.d.line([x2*S, y2*S,
                         (x2 - cabeza*math.cos(a + s_*0.45))*S,
                         (y2 - cabeza*math.sin(a + s_*0.45))*S],
                        fill=color, width=grosor*S)

    def linea(self, x1, y1, x2, y2, color=LINEA, grosor=1):
        self.d.line([x1*S, y1*S, x2*S, y2*S], fill=color, width=grosor*S)

    def titulo(self, t, sub=None):
        self.txt(30, 24, t, BOLD(15), TINTA)
        if sub:
            self.txt(30, 46, sub, REG(10), GRIS)
        self.linea(30, 66, self.w-30, 66, LINEA)

    def guardar(self, nombre):
        self.img.resize((self.w, self.h), Image.LANCZOS).save(os.path.join(OUT, nombre))
        print("  generado:", nombre)


def etiqueta(L, x, y, texto, color_txt, color_fondo):
    f = SEMI(8)
    w = L.d.textlength(texto, font=f) / S + 14
    L.caja(x, y, w, 17, color_fondo, color_fondo, r=8)
    L.txt(x + 7, y + 4, texto, f, color_txt)
    return w


# ---------------------------------------------------------------- FIGURA 1
def fig_actores():
    L = Lienzo(1000, 420)
    L.titulo("Figura 1. Actores del sistema y alcance de cada uno",
             "Quien hace que, desde donde, y con que restriccion de datos")

    acts = [
        ("TECNICO", "Celular, en vía", AZUL, AZUL_S,
         ["Recibe la orden de trabajo asignada", "Escanea el QR del activo",
          "Responde el checklist de inspección", "Toma fotografías y firma",
          "Cierra validando su posición GPS"],
         "Trabaja sin señal.\nSincroniza al recuperarla."),
        ("SUPERVISOR", "Navegador, CCO", VERDE, VERDE_S,
         ["Programa y asigna las órdenes", "Revisa la evidencia recibida",
          "Aprueba o devuelve al técnico", "Consulta el tablero de la zona",
          "Recibe la alerta de fuera de servicio"],
         "Ve su zona.\nCierra las órdenes."),
        ("ADMINISTRADOR", "Navegador", AMBAR, AMBAR_S,
         ["Gestiona usuarios y roles", "Mantiene el inventario de activos",
          "Define los formularios de inspección", "Administra los catálogos",
          "Publica los cambios a los técnicos"],
         "Ve todo.\nAutoriza cambios."),
        ("CONSULTA", "Navegador", GRIS, SUAVE,
         ["Consulta información", "Exporta reportes", "No modifica nada", "", ""],
         "Solo lectura.\n¿Interventoría entra aquí? D-13"),
    ]

    x0, ancho, sep = 30, 228, 15
    for i, (nom, donde, c, cs, tareas, nota) in enumerate(acts):
        x = x0 + i * (ancho + sep)
        L.caja(x, 90, ancho, 250, FONDO, LINEA, r=8)
        L.caja(x, 90, ancho, 44, cs, cs, r=8)
        L.d.rectangle([x*S, 120*S, (x+ancho)*S, 134*S], fill=cs)
        L.txt(x + 14, 100, nom, BOLD(11), c)
        L.txt(x + 14, 117, donde, REG(9), GRIS)
        yy = 148
        for t in tareas:
            if not t:
                continue
            L.d.ellipse([(x+15)*S, (yy+5)*S, (x+19)*S, (yy+9)*S], fill=c)
            L.parrafo(x + 26, yy, t, REG(9), TINTA, ancho=30, interlinea=12)
            yy += 12 * (1 + t.count(" ") // 6) + 10
        L.linea(x + 14, 300, x + ancho - 14, 300, LINEA)
        for j, ln in enumerate(nota.split("\n")):
            L.txt(x + 14, 308 + j*13, ln, SEMI(9), c)

    L.txt(30, 360, "Restricción transversal: cada usuario descarga únicamente los activos de su zona (Security Filter).", SEMI(10), TINTA)
    L.txt(30, 378, "Hoy esa regla dejaría a todos los técnicos con cero activos. Es la decisión D-03.", REG(10), ROJO)
    L.guardar("fig_01_actores.png")


# ---------------------------------------------------------------- FIGURA 2
def fig_flujo_tecnico():
    L = Lienzo(1000, 560)
    L.titulo("Figura 2. Flujo del técnico en campo (CU-01)",
             "El ciclo que justifica el sistema. En ámbar, los puntos que dependen de una decisión pendiente")

    pasos = [
        ("1", "Sincroniza", "Con señal, al\niniciar jornada", None),
        ("2", "Llega al activo", "Ya sin señal,\nopera en caché", None),
        ("3", "Escanea el QR", "o abre la OT\nasignada", None),
        ("4", "Abre el checklist", "Según el tipo\nde activo", "D-09"),
        ("5", "Responde y\nfotografía", "Checklist,\nfotos, firma", "D-10"),
        ("6", "Cierra con GPS", "Valida distancia\nal activo", "D-01"),
        ("7", "Cola local", "Guardado\noffline", None),
        ("8", "Sincroniza", "Sube solo, al\nrecuperar señal", None),
    ]
    x0, w, sep, y = 30, 106, 17, 96
    for i, (n, tit, sub, dec) in enumerate(pasos):
        x = x0 + i * (w + sep)
        pend = dec is not None
        L.caja(x, y, w, 92, AMBAR_S if pend else SUAVE, AMBAR if pend else LINEA, r=7)
        L.d.ellipse([(x+9)*S, (y+9)*S, (x+25)*S, (y+25)*S], fill=AMBAR if pend else AZUL)
        L.txt(x + 17, y + 12, n, BOLD(9), FONDO, anchor="ma")
        for j, ln in enumerate(tit.split("\n")):
            L.txt(x + 9, y + 33 + j*13, ln, BOLD(10), TINTA)
        for j, ln in enumerate(sub.split("\n")):
            L.txt(x + 9, y + 60 + j*12, ln, REG(8), GRIS)
        if pend:
            L.txt(x + w - 9, y + 8, dec, BOLD(8), AMBAR, anchor="ra")
        if i < len(pasos) - 1:
            L.flecha(x + w + 2, y + 46, x + w + sep - 3, y + 46)

    L.txt(30, 214, "Excepciones que hoy no tienen respuesta definida", BOLD(12), TINTA)
    exc = [
        ("E-02", "El GPS no fija posición o su precisión es mala (túnel, cañón, copa densa)",
         "Hoy bloquearía el guardado y el técnico perdería una hora de trabajo. ¿Cierre con excepción supervisada o bloqueo estricto?", "D-04", ROJO, ROJO_S),
        ("E-04", "El técnico llega pero no puede terminar: falta repuesto, lluvia, acceso cerrado",
         "Es el caso más común en la operación real. Si no se modela, el técnico fuerza un cierre falso o no registra nada.", "D-07", ROJO, ROJO_S),
        ("E-03", "Se agota la batería o lo interrumpen a mitad del formulario",
         "Una inspección de poste SOS son 15 preguntas más fotografías. Perderlas devuelve al técnico al papel.", "D-05", AMBAR, AMBAR_S),
        ("E-05", "Encuentra en vía un activo que no está en el inventario",
         "No hay ruta para reportarlo. ¿El técnico puede levantar una novedad para que el supervisor la apruebe?", "D-08", AMBAR, AMBAR_S),
        ("E-06", "Dos técnicos registran trabajo sobre la misma orden",
         "Sin ciclo de vida de la orden no hay regla que lo impida ni que lo resuelva.", "D-06", AMBAR, AMBAR_S),
    ]
    yy = 240
    for cod, sit, imp, dec, c, cs in exc:
        L.caja(30, yy, 940, 56, FONDO, LINEA, r=6)
        L.caja(30, yy, 5, 56, c, c, r=2)
        L.txt(46, yy + 9, cod, BOLD(10), c)
        L.txt(92, yy + 9, sit, SEMI(10), TINTA)
        L.txt(92, yy + 28, imp, REG(9), GRIS)
        etiqueta(L, 890, yy + 8, dec, c, cs)
        yy += 62
    L.guardar("fig_02_flujo_tecnico.png")


# ---------------------------------------------------------------- FIGURA 3
def fig_coordenadas():
    L = Lienzo(1000, 430)
    L.titulo("Figura 3. Por qué el control GPS hoy no funciona (hallazgo B-01)",
             "Los 34 activos del inventario tienen registrada la misma coordenada, y no está en el corredor")

    # Panel izquierdo: lo registrado
    L.caja(30, 92, 455, 250, FONDO, ROJO, r=8, grosor=2)
    L.caja(30, 92, 455, 34, ROJO_S, ROJO_S, r=8)
    L.d.rectangle([30*S, 116*S, 485*S, 126*S], fill=ROJO_S)
    L.txt(46, 101, "LO QUE ESTÁ REGISTRADO HOY", BOLD(10), ROJO)
    L.txt(46, 142, "4.728512, -74.114531", BOLD(16), TINTA)
    L.txt(46, 166, "Un único punto, en Bogotá, para los 34 activos.", REG(10), GRIS)
    cx, cy = 258, 238
    L.d.ellipse([(cx-38)*S, (cy-38)*S, (cx+38)*S, (cy+38)*S], outline=ROJO, width=1*S)
    L.d.ellipse([(cx-8)*S, (cy-8)*S, (cx+8)*S, (cy+8)*S], fill=ROJO)
    L.txt(cx, cy + 50, "34 activos apilados", SEMI(9), ROJO, anchor="ma")
    L.txt(cx, cy + 64, "en la misma coordenada", REG(9), GRIS, anchor="ma")

    # Panel derecho: la realidad
    L.caja(515, 92, 455, 250, FONDO, VERDE, r=8, grosor=2)
    L.caja(515, 92, 455, 34, VERDE_S, VERDE_S, r=8)
    L.d.rectangle([515*S, 116*S, 970*S, 126*S], fill=VERDE_S)
    L.txt(531, 101, "DÓNDE ESTÁN REALMENTE", BOLD(10), VERDE)
    L.txt(531, 142, "Corredor Sisga", BOLD(16), TINTA)
    L.txt(531, 166, "Repartidos entre UF1 y UF4, a decenas de kilómetros.", REG(10), GRIS)
    L.linea(545, 262, 940, 232, GRIS, 2)
    for i, (px, py, et) in enumerate([(560, 259, "UF1"), (655, 252, "UF2"),
                                      (755, 244, "UF3"), (890, 234, "UF4")]):
        L.d.ellipse([(px-5)*S, (py-5)*S, (px+5)*S, (py+5)*S], fill=VERDE)
        L.txt(px, py + 12, et, REG(9), GRIS, anchor="ma")
    L.txt(742, 288, "Los activos están sobre el corredor, no en un punto", REG(9), GRIS, anchor="ma")

    L.caja(30, 358, 940, 46, AMBAR_S, AMBAR, r=6)
    L.txt(46, 366, "Consecuencia:", BOLD(10), AMBAR)
    L.txt(46, 383, "la regla compara la posición del técnico contra esa coordenada. Un técnico frente a un poste en Machetá nunca podrá cerrar; "
                   "cualquiera en ese punto de Bogotá validaría los 34 activos.", REG(9), TINTA)
    L.guardar("fig_03_coordenadas.png")


# ---------------------------------------------------------------- FIGURA 4
def fig_ciclo_ot():
    L = Lienzo(1000, 360)
    L.titulo("Figura 4. Ciclo de vida propuesto para la orden de trabajo (decisión D-06)",
             "Hoy existen tres estados en los datos, sin regla que defina quién cambia cada uno")

    est = [
        ("Programada", "Supervisor", 40),
        ("Asignada", "Supervisor", 205),
        ("En ejecución", "Técnico", 370),
        ("En revisión", "Técnico", 535),
        ("Cerrada", "Supervisor", 700),
    ]
    y = 118
    for i, (nom, quien, x) in enumerate(est):
        final = nom == "Cerrada"
        L.caja(x, y, 140, 62, VERDE_S if final else AZUL_S, VERDE if final else AZUL, r=8)
        L.txt(x + 70, y + 15, nom, BOLD(11), VERDE if final else AZUL, anchor="ma")
        L.txt(x + 70, y + 36, quien, REG(9), GRIS, anchor="ma")
        if i < len(est) - 1:
            L.flecha(x + 143, y + 31, x + 202, y + 31)

    L.caja(700, 220, 140, 62, AMBAR_S, AMBAR, r=8)
    L.txt(770, 235, "Suspendida", BOLD(11), AMBAR, anchor="ma")
    L.txt(770, 256, "Supervisor", REG(9), GRIS, anchor="ma")
    L.flecha(640, 175, 700, 235, AMBAR)

    L.caja(860, 118, 110, 62, ROJO_S, ROJO, r=8)
    L.txt(915, 133, "Vencida", BOLD(11), ROJO, anchor="ma")
    L.txt(915, 154, "Sistema", REG(9), GRIS, anchor="ma")
    L.flecha(845, 149, 857, 149, ROJO)

    L.flecha(605, 186, 445, 186, GRIS)
    L.txt(525, 192, "devuelta con observación", REG(9), GRIS, anchor="ma")

    L.caja(30, 300, 940, 40, SUAVE, LINEA, r=6)
    L.txt(46, 312, "Preguntas abiertas:  ¿un técnico puede ejecutar sin orden previa (correctivo en ruta)?   "
                   "¿cuándo una orden se considera vencida?   ¿quién la suspende y con qué motivos?", REG(10), TINTA)
    L.guardar("fig_04_ciclo_ot.png")


# ---------------------------------------------------------------- FIGURA 5
def fig_ruta_critica():
    L = Lienzo(1000, 480)
    L.titulo("Figura 5. De sus respuestas al cronograma",
             "El proyecto no tiene fecha hasta que se resuelvan D-01 y D-09, que son trabajo del equipo de la Concesión")

    fases = [
        ("1. DEFINICIÓN", "Esta mesa de trabajo", ["Las 14 decisiones", "Acta firmada"], AZUL, AZUL_S),
        ("2. DATOS", "Trabajo de la Concesión", ["D-01 Coordenadas reales", "D-09 Bancos de preguntas",
                                                  "Realineación de sedes"], ROJO, ROJO_S),
        ("3. CONFIGURACIÓN", "Trabajo técnico", ["Reglas y validaciones", "Formularios y bots", "Reportes"], AMBAR, AMBAR_S),
        ("4. PRUEBA", "Una persona, extremo a extremo", ["Con señal y en modo avión", "Registros reales en la base"], AMBAR, AMBAR_S),
        ("5. PILOTO", "10 celulares en vía", ["Solo si la prueba pasó"], VERDE, VERDE_S),
    ]
    x0, w, sep, y = 30, 176, 12, 96
    for i, (nom, sub, items, c, cs) in enumerate(fases):
        x = x0 + i * (w + sep)
        L.caja(x, y, w, 148, FONDO, c, r=8)
        L.caja(x, y, w, 40, cs, cs, r=8)
        L.d.rectangle([x*S, (y+26)*S, (x+w)*S, (y+40)*S], fill=cs)
        L.txt(x + 13, y + 9, nom, BOLD(10), c)
        L.txt(x + 13, y + 24, sub, REG(8), GRIS)
        yy = y + 52
        for it in items:
            L.d.rectangle([(x+13)*S, (yy+5)*S, (x+16)*S, (yy+8)*S], fill=c)
            yy = L.parrafo(x + 22, yy, it, REG(9), TINTA, ancho=22, interlinea=12) + 6
        if i < len(fases) - 1:
            L.flecha(x + w + 1, y + 74, x + w + sep - 2, y + 74, c)

    L.caja(30, 264, 940, 52, ROJO_S, ROJO, r=6)
    L.txt(46, 274, "Ruta crítica", BOLD(11), ROJO)
    L.txt(46, 293, "D-01 (levantar las coordenadas de los 34 activos) y D-09 (redactar los bancos de preguntas) son trabajo del equipo de la Concesión, "
                   "no de configuración. Se miden en semanas. El cronograma completo lo fijan estas dos y no las demás.", REG(9), TINTA)

    L.txt(30, 338, "Qué habilita cada bloque de decisiones", BOLD(11), TINTA)
    filas = [
        ("D-01, D-02", "Coordenadas y radio de tolerancia", "Habilita el control GPS y la salida a campo"),
        ("D-03", "Significado de la sede", "Habilita la descarga de datos al celular"),
        ("D-04 a D-08", "Excepciones y ciclo de la orden", "Habilita la aceptación en campo y el indicador de cumplimiento"),
        ("D-09 a D-11", "Formularios y evidencia", "Fija el alcance real del primer sprint"),
        ("D-12, D-13", "Reportes e indicadores", "Habilita los entregables a Dirección e Interventoría"),
        ("D-14", "Licencias y gobierno", "Habilita la salida a producción"),
    ]
    yy = 360
    for cod, tema, hab in filas:
        L.linea(30, yy, 970, yy, LINEA)
        L.txt(42, yy + 6, cod, BOLD(9), AZUL)
        L.txt(140, yy + 6, tema, SEMI(9), TINTA)
        L.txt(470, yy + 6, hab, REG(9), GRIS)
        yy += 20
    L.linea(30, yy, 970, yy, LINEA)
    L.guardar("fig_05_ruta_critica.png")


if __name__ == "__main__":
    print("Generando esquemas en", OUT)
    fig_actores()
    fig_flujo_tecnico()
    fig_coordenadas()
    fig_ciclo_ot()
    fig_ruta_critica()
    print("Listo.")
