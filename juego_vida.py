import numpy as np
import pygame
import time
import random

# inicializar pygame
pygame.init()

# constantes para la pantalla
WIDTH, HEIGHT = 800, 800 # Dimensiones en px de la ventana
N = 50 # Numero de celdas en cada dimension
CELL_WIDTH = WIDTH / N # Ancho de cada celda
CELL_HEIGHT = HEIGHT / N # Altura de cada celda
DEATH = 0
ALIVE = 1 

# Configuración de texto para contadores con comic sans obviamente
font = pygame.font.SysFont("Comic sans", 20)
pauseExect = True # El juego inicia en pausa para poder dibujar
generation = 0

gameState = np.zeros((N, N)) # Matriz de N x N con todas las celdas muertas

#Inicializar celdas vivas para probar el juego
#gameState[5, 3] = ALIVE
#gameState[5, 4] = ALIVE
#gameState[5, 5] = ALIVE

screen = pygame.display.set_mode((WIDTH, 840)) # Altura extra para contadores
pygame.display.set_caption("Conway's Game of Life") # Titulo de la ventana

bg = 25, 25, 25 # Color de fondo
screen.fill(bg) # Rellenar la pantalla con el color de fondo, nigga

# Bucle pa que no se cierre la ventana
while True:
    newGameState = np.copy(gameState) # Copia del estado del juego para actualizarlo despues de recorrer todas las celdas
    
    screen.fill(bg) # Rellenar la pantalla con el color de fondo, para borrar la pantalla anterior
    
    #Gestión de Eventos (Mouse y Teclado)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        # Control por teclado
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE: # Espacio para Pausa
                pauseExect = not pauseExect
            if event.key == pygame.K_c:     # C para Limpiar 
                newGameState = np.zeros((N, N))
                generation = 0
                pauseExect = True
            if event.key == pygame.K_r:     # R para Aleatorio 
                newGameState = np.random.randint(2, size=(N, N))
                generation = 0

        # Insertar células con el Mouse
        mouseClick = pygame.mouse.get_pressed()
        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            if posY < HEIGHT: # Evitar dibujar en la zona de contadores

                celdaX = min(int(posX / CELL_WIDTH), N - 1)
                celdaY = min(int(posY / CELL_HEIGHT), N - 1)
                
                # Clic izquierdo revive, derecho mata 
                if mouseClick[0]:
                    newGameState[celdaX, celdaY] = ALIVE
                elif mouseClick[2]:
                    newGameState[celdaX, celdaY] = DEATH

    # Variables para contar células
    alive_count = 0
    dead_count = 0

    for y in range (0, N):
        for x in range(0, N):
            
            # contadores
            if gameState[x, y] == ALIVE: alive_count += 1
            else: dead_count += 1

            if not pauseExect:
                #Calcular el numero de vecinos, la parte de % es para simular un mundo toroidal (pacman)
                cell_neighbors = gameState[(x-1) % N, (y-1) % N] + \
                                 gameState[(x)   % N, (y-1) % N] + \
                                 gameState[(x+1) % N, (y-1) % N] + \
                                 gameState[(x-1) % N, (y)   % N] + \
                                 gameState[(x+1) % N, (y)   % N] + \
                                 gameState[(x-1) % N, (y+1) % N] + \
                                 gameState[(x)   % N, (y+1) % N] +  \
                                 gameState[(x+1) % N, (y+1) % N]
                                 
                #Reglas del juego de la vida
                
                #regla 1: Una celda muerta con exactamente 3 vecinos vivos, "revive"
                if gameState[x, y] == DEATH and cell_neighbors == 3:
                    newGameState[x, y] = ALIVE

                #regla 2: Una celda viva con menos de 2 o más de 3 vecinos vivos, "muere"
                elif gameState[x, y] == ALIVE and (cell_neighbors < 2 or cell_neighbors > 3):
                    newGameState[x, y] = DEATH

            # Crear los cuadros de cada celda
            cuadro = [((x) * CELL_WIDTH, y * CELL_HEIGHT),
                    ((x+1) * CELL_WIDTH, y * CELL_HEIGHT),
                    ((x+1) * CELL_WIDTH, (y+1) * CELL_HEIGHT),
                    ((x) * CELL_WIDTH, (y+1) * CELL_HEIGHT)]
            
            # Dibujar las celdas para cada coordenada, en funcion de su estado
            if newGameState[x, y] == DEATH:
                pygame.draw.polygon(screen, (128, 128, 128), cuadro, 1)
            else:
                pygame.draw.polygon(screen, (255, 255, 255), cuadro, 0)
    
    # Incrementar generación
    if not pauseExect and alive_count > 0:
        generation += 1

    # Cotadores y controles
    INFO = font.render(f"Gen: {generation}  |  Vivas: {alive_count}  |  Muertas: {dead_count}", True, (255, 255, 255))
    screen.blit(INFO, (10, HEIGHT + 10))
    CONTROLS = font.render("[Espacio]: Pausa | [C]: Limpiar | [R]: Aleatorio", True, (255, 255, 255))
    screen.blit(CONTROLS, (380, HEIGHT + 10))

    gameState = np.copy(newGameState)
            
    pygame.display.flip()
    time.sleep(0.1) #Velocidad de generaciones / muertes