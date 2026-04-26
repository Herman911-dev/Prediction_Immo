import csv
import io
import logging
import os
import time

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine


# Configuration du Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Chargement des variables d'environnement
load_dotenv()
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
CSV_PATH = "data/cleaned/dvf_idf_cleaned.csv"
TABLE_NAME = "transactions"

# FONCTIONS MÉTIER

def psql_insert_copy(table, conn, keys, data_iter):
    """
    Exécute une insertion SQL en masse en utilisant la commande native COPY de PostgreSQL.
    
    Cette méthode utilise le module standard 'csv' de Python pour formater les données,
    assurant une compatibilité totale avec les versions récentes de Pandas (2.0+).
    """
    # Extraction de la connexion bas-niveau (psycopg2) depuis SQLAlchemy
    dbapi_conn = conn.connection
    with dbapi_conn.cursor() as cur:
        # Création d'un buffer en mémoire (fichier temporaire virtuel)
        s_buf = io.StringIO()
        
        # Formatage des données vers le buffer via le module csv standard
        writer = csv.writer(s_buf)
        writer.writerows(data_iter)
        s_buf.seek(0)
        
        # Construction dynamique de la requête SQL "COPY"
        columns = ', '.join(f'"{k}"' for k in keys)
        table_name = f'{table.schema}.{table.name}' if table.schema else table.name
        sql = f'COPY {table_name} ({columns}) FROM STDIN WITH CSV'
        
        # Exécution de la copie
        cur.copy_expert(sql=sql, file=s_buf)

def main():
    """Point d'entrée principal du pipeline d'ingestion PostgreSQL."""
    start_time = time.time()
    logging.info("Démarrage du processus d'ingestion massive...")

    try:
        # Connexion au moteur PostgreSQL
        db_uri = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        engine = create_engine(db_uri)
        
        # Chargement du jeu de données nettoyé
        logging.info(f"Lecture du fichier source : {CSV_PATH}")
        df = pd.read_csv(CSV_PATH)
        
        # Injection dans la base de données
        logging.info(f"Injection de {len(df):,} lignes dans la table '{TABLE_NAME}'...")
        
        # Standardisation (snake_case) imposée par les bonnes pratiques SQL
        logging.info("Standardisation des noms de colonnes (snake_case)...")
        df.columns = [col.lower().replace(' ', '_') for col in df.columns]
        
        # Injection par lots (chunksize) pour éviter la saturation de la RAM (MemoryError)
        df.to_sql(
            name=TABLE_NAME, 
            con=engine, 
            if_exists='replace', 
            index=False, 
            method=psql_insert_copy,
            chunksize=100000 
        )
        
        elapsed_time = time.time() - start_time
        logging.info(f"SUCCÈS : Données ingérées avec succès en {elapsed_time:.2f} secondes.")
        
    except FileNotFoundError:
        logging.error(f"ÉCHEC : Le fichier {CSV_PATH} est introuvable. Vérifiez votre chemin d'accès.")
    except Exception as e:
        logging.error(f"ÉCHEC : Une erreur critique est survenue lors de l'ingestion : {e}")

if __name__ == "__main__":
    main()