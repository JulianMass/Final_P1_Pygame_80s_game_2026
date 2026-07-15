import pygame
from Constantes import *
from Funciones import *

pygame.init()

boton_suma = crear_elemento_juego("Texturas/mas.png", 60, 60, 470, 170)
boton_resta = crear_elemento_juego("Texturas/menos.png", 60, 60, 50, 170)
boton_volver = crear_elemento_juego("Texturas/textura_respuesta.jpg", 100, 40, 10, 10)
boton_dificultad_menos = crear_elemento_juego("Texturas/menos.png", 60, 60, 50, 270)
boton_dificultad_mas = crear_elemento_juego("Texturas/mas.png", 60, 60 ,470, 270)
boton_musica = crear_elemento_juego("Texturas/textura_respuesta.jpg", 140, 45, 190, 530)
dificultades = ["Facil", "Normal", "Dificil", "Personalizada"]

boton_vidas_menos = crear_elemento_juego("Texturas/menos.png", 30, 30, 240, 335)
boton_vidas_mas = crear_elemento_juego("Texturas/mas.png", 30, 30, 410, 335)
boton_tiempo_menos = crear_elemento_juego("Texturas/menos.png", 30, 30, 240, 370)
boton_tiempo_mas = crear_elemento_juego("Texturas/mas.png", 30, 30, 410, 370)
boton_acierto_menos = crear_elemento_juego("Texturas/menos.png", 30, 30, 240, 405)
boton_acierto_mas = crear_elemento_juego("Texturas/mas.png", 30, 30, 410, 405)
boton_error_menos = crear_elemento_juego("Texturas/menos.png", 30, 30, 240, 440)
boton_error_mas = crear_elemento_juego("Texturas/mas.png", 30, 30, 410, 440)


def administrar_botones(boton_suma:dict, boton_resta:dict, boton_dificultad_mas:dict, boton_dificultad_menos:dict, boton_volver:dict, boton_musica:dict, boton_vidas_menos:dict, boton_vidas_mas:dict, boton_tiempo_menos:dict, boton_tiempo_mas:dict, boton_acierto_menos:dict, boton_acierto_mas:dict, boton_error_menos:dict, boton_error_mas:dict, datos_juego:dict, pos_mouse:tuple) -> str:
    ventana = "ajustes"
    
    if boton_suma["rectangulo"].collidepoint(pos_mouse):
        if datos_juego["volumen_musica"] <= 95:
            datos_juego["volumen_musica"] += 5
            if datos_juego["musica_activada"]:
                pygame.mixer.music.set_volume(datos_juego["volumen_musica"] / 100)
            SONIDO_ACIERTO.play()
        else:
            SONIDO_ERROR.play()
    elif boton_resta["rectangulo"].collidepoint(pos_mouse):
        if datos_juego["volumen_musica"] > 0:
            datos_juego["volumen_musica"] -= 5
            if datos_juego["musica_activada"]:
                pygame.mixer.music.set_volume(datos_juego["volumen_musica"] / 100)
            SONIDO_ACIERTO.play()
        else: 
            SONIDO_ERROR.play()
    elif boton_volver["rectangulo"].collidepoint(pos_mouse):
        SONIDO_ACIERTO.play()
        ventana = "menu"
    elif boton_dificultad_mas["rectangulo"].collidepoint(pos_mouse):
        indice = dificultades.index(datos_juego["dificultad"])
        if indice < len(dificultades) - 1:
            datos_juego["dificultad"] = dificultades[indice + 1]
            SONIDO_ACIERTO.play()
        else:
            SONIDO_ERROR.play()
    elif boton_dificultad_menos["rectangulo"].collidepoint(pos_mouse):
        indice = dificultades.index(datos_juego["dificultad"])
        if indice > 0:
            datos_juego["dificultad"] = dificultades[indice - 1]
            SONIDO_ACIERTO.play()
        else:
            SONIDO_ERROR.play()
    elif boton_musica["rectangulo"].collidepoint(pos_mouse):   
        datos_juego["musica_activada"] = not datos_juego["musica_activada"]
        if datos_juego["musica_activada"]:
            pygame.mixer.music.set_volume(datos_juego["volumen_musica"] / 100)
        else:
            pygame.mixer.music.set_volume(0)
        SONIDO_ACIERTO.play()
    elif datos_juego["dificultad"] == "Personalizada":

        # VIDAS
        if boton_vidas_mas["rectangulo"].collidepoint(pos_mouse):
            if datos_juego["vidas_iniciales"] < 10:
                datos_juego["vidas_iniciales"] += 1
                SONIDO_ACIERTO.play()
            else:
                SONIDO_ERROR.play()

        elif boton_vidas_menos["rectangulo"].collidepoint(pos_mouse):
            if datos_juego["vidas_iniciales"] > 1:
                datos_juego["vidas_iniciales"] -= 1
                SONIDO_ACIERTO.play()
            else:
                SONIDO_ERROR.play()

        # TIEMPO
        elif boton_tiempo_mas["rectangulo"].collidepoint(pos_mouse):
            if datos_juego["tiempo_inicial"] < 300:
                datos_juego["tiempo_inicial"] += 5
                SONIDO_ACIERTO.play()
            else:
                SONIDO_ERROR.play()

        elif boton_tiempo_menos["rectangulo"].collidepoint(pos_mouse):
            if datos_juego["tiempo_inicial"] > 15:
                datos_juego["tiempo_inicial"] -= 5
                SONIDO_ACIERTO.play()
            else:
                SONIDO_ERROR.play()

        # PUNTOS ACIERTO
        elif boton_acierto_mas["rectangulo"].collidepoint(pos_mouse):
            if datos_juego["puntos_acierto"] < 500:
                datos_juego["puntos_acierto"] += 25
                SONIDO_ACIERTO.play()
            else:
                SONIDO_ERROR.play()

        elif boton_acierto_menos["rectangulo"].collidepoint(pos_mouse):
            if datos_juego["puntos_acierto"] > 25:
                datos_juego["puntos_acierto"] -= 25
                SONIDO_ACIERTO.play()
            else:
                SONIDO_ERROR.play()

        # PUNTOS ERROR
        elif boton_error_mas["rectangulo"].collidepoint(pos_mouse):
            if datos_juego["puntos_error"] < 0:
                datos_juego["puntos_error"] += 25
                SONIDO_ACIERTO.play()
            else:
                SONIDO_ERROR.play()

        elif boton_error_menos["rectangulo"].collidepoint(pos_mouse):
            if datos_juego["puntos_error"] > -500:
                datos_juego["puntos_error"] -= 25
                SONIDO_ACIERTO.play()
            else:
                SONIDO_ERROR.play()

    return ventana

def mostrar_ajustes(pantalla:pygame.Surface, cola_eventos:list[pygame.event.Event], datos_juego:dict) -> str:
    ventana = "ajustes"
    
    for evento in cola_eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            ventana = administrar_botones(boton_suma, boton_resta, boton_dificultad_mas, boton_dificultad_menos, boton_volver, boton_musica, boton_vidas_menos, boton_vidas_mas, boton_tiempo_menos, boton_tiempo_mas, boton_acierto_menos, boton_acierto_mas, boton_error_menos, boton_error_mas, datos_juego, evento.pos)
            
    
    pantalla.blit(FONDO_AJUSTES,(0,0))    
    pantalla.blit(boton_suma["superficie"], boton_suma["rectangulo"])
    pantalla.blit(boton_resta["superficie"], boton_resta["rectangulo"])
    pantalla.blit(boton_dificultad_mas["superficie"], boton_dificultad_mas["rectangulo"])
    pantalla.blit(boton_dificultad_menos["superficie"], boton_dificultad_menos["rectangulo"])
    pantalla.blit(boton_volver["superficie"], boton_volver["rectangulo"])

    mostrar_texto(pantalla, "Volumen", (165, 110), FUENTE_GEORGIA_50, COLOR_NEGRO)
    mostrar_texto(pantalla, f"{datos_juego['volumen_musica']} %", (230, 165), FUENTE_GEORGIA_50, COLOR_NEGRO)
    mostrar_texto(boton_volver["superficie"], "Volver", (5, 5), FUENTE_GEORGIA_20, COLOR_BLANCO)
    mostrar_texto(pantalla, "Dificultad", (165, 225), FUENTE_GEORGIA_50, COLOR_NEGRO)
    mostrar_texto(pantalla, datos_juego["dificultad"], (180, 275), FUENTE_GEORGIA_40, COLOR_NEGRO)


    if datos_juego["dificultad"] == "Personalizada":

        pantalla.blit(boton_vidas_menos["superficie"], boton_vidas_menos["rectangulo"])
        pantalla.blit(boton_vidas_mas["superficie"], boton_vidas_mas["rectangulo"])

        pantalla.blit(boton_tiempo_menos["superficie"], boton_tiempo_menos["rectangulo"])
        pantalla.blit(boton_tiempo_mas["superficie"], boton_tiempo_mas["rectangulo"])

        pantalla.blit(boton_acierto_menos["superficie"], boton_acierto_menos["rectangulo"])
        pantalla.blit(boton_acierto_mas["superficie"], boton_acierto_mas["rectangulo"])

        pantalla.blit(boton_error_menos["superficie"], boton_error_menos["rectangulo"])
        pantalla.blit(boton_error_mas["superficie"], boton_error_mas["rectangulo"])


        mostrar_texto(pantalla, "Vidas", (130, 338), FUENTE_GEORGIA_25, COLOR_NEGRO)
        mostrar_texto(pantalla, str(datos_juego["vidas_iniciales"]), (330, 335), FUENTE_GEORGIA_25, COLOR_NEGRO)

        mostrar_texto(pantalla, "Tiempo", (130, 373), FUENTE_GEORGIA_25, COLOR_NEGRO)
        mostrar_texto(pantalla, str(datos_juego["tiempo_inicial"]), (330, 370), FUENTE_GEORGIA_25, COLOR_NEGRO)

        mostrar_texto(pantalla, "Acierto", (130, 408), FUENTE_GEORGIA_25, COLOR_NEGRO)
        mostrar_texto(pantalla, str(datos_juego["puntos_acierto"]), (330, 405), FUENTE_GEORGIA_25, COLOR_NEGRO)

        mostrar_texto(pantalla, "Error", (130, 443), FUENTE_GEORGIA_25, COLOR_NEGRO)
        mostrar_texto(pantalla, str(datos_juego["puntos_error"]), (330, 440), FUENTE_GEORGIA_25, COLOR_NEGRO)


    mostrar_texto(pantalla, "Musica", (200, 500), FUENTE_GEORGIA_30, COLOR_NEGRO)
    estado = "ON"

    if not datos_juego["musica_activada"]:
        estado = "OFF"

    boton_musica["superficie"] = pygame.image.load("Texturas/textura_respuesta.jpg")
    boton_musica["superficie"] = pygame.transform.scale(boton_musica["superficie"], (140, 45))
    mostrar_texto(boton_musica["superficie"], estado, (30, 5), FUENTE_GEORGIA_25, COLOR_BLANCO)

    pantalla.blit(boton_musica["superficie"], boton_musica["rectangulo"])
    
    return ventana
    

