import pygame
from Constantes import *
from Funciones import *

pygame.init()

boton_agregar = crear_elemento_juego("Texturas/textura_respuesta.jpg", 240, 60, 180, 240)
boton_volver = crear_elemento_juego("Texturas/textura_respuesta.jpg", 100, 40, 10, 10)

def mostrar_agregar_preguntas(pantalla:pygame.Surface, cola_eventos:list, datos_juego:dict) -> str:
    ventana = "agregar preguntas"

    for evento in cola_eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                if boton_volver["rectangulo"].collidepoint(evento.pos):
                    SONIDO_ACIERTO.play()
                    ventana = "menu"

                elif boton_agregar["rectangulo"].collidepoint(evento.pos):
                    if agregar_preguntas_csv():
                        datos_juego["lista_preguntas"] = leer_preguntas_csv()
                        datos_juego["mensaje_agregar"] = "Se agregaron 30 preguntas."
                        SONIDO_ACIERTO.play()
                    else:
                        datos_juego["mensaje_agregar"] = "Las preguntas ya fueron agregadas."
                        SONIDO_ERROR.play()


    pantalla.blit(FONDO_RANKINGS,(0,0))
    pantalla.blit(boton_volver["superficie"], boton_volver["rectangulo"])
    pantalla.blit(boton_agregar["superficie"], boton_agregar["rectangulo"])

    mostrar_texto(boton_volver["superficie"], "Volver", (10, 8), FUENTE_GEORGIA_20, COLOR_BLANCO)
    mostrar_texto(boton_agregar["superficie"], "Agregar", (55, 15), FUENTE_GEORGIA_30, COLOR_BLANCO)
    
    mostrar_texto(pantalla, "AGREGAR PREGUNTAS", (110, 80), FUENTE_GEORGIA_40, COLOR_NEGRO)
    mostrar_texto(pantalla, "Se agregarán las 30 preguntas", (90, 170), FUENTE_GEORGIA_25, COLOR_NEGRO)
    mostrar_texto(pantalla, "extras al juego.", (180, 205), FUENTE_GEORGIA_25, COLOR_NEGRO)

    if "mensaje_agregar" in datos_juego:
        mostrar_texto(pantalla, datos_juego["mensaje_agregar"], (80,340), FUENTE_GEORGIA_25, COLOR_NEGRO)

    return ventana