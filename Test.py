import csv

with open('Data/Events/Civ_Event_Weights.csv', encoding="utf8") as r:
    cs = csv.reader(r, delimiter=";")
    lines = [x for x in cs]

fixed_a = []

for i in range(len(lines)):
    for j in range(len(lines[i])):
        lines[i][j] = lines[i][j].split(",")
        for k in range(len(lines[i][j])):
            lines[i][j][k] = float(lines[i][j][k])

        