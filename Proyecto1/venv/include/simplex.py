def comprobarMax(vector):
    bandera = False
    for valor in vector:
        if valor < 0:
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
    for i in range(len(vector)):
        vector[i] = vector[i] * divisor
    return vector

def iterarMatriz(matriz,filaPivote,columnaPivote):
    for i in range(len(matriz)):
        multiplo = matriz[i][columnaPivote]
        for j in range(len(matriz[0])):
            if i != filaPivote:
                matriz[i][j] = matriz[i][j] + -multiplo * matriz[filaPivote][j]
    return matriz

def metodoSimplex(matriz,VB,VNB):
    ultimaColumna = len(matriz[0]) - 1
    while comprobarMax(matriz[0]):
        columnaPivote = encontrarMenor(matriz[0])
        filaPivote = coeficienteMenor(matriz, columnaPivote, ultimaColumna)
        pivote = matriz[filaPivote][columnaPivote]
        matriz[filaPivote] = prepararFilaPivote(matriz[filaPivote], 1/pivote)
        matriz = iterarMatriz(matriz,filaPivote,columnaPivote)
        VB[filaPivote] = VNB[columnaPivote]

    


matriz = [[-3,-5,0,0,0,0],
          [1,0,1,0,0,4],
          [0,2,0,1,0,12],
          [3,2,0,0,1,18]]

a = ['U','S3','S4','S5']
b = ['X1','X2','S3','S4','S5']

metodoSimplex(matriz,a,b)
