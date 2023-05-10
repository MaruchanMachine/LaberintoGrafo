"""
Alumnos: Figueroa Peña Angela Fabiana 19130188
         Espinoza Vega Enrique Manuel 19130183
         García Gutierrez Juan Antonio 19130158
"""
from queue import Queue
import pygame
from pygame import font

# Configuración de pantalla
ancho = 800
alto = 480
tamaño_celda = 40
color_fondo = (255, 255, 255)
color_camino = (0, 255, 0)
color_inicio = (0, 0, 255)
color_fin = (255, 0, 0)
color_pared = (0, 0, 0)

# Inicializar pygame
pygame.init()
pantalla = pygame.display.set_mode((ancho,alto))
pygame.display.set_caption("Solución del laberinto")
fuente = font.SysFont("Arial",36)

texto = fuente.render("El laberinto no tiene solución",True,(255,255,255))

def construir_grafo(laberinto, filas, columnas, inicio, fin):
    grafo = {}
    for fila in range(filas):
        for col in range(columnas):
            nodo = (fila, col)
            #print(nodo)
            if laberinto[fila][col] == '0':
                vecinos = []
                if col < columnas - 1 and laberinto[fila][col + 1] == '0':
                    vecinos.append((fila, col + 1))
                if fila < filas - 1 and laberinto[fila + 1][col] == '0':
                    vecinos.append((fila + 1, col))
                if col > 0 and laberinto[fila][col - 1] == '0':
                    vecinos.append((fila, col - 1))
                if fila > 0 and laberinto[fila - 1][col] == '0':
                    vecinos.append((fila - 1, col))
                grafo[nodo] = vecinos


    return grafo

def bfs(grafo, inicio, fin):
    """Encuentra el camino más corto desde inicio a fin en el grafo"""
    visitados = set()
    cola = Queue()
    cola.put([inicio])
    while not cola.empty():
        camino = cola.get()
        nodo = camino[-1]
        if nodo == fin:
            return camino
        if nodo in visitados:
            continue
        visitados.add(nodo)
        for ady in grafo[nodo]:
            nuevo_camino = list(camino)
            nuevo_camino.append(ady)
            cola.put(nuevo_camino)

def leer_laberinto(nombre_archivo):
    with open(nombre_archivo) as archivo:
        filas = int(archivo.readline())
        columnas = int(archivo.readline())
        inicio = tuple(map(int, archivo.readline().strip().split(',')))
        fin = tuple(map(int, archivo.readline().strip().split(',')))
        laberinto = []
        for linea in archivo:
            laberinto.append(list(linea.strip()))

    return laberinto, filas, columnas, inicio, fin

laberinto, filas, columnas, inicio, fin = leer_laberinto("laberinto.txt")
grafo = construir_grafo(laberinto, filas, columnas, (inicio[0], inicio[1]), (fin[0], fin[1]))
camino = bfs(grafo, inicio, fin)

# Dibujar el laberinto y la solución
if(camino != None):

    for fila in range(filas):
        for col in range(columnas):
            x = col * tamaño_celda
            y = fila * tamaño_celda
            if laberinto[fila][col] == '+':
                pygame.draw.rect(pantalla, color_pared, (x, y, tamaño_celda, tamaño_celda))
                print('+', end='')
            elif (fila, col) == inicio:
                pygame.draw.rect(pantalla, color_inicio, (x, y, tamaño_celda, tamaño_celda))
                print(' ', end='')
            elif (fila, col) == fin:
                pygame.draw.rect(pantalla, color_fin, (x, y, tamaño_celda, tamaño_celda))
                print(' ', end='')
            elif (fila, col) in camino:
                pygame.draw.rect(pantalla, color_camino, (x, y, tamaño_celda, tamaño_celda))
                print(' ', end='')
            else:
                pygame.draw.rect(pantalla, color_fondo, (x, y, tamaño_celda, tamaño_celda))
                print('0', end='')
        print()
else:
    print("El laberinto es insoluble")
    pantalla.blit(texto, (150,200))

# Actualizar la pantalla
pygame.display.update()

# Esperar hasta que el usuario cierre la ventana
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            quit()