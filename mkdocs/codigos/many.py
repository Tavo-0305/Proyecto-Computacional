#!/usr/bin/env python3

"""
Simulación de colisiones elásticas entre múltiples discos en un espacio cerrado.

Este script configura y ejecuta una simulación de colisiones elásticas utilizando
los objetos `Disco` y `Escenario` definidos en el módulo `classes`. Se generan 
aleatoriamente posiciones iniciales para un conjunto de discos y se les asignan
colores y radios variados. La simulación se ejecuta y se visualiza en tiempo real.

Dependencias:
- numpy
- classes (debe incluir las clases `Disco` y `Escenario`).
"""

import numpy as np
from classes import Disco, Escenario

# Definición del espacio de simulación y parámetros iniciales
espacioHorizontal = 1.0  # Ancho del contenedor
espacioVertical = 1.0    # Alto del contenedor
cantidadDiscos = 50      # Número de discos en la simulación

# Define el tamaño de la cuadrícula para posicionar los discos
largoMatriz = 1
while True:
    if largoMatriz * largoMatriz < cantidadDiscos:
        largoMatriz += 1
    else:
        break

# Define las distancias verticales y horizontales de separación entre los discos
distanciaHorizontal = espacioHorizontal / (largoMatriz + 1)
distanciaVertical = espacioVertical / (largoMatriz + 1)

# Inicializa la matriz de posiciones y asigna la posición inicial
posiciones = np.zeros([largoMatriz * largoMatriz, 2])
posiciones[0] = [distanciaHorizontal, distanciaVertical]

# Calcula las posiciones iniciales distribuidas uniformemente en la cuadrícula
for i in range(1, largoMatriz * largoMatriz):
    if round(posiciones[i - 1][0] + distanciaHorizontal, 2) >= espacioHorizontal:
        posiciones[i][0] = distanciaHorizontal
        posiciones[i][1] = distanciaVertical + posiciones[i - 1][1]
    else:
        posiciones[i][0] = distanciaHorizontal + posiciones[i - 1][0]
        posiciones[i][1] = posiciones[i - 1][1]

# Selecciona aleatoriamente las posiciones iniciales de los discos
indicesAleatorios = np.random.choice(largoMatriz * largoMatriz, cantidadDiscos, replace=False)
posiciones = posiciones[indicesAleatorios]

# Crea los objetos `Disco` con radios asignados aleatoriamente
discos = [0] * cantidadDiscos # Lista vacía donde se almacenan los objetos 'Disco'
for i in range(cantidadDiscos):

    # Define los colores de los discos en un orden secuencial
    if i % 5 == 0:
        color = '#0033ff' # Color azul
    elif i % 5 == 1:
        color = '#cc0000' # Color rojo
    elif i % 5 == 2:
        color = '#009933' # Color verde
    elif i % 5 == 3:
        color = '#ffcc33' # Color amarillo
    else:
        color = '#990099' # Color morado

    radio = 0.01
    #radio = np.random.uniform(0.04, 0.05)  # Radio aleatorio entre 0.01 y 0.05
    discos[i] = Disco(posiciones[i][0], posiciones[i][1], color, radio)

# Configuración del escenario de simulación
simulacion = Escenario(discos, 0.01,espacioHorizontal,espacioVertical,timerVisible=True)  # Paso de tiempo de 0.01 unidades

# Ejecución de la simulación
simulacion.runSimulation()
