import os
from os import remove


"""
Función que genera una matriz de ceros del tamano especifico necesario.
E: un string conteniendo la descripcion de la matriz
S: una matriz compuesta de ceros
"""
def crear_matriz(descripcion):
    variables_decision = int(descripcion[2])
    cant_restricciones = int(descripcion[3])
    filas = cant_restricciones + 1
    columnas = variables_decision + 1
    matriz_primal = []
    for i in range(filas):
        matriz_primal.append([0] * columnas)
    return matriz_primal


"""
Función que agrega los coeficientes de las restricciones a la matriz del problema primal
E: archivos de texto, matriz del problema primal, un string conteniendo la descripcion de la matriz del problema primal
S: la matriz del problema primal
"""
def agregar_restricciones(archivo, matriz_primal, descripcion):
    variables_decision = int(descripcion[2])
    columna_resultados = len(matriz_primal[0]) - 1
    fila = 0
    for restriccion in archivo.readlines():
        datos_restriccion = restriccion[:-1].split(",")
        for dato in range(variables_decision):
            matriz_primal[fila][dato] = datos_restriccion[dato]
        matriz_primal[fila][columna_resultados] = datos_restriccion[variables_decision + 1]
        fila += 1

    return matriz_primal


"""
Función que agrega los coeficientes del problema primal a la parte inferior de la matriz del problema
E: matriz del problema primal, un string con la descripcion de la matriz, un arreglo con los coeficientes 
de la funcion objetivo.
S: matriz del problema primal
"""
def agregar_funcion_objetivo(matriz_primal, descripcion, funcion_objetivo):
    tipo_optimizacion = descripcion[1]
    variables_decision = int(descripcion[2])
    for valor in range(variables_decision):
        if tipo_optimizacion == "max":
            matriz_primal[-1][valor] = -funcion_objetivo[valor]
        else:
            matriz_primal[-1][valor] = funcion_objetivo[valor]

    return matriz_primal


"""
Función que arma la matriz del problema primal. Para esto, realiza llamados a distintas funciones que le dan estructura
a la matriz y la llenan con sus respectivos datos.
E: un string conteniendo el nombre del archivo
S: matriz del problema primal
"""
def armar_matriz(nombre_archivo):
    archivo = open(nombre_archivo, "r")
    descripcion = archivo.readline()[:-1].split(',')
    funcion_objetivo = archivo.readline()[:-1].split(',')
    matriz_primal = crear_matriz(descripcion)
    matriz_primal = agregar_restricciones(archivo, matriz_primal, descripcion)
    matriz_primal = agregar_funcion_objetivo(matriz_primal, descripcion, funcion_objetivo)
    archivo.close()

    return matriz_primal


"""
Función que averigua si el problema con el que se esta trabajando es de maximizacion o minimizacion
E: un string con el nombre del archivo
S: un string indicando si el problema es "max" o "min"
"""
def tipo_problema(nombre_archivo):
    archivo = open(nombre_archivo, "r")
    descripcion = archivo.readline()[:-1].split(',')
    tipo = descripcion[1]
    return tipo


"""
Función que se encarga de leer el archivo. Generando la matriz del problema primal y obteniendo el tipo de problema 
con el que se va a trabajar
E: el nombre del archivo de texto con el problema primal
S: una tupla con la matriz del problema primal y un string indicando el tipo de problema
"""
def leer_archivo(nombre_archivo):
    matriz_primal = armar_matriz(nombre_archivo)
    tipo = tipo_problema(nombre_archivo)

    return (matriz_primal, tipo)


"""
Función que transpone una matriz de cualquiera tamano
E: un arreglo de dos dimensiones con los coeficientes del problema primal
S: un arreglo de dos dimensiones con los valores transpuestos
"""
def transponer(matriz_primal):
    transpuesta = [[matriz_primal[j][i] for j in range(len(matriz_primal))] for i in range(len(matriz_primal[0]))]
    return transpuesta


"""
Función que estructura la matriz del problema dual. Para esto transpone la matriz y luego reacomoda las filas,
colocando la de los coeficientes de la funcion objetivo en la parte de arriba.
E: la matriz del problema primal
S: matriz del problema dual
"""
def armar_dual(primal):
    matriz = transponer(primal)
    matriz_dual = [fila[:] for fila in matriz]
    funcion_objetivo = matriz[-1]
    for fila in range(len(matriz) - 1):
        matriz_dual[fila + 1] = matriz[fila]
    matriz_dual[0] = funcion_objetivo
    return matriz_dual


"""
Función que se encarga de generar un nuevo archivo de texto con el mismo formato con el que se ha decidido trabajar, 
en el cual se insertan la informacion del problema dual.
E: string con el nombre del archivo conteniendo el problema primal, matriz del problema dual, string indicando el
tipo de problema 
S: string con el nombre del nuevo archivo 
"""
def escribir_archivo_dual(nombre_archivo, matriz_dual, tipo):
    texto = ''
    if tipo == "max":
        tipo_dual = "min"
        rest = ">="
    elif tipo == "min":
        tipo_dual = "max"
        rest = "<="
    num_variables = len(matriz_dual[0]) - 1
    num_restricciones = len(matriz_dual) - 1
    texto += '2,' + tipo_dual + ',' + str(num_variables) + ',' + str(num_restricciones) + '\n' + str(matriz_dual[0][0])
    for item in range(1, len(matriz_dual[0]) - 1):
        texto += ',' + str(matriz_dual[0][item])
    for fila in range(1, len(matriz_dual)):
        texto += '\n'
        for columna in range(len(matriz_dual[0]) - 1):
            texto += str(matriz_dual[fila][columna]) + ','
        texto += rest + ',' + str(matriz_dual[fila][-1]) + '\r'

    nombre_archivo_dual = nombre_archivo + '_dual.txt'
    if os.path.isfile(nombre_archivo_dual):
        remove(nombre_archivo_dual)
    f = open(nombre_archivo_dual,'w')
    f.write(texto)
    f.close()
    return nombre_archivo_dual


"""
Función principal que se encarga de leer el archivo, generar una matriz para el problema primal, con ella armar una
matriz para el problema dual y finalmente crear un nuevo archivo con esta matriz. 
E: el nombre del archivo con el problema primal
S: el nombre del archivo con el problema dual
"""
def dual(nombre_archivo):
    (matriz_primal, tipo) = leer_archivo(nombre_archivo)
    matriz_dual = armar_dual(matriz_primal)
    nombre_archivo_dual = escribir_archivo_dual(nombre_archivo.split(".")[0], matriz_dual, tipo)
    return nombre_archivo_dual
