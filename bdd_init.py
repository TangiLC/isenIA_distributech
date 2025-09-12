from scripts.utils.requetes_sql import init_bdd

# COMMANDE_PATH="data/commande_revendeur_tech_express.csv"
# COMMANDE_PATH = "data/commande_avec_erreurs.csv"
# SQLITE_PATH = "data/base_stock.sqlite"
DATA_PATH = "./data/"
BDD_SCRIPT_INIT = "./bdd/script_create.sql"
BDD_SCRIPT_POPULATE = "./bdd/script_populate.sql"


def init_and_populate():

    for script_path, description in [
        (BDD_SCRIPT_INIT, "création tables MySQL"),
        (BDD_SCRIPT_POPULATE, "population initiale"),
    ]:
        print(f"🔄 {description}...")
        if not init_bdd(script_path):
            print(f"❌ Échec : {description}")
            return False
        print(f"✅ {description} réussie")


init_and_populate()
