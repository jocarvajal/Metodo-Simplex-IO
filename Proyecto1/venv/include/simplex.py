from metodo_simplex import metodoSimplex
from dosfases import  dos_fases
import os.path
from os import remove

def validar_archivo(nombre):
    valido = True
    cant_variables = -1

    archivo = open(nombre, "r")

    descripcion = archivo.readline()[:-1].split(",")
    if len(descripcion) != 4:
        print("Datos faltantes en la primera fila")
        valido = False
    elif descripcion[0].isnumeric() is False or int(descripcion[0]) < 0 or int(descripcion[0]) > 3:
        print("Metodo ingresado incorrecto")
        valido = False
    elif descripcion[1] != "min" and descripcion[1] != "max":
        print("No se ingreso la palabra clave 'max' o 'min'")
        valido = False
    elif descripcion[2].isdigit() is False or descripcion[3].isdigit() is False:
        print("No se ingreso una cantidad de variables y/o restricciones valido")
        valido = False
    else:
        cant_variables = int(descripcion[2])

    if cant_variables != -1:
        funcion_objetivo = archivo.readline()[:-1].split(",")
        if len(funcion_objetivo) != cant_variables:
            print("No se ingreso la cantidad de variables indicada para la funcion objetivo")
            valido = False
        for variable in funcion_objetivo:
            try:
                float(variable)
            except:
                print("Valor invalido: " + variable)
                valido = False

        for restriccion in archivo.readlines():
            datos = restriccion[:-1].split(",")
            if len(datos) != (cant_variables + 2):
                print("no se ingreso el numero correcto de variables en alguna restriccion")
                valido = False
            elif datos[cant_variables] != ">=" and datos[cant_variables] != "=" and datos[cant_variables] != "<=":
                print("La restriccion no tiene un condicion valida")
                valido = False
            else:
                datos.pop(cant_variables)
                for valor in datos:
                    try:
                        float(valor)
                    except:
                        print("Valor invalido en la restriccion: " + valor)
                        valido = False

    archivo.close()
    return valido

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
            matriz[0][valor] = -float(funcion_objetivo[valor])
        else:
            matriz[0][valor] = float(funcion_objetivo[valor])

    return matriz

def agregar_restricciones(archivo, matriz, descripcion):
    variables_decision = int(descripcion[2])
    fila = 1
    columna_resultados = len(matriz[0]) - 1
    variables_agregadas = 0
    for restriccion in archivo.readlines():
        datos_restriccion = restriccion[:-1].split(",")
        for dato in range(variables_decision):
            matriz[fila][dato] = float(datos_restriccion[dato])
        if datos_restriccion[variables_decision] == "<=" or datos_restriccion[variables_decision] == "=":
            matriz[fila][variables_decision + variables_agregadas] = 1
            variables_agregadas += 1
        else:
            matriz[fila][variables_decision + variables_agregadas] = -1
            matriz[fila][variables_decision + variables_agregadas + 1] = 1
            variables_agregadas += 2
        matriz[fila][columna_resultados] = float(datos_restriccion[variables_decision + 1])
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
            VB.append("S" + str(variables_holgura))
        elif tipo_restriccion == "=":
            variables_artificiales += 1
            VB.append("R" + str(variables_artificiales))
        else:
            variables_artificiales += 1
            variables_holgura += 1
            VB.append("R" + str(variables_artificiales))
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
            VNB.append("S" + str(variables_holgura))
        elif tipo_restriccion == "=":
            variables_artificiales += 1
            VNB.append("R" + str(variables_artificiales))
        else:
            variables_artificiales += 1
            variables_holgura += 1
            VNB.append("S" + str(variables_holgura))
            VNB.append("R" + str(variables_artificiales))
    VNB.append("SOL")
    archivo.close()

    return VNB

'''Esta funcion leer un archivo valido y retorna una matriz con:
    la primera fila tiene la funcion objetivo ya igualada a 0 y en max independientemente
    si le entro min o max. 
    Y el resto de fila son las restricciones con las variables de holgura(S) y artificiales(R)
    Agregadas.
    En caso de GranM o dos fases hay que agregar las Mr a la funcion objetivo.
    Tambien retorna el metodo que se va a utilizar, las variables basicas iniciales y todas las variables
    del problema'''
def leer_archivo(nombre):
    (matriz, metodo) = armar_matriz(nombre)
    VB = basicas_iniciales(nombre)
    VNB = no_basicas(nombre)

    return (matriz, metodo, VB, VNB)

def obtener_resultado(matriz, VB, VNB):
    resultados = [0]*(len(VNB)+1)
    tam = len(matriz)
    columna_resultado = len(matriz[0])-1
    for valor in range(tam):
        if valor == 0:
            if matriz[valor][columna_resultado] < 0:
                resultados[0] = -matriz[valor][columna_resultado]
            else:
                resultados[0] = matriz[valor][columna_resultado]
        else:
            pos_resultado = VNB.index(VB[valor]) + 1
            resultados[pos_resultado] = matriz[valor][columna_resultado]

    return resultados

def escribir_respuesta_final(respuestas):
    desgloce = ''
    tam = len(respuestas)

    print('\n Resultado Final: U = ' + str(respuestas[0]) + '\n')
    i = 1
    while i < tam:
        if i == tam - 1:
            desgloce += str(respuestas[i])
        else:
            desgloce += str(respuestas[i]) + ', '
        i += 1
    print('BF = (' + desgloce + ')')
    return 0

def main(nombre_archivo):

    if os.path.isfile("_sol.txt"):
        remove('_sol.txt')
    if validar_archivo(nombre_archivo):
        (matriz, metodo, VB, VNB) = leer_archivo(nombre_archivo)
        print(matriz)
        print(VB)
        print(VNB)

        if metodo == 0:
            (matriz, VB, VNB) = metodo_simplex(matriz, VB, VNB)
            escribir_respuesta_final(obtener_resultado(matriz, VB, VNB))
        #elif metodo == 1:
            #granM(matriz, VB, VNB)
        elif metodo == 2:
            (matriz, VB, VNB) = dos_fases(matriz, VB, VNB)
            escribir_respuesta_final(obtener_resultado(matriz, VB, VNB))
        #elif metodo == 3:
            #dual(matriz, VB, VNB)
    else:
        print("Archivo incorrecto")

main("problema2.txt")