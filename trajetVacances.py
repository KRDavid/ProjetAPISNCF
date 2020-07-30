import folium
from numpy import random
import psycopg2
import pandas as pd

try:
    connexion = psycopg2.connect(
        database="vacances",
        user="masterUsername",
        password="SqualeApollo7",
        host="rds-postgresql-vacances.cvr2tfzdfp0j.eu-west-3.rds.amazonaws.com",
        port='5432'
    )

    #create_tables()

    curseur = connexion.cursor()

    # Création des tables une à une
    curseur.execute("""SELECT total_trajet.id_total, trajet.inseedepart, trajet.inseearrivee, trajet.emis_co2, trajet.duree, ville.longitude, ville.latitude
                    FROM trajet, total_trajet, trajet_ville, ville
                    WHERE trajet.id = total_trajet.id_trajet
                    AND	trajet.id = trajet_ville.id_trajet
                    AND	ville.id = trajet_ville.id_ville
                    ORDER BY ville.longitude, ville.latitude;""")

    rtRq5 = curseur.fetchall()
    
    # Afficher le résultat
    print("\nRésultat: \n")
    for ligne in rtRq5:
        print(ligne[0], " | ", ligne[1])

    # fin de connexion avec PostgreSQL
    curseur.close()
    # commiter les modifications
    connexion.commit()

except (Exception, psycopg2.DatabaseError) as error:
    print(error)
finally:
    if connexion is not None:
        connexion.close()

data = pd.DataFrame(rtRq5) # Convertit le résultat de la requete en DataFrame

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
my_map.save("./trajetVacances.html")