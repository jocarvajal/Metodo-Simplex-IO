def comprobarMax(vector):
    bandera = False
    for valor in vector:
        if valor < 0:
            bandera = True
    return bandera

def comprobarMin(vector):
    bandera = False
    for valor in vector:
        if valor > 0:
            bandera = True
    return bandera

def encontrarMenor(vector):
    menor = vector[0]
    posicion = 0
    for i in range(len(vector)):
        if vector[i] < menor:
            menor = vector[i]
            posicion = i
    return posicion

def encontrarMayor(vector):
    mayor = vector[0]
    i = 0
    posicion = 0
    for i in range(len(vector)):
        if vector[i] > mayor:
            mayor = vector[i]
            posicion = i
    return posicion

def coeficienteMenor(matriz, columnaPivote, ultimaColumna):
    fila = 1
    menorCoeficiente = 10000000
    posicion = 0
    for fila in range(len(matriz)):
        if matriz[fila][columnaPivote] > 0:
            coeficiente = matriz[fila][ultimaColumna] / matriz[fila][columnaPivote]
            if coeficiente < menorCoeficiente:
                menorCoeficiente = coeficiente
                posicion = fila
    return posicion

def prepararFilaPivote(vector, divisor):
    print(vector)
    for i in range(len(vector)):
        vector[i] = vector[i] * divisor
    return vector

def iterarMatriz(matriz,filaPivote,columnaPivote):
    print(matriz,'\n')
    for i in range(len(matriz)):
        piv = matriz[i][columnaPivote]
        for j in range(len(matriz[0])):
            if i != filaPivote:
                multiplo = piv
                print(matriz[i][j])
                matriz[i][j] = matriz[i][j] + -multiplo * matriz[filaPivote][j]
                print("A",matriz[i][j])
    print(matriz)
    return matriz



def metodoSimplex(matriz,optimizacion):
    ultimaColumna = len(matriz[0]) - 1
    pivote = 0
    if optimizacion == "max":
        while comprobarMax(matriz[0]):
            columnaPivote = encontrarMenor(matriz[0])
            filaPivote = coeficienteMenor(matriz, columnaPivote, ultimaColumna)
            pivote = matriz[filaPivote][columnaPivote]
            matriz[filaPivote] = prepararFilaPivote(matriz[filaPivote], 1/pivote)
            matriz = iterarMatriz(matriz,filaPivote,columnaPivote)

    else:
        while comprobarMin(matriz[0]):
            columnaPivote = encontrarMayor(matriz[0])
            filaPivote = coeficienteMenor(matriz, columnaPivote, ultimaColumna)
            pivote = matriz[filaPivote][columnaPivote]
            matriz[filaPivote] = prepararFilaPivote(matriz[filaPivote], 1/pivote)
            matriz = iterarMatriz(matriz,filaPivote,columnaPivote)



matriz = [[-3,-5,0,0,0,0],
          [1,0,1,0,0,4],
          [0,2,0,1,0,12],
          [3,2,0,0,1,18]]

metodoSimplex(matriz,"max")