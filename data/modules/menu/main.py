from data.modules.menu.menu import main as starting
from data.modules.menu.choix_perso import main as choix
from data.modules.menu.choix_map import main as choix2


def debut():

    tabinfo = ["", "", ""]

    def suivant1(tabinfo):
        
        if tabinfo[0] == "":
            suiv = "feur"
            while suiv != "quitter":
                suiv = choix()
                
                if suiv == "retour":
                    manager(tabinfo)
                    
                if suiv[2] == "suivant":
                    tabinfo[1] = suiv[0]
                    tabinfo[2] = suiv[1]
                    print(tabinfo)
                    return suivant2(tabinfo)
                
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
                return "ok"
                
                
            

    def manager(tabinfo):
        
        
        if tabinfo[0] == "":
            
            suiv = "feur"
            while suiv != "stop":

                suiv = starting()
                
                print(suiv)
                if suiv == "choix_perso":
                    return suivant1(tabinfo)
                    
                if suiv == "quitter":
                    quit()
        
    print(tabinfo)
    manager(tabinfo)
    print(tabinfo)
    return tabinfo
    

