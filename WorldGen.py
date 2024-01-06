#Libraries
import numpy as np
from numpy import random
import csv
import os


#Other scripts
import Classes as hc
import General as gs


#Settings for world creation
def settings():
    star_count, civs = -1, -1
    ratio = 0
    size = 0
    
    #Save Name
    save_name = input("Enter world name: ")

    while os.path.isdir(f'Saves/{save_name}'):
        save_name = input("\n This world already exists, choose another name:")
    
    #Determines size of star grid
    while size < 25:
        size = int(input("Enter world size (Minimum 25): "))
    
    #Determins ratio of stars to space generated
    while star_count <=0 or star_count>3:
        star_count = int(input("""Enter star count
    1. Small
    2. Medium
    3. Large
    """))
        
    if star_count == 1:
        ratio = size ** 2 * 0.1
    elif star_count == 2:
        ratio = size ** 2 * 0.2
    elif star_count == 3:
        ratio = size ** 2 * 0.3
    
    #Determines number of civilizations generated
    while civs <= 0 or civs > 3:
        civs = int(input("""Enter Civilization Density
    1. Sparse
    2. Normal
    3. Dense
    """))
        
    if civs == 1:
        civ_ratio = size ** 2 * 0.005
    elif civs == 2:
        civ_ratio = size ** 2 * 0.01
    elif civs == 3:
        civ_ratio = size ** 2 * 0.015
        
    civ_ratio, ratio = int(civ_ratio), int(ratio)
    
    print(f"""SETTINGS
    SIZE: {size}
    STAR COUNT: {ratio}
    CIVILIZATION COUNT: {civ_ratio}""")
    
    return size, ratio, civ_ratio, save_name


#Generates the grid for the stars, weighting to decrease likelihood of golden, tyrian and arcane stars from
#spawning
def grid_creation(size, star_ratio):
    world = np.full((size,size), 0)
    
    for i in range(star_ratio):
        
        x, y = random.choice(size), random.choice(size)
        
        if world[x, y] == 0:
            star_type = random.randint(1, 12)
            unique_chance = random.rand()
            if star_type == 11 and unique_chance <= 0.9:
                star_type = random.randint(1, 11)
            elif star_type == 10 and unique_chance <= 0.7:
                star_type = random.randint(1, 10)
            elif star_type == 8 and unique_chance <= 0.5:
                star_type = random.randint(1, 8)
            world[x, y] = star_type
            
    return world

#Assigns traits to stars
def star_trait_generation(world, s_class, save_name):
    #Takes in the type of star then generates traits based on star weights
    def traits(star_type, star_weights):
        for s, weights in star_weights.items():
            if s == star_type:
                star_traits = {"Fertility": weights[0] + round(random.uniform(low = -0.3, high=0.3),2),
                              "Minerals": weights[1] + round(random.uniform(low = -0.3, high=0.3),2),
                              "Savagery": weights[2] + round(random.uniform(low = -0.3, high=0.3),2),
                              "Mana": weights[3] + round(random.uniform(low = -0.3, high=0.3),2),
                              "Water": weights[4] + round(random.uniform(low = -0.3, high=0.3),2)}
            
        return star_traits
    
    global star_names
    star_info = {}
    star_weights ={}
    
    #Opens file containing resource weights for different star types
    weights = gs.open_file("Data/Weights/Star_Trait_Weights.csv")

    star_weights = {i+1:[float(x) for x in weights[i]] for i in range(len(weights))}
    
    #Iterates through all grid spaces and if they are a star, generates a class maps
    #A tuple of the coordinates to the class in a dictionary
    for x in range(len(world)):
        for y in range(len(world)):
            if world[x, y] != 0:
                star_info[(x, y)] = s_class("Undiscovered", world[x,y], 0,0, 
                                 traits(world[x, y], star_weights))
    
    return star_info

#Generates Civilizations for the Start of the Game
def start_civ_generation(world, civ_info, settlement_info, star_info, char_info, Civ, Settlement, Char, civ_count):
    #Loads the weights for races and stores them in a dictionary mapping the name of the race to its preferences
    race_weights = gs.open_file('Data/Weights/Race_Star_Weights.csv')

    race_preferences = {weight[0]:[weight[i] for i in range(len(weight)) if i != 0] for weight in race_weights}

    #Loads coordinates of stars
    coords = [coord for coord in star_info.keys()]

    race_weights = gs.open_file('Data/Weights/Race_Star_Weights.csv')

    #Maps star preferences of races to the names of those races
    race_preferences = {weight[0]:[weight[i] for i in range(len(weight)) if i != 0] for weight in race_weights}

    races = [race for race in race_preferences.keys()]
    coords = [coord for coord in star_info.keys()]

    #Ensures a human civilization exists in the simulation
    while len(civ_info) == 0:
        civ_info, settlement_info, char_info = hc.new_civ(star_info, civ_info, settlement_info, char_info, Civ, Settlement, Char, coords, race_preferences, "Human")

    #Generates the rest of the civs, picking a random race each time
    for i in range(2, civ_count+1):
        civ_info, settlement_info, char_info = hc.new_civ(star_info, civ_info, settlement_info, char_info, Civ, Settlement, Char, coords, race_preferences, random.choice(races))

    return civ_info, settlement_info, char_info