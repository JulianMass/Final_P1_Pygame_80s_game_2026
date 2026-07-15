import pygame
from Constantes import *
from Funciones import *

pygame.init()

def crear_lista_botones(cantidad_botones:int, textura:str, ancho:int, alto:int, x:int, y:int) -> list | None:
    if os.path.exists(textura):
        lista_botones = []

        for i in range (cantidad_botones):
            boton = crear_elemento_juego(textura, ancho, alto, x, y)
            lista_botones.append(boton)
            y += (alto + 20)
    else:
        lista_botones = None
    
    return lista_botones


fondo_menu = pygame.image.load("Texturas/fondo_menu.jpg")
fondo_menu = pygame.transform.scale(fondo_menu,PANTALLA)

lista_botones = crear_lista_botones(6, "Texturas/textura_boton.jpg", ANCHO_BOTON, ALTO_BOTON, 150, 130)
lista_texto_botones = ["Jugar", "Ajustes", "Rankings", "Ranking Preguntas", "Agregar Preguntas", "Salir"]
lista_tamaño_botones = [110, 100, 85, 30, 25, 115]


def mostrar_menu(pantalla:pygame.Surface, cola_eventos:list[pygame.event.Event]) -> str:
    ventana = "menu"

    for evento in cola_eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            for i in range(len(lista_botones)):
                if lista_botones[i]["rectangulo"].collidepoint(evento.pos):
                    SONIDO_ACIERTO.play()
                    ventana = lista_texto_botones[i].lower()


    pantalla.blit(fondo_menu,(0,0))

    for i in range(len(lista_botones)):
        pantalla.blit(lista_botones[i]["superficie"], lista_botones[i]["rectangulo"])
        mostrar_texto(lista_botones[i]["superficie"], lista_texto_botones[i], (lista_tamaño_botones[i], 10) ,FUENTE_GEORGIA_30, COLOR_BLANCO)

    return ventana
