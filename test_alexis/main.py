from menu import main as starting
from choix_perso import main as choix
from choix_map import main as choix2 


def debut():

    tabinfo = ["", "", ""]

    def suivant1(tabinfo):
        
        suiv = "feur"
        while suiv != "quitter":
            suiv = choix()
            
            if suiv == "retour":
                manager(tabinfo)
                
            if suiv[2] == "suivant":
                tabinfo[1] = suiv[0]
                tabinfo[2] = suiv[1]
                print(tabinfo)
                suivant2(tabinfo)
                
    def suivant2(tabinfo):
        
        print("SUIVVVVANNNT")
        suiv = "feur"
        while suiv != "quitter":
            suiv = choix2()
            
            if suiv == "retour":
                manager(tabinfo)
            
            if suiv[1] == "fini":
                tabinfo[0] = suiv[0]
                print(tabinfo)
                manager(tabinfo)
                
                
            

    def manager(tabinfo):
        
        
        if tabinfo[0] == "":
            
            suiv = "feur"
            while suiv != "stop":

                suiv = starting()
                
                print(suiv)
                if suiv == "choix_perso":
                    suivant1(tabinfo)
                    
                if suiv == "quitter":
                    quit()
        
        print(tabinfo)
        return tabinfo

    return manager(tabinfo)

debut()
    

