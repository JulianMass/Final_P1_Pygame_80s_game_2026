import pygame
import json
from Constantes import *
from Funciones import *
from datetime import datetime

pygame.init()


def mostrar_game_over(pantalla:pygame.Surface,datos_juego:dict,cola_eventos:list[pygame.event.Event],lista_rankings:list) -> str:
    ventana = "terminado"
    cuadro_texto = crear_elemento_juego("Texturas/textura_boton.jpg",300,50,150,270) 

    for evento in cola_eventos:
        if evento.type == pygame.TEXTINPUT:
            if evento.text.isalpha():
                datos_juego["nombre"] += evento.text
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_BACKSPACE:
                datos_juego["nombre"] = datos_juego["nombre"][0:-1]
            elif evento.key == pygame.K_RETURN:
                nombre = datos_juego["nombre"].strip()
                if nombre != "":
                    fecha = datetime.now().strftime("%d/%m/%Y")
                    lista_rankings.append({
                        "nombre": nombre,
                        "puntaje": datos_juego["puntuacion"],
                        "fecha": fecha
                    })
                    lista_rankings.sort(key=lambda x: x["puntaje"], reverse=True)
                    lista_rankings[:] = lista_rankings[:10]

                    with open("rankings.json", "w", encoding="utf-8") as archivo:
                        json.dump(lista_rankings, archivo, indent=4, ensure_ascii=False)

                datos_juego["nombre"] = ""
                ventana = "menu"

    pantalla.blit(FONDO_TERMINADO,(0,0))
    mostrar_texto(pantalla,f"Termino el juego: {datos_juego.get("puntuacion")} pts", (65, 110), FUENTE_GEORGIA_40, COLOR_BLANCO)

    mostrar_texto(cuadro_texto["superficie"],f"{datos_juego.get("nombre")}", (10, 10), FUENTE_GEORGIA_30, COLOR_BLANCO)
    pantalla.blit(cuadro_texto["superficie"], cuadro_texto["rectangulo"])

    return ventana
    