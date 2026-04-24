# Cahier des Charges Fonctionnel et Technique - Prediction Immo

## 1. Spécifications Fonctionnelles
L'application doit permettre les actions suivantes :
* **Chargement des données :** Importer les fichiers DVF de 2021 à 2025.
* **Interface de saisie :** Formulaire comprenant :
    * Type de bien (Appartement / Maison).
    * Surface réelle bâtie (m²).
    * Nombre de pièces principales.
    * Code postal / Département.
* **Moteur de prédiction :** Calculer une estimation du prix de vente via un modèle de régression.
* **Visualisation :** Afficher l'historique des ventes similaires dans un rayon géographique proche.

## 2. Spécifications Techniques
* **Langage :** Python 3.10+.
* **Traitement de données :** Pandas / Numpy.
* **Machine Learning :** Scikit-Learn (Random Forest ou Régression Linéaire).
* **Interface :** Streamlit.
* **Conteneurisation :** Docker / Docker-compose.
* **Versionnage :** Git (GitHub).

## 3. Contraintes et Performances
* **Volume de données :** Capacité à traiter des datasets de plusieurs gigaoctets (millions de lignes).
* **Temps de réponse :** L'inférence (prédiction) doit être quasi-instantanée (< 1s).
* **Qualité de code :** Respect strict de la PEP8 et couverture de tests unitaires via Pytest.

## 4. Sécurité et Confidentialité
* **RGPD :** Anonymisation des données lors du traitement.
* **Validation :** Contrôle de cohérence des données saisies (pas de surface négative, etc.).