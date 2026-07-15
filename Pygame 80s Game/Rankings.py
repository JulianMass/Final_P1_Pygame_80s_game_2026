import pygame
import json
from Constantes import *
from Funciones import *

pygame.init()

ruta_rankings = "rankings.json"

boton_volver = crear_elemento_juego("Texturas/textura_respuesta.jpg", 100, 40, 10, 10)

def cargar_rankings():
    lista_rankings = []
    if os.path.exists(ruta_rankings):
        with open(ruta_rankings, "r", encoding="utf-8") as archivo:
            lista_rankings = json.load(archivo)
    return lista_rankings

def guardar_rankings(lista_rankings):
    with open(ruta_rankings, "w", encoding="utf-8") as archivo:
        json.dump(lista_rankings, archivo, indent=4, ensure_ascii=False)

def agregar_al_ranking(nombre, puntaje, lista_rankings):
    lista_rankings.append({"nombre": nombre, "puntaje": puntaje})
    lista_rankings.sort(key=lambda x: x["puntaje"], reverse=True)
    lista_rankings[:] = lista_rankings[:10]
    guardar_rankings(lista_rankings)

def mostrar_rankings(pantalla:pygame.Surface, cola_eventos:list[pygame.event.Event], lista_rankings:list) -> str:
    ventana = "rankings"
    
    for evento in cola_eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                if boton_volver["rectangulo"].collidepoint(evento.pos):
                    SONIDO_ACIERTO.play()
                    ventana = "menu"
    
    pantalla.blit(FONDO_RANKINGS, (0, 0))
    
    pantalla.blit(boton_volver["superficie"],boton_volver["rectangulo"])
    mostrar_texto(pantalla,f"Top 10 jugadores/as", (80, 70), FUENTE_GEORGIA_50, COLOR_NEGRO)
    mostrar_texto(boton_volver["superficie"], "Volver", (5, 5), FUENTE_GEORGIA_20, COLOR_BLANCO)

    y = 140
    for jugador in lista_rankings:
        texto = (f"{jugador['nombre']} - "
                 f"{jugador['puntaje']} puntos - "
                 f"{jugador.get('fecha', '--/--/----')}")
        mostrar_texto(pantalla, texto, (45, y), FUENTE_GEORGIA_30, COLOR_NEGRO)
        y += 45
    return ventana
    