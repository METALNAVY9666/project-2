from menu import main as starting
from choix_perso import main as choix
from choix_map import main as choix2 


def suivant1():
    
    suiv = "feur"
    while suiv != "quitter":
        suiv = choix()
        
        if suiv == "retour":
            manager()
            
        if suiv[2] == "suivant":
            suivant2()
            
def suivant2():
    
    print("SUIVVVVANNNT")
    suiv = "feur"
    while suiv != "quitter":
        suiv = choix2()
        
        if suiv == "retour":
            manager()
            


def manager():
    suiv = "feur"
    
    while suiv != "stop":

        suiv = starting()
        
        print(suiv)
        if suiv == "choix_perso":
            suivant1()
            
        if suiv == "quitter":
            quit()
        
manager()
    

