import requests
import json
import os
import sys
import psycopg2



#Initialisation des variables
i = 0
code_insee_reg = []
code_insee_depar = []
num_dep_reg = []
num_dep = []
longitude = []
latitude = []


#Connection à la BDD
bdd = psycopg2.connect(
    database="vacances",
    user="masterUsername",
    password="SqualeApollo7",
    host="rds-postgresql-vacances.cvr2tfzdfp0j.eu-west-3.rds.amazonaws.com",
    port='5432')
cur = bdd.cursor()


#Mise a jour des codes insee
cur.execute("""UPDATE ville SET insee = 75056 WHERE name = 'Paris 01';""")
cur.execute("""UPDATE ville SET insee = 69123 WHERE name = 'Lyon 01';""")
cur.execute("""UPDATE ville SET insee = 13055 WHERE name = 'Marseille 01';""")
cur.execute("""UPDATE ville SET insee = 93010 WHERE name = 'Bobigny';""")
cur.execute("""UPDATE ville SET insee = 7181 WHERE name = 'Privas';""")
cur.execute("""UPDATE ville SET insee = 4049 WHERE name = 'Digne-les-Bains';""")
print("Update OK")
bdd.commit()


#Recuperation des JSON contennant les donnees des prefectures de region et de departement
prefecregion = requests.get('https://data.opendatasoft.com/api/records/1.0/search/?dataset=correspondance-code-insee-code-postal%40public&rows=100&facet=insee_com&facet=nom_dept&facet=nom_region&facet=statut&refine.statut=Pr%C3%A9fecture+de+r%C3%A9gion').json()
prefecdepar = requests.get('https://data.opendatasoft.com/api/records/1.0/search/?dataset=correspondance-code-insee-code-postal%40public&rows=100&facet=insee_com&facet=nom_dept&facet=nom_region&facet=statut&refine.statut=Pr%C3%A9fecture').json()
prefeccap = requests.get('https://data.opendatasoft.com/api/records/1.0/search/?dataset=correspondance-code-insee-code-postal%40public&facet=insee_com&facet=nom_dept&facet=nom_region&facet=statut&refine.statut=Capitale+d%27%C3%A9tat').json()

i = 0
#Recuperation des donnees utiles dans le JSON des prefectures de region
while i < len(prefecregion["records"]) :
    code_insee = prefecregion["records"][i]["fields"]["insee_com"]
    nom_comm = prefecregion["records"][i]["fields"]["nom_comm"]
    if code_insee == '69381' :
        code_insee = '69123'
    if code_insee == '13201' :
        code_insee = '13055'
    code = [code_insee]
    if nom_comm != "AJACCIO" :
            cur.execute("""UPDATE ville SET prefecture = '1' WHERE insee = %s;""", code)

    i = i + 1
bdd.commit()
    
    
i = 0
#Recuperation des donnees utiles dans le JSON des prefectures de departement
while i < len(prefecdepar["records"]) :
    code_insee = prefecdepar["records"][i]["fields"]["insee_com"]
    if code_insee == '93008' :
        code_insee = '93010'
    if code_insee == '4070' :
        code_insee = '4049'
    if code_insee == '7186' :
        code_insee = '7181'
    code = [code_insee]
    if code_insee != '2B033' :
        cur.execute("""UPDATE ville SET prefecture = '1' WHERE insee = %s;""", code)
    i = i + 1
bdd.commit()


code_insee = prefeccap["records"][0]["fields"]["insee_com"]
if code_insee == '75101' :
    code_insee = '75056'
code = [code_insee]
cur.execute("""UPDATE ville SET prefecture = '1' WHERE insee = %s;""", code)
bdd.commit()


bdd.close()


