#!/usr/bin/env python3

"""
Simulación simplificada de colisiones elásticas entre 4 discos en un espacio cerrado.

Este script configura y ejecuta una simulación de colisiones elásticas utilizando
los objetos `Disco` y `Escenario` definidos en el módulo `classes`. Las posiciones
iniciales de los discos se asignan de manera aleatoria, y todos los discos tienen
el mismo radio.

Dependencias:
- numpy
- classes (debe incluir las clases `Disco` y `Escenario`).
"""

import numpy as np
from classes import Disco, Escenario

# Definición del espacio de simulación y parámetros iniciales
espacioHorizontal = 1.0  # Ancho del contenedor
espacioVertical = 1.0    # Alto del contenedor
cantidadDiscos = 4       # Número de discos en la simulación
radioDiscos = 0.10       # Radio común para todos los discos

# Generación de posiciones iniciales aleatorias para los discos
# Asegurando que los discos no estén superpuestos
posiciones = []
while len(posiciones) < cantidadDiscos:
    nueva_pos = np.random.uniform(radioDiscos, espacioHorizontal - radioDiscos, 2)
    if all(np.linalg.norm(nueva_pos - p) > 2 * radioDiscos for p in posiciones):
        posiciones.append(nueva_pos)

# Crea los objetos `Disco` con colores asignados cíclicamente
colores = ['blue', 'red', 'green', 'orange']
discos = [
    Disco(pos[0], pos[1], colores[i % len(colores)], radioDiscos)
    for i, pos in enumerate(posiciones)
]

# Configuración del escenario de simulación
simulacion = Escenario(discos, 0.01)

# Ejecución de la simulación
simulacion.runSimulation()
