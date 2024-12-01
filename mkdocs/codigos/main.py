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

# Configuración de la cuadrícula para posicionar los discos
largoMatriz = 1
while True:
    if largoMatriz * largoMatriz < cantidadDiscos:
        largoMatriz += 1
    else:
        break

distanciaHorizontal = espacioHorizontal / (largoMatriz + 1)
distanciaVertical = espacioVertical / (largoMatriz + 1)
posiciones = np.zeros([largoMatriz * largoMatriz, 2])  # Inicializa posiciones en una cuadrícula
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

# Crea los objetos `Disco` con colores y radios asignados aleatoriamente
discos = [0] * cantidadDiscos
for i in range(cantidadDiscos):
    if i % 4 == 0:
        color = 'blue'
    elif i % 4 == 1:
        color = 'red'
    elif i % 4 == 2:
        color = 'green'
    else:
        color = 'orange'

    radio = np.random.uniform(0.01, 0.05)  # Radio aleatorio entre 0.01 y 0.05
    discos[i] = Disco(posiciones[i][0], posiciones[i][1], color, radio)

# Configuración del escenario de simulación
simulacion = Escenario(discos, 0.005)  # Paso de tiempo de 0.005 unidades

# Ejecución de la simulación
simulacion.runSimulation()
