#This file contains the base structure data for classes
#It also contains the functions needed to create a new class actor

#Libraries
from numpy import random
import General as gs

def classes():
    #Civilization Class
    #Name is the Name of the Civilization
    #Home Star is the coordinates indicating the capital of the Civ
    #Controlled is a list of tuples relating to coordinates of controlled stars
    #Star Preferences is the preferred stars of the Civ, usually determined by race
    #Traits are the unique attributes of the Civ that determine how it acts in the game
    #Ruler is the leader of the civ, their traits can influence Civ Traits
    #Modifiers are currently active effects that modify the state of the civilization
    #Pantheon is the group of deities the civilization worships
    class Civ:
        def __init__(self, name, home_star, controlled, star_prefs, traits, ruler, economy, policy, modifiers, pantheon):
            self.name = str(name)
            self.home_star = tuple(home_star)
            self.controlled = list(controlled)
            self.star_prefs = list(star_prefs)
            self.traits = list(traits)
            self.ruler = str(ruler)
            self.economy = list(economy)
            self.policy = int(policy)
            self.modifiers = list(modifiers)
            self.pantheon = str(pantheon)
        
    #Character Class
    #Name is the name of the character
    #Race is the race of the character
    #Type is what role a Character plays (Leader, Scholar, Adventurer)
    #Traits influence how the character acts in the world
    #Location is the current coordinates of the character
    #Age is the age of the character, influences health of character
    #Status is whether the character is alive or dead
    #Max_HP is the maximum HP of a character, HP is their current HP
    class Char:
        def __init__(self, name, race, type, traits, location, age, status, max_hp, hp):
            self.name = str(name)
            self.race = str(race)
            self.type = int(type)
            self.traits = list(traits)
            self.location = tuple(location)
            self.age = int(age)
            self.status = bool(status)
            self.max_hp = int(max_hp)
            self.hp = int(hp)

    #Star Class
    #Name is the name of the star, usually starts as "Undiscovered"
    #Variant is the type of star such as verdant, arcane, etc.
    #Discovered tells the simulation whether the star has been discovered by a civ and is active in the game
    #Settled tells the simulation whether the star is settled and should be checked for settlement activity
    #during a turn
    #Traits are the unique attributes of a star such as fertility, mineral quantity, etc. 
    class Star:
        def __init__(self, name, variant, discovered, settled, traits):
            self.name = str(name)
            self.variant = int(variant)
            self.discovered = bool(discovered)
            self.settled = bool(settled)
            self.traits = dict(traits)

    #Settlement Class
    #Name of the settlement
    #Traits are unique attributes of the settlement
    #Character who leads the settlement and influences policy
    #Population is the number of residents of the settlement
    #Characters are notable people who are either permanently or temporarily residing in the settlement
    #Modifiers are currently active effects on the state of the Settlement
    class Settlement:
        def __init__(self, name, leader, economy, population, characters, modifiers):
            self.name = str(name)
            self.leader = str(leader)
            self.economy = list(economy)
            self.population = int(population)
            self.characters = list(characters)
            self.modifiers = list(modifiers)

    #Deity Class
    #Name is the name of the Deity
    #Traits is the traits of the deity
    #Pantheons is groups of Deities that this deity is a part of
    #Type is the type of Deity the Deity is (Celestial, Draconic, Demonic, Beastly)
    #Domain is the area the god has power over (Death, Fertility, Harvest, etc.)
    class Deity:
        def __init__(self, name, traits, type, domain):
            self.name = str(name)
            self.traits = list(traits)
            self.type = int(type)
            self.domain = str(domain)

    #Pantheon Class
    #Name is the name of the pantheon
    #Domain is the domain of the pantheon relating to a certain character trait
    #Members are the gods who are a member of the pantheon
    class Pantheon:
        def __init__(self, name, domain, members):
            self.name = str(name)
            self.domain = str(domain)
            self.members = list(members)

    return Civ, Char, Star, Settlement, Deity, Pantheon


#Creates a new settlement
def new_settlement(star_info, settlement_info, char_info, Char, Settlement, race, coord, population = random.randint(50, 100)):
    
    #Connects name of settlement to name of resident star
    name = star_info[coord].name
    
    #Creates a new character to be the leader of the civ
    char_info = new_character(char_info, Char, coord, race, 0, age = random.randint(21, 42))

    #Generates development points for settlement
    #Prioritizes based on resources of star
    econ = []

    #Creates a class and maps the coordinate of the settlement to the class
    settlement_info[coord] = Settlement(name, len(char_info)-1, econ, population, [], [])
    return settlement_info, char_info


#Creates a new Character
def new_character(char_info, Char, coord, race, type = -1, age = 18):
    global char_type

    #Pick a name from the name data for the character race
    names = gs.open_file(f'Data/Language/{race}/Names.csv')
    name = " ".join([random.choice(names[0]), random.choice(names[1])])

    #Loads trait data and picks traits based off character type
    #LANGUAGE TRAITS IS FOR PICKING TRAITS
    #WEIGHTS TRAITS IS FOR WHAT THE TRAIT DOES
    if type < 0: 
        type = random.choice(0, len(char_type))

    traits = gs.open_file("Data/Language/Traits.csv")[0]
    traits = [random.choice(traits) for i in range(3)]

    #Creates the class for the new character and maps the ID to the class in the char_info dict
    char_info[len(char_info)] = Char(name, race, type, traits, coord, age, 0, 100, 100)

    return char_info

#New Civilization
def new_civ(star_info, civ_info, settlement_info, char_info, Civ, Settlement, Char, coords, race_preferences, race):
    Valid = False
    Checked_Coords = []

    while not Valid:
        coord = coords[random.randint(0, len(coords))]
        for star in range(len(race_preferences[race])):
            if race_preferences[race][star].isdigit() and int(race_preferences[race][star]) == 1 and star_info[coord].variant == star:
                Valid = True
                break

        Checked_Coords.append(coord)
        if len(Checked_Coords) == len(coords) and Valid == False:
            return 
        
    #Updates Discovery Status and Name of Capital Star
    star_info[coord] = gs.star_discovered(race, star_info[coord])

    #Establishes a settlement in the home system
    settlement_info, char_info = new_settlement(star_info, settlement_info, char_info, Char, Settlement, race, coord, population = 10_000)

    #Creates a ruler for the civilization
    char_info = new_character(char_info, Char, coord, race, type = 0, age = random.randint(31, 72))
    ruler = char_info[len(char_info)-1]

    #Generates Civilization Traits
    traits = [random.choice(gs.open_file('Data/Language/Traits.csv')[1]) for i in range(3)]

    #Generates Civ Name
    govs = gs.open_file(f'Data/Language/{race}/Gov.csv')[0]

    #Selects a random government type using a random integer and the loaded csv file
    gov_types = gs.open_file('Data/Language/Gov_Types.csv')[random.randint(0, 2)]

    name = f"The {random.choice(gov_types)} of {random.choice(govs)}"

    #Takes starting economy from first settlement
    economy = settlement_info[coord].economy

    #Creates new civ mapping its ID to the class
    civ_info[len(civ_info)] = Civ(name, coord, [coord], race_preferences[race], traits, ruler, economy, 0, [], "")
    return civ_info, settlement_info, char_info

def new_deity(deity_info, Deity, deity_data, n):
    domain = deity_data[n][0]
    print(domain)
    name = f"{random.choice(deity_data[0])}, God of {domain}"
    while name in list(deity_info.keys()):
        name = f"{random.choice(deity_data[0])}, God of {domain}"
    traits = deity_data[n][1:]
    deity_info[domain] = Deity(name, traits, 0, domain)
    return deity_info