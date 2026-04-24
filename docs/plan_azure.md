# Plan de Déploiement Cloud - Azure

## 1. Stratégie d'Infrastructure
Pour garantir la portabilité et la rapidité de mise en ligne, l'application est déployée via une architecture **PaaS (Platform as a Service)** sur Microsoft Azure :
* **Service :** Azure App Service for Containers.
* **Registre :** Azure Container Registry (ACR) pour l'hébergement de l'image Docker.
* **Région :** France Central (pour la conformité RGPD et la latence).

## 2. Pipeline de Déploiement (Workflow)
1. **Build :** Création de l'image Docker finale en local.
2. **Push :** Envoi de l'image vers l'Azure Container Registry.
3. **Release :** Mise à jour de l'App Service pour pointer vers la nouvelle image.
4. **Environnement :** Injection des variables d'environnement (Connexion DB, Clés API) via les "Application Settings" d'Azure.

## 3. Sécurité & Disponibilité
* **SSL/TLS :** HTTPS activé par défaut sur l'URL `.azurewebsites.net`.
* **Isolation :** Utilisation de secrets Azure pour éviter de stocker les mots de passe dans le code.
* **Monitoring :** Suivi de l'état de santé du container via Azure Logs.