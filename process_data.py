write = ""

with open("training_data.csv", "r") as f:
    file = f.readlines()

# Remove the last column
for i in file:
    sp = i.split(",")
    write += ("".join([i + "," for i in sp[:-1]]))[:-1] + "\n"

with open("data.csv", "w") as f:
    f.write(write)
