#Libraries
import csv
import os
import numpy as np

def save_data(world, star_info, civ_info, char_info, settlement_info, deity_info, pantheon_info, save_name):
        
        #Creates Save Directories
        os.mkdir(f'Saves/{save_name}')
        os.mkdir(f'Saves/{save_name}/World')

        np.savetxt(f'Saves/{save_name}/World/Grid.csv', world, delimiter=",")

        def save_file(path, info):
            with open(path, 'w', newline="") as outfile:
                r = csv.writer(outfile)
                for i, data in info.items():
                    print(vars(data).values())
                    l = list(vars(data).values())
                    print(l)
                    l.insert(0, i)
                    print(l)
                    print(f"""WRITING\n
ID: {i}
DATA: {l}""")
                    r.writerow(l)

        save_file(f"Saves/{save_name}/World/Star_Data.csv", star_info)
        save_file(f"Saves/{save_name}/World/Civ_Data.csv", civ_info)
        save_file(f"Saves/{save_name}/World/Char_Data.csv", char_info)
        save_file(f"Saves/{save_name}/World/Settlement_Data.csv", settlement_info)
        save_file(f"Saves/{save_name}/World/Deity_Data.csv", deity_info)
        save_file(f"Saves/{save_name}/World/Pantheon_Data.csv", pantheon_info)
        
        return