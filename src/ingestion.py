import pandas as pd
from pathlib import Path
import time
import re
import logging
import os

# Configuration de Logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def process_dvf_file(file_path):
    """
    Ouvre, filtre et nettoie un fichier DVF brut.
    Ne garde que les ventes résidentielles d'Île-de-France avec des valeurs cohérentes.
    """
    # Configuration des filtres géographiques et colonnes
    idf_depts = ['75', '77', '78', '91', '92', '93', '94', '95']
    cols_to_keep = [
        'Date mutation', 'Nature mutation', 'Valeur fonciere', 
        'Code postal', 'Code departement', 'Type local', 
        'Surface reelle bati', 'Nombre pieces principales', 'Surface terrain'
    ]

    try:
        # Lecture optimisée
        df = pd.read_csv(file_path, sep="|", usecols=cols_to_keep, low_memory=False, dtype={'Code departement': str})
        
        # Filtrage immédiat
        df = df[df['Code departement'].isin(idf_depts)]
        df = df[df['Nature mutation'] == 'Vente']
        df = df[df['Type local'].isin(['Maison', 'Appartement'])]

        # Optimisation des types
        df['Type local'] = df['Type local'].astype('category')
        df['Code departement'] = df['Code departement'].astype('category')

        # Nettoyage et Conversion
        df['Valeur fonciere'] = df['Valeur fonciere'].astype(str).str.replace(',', '.').astype(float)
        df['Date mutation'] = pd.to_datetime(df['Date mutation'], dayfirst=True)
        df['Surface terrain'] = df['Surface terrain'].fillna(0)

        # Suppression des valeurs nulles et calcul du prix_m2
        df = df.dropna(subset=['Valeur fonciere', 'Surface reelle bati'])
        df = df[df['Surface reelle bati'] > 0]
        df['prix_m2'] = df['Valeur fonciere'] / df['Surface reelle bati']

        # Filtres Métier (Logique conservée)
        df = df[(df['prix_m2'] >= 1000) & (df['prix_m2'] <= 31000)]
        df = df[(df['Surface reelle bati'] >= 9) & (df['Surface reelle bati'] <= 300)]
        df = df[(df['Nombre pieces principales'] >= 1) & (df['Nombre pieces principales'] <= 10)]
        
        return df

    except FileNotFoundError:
        logger.error(f"Fichier introuvable : {file_path}")
        return None
    except Exception as e:
        logger.error(f"Erreur lors du traitement de {file_path.name} : {e}")
        return None

def main():
    logger.info("Début du pipeline d'ingestion DVF SCALABLE.")
    start_time = time.time()

    try:
        data_dir = Path("data")
        all_dfs = []

        # Découverte automatique des fichiers
        dvf_files = list(data_dir.glob("ValeursFoncieres-*.txt"))
        
        if not dvf_files:
            logger.warning("Aucun fichier trouvé dans le dossier /data.")
            return

        # Tri des fichiers
        dvf_files.sort()
        logger.info(f"{len(dvf_files)} fichiers identifiés pour traitement.")

        for file_path in dvf_files:
            year_match = re.search(r"(\d{4})", file_path.name)
            year = year_match.group(1) if year_match else "Inconnue"
            
            logger.info(f"Traitement de l'année {year} ({file_path.name})...")
            
            df_year = process_dvf_file(file_path) 
            
            if df_year is not None:
                logger.info(f"{len(df_year):,} transactions conservées pour {year}.")
                all_dfs.append(df_year)

        # Fusion et Sauvegarde
        if all_dfs:
            logger.info("Fusion des données multi-annuelles en cours...")
            master_df = pd.concat(all_dfs, ignore_index=True)
            
            output_dir = data_dir / "cleaned"
            os.makedirs(output_dir, exist_ok=True)
            output_path = output_dir / "dvf_idf_cleaned.csv"
            
            logger.info(f"Sauvegarde du fichier final : {output_path}")
            master_df.to_csv(output_path, index=False)
            
            # Bilan Final
            execution_time = time.time() - start_time
            logger.info("="*40)
            logger.info("INGESTION TERMINÉE AVEC SUCCÈS !")
            logger.info(f"Volume total : {len(master_df):,} transactions.")
            logger.info(f"Temps d'exécution : {execution_time:.2f} secondes.")
            logger.info("="*40)
        else:
            logger.error("Aucune donnée n'a pu être traitée.")

    except Exception as e:
        logger.exception(f"Erreur critique durant l'exécution : {e}")

if __name__ == "__main__":
    main()