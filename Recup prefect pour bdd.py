import requests
import json
import os
import pandas as pd
import keyring
import pprint
import sys
import matplotlib
import numpy as np


#Initialisation des variables
i = 0
code_insee_reg = []
code_insee_depar = []
num_dep_reg = []
num_dep = []




#Definition du token pour l'API SNCF
token = '72b6ca17-c5b4-4982-8d7f-b47ee343b471'


#Definition de la fonction permettant de recuperer les donnees utiles des JSON et de les envoyer en base de donnees
def recup_villes() :

    #Recuperation des JSON contennant les donnees des prefectures de region et de departement
    prefecregion = requests.get('https://data.opendatasoft.com/api/records/1.0/search/?dataset=correspondance-code-insee-code-postal%40public&rows=100&facet=insee_com&facet=nom_dept&facet=nom_region&facet=statut&refine.statut=Pr%C3%A9fecture+de+r%C3%A9gion').json()
    prefecdepar = requests.get('https://data.opendatasoft.com/api/records/1.0/search/?dataset=correspondance-code-insee-code-postal%40public&rows=100&facet=insee_com&facet=nom_dept&facet=nom_region&facet=statut&refine.statut=Pr%C3%A9fecture').json()


    i = 0

    #Recuperation des donnees utiles dans le JSON des prefectures de region
    while i < len(prefecregion["records"]) :
        print("Extraction ligne {} du prefecregion.json".format(i))
        code_insee_reg = prefecregion["records"][i]["fields"]["insee_com"]
        num_dep_reg = prefecregion["records"][i]["fields"]["code_reg"]
        nom_dep_reg = prefecregion["records"][i]["fields"]["nom_comm"]
        i = i + 1

    i = 0

    #Recuperation des donnees utiles dans le JSON des prefectures de departement
    while i < len(prefecdepar["records"]) :
        print("Extraction ligne {} du prefecdepar.json".format(i))
        code_insee_depar = prefecdepar["records"][i]["fields"]["insee_com"]
        num_dep = prefecdepar["records"][i]["fields"]["code_reg"]
        nom_dep = prefecdepar["records"][i]["fields"]["com_comm"]
        i = i + 1
    

print(code_insee_reg)