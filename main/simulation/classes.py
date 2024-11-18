#!/usr/bin/env python3

'''
En este documento creamos las clases necesarias que vamos a necesitar para correr la simulación
La idea es llamar las clases en el main.py y correr la simulación ahí
'''
#Primero se importan las librerias necesarias:
import os
import numpy as np 
import matplotlib.pyplot as plt
from datetime import datetime as dt
from matplotlib.patches import Circle
from matplotlib.animation import FuncAnimation

#Se definen las clases:
class Disco:
	def __init__(self,xCoord,yCoord,colorDisco,radio = 0.07):
		self.radio = radio
		self.posicion = np.array([xCoord,yCoord])
		self.velocidad = np.array([np.random.uniform(-1,1), np.random.uniform(-1,1)])
		self.figura = Circle(self.posicion,self.radio, color=colorDisco)
		#Suponiendo que todos los discos tengan igual masa
		self.masa = 1

	def changePosition(self,dt):
		self.posicion[0] += self.velocidad[0] * dt
		self.posicion[1] += self.velocidad[1] * dt
		self.figura.set_center(self.posicion)

	def wallCollision(self,xLimite,yLimite):
		if self.posicion[0] - self.radio <= xLimite[0] or self.posicion[0] + self.radio >= xLimite[1]:
			self.velocidad[0] *= -1
		if self.posicion[1] - self.radio <= yLimite[0] or self.posicion[1] + self.radio >= yLimite[1]:
			self.velocidad[1] *= -1

	def diskCollision(self,discoExt):
		#Determina la distancia entre el centro de los dos discos
		distCentros = np.linalg.norm(self.posicion - discoExt.posicion)

		#Si esa distancia es menor o igual a la suma de los radios, estan colisionando
		if distCentros <= self.radio + discoExt.radio:
			#Para el disco "self"
			masaRelacion = 2 * discoExt.masa / (self.masa + discoExt.masa)
			difPos = discoExt.posicion - self.posicion
			difVel = discoExt.velocidad - self.velocidad
			self.velocidad += (masaRelacion * np.dot(difVel,difPos) / np.dot(difPos,difPos)) * difPos

			#Para el disco externo
			masaRelacion = 2 * self.masa / (self.masa + discoExt.masa)
			difPos *= -1
			difVel *= -1
			discoExt.velocidad += (masaRelacion * np.dot(difVel,difPos) / np.dot(difPos,difPos)) * difPos

class Escenario:
	def __init__(self, discos, anchoEscenario = 1, largoEscenario = 1):
		self.discos = discos
		self.yLimite = [0, largoEscenario]
		self.xLimite = [0, anchoEscenario]
		self.espacio = self.setSpace()
		self.step = 0.01
		self.time = 0
		self.fileName = self.initFile()
		
	def setSpace(self):
		fig, ax = plt.subplots(figsize=(8, 8))
		ax.set_xlim(0, 1)
		ax.set_ylim(0, 1)
		ax.set_aspect('equal')
		ax.set_xticks([0,1])
		ax.set_yticks([0,1])
		ax.set_facecolor('whitesmoke')  
		ax.set_title("Simulacion de la dinamica molecular de discos solidos", fontsize=12, fontweight='bold')
		for d in self.discos:
			ax.add_patch(d.figura)

		return [fig, ax]

	def framing(self,frame):
		#Linea de datos de los discos en el tiempo T
		datos = f"{self.time}"

		#Para cada disco
		for d in self.discos:
			#Actualiza su posicion al siguiente step
			d.changePosition(self.step)

			#Agrega la posicion X a la linea de datos
			datos += f",{d.posicion[0]},{d.posicion[1]},{d.velocidad[0]},{d.velocidad[1]}"
			
			#Comprueba colisiones con las paredes
			d.wallCollision(self.xLimite,self.yLimite)
		
		self.updateFile(f"{datos}\n")

		contador = 0
		while contador < len(self.discos):
			for i in range(contador + 1,len(self.discos)):
				self.discos[contador].diskCollision(self.discos[i])
			contador += 1

		self.time += self.step
		
		return [d.figura for d in self.discos] 

	def runSimulation(self):
		#Ejecuta la simulacion
		simulacion = FuncAnimation(self.espacio[0],self.framing,frames=range(100), blit=True, interval=10)
		plt.show()

	def initFile(self):
		#Genera la ruta con el nombre del archivo
		#fileName = os.path.join(f"Simulacion {dt.now().strftime('%Y%m%d-%H%M')}.csv")
		fileName = "Datos_Simulacion.csv"

		#Genera el titular que va en la primera linea del archivo
		titular = "T"
		for i in range(1,len(self.discos) + 1):
			titular += f",X_{i},Y_{i},Vx_{i},Vy_{i}"
		titular += "\n"
		
		#Crea el archivo y le agrega el titular
		with open(fileName,"w") as file:
			file.write(titular)
		
		#Retorna el nombre del archivo
		return fileName

	def updateFile(self,datos):
		#Este método se encarga de generar un archivo .csv que guarde los datos de posición, velocidad y tiempos para realizar un pequeño análisis de datos del comportamiento de las colisiones
		with open(self.fileName,"a") as file:
			file.write(datos)
