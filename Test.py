with open('Saves/Solaris/World/Star_Data.csv') as r:
    out_file = [line.strip("\n") for line in r.readlines()]
for file in out_file[0].split(","):
    print(file)

print(type(out_file[0].split(",")[5]))