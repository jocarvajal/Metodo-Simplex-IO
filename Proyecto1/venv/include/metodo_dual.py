def crear_matriz(descripcion):
    variables_decision = int(descripcion[2])
    cant_restricciones = int(descripcion[3])
    filas = cant_restricciones + 1
    columnas = variables_decision + 1
    matriz_primal = []
    for i in range(filas):
        matriz_primal.append([0] * columnas)
    return matriz_primal


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


def agregar_funcion_objetivo(matriz_primal, descripcion, funcion_objetivo):
    tipo_optimizacion = descripcion[1]
    variables_decision = int(descripcion[2])
    for valor in range(variables_decision):
        if tipo_optimizacion == "max":
            matriz_primal[-1][valor] = -funcion_objetivo[valor]
        else:
            matriz_primal[-1][valor] = funcion_objetivo[valor]

    return matriz_primal


def armar_matriz(nombre_archivo):
    archivo = open(nombre_archivo, "r")
    descripcion = archivo.readline()[:-1].split(',')
    funcion_objetivo = archivo.readline()[:-1].split(',')
    matriz_primal = crear_matriz(descripcion)
    matriz_primal = agregar_restricciones(archivo, matriz_primal, descripcion)
    matriz_primal = agregar_funcion_objetivo(matriz_primal, descripcion, funcion_objetivo)
    archivo.close()

    return matriz_primal


def tipo_problema(nombre_archivo):
    archivo = open(nombre_archivo, "r")
    descripcion = archivo.readline()[:-1].split(',')
    tipo = descripcion[1]
    return tipo


def leer_archivo(nombre_archivo):
    matriz_primal = armar_matriz(nombre_archivo)
    tipo = tipo_problema(nombre_archivo)

    return (matriz_primal, tipo)


def transponer(matriz_primal):
    transpuesta = [[matriz_primal[j][i] for j in range(len(matriz_primal))] for i in range(len(matriz_primal[0]))]
    return transpuesta


def armar_dual(primal):
    matriz = transponer(primal)
    matriz_dual = [fila[:] for fila in matriz]
    funcion_objetivo = matriz[-1]
    for fila in range(len(matriz) - 1):
        matriz_dual[fila + 1] = matriz[fila]
    matriz_dual[0] = funcion_objetivo
    return matriz_dual


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
    f = open(nombre_archivo_dual,'r+')
    f.seek(0)
    f.write(texto)
    f.truncate()
    f.close()
    return nombre_archivo_dual


def dual(nombre_archivo):
    (matriz_primal, tipo) = leer_archivo(nombre_archivo)
    matriz_dual = armar_dual(matriz_primal)
    nombre_archivo_dual = escribir_archivo_dual(nombre_archivo.split(".")[0], matriz_dual, tipo)
    return nombre_archivo_dual
