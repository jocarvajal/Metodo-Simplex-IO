from metodo_simplex import metodoSimplex

def primera_fase(matriz, VB, VNB):
    filas_restar = []

    for variable in range(len(VB)):
        if VB[variable][0] == 'R':
            filas_restar.append(variable)
    matriz = colocar_artificiales(matriz, filas_restar, VB, VNB)
    matriz = restar_restricciones(matriz, filas_restar)
    return  matriz

def restar_restricciones(matriz, filas_restar):
    for fila in range(len(filas_restar)):
        for columna in range(len(matriz[0])):
            matriz[0][columna] += -matriz[filas_restar[fila]][columna]
    return matriz

def colocar_artificiales(matriz, filas_restar, VB, VNB):
    fila_nueva = [0]*len(matriz[0])

    for campo in filas_restar:
        fila_nueva[VNB.index(VB[campo])] = 1
    matriz[0] = fila_nueva
    return matriz

def segunda_fase(matriz, matriz_segunda_fase, VB, VNB):
    matriz_segunda_fase[0] = matriz[0]
    campos_borrar = buscar_columnas_borrar(VNB)
    borrar_columnas(matriz_segunda_fase, VNB, campos_borrar)
    campos_ceros = columnas_validar(matriz_segunda_fase, VB[1:], VNB)
    matriz_segunda_fase = poner_ceros(matriz_segunda_fase, campos_ceros)
    return  (matriz_segunda_fase , VNB)

def buscar_columnas_borrar(VNB):
    columnas = []
    for indice in range(len(VNB)):
        if VNB[indice][0] == 'R':
            columnas.append(indice)
    return columnas

def borrar_columnas(matriz, VNB, campos):
    columnas_borradas = 0
    for campo in campos:
        VNB.pop(campo - columnas_borradas)
        for fila in matriz:
            fila.pop(campo-columnas_borradas)
        columnas_borradas += 1

def columnas_validar(matriz, VB, VNB):
    columnas = []
    for valor in VB:
        posicion = VNB.index(valor)
        if matriz[0][posicion] != 0:
            columnas.append(VNB.index(valor))
    return  columnas

def poner_ceros(matriz, campos):
    filas = buscar_filas(matriz, campos)
    for i in range(len(campos)):
        multiplo = matriz[0][campos[i]]
        for columna in range(len(matriz[0])):
            matriz[0][columna] = matriz[0][columna]+-multiplo*matriz[filas[i]][columna]
    return matriz

def buscar_filas(matriz, campos):
    filas = []
    fila = 1
    tam = len(matriz)
    for campo in campos:
        while fila < tam and matriz[fila][campo] != 1:
            fila += 1
        if fila < tam:
            filas.append(fila)
        else:
            filas.append(-1)
    return filas

def dos_fases(matriz, VB, VNB):
    matriz_primera_fase = primera_fase(matriz[:], VB, VNB)
    (matriz_primera_fase, VB, VNB) = metodoSimplex(matriz_primera_fase, VB, VNB)
    # Salio no acotada
    if (matriz_primera_fase == 0):
        return (0,0,0)
    f = open('_sol.txt', 'a')
    f.write('\n' + "Segunda Fase" + '\n')
    f.close()
    (matriz_segunda_fase, nuevo_VNB) = segunda_fase(matriz[:], matriz_primera_fase, VB, VNB[:])
    (matriz_segunda_fase, VB, nuevo_VNB) = metodoSimplex(matriz_segunda_fase, VB, nuevo_VNB)

    return (matriz_segunda_fase, VB, nuevo_VNB)
