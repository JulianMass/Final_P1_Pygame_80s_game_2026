from Constantes import *
import os
import random
from Preguntas import *

# ==========================================================
# =============== FUNCIONES DE CREACIÓN ====================
# ==========================================================

# ----------------------------------------------------------
# Inicializa el diccionario principal con todos los datos
# necesarios para comenzar una nueva partida.
# ----------------------------------------------------------
def crear_datos_juego() -> dict:
    datos_juego = {
        "nombre": "",
        "tiempo_restante": TIEMPO_TOTAL,
        "puntuacion": 0,
        "cantidad_vidas": CANTIDAD_VIDAS,
        "i_pregunta": 0,

        "volumen_musica": 100, 
        "musica_activada": True,
        
        "dificultad": "Normal",
        "tiempo_inicial": TIEMPO_TOTAL,
        "vidas_iniciales": CANTIDAD_VIDAS,

        "puntos_acierto": 100,
        "puntos_error": -50,

        "racha": 0,

        "comodines": {       
            "bomba": True,
            "x2": True,
            "doble_chance": True,
            "pasar": True
        },

        "x2_activo": False,           
        "doble_chance_activo": False,
        "primer_error_doble": False,
        "saltar_pregunta": False,

        "respuestas_ocultas": [],

        "pregunta_actual": None,
        "lista_respuestas": None,
        "cuadro_pregunta": None,

        "pagina_ranking_preguntas": 0
    }

    return datos_juego

# ----------------------------------------------------------
# Crea un elemento gráfico del juego cargando una imagen,
# escalándola al tamaño indicado y asignándole una posición.
# ----------------------------------------------------------
def crear_elemento_juego(textura:str, ancho_elemento:int, alto_elemento:int, pos_x:int, pos_y:int) -> dict | None:
    if os.path.exists(textura):
        elemento_juego = {}
        elemento_juego["superficie"] = pygame.image.load(textura)
        elemento_juego["superficie"] = pygame.transform.scale(elemento_juego["superficie"],(ancho_elemento,alto_elemento))
        elemento_juego["rectangulo"] = pygame.rect.Rect(pos_x,pos_y,ancho_elemento,alto_elemento)
    else:
        elemento_juego = None
    
    return elemento_juego

# ----------------------------------------------------------
# Crea la lista de botones de respuesta que utilizará
# el jugador durante la partida.
# ----------------------------------------------------------
def crear_lista_respuestas(cantidad_respuestas:int, textura:str, ancho:int, alto:int, x:int, y:int) -> list | None:
    if os.path.exists(textura):
        lista_respuestas = []

        for i in range (cantidad_respuestas):
            cuadro_respuesta = crear_elemento_juego(textura, ancho, alto, x, y)
            cuadro_respuesta["visible"] = True # agregado el nuevo dato al dict
            lista_respuestas.append(cuadro_respuesta)
            y += alto + 20
    else:
        lista_respuestas = None
    
    return lista_respuestas


# ==========================================================
# ============== FUNCIONES DE PARTIDA ======================
# ==========================================================

# ----------------------------------------------------------
# Configura una nueva partida cargando la primera pregunta
# y reiniciando los elementos gráficos necesarios.
# ----------------------------------------------------------
def iniciar_partida(datos_juego:dict, lista_preguntas:list) -> None:
    datos_juego["lista_preguntas"] = lista_preguntas
    datos_juego["i_pregunta"] = 0
    datos_juego["pregunta_actual"] = obtener_pregunta_actual(datos_juego, lista_preguntas)
    if datos_juego["pregunta_actual"] != None:
        datos_juego["pregunta_actual"]["veces_preguntada"] += 1
        guardar_preguntas_csv(datos_juego["lista_preguntas"])
    datos_juego["cuadro_pregunta"] = crear_elemento_juego("Texturas/textura_pregunta.jpg", ANCHO_PREGUNTA, ALTO_PREGUNTA, 120, 100)
    datos_juego["lista_respuestas"] = crear_lista_respuestas(4, "Texturas/textura_respuesta.jpg", ANCHO_RESPUESTA, ALTO_RESPUESTA, 195, 275)

# ----------------------------------------------------------
# Devuelve la pregunta correspondiente al índice actual
# de la partida.
# ----------------------------------------------------------
def obtener_pregunta_actual(datos_juego:dict, lista_preguntas:list) -> dict | None:
    if type(lista_preguntas) == list and len(lista_preguntas) > 0:
        indice = datos_juego["i_pregunta"]
        if indice < len(lista_preguntas):
            return lista_preguntas[indice]
    
    return None

# ----------------------------------------------------------
# Avanza a la siguiente pregunta y reinicia los elementos
# necesarios para continuar la partida.
# ----------------------------------------------------------
def pasar_pregunta(datos_juego:dict, lista_preguntas:list) -> bool:
    if type(datos_juego) == dict and datos_juego.get("i_pregunta") != None:
        datos_juego["i_pregunta"] += 1 # avanza la pregunta
        verificar_indice(datos_juego, lista_preguntas) # si llego al final de la lista vuelve al principio   
        datos_juego["respuestas_ocultas"] = [] # restablece respuestas ocultas de la bomba
        datos_juego["cuadro_pregunta"] = crear_elemento_juego("Texturas/textura_pregunta.jpg", ANCHO_PREGUNTA, ALTO_PREGUNTA, 120, 100)
        datos_juego["lista_respuestas"] = crear_lista_respuestas(4, "Texturas/textura_respuesta.jpg", ANCHO_RESPUESTA, ALTO_RESPUESTA, 195, 275)
        datos_juego["pregunta_actual"] = obtener_pregunta_actual(datos_juego, lista_preguntas)
        if datos_juego["pregunta_actual"] != None:
            datos_juego["pregunta_actual"]["veces_preguntada"] += 1
            guardar_preguntas_csv(datos_juego["lista_preguntas"])
        
        return True
    
    return False

# ----------------------------------------------------------
# Verifica si el índice actual superó la cantidad de
# preguntas y lo reinicia cuando corresponde.
# ----------------------------------------------------------
def verificar_indice(datos_juego:dict, lista_preguntas:list) -> bool:
    if type(datos_juego) == dict and datos_juego.get("i_pregunta") != None:
        retorno = True
        if datos_juego["i_pregunta"] >= len(lista_preguntas):
            datos_juego["i_pregunta"] = 0
            mezclar_lista(lista_preguntas)    
    else:
        retorno = False
        
    return retorno


# ==========================================================
# =============== FUNCIONES DE RESPUESTAS ==================
# ==========================================================

# ----------------------------------------------------------
# Comprueba si la respuesta elegida es correcta y aplica
# las modificaciones correspondientes.
# ----------------------------------------------------------
def verificar_respuesta(pregunta_actual:dict, datos_juego:dict, respuesta:int, indice_respuesta:int, lista_respuestas:list, sonido_acierto:pygame.mixer.Sound, sonido_error:pygame.mixer.Sound) -> bool:
    if type(pregunta_actual) != dict or pregunta_actual.get("respuesta_correcta") is None:
        return False
        
    if pregunta_actual["respuesta_correcta"] == respuesta:
            pregunta_actual["aciertos"] += 1
            guardar_preguntas_csv(datos_juego["lista_preguntas"])
            if datos_juego["x2_activo"]:
                modificar_puntuacion(datos_juego, datos_juego["puntos_acierto"] * 2)
                datos_juego["x2_activo"] = False
            else:
                modificar_puntuacion(datos_juego, datos_juego["puntos_acierto"])
            datos_juego["doble_chance_activo"] = False
            datos_juego["primer_error_doble"] = False
            sonido_acierto.play()
            return True
    else:
        if datos_juego["doble_chance_activo"]:
            if not datos_juego["primer_error_doble"]:
                datos_juego["primer_error_doble"] = True
                lista_respuestas[indice_respuesta]["visible"] = False
                sonido_error.play()
                return False
            else:
                pregunta_actual["errores"] += 1
                guardar_preguntas_csv(datos_juego["lista_preguntas"])
                modificar_puntuacion(datos_juego, datos_juego["puntos_error"])
                modificar_vida(datos_juego, -1)
                datos_juego["doble_chance_activo"] = False
                datos_juego["primer_error_doble"] = False
                sonido_error.play()
                return True
        else:
            pregunta_actual["errores"] += 1
            guardar_preguntas_csv(datos_juego["lista_preguntas"])
            modificar_puntuacion(datos_juego, datos_juego["puntos_error"])
            modificar_vida(datos_juego, -1)
            sonido_error.play()
            return True

# ----------------------------------------------------------
# Detecta la respuesta seleccionada por el jugador y
# procesa el resultado obtenido.
# ----------------------------------------------------------
def responder_pregunta(lista_preguntas:list, lista_respuestas:list, sonido_acierto:pygame.mixer.Sound, sonido_error:pygame.mixer.Sound, pos_mouse:tuple, pregunta_actual:dict, datos_juego:dict) -> bool:
        retorno = False
        for i in range(len(lista_respuestas)):
            if lista_respuestas[i]["visible"]:
                if lista_respuestas[i]["rectangulo"].collidepoint(pos_mouse):
                    respuesta = i + 1
                    avanzar = verificar_respuesta(pregunta_actual, datos_juego, respuesta, i, lista_respuestas, sonido_acierto, sonido_error)
                
                    if avanzar:
                        if pregunta_actual["respuesta_correcta"] == respuesta:
                            datos_juego["racha"] += 1
                            if datos_juego["racha"] >= 5:
                                datos_juego["cantidad_vidas"] += 1
                                datos_juego["racha"] = 0
                        else:
                            datos_juego["racha"] = 0

                        pasar_pregunta(datos_juego, lista_preguntas)
                        retorno = True
                    break # ya se encontro la respuesta, no hace falta seguir recorriendo la lista
        
        return retorno


# ==========================================================
# ================== PUNTAJE Y VIDAS =======================
# ==========================================================

# ----------------------------------------------------------
# Modifica el puntaje actual del jugador.
# ----------------------------------------------------------
def modificar_puntuacion(datos_juego:dict, incremento:int) -> bool:
    if type(datos_juego) == dict and datos_juego.get("puntuacion") != None:
        retorno = True
        datos_juego["puntuacion"] += incremento
    else:
        retorno = False
        
    return retorno

# ----------------------------------------------------------
# Modifica la cantidad de vidas disponibles.
# ----------------------------------------------------------
def modificar_vida(datos_juego:dict,incremento:int) -> bool:
    if type(datos_juego) == dict and datos_juego.get("cantidad_vidas") != None:
        retorno = True
        datos_juego["cantidad_vidas"] += incremento
    else:
        retorno = False
        
    return retorno

# ----------------------------------------------------------
# Reinicia las estadísticas necesarias para comenzar
# una nueva partida.
# ----------------------------------------------------------
def reiniciar_estadisticas(datos_juego:dict) -> bool:
    if type(datos_juego) == dict:
        
        configurar_dificultad(datos_juego)

        datos_juego.update({
            "tiempo_restante": datos_juego["tiempo_inicial"],
            "puntuacion": 0,
            "cantidad_vidas": datos_juego["vidas_iniciales"],
            "i_pregunta": 0,
            "racha": 0,  
            "comodines": {       
                "bomba": True,
                "x2": True,
                "doble_chance": True,
                "pasar": True
            },
            "x2_activo": False,           
            "doble_chance_activo": False,
            "primer_error_doble": False,
            "saltar_pregunta": False,
            "respuestas_ocultas": [],
            "pregunta_actual": None,
            "lista_respuestas": None,
            "cuadro_pregunta": None,
            "pagina_ranking_preguntas": 0
        })
        retorno = True
    else:
        retorno = False
        
    return retorno


# ==========================================================
# ============== FUNCIONES DE COMODINES ====================
# ==========================================================

# ----------------------------------------------------------
# Elimina dos respuestas incorrectas de la pregunta actual.
# ----------------------------------------------------------
def usar_bomba(pregunta_actual:dict, lista_respuestas:list) -> None:
    correcta = pregunta_actual["respuesta_correcta"] - 1
    indices = []
    for i in range(len(lista_respuestas)):
        if i != correcta:
            indices.append(i)
    eliminar = random.sample(indices, 2)
    for indice in eliminar:
        lista_respuestas[indice]["visible"] = False

# ----------------------------------------------------------
# Activa el comodín de doble puntaje para la próxima
# respuesta correcta.
# ----------------------------------------------------------
def usar_comodin_x2(datos_juego:dict) -> None:
    if datos_juego["comodines"]["x2"]:
        datos_juego["x2_activo"] = True 
        datos_juego["comodines"]["x2"] = False 

# ----------------------------------------------------------
# Permite equivocarse una vez sin perder vidas.
# ----------------------------------------------------------
def usar_comodin_doble_chance(datos_juego:dict) -> None:
    if datos_juego["comodines"]["doble_chance"]:
        datos_juego["comodines"]["doble_chance"] = False  
        datos_juego["doble_chance_activo"] = True 
        datos_juego["primer_error_doble"] = False

# ----------------------------------------------------------
# Salta la pregunta actual sin responderla.
# ----------------------------------------------------------
def usar_comodin_pasar(datos_juego:dict, lista_preguntas:list) -> None:
    if datos_juego["comodines"]["pasar"]:
        datos_juego["comodines"]["pasar"] = False  
        pasar_pregunta(datos_juego, lista_preguntas)


# ==========================================================
# ============== FUNCIONES DE ARCHIVOS CSV =================
# ==========================================================

# ----------------------------------------------------------
# Genera el archivo CSV con las preguntas originales.
# ----------------------------------------------------------
def generar_csv_preguntas(nombre_archivo:str = "preguntas.csv") -> None:
    if len(lista_preguntas_original) == 0:
        return
    
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        
        encabezados = list(lista_preguntas_original[0].keys()) # obtiene automaticamente los encabezados
        linea = ""

        for i in range(len(encabezados)):
            linea += encabezados[i]
            if i < len(encabezados) - 1:
                linea += ","
        
        archivo.write(linea + "\n")

        for pregunta in lista_preguntas_original:
            linea = ""
            
            for i in range (len(encabezados)):
                linea += str(pregunta[encabezados[i]])
                if i < len(encabezados) - 1:
                    linea += ","

            archivo.write(linea + "\n")

# ----------------------------------------------------------
# Genera el archivo CSV con las preguntas adicionales.
# ----------------------------------------------------------
def generar_csv_preguntas_extra(nombre_archivo:str = "preguntas_extra.csv") -> list:
    if len(lista_preguntas_extra) == 0:
        return

    with open(nombre_archivo, "w", encoding="utf-8") as archivo:

        encabezados = list(lista_preguntas_extra[0].keys())
        linea = ""

        for i in range(len(encabezados)):
            linea += encabezados[i]
            if i < len(encabezados)-1:
                linea += ","

        archivo.write(linea + "\n")

        for pregunta in lista_preguntas_extra:

            linea = ""

            for i in range(len(encabezados)):
                linea += str(pregunta[encabezados[i]])

                if i < len(encabezados)-1:
                    linea += ","

            archivo.write(linea + "\n")

# ----------------------------------------------------------
# Lee las preguntas almacenadas en el archivo CSV y
# las devuelve en una lista de diccionarios.
# ----------------------------------------------------------
def leer_preguntas_csv(nombre_archivo:str = "preguntas.csv") -> list:
    lista_preguntas = []
    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        lineas = archivo.readlines()
        encabezados = lineas[0].strip().split(",")
        
        for i in range(1, len(lineas)): # recorre desde la 2 linea pq la 1 es el encabezado
            datos = lineas[i].strip().split(",")
            pregunta = {} # arma el diccionario
            
            for j in range(len(encabezados)):
                clave = encabezados[j]
                valor = datos[j]
                if clave in ("respuesta_correcta", "veces_preguntada", "aciertos", "errores"):
                    valor = int(valor) # como el archivo es todo texto, lo vuelve int
                pregunta[clave] = valor
            
            lista_preguntas.append(pregunta)

    return lista_preguntas

# ----------------------------------------------------------
# Guarda la lista actual de preguntas en el archivo CSV.
# ----------------------------------------------------------
def guardar_preguntas_csv(lista_preguntas:list, nombre_archivo:str="preguntas.csv") -> None:
    if len(lista_preguntas) == 0:
        return
    
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        encabezados = list(lista_preguntas[0].keys())
        linea = ""

        for i in range(len(encabezados)):
            linea += encabezados[i]

            if i < len(encabezados) - 1:
                linea += ","

        archivo.write(linea + "\n")

        for pregunta in lista_preguntas:
            linea = ""

            for i in range(len(encabezados)):
                linea += str(pregunta[encabezados[i]])

                if i < len(encabezados) - 1:
                    linea += ","

            archivo.write(linea + "\n")

# ----------------------------------------------------------
# Agrega al archivo principal las preguntas almacenadas
# en el archivo de preguntas extra.
# ----------------------------------------------------------
def agregar_preguntas_csv(nombre_original:str="preguntas.csv", nombre_extra:str="preguntas_extra.csv") -> bool:

    lista = leer_preguntas_csv(nombre_original)

    if len(lista) >= 60:
        return False

    with open(nombre_original, "a", encoding="utf-8") as archivo_original:
        with open(nombre_extra, "r", encoding="utf-8") as archivo_extra:
            lineas = archivo_extra.readlines()
            
            for i in range(1, len(lineas)):
                archivo_original.write(lineas[i])

    return True


# ==========================================================
# ================= FUNCIONES DE MÚSICA ====================
# ==========================================================

# ----------------------------------------------------------
# Inicializa el mezclador de sonido y reproduce la música
# de fondo en bucle.
# ----------------------------------------------------------
def iniciar_musica(ruta_archivo:str, volumen:int):
    pygame.mixer.music.load(ruta_archivo)
    pygame.mixer.music.set_volume(volumen/ 100)
    pygame.mixer.music.play(-1, start=1.8)

# ==========================================================
# ============= FUNCIONES DE VISUALIZACION =================
# ==========================================================

# ----------------------------------------------------------
# Muestra un texto sobre una superficie ajustándolo
# automáticamente cuando supera el ancho disponible.
# ----------------------------------------------------------
def mostrar_texto(surface, text, pos, font, color=pygame.Color('white')):
    words = [word.split(' ') for word in text.splitlines()]  
    space = font.size(' ')[0]  
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, True, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  
                y += word_height  
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  
        y += word_height  

# ----------------------------------------------------------
# Muestra en pantalla el tiempo restante, la puntuación
# y la cantidad de vidas del jugador.
# ----------------------------------------------------------
def mostrar_datos_juego(pantalla:pygame.Surface,datos_juego:dict) -> bool:
    if type(datos_juego) == dict:
        mostrar_texto(pantalla,f"Tiempo: {datos_juego.get("tiempo_restante")} segundos",(10,10),FUENTE_GEORGIA_20)
        mostrar_texto(pantalla,f"Puntuacion: {datos_juego.get("puntuacion")}",(10,40),FUENTE_GEORGIA_20)
        mostrar_texto(pantalla,f"Vidas: {datos_juego.get("cantidad_vidas")}",(10,70),FUENTE_GEORGIA_20)
        retorno = True
    else:
        retorno = False
        
    return retorno

# ----------------------------------------------------------
# Mezcla aleatoriamente el orden de las preguntas.
# ----------------------------------------------------------
def mezclar_lista(lista_preguntas:list) -> bool:
    if type(lista_preguntas) == list and len(lista_preguntas) > 0:
        retorno = True
        random.shuffle(lista_preguntas)
    else:
        retorno = False
    
    return retorno


# ==========================================================
# =================== PUNTAJE Y VIDAS ======================
# ==========================================================

# ----------------------------------------------------------
# Modifica la cantidad de vidas del jugador.
# ----------------------------------------------------------
def modificar_vida(datos_juego:dict,incremento:int) -> bool:
    if type(datos_juego) == dict and datos_juego.get("cantidad_vidas") != None:
        retorno = True
        datos_juego["cantidad_vidas"] += incremento
    else:
        retorno = False
        
    return retorno


# ==========================================================
# ================ FUNCIONES DE DIBUJADO ===================
# ==========================================================

# ----------------------------------------------------------
# Dibuja todos los elementos principales de la partida:
# fondo, datos del jugador, pregunta y respuestas.
# ----------------------------------------------------------
def dibujar_pantalla(pantalla:pygame.Surface, datos_juego:dict, cuadro_pregunta:dict, lista_respuestas:dict, pregunta_actual:dict) -> None:
    if type(datos_juego) == dict and type(cuadro_pregunta) == dict:
        pantalla.blit(FONDO_JUEGO, (0, 0))
        mostrar_datos_juego(pantalla,datos_juego)

        cuadro_pregunta["superficie"] = TEXTURA_PREGUNTA.copy()
        mostrar_texto(cuadro_pregunta["superficie"], pregunta_actual["descripcion"], (20,20), FUENTE_GEORGIA_25)
        pantalla.blit(cuadro_pregunta["superficie"], cuadro_pregunta["rectangulo"])

        for i in range(len(lista_respuestas)):
            if lista_respuestas[i]["visible"]:
                lista_respuestas[i]["superficie"] = TEXTURA_RESPUESTA.copy()
                mostrar_texto(lista_respuestas[i]["superficie"], pregunta_actual.get(f"respuesta_{i+1}"), (25,10), FUENTE_GEORGIA_20, COLOR_BLANCO)
                pantalla.blit(lista_respuestas[i]["superficie"], lista_respuestas[i]["rectangulo"])

# ----------------------------------------------------------
# Dibuja únicamente los comodines que todavía están
# disponibles durante la partida.
# ----------------------------------------------------------
def dibujar_comodines(pantalla:pygame.Surface, botones_comodines:list, datos_juego:dict) -> None:
    if datos_juego["comodines"]["bomba"]:
        pantalla.blit(botones_comodines[0]["superficie"], botones_comodines[0]["rectangulo"])
    if datos_juego["comodines"]["x2"]:
        pantalla.blit(botones_comodines[1]["superficie"], botones_comodines[1]["rectangulo"])
    if datos_juego["comodines"]["doble_chance"]:
        pantalla.blit(botones_comodines[2]["superficie"], botones_comodines[2]["rectangulo"])
    if datos_juego["comodines"]["pasar"]:
        pantalla.blit(botones_comodines[3]["superficie"], botones_comodines[3]["rectangulo"])


# ==========================================================
# =============== CONFIGURACIÓN DEL JUEGO ==================
# ==========================================================

# ----------------------------------------------------------
# Configura los valores iniciales de la partida según
# la dificultad seleccionada.
# ----------------------------------------------------------
def configurar_dificultad(datos_juego:dict) -> None:
    dificultad = datos_juego["dificultad"]
    if dificultad == "Facil":
        datos_juego["tiempo_inicial"] = 60
        datos_juego["vidas_iniciales"] = 5
        datos_juego["puntos_acierto"] = 50
        datos_juego["puntos_error"] = -25
    elif dificultad == "Normal":
        datos_juego["tiempo_inicial"] = 40
        datos_juego["vidas_iniciales"] = 3
        datos_juego["puntos_acierto"] = 100
        datos_juego["puntos_error"] = -50
    elif dificultad == "Dificil":
        datos_juego["tiempo_inicial"] = 20
        datos_juego["vidas_iniciales"] = 2
        datos_juego["puntos_acierto"] = 150
        datos_juego["puntos_error"] = -75
  

