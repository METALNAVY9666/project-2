import os

rootdir = os.getcwd()

lines = 0

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        #print os.path.join(subdir, file)
        filepath = subdir + os.sep + file

        if filepath.endswith(".py") and not "line_count" in filepath:
            with open(filepath, "r", encoding="utf-8") as file:
                temp = file.readlines()
                file.close()
            lines += len(temp)
print(lines)