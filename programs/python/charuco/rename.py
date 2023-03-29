import os

# read all folders that have a number in the name

# for each folder, read all images

def rename_files(folder):
    files = os.listdir(folder)
    print(files)
    for i, file in enumerate(files):
        print("./testall/" + folder.replace("./","") + "_" + file)
        os.rename(folder + "/" + file, "./testall/" + folder.replace("./","") + "_" + file)
        pass

# for each folder

res = [x for x in os.listdir("./") if any(i.isdigit() for i in x) and not any(i == "." for i in x)]
print(res)

for folder in res:
    print(folder)
    rename_files("./" + folder)
