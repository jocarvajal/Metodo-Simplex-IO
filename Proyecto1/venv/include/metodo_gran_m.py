from metodo_simplex import metodoSimplex

"""
Funcion principal de la gran M, saca las posiciones de las variables basicas
y llama a colocar las M y luego a eliminarlas de la funcion objetivo
E: Matriz con los valores, vector con las variables basicas y vector con las no basicas
S: Retorna los variables de entrada ya iteradas y con la solucion final (si existe)
"""
def gran_m(matriz, variables_basicas, variables_no_basicas):
   posiciones_r = [i for i,variable in enumerate(variables_basicas) if variable[0] == 'R']

   matriz = colocar_m(matriz, posiciones_r, variables_basicas, variables_no_basicas)

   matriz = eliminar_m(matriz, posiciones_r)

   return metodoSimplex(matriz, variables_basicas, variables_no_basicas)

"""
Funcion que coloca las M en la funcion objetivo
E: Matriz con los valores, posicion de las variables artificiales
vector con las variables basicas y vector con las no basicas
S: matriz con las M en el reglon de la funcion objetivo
"""
def colocar_m(matriz, posiciones_r, variables_basicas, variables_no_basicas):
    for posicion in posiciones_r:
            matriz[0][variables_no_basicas.index(variables_basicas[posicion])] = 1000

    return matriz

"""
Funcion que elimina las M en la funcion objetivo
E: matriz con las M en el reglon de la funcion objetivo, posicion de las variables artificiales
S: matriz con 0's en el reglon de la funcion objetivo donde haya una variable artificial
"""
def eliminar_m(matriz, posiciones_r):
    for fila in posiciones_r:
        for columna in range(len(matriz[0])):
            matriz[0][columna] += -1000*matriz[fila][columna]

    return matriz