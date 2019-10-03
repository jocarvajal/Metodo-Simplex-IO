from metodo_simplex import metodoSimplex, comprobar_multiples, conseguir_multiple
from metodo_gran_m import gran_m
from dosfases import dos_fases
from metodo_dual import dual
import os.path
import argparse
#import math
from os import remove

'''
Función que valida el archivo entrante.
E; El nombre del archivo.
S; True si es valido, False de lo contrario.
'''
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

'''
Función que indica la cantidad total de variables de holgura y artificiales que se agregarán.
E: EL nombre del archivo que se esta utilizando.
S: EL número de variables a agregar.
'''
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

'''
Función que crea un matriz vacia con el tamaño necesario para acomodar el problema.
E: La primera fila del archivo, y la cantidad de varibles de holgura y artificiales involucradas.
S: Un matriz vacia con el tamaño necesario.
'''
def crear_matriz(descripcion, variables_agregar):
    variables_decision = int(descripcion[2])
    cant_restricciones = int(descripcion[3])
    filas = cant_restricciones + 1
    columnas = variables_agregar + variables_decision + 1
    matriz = []
    for i in range(filas):
        matriz.append([0.0] * columnas)

    return matriz

'''
Función que agrega la función objetivo a la primera fila de la matriz inicial, esta función hace que todo lo
entrante sea max, si entra un minimo de una vez lo convierte.
E: La matriz inicial vacia, la primera fila del archivo, y los datos constantes de la función objetivo.
S: La matriz inicial solo con la primera fila.
'''
def agregar_funcion_objetivo(matriz, descripcion, funcion_objetivo):
    tipo_optimizacion = descripcion[1]
    variables_decision = int(descripcion[2])
    for valor in range(variables_decision):
        if tipo_optimizacion == "max":
            matriz[0][valor] = -float(funcion_objetivo[valor])
        else:
            matriz[0][valor] = float(funcion_objetivo[valor])

    return matriz

'''
Función auxiliar que agrega las filas de las restricciones a la metriz inicial.
E; Nombre del archivo, la matriz inicial incompleta, la primera fila del archivo.
S: la matriz final completa.
'''
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
            matriz[fila][variables_decision + variables_agregadas] = 1.0
            variables_agregadas += 1
        else:
            matriz[fila][variables_decision + variables_agregadas] = -1.0
            matriz[fila][variables_decision + variables_agregadas + 1] = 1.0
            variables_agregadas += 2
        matriz[fila][columna_resultados] = float(datos_restriccion[variables_decision + 1])
        fila += 1

    return matriz

'''
Función principal en el proceso de montar la matriz inicial.
E: El nombre del archivo.
S: La matriz inicial y el método con el que se procesará.
'''
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

'''
Función que lee el archivo y indica que metodo se va a usar.
E: EL nombre del archivo que se esta utilizando.
S: EL número del método a utilizar.'''
def averiguar_metodo(nombre_archivo):
    archivo = open(nombre_archivo, "r")
    descripcion = archivo.readline()[:-1].split(',')
    metodo = int(descripcion[0])
    archivo.close()
    return metodo

'''
Función que lee el archivo para saber las variables básicas iniciales.
E: El nombre del archivo que se esta utilizando.
S: Un vector con las variables básicas.
'''
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

'''
Función que lee el archivo y monta dos vectores: uno con todos los tipos de variables presentes 
y otro con los tipos de restricciones presentes.
E: EL nombre del archivo que se esta utilizando.
S: Dos vectores: todos los tipos de variables presentes y tipos de restriccioness.
'''
def no_basicas(nombre_archivo):
    VNB = []
    signos_restriccion = []
    variables_holgura = 0
    variables_artificiales = 0
    archivo = open(nombre_archivo, "r")
    variables_decision = int(archivo.readline().split(",")[2])
    archivo.readline()
    for i in range(1, variables_decision + 1):
        VNB.append("X" + str(i))
    for restriccion in archivo.readlines():
        tipo_restriccion = restriccion.split(",")[variables_decision]
        signos_restriccion.append(tipo_restriccion)
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
    return (VNB, signos_restriccion)

'''
Funcion principal para leer el archivo.
E: El nombre del archivo a leer.
S: La matriz montada del problema en max(de ser minimo se convertira en la lectura del archivo), el número del método
    a ejecutar, las variables básicas, todas las variables(cotando las de holgura y artificiales), y los tipos de 
    restricciones los que el programa cuenta'''
def leer_archivo(nombre):
    (matriz, metodo) = armar_matriz(nombre)
    VB = basicas_iniciales(nombre)
    (VNB, signos_restriccion) = no_basicas(nombre)

    return (matriz, metodo, VB, VNB, signos_restriccion)

'''
Funcion que acomoda el BF final del problema.
E: la matriz resultante, las variables básicas finales, y todas las variables involucradas en el problema.
S: Un vector con el resultado acomodado de U y las variables básicas en orden.
'''
def obtener_resultado(matriz, VB, VNB):
    resultados = [0] * (len(VNB))
    tam = len(matriz)
    columna_resultado = len(matriz[0]) - 1
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


'''
Función que se encarga de ubicar las columnas donde se encuentran variables artificales R, con el objetivo de no
tomarlas en cuenta en el calculo de factibilidad
E: un arreglo de las variables no basicas.
S: un arreglo de booleanos indicando las posiciones donde hay variables artificiales en la funcion objetivo original
'''
def posiciones_r(VNB):
    posiciones = [False] * len(VNB)
    for i in range(len(VNB)):
        if VNB[i][0] == 'R':
            posiciones[i] = True
    return posiciones


'''
Función que se encarga de evaluar el vector de resultados finales en las restricciones planteadas en el problema 
original. Para comprobar la factibilidad se multiplica vectorialmente cada linea correspondiente a restriccion en la 
matriz original por el vector de resultados. 
E: el vector de resultados, la matriz original, los signos de restriccion de la matriz original, las posiciones de las
variables artificiales en la matriz original.
S: un valor booleano indicando la factibilidad.
'''
def verificar_factibilidad(resultados, matriz_original, signos_restriccion, posiciones):
    factible = True
    for i in range(1, len(matriz_original)):
        suma = 0
        k = 0
        for j in range(len(resultados)-1):
            if not posiciones[j]:
                suma += resultados[k+1] * matriz_original[i][j]
                k += 1
        suma = round(suma, 1)
        if signos_restriccion[i-1] == "<=":
            if suma > matriz_original[i][-1]:
                factible = False
        elif signos_restriccion[i-1] == "=":
            if suma != matriz_original[i][-1]:
                factible = False
        else:
            if suma < matriz_original[i][-1]:
                factible = False

    return factible

'''
Función que escribe la respuesta del problema ejecutado en la terminal
E: Las soluciones de las incognitas encontradas, el nombre del archivo, y si es factible
S: Ninguna.
'''
def escribir_respuesta_final(respuestas, nombre_archivo, factibilidad):
    desgloce = ''
    tam = len(respuestas)

    print('\nResultado Final ' + nombre_archivo + ': U = ' + str(respuestas[0]) + '\n')
    i = 1
    while i < tam:
        if i == tam - 1:
            desgloce += str(respuestas[i])
        else:
            desgloce += str(respuestas[i]) + ', '
        i += 1
    print('BF = (' + desgloce + ')\n')

    if factibilidad:
        print('\nLa respuesta óptima encontrada es factible.\n')
    else:
        print('\nLa respuesta óptima encontrada no es factible.\n')

'''
Función principal que ejecuta el programa.
E: El nombre de un archivo.
S: Ninguna.
'''
def main(nombre_archivo):
    
    if os.path.isfile(nombre_archivo.split(".")[0] + "_sol.txt"):
        remove(nombre_archivo.split(".")[0] + '_sol.txt')
    if validar_archivo(nombre_archivo):
        metodo = averiguar_metodo(nombre_archivo)
        if metodo == 3:
            print("El problema dual será resuelto mediante el método de las 2 fases")
            if os.path.isfile(nombre_archivo.split(".")[0] + "_dual_sol.txt"):
                remove(nombre_archivo.split(".")[0] + '_dual_sol.txt')
            nombre_archivo = dual(nombre_archivo)

        (matriz, metodo, VB, VNB, signos_restriccion) = leer_archivo(nombre_archivo)
        matriz_original = [fila[:] for fila in matriz]
        VNB_original = [v for v in VNB]

        cumple_restriccion = True

        if metodo == 0:
            for variable in VNB:
                if (variable[0] == 'R'):
                    cumple_restriccion = False

            if (cumple_restriccion):
                (matriz, VB, VNB) = metodoSimplex(matriz, VB, VNB, nombre_archivo.split(".")[0])
            else:
                print("\nMetodo simplex solo puede tener restricciones de '<='\n")
        elif metodo == 1:
            (matriz, VB, VNB) = gran_m(matriz, VB, VNB, nombre_archivo.split(".")[0])
        elif metodo == 2:
            (matriz, VB, VNB) = dos_fases(matriz, VB, VNB, nombre_archivo.split(".")[0])

        # Esta condicion es para verificar si es no acotada
        if (matriz != 0 and matriz != None and cumple_restriccion):
            (columna_pivote, soluciones_multiples) = comprobar_multiples(matriz[0], VB, VNB,
                                                                         nombre_archivo.split(".")[0])
            if (soluciones_multiples):
                (matriz, VB, VNB) = conseguir_multiple(matriz, VB, VNB, columna_pivote, nombre_archivo.split(".")[0])

            resultados = obtener_resultado(matriz, VB, VNB)
            posiciones = posiciones_r(VNB_original)
            factibilidad = verificar_factibilidad(resultados, matriz_original, signos_restriccion, posiciones)
            escribir_respuesta_final(resultados, nombre_archivo.split(".")[0], factibilidad)

    else:
        print("Archivo " + nombre_archivo + " incorrecto")

'''
Código que inicia la ejecución del programa.
Las entradas son dadas por consolas.
'''
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'Corra el archivo simplex.py seguido de los archivos que tienen los problemas a resolver en formato txt')
    parser.add_argument("archivos", metavar="archivo.txt", help = "Uno o más archivos a ejecutar", nargs = '+')
    args = parser.parse_args()
    tam = len(args.archivos)
  
    for archivo in args.archivos:
        if ".txt" in archivo:
            main(archivo)
            print("-" * 50)
        else:
            print("El programa solo acepta .txt, intente ingresando otro archivo")
