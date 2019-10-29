# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal.
"""

"""
BlackJack: sumar un valor lo más próximo a 21 pero sin pasarse

En un casino cada jugador de la mesa juega únicamente contra el crupier, intentando conseguir una mejor jugada que este.
El crupier está sujeto a reglas fijas que le impiden tomar decisiones sobre el juego. 
Por ejemplo, está obligado a pedir carta siempre que su puntuación sume 16 o menos, y obligado a plantarse si suma 17 o
más. Las cartas numéricas suman su valor, las figuras suman 10 y el As vale 11 o 1, a elección del jugador. 
En el caso del crupier, los Ases valen 11 mientras no se pase de 21, y 1 en caso contrario. 
La mejor jugada es conseguir 21 con solo dos cartas, esto es con un As más carta de valor 10. 
Esta jugada se conoce como Blackjack o 21 natural. Un Blackjack gana sobre un 21 conseguido con más de dos cartas. 

El crupier se pasa de 21. Si se pasa, los jugadores que todavía siguen en la mesa ganaran sus apuestas. 
Los jugadores que todavía seguirán en la mesa son aquellos que no se pasaron de 21 cuando jugaron su mano, 
ya que cuando un jugador se pasa de 21 pierde sus apuestas y deja de formar parte de la partida en el momento 
que se pasa.

El crupier no se pasa de 21. Según las reglas del blackjack que debe cumplir, su mano siempre tendrá un valor 
igual o mayor que 17. Por tanto, los jugadores que se plantaron con una mano con un valor menor a 17 solo podrán 
ganar si el crupier se pasa.
"""

####  Participantes

#1.- Crupier
#2.- N jugadores

### Condiciones del crupier:
# - Obligado a seguir tomando cartas(Crupier keep playing) si su puntuación máxima son <= 16
# - Obligado a plantarse (Crupier stop playing) si su puntuación máxima son >= 17 y <= 21
# - El As vale 11 para el crupier si su puntuación es >=17 y <=21, y vale 1 si su puntuación es >=21


### Valores de las cartas:
# Las cartas numéricas valen el número en sí
# Los 'monos' valen 10 y es As puede valer 11 o 1 según la elección del jugador



### Pasos a seguir

# - Definir un diccionario con las cartas y sus respectivos valores
# - Input al número de jugadores, máximo pueden ser 3.
# - Definir al crupier que siempre va a jugar a parte de los n jugadores
# - Crear una función para los juegos de los n
# - Crear una función para el juego del crupier
# - Crear una función para comparar el resultado de todos los involucrados


#Definir el número de jugadores ya en una lista
#def n_jugadores():
#    while True:
#        try:
#            n = int(input("Cuántos le entran?: "))
#            if n > 0 and n <=3:
#                lst_jugadores = [e for e in range(n)]
#                lst_jugadores.append(len(lst_jugadores))
#                return lst_jugadores
#            else:
#                print("Máximo 3 jugadores, mínimo 1")
#        except ValueError:
#            print("No strings allowerd: Máximo 3 jugadores, mínimo 1")
#    
#n = n_jugadores()

################################################################################

### Condiciones del juego
# 1.-Si tu total > 21 pierdes
# 2.-Si el Crupier se pasa de 21 los jugadores ganan
# 3.-Puedes campechanear el valor de tus As's a como te convenga
# 4.-Si salen 4 cartas del mismo key, esta deja de entrar en el juego

import random

######  Jalas o te quedas? #########
def decision_jugador():
    
    while True:
        
        desicion = input("Te quedas (q) o jalas otra carta (j)")
        
        if desicion == 'j':
            return False  
        elif desicion == 'q':
            return True 
        else:
            print("Las opciones válidas son 'q' para quedarse o 'j' para jalar otra carta")


####### La condición del valor del As  ###########
def total_mano(mano):
    total = 0
    for carta in mano:
	    if carta == "Jota" or carta == "Reina" or carta == "Rey":
	        total+= 10
	    elif carta == "As":
	        if total >= 11: total+= 1
	        else: total+= 11
	    else: total += carta
    return total


##########   Juego General   ########
def el_juego():
    baraja = [1,2,3,4,5,6,7,8,9,10,'Jota', 'Reina', 'Rey', 'As']
    baraja = baraja*4
    random.shuffle(baraja)
    jugador = [baraja.pop() for e in range(2)]
#    crupier = [deck.pop() for e in range(2)]
    
    while True:
        print("Estas son las cartas que tienes actualmente", jugador)
        
        total_puntos = total_mano(jugador)
        if total_puntos == 21:
            print("Mano:", jugador)
            print("Ganaste!")
            return 'win'
            #break
        
        quedarse = decision_jugador()
                      
        if quedarse:
            print("Aquí decidiste quedarte. Puntos finales:", total_puntos)
            return total_puntos
            #break
        elif not quedarse:
            jugador.append(baraja.pop())
            total_puntos = total_mano(jugador)
        
        if total_puntos > 21:
            print("Mano:", jugador)
            print("Te acabas de pasar con un total de:", total_puntos)
            return  'lost'
            #break
        elif total_puntos == 21:
            print("Mano:", jugador)
            print("Ganaste!")
            return 'win'
            #break

el_juego()

#def main():
#    
#    print("Jugador 'a', empieza")
#    a = el_juego()
#    print("Jugador 'b', dale que es mole de olla")
#    b = el_juego()
#    
#    if a>b:
#        return "El jugador 'a' es el ganador"
#    elif b>a:
#        return "El jugador 'b' es el ganador"
#    elif a == 'win':
#        return "El jugador 'a' ha ganado"
#    elif a == 'lost':
#        return "El jugador 'b' ha ganado"
#
#main()

