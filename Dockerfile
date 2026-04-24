# 1. Image de base 
FROM python:3.10-slim
# 2. Dossier de travail dans le conteneur
WORKDIR /app
# 3. Installation des dépendances système (si besoin)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 4. Copie et installation des bibliothèques Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# 5. Copie de tout le code du projet
COPY . .
# 6. Port utilisé par Streamlit
EXPOSE 8501
# 7. Commande de lancement (on l'ajustera plus tard)
CMD ["streamlit", "run", "src/app.py"]