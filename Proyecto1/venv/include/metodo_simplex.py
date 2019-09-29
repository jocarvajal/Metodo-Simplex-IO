import sys


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
    estado = 1
    escribirTablas(matriz,VB,VNB,'Ninguno','Ninguno','Ninguno',0)
    while comprobarMax(matriz[0]):
        columnaPivote = encontrarMenor(matriz[0])
        filaPivote = coeficienteMenor(matriz, columnaPivote, ultimaColumna)
        pivote = matriz[filaPivote][columnaPivote]
        matriz[filaPivote] = prepararFilaPivote(matriz[filaPivote], 1/pivote)
        matriz = iterarMatriz(matriz,filaPivote,columnaPivote)
        saliente = VB[filaPivote]
        entrante = VNB[columnaPivote]
        VB[filaPivote] = VNB[columnaPivote]
        escribirTablas(matriz[:],VB[:],VNB[:],pivote,entrante,saliente,estado)
        estado += 1

    return (matriz, VB)

def escribirTablas(matriz,VB,VNB,pivote,entrante,saliente,estado):
    texto = ''
    formatearDecimales(matriz)
    VNB = [["VB"] + VNB]
    matrizImprimible = []
    i = 0
    tam = len(matriz[0])
    while i < len(matriz):
        matrizImprimible += [[VB[i]] + matriz[i]]
        i += 1
    matrizImprimible = VNB + matrizImprimible
    texto += '\n' + '-' * (tam * 17 + 4) + '\n'
    for fila in range(len(matrizImprimible)):
        for columna in range(len(matrizImprimible[0])):
            texto += str(matrizImprimible[fila][columna]) +'     |     \t'
        texto += '\n' + '-' * (tam * 17 + 4) + '\n'
    f = open('_sol.txt','a')
    f.write('\nEstado ' + str(estado) + '\n')
    f.write(texto)
    f.write('VB entrante: ' + str(entrante) + ', VB saliente: ' + str(saliente) + ' Numero Pivot: '+ str(pivote) + '\n')
    f.close()

def formatearDecimales(matriz):
    for fila in range(len(matriz)):
        for columna in range(len(matriz[0])):
            matriz[fila][columna] = round(matriz[fila][columna],1)



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


