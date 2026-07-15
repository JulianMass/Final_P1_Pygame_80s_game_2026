import pygame
from Constantes import *
from Funciones import *
from Menu import *

pygame.init

evento_1_s = pygame.USEREVENT
pygame.time.set_timer(evento_1_s,1000)

def mostrar_juego(pantalla:pygame.Surface, cola_eventos:list[pygame.event.Event], datos_juego:dict) -> str:
        ventana = "jugar"

        cuadro_pregunta = datos_juego["cuadro_pregunta"]
        lista_respuestas = datos_juego["lista_respuestas"]
        pregunta_actual = datos_juego["pregunta_actual"]
        boton_bomba = crear_elemento_juego("Texturas/bomba.png", 65, 65, 50, 200)
        boton_x2 = crear_elemento_juego("Texturas/x2.png", 65, 65, 50, 300)
        boton_doble_chance = crear_elemento_juego("Texturas/segunda_chance.png", 65, 65, 50, 400)
        boton_pasar = crear_elemento_juego("Texturas/pasar_pregunta.png", 65, 65, 50, 500)
        botones_comodines = [boton_bomba, boton_x2, boton_doble_chance, boton_pasar]
        
        dibujar_pantalla(pantalla, datos_juego, cuadro_pregunta, lista_respuestas, pregunta_actual)

        dibujar_comodines(pantalla, botones_comodines, datos_juego)
        
        for evento in cola_eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if responder_pregunta(datos_juego["lista_preguntas"], lista_respuestas, SONIDO_ACIERTO, SONIDO_ERROR, evento.pos, pregunta_actual, datos_juego):
                    pregunta_actual = datos_juego["pregunta_actual"]
                    lista_respuestas = datos_juego["lista_respuestas"]
                    continue
                elif boton_bomba["rectangulo"].collidepoint(evento.pos) and datos_juego["comodines"]["bomba"]:
                    usar_bomba(pregunta_actual, lista_respuestas)
                    datos_juego["comodines"]["bomba"] = False
                    SONIDO_ACIERTO.play()
                elif boton_x2["rectangulo"].collidepoint(evento.pos) and datos_juego["comodines"]["x2"]:
                    usar_comodin_x2(datos_juego)
                    SONIDO_ACIERTO.play()
                elif boton_doble_chance["rectangulo"].collidepoint(evento.pos) and datos_juego["comodines"]["doble_chance"]:
                    usar_comodin_doble_chance(datos_juego)
                    SONIDO_ACIERTO.play()
                elif boton_pasar["rectangulo"].collidepoint(evento.pos) and datos_juego["comodines"]["pasar"]:
                    usar_comodin_pasar(datos_juego, datos_juego["lista_preguntas"])
                    pregunta_actual = datos_juego["pregunta_actual"]
                    lista_respuestas = datos_juego["lista_respuestas"]
                    SONIDO_ACIERTO.play()
                elif evento.type == evento_1_s:
                    if datos_juego["tiempo_restante"] > 0:
                        datos_juego["tiempo_restante"] -= 1
                    else:
                        ventana = "terminado"
            if evento.type == evento_1_s:  
                if datos_juego["tiempo_restante"] > 0:
                    datos_juego["tiempo_restante"] -= 1  
                else:
                    ventana = "terminado"

        if datos_juego["cantidad_vidas"] == 0:
            pygame.time.delay(300)
            ventana = "terminado"

        pygame.display.flip()
        return ventana



