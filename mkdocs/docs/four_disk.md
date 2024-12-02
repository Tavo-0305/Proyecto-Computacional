En este documento se realiza una simulación para únicamente 4 discos. Para realiza esto tenemos como dependencias las siguientes clases:

-numpy

-classes (debe incluir las clases `Disco` y `Escenario`).

Por lo tanto, comenzamos llamando cada clase:
```py
import numpy as np
from classes import Disco, Escenario
```
Seguidamente, definimos el tamaño del espacio de simulación y los parámetros iniciales, siento estos 4 dicsos y con radio de 0.10:

```py
espacioHorizontal = 1.0  
espacioVertical = 1.0    
cantidadDiscos = 4       
radioDiscos = 0.10  
```
Después se definen las posiciones aleatoriamente para los discos, asegurando a la vez que los discos no estén superpuestos

```py
posiciones = []
while len(posiciones) < cantidadDiscos:
    nueva_pos = np.random.uniform(radioDiscos, espacioHorizontal - radioDiscos, 2)
    if all(np.linalg.norm(nueva_pos - p) > 2 * radioDiscos for p in posiciones):
        posiciones.append(nueva_pos)
```
Podemos perzonalizar los discos asignándoles colores de manera cíclica, en nuestro caso decidimos utilizar los colores: azul, rojo, verde y naranja:
```py
colores = ['blue', 'red', 'green', 'orange']
discos = [
    Disco(pos[0], pos[1], colores[i % len(colores)], radioDiscos)
    for i, pos in enumerate(posiciones)
]
```
Finalmente, configuramos el espacio de simulación y ejecutamos la simulación:
```py
simulacion = Escenario(discos, 0.01)
```
simulacion.runSimulation(

![Simulación de 4 discos](imagenes/4disk.gif)