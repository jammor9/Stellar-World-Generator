#Contains general functions used throughout the code

import random

#Used to open a .csv file and strip the lists of any whitespace
def open_file(path):
    with open(path) as r:
        l = [ri.strip("\n").split(",") for ri in r]
    
    for i in range(len(l)):
        fl = []
        for x in l[i]:
            if x != "":
                fl.append(x)
        l[i] = fl

    return l

def star_discovered(race, s_class):
     
    #Generates a name for the star based of the language data of the discovering race
    names = open_file(f'Data/Language/{race}/Stars.csv')
    name = random.choice(names[0]) + random.choice(names[1])

    s_class.name = name
    s_class.discovered = True

    #print(f"STAR DISCOVERED: {vars(s_class)}")
    return s_class