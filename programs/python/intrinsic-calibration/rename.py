import os

# read all folders that have a number in the name

# for each folder, read all images

def rename_files(folder):
    files = os.listdir(folder)
    print(files)
    for i, file in enumerate(files):        
        os.rename(folder + "/" + file, "../testall/" + folder.replace("../", "") + str(i) + ".png")

# for each folder

res = [x for x in os.listdir("../") if any(i.isdigit() for i in x) and not any(i == "." for i in x)]
print(res)

for folder in res:
    rename_files("../" + folder)
