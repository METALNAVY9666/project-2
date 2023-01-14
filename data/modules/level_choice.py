"""contient les classes permettant de sélectionner un niveau, module temporaire donc en s'en branle de pep8 OQUS%ODHqhdIHMMSIOKDHMQIOHSDIUQHSD nanaère la ligne est longue jmen blk"""
from tkinter import Tk, Button
from data.modules.settings import read_levels


choice = None

def pick_level():
    """créer une fenetre de choix de niveaux"""

    levels = list(read_levels().keys())


    root = Tk()

    for level in levels:
        Button(root, text=level, command = lambda x=level : pick(root, x)).pack()

    root.mainloop()
    print(choice)
    return choice

def pick(tk, level):
    """renvoie le niveau sélectionné"""
    global choice # ooooouuuuu le global ouuuuu jmen fous
    tk.destroy()
    choice = level
    