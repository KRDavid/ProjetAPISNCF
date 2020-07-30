import csv
import os
import sys
import psycopg2


#Connection à la BDD
bdd = psycopg2.connect(
    database="vacances",
    user="masterUsername",
    password="SqualeApollo7",
    host="rds-postgresql-vacances.cvr2tfzdfp0j.eu-west-3.rds.amazonaws.com",
    port='5432')
cur = bdd.cursor()


fichier = "ensemble_comm.csv"
base_dir = os.path.dirname(sys.argv[0])
path = os.path.join(base_dir, fichier)


i = 0
cur.execute("""DELETE FROM ville;""")
bdd.commit()

#Lecture du csv puis insertion en BDD
with open (path) as file :
    dic = csv.DictReader(file)
    for row in dic :
        insee = row["insee"]
        nom_com = row["nom_commune"]
        zip_code = row["zip_code"]
        lat = row["latitude"]
        longi = row["longitude"]
        data = [nom_com, longi, lat, insee, zip_code]
        try :
            cur.execute("""INSERT INTO ville(name, longitude, latitude, insee, zip_code) VALUES(%s, %s, %s, %s, %s);""", data)
        except :
            pass
        if i % 2000 == 0:
            print(f"Ligne n°{i}")
            bdd.commit()
        i = i + 1
bdd.commit()

bdd.close()