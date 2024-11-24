#!/usr/bin/env python3

'''
En este documento creamos las clases necesarias que vamos a necesitar para correr la simulación
La idea es llamar las clases en el main.py y correr la simulación ahí
'''
# Primero se importan las librerias necesarias:
import os
import numpy as np 
import matplotlib.pyplot as plt
from datetime import datetime as dt
from matplotlib.patches import Circle
from matplotlib.animation import FuncAnimation

# Se definen las clases:
class Disco:
	def __init__(self,posicionX,posicionY,colorDisco,radio = 0.1):
		self.radius = radio
		self.position = np.array([posicionX,posicionY])
		self.velocity = np.array([np.random.uniform(-1,1), np.random.uniform(-1,1)])
		self.figure = Circle(self.position,self.radius, color=colorDisco)
		self.keepVelocity = False
		self.mass = 1 * radio

	# Funcion que actualiza la posicion del disco en un paso de tiempo dt
	def changePosition(self,dt):
		# Actualiza los valores del numpy array de posicion
		self.position += self.velocity * dt
		# Actualiza la posicion de la figura en la simulacion
		self.figure.set_center(self.position)
	
	# Comprueba y resuelve una colision con los limites de la caja
	def wallCollision(self,xLimite,yLimite):
		#Revisa la colision con los limites horizontales de la caja
		if self.position[0] - self.radius <= xLimite[0]:
			#Ajusta la posicion del disco e invierte la velocidad horizontal
			self.velocity[0] *= -1
			self.position[0] = self.radius
			# Actualiza la posicion de la figura en la simulacion
			self.figure.set_center(self.position)

		if self.position[0] + self.radius >= xLimite[1]:
			#Ajusta la posicion del disco e invierte la velocidad horizontal
			self.velocity[0] *= -1
			self.position[0] = xLimite[1] - self.radius
			# Actualiza la posicion de la figura en la simulacion
			self.figure.set_center(self.position)

		#Revisa la colision con los limites verticales de la caja
		if self.position[1] - self.radius <= yLimite[0]:
			#Ajusta la posicion del disco e invierte la velocidad horizontal
			self.velocity[1] *= -1
			self.position[1] = self.radius
			# Actualiza la posicion de la figura en la simulacion
			self.figure.set_center(self.position)
			
		if self.position[1] + self.radius >= yLimite[1]:
			#Ajusta la posicion del disco e invierte la velocidad horizontal
			self.velocity[1] *= -1
			self.position[1] = yLimite[1] - self.radius
			# Actualiza la posicion de la figura en la simulacion
			self.figure.set_center(self.position)

	# Comprueba y resuelve una colision con otro disco
	def diskCollision(self,otherD):
		# Determina la distancia entre el centro de los dos discos
		distance = np.linalg.norm(self.position - otherD.position)

		#Si la distancia es menor o igual a la suma de los radios, estan colisionando
		if distance <= self.radius + otherD.radius:
			#Obtiene la distancia de superposicion entre los discos
			overlap = self.radius + otherD.radius - distance

			#Obtiene el vector unitario que contiene los valores de superposicion
			overlapVector = overlap * (self.position - otherD.position) / distance

			#Ajusta las posiciones de los discos para evitar la superposicion
			self.position +=  overlapVector
			otherD.position -= overlapVector

			#Actualiza las posiciones en la simulacion
			self.figure.set_center(self.position)
			otherD.figure.set_center(otherD.position)

			#Para el disco "self"
			massRelation = 2 * otherD.mass / (self.mass + otherD.mass)
			difPos = otherD.position - self.position
			difVel = otherD.velocity - self.velocity
			self.velocity += (massRelation * np.dot(difVel,difPos) / np.dot(difPos,difPos)) * difPos

			#Para el disco "otherD"
			massRelation = 2 * self.mass / (self.mass + otherD.mass)
			difPos *= -1
			difVel *= -1
			otherD.velocity += (massRelation * np.dot(difVel,difPos) / np.dot(difPos,difPos)) * difPos

class Escenario:
	def __init__(self, discos,dt = 0.01, anchoEscenario = 1, largoEscenario = 1):
		self.dList = discos
		self.walls = [[0, anchoEscenario], [0, largoEscenario]]
		self.yLimite = [0, largoEscenario]
		self.xLimite = [0, anchoEscenario]
		self.screen = self.setScreen()
		self.step = dt
		self.fileName = self.initFile()
		
	def setScreen(self):
		fig, ax = plt.subplots(figsize=(8, 8))
		ax.set_xlim(self.walls[0])
		ax.set_ylim(self.walls[1])
		ax.set_aspect('equal')
		ax.set_xticks(self.walls[0])
		ax.set_yticks(self.walls[1])
		ax.set_facecolor("#ADD8E6")  
		ax.set_title("Simulacion de la dinamica molecular de discos solidos", fontsize=12, fontweight='bold')
		# Agregar un contador en pantalla
		timer = ax.text(0.05, 0.95, "Tiempo: 0.00 s", transform=ax.transAxes, fontsize=12, color="black", ha="left")
		energy = ax.text(0.05, 0.90, "Energia: 0.00 J", transform=ax.transAxes, fontsize=12, color="black", ha="left")
		for d in self.dList:
			ax.add_patch(d.figure)

		return [fig, ax, timer, energy]

	def framing(self,frame):
		#Linea de datos de los discos en el tiempo T
		datos = f"{self.step * frame}"
		
		energy = 0

		#Para cada disco
		for d in self.dList:
			#Actualiza su posicion al siguiente step
			d.changePosition(self.step)

			#Agrega la posicion X a la linea de datos
			datos += f",{d.position[0]},{d.position[1]},{d.velocity[0]},{d.velocity[1]}"
			
			#Comprueba colisiones con las paredes
			d.wallCollision(self.xLimite,self.yLimite)

			#Suma la energia
			energy += d.mass * np.linalg.norm(d.velocity) ** 2

		#Agrega los datos de los discos al archivo
		self.updateFile(f"{datos}\n")

		#Ciclo que comprueba las colisiones entre discos
		contador = 0
		while contador < len(self.dList):
			for i in range(contador + 1,len(self.dList)):
				self.dList[contador].diskCollision(self.dList[i])
			contador += 1
		
		#Actualiza el timer en pantalla
		self.screen[2].set_text(f"Tiempo: {self.step * frame:.2f} s")
		self.screen[3].set_text(f"Energia: {energy:.2f} J")
		
		return [d.figure for d in self.dList]  + [self.screen[2]] + [self.screen[3]] 

	def runSimulation(self):
		#Ejecuta la simulacion
		simulacion = FuncAnimation(self.screen[0],self.framing, blit=True, interval=20, cache_frame_data=False)
		plt.show()

	def initFile(self):
		#Genera la ruta con el nombre del archivo
		#fileName = os.path.join(f"Simulacion {dt.now().strftime('%Y%m%d-%H%M')}.csv")
		fileName = "Datos_Simulacion.csv"

		#Genera el titular que va en la primera linea del archivo
		titular = "T"
		for i in range(1,len(self.dList) + 1):
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
