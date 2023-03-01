import os

rootdir = os.getcwd()

lines = 0

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        filepath = subdir + os.sep + file
        if filepath.endswith(".py"):
            os.system(f"pylint {filepath}")