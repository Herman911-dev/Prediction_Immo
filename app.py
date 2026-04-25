import streamlit as st
import datetime
from src.predictor import RealEstatePredictor # Assure-toi que le chemin d'import est correct selon ton dossier

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Estimateur Immo IDF",
    page_icon="🏠",
    layout="centered"
)

# --- CHARGEMENT DE L'IA (Mise en cache pour la vitesse) ---
@st.cache_resource
def load_ai():
    return RealEstatePredictor()

predictor = load_ai()

# --- HEADER ---
st.title("🏠 IA d'Estimation Immobilière")
st.markdown("Estimez le prix de votre appartement ou maison grâce à notre modèle d'Intelligence Artificielle entraîné sur les données publiques de l'État (DVF).")
st.divider()

# --- INTERFACE UTILISATEUR (Formulaire) ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("📍 Localisation & Type")
    type_bien = st.selectbox("Type de bien", ["Appartement", "Maison"])
    code_postal = st.text_input("Code Postal", value="75015", max_chars=5)
    date_est = st.date_input("Date de l'estimation", datetime.date.today())

with col2:
    st.subheader("📏 Caractéristiques")
    surface = st.number_input("Surface habitable (m²)", min_value=9, max_value=500, value=50)
    nb_pieces = st.number_input("Nombre de pièces", min_value=1, max_value=15, value=2)
    
    # Le terrain n'a de sens que pour une maison
    if type_bien == "Maison":
        terrain = st.number_input("Surface du terrain (m²)", min_value=0, max_value=5000, value=100)
    else:
        terrain = 0

st.divider()

# --- BOUTON DE PRÉDICTION ---
# Tout ce qui est dans ce 'if' ne s'exécute que quand on clique sur le bouton
if st.button("🔮 Lancer l'estimation", use_container_width=True, type="primary"):
    
    # Petite animation de chargement sympa
    with st.spinner("L'IA analyse le marché immobilier local..."):
        try:
            # Appel de notre fichier predictor.py
            prix_estime = predictor.predict(
                surface=surface,
                nb_pieces=nb_pieces,
                terrain=terrain,
                type_bien=type_bien,
                code_postal=code_postal,
                date_mutation=date_est
            )
            
            # Affichage du résultat en grand
            st.success("✅ Estimation terminée !")
            st.metric(label="Valeur estimée de votre bien", value=f"{prix_estime:,.0f} €".replace(",", " "))
            
            # Petit mot d'avertissement métier
            st.caption("⚠️ Cette estimation est générée par un algorithme. Elle ne remplace pas l'expertise physique d'un agent immobilier (état intérieur, vue, étage...).")
            
        except Exception as e:
            st.error(f"Oups ! Une erreur s'est produite lors de l'estimation. Vérifiez vos données. (Erreur technique : {e})")