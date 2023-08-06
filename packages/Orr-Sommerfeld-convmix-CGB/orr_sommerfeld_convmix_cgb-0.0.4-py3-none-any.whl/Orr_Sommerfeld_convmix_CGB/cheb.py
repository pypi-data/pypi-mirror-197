def cheb(N):
    if N==0: 
        D = 0.; x = 1.
    else:
        n=arange(0,N+1) #genero un vector que va desde 0 hasta N+1 con paso 1
        #Tomo el array n y lo convierto en una matriz de N+1 filas (cada fila le aplica el coseno)y 1 columna
        x = cos(pi*n/N).reshape(N+1,1)
        #hstack concatena 3 arrays: [2.] con ones(N-1) con [2.]. Y luego los afecta por (-1)**n. Como resultado
        #obtengo un array de N+1, al cual luego le hago reshape para hecerlo columna
        c = (hstack(( [2.], ones(N-1), [2.]))*(-1)**n).reshape(N+1,1)
        #Genero una matríz con tile(). En este caso toma al vector x y lo convierte en una matriz de 1 fila y N+1 columnas
        #Pero cada elemento de la matriz nueva es el vector x. Entonces el vector columna x (de N+1 filas) 
        #se replica N+1 veces, dando como resultado una matriz cuadrada de N+1xN+1
        X = tile(x,(1,N+1)) 
        #Defino dX como la resta de X y su transpuesta
        dX = X - X.T
        # c*(1./c).T Crea los coeficientes de atras de cada elemento de D
        D=(c*(1./c).T)/(dX+eye(N+1))
        #Resto D menos una matriz donde cada elemento de la diagonal contiene la suma de los elementos de la
        #columna de D.T correspondiente
        D=D-diag(sum(D.T,axis=0)) 
        #retorno tanto D como el vector que tiene los puntos de Chebyshev, como un vector fila
    return D, x.reshape(N+1)
