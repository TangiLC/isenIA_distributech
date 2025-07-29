import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()


def init_connection():
    """Initialisation de la connection mysql-connector
    Returns:
        connector.connect: le connecteur actif
    """
    return mysql.connector.connect(
        host=os.getenv("BDD_HOST"),
        port=os.getenv("BDD_PORT"),
        user=os.getenv("BDD_USER"),
        password=os.getenv("BDD_PASSWORD"),
        database=os.getenv("BDD_NAME"),
    )


###############################################################################
def insert_into_bddlogs(path, table):
    """Ajout d'une entrée dans la table log (commande ou production)
    Args:
        path (str): le chemin du fichier csv archivé
        table(str): nom de la table de la BDD (log_commande_brut ou log_production_brut)
    Returns:
        _(boolean): succès/échec de l'insertion en BDD
    """
    try:
        conn = init_connection()
        cursor = conn.cursor()

        requete = f"""
            INSERT INTO `{table}` (log_date, nom_fichier)
            VALUES (NOW(), %s)
        """
        cursor.execute(requete, (path,))
        log_id = cursor.lastrowid

        conn.commit()
        cursor.close()
        conn.close()

        return log_id

    except mysql.connector.Error as err:
        print(f"❌ Erreur lors de l'insertion du log : {err}")
        return None


###############################################################################
def get_revendeur_region():
    """Requête pour créeer un dictionnaire de relations revendeur/region
    Returns:
        revendeur_region_map(dict): dictionnaire des relations
    """
    try:
        conn = init_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT revendeur_id, region_id FROM revendeur")

        # Construction du dictionnaire {revendeur_id: region_id}
        revendeur_region_map = {}
        for revendeur_id, region_id in cursor.fetchall():
            revendeur_region_map[revendeur_id] = region_id

        cursor.close()
        conn.close()

        return revendeur_region_map

    except mysql.connector.Error as err:
        print(f"❌ Erreur de connexion ou de requête MySQL : {err}")
        return {}


##############################################################################
def get_product_unit_prices():
    """Requête pour créeer un dictionnaire de relations produit/cout_unitaire
    Returns:
        product_price_map(dict): dictionnaire des relations
    """
    try:
        conn = init_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT product_id, cout_unitaire FROM produit")

        product_price_map = {}
        for product_id, cout_unitaire in cursor.fetchall():
            product_price_map[product_id] = float(cout_unitaire)

        cursor.close()
        conn.close()

        return product_price_map

    except mysql.connector.Error as err:
        print(f"❌ Erreur de connexion ou de requête MySQL : {err}")
        return {}


##############################################################################
def check_commande_already_exists(num_c, prod_id):
    """Vérification de l'existance d'un couple numéro de commande/produit_id
    Args:
        num_c(str): numero de commande à vérifier
        prod_id(int): id du produit
    Returns:
        _(boolean): Existance/Absence du couple
    """
    try:
        conn = init_connection()
        cursor = conn.cursor()
        query_commande = """
            SELECT commande_id FROM commande WHERE numero_commande = %s
        """
        cursor.execute(query_commande, (num_c,))
        results = cursor.fetchall()

        if results is None:
            return False

        query_liaison = """
            SELECT 1 FROM commande_produit WHERE commande_id = %s AND product_id = %s LIMIT 1
        """
        for (commande_id,) in results:
            cursor.execute(query_liaison, (commande_id, prod_id))
            if cursor.fetchone() is not None:
                cursor.close()
                conn.close()
                return True
        cursor.close()
        conn.close()
        return False

    except mysql.connector.Error as err:
        print(f"❌ Erreur MySQL : {err}")
        return False


###############################################################################
def check_production_already_exists(prodn_ref, prodt_id, prodn_date):
    """Vérification de l'existance d'un triplet production_ref/product_id/production_date
    Args:
        prodn_ref(int): reférence de la production
        prodt_id(int): id du produit
        prodn_date(str): date de production

    Returns:
        _(boolean): Existance/Absence du triplet
    """
    try:
        conn = init_connection()
        cursor = conn.cursor()

        query_production = """
            SELECT production_id FROM production WHERE production_ref = %s AND date_production = %s
        """
        cursor.execute(query_production, (prodn_ref, prodn_date))
        results = cursor.fetchall()

        if results is None:
            return False

        query_liaison = """
            SELECT 1 FROM production_produit WHERE production_id = %s AND product_id = %s LIMIT 1
        """
        for (production_id,) in results:
            cursor.execute(query_liaison, (production_id, prodt_id))
            if cursor.fetchone() is not None:
                cursor.close()
                conn.close()
                return True

        cursor.close()
        conn.close()
        return False

    except mysql.connector.Error as err:
        print(f"❌ Erreur MySQL : {err}")
        return False
