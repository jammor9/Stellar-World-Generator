import numpy as np
from numpy import random

import matplotlib.pyplot as plt


#Base Markov Chain
def markov(ls, la, n = 300):
    pi = np.array([0, 0 ,0, 0])

    start_state = random.randint(0, len(ls))
    prev_state = start_state
    pi[start_state] = 1

    print(f'{ls[start_state]} ----->', end = " ")

    for i in range(n):
        current_state = random.choice([x for x in range(len(ls))], p=la[prev_state])
        prev_state = current_state
        pi[current_state] += 1
        print(f'{ls[current_state]} ----->', end=" ")

    return print(f'\n {pi/n}')

markov(["burger", "pizza", "hot dog", "rectangle"], [[0.4, 0.4, 0.2, 0], [0.3, 0.3, 0.4, 0], [0.8, 0.2, 0, 0], [0.2, 0, 0, 0.8]], n=30_000)

#Transient Markov

#Burger is a transient state
#   This is because there is no way to return to burger once it has been left
#The other two are recurrent as they can be returned to

#Transient Markovs can be reduced down to become irreducible
#markov(["burger", "pizza", "hot dog"], [[0.7, 0.3, 0], [0, 0.5, 0.5], [0, 0.3, 0.7]])
        