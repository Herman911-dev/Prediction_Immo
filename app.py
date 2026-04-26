import streamlit as st
from datetime import date
import time

from src.predictor import RealEstatePredictor

# ==========================================
# CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="EstimaTech IDF",
    page_icon="🏙️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==========================================
# CSS — Dark Premium
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Serif+Display&display=swap');

/* ---- Reset & Base ---- */
#MainMenu, footer, header { visibility: hidden; }

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: #E2E8F0;
}

.stApp {
    background: #0D1117;
}

/* ---- Scrollbar ---- */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #0D1117; }
::-webkit-scrollbar-thumb { background: #30363D; border-radius: 4px; }

/* ---- Hero ---- */
.hero {
    text-align: center;
    padding: 56px 0 40px;
}
.hero-eyebrow {
    display: inline-block;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #F59E0B;
    background: rgba(245,158,11,0.1);
    border: 1px solid rgba(245,158,11,0.25);
    border-radius: 100px;
    padding: 4px 14px;
    margin-bottom: 20px;
}
.hero-title {
    font-family: 'DM Serif Display', serif;
    font-size: clamp(2rem, 5vw, 3rem);
    font-weight: 400;
    color: #F1F5F9;
    line-height: 1.15;
    margin: 0 0 14px;
}
.hero-title span {
    color: #F59E0B;
}
.hero-sub {
    color: #64748B;
    font-size: 1rem;
    font-weight: 300;
    max-width: 420px;
    margin: 0 auto;
    line-height: 1.6;
}

/* ---- Step indicator ---- */
.steps-container {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0;
    margin: 32px 0 40px;
}
.step-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 6px;
}
.step-circle {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.8rem;
    font-weight: 600;
    border: 2px solid #30363D;
    color: #64748B;
    background: #161B22;
    transition: all 0.3s;
}
.step-circle.active {
    border-color: #F59E0B;
    color: #F59E0B;
    background: rgba(245,158,11,0.1);
    box-shadow: 0 0 20px rgba(245,158,11,0.2);
}
.step-circle.done {
    border-color: #10B981;
    color: #10B981;
    background: rgba(16,185,129,0.1);
}
.step-label {
    font-size: 0.68rem;
    font-weight: 500;
    color: #64748B;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}
.step-label.active { color: #F59E0B; }
.step-label.done { color: #10B981; }
.step-connector {
    width: 60px;
    height: 1px;
    background: #30363D;
    margin-bottom: 22px;
}
.step-connector.done { background: #10B981; }

/* ---- Cards ---- */
.card {
    background: #161B22;
    border: 1px solid #21262D;
    border-radius: 16px;
    padding: 32px 36px;
    margin-bottom: 20px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.4);
}
.card-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: #E2E8F0;
    margin-bottom: 4px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.card-desc {
    font-size: 0.85rem;
    color: #64748B;
    margin-bottom: 28px;
}

/* ---- Streamlit widget overrides ---- */
div[data-testid="stSelectbox"] label,
div[data-testid="stNumberInput"] label,
div[data-testid="stTextInput"] label,
div[data-testid="stRadio"] label {
    color: #94A3B8 !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.04em !important;
    text-transform: uppercase !important;
}

div[data-testid="stSelectbox"] > div > div,
div[data-testid="stNumberInput"] input,
div[data-testid="stTextInput"] input {
    background: #0D1117 !important;
    border: 1px solid #30363D !important;
    border-radius: 10px !important;
    color: #E2E8F0 !important;
    font-family: 'DM Sans', sans-serif !important;
}

div[data-testid="stSelectbox"] > div > div:focus-within,
div[data-testid="stNumberInput"] input:focus,
div[data-testid="stTextInput"] input:focus {
    border-color: #F59E0B !important;
    box-shadow: 0 0 0 3px rgba(245,158,11,0.15) !important;
    outline: none !important;
}

/* Radio buttons as toggle pills */
div[data-testid="stRadio"] > div {
    gap: 12px !important;
    flex-direction: row !important;
    flex-wrap: wrap !important;
}
div[data-testid="stRadio"] > div > label {
    background: #0D1117 !important;
    border: 1px solid #30363D !important;
    border-radius: 100px !important;
    padding: 8px 20px !important;
    color: #94A3B8 !important;
    font-size: 0.88rem !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
    text-transform: none !important;
    letter-spacing: 0 !important;
    font-weight: 400 !important;
}
div[data-testid="stRadio"] > div > label:has(input:checked) {
    background: rgba(245,158,11,0.12) !important;
    border-color: #F59E0B !important;
    color: #F59E0B !important;
}

/* Buttons */
div[data-testid="stFormSubmitButton"] > button,
.stButton > button {
    background: #F59E0B !important;
    color: #0D1117 !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    padding: 12px 28px !important;
    transition: all 0.2s !important;
    letter-spacing: 0.02em !important;
}
div[data-testid="stFormSubmitButton"] > button:hover,
.stButton > button:hover {
    background: #FCD34D !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 24px rgba(245,158,11,0.3) !important;
}

/* Secondary button */
.stButton > button[kind="secondary"] {
    background: transparent !important;
    color: #64748B !important;
    border: 1px solid #30363D !important;
}
.stButton > button[kind="secondary"]:hover {
    color: #E2E8F0 !important;
    border-color: #64748B !important;
    transform: none !important;
    box-shadow: none !important;
}

/* ---- Result card ---- */
.result-wrapper {
    background: linear-gradient(135deg, #161B22 0%, #1C2230 100%);
    border: 1px solid #21262D;
    border-radius: 20px;
    padding: 44px 36px;
    text-align: center;
    box-shadow: 0 8px 40px rgba(0,0,0,0.5);
    position: relative;
    overflow: hidden;
    margin-top: 10px;
}
.result-wrapper::before {
    content: '';
    position: absolute;
    top: -60px; left: 50%;
    transform: translateX(-50%);
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(245,158,11,0.08) 0%, transparent 70%);
    pointer-events: none;
}
.result-label {
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #64748B;
    margin-bottom: 12px;
}
.result-price {
    font-family: 'DM Serif Display', serif;
    font-size: clamp(2.5rem, 7vw, 3.8rem);
    font-weight: 400;
    color: #F59E0B;
    line-height: 1;
    margin-bottom: 8px;
}
.result-meta {
    font-size: 0.85rem;
    color: #475569;
    margin-bottom: 28px;
}
.result-badges {
    display: flex;
    gap: 10px;
    justify-content: center;
    flex-wrap: wrap;
}
.badge {
    background: rgba(255,255,255,0.04);
    border: 1px solid #30363D;
    border-radius: 8px;
    padding: 6px 14px;
    font-size: 0.8rem;
    color: #94A3B8;
}

/* ---- Divider ---- */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #30363D, transparent);
    margin: 32px 0;
}

/* ---- Native Streamlit form styled as card ---- */
div[data-testid="stForm"] {
    background: #161B22 !important;
    border: 1px solid #21262D !important;
    border-radius: 16px !important;
    padding: 32px 36px !important;
    box-shadow: 0 4px 24px rgba(0,0,0,0.4) !important;
}

/* ---- Force hero centering ---- */
.block-container {
    text-align: center;
}
.block-container > div {
    text-align: left;
}
div[data-testid="stForm"] {
    text-align: left;
}

/* ---- Warning & Error ---- */
div[data-testid="stAlert"] {
    background: rgba(239,68,68,0.08) !important;
    border: 1px solid rgba(239,68,68,0.3) !important;
    border-radius: 10px !important;
    color: #FCA5A5 !important;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# CACHE
# ==========================================
@st.cache_resource
def load_predictor():
    return RealEstatePredictor()

try:
    predictor = load_predictor()
except Exception as e:
    st.error("⚠️ Impossible de charger le modèle. Vérifiez que les modèles sont entraînés.")
    st.stop()

# ==========================================
# SESSION STATE (étapes)
# ==========================================
if "step" not in st.session_state:
    st.session_state.step = 1
if "form_data" not in st.session_state:
    st.session_state.form_data = {}

# ==========================================
# HERO
# ==========================================
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">Île-de-France · Estimation IA</div>
    <h1 class="hero-title">Quelle est la valeur<br>de votre <span>bien</span> ?</h1>
    <p class="hero-sub">Obtenez une estimation précise en moins de 30 secondes, basée sur les transactions réelles du marché.</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# STEP INDICATOR
# ==========================================
def step_class(target):
    if st.session_state.step > target:
        return "done"
    elif st.session_state.step == target:
        return "active"
    return ""

s1 = step_class(1)
s2 = step_class(2)
s3 = step_class(3)

connector_1 = "done" if st.session_state.step > 1 else ""
connector_2 = "done" if st.session_state.step > 2 else ""

icon1 = "✓" if s1 == "done" else "1"
icon2 = "✓" if s2 == "done" else "2"
icon3 = "✓" if s3 == "done" else "3"

st.markdown(f"""
<div class="steps-container">
    <div class="step-item">
        <div class="step-circle {s1}">{icon1}</div>
        <span class="step-label {s1}">Le bien</span>
    </div>
    <div class="step-connector {connector_1}"></div>
    <div class="step-item">
        <div class="step-circle {s2}">{icon2}</div>
        <span class="step-label {s2}">Localisation</span>
    </div>
    <div class="step-connector {connector_2}"></div>
    <div class="step-item">
        <div class="step-circle {s3}">{icon3}</div>
        <span class="step-label {s3}">Surfaces</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ==========================================
# ÉTAPE 1 — Type de bien
# ==========================================
if st.session_state.step == 1:
    with st.form("step1_form"):
        st.markdown('<div class="card-title">🏠 Type de bien</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-desc">Sélectionnez la nature du bien à estimer</div>', unsafe_allow_html=True)
        type_bien = st.radio(
            "Type",
            ["Appartement", "Maison"],
            label_visibility="collapsed"
        )
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("Continuer →", use_container_width=True)

    if submitted:
        st.session_state.form_data["type_bien"] = type_bien
        st.session_state.step = 2
        st.rerun()


# ==========================================
# ÉTAPE 2 — Localisation
# ==========================================
elif st.session_state.step == 2:
    with st.form("step2_form"):
        st.markdown('<div class="card-title">📍 Localisation</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-desc">Renseignez le code postal du bien en Île-de-France</div>', unsafe_allow_html=True)
        code_postal = st.text_input(
            "Code postal",
            placeholder="Ex : 75011, 93100, 92200…",
            max_chars=5
        )
        st.markdown("<br>", unsafe_allow_html=True)
        # "Continuer" déclaré EN PREMIER dans le DOM → reçoit Entrée.
        # CSS flex order pour l'afficher visuellement à droite.
        col_back, col_next = st.columns([1, 2])
        with col_next:
            submitted = st.form_submit_button("Continuer →", use_container_width=True)
        with col_back:
            back = st.form_submit_button("← Retour", use_container_width=True)

    if back:
        st.session_state.step = 1
        st.rerun()
    if submitted:
        if len(code_postal) != 5 or not code_postal.isdigit():
            st.warning("⚠️ Entrez un code postal valide à 5 chiffres.")
        else:
            st.session_state.form_data["code_postal"] = code_postal
            st.session_state.step = 3
            st.rerun()


# ==========================================
# ÉTAPE 3 — Surfaces
# ==========================================
elif st.session_state.step == 3:
    is_maison = st.session_state.form_data.get("type_bien") == "Maison"

    with st.form("step3_form"):
        st.markdown('<div class="card-title">📐 Caractéristiques</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-desc">Renseignez les surfaces et le nombre de pièces</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            surface = st.number_input("Surface habitable (m²)", min_value=9, max_value=500, value=50, step=1)
        with col2:
            nb_pieces = st.number_input("Nombre de pièces", min_value=1, max_value=15, value=2, step=1)

        if is_maison:
            terrain = st.number_input("Surface terrain (m²)", min_value=0, max_value=5000, value=100, step=10)
        else:
            terrain = 0

        st.markdown("<br>", unsafe_allow_html=True)
        col_back, col_next = st.columns([1, 2])
        with col_next:
            submitted = st.form_submit_button("Obtenir l'estimation 🚀", use_container_width=True)
        with col_back:
            back = st.form_submit_button("← Retour", use_container_width=True)

    if back:
        st.session_state.step = 2
        st.rerun()

    if submitted:
        fd = st.session_state.form_data
        with st.spinner("Analyse du marché en cours…"):
            time.sleep(1.2)
            try:
                estimation = predictor.predict(
                    surface=surface,
                    nb_pieces=nb_pieces,
                    terrain=terrain,
                    type_bien=fd["type_bien"],
                    code_postal=fd["code_postal"],
                    date_mutation=date.today().strftime("%Y-%m-%d")
                )

                prix_m2 = estimation / surface if surface > 0 else 0

                st.markdown(f"""
                <div class="result-wrapper">
                    <div class="result-label">Valeur estimée</div>
                    <div class="result-price">{estimation:,.0f} €</div>
                    <div class="result-meta">{fd['type_bien']} · {fd['code_postal']} · {surface} m²</div>
                    <div class="result-badges">
                        <span class="badge">≈ {prix_m2:,.0f} €/m²</span>
                        <span class="badge">{nb_pieces} pièce{"s" if nb_pieces > 1 else ""}</span>
                        {f"<span class='badge'>Terrain {terrain} m²</span>" if is_maison and terrain > 0 else ""}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Nouvelle estimation", use_container_width=True):
                    for key in list(st.session_state.keys()):
                        del st.session_state[key]
                    st.rerun()

            except Exception as e:
                st.error(f"Une erreur est survenue : {e}")