import pandas as pd
from pathlib import Path
import time
import re

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

    # Lecture optimisée
    try:
        df = pd.read_csv(file_path, sep="|", usecols=cols_to_keep, low_memory=False, dtype={'Code departement': str})
    except FileNotFoundError:
        print(f"Fichier introuvable : {file_path}")
        return None

    # Filtrage immédiat
    df = df[df['Code departement'].isin(idf_depts)]
    df = df[df['Nature mutation'] == 'Vente']
    df = df[df['Type local'].isin(['Maison', 'Appartement'])]

    # Optimisation des types
    df['Type local'] = df['Type local'].astype('category')
    df['Code departement'] = df['Code departement'].astype('category')

    # Nettoyage et Conversion
    # Transformation du prix
    df['Valeur fonciere'] = df['Valeur fonciere'].astype(str).str.replace(',', '.').astype(float)
    # Transformation de la date
    df['Date mutation'] = pd.to_datetime(df['Date mutation'], dayfirst=True)
    # Gestion des terrains
    df['Surface terrain'] = df['Surface terrain'].fillna(0)

    # Suppression des valeurs nulles et calcul du prix_m2
    df = df.dropna(subset=['Valeur fonciere', 'Surface reelle bati'])
    df = df[df['Surface reelle bati'] > 0]
    df['prix_m2'] = df['Valeur fonciere'] / df['Surface reelle bati']

    # Filtres Métier
    df = df[(df['prix_m2'] >= 1000) & (df['prix_m2'] <= 31000)]
    df = df[(df['Surface reelle bati'] >= 9) & (df['Surface reelle bati'] <= 300)]
    df = df[(df['Nombre pieces principales'] >= 1) & (df['Nombre pieces principales'] <= 10)]

    return df

def main():
    print("Début du pipeline d'ingestion DVF SCALABLE...")
    start_time = time.time()

    data_dir = Path("data")
    all_dfs = []

    # Découverte automatique des fichiers
    # On cherche tous les fichiers qui commencent par "ValeursFoncieres-" et finissent par ".txt"
    dvf_files = list(data_dir.glob("ValeursFoncieres-*.txt"))
    
    if not dvf_files:
        print("Aucun fichier trouvé dans le dossier /data.")
        return

    # Tri des fichiers pour traiter les années dans l'ordre
    dvf_files.sort()

    for file_path in dvf_files:
        # On extrait l'année du nom du fichier pour le print
        year_match = re.search(r"(\d{4})", file_path.name)
        year = year_match.group(1) if year_match else "Inconnue"
        
        print(f"Traitement automatique de l'année {year} ({file_path.name})...")
        
        df_year = process_dvf_file(file_path) 
        
        if df_year is not None:
            print(f"  {len(df_year)} transactions conservées.")
            all_dfs.append(df_year)

    # Fusion de toutes les années
    if all_dfs:
        print("\n Fusion des données en cours...")
        master_df = pd.concat(all_dfs, ignore_index=True)
        
        # Sauvegarde du fichier propre
        output_path = data_dir / "dvf_idf_cleaned.csv"
        master_df.to_csv(output_path, index=False)
        
        # Bilan
        end_time = time.time()
        execution_time = end_time - start_time
        
        print("\n" + "="*40)
        print(" INGESTION TERMINÉE !")
        print(f" Volume total : {len(master_df)} transactions sur 5 ans.")
        print(f" Fichier sauvegardé : {output_path}")
        print(f" Temps d'exécution : {execution_time:.2f} secondes.")
        print("="*40 + "\n")
    else:
        print("Aucune donnée n'a pu être traitée.")

# Point d'entrée du script
if __name__ == "__main__":
    main()