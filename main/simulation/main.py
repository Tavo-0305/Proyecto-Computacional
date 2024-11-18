#!/usr/bin/env python3

from classes import Disco, Escenario
#Creamos los objetos de tipo disco
disco1 = Disco(0.2,0.2,'red')
disco2 = Disco(0.8,0.8,'blue')
disco3 = Disco(0.8,0.2,'green')
disco4 = Disco(0.2,0.8,'orange')
#Objeto de tipo animación
simulacion = Escenario([disco1,disco2,disco3,disco4]) #Recuerde que la dimensión es unitaria
#Corrermos la simulacion
simulacion.runSimulation()
#Además debemos implementar un script para crear un archivo .csv con los datos de los discos
