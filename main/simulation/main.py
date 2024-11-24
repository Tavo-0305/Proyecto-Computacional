#!/usr/bin/env python3

import numpy as np
from classes import Disco, Escenario
#Creamos los objetos de tipo disco

espacioHorizontal = 1.0
espacioVertical = 1.0
cantidadDiscos = 50

largoMatriz = 1
while True:
    if largoMatriz * largoMatriz < cantidadDiscos:
        largoMatriz +=1
    else:
        break

distanciaHorizontal = espacioHorizontal / (largoMatriz + 1)
distanciaVertical = espacioVertical / (largoMatriz + 1)
posiciones = np.zeros([largoMatriz * largoMatriz,2])
posiciones[0] = [distanciaHorizontal,distanciaVertical]

contador = 1
for i in range(1,largoMatriz * largoMatriz):
    if round(posiciones[i-1][0] + distanciaHorizontal,2) >= espacioHorizontal:
        posiciones[i][0] = distanciaHorizontal
        posiciones[i][1] = distanciaVertical + posiciones[i-1][1]
    else:
        posiciones[i][0] = distanciaVertical + posiciones[i-1][0]
        posiciones[i][1] = posiciones[i-1][1]

indicesAleatorios = np.random.choice(largoMatriz * largoMatriz,cantidadDiscos,False)
posiciones = posiciones[indicesAleatorios]

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
    
    radio = np.random.uniform(0.01,0.05)

    discos[i] = Disco(posiciones[i][0],posiciones[i][1],color,radio)

#Objeto de tipo animación
simulacion = Escenario(discos,0.005) #Recuerde que la dimensión es unitaria
#Corrermos la simulacion
simulacion.runSimulation()
#Además debemos implementar un script para crear un archivo .csv con los datos de los discos
