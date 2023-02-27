""" Ce module permet de racorder le menu principal, le menu de choix des
personnages et le menu de choix de map. Ce qui permettera ensuite de récolter
les informations des persos et de la map choisis."""
from data.modules.menu.menu import main as starting
from data.modules.menu.choix_perso import main as choix
from data.modules.menu.choix_map import main as choix2


def suivant1(tabinfo):
    """
    Fonction qui permet de lancer le menu de choix des personnages.
    """
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
    return None


def suivant2(tabinfo):
    """
    Fonction qui permet de lancer le menu de choix de maps.
    """
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
    """
    Fonction qui permet de lancer le menu principal.
    """
    if tabinfo[0] == "":
        suiv = "feur"

        while suiv != "stop":
            suiv = starting()
            print(suiv)

            if suiv == "choix_perso":
                return suivant1(tabinfo)

            if suiv == "quitter":
                quit()
    return None


def debut():
    """
    Fonction qui renvoie les informations des persos et de la map choisis.
    """
    tabinfo = ["", "", ""]
    manager(tabinfo)
    return tabinfo[0], [tabinfo[1], tabinfo[2]]
