# Paso 1: definir el estado de juego. 
# Paso 1.1: Crear el tablero inicial del juego usando matrices.
FILAS = 5
COLUMNAS = 5

def crear_tablero(filas, columnas):
    return [["." for _ in range(columnas)] for _ in range(filas)]

tablero_inicial = crear_tablero(FILAS, COLUMNAS)

def agregar_paredes(tablero, lista_paredes):
    for fila, columna in lista_paredes:
        tablero[fila][columna] = "#"

paredes = [(1,1), (2,1), (2,3), (2,4), (4,0), (4,1), (4,3)]
agregar_paredes(tablero_inicial, paredes)


# Paso 1.2: definir los jugadores
RATON_INICIAL = (2, 2)
GATO_INICIAL = (4, 3)

# Paso 1.3: definir turno inicial
TURNO_RATON = True


# Paso 2: Mostrar el tablero
def mostrar_tablero(tablero, raton_pos, gato_pos):
    for i in range(len(tablero)):
        for j in range(len(tablero[i])):
            if (i, j) == raton_pos:
                print("R", end=" ")
            elif (i, j) == gato_pos:
                print("G", end=" ")
            else:
                print(tablero[i][j], end=" ")
        print()
    print()


# Paso 3: movimientos válidos
MOVIMIENTOS = [
    (-1, 0),  # arriba
    (1, 0),   # abajo
    (0, -1),  # izquierda
    (0, 1)    # derecha
]

def obtener_movimientos_validos(tablero, posicion):
    movimientos_validos = []

    filas = len(tablero)
    columnas = len(tablero[0])

    for movimiento in MOVIMIENTOS:
        nueva_fila = posicion[0] + movimiento[0]
        nueva_columna = posicion[1] + movimiento[1]

        if 0 <= nueva_fila < filas and 0 <= nueva_columna < columnas:
            if tablero[nueva_fila][nueva_columna] != "#":
                movimientos_validos.append((nueva_fila, nueva_columna))

    return movimientos_validos


# Paso 4: función de movimiento aleatorio (ratón)
import random

def mover_aleatorio(tablero, posicion):
    opciones = obtener_movimientos_validos(tablero, posicion)

    if opciones:
        return random.choice(opciones)
    else:
        return posicion


# Paso 5: Minimax

def estado_terminal(raton_pos, gato_pos):  #define una funcion que recibe las posiciones iniciales del gato y del raton. 
    return raton_pos == gato_pos           #compara ambas posiciones y devuelve true o false si las posiciones coinciden. 


def distancia_manhattan(pos1, pos2):  #¿Por que manhattan? --> Porque en el juego defini que no pueden haber movimientos diagonales, solo pueden ser horizontales o verticales. 
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])  #Nos permite decidir la minima cantidad de pasos que el gato necesitaria para atrapar al raton. Convierte las coordenadas ((tuplas)) en un parametro numerico especifico. 

#FUNCION DE EVALUACION: le asigna un valor numerico a cada estado del juego, dependiendo de la posicion del gato y del raton.
# Si el gato atrapa al raton, el valor es 100 (el mejor estado posible para el gato). Si no, se calcula la distancia manhattan entre el gato y el raton, y se devuelve su negativo (porque queremos que el gato se acerque al raton, y un numero mas grande representa un estado mejor para el gato).
# El valor de la funcion de evaluacion es lo que el algoritmo minimax va a usar para comparar los diferentes estados del juego y decidir cual es el mejor movimiento para el gato.
#Mi función de evaluación combina una evaluación exacta para estados terminales y una heurística basada en la distancia Manhattan negativa para estados intermedios. 
def evaluar_estado(raton_pos, gato_pos):
    if estado_terminal(raton_pos, gato_pos):
        return 100  # el gato ganó  #definimos 100 como el mejor estado posible para el gato, pero podria ser 999, 1000, o cualquiero numero lo suficientemente grande. 
#Debe ser el numero mas grande porque el gato es MAX, y MAX siempre elige el numero mas grande.
    return -distancia_manhattan(raton_pos, gato_pos)
#¿por que distancia manhattan es negativo? --> porque el algoritmo va a comparar numeros y MAX va a elegir el mayor numero entre todos.
#Por ejemplo, sin en distancia manhattan nos da una dist. de 1 y una dist. de 5 , el MAX va a elegir el 5 , pero significaria que se alejando del raton, y lo que queremos es que se acerque.
#Por eso cambiamos a negativo, Minimax compara: -1 > -5, y el algoritmo elegiria -1 (el mayor), y el gato se acercaria al raton.  

def minimax(tablero, raton_pos, gato_pos, profundidad, es_turno_gato):  #Obs: minimax va a retornar un numero que representa que tan bueno es el estado del juego. 
    if profundidad == 0 or estado_terminal(raton_pos, gato_pos):  #caso base: si la profundidad es cero o el gato atrapo al raton, se evalua el estado actual del juego.
        return evaluar_estado(raton_pos, gato_pos)

    if es_turno_gato:  # MAX (gato)
        mejor_valor = float("-inf")  #inicializamos el mejor valor como el menor numero posible, porque el gato quiere maximizar, y cualquier valor sera mejor que -inf.
        movimientos = obtener_movimientos_validos(tablero, gato_pos) 

        for movimiento in movimientos:
            valor = minimax(
                tablero,
                raton_pos,
                movimiento,
                profundidad - 1,
                False
            )

            mejor_valor = max(mejor_valor, valor)

        return mejor_valor  #hojas de minimax

    else:  # MIN (ratón)
        mejor_valor = float("inf")
        movimientos = obtener_movimientos_validos(tablero, raton_pos)

        for movimiento in movimientos:
            valor = minimax(
                tablero,
                movimiento,
                gato_pos,
                profundidad - 1,
                True
            )

            mejor_valor = min(mejor_valor, valor)

        return mejor_valor


def mejor_movimiento_gato(tablero, raton_pos, gato_pos, profundidad):
    mejor_valor = float("-inf")
    mejor_mov = gato_pos

    movimientos = obtener_movimientos_validos(tablero, gato_pos)

    for movimiento in movimientos:
        valor = minimax(
            tablero,
            raton_pos,
            movimiento,
            profundidad - 1,
            False
        )

        if valor > mejor_valor:
            mejor_valor = valor
            mejor_mov = movimiento

    return mejor_mov #devuelve el mejor movimiento que el gato puede hacer, considerando las posibles respuestas del raton.


# -------------------------
# BUCLE PRINCIPAL DEL JUEGO
# -------------------------

raton_pos = RATON_INICIAL
gato_pos = GATO_INICIAL
turno_raton = TURNO_RATON

PROFUNDIDAD = 3  # profundidad de búsqueda del minimax
# Implementación del límite de turnos para evitar bucle infinito
MAX_TURNOS = 50
turnos = 0

while turnos < MAX_TURNOS:

    mostrar_tablero(tablero_inicial, raton_pos, gato_pos)

    if turno_raton:
        raton_pos = mover_aleatorio(tablero_inicial, raton_pos)
    else:
        gato_pos = mejor_movimiento_gato(      #se usa MINIMAX para que el gato elija el mejor movimiento posible, considerando las posibles respuestas del raton.
            tablero_inicial,
            raton_pos,
            gato_pos,
            PROFUNDIDAD
        )

    if raton_pos == gato_pos:
        mostrar_tablero(tablero_inicial, raton_pos, gato_pos)
        print("¡El gato atrapó al ratón!")
        break

    turno_raton = not turno_raton
    turnos += 1

else:
    mostrar_tablero(tablero_inicial, raton_pos, gato_pos)
    print("¡Empate! El ratón escapó después de demasiados turnos.")