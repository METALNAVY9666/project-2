from menu import main as starting
from choix_perso import main as choix


def suivant1():
    
    suiv = "feur"
    while suiv != "quitter":
        suiv = choix()
        
        if suiv == "retour":
            manager()


def manager():
    suiv = "feur"
    
    while suiv != "quitter":

        suiv = starting()
        
        print(suiv)
        if suiv == "choix_perso":
            suivant1()
        
manager()
    

