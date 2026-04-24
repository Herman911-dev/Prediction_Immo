# Analyse des Risques et Conformité - Prediction Immo

## 1. Matrice des Risques Techniques
| Risque | Impact | Probabilité | Mesure d'atténuation (Mitigation) |
| :--- | :--- | :--- | :--- |
| **Saturation Mémoire** (Fichiers DVF trop lourds) | Critique | Haute | Utilisation de chargement par "chunks" avec Pandas et nettoyage immédiat des colonnes inutiles. |
| **Bruit dans les données** (Valeurs aberrantes) | Moyen | Très Haute | Mise en place de filtres statistiques (IQR) pour supprimer les ventes irréalistes (ex: 1€). |
| **Sécurité du Code** (Injection via interface) | Majeur | Faible | Validation stricte des types d'entrée avec Pydantic et sanitisation des formulaires Streamlit. |
| **Obsolescence du modèle** | Faible | Moyenne | Mise en place d'un pipeline de ré-entraînement facile avec les nouvelles données Etalab. |

## 2. Conformité RGPD & Protection des données
Bien que les données DVF soient en Open Data, le projet respecte les principes suivants :
* **Minimisation :** Seules les données strictement nécessaires à la prédiction (prix, surface, localisation) sont conservées.
* **Anonymisation :** Les noms des vendeurs/acheteurs ne sont jamais importés. Les numéros de parcelles sont traités de manière agrégée pour éviter le ciblage individuel.
* **Sécurité :** Les fichiers bruts sont stockés dans un dossier `data/` protégé par le `.gitignore` pour ne pas être exposés publiquement sur GitHub.

## 3. Plan de Continuité
En cas d'indisponibilité de l'API de géocodage ou des sources de données, l'application fonctionnera en mode dégradé avec les dernières données locales mises en cache.