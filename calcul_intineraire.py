import json
import requests
import os
import sys
from dateutil import parser
import psycopg2


#Connection à la BDD
bdd = psycopg2.connect(
    database="vacances",
    user="masterUsername",
    password="SqualeApollo7",
    host="rds-postgresql-vacances.cvr2tfzdfp0j.eu-west-3.rds.amazonaws.com",
    port='5432')
cur = bdd.cursor()


#Initialisation des variables
liste_villes = []
liste_villes2 = []
ville_depart = ('Paris 01',)
insee_dep = 75056
heure_depart = "20200901T080000"
emis_co2_total = 0
duree_totale = 0


#Definition des token pour l'API SNCF
token = '72b6ca17-c5b4-4982-8d7f-b47ee343b471'
token2 = 'd9a679d2-5aa3-4278-b77b-e67854bc419c'
token3 = '6c87ae0f-6346-48b5-9313-585d3520c7b8'
token4 = '10d0fc92-fa71-4883-a8fc-e2fa0a39b7b9'
token5 = '70befc1f-299e-4886-b156-81418804cc31'
token6 = '1918bf7e-ecd5-4381-bc4d-56ad9bb8d2ad'
token7 = 'eec29c47-70d0-4c54-9e8c-578883c3c8af'
token8 = 'f1feeea7-4362-42f5-bb26-610bc441a6bf'


cur.execute("""SELECT name FROM ville WHERE prefecture = '1';""")
villes = cur.fetchall()
#Creation des listes contenant les noms de toutes les prefectures
for ville in villes :
    liste_villes.append(ville)
    liste_villes2.append(ville)


#Retrait de la ville de départ
liste_villes.remove(ville_depart)
liste_villes2.remove(ville_depart)


#Effacement des precedents itineraires
cur.execute("""INSERT INTO total VALUES(1, 0, 0) ON CONFLICT (id) DO UPDATE SET cumul_co2 = 0, cumul_duree = 0;""")
cur.execute("""INSERT INTO total VALUES(2, 0, 0) ON CONFLICT (id) DO UPDATE SET cumul_co2 = 0, cumul_duree = 0;""")
cur.execute("""DELETE FROM trajet_ville;""")
cur.execute("""DELETE FROM total_trajet;""")
bdd.commit()

cur.execute("""DELETE FROM trajet;""")
bdd.commit()

i = 0
j = 0
#Fonction pour trouver le trajet le plus rapide
while liste_villes != [] :
    
    for ville in liste_villes :
        i = i + 1
        cur.execute("""SELECT insee FROM ville WHERE name = %s ;""", ville)
        insee_arr = str(cur.fetchone())
        insee_arr = insee_arr[1:-2]

        #Requete vers l'API SNCF pour retourner le trajet entre la ville actuelle et la prochaine ville (insee_arr)
        r = requests.get(f'https://api.sncf.com/v1/coverage/sncf/journeys?from=admin%3Afr%3A{insee_dep}&to=admin%3Afr%3A{insee_arr}&datetime={heure_depart}&', auth=(token5, '')).json()
        
        if "error" not in r.keys() :
            if "journeys" in r.keys() :
                #Extraction des donnees du JSON renvoye par l'API SNCF + envoi en BDD dans la table brouillon
                co2 = r["journeys"][0]["co2_emission"]["value"]
                heure_arrivee = r["journeys"][0]["arrival_date_time"]
                date_arr = parser.isoparse(heure_arrivee)
                date_dep = parser.isoparse(heure_depart)
                date_arr = int(round(date_arr.timestamp()))
                date_dep = int(round(date_dep.timestamp()))
                temps_arr = (date_arr - date_dep)/3600
                data = [insee_dep, insee_arr, heure_arrivee, co2, temps_arr]
                cur.execute("""INSERT INTO brouillon (inseedepart, inseearrivee, date_arr, emis_co2, duree) VALUES (%s, %s, %s, %s, %s);""", data)
            
    bdd.commit()
    #Recuperation du meilleur trajet dans la table brouillon
    cur.execute("""SELECT inseedepart, inseearrivee, date_arr, emis_co2, duree FROM brouillon WHERE duree = (SELECT MIN(duree) FROM brouillon);""")
    best_result = cur.fetchone()
    try :
        ancien_insee =  best_result[0]
        insee_dep = best_result[1]
        heure_depart = best_result[2]
        emis_co2 = best_result[3]
        duree = best_result[4]
        emis_co2_total = emis_co2_total + emis_co2
        duree_totale = duree_totale + duree
        data_trajet = [ancien_insee, insee_dep, emis_co2, duree]

        #Insertion du resultat dans la table trajet + vidage de la table brouillon
        cur.execute("""INSERT INTO trajet (inseedepart, inseearrivee, emis_co2, duree) VALUES (%s, %s, %s, %s);""", data_trajet)
        cur.execute("""DELETE FROM brouillon;""")
    except TypeError as error :
        print(error)

    if i % 3700 == 0 :
        token5 = token2


    bdd.commit()
    j = j + 1
    print(f"Etape n°{j} OK")
    #Suppression de la ville d'arrivee de la liste des villes restantes
    cur.execute("""SELECT name FROM ville WHERE insee = %s ;""", (insee_dep,))
    ville = cur.fetchone()

    try :
        liste_villes.remove(ville)
    except :
        villes_restantes = liste_villes
        liste_villes = []
    
    #Mise a jour de la table trajet_ville
    insee = [insee_dep]
    cur.execute("""SELECT id FROM trajet WHERE inseearrivee = %s;""", insee)
    d1 = cur.fetchone()
    cur.execute("""SELECT id FROM ville WHERE insee = %s;""", insee)
    d2 = cur.fetchone()
    data = [d1, d2]
    cur.execute("""INSERT INTO trajet_ville(id_trajet, id_ville) VALUES(%s, %s);""", data)

    #Mise a jour de la table trajet_total
    cur.execute("""SELECT id FROM trajet WHERE inseearrivee = %s;""", insee)
    d = cur.fetchone()
    cur.execute("""INSERT INTO total_trajet(id_trajet, id_total) VALUES(%s, 1);""", d)

lduree_totale = [duree_totale]
lemis_co2_total = [emis_co2_total]
cur.execute("""UPDATE total SET cumul_duree = %s WHERE id = 1;""", lduree_totale)
cur.execute("""UPDATE total SET cumul_co2 = %s WHERE id = 1;""", lemis_co2_total)
bdd.commit()

#Reinitialisation des variables    
insee_dep = 75056
heure_depart = "20200901T080000"
j = 0
i = 0
emis_co2_total = 0
duree_totale = 0


#Fonction pour trouver le trajet rejettant le moins de CO2    
while liste_villes2 != [] :
    
    for ville in liste_villes2 :
        i = i + 1
        cur.execute("""SELECT insee FROM ville WHERE name = %s ;""", ville)
        insee_arr = str(cur.fetchone())
        insee_arr = insee_arr[1:-2]

        #Requete vers l'API SNCF pour retourner le trajet entre la ville actuelle et la prochaine ville (insee_arr)
        r = requests.get(f'https://api.sncf.com/v1/coverage/sncf/journeys?from=admin%3Afr%3A{insee_dep}&to=admin%3Afr%3A{insee_arr}&datetime={heure_depart}&', auth=(token3, '')).json()
        
        if "error" not in r.keys() :
            if "journeys" in r.keys() :
                #Extraction des donnees du JSON renvoye par l'API SNCF + envoi en BDD dans la table brouillon
                co2 = r["journeys"][0]["co2_emission"]["value"]
                heure_arrivee = r["journeys"][0]["arrival_date_time"]
                date_arr = parser.isoparse(heure_arrivee)
                date_dep = parser.isoparse(heure_depart)
                date_arr = int(round(date_arr.timestamp()))
                date_dep = int(round(date_dep.timestamp()))
                temps_arr = (date_arr - date_dep)/3600
                data = [insee_dep, insee_arr, heure_arrivee, co2, temps_arr]
                cur.execute("""INSERT INTO brouillon (inseedepart, inseearrivee, date_arr, emis_co2, duree) VALUES (%s, %s, %s, %s, %s);""", data)
                
    bdd.commit()
    j = j + 1
    print(f"Etape n°{j} OK")
    if i % 4500 == 0 :
        token4 = token8
    #Recuperation du meilleur trajet dans la table brouillon
    cur.execute("""SELECT inseedepart, inseearrivee, date_arr, emis_co2, duree FROM brouillon WHERE emis_co2 = (SELECT MIN(emis_co2) FROM brouillon);""")
    try : 
        best_result = cur.fetchone()
        ancien_insee =  best_result[0]
        insee_dep = best_result[1]
        heure_depart = best_result[2]
        emis_co2 = best_result[3]
        duree = best_result[4]
        emis_co2_total = emis_co2_total + emis_co2
        duree_totale = duree_totale + duree
        data_trajet = [ancien_insee, insee_dep, emis_co2, duree]

        #Insertion du resultat dans la table trajet + vidage de la table brouillon
        cur.execute("""INSERT INTO trajet (inseedepart, inseearrivee, emis_co2, duree) VALUES (%s, %s, %s, %s);""", data_trajet)
        cur.execute("""DELETE FROM brouillon;""")
        bdd.commit()
    except TypeError as Error : 
        print(Error)


    #Mise a jour de la table trajet_ville
    insee = [insee_dep]
    cur.execute("""SELECT id FROM trajet WHERE inseearrivee = %s;""", insee)
    d1 = cur.fetchone()
    cur.execute("""SELECT id FROM ville WHERE insee = %s;""", insee)
    d2 = cur.fetchone()
    data = [d1, d2]
    cur.execute("""INSERT INTO trajet_ville(id_trajet, id_ville) VALUES(%s, %s);""", data)

    #Mise a jour de la table trajet_total
    cur.execute("""SELECT id FROM trajet WHERE inseearrivee = %s;""", insee)
    d = cur.fetchone()
    cur.execute("""INSERT INTO total_trajet(id_trajet, id_total) VALUES(%s, 2);""", d)


    #Suppression de la ville d'arrivee de la liste des villes restantes
    cur.execute("""SELECT name FROM ville WHERE insee = %s ;""", (insee_dep,))
    ville = cur.fetchone()


    try :
        liste_villes2.remove(ville)
    except :
        villes_restantes2 = liste_villes2
        liste_villes2 = []

lduree_totale = [duree_totale]
lemis_co2_total = [emis_co2_total]
cur.execute("""UPDATE total SET cumul_duree = %s WHERE id = 2;""", lduree_totale)
cur.execute("""UPDATE total SET cumul_co2 = %s WHERE id = 2;""", lemis_co2_total)
bdd.commit()


bdd.close()