"""programme permettant de générer des niveaux rapidement"""
import json
from tkinter import Tk, Button, Label, Listbox
from tkinter.filedialog import askopenfilename, askdirectory

buttons = {}
labels = {}

texts = {
    "edit": "Modifier le niveau séléctionné",
    "add": "Ajouter un niveau",
    "add_bg": "Ajouter un fond"
}

def read_levels():
    """lis les niveaux"""
    with open("../gfx/levels/levels.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        file.close()
    return data

def add_bg():
    """ajoute un niveau"""
    

def edit_level():
    """modifie le niveau"""
    ...

root = Tk()
root.title("Générateur de niveaux")
root.geometry("480x360")
root.resizable(False, False)

labels["edit"] = Label(root, text="Modifier un niveau")
labels["edit"].grid(column=0, row=0)

buttons["edit"] = Button(root, text=texts["edit"], command=edit_level)
buttons["edit"].grid(column=0, row=1)

levels_box = Listbox(root)
for level in list(read_levels().keys()):
    levels_box.insert("end", level)
levels_box.grid(column=0, row=2)

labels["add"] = Label(root, text=texts["add"])
labels["add"].grid(column=1, row=0, columnspan=2)

buttons["add_bg"] = Button(root, text=texts["add_bg"], command=add_level)
buttons["add_bg"].grid(column=1, row=1)

labels["bg"] = Label(root)
labels["bg"].grid(column=1, row=2)

root.mainloop()