Este script configura y ejecuta una simulación de colisiones elásticas utilizando
los objetos `Disco` y `Escenario` definidos en el módulo `classes`. Se generan 
aleatoriamente posiciones iniciales para un conjunto de discos y se les asignan
colores y radios variados. La simulación se ejecuta y se visualiza en tiempo real.

Dependencias:
- numpy
- classes (debe incluir las clases `Disco` y `Escenario`).

Primero definimos el espacio de simulación y los parámetros iniciales. En nuestro caso utilizamos un tamaño de 1x1 para el contenedor y definimos un valor de 50 discos para la simulación, de la siguiente manera:

``` py
espacioHorizontal = 1.0
espacioVertical = 1.0
cantidadDiscos = 50
```
Seguido de esto se configuró la cuadrícula para poder posicionar los discos, de tal manera que si el cuadrado del largo de la matriz es menor a la cantidad de discos, se le suma 1 al largo de la matriz. Es decir:
``` py
largoMatriz = 1
while True:
    if largoMatriz * largoMatriz < cantidadDiscos:
        largoMatriz += 1
    else:
        break
```
Con esto, definimos las distancias horizontales y verticales del contenedor e inicializamos las pocisiones en una cuadrícula:

```py
distanciaHorizontal = espacioHorizontal / (largoMatriz + 1)
distanciaVertical = espacioVertical / (largoMatriz + 1)
posiciones = np.zeros([largoMatriz * largoMatriz, 2]) 
posiciones[0] = [distanciaHorizontal, distanciaVertical]

```
