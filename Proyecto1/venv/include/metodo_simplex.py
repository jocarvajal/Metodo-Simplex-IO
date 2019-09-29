"""
Funcion que verifica que la fila U tenga todos sus valores positivos para terminar de iterar
E : Fila con los valores de la funcion objetivo
S : Booleano que retorna False si todos los valores son positivps y True si sucede lo contrario
"""

def comprobar_max(vector):
    bandera = False
    for valor in range(len(vector)-1):
        if vector[valor] < 0:
            bandera = True
    return bandera


""" 
Funcion que busca el mayor de los menores en la fila U para tomarlo como columna pivote 
E : Fila con los valores de la funcion objetivo
S : Posicion de la columna pivote 
"""
def encontrar_menor(vector):
    menor = vector[0]
    posicion = 0
    for i in range(len(vector)-1):
        if vector[i] < menor:
            menor = vector[i]
            posicion = i
    return posicion

""" 
Funcion que localiza si hay dos cocientes iguales, haciendo mencion que es una funcion degenerada
E : Dos cocientes flotantes
S : None
"""
def es_degenerada(cociente1,cociente2):
    if cociente1 == cociente2:
        print("Presenta una funcion degenerada\n")


""" 
Funcion que verifica si la funcion es no acotada
E : Posicion de la fila pivote 
S : Booleano que retorna False si la posicion tiene un valor dentro de la lista y True ssi su valor es -1 dando referencia
     que no se pudo encontrar un valor pivote
"""
def comprobar_no_acotado(posicion):
    es_no_acotada = False
    if posicion == -1:
        es_no_acotada = True
    return es_no_acotada


""" 
Funcion que busca el menor cociente para usarlo como fila pivote 
E : Matriz con los valores a iterar,posicion de la columna pivote, posicion de la columna solucion
S : Posicion de la fila pivote 
"""
def cociente_menor(matriz, columna_pivote, ultima_columna):
    menor_cociente = 10000000
    posicion = -1
    for fila in range(1, len(matriz)):
        if matriz[fila][columna_pivote] > 0:
            cociente = matriz[fila][ultima_columna] / matriz[fila][columna_pivote]
            if cociente < menor_cociente:
                anterior_cociente = menor_cociente
                menor_cociente = cociente
                posicion = fila
                es_degenerada(anterior_cociente,menor_cociente)
    return posicion

""" 
Funcion que divide toda la fila pivote entre el valor de numero pivote 
E : Fila pivote , valor numero pivote 
S : Retorna la fila pivote lista para el metodo de Gauss
"""
def preparar_fila_pivote(vector, divisor):
    for i in range(len(vector)):
        vector[i] = vector[i] * divisor
    return vector

""" 
Funcion encargada de aplicar el metodo Gauss Jordan a todas sus filas usando los valores de la fila pivote 
E : Matriz iterable,pos fila pivote, pos columna pivote 
S : Matriz iterada 
"""
def iterar_matriz(matriz,fila_pivote,columna_pivote):
    for i in range(len(matriz)):
        multiplo = matriz[i][columna_pivote]
        for j in range(len(matriz[0])):
            if i != fila_pivote:
                matriz[i][j] = matriz[i][j] + -multiplo * matriz[fila_pivote][j]
    return matriz


""" 
Funcion que verifica si hay soluciones multiples 
E : Fila con los valores de la funcion objetivo y un vector con las varaibles no basicas 
S : Devuelve True si una de las vaiables artificiales presenta un valor de 0 al final del proceso 
"""
def comprobar_multiples(vector, VB, VNB):
    tiene_multiple = False
    for basica in VB:
        for valor in range(len(vector)):
            if basica != VNB[valor] and vector[valor] == 0 and VNB[valor] != "SOL" :
                tiene_multiple = True
                print("Presenta respuesta multiple\n")
                break
    return tiene_multiple

def conseguir_multiple(matriz,VB,VNB):
    columna_pivote = 0
    for basica in VB:
        for valor in range(len(matriz[0])):
            if basica != VNB[valor] and matriz[0][valor] == 0 and VNB[valor] != "SOL":
                columna_pivote = valor
    fila_pivote = cociente_menor(matriz, columna_pivote, len(matriz[0]) - 1)
    pivote = matriz[fila_pivote][columna_pivote]
    matriz[fila_pivote] = preparar_fila_pivote(matriz[fila_pivote], 1 / pivote)
    matriz = iterar_matriz(matriz, fila_pivote, columna_pivote)
    saliente = VB[fila_pivote]
    entrante = VNB[columna_pivote]
    VB[fila_pivote] = VNB[columna_pivote]
    escribir_tablas(matriz[:], VB[:], VNB[:], pivote, entrante, saliente, "Extra")


""" 
Funcion que lleva el ciclo de busqueda del numero pivote y manipular los datos con el metodo Gauss de acuerdo a lvalor pivote 
E : Matriz con los valores, vector con las variables basicas y vector con las no basicas 
S : Retorna los vriables de entrada ya iteradas y con la solucion final 
"""
def metodoSimplex(matriz,VB,VNB):
    ultima_columna = len(matriz[0]) - 1
    estado = 1
    escribir_tablas(matriz,VB,VNB,'Ninguno','Ninguno','Ninguno',0)
    while comprobar_max(matriz[0]):
        columna_pivote = encontrar_menor(matriz[0])
        fila_pivote = cociente_menor(matriz, columna_pivote, ultima_columna)
        if comprobar_no_acotado(fila_pivote):
            print("Funcion no acotada\n")
            return None
        pivote = matriz[fila_pivote][columna_pivote]
        matriz[fila_pivote] = preparar_fila_pivote(matriz[fila_pivote], 1/pivote)
        matriz = iterar_matriz(matriz,fila_pivote,columna_pivote)
        saliente = VB[fila_pivote]
        entrante = VNB[columna_pivote]
        VB[fila_pivote] = VNB[columna_pivote]
        escribir_tablas(matriz[:],VB[:],VNB[:],pivote,entrante,saliente,estado)
        estado += 1
    if comprobar_multiples(matriz[0], VB, VNB):
        conseguir_multiple(matriz, VB, VNB)
    return (matriz, VB, VNB)

""" 
Funcion que escribe en el archivo olucion los valores de cada iteracion 

"""

def escribir_tablas(matriz,VB,VNB,pivote,entrante,saliente,estado):
    texto = ''
    formatear_decimales(matriz)
    VNB = [["VB"] + VNB]
    matriz_imprimible = []
    i = 0
    tam = len(matriz[0])
    while i < len(matriz):
        matriz_imprimible += [[VB[i]] + matriz[i]]
        i += 1
    matriz_imprimible = VNB + matriz_imprimible
    texto += '\n' + '-' * (tam * 17 + 4) + '\n'
    for fila in range(len(matriz_imprimible)):
        for columna in range(len(matriz_imprimible[0])):
            texto += str(matriz_imprimible[fila][columna]) +'     |     \t'
        texto += '\n' + '-' * (tam * 17 + 4) + '\n'
    f = open('_sol.txt','a')
    f.write('\nEstado ' + str(estado) + '\n')
    f.write(texto)
    f.write('VB entrante: ' + str(entrante) + ', VB saliente: ' + str(saliente) + ' Numero Pivot: '+ str(pivote) + '\n')
    f.close()

""" 
Funcion que disminuye la cantidad de los decimales para mejor presentacion en el archivo soluion 
E : Matrizz con todos los valores 

"""
def formatear_decimales(matriz):
    for fila in range(len(matriz)):
        for columna in range(len(matriz[0])):
            matriz[fila][columna] = round(matriz[fila][columna], 1)



"""if __name__ == "__main__":
    tam = len(sys.argv)
    if tam < 3:
        print("Error al correr simplex.py, intente de nuevo colocando un archivo correctamente")

    else:
        i = 2
        while i < tam:
            if ".txt" in sys.argv[i]:
                sys.exit(leerArchivo(sys.argv[i]))
            else:
                print("El programa solo acepta .txt, intente ingresando otro archivo") """


