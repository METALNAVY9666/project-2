"""permet de lire des options"""
import json


def read_settings():
    """lis le fichier options"""
    with open("data/settings.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        file.close()
    return data

def read_levels():
    """lis les niveaux"""
    with open("data/gfx/levels/levels.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        file.close()
    return data