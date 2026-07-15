import pygame
from Constantes import *
from Funciones import *

pygame.init()

boton_volver = crear_elemento_juego("Texturas/textura_respuesta.jpg", 100, 40, 10, 10)
boton_anterior = crear_elemento_juego("Texturas/textura_respuesta.jpg", 60, 40, 150, 550)
boton_siguiente = crear_elemento_juego("Texturas/textura_respuesta.jpg", 60, 40, 390, 550)

def mostrar_ranking_preguntas(pantalla:pygame.Surface, cola_eventos:list, datos_juego:dict, lista_preguntas:list) -> str:
    ventana = "ranking preguntas"
    top5 = obtener_top_5_preguntas(lista_preguntas)
    pagina = datos_juego["pagina_ranking_preguntas"]
    inicio = pagina * 3
    fin = inicio + 3
    preguntas = top5[inicio:fin]

    for evento in cola_eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if boton_volver["rectangulo"].collidepoint(evento.pos):
                SONIDO_ACIERTO.play()
                datos_juego["pagina_ranking_preguntas"] = 0
                ventana = "menu"
            elif boton_siguiente["rectangulo"].collidepoint(evento.pos):
                if pagina < 1:
                    datos_juego["pagina_ranking_preguntas"] += 1
                    SONIDO_ACIERTO.play()
            elif boton_anterior["rectangulo"].collidepoint(evento.pos):
                if pagina > 0:
                    datos_juego["pagina_ranking_preguntas"] -= 1
                    SONIDO_ACIERTO.play()

    pantalla.blit(FONDO_RANKINGS_PREGUNTAS, (0, 0))
    pantalla.blit(boton_volver["superficie"], boton_volver["rectangulo"])

    mostrar_texto(boton_volver["superficie"], "Volver", (10, 8), FUENTE_GEORGIA_20, COLOR_BLANCO)
    mostrar_texto(pantalla, "TOP 5 PREGUNTAS", (120, 35), FUENTE_GEORGIA_40, COLOR_NEGRO)

    y = 95

    for i in range(len(preguntas)):
        pregunta = preguntas[i]
        porcentaje = calcular_porcentaje_aciertos(pregunta)
        descripcion = pregunta["descripcion"]

        if len(descripcion) > 48:
            corte = descripcion.rfind(" ", 0, 48)

            linea1 = descripcion[:corte]
            linea2 = descripcion[corte + 1:]
        else:
            linea1 = descripcion
            linea2 = ""

        mostrar_texto(pantalla, f"{inicio + i + 1}) {linea1}", (20, y), FUENTE_GEORGIA_20, COLOR_NEGRO)

        if linea2 != "":
            mostrar_texto(pantalla, linea2, (40, y + 22), FUENTE_GEORGIA_20, COLOR_NEGRO)

        mostrar_texto(pantalla, f"Porcentaje aciertos: {porcentaje:.1f}%", (40, y + 48), FUENTE_GEORGIA_20, COLOR_NEGRO)
        mostrar_texto(pantalla, f"Aciertos: {pregunta['aciertos']}", (40, y + 70), FUENTE_GEORGIA_20, COLOR_NEGRO)
        mostrar_texto(pantalla, f"Errores: {pregunta['errores']}", (220, y + 70), FUENTE_GEORGIA_20, COLOR_NEGRO)
        mostrar_texto(pantalla, f"Preguntada: {pregunta['veces_preguntada']}", (370, y + 70), FUENTE_GEORGIA_20, COLOR_NEGRO)
        pygame.draw.line(pantalla, COLOR_NEGRO, (20, y + 98), (580, y + 98), 2)

        y += 135

    pantalla.blit(boton_anterior["superficie"], boton_anterior["rectangulo"])
    pantalla.blit(boton_siguiente["superficie"], boton_siguiente["rectangulo"])

    mostrar_texto(boton_anterior["superficie"], "<<", (12, 3), FUENTE_GEORGIA_30, COLOR_NEGRO)
    mostrar_texto(boton_siguiente["superficie"], ">>", (12, 3), FUENTE_GEORGIA_30, COLOR_NEGRO)
    mostrar_texto(pantalla, f"Página {pagina+1}/2", (245, 555), FUENTE_GEORGIA_20, COLOR_NEGRO)
    
    return ventana

# ==========================================================
# ======== FUNCIONES DE RANKING DE PREGUNTAS ===============
# ==========================================================

# ----------------------------------------------------------
# Calcula el porcentaje de respuestas correctas de una
# pregunta según sus estadísticas.
# ----------------------------------------------------------
def calcular_porcentaje_aciertos(pregunta:dict) -> float:
    total = pregunta["aciertos"] + pregunta["errores"]
    if total == 0:
        return 0
    
    return (pregunta["aciertos"] * 100 / total)

# ----------------------------------------------------------
# Obtiene las cinco preguntas con mayor porcentaje
# de respuestas correctas.
# ----------------------------------------------------------
def obtener_top_5_preguntas(lista_preguntas:list) -> list:
    lista_ordenada = sorted(lista_preguntas, key=calcular_porcentaje_aciertos, reverse=True)

    return lista_ordenada[:5]

# ----------------------------------------------------------
# Divide un texto largo en varias líneas respetando una
# cantidad máxima de caracteres por línea.
# ----------------------------------------------------------
def dividir_texto(texto:str, max_caracteres:int) -> list:
    palabras = texto.split()
    lineas = []
    linea = ""
    for palabra in palabras:
        if len(linea + palabra) <= max_caracteres:
            linea += palabra + " "
        else:
            lineas.append(linea.strip())
            linea = palabra + " "

    if linea != "":
        lineas.append(linea.strip())

    return lineas