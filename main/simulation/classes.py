'''
En este documento creamos las clases necesarias que vamos a necesitar para correr la simulación
La idea es llamar las clases en el main.py y correr la simulación ahí
'''
#Primero se importan las librerias necesarias:
import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib.animation import FuncAnimation
#Se definen las clases:
class Disco:
	def __init__(self,radio,x_coord,y_coord):
		pass
	def manejo_pos(self,dt):
		pass
	def detectar_colision(self,disco_externo):
		pass
	def resolver_colisiones(self,disco_externo):
		pass
	def generador_datos(self,x_coord,y_coord):
		#Este método se encarga de generar un archivo .csv que guarde los datos de posición, velocidad y tiempos para realizar un pequeño análisis de datos del comportamiento de las colisiones
		pass
class Animacion:
	def __init__(self,dimension,array_discos):
		pass
	def framing(self):
		pass
	def run(self)
		pass
