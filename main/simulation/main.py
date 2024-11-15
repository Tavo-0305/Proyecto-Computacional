from classes import Disco, Animacion
#Creamos los objetos de tipo disco
disco1 = Disco()
disco2 = Disco()
disco3 = Disco()
disco4 = Disco()
#Objeto de tipo animación
simulacion = Animacion(1,[disco1,disco2,disco3,disco4]) #Recuerde que la dimensión es unitaria
#Corrermos la simulacion
simulacion.run()
#Además debemos implementar un script para crear un archivo .csv con los datos de los discos