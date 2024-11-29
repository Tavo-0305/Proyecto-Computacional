#!/usr/bin/env python3

"""
Simulación de colisiones entre discos sólidos en 2D.

Este módulo permite realizar simulaciones de colisiones elásticas entre discos dentro 
de un contenedor cerrado. Incluye visualización interactiva en tiempo real y exportación
de datos a un archivo CSV.

Clases principales:
- `Disco`: Representa un disco con posición, velocidad y radio.
- `Escenario`: Define el espacio de simulación y administra las interacciones entre los discos y las paredes.
"""

# Se importan librerías necesarias
import os
import numpy as np 
import matplotlib.pyplot as plt
from datetime import datetime as dt
from matplotlib.patches import Circle
from matplotlib.animation import FuncAnimation

class Disco:
	"""
    Representa un disco sólido en la simulación.

    Atributos:
        radius (float): Radio del disco.
        position (numpy.ndarray): Posición del disco como un array [x, y].
        velocity (numpy.ndarray): Velocidad del disco como un array [vx, vy].
        figure (matplotlib.patches.Circle): Representación gráfica del disco.
        keepVelocity (bool): Si es True, conserva la velocidad durante las colisiones.
        mass (float): Masa del disco, calculada proporcionalmente al radio.
    """
	def __init__(self,posicionX,posicionY,colorDisco,radio = 0.1):
		"""
        Inicializa un disco en la simulación.

        Args:
            posicionX (float): Coordenada X inicial del disco.
            posicionY (float): Coordenada Y inicial del disco.
            colorDisco (str): Color del disco para la visualización.
            radio (float, opcional): Radio del disco. Por defecto es 0.1.
        """
		self.radius = radio
		self.position = np.array([posicionX,posicionY])
		self.velocity = np.array([np.random.uniform(-1,1), np.random.uniform(-1,1)])
		self.figure = Circle(self.position,self.radius, color=colorDisco)
		self.keepVelocity = False
		self.mass = 1 * radio

	def changePosition(self,dt):
		"""
        Actualiza la posición del disco basado en su velocidad.

        Args:
            dt (float): Paso de tiempo.
        """
		self.position += self.velocity * dt
		self.figure.set_center(self.position)
	
	def wallCollision(self,xLimite,yLimite):
		"""
        Detecta y resuelve colisiones con las paredes del contenedor.

        Args:
            xLimite (list): Límites en el eje X [x_min, x_max].
            yLimite (list): Límites en el eje Y [y_min, y_max].
        """
		# Colisión con los límites horizontales
		if self.position[0] - self.radius <= xLimite[0]:
			self.velocity[0] *= -1
			self.position[0] = self.radius
			self.figure.set_center(self.position)
		if self.position[0] + self.radius >= xLimite[1]:
			self.velocity[0] *= -1
			self.position[0] = xLimite[1] - self.radius
			self.figure.set_center(self.position)

		 # Colisión con los límites verticales
		if self.position[1] - self.radius <= yLimite[0]:
			self.velocity[1] *= -1
			self.position[1] = self.radius
			self.figure.set_center(self.position)
		if self.position[1] + self.radius >= yLimite[1]:
			self.velocity[1] *= -1
			self.position[1] = yLimite[1] - self.radius
			self.figure.set_center(self.position)

	def diskCollision(self,otherD):
		"""
        Detecta y resuelve colisiones elásticas con otro disco.

        Args:
            otherD (Disco): Otro objeto de tipo `Disco`.
        """
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
    """
    Administra el espacio de simulación y las interacciones entre discos.

    Atributos:
        dList (list): Lista de objetos `Disco` en la simulación.
        walls (list): Límites del escenario en formato [[x_min, x_max], [y_min, y_max]].
        xLimite (list): Límites en el eje X.
        yLimite (list): Límites en el eje Y.
        screen (list): Elementos gráficos de `matplotlib` para la visualización.
        step (float): Paso de tiempo para cada actualización.
        fileName (str): Nombre del archivo CSV donde se guardan los datos.
    """
    def __init__(self, discos, dt=0.01, anchoEscenario=1, largoEscenario=1):
        """
        Inicializa un nuevo escenario para la simulación.

        Args:
            discos (list): Lista de objetos `Disco`.
            dt (float, opcional): Paso de tiempo para cada actualización. Por defecto es 0.01.
            anchoEscenario (float, opcional): Ancho del contenedor. Por defecto es 1.
            largoEscenario (float, opcional): Largo del contenedor. Por defecto es 1.
        """
        self.dList = discos
        self.walls = [[0, anchoEscenario], [0, largoEscenario]]
        self.xLimite = [0, anchoEscenario]
        self.yLimite = [0, largoEscenario]
        self.screen = self.setScreen()
        self.step = dt
        self.fileName = self.initFile()

    def setScreen(self):
        """
        Configura la visualización gráfica del escenario con `matplotlib`.

        Returns:
            list: Elementos de la figura y ejes para la animación.
        """
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.set_xlim(self.walls[0])
        ax.set_ylim(self.walls[1])
        ax.set_aspect('equal')
        ax.set_facecolor("#ADD8E6")
        timer = ax.text(0.05, 0.95, "Tiempo: 0.00 s", transform=ax.transAxes)
        energy = ax.text(0.05, 0.90, "Energía: 0.00 J", transform=ax.transAxes)
        for d in self.dList:
            ax.add_patch(d.figure)
        return [fig, ax, timer, energy]

    def framing(self, frame):
        """
        Actualiza la posición y estado de los discos para cada cuadro de la simulación.

        Args:
            frame (int): Número de cuadro actual en la simulación.

        Returns:
            list: Elementos gráficos actualizados para el cuadro.
        """
        datos = f"{self.step * frame}"
        energy = 0

        for d in self.dList:
            d.changePosition(self.step)
            datos += f",{d.position[0]},{d.position[1]},{d.velocity[0]},{d.velocity[1]}"
            d.wallCollision(self.xLimite, self.yLimite)
            energy += d.mass * np.linalg.norm(d.velocity) ** 2

        self.updateFile(f"{datos}\n")
        for i, disco in enumerate(self.dList):
            for other in self.dList[i + 1 :]:
                disco.diskCollision(other)

        self.screen[2].set_text(f"Tiempo: {self.step * frame:.2f} s")
        self.screen[3].set_text(f"Energía: {energy:.2f} J")
        return [d.figure for d in self.dList] + [self.screen[2], self.screen[3]]

    def runSimulation(self):
        """
        Ejecuta la simulación y muestra la animación en pantalla.
        """
        simulation = FuncAnimation(self.screen[0], self.framing, blit=True, interval=20, cache_frame_data=False)
        plt.show()

    def initFile(self):
        """
        Inicializa el archivo CSV para guardar los datos de la simulación.

        Returns:
            str: Nombre del archivo CSV creado.
        """
        fileName = "Datos_Simulacion.csv"
        header = "T"
        for i in range(1, len(self.dList) + 1):
            header += f",X_{i},Y_{i},Vx_{i},Vy_{i}"
        with open(fileName, "w") as f:
            f.write(header + "\n")
        return fileName

    def updateFile(self, data):
        """
        Escribe una línea de datos en el archivo CSV.

        Args:
            data (str): Datos a escribir.
        """
        with open(self.fileName, "a") as f:
            f.write(data)
