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
import numpy as np 
import matplotlib.pyplot as plt
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
		self.mass = 1 * radio

	def changePosition(self,dt):
		"""
        Actualiza la posición del disco basado en su velocidad.

        Args:
            dt (float): Paso de tiempo.
        """
		self.position += self.velocity * dt
		self.figure.set_center(self.position)
	
	def wallCollision(self,walls):
		"""
        Detecta y resuelve colisiones con las paredes del contenedor.

        Args:
            walls (list): Límites del escenario en formato [[x_min, x_max], [y_min, y_max]].
        """
		# Colisión con los límites horizontales
		if self.position[0] - self.radius <= walls[0][0]:
			self.velocity[0] *= -1
			self.position[0] = self.radius
			self.figure.set_center(self.position)
		if self.position[0] + self.radius >= walls[0][1]:
			self.velocity[0] *= -1
			self.position[0] = walls[0][1] - self.radius
			self.figure.set_center(self.position)

		 # Colisión con los límites verticales
		if self.position[1] - self.radius <= walls[1][0]:
			self.velocity[1] *= -1
			self.position[1] = self.radius
			self.figure.set_center(self.position)
		if self.position[1] + self.radius >= walls[1][1]:
			self.velocity[1] *= -1
			self.position[1] = walls[1][1] - self.radius
			self.figure.set_center(self.position)

	def diskCollision(self,otherD):
		"""
        Detecta y resuelve colisiones elásticas con otro disco.

        Args:
            otherD (Disco): Otro objeto de tipo `Disco`.
        """
        # Calcula la distancia entre los centros de los dos discos
		distance = np.linalg.norm(self.position - otherD.position)

		# Si la distancia es menor o igual a la suma de los radios, están colisionando
		if distance <= self.radius + otherD.radius:
			# Obtiene la distancia de superposición entre los discos
			overlap = self.radius + otherD.radius - distance

			# Obtiene el vector unitario del vector de superposición
			overlapVector = overlap * (self.position - otherD.position) / distance

			# Ajusta las posiciones de los discos para evitar la superposición
			self.position +=  overlapVector
			otherD.position -= overlapVector

			# Actualiza las posiciones en la simulación
			self.figure.set_center(self.position)
			otherD.figure.set_center(otherD.position)

			# Asigna la nueva velocidad para el disco "self"
			massRelation = 2 * otherD.mass / (self.mass + otherD.mass)
			difPos = otherD.position - self.position
			difVel = otherD.velocity - self.velocity
			self.velocity += (massRelation * np.dot(difVel,difPos) / np.dot(difPos,difPos)) * difPos

			# Asigna la nueva velocidad para el disco "otherD"
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
        screen (list): Elementos gráficos de `matplotlib` para la visualización.
        step (float): Paso de tiempo para cada actualización.
        fileName (str): Nombre del archivo CSV donde se guardan los datos.
    """
    def __init__(self, discos, dt=0.01, anchoEscenario=1, largoEscenario=1, timerVisible=True):
        """
        Inicializa un nuevo escenario para la simulación.

        Args:
            discos (list): Lista de objetos `Disco`.
            dt (float, opcional): Paso de tiempo para cada actualización. Por defecto es 0.01.
            anchoEscenario (float, opcional): Ancho del contenedor. Por defecto es 1.
            largoEscenario (float, opcional): Largo del contenedor. Por defecto es 1.
            timerVisible (bool, opcional): Visibilidad del paso del tiempo en la simulación. Por defecto es True.
        """
        self.dList = discos
        self.walls = [[0, anchoEscenario], [0, largoEscenario]]
        self.screen = self.setScreen()
        self.step = dt
        self.fileName = self.initFile()
        self.timerVisible = timerVisible

    def setScreen(self):
        """
        Configura la visualización gráfica del escenario con `matplotlib`.

        Returns:
            list: Elementos de la figura y ejes para la animación.
        """
        # Crea el espacio de visualización de la simulación
        fig, ax = plt.subplots(figsize=(8, 8))

        #Define el tamaño de la zona de simulación
        ax.set_xlim(self.walls[0])
        ax.set_ylim(self.walls[1])
        ax.set_aspect('equal') # Define la relación de aspecto

        # Configura la zona de simulación
        ax.set_facecolor("#000000") # Color zona simulacion (negro)
        fig.patch.set_facecolor("#000000") #Color ventana (negro)

        #Cambia el color de los ejes a blanco
        ax.spines['top'].set_color('white')
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.spines['right'].set_color('white')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        
        # Crea el timer dentro de una caja transparente
        timer = ax.text(0.02, 0.96, "Tiempo: 0.00 s", transform=ax.transAxes, color="white", fontsize=12,
        bbox=dict(facecolor="black", alpha=0.7, edgecolor="white", boxstyle="round,pad=0.3"))

        # Agrega los discos en su posicion inicial
        for disc in self.dList:
            ax.add_patch(disc.figure)
        
        return [fig, timer]

    def framing(self, frame):
        """
        Actualiza la posición y estado de los discos para cada cuadro de la simulación.

        Args:
            frame (int): Número de cuadro actual en la simulación.

        Returns:
            list: Elementos gráficos actualizados para el cuadro.
        """
        datos = f"{self.step * frame}"

        for d in self.dList:
            d.changePosition(self.step)
            datos += f",{d.position[0]},{d.position[1]},{d.velocity[0]},{d.velocity[1]}"
            d.wallCollision(self.walls)

        self.updateFile(f"{datos}\n")
        for i, disco in enumerate(self.dList):
            for other in self.dList[i + 1 :]:
                disco.diskCollision(other)
        
        self.screen[1].set_text(f"Tiempo: {self.step * frame:.2f} s")

        return [d.figure for d in self.dList] + [self.screen[1]]

    def runSimulation(self):
        """
        Ejecuta la simulación y muestra la animación en pantalla.
        """

        if self.timerVisible == False:
              self.screen[1].set_visible(False)
        simulation = FuncAnimation(self.screen[0], self.framing, blit=False, interval=20, cache_frame_data=False)
        plt.show()

    def initFile(self):
        """
        Inicializa el archivo CSV para guardar los datos de la simulación.

        Returns:
            str: Nombre del archivo CSV creado.
        """
        # Nombre del archivo donde se almacena la información de la simulación
        fileName = "Datos_Simulacion.csv"

        # Crea el encabezado del archivo
        header = "T"
        for i in range(1, len(self.dList) + 1):
            header += f",X_{i},Y_{i},Vx_{i},Vy_{i}"

        # Crea el archivo y le agrega el encabezado
        with open(fileName, "w") as f:
            f.write(header + "\n")

        return fileName

    def updateFile(self, data):
        """
        Escribe una línea de datos en el archivo CSV.

        Args:
            data (str): Datos a escribir.
        """
        # Abre el archivo y le agrega una nueva línea de datos
        with open(self.fileName, "a") as f:
            f.write(data)
