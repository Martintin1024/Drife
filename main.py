import random

### DICCIONARIO PARA RANDOMIZADO ###


## DICCIONARIO CHILL ##

opciones_chill = {
    1 : 0.25,
    2 : 0.20,
    3 : 0.05,
    4 : 0.05,
    5 : 0.20,
    6 : 0.20,
    7 : 0.05
}

## DICCIONARIO CHILL ##


## DICCIONARIO TOCHO ##

opciones_tocho = {
    1 : 0.30,
    2 : 0.30,
    3 : 0.30,
    4 : 0.10
}

## DICCIONARIO TOCHO ##



### FUNCIONES ###

## RECOMPENSAS CHILL ##

def nada():
    print("Respirá profundo y seguí con tu vida crack")

def meditar():
    print("Frenate 10 minutos y meditá, que te vas a sentir mucho más tranquilo")

def musica():
    print("Escuchate dos temitas pa y volvé a la carga")

def comer():
    print("Hacete algo para morfar gordito, que seguro quemaste bastante energía")

def mona():
    print("Andá a jugar con mona, le vas a hacer un favor a los dos")

def sol():
    print("La vitamina D te llama, tomate un ratito de sol")

def baño():
    print("Bañate sucio (mentira, te quiero)")

## RECOMPENSAS CHILL ##



## RECOMPENSAS TOCHAS ##

def jugar():
    print("Jugate lo que quieras pa, te lo ganaste")

def paseo():
    print("Te ganaste un paseo (si es de noche guardatelo para otro dia)")

def album():
    print("Estas de suerte, te ganaste escuchar un album de principio a fin, disfrutalo putita")

def baño_musical():
    print("Hoy te toca mover el orto mientras te bañás, te lo ganaste")

## RECOMPENSAS TOCHAS ##





## RANDOMIZADO CHILL ##

def chill_random(probabilidades): ### DECLARAMOS FUNCION
    r = random.random() ### RANDOMIZAMOS VALOR
    for opciones, prob in probabilidades.items(): ### ARRANCAMOS CICLO FOR: OPC ES LA CLAVE DEL DICT, PROB EL VALOR, Y PROB.ITEMS() EL NUMERO MAXIMO DE VUELTAS (en este caso, seria el total de items)
        if r < prob: ### SI LA PROB > R
            return opciones ### SALE DE LA FUNCION DEVOLVIENDO LA CLAVE EN LA QUE CORTÓ
        r -= prob ### SI NO RESTA EL VALOR Y VUELVE A ARRANCAR

### EJEMPLO (MOMENTO EN EL QUE LO CREO)

### SI R = 24, ENTRA AL BUCLE, Y ME DEVUELVE 1
### SI R = 26, ENTRA AL BUCLE, RESTA PROB PORQUE NO ENTRÓ, DA LA SEGUNDA VUELVA Y DEVUELVE 2 PORQUE SI ENTRÓ

## RANDOMIZADO CHILL ##




## RANDOMIZADO TOCHO ##

def tocho_random(probabilidades): ### DECLARAMOS FUNCION
    r = random.random() ### RANDOMIZAMOS VALOR
    for opciones, prob in probabilidades.items(): ### ARRANCAMOS CICLO FOR: OPC ES LA CLAVE DEL DICT, PROB EL VALOR, Y PROB.ITEMS() EL NUMERO MAXIMO DE VUELTAS (en este caso, seria el total de items)
        if r < prob: ### SI LA PROB > R
            return opciones ### SALE DE LA FUNCION DEVOLVIENDO LA CLAVE EN LA QUE CORTÓ
        r -= prob ### SI NO RESTA EL VALOR Y VUELVE A ARRANCAR

## RANDOMIZADO TOCHO ##

### DEVOLUCIONES ###

def devolver_chill():
    print("Felicidades por terminar tu sesión, acá está tu recompensa: ")
    premio = chill_random(opciones_chill)
    if int(premio) == 1:
        nada()
    elif int(premio) == 2:
        meditar()
    elif int(premio) == 3:
        musica()
    elif int(premio) == 4:
        comer()
    elif int(premio) == 5:
        mona()
    elif int(premio) == 6:
        sol()
    elif int(premio) == 7:
        baño()

def devolver_tocho():
    print("Felicidades por terminar tu dia de trabajo, acá está tu recompensa: ")
    premio = tocho_random(opciones_tocho)
    if int(premio) == 1:
        jugar()
    if int(premio) == 2:
        paseo()
    if int(premio) == 3:
        album()
    if int(premio) == 4:
        baño_musical()

### DEVOLUCIONES ###

### CODIGO MAIN ###

print("BIENVENIDO A LA RULETA DE LA VICTORIA")
print("Usted esta aquí para elegir su recompensa")
print("En primer lugar, qué tipo de recompensa quiere?")
recompensa = input("Pulse 1 si es entre sesiones de trabajo o 2 si ya terminó de trabajar: ")

if int(recompensa) == 1:
    devolver_chill()
elif int(recompensa) == 2:
    devolver_tocho()