import folium
from numpy import random
import psycopg2
import pandas as pd
import os
import sys

connexion = psycopg2.connect(
        database="vacances",
        user="masterUsername",
        password="SqualeApollo7",
        host="rds-postgresql-vacances.cvr2tfzdfp0j.eu-west-3.rds.amazonaws.com",
        port='5432')

    #create_tables()

cur = connexion.cursor()

base_dir = os.path.dirname(sys.argv[0])

path = os.path.join(base_dir, "trajetVacancesduree.html")
path2 = os.path.join(base_dir, "trajetVacancesco2.html")

cur.execute("""SELECT ville.latitude, ville.longitude
                    FROM trajet, total_trajet, trajet_ville, ville
                    WHERE trajet.id = total_trajet.id_trajet
                    AND    trajet.id = trajet_ville.id_trajet
                    AND    ville.id = trajet_ville.id_ville
                    and total_trajet.id_total = '1'
                    ORDER BY ville.longitude, ville.latitude;""")

rqduree = cur.fetchall()


data = pd.DataFrame(rqduree) # Convertit le résultat de la requete en DataFrame

# On convertit le DataFrame en martices
matrice = data.to_numpy()

# Load map centred on average coordinates
ave_lat = sum(p[0] for p in matrice)/len(matrice)
ave_lon = sum(p[1] for p in matrice)/len(matrice)
my_map = folium.Map(location=[ave_lat, ave_lon], zoom_start=6)

#add a markers 'a'
for each in matrice:  
    my_map.add_child(folium.CircleMarker(location=each,
    fill='true',
    radius = 6,
    popup= 'Hi',
    fill_color='blue',
    color = 'clear',
    fill_opacity=1))
    
# add lines
folium.PolyLine(matrice, color="green", weight=2.5, opacity=1).add_to(my_map)
 
# Save map
my_map.save(path)



# Création des tables une à une
cur.execute("""SELECT ville.latitude, ville.longitude
                    FROM trajet, total_trajet, trajet_ville, ville
                    WHERE trajet.id = total_trajet.id_trajet
                    AND    trajet.id = trajet_ville.id_trajet
                    AND    ville.id = trajet_ville.id_ville
                    and total_trajet.id_total = '2'
                    ORDER BY ville.longitude, ville.latitude;""")

rqco2 = cur.fetchall()


data = pd.DataFrame(rqco2) # Convertit le résultat de la requete en DataFrame

# On convertit le DataFrame en martices
matrice = data.to_numpy()

# Load map centred on average coordinates
ave_lat = sum(p[0] for p in matrice)/len(matrice)
ave_lon = sum(p[1] for p in matrice)/len(matrice)
my_map = folium.Map(location=[ave_lat, ave_lon], zoom_start=6)

#add a markers 'a'
for each in matrice:  
    my_map.add_child(folium.CircleMarker(location=each,
    fill='true',
    radius = 6,
    popup= 'Hi',
    fill_color='blue',
    color = 'clear',
    fill_opacity=1))

# add title
loc = 'Affichage du parcours'
title_html = '''
             <h3 align="center" style="font-size:16px"><b>{}</b></h3>
             '''.format(loc)   

my_map.get_root().html.add_child(folium.Element(title_html))
    
# add lines
folium.PolyLine(matrice, color="green", weight=2.5, opacity=1).add_to(my_map)
 
# Save map
my_map.save(path2)