from metodo_simplex import metodoSimplex


def variables_restricciones(nombre_archivo):
    archivo = open(nombre_archivo, "r")
    cantidad_variables = 0
    restriccion = int(archivo.readline().split(',')[2])
    archivo.readline()
    for linea in archivo.readlines():
        tipo_restriccion = linea.split(',')[restriccion]
        if tipo_restriccion == "<=" or tipo_restriccion == "=":
            cantidad_variables += 1
        else:
            cantidad_variables += 2
    archivo.close()

    return cantidad_variables

def crear_matriz(descripcion, variables_agregar):
    variables_decision = int(descripcion[2])
    cant_restricciones = int(descripcion[3])
    filas = cant_restricciones + 1
    columnas = variables_agregar + variables_decision + 1
    matriz = []
    for i in range(filas):
        matriz.append([0] * columnas)

    return matriz

def agregar_funcion_objetivo(matriz, descripcion, funcion_objetivo):
    tipo_optimizacion = descripcion[1]
    variables_decision = int(descripcion[2])
    for valor in range(variables_decision):
        if tipo_optimizacion == "max":
            matriz[0][valor] = -int(funcion_objetivo[valor])
        else:
            matriz[0][valor] = int(funcion_objetivo[valor])

    return matriz

def agregar_restricciones(archivo, matriz, descripcion):
    variables_decision = int(descripcion[2])
    fila = 1
    columna_resultados = len(matriz[0]) - 1
    variables_agregadas = 0
    for restriccion in archivo.readlines():
        datos_restriccion = restriccion[:-1].split(",")
        for dato in range(variables_decision):
            matriz[fila][dato] = int(datos_restriccion[dato])
        if datos_restriccion[variables_decision] == "<=" or datos_restriccion[variables_decision] == "=":
            matriz[fila][variables_decision + variables_agregadas] = 1
            variables_agregadas += 1
        else:
            matriz[fila][variables_decision + variables_agregadas] = -1
            matriz[fila][variables_decision + variables_agregadas + 1] = 1
            variables_agregadas += 2
        matriz[fila][columna_resultados] = int(datos_restriccion[variables_decision + 1])
        fila += 1

    return matriz

def armar_matriz(nombre_archivo):
    variables_agregar = variables_restricciones(nombre_archivo)
    archivo = open(nombre_archivo, "r")
    # El [:-1] es para quitar el salto de linea
    descripcion = archivo.readline()[:-1].split(',')
    funcion_objetivo = archivo.readline()[:-1].split(",")
    matriz = crear_matriz(descripcion, variables_agregar)
    matriz = agregar_funcion_objetivo(matriz, descripcion, funcion_objetivo)
    matriz = agregar_restricciones(archivo, matriz, descripcion)
    metodo = int(descripcion[0])
    archivo.close()

    return (matriz, metodo)

def basicas_iniciales(nombre_archivo):
    VB = ["U"]
    variables_holgura = 0
    variables_artificiales = 0
    archivo = open(nombre_archivo, "r")
    variables_decision = int(archivo.readline().split(",")[2])
    archivo.readline()
    for restriccion in archivo.readlines():
        tipo_restriccion = restriccion.split(",")[variables_decision]
        if tipo_restriccion == "<=":
            variables_holgura += 1
            VB.append("R" + str(variables_holgura))
        elif tipo_restriccion == "=":
            variables_artificiales += 1
            VB.append("S" + str(variables_artificiales))
        else:
            variables_artificiales += 1
            variables_holgura += 1
            VB.append("S" + str(variables_artificiales))
        archivo.close()

    return VB

def no_basicas(nombre_archivo):
    VNB = []
    variables_holgura = 0
    variables_artificiales = 0
    archivo = open(nombre_archivo, "r")
    variables_decision = int(archivo.readline().split(",")[2])
    archivo.readline()
    for i in range(1, variables_decision + 1):
        VNB.append("X" + str(i))
    for restriccion in archivo.readlines():
        tipo_restriccion = restriccion.split(",")[variables_decision]
        if tipo_restriccion == "<=":
            variables_holgura += 1
            VNB.append("R" + str(variables_holgura))
        elif tipo_restriccion == "=":
            variables_artificiales += 1
            VNB.append("S" + str(variables_artificiales))
        else:
            variables_artificiales += 1
            variables_holgura += 1
            VNB.append("R" + str(variables_holgura))
            VNB.append("S" + str(variables_artificiales))
    VNB.append("SOL")
    archivo.close()

    return VNB

def leer_archivo(nombre):
    (matriz, metodo) = armar_matriz(nombre)
    VB = basicas_iniciales(nombre)
    VNB = no_basicas(nombre)
    print(matriz)
    print(VB)
    print(VNB)

    return (matriz, metodo, VB, VNB)

def main(nombre_archivo):
    (matriz, metodo, VB, VNB) = leer_archivo(nombre_archivo)
    if metodo == 0:
        metodoSimplex(matriz, VB, VNB)
    #elif metodo == 1:
        #granM(matriz, VB, VNB)
    #elif metodo == 2:
        #dos_fases(matriz, VB, VNB)
    #elif metodo == 3:
        #dual(matriz, VB, VNB)

# remove('_sol.txt')
# metodoSimplex(matriz,VB,VNB)
main("problema1.txt")