# On prend la version de Python
FROM python:3.14-slim

# On crée le dossier principal dans le mini-ordinateur
WORKDIR /app

# On copie le fichier des dépendances en premier
COPY requirements.txt .

# On installe toutes tes bibliothèques (Pandas, Streamlit, Scikit-learn, etc.)
RUN pip install --no-cache-dir -r requirements.txt

# On copie les éléments vitaux de l'application
COPY app.py .
COPY src/ ./src/
COPY models/ ./models/

# Si l'app a besoin de lire le CSV pour afficher des stats, on décommente la ligne :
# COPY data/cleaned/dvf_idf_cleaned.csv ./data/cleaned/

# On ouvre la porte 8501 
EXPOSE 8501

# La commande pour lancer le site
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]