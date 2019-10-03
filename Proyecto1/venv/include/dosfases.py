from metodo_simplex import metodoSimplex

'''
Función que acomoda la matriz para realizar la primera fase.
E: La matriz inicial, las variables básicas iniciales, todas las variables del problema.
S: La matriz de la primera lista para ejecutar simplex.
'''
def primera_fase(matriz, VB, VNB):
    filas_restar = []

    for variable in range(len(VB)):
        if VB[variable][0] == 'R':
            filas_restar.append(variable)
    matriz = colocar_artificiales(matriz, filas_restar, VB, VNB)
    matriz = restar_restricciones(matriz, filas_restar)
    return  matriz

'''
Función que ayuda a crear la primer fila de la primera fase.
E: la matriz inicial, los números de las filas que hay que restar.
S: LA matriz con la primer fila ya procesada.
'''
def restar_restricciones(matriz, filas_restar):
    for fila in range(len(filas_restar)):
        for columna in range(len(matriz[0])):
            matriz[0][columna] += -matriz[filas_restar[fila]][columna]
    return matriz

'''
Funciń que crea una fila del tamaño de la matriz, con solo las variables artificiales.
E: La matriz inicial, las filas que se le restarán a la primera fila, las variable básicas, y todas las variables.
S: La matriz inicial con la primera fila con solo las variables artificiales(igualadas a 1.
'''
def colocar_artificiales(matriz, filas_restar, VB, VNB):
    fila_nueva = [0]*len(matriz[0])

    for campo in filas_restar:
        fila_nueva[VNB.index(VB[campo])] = 1
    matriz[0] = fila_nueva
    return matriz

'''
Función principal que acomoda la matriz para ejecutar la segunda fase.
E: La matriz inicial como comenzo, la matriz resultante de la primera fase, las variables básicas, y todas las variables.
S: La matriz acomodada para la segunda fase y todas las variables pero ahora sin las artificiales.
'''
def segunda_fase(matriz, matriz_segunda_fase, VB, VNB):
    matriz_segunda_fase[0] = matriz[0]
    campos_borrar = buscar_columnas_borrar(VNB)
    borrar_columnas(matriz_segunda_fase, VNB, campos_borrar)
    campos_ceros = columnas_validar(matriz_segunda_fase, VB[1:], VNB)
    matriz_segunda_fase = poner_ceros(matriz_segunda_fase, campos_ceros)
    return  (matriz_segunda_fase , VNB)

'''
Función que valida cuales columnas representan variables artificiales.
E: Todas las variables del problema.
S: Número de columnas que son de variables artificiales.
'''
def buscar_columnas_borrar(VNB):
    columnas = []
    for indice in range(len(VNB)):
        if VNB[indice][0] == 'R':
            columnas.append(indice)
    return columnas

'''
Funcion que elimina las columnas de las variables artificiales tanto en la matriz como en el vector de todas
las variables.
E: Matriz resultante de la primera fase, todas las variables, campos de las columnas de variables artificiales.
S: Ninguna.
'''
def borrar_columnas(matriz, VNB, campos):
    columnas_borradas = 0
    for campo in campos:
        VNB.pop(campo - columnas_borradas)
        for fila in matriz:
            fila.pop(campo-columnas_borradas)
        columnas_borradas += 1

'''
Función que valida si las variables básicas estan en cero después de la primera fase.
E: La matriz de la primera fase, las variables básicas, y todas las variables.
S: Número de las columnas que es necesario poner en cero.
'''
def columnas_validar(matriz, VB, VNB):
    columnas = []
    for valor in VB:
        posicion = VNB.index(valor)
        if matriz[0][posicion] != 0:
            columnas.append(VNB.index(valor))
    return  columnas

'''
Función que pone en cero los campo de la primera fila que son variables básicas.
E: La matriz para la segunda fase, y los campos de las variables básicas que hay que poner en cero.
S: La matriz completamente lista para ejecutar la segunda fase con el método simplex.
'''
def poner_ceros(matriz, campos):
    filas = buscar_filas(matriz, campos)
    for i in range(len(campos)):
        multiplo = matriz[0][campos[i]]
        for columna in range(len(matriz[0])):
            matriz[0][columna] = matriz[0][columna]+-multiplo*matriz[filas[i]][columna]
    return matriz

'''
Función auxiliar que ve cuales filas cuantan con los unos para poner en cero las variables báscias en la primer fila.
E: La matriz que se esta acomodando para segunda fase, los campos que representan las columnas de las variables básicas
S: Vector con las filas que se utilizaran. 
'''
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

'''
Función que valida si es posible pasar a segunda fase.
E: Las variables básicas resultantes de primera fase.
S: True si es posible pasar a segunda fase, False de lo contrario.
'''
def comprobar_primera_face(VB):
    tiene_solucion = True
    for variable in VB:
        if variable[0] == 'R':
            tiene_solucion = False
    return tiene_solucion

'''
Función principal que ejecuta el método de dos fases.
E: La matriz inicial, las variables básicas iniciales, todas las variables, y el nombre del archivo que se utiliza.
S: Null si no se pudo resolver, sino la matriz resultante, las variables básicas y todas las variables sin las
    artificiales.
'''
def dos_fases(matriz, VB, VNB, nombre_archivo):
    matriz_primera_fase = primera_fase(matriz[:], VB, VNB)
    (matriz_primera_fase, VB, VNB) = metodoSimplex(matriz_primera_fase, VB, VNB, nombre_archivo)
    # Salio no acotada
    if (matriz_primera_fase == 0):
        return (0,0,0)
    elif( not comprobar_primera_face(VB)):
        print("Variables artificiales resultantes de la primera fase.")
        print("El ejercicio no cuenta con solucion optima.")
        f = open(nombre_archivo + '_sol.txt', 'a')
        f.write('\n' + "No se puede pasar a segunda fase." + '\n')
        f.close()
        return (None, None, None)
    f = open(nombre_archivo + '_sol.txt', 'a')
    f.write('\n' + "Segunda Fase" + '\n')
    f.close()
    (matriz_segunda_fase, nuevo_VNB) = segunda_fase(matriz[:], matriz_primera_fase, VB, VNB[:])
    (matriz_segunda_fase, VB, nuevo_VNB) = metodoSimplex(matriz_segunda_fase, VB, nuevo_VNB,nombre_archivo)

    return (matriz_segunda_fase, VB, nuevo_VNB)
