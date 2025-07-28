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
def insert_commande_product(log_id, comm):
    """Ajout d'une commande dans la base MySQL, avec relations
    Args:
        log_id (int): id de référence du fichier commande en archive logs
        comm(dict): les données de commande à insérer
    Returns:
        _(boolean): succès/échec de l'insertion en BDD
    """
    try:
        conn = init_connection()
        cursor = conn.cursor()

        insert_commande = """
            INSERT INTO commande (log_id,numero_commande, commande_date, revendeur_id)
            VALUES (%s,%s, %s, %s)
        """
        cursor.execute(
            insert_commande,
            (
                log_id,
                comm["numero_commande"],
                comm["commande_date"],
                comm["revendeur_id"],
            ),
        )

        commande_id = cursor.lastrowid
        insert_commande_produit = """
            INSERT INTO commande_produit (commande_id, product_id, quantity)
            VALUES (%s, %s, %s)
        """
        cursor.execute(
            insert_commande_produit, (commande_id, comm["product_id"], comm["quantity"])
        )
        conn.commit()
        cursor.close()
        conn.close()

        return True

    except mysql.connector.Error as err:
        print(f"❌ Erreur de connexion ou de requête MySQL : {err}")
        return False


###############################################################################
def insert_production_product(log_id, prod):
    """Ajout d'une production dans la base MySQL, avec relations
    Args:
        log_id (int): id de référence du fichier commande en archive logs
        prod(dict): les données de production à insérer
    Returns:
        _(boolean): succès/échec de l'insertion en BDD
    """
    try:
        conn = init_connection()
        cursor = conn.cursor()

        insert_production = """
            INSERT INTO production (log_id,production_ref, date_production)
            VALUES (%s,%s, %s)
        """
        cursor.execute(
            insert_production, (log_id, prod["production_id"], prod["date_production"])
        )

        prod_id = cursor.lastrowid

        insert_production_produit = """
            INSERT INTO production_produit (production_id, product_id, quantity)
            VALUES (%s, %s, %s)
        """
        cursor.execute(
            insert_production_produit, (prod_id, prod["product_id"], prod["quantity"])
        )

        conn.commit()
        return True

    except mysql.connector.Error as err:
        print(f"❌ Erreur MySQL lors de l'insertion de production : {err}")
        return False

    finally:
        if "cursor" in locals():
            cursor.close()
        if "conn" in locals():
            conn.close()


###############################################################################
def update_stock_produit(stock, plus_minus):
    """Ajout du stock dans la base MySQL, avec relations
    Args:
        stock(dict): les données de stock à insérer
        plus_minus(int): un facteur (-1 ou 1) pour le retrait ou l'ajout de quantité
    Returns:
        _(boolean): succès/échec de l'insertion en BDD
    """
    try:
        conn = init_connection()
        cursor = conn.cursor()

        get_last_stock = """SELECT quantity FROM stock WHERE product_id=%s
            ORDER BY stock_date DESC LIMIT 1;
        """
        cursor.execute(get_last_stock, (stock["product_id"],))
        result = cursor.fetchone()
        last_quantity = result[0] if result else 0
        new_stock = last_quantity + plus_minus * stock["movement"]
        insert_stock = """INSERT INTO stock (stock_date,product_id,movement,quantity,operator_id)
        VALUES (%s,%s,%s,%s,%s)
        """
        stock_values = (
            stock["stock_date"],
            stock["product_id"],
            stock["movement"],
            new_stock,
            stock["operator_id"],
        )
        cursor.execute(insert_stock, stock_values)
        conn.commit()
        cursor.close()
        conn.close()

        return True

    except mysql.connector.Error as err:
        print(f"❌ Erreur de connexion ou de requête MySQL : {err}")
        return False


###############################################################################
def load_commande_produit(name, data_df):
    """Préparation des requêtes de stockage des données commandes dans la BDD
    Args:
        name (lst): name[1] est l'id du ficher dans la table log
        data_df (dataframe): données nettoyées à stocker en BDD
    """
    for index, row in data_df.iterrows():
        comm = row.to_dict()
        stock_dict = {
            "stock_date": comm["commande_date"],
            "product_id": comm["product_id"],
            "movement": comm["quantity"],
            "operator_id": comm["revendeur_id"],
        }
        success = insert_commande_product(name[1], comm)

        if success:
            update_stock_produit(stock_dict, -1)
            print(f"✅ Ligne {index + 2} : commande insérée")


###############################################################################
def load_production_produit(name, data_df):
    """Préparation des requêtes de stockage des données production dans la BDD
    Args:
        name (lst): name[1] est l'id du ficher dans la table log
        data_df (dataframe): données nettoyées à stocker en BDD
    """
    for index, row in data_df.iterrows():
        prod = row.to_dict()
        stock_dict = {
            "stock_date": prod["date_production"],
            "product_id": prod["product_id"],
            "movement": prod["quantity"],
            "operator_id": None,
        }
        success = insert_production_product(name[1], prod)

        if success:
            update_stock_produit(stock_dict, 1)
            print(f"✅ Ligne {index + 2} : production insérée")
