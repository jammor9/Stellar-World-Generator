#Libraries
import numpy as np

import tkinter as tk
from tkinter import ttk

import matplotlib.pyplot as plt
from matplotlib import colors

#Other Scripts
import WorldGen as wg
import Save as save
import Classes as hc

#Global Variables
star_names = {0:"Space",1:"Verdant",2:"Primeval",3:"Stone",4:"Submerged",5:"Dry",6:"Tropical",7:"Frosty",
                  8:"Arcane",9:"Crimson",10:"Tyrian",11:"Golden"}

star_color = {0:'#000000',1:'#6cf542',2:'#243d1d',3:'#5e5b55',4:'#223b7a',5:'#7a6f41', 
            6:'#3f4d25',7:'#34a8a8',8:'#41ba65',9:'#590c22',10:'#4e0e63',11:'#e0b710'}

char_type = {0:"Leader",1:"Adventurer",2:"Scholar"}

policy = {0:"Colonial Expansion", 1:"Military Conflict", 2:"Economic Development", 3:"Diplomatic Development"}

#Base Program Function
def generate_world():
    #Reads in classes from Classes.py
    Civ, Char, Star, Settlement, Deity, Pantheon = hc.classes()

    #Base Dictionaries that contain all data for the simulation
    star_info, char_info, settlement_info, civ_info, pantheon_info, deity_info = {}, {}, {}, {}, {}, {}
    
    print("Welcome to Solar WorldGen, starting generation...")
    size, star_ratio, civ_count, save_name, max_years = wg.settings()
    world = wg.grid_creation(size, star_ratio)
    
    while any(i not in world for i in range(12)):
        print("World rejected... New generation begun\n")
        world = wg.grid_creation(size, star_ratio)

    #Generates World Data for Star Grid Tiles
    star_info = wg.star_trait_generation(world, Star, save_name)

    #Generates game star civs
    civ_info, settlement_info, char_info = wg.start_civ_generation(world, civ_info, settlement_info, star_info, char_info, Civ, Settlement, Char, civ_count)

    #Generates game start pantheons and deities
    civ_info, pantheon_info, deity_info = wg.pantheon_generation(world, civ_info, pantheon_info, deity_info, Deity, Pantheon)
    
    #Saves the simulation and displays resulting grid
    #save.save_data(world, star_info, civ_info, char_info, settlement_info, deity_info, pantheon_info, save_name)
    tkinter_grid(world, len(world))
    
    return

def grid_display(world):
    global star_names
    
    unique, count = np.unique(world, return_counts = True)
    
    for u, c in zip(unique, count):
        print(f"{star_names[u]} Stars appear {c} times")
    
    star_col = colors.ListedColormap(['#000000','#6cf542', '#243d1d', '#5e5b55', '#223b7a', '#7a6f41', 
                                      '#3f4d25', '#34a8a8', '#41ba65', '#590c22','#4e0e63', '#e0b710'])
    
    plt.pcolormesh(world, cmap = star_col)
    plt.colorbar()
    plt.show()
    return

def tkinter_grid(world, size):
    global star_color, star_names

    root = tk.Tk()

    s = ttk.Style()

    s.configure('window.TFrame', background = "#000000")

    for i in range(len(star_color)):
        s.configure(f'{star_names[i]}.TFrame', background = f'{star_color[i]}')
    
    mainFrame = ttk.Frame(root, width = size, height = size, style = 'window.TFrame')

    for x in range(size):
        for y in range(size):
            print("Writing:",x,y)
            frame = ttk.Frame(mainFrame, width = 1, height = 1, style = f'{star_names[world[x, y]]}.TFrame')
            frame.grid(row = x, column = y)

    mainFrame.grid(row = 0, column = 0)

generate_world()

print("Finished")