#Contains general functions used throughout the code

import random
import csv

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

#Reads the weights from .csv files that use ';' delimiters
def open_weights(path):
    with open(path, encoding="utf8") as r:
        lines = [x for x in csv.reader(r, delimiter=";")]
    
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            lines[i][j] = lines[i][j].split(",")
            for k in range(len(lines[i][j])):
                lines[i][j][k] = float(lines[i][j][k])
    
    return lines

#Declares that a star has been discovered and updates info for the star
def star_discovered(race, s_class):
     
    #Generates a name for the star based of the language data of the discovering race
    names = open_file(f'Data/Language/{race}/Stars.csv')
    name = random.choice(names[0]) + random.choice(names[1])
    s_class.name = name
    s_class.discovered = True
    return s_class