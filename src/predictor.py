import joblib
import pandas as pd
import os
from pathlib import Path
import logging
import time

# Configuration du Logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class RealEstatePredictor:
    """
    Classe professionnelle pour gérer les prédictions immobilières.
    Elle gère le chargement automatique des modèles et la transformation des données.
    """
    
    def __init__(self):
        # Gestion dynamique des chemins
        # On récupère le dossier où se trouve ce fichier 
        self.base_path = Path(__file__).parent
        self.models_path = self.base_path.parent / "models"
        
        # Initialisation des variables
        self.model = None
        self.postal_means = None
        self.expected_columns = None
        
        # Chargement automatique au démarrage
        self._load_artifacts()

    def _load_artifacts(self):
        """Charge les fichiers .joblib en vérifiant leur existence."""
        logger.info("Initialisation du Predictor. Recherche des modèles...")
        files = {
            "model": self.models_path / "rf_model_immo.joblib",
            "postal": self.models_path / "postal_means.joblib",
            "columns": self.models_path / "expected_columns.joblib"
        }
        
        try:
            # Vérification de sécurité
            for name, path in files.items():
                if not path.exists():
                    raise FileNotFoundError(f"Le fichier {path} est introuvable.")
                
            
            # Chargement effectif
            self.model = joblib.load(files["model"])
            self.postal_means = joblib.load(files["postal"])
            self.expected_columns = joblib.load(files["columns"])
            
            logger.info("Intelligence Artificielle et méta-données chargées avec succès.")
        
        except Exception as e:
            logger.exception(f"Erreur critique lors du chargement des modèles : {e}")
            raise

    def predict(self, surface, nb_pieces, terrain, type_bien, code_postal, date_mutation):
        """Réalise la prédiction à partir des données brutes utilisateur."""
        logger.info(f"Demande de prédiction reçue : {type_bien} de {surface}m² à {code_postal}.")
        
        try:
            # Feature Engineering
            date = pd.to_datetime(date_mutation)
            annee, mois = date.year, date.month
            surface_par_piece = surface / max(1, nb_pieces)
            
            # Récupération du score postal (moyenne globale si inconnu)
            postal_score = self.postal_means.get(str(code_postal), self.postal_means.mean())
            est_paris = 1 if str(code_postal).startswith('75') else 0
            
            # PRÉPARATION DU FORMAT 
            input_data = {col: [0] for col in self.expected_columns}
            input_data.update({
                'surface_reelle_bati': [surface],
                'nb_pieces': [nb_pieces],
                'surface_terrain': [terrain],
                'annee': [annee],
                'mois': [mois],
                'surface_par_piece': [surface_par_piece],
                'postal_score': [postal_score],
                'est_paris': [est_paris]
            })
            
            if type_bien == "Maison" and 'type_local_Maison' in input_data:
                input_data['type_local_Maison'] = [1]
                
            # Conversion en DataFrame et remise en ordre des colonnes
            df_final = pd.DataFrame(input_data)[self.expected_columns]
            
            # PRÉDICTION
            res = self.model.predict(df_final)[0]
            logger.info(f"Prédiction réussie : {res:,.2f} €")
            return round(res, 2)
            
        except Exception as e:
            logger.error(f"Erreur lors du calcul de la prédiction : {e}")
            raise

# --- TEST ---
if __name__ == "__main__":
    # On instancie le prédicteur une seule fois
    logger.info("Lancement du test local de predictor.py")
    start_time = time.time()
    
    try:
        # On demande une estimation
        predictor = RealEstatePredictor()
        prix = predictor.predict(
            surface=45, 
            nb_pieces=2, 
            terrain=0, 
            type_bien="Appartement", 
            code_postal="75011", 
            date_mutation="2024-06-01"
        )
        
        execution_time = round((time.time() - start_time) * 1000, 2)
        logger.info(f"Test terminé en {execution_time} ms. Prix final estimé : {prix:,.0f} €")
        
    except Exception as e:
        logger.error("Le test a échoué.")