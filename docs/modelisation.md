# Modélisation des Données - Prediction Immo

## 1. Dictionnaire des données (Extrait)
* **Bien Immobilier :** ID, Type (Maison/Appart), Surface (m²), Nb_Pieces.
* **Localisation :** Code_Postal, Commune, Code_Departement, Longitude, Latitude.
* **Transaction :** ID_Vente, Date_Mutation, Valeur_Fonciere.

## 2. Schéma Relationnel (MCD)
Pour répondre aux besoins de l'application, la structure suivante est retenue :
```
mermaiderDiagram
    LOCALISATION ||--o{ BIEN : "se situe"
    BIEN ||--o{ TRANSACTION : "fait l'objet de"

    LOCALISATION {
        string code_postal PK
        string commune
        string code_departement
        float longitude
        float latitude
    }

    BIEN {
        int id_bien PK
        string type_local
        float surface_reelle
        int nb_pieces
        string code_postal FK
    }

    TRANSACTION {
        int id_mutation PK
        date date_mutation
        float valeur_fonciere
        int id_bien FK
    }
```

**Justification :** Cette structure permet d'historiser plusieurs ventes pour un même bien ou une même zone géographique sans duplication inutile d'informations.

## 3. Choix Technologiques
* **Stockage Brut :** Fichiers Parquet (optimisés pour le volume DVF) pour la phase de Machine Learning.
* **Base Applicative :** SQLite ou PostgreSQL pour la gestion des utilisateurs et l'historique des recherches.
* **Contraintes d'intégrité :** Utilisation de clés étrangères pour lier les transactions aux localisations afin d'éviter les données orphelines.