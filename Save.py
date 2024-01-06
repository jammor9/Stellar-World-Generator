#Libraries
import csv
import os
import numpy as np

def save_data(world, star_info, civ_info, char_info, settlement_info, save_name):
        
        #Creates Save Directories
        os.mkdir(f'Saves/{save_name}')
        os.mkdir(f'Saves/{save_name}/World')

        np.savetxt(f'Saves/{save_name}/World/Grid.csv', world, delimiter=",")        

        with open(f"Saves/{save_name}/World/Star_Data.csv", 'w', newline="") as outfile:
            r = csv.writer(outfile)
            for coord, s_data in star_info.items():
                print(f"""WRITING \n
COORDINATES: {coord}
STAR DATA: {vars(s_data)}\n\n""")
                r.writerow([coord, s_data.name, s_data.variant, s_data.discovered, s_data.settled, s_data.traits])

        with open(f"Saves/{save_name}/World/Civ_Data.csv", 'w', newline="") as outfile:
            r = csv.writer(outfile)
            for civ_id, civ_data in civ_info.items():
                print(f"""WRITING \n
ID: {civ_id}
CIV DATA: {vars(civ_data)}\n\n""")
                r.writerow([civ_id, civ_data.name, civ_data.home_star, civ_data.controlled, civ_data.star_prefs, civ_data.traits, civ_data.ruler, civ_data.economy, civ_data.policy])

        with open(f"Saves/{save_name}/World/Char_Data.csv", 'w', newline="") as outfile:
            r = csv.writer(outfile)
            for char_id, char_data in char_info.items():
                print(f"""WRITING \n
ID: {char_id}
CHAR DATA: {vars(char_data)}\n\n""")
                r.writerow([char_id, char_data.name, char_data.race, char_data.type, char_data.traits, char_data.location, char_data.age, char_data.status, char_data.max_hp, char_data.hp])

        with open(f"Saves/{save_name}/World/Settlement_Data.csv", 'w', newline = "") as outfile:
            r = csv.writer(outfile)
            for coord, set_data in settlement_info.items():
                print(f"""WRITING \n
COORDINATES: {coord}
SETTLEMENT DATA: {vars(set_data)}\n\n""")
                r.writerow([coord, set_data.name, set_data.leader, set_data.economy, set_data.population, set_data.characters])
        
        return