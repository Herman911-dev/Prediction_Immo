import time
import logging
from datetime import date

import streamlit as st
from src.predictor import RealEstatePredictor



# CONFIGURATION INITIALE
st.set_page_config(
    page_title="EstimaTech IDF | IA",
    page_icon="🏙️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# GESTION DU CACHE & MÉMOIRE
@st.cache_resource(show_spinner="Chargement du moteur d'IA...")
def load_predictor():
    """
    Mise en cache du modèle de Machine Learning.
    Choix technique : '@st.cache_resource' évite de recharger les lourds fichiers 
    .joblib à chaque interaction de l'utilisateur (clic, saisie), garantissant 
    une interface fluide et sans latence.
    """
    return RealEstatePredictor()

def init_session_state():
    """Initialise les variables de session pour le formulaire multi-étapes."""
    if "step" not in st.session_state:
        st.session_state.step = 1
    if "form_data" not in st.session_state:
        st.session_state.form_data = {}

def reset_estimation():
    """Réinitialise l'application pour une nouvelle estimation."""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# COMPOSANTS VISUELS (UI/CSS)
def inject_custom_css():
    """
    Injection de CSS pour surcharger le style par défaut de Streamlit.
    Choix UX : On donne à l'application un aspect "SaaS Premium" (thème sombre, 
    typographie soignée, ombres portées) pour renforcer la crédibilité de l'IA.
    """
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Serif+Display&display=swap');

    #MainMenu, footer, header { visibility: hidden; }
    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; color: #E2E8F0; }
    .stApp { background: #0D1117; }

    /* En-tête (Hero) */
    .hero { text-align: center; padding: 40px 0 30px; }
    .hero-eyebrow { 
        display: inline-block; font-size: 0.72rem; font-weight: 600; letter-spacing: 0.18em;
        text-transform: uppercase; color: #F59E0B; background: rgba(245,158,11,0.1);
        border: 1px solid rgba(245,158,11,0.25); border-radius: 100px; padding: 4px 14px; margin-bottom: 20px;
    }
    .hero-title { font-family: 'DM Serif Display', serif; font-size: clamp(2rem, 5vw, 3rem); margin: 0 0 10px; }
    .hero-title span { color: #F59E0B; }
    .hero-sub { color: #64748B; font-size: 1rem; max-width: 420px; margin: 0 auto; line-height: 1.6; }

    /* Indicateur d'étapes (Stepper) */
    .steps-container { display: flex; align-items: center; justify-content: center; margin: 20px 0 40px; }
    .step-item { display: flex; flex-direction: column; align-items: center; gap: 6px; }
    .step-circle { 
        width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center;
        font-size: 0.8rem; font-weight: 600; border: 2px solid #30363D; color: #64748B; background: #161B22; transition: all 0.3s;
    }
    .step-circle.active { border-color: #F59E0B; color: #F59E0B; background: rgba(245,158,11,0.1); box-shadow: 0 0 20px rgba(245,158,11,0.2); }
    .step-circle.done { border-color: #10B981; color: #10B981; background: rgba(16,185,129,0.1); }
    .step-label { font-size: 0.68rem; font-weight: 500; color: #64748B; text-transform: uppercase; }
    .step-label.active { color: #F59E0B; }
    .step-label.done { color: #10B981; }
    .step-connector { width: 50px; height: 1px; background: #30363D; margin-bottom: 22px; }
    .step-connector.done { background: #10B981; }

    /* Surcharge des inputs Streamlit */
    div[data-testid="stForm"] { background: #161B22; border: 1px solid #21262D; border-radius: 16px; padding: 30px; box-shadow: 0 4px 24px rgba(0,0,0,0.4); }
    div[data-testid="stSelectbox"] > div > div, div[data-testid="stNumberInput"] input, div[data-testid="stTextInput"] input { background: #0D1117; border: 1px solid #30363D; border-radius: 10px; color: #E2E8F0; }
    
    /* Boutons */
    div[data-testid="stFormSubmitButton"] > button, .stButton > button {
        background: #F59E0B; color: #0D1117; border: none; border-radius: 10px; font-weight: 600; transition: all 0.2s; width: 100%;
    }
    div[data-testid="stFormSubmitButton"] > button:hover, .stButton > button:hover { background: #FCD34D; transform: translateY(-1px); }
    
    /* Carte de résultat */
    .result-wrapper { background: linear-gradient(135deg, #161B22 0%, #1C2230 100%); border: 1px solid #21262D; border-radius: 20px; padding: 40px; text-align: center; margin-top: 10px;}
    .result-label { font-size: 0.75rem; font-weight: 600; letter-spacing: 0.15em; text-transform: uppercase; color: #64748B; margin-bottom: 12px; }
    .result-price { font-family: 'DM Serif Display', serif; font-size: 3.5rem; color: #F59E0B; margin-bottom: 8px; }
    .result-meta { font-size: 0.85rem; color: #475569; margin-bottom: 25px; }
    .badge { background: rgba(255,255,255,0.04); border: 1px solid #30363D; border-radius: 8px; padding: 6px 14px; font-size: 0.8rem; color: #94A3B8; margin: 0 5px; display: inline-block;}
    </style>
    """, unsafe_allow_html=True)

def render_header():
    """Affiche l'en-tête et l'indicateur d'étapes dynamique."""
    st.markdown("""
    <div class="hero">
        <div class="hero-eyebrow">Île-de-France · Estimation IA</div>
        <h1 class="hero-title">Quelle est la valeur<br>de votre <span>bien</span> ?</h1>
        <p class="hero-sub">Obtenez une estimation précise basée sur les transactions réelles de l'État (DVF).</p>
    </div>
    """, unsafe_allow_html=True)

    step = st.session_state.step
    s1, s2, s3 = ("done" if step > 1 else "active" if step == 1 else "", 
                  "done" if step > 2 else "active" if step == 2 else "", 
                  "done" if step > 3 else "active" if step == 3 else "")
    
    st.markdown(f"""
    <div class="steps-container">
        <div class="step-item"><div class="step-circle {s1}">{'✓' if s1=='done' else '1'}</div><span class="step-label {s1}">Le bien</span></div>
        <div class="step-connector {s1}"></div>
        <div class="step-item"><div class="step-circle {s2}">{'✓' if s2=='done' else '2'}</div><span class="step-label {s2}">Lieu</span></div>
        <div class="step-connector {s2}"></div>
        <div class="step-item"><div class="step-circle {s3}">{'✓' if s3=='done' else '3'}</div><span class="step-label {s3}">Surfaces</span></div>
    </div>
    """, unsafe_allow_html=True)

# LOGIQUE DES ÉTAPES DU FORMULAIRE
# Choix UX : Séparer en étapes réduit la charge cognitive de l'utilisateur.
# Choix Technique : L'utilisation de 'st.form' évite les rechargements de page inutiles.

def render_step_1():
    with st.form("step1"):
        st.subheader("🏠 Type de bien")
        type_bien = st.radio("Sélectionnez la nature du bien", ["Appartement", "Maison"])
        if st.form_submit_button("Continuer →"):
            st.session_state.form_data["type_bien"] = type_bien
            st.session_state.step = 2
            st.rerun()

def render_step_2():
    with st.form("step2"):
        st.subheader("📍 Localisation")
        code_postal = st.text_input("Code postal (Île-de-France)", placeholder="Ex: 75011", max_chars=5)
        
        col_back, col_next = st.columns([1, 2])
        submitted = col_next.form_submit_button("Continuer →")
        back = col_back.form_submit_button("← Retour")

    if back:
        st.session_state.step = 1
        st.rerun()
    if submitted:
        if len(code_postal) == 5 and code_postal.isdigit():
            st.session_state.form_data["code_postal"] = code_postal
            st.session_state.step = 3
            st.rerun()
        else:
            st.error("Veuillez saisir un code postal valide (5 chiffres).")

def render_step_3(predictor):
    fd = st.session_state.form_data
    is_maison = (fd.get("type_bien") == "Maison")

    with st.form("step3"):
        st.subheader("📐 Caractéristiques")
        col1, col2 = st.columns(2)
        surface = col1.number_input("Surface habitable (m²)", min_value=9, max_value=500, value=50)
        nb_pieces = col2.number_input("Nombre de pièces", min_value=1, max_value=15, value=2)
        terrain = st.number_input("Surface terrain (m²)", min_value=0, value=100) if is_maison else 0

        col_back, col_next = st.columns([1, 2])
        submitted = col_next.form_submit_button("Estimer mon bien 🚀")
        back = col_back.form_submit_button("← Retour")

    if back:
        st.session_state.step = 2
        st.rerun()

    if submitted:
        # Simulation d'un temps de calcul pour rassurer l'utilisateur sur la "réflexion" de l'IA
        with st.spinner("L'Intelligence Artificielle croise vos données avec le marché..."):
            time.sleep(1)
            try:
                estimation = predictor.predict(
                    surface=surface, nb_pieces=nb_pieces, terrain=terrain,
                    type_bien=fd["type_bien"], code_postal=fd["code_postal"],
                    date_mutation=date.today().strftime("%Y-%m-%d")
                )
                prix_m2 = estimation / surface if surface > 0 else 0

                st.markdown(f"""
                <div class="result-wrapper">
                    <div class="result-label">Valeur marchande estimée</div>
                    <div class="result-price">{estimation:,.0f} €</div>
                    <div class="result-meta">{fd['type_bien']} · Code postal {fd['code_postal']} · {surface} m²</div>
                    <div>
                        <span class="badge">≈ {prix_m2:,.0f} €/m²</span>
                        <span class="badge">{nb_pieces} pièce(s)</span>
                        {f"<span class='badge'>Terrain {terrain} m²</span>" if terrain > 0 else ""}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                if st.button("Faire une nouvelle estimation"):
                    reset_estimation()

            except Exception as e:
                st.error("Erreur technique lors de l'estimation. Veuillez réessayer.")
                logging.error(f"Erreur UI Predictor : {e}")

# ORCHESTRATION PRINCIPALE

def main():
    """Point d'entrée de l'application Streamlit."""
    try:
        predictor = load_predictor()
    except Exception as e:
        st.error("Le modèle d'Intelligence Artificielle est indisponible.")
        return

    init_session_state()
    inject_custom_css()
    render_header()

    # Routage vers la bonne étape du formulaire
    if st.session_state.step == 1:
        render_step_1()
    elif st.session_state.step == 2:
        render_step_2()
    elif st.session_state.step == 3:
        render_step_3(predictor)


if __name__ == "__main__":
    main()