import mysql.connector
from dotenv import load_dotenv
import os
 
load_dotenv()
 
 
def inserer_commande():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("BDD_HOST"),
            port=os.getenv("BDD_PORT"),
            user=os.getenv("BDD_USER"),
            password=os.getenv("BDD_PASSWORD"),
            database=os.getenv("BDD_NAME"),
        )
        cursor = conn.cursor()
 
sql = """
        START TRANSACTION ;
 
INSERT INTO commande (numero_commande, commande_date, revendeur_id) VALUES (dataFile[« numero_commande »],dataFile[« commande_date »], dataFile[« revendeur_id »]) ;
"""
 
        conn.commit()  # valide l'insertion
 
        cursor.close()
        conn.close()