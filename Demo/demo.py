# Importamos las librerías necesarias
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Definimos la clase para los discos
class Disco:
    def __init__(self, radio, x_coord, y_coord):
        self.radio = radio
        self.x_coord = x_coord
        self.y_coord = y_coord
        # Definimos las variables de velocidades aleatorias:
        self.velocidad_x = np.random.uniform(-1, 1)  # Valores igualmente probables en el rango
        self.velocidad_y = np.random.uniform(-1, 1)

    # Definimos algunos métodos
    def manejo_pos(self, dt):  # dt representa el paso del tiempo
        self.x_coord += self.velocidad_x * dt
        self.y_coord += self.velocidad_y * dt

    def detectar_colisiones(self, disco_externo):
        d = np.sqrt((self.x_coord - disco_externo.x_coord) ** 2 + (self.y_coord - disco_externo.y_coord) ** 2)
        return d < (self.radio + disco_externo.radio)  # Detecta colisión si la distancia entre centros es menor que la suma de los radios

    def resolver_colisión(self, disco_externo):
        dx = disco_externo.x_coord - self.x_coord
        dy = disco_externo.y_coord - self.y_coord
        distancia = np.sqrt(dx ** 2 + dy ** 2)
        # Normalizamos las distancias:
        nx = dx / distancia
        ny = dy / distancia
        # Normalizamos las velocidades
        v1_normal = self.velocidad_x * nx + self.velocidad_y * ny
        v2_normal = disco_externo.velocidad_x * nx + disco_externo.velocidad_y * ny
        # Actualizamos las velocidades
        self.velocidad_x += (v2_normal - v1_normal) * nx
        self.velocidad_y += (v2_normal - v1_normal) * ny
        disco_externo.velocidad_x += (v1_normal - v2_normal) * nx
        disco_externo.velocidad_y += (v1_normal - v2_normal) * ny

# Simulación de dos discos
disco1 = Disco(radio=0.05, x_coord=-0.3, y_coord=0)
disco2 = Disco(radio=0.05, x_coord=0.3, y_coord=0)
dt = 0.01  # Paso de tiempo

# Configuración de la visualización en Matplotlib
fig, ax = plt.subplots()
ax.set_xlim(-0.5, 0.5)
ax.set_ylim(-0.5, 0.5)
disco1_patch = plt.Circle((disco1.x_coord, disco1.y_coord), disco1.radio, fc='blue')
disco2_patch = plt.Circle((disco2.x_coord, disco2.y_coord), disco2.radio, fc='red')
ax.add_patch(disco1_patch)
ax.add_patch(disco2_patch)

# Función de actualización para la animación
def framing(frame):
    # Actualizar posiciones
    disco1.manejo_pos(dt)
    disco2.manejo_pos(dt)
    # Detectar y resolver colisiones entre los discos
    if disco1.detectar_colisiones(disco2):
        disco1.resolver_colisión(disco2)
    # Detectar colisiones con las paredes de la caja unitaria
    for disco in [disco1, disco2]:
        if disco.x_coord - disco.radio < -0.5 or disco.x_coord + disco.radio > 0.5:
            disco.velocidad_x *= -1
        if disco.y_coord - disco.radio < -0.5 or disco.y_coord + disco.radio > 0.5:
            disco.velocidad_y *= -1
    # Actualizar las posiciones de los gráficos
    disco1_patch.set_center((disco1.x_coord, disco1.y_coord))
    disco2_patch.set_center((disco2.x_coord, disco2.y_coord))
    return disco1_patch, disco2_patch

# Configurar y ejecutar la animación
ani = FuncAnimation(fig, framing, frames=range(1000), blit=True, interval=10)
plt.show()

#Para ejecutar: pyhton3 demo.py

#Esto sería una demo básica del proyecto
