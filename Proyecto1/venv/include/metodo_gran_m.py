from metodo_simplex import metodoSimplex

def gran_m(matriz, variables_basicas, variables_no_basicas):
   posiciones_r = [i for i,variable in enumerate(variables_basicas) if variable[0] == 'R']

   matriz = colocar_m(matriz, posiciones_r, variables_basicas, variables_no_basicas)

   matriz = eliminar_m(matriz, posiciones_r)

   (matriz, variables_basicas, variables_no_basicas) = metodoSimplex(matriz, variables_basicas, variables_no_basicas)

   print(matriz, variables_basicas, variables_no_basicas)

def colocar_m(matriz, posiciones_r, variables_basicas, variables_no_basicas):
    for posicion in posiciones_r:
            matriz[0][variables_no_basicas.index(variables_basicas[posicion])] = 1000

    return matriz

def eliminar_m(matriz, posiciones_r):
    for fila in posiciones_r:
        for columna in range(len(matriz[0])):
            matriz[0][columna] += -1000*matriz[fila][columna]

    return matriz


#print(gran_m([[0.4, 0.5, 0, 0, 0, 0, 0],
#              [0.3, 0.1, 1, 0, 0, 0, 2.7],
#              [0.5, 0.5, 0, 1, 0, 0, 6],
#              [0.6, 0.4, 0, 0, -1, 1, 6]], ["U", "S1", "R1", "R2"], ["X1", "X2", "S1", "R1", "S2", "R2", "SOL"]))