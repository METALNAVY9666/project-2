"""programme permettant de générer des niveaux rapidement"""
import json
from tkinter import Tk, Button, Label, Listbox
from tkinter.filedialog import askopenfilename, askdirectory

buttons = {}
labels = {}

def read_levels():
    """lis les niveaux"""
    with open("../gfx/levels/levels.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        file.close()
    return data

def edit_level():
    """modifie le niveau"""

root = Tk()

labels["edit"] = Label(root, text="Modifier un niveau")
labels["edit"].grid(column=0, row=0)

levels_box = Listbox(root)
for level in list(read_levels().keys()):
    levels_box.insert("end", level)
levels_box.grid(column=0, row=1)

buttons["edit"] = Button(root, text="Modifier le niveau séléctionné", command=edit_level)
buttons["edit"].grid(column=0, row=2)

root.mainloop()