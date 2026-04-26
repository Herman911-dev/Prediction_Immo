# Prediction_Immo

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg?logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791.svg?logo=postgresql&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B.svg?logo=streamlit&logoColor=white)
![Machine Learning](https://img.shields.io/badge/Machine_Learning-XGBoost_%7C_RF-green.svg)

**EstimaTech IDF** est une solution Data/MLOps complète permettant d'estimer avec précision le prix de vente d'un bien immobilier en Île-de-France (appartements et maisons). 

Basé sur les données ouvertes de l'État français (**DVF - Demandes de Valeurs Foncières**), ce projet intègre un pipeline ETL robuste, une modélisation par Machine Learning, et une architecture conteneurisée prête à être déployée dans le Cloud.

---

## Fonctionnalités clés

* **Prédiction instantanée :** Estimation basée sur les caractéristiques du bien (surface, pièces, terrain, code postal).
* **Intelligence Géographique :** Utilisation du *Target Encoding* pour capturer la valeur intrinsèque des codes postaux franciliens.
* **Pipeline Automatisé (MLOps) :** Scripts d'extraction, de nettoyage et d'ingestion massive (`COPY`) en base de données.
* **Architecture Isolé :** Conteneurisation complète (App + BDD) avec Docker et Docker Compose.
* **Interface :** Frontend Streamlit avec un design sur-mesure pour une expérience utilisateur optimale.

---

## 🛠️ Stack Technique

| Composant | Technologies utilisées |
| :--- | :--- |
| **Frontend / UI** | Streamlit, CSS custom |
| **Machine Learning** | Scikit-learn (Random Forest), XGBoost, Joblib |
| **Data Processing** | Pandas, NumPy |
| **Base de données** | PostgreSQL 15 |
| **ORM / Ingestion** | SQLAlchemy, Psycopg2, module `csv` (Bulk Insert) |
| **Infrastructure** | Docker, Docker-compose |
| **Cloud (Cible)** | Azure (Container Registry, App Service) |

---

## 📂 Architecture du Projet

```text
Prediction_Immo/
├── app.py                  # Interface Streamlit principale (Frontend)
├── src/                    # Code source métier
│   ├── ingestion.py        # Script ETL (Extraction & Nettoyage DVF)
│   ├── to_sql.py           # Ingestion massive vers PostgreSQL
│   ├── train.py            # Entraînement du modèle ML et sérialisation
│   └── predictor.py        # Classe d'inférence sécurisée
├── models/                 # Modèles sérialisés (.joblib)
├── data/                   # Données brutes et nettoyées (DVF)
├── Dockerfile              # Instructions de build de l'image Streamlit
├── docker-compose.yml      # Orchestration des services (App + PostgreSQL)
├── requirements.txt        # Dépendances Python
├── env.example             # Template des variables d'environnement
└── update_pipeline.bat     # Script d'automatisation global (Windows)