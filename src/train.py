# A lancer que la 1er fois, et à relancer quand vous mettez votre Base de Données à Jour
# L'entraînement prend beaucoup de temps !

import os
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, VotingRegressor
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import joblib
import logging
import time
from pathlib import Path

# Configuration du logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    start_time = time.time()
    logger.info("Début de la phase d'entraînement (MLOps)...")

    # Chemins
    base_path   = Path(__file__).parent.parent
    models_path = base_path / "models"
    os.makedirs(models_path, exist_ok=True)

    try:
        # Connexion PostgreSQL (Docker)
        load_dotenv()
        DB_USER = os.getenv("DB_USER")
        DB_PASS = os.getenv("DB_PASSWORD")
        DB_HOST = os.getenv("DB_HOST")
        DB_PORT = os.getenv("DB_PORT")
        DB_NAME = os.getenv("DB_NAME")

        db_uri = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        engine = create_engine(db_uri)
        logger.info(f"Connexion à PostgreSQL ({DB_HOST}:{DB_PORT}/{DB_NAME})...")

        # Extraction depuis la BDD
        query = text("""
            SELECT
                date_mutation,
                valeur_fonciere,
                code_postal,
                surface_reelle_bati,
                nombre_pieces_principales AS nb_pieces,
                surface_terrain,
                type_local
            FROM transactions
            WHERE surface_reelle_bati > 0
              AND valeur_fonciere BETWEEN 10000 AND 2000000
              AND type_local IN ('Appartement', 'Maison')
        """)

        logger.info("Extraction des données depuis PostgreSQL...")
        df = pd.read_sql(query, engine)
        logger.info(f"{len(df):,} transactions récupérées.")

        # Feature Engineering
        logger.info("Création des variables (Feature Engineering)...")

        # Dimension temporelle
        df['date_mutation'] = pd.to_datetime(df['date_mutation'])
        df['annee'] = df['date_mutation'].dt.year
        df['mois']  = df['date_mutation'].dt.month

        # Ratio de standing
        df['surface_par_piece'] = df['surface_reelle_bati'] / df['nb_pieces'].replace(0, 1)


        # Target Encoding : prix moyen par code postal (aligné sur le notebook)
        logger.info("Calcul de la mémoire géographique (Target Encoding)...")
        postal_means       = df.groupby('code_postal')['valeur_fonciere'].mean()
        df['postal_score'] = df['code_postal'].map(postal_means)

        # Biais parisien
        df['est_paris'] = df['code_postal'].astype(str).str.startswith('75').astype(int)

        # Nettoyage
        df['surface_terrain'] = df['surface_terrain'].fillna(0)

        # One-Hot Encoding
        df = pd.get_dummies(df, columns=['type_local'], drop_first=True)

        # Sélection des features
        features = [
            'surface_reelle_bati',
            'nb_pieces',
            'surface_terrain',
            'annee',
            'mois',
            'surface_par_piece',
            'postal_score',
            'est_paris',
        ]
        if 'type_local_Maison' in df.columns:
            features.append('type_local_Maison')

        X = df[features].dropna()
        y = df.loc[X.index, 'valeur_fonciere']

        # Split Train / Test
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        logger.info(f"Données d'entraînement : {len(X_train):,} lignes.")

        # Entraînement (Voting Regressor RF + XGBoost)
        logger.info("Entraînement du modèle en cours... Cela peut prendre quelques minutes.")
        rf  = RandomForestRegressor(n_estimators=100, max_depth=15, n_jobs=-1)
        xgb = XGBRegressor(n_estimators=300, learning_rate=0.05, max_depth=8, n_jobs=-1)

        model = VotingRegressor([('rf', rf), ('xgb', xgb)])
        model.fit(X_train, y_train)

        # Évaluation
        y_pred = model.predict(X_test)
        r2  = r2_score(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        logger.info(f"Performances -> R² : {r2:.3f} | MAE : {mae:,.0f} €")

        # Sauvegarde
        logger.info("Sauvegarde des fichiers .joblib...")
        joblib.dump(model,                 models_path / 'rf_model_immo.joblib')
        joblib.dump(postal_means,          models_path / 'postal_means.joblib')
        joblib.dump(list(X_train.columns), models_path / 'expected_columns.joblib')

        elapsed = time.time() - start_time
        logger.info(f"RÉ-ENTRAÎNEMENT TERMINÉ AVEC SUCCÈS en {elapsed:.2f} secondes !")

    except Exception as e:
        logger.exception(f"Erreur critique lors de l'entraînement : {e}")

if __name__ == "__main__":
    main()