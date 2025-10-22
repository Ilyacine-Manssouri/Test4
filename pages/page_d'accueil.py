import streamlit as st
import pandas as pd
import pathlib
import os

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Page d'accueil",
    layout="wide",
    page_icon="images/NEURONAIZE-ICONE-BLANC.png",
)

# --- CONSTANTES ---
OUTPUT_DIR = "Data/Data_base"
CSS_PATH = pathlib.Path("assets/styles.css")


# --- FONCTIONS UTILITAIRES ---
def load_css(file_path: pathlib.Path):
    """Charge une feuille de style CSS externe."""
    if file_path.exists():
        with open(file_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.warning(f"⚠️ Fichier CSS non trouvé : {file_path}")

@st.cache_data
def save_uploaded_file(uploaded_file):
    """Enregistre un fichier uploadé localement dans le dossier OUTPUT_DIR."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    save_path = os.path.join(OUTPUT_DIR, uploaded_file.name)
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return save_path

@st.cache_data
def read_uploaded_file(file):
    """Lit un fichier CSV, Excel ou JSON et renvoie un DataFrame."""
    try:
        if isinstance(file, str):  # Si c’est un chemin de fichier
            if file.endswith(".csv"):
                return pd.read_csv(file)
            elif file.endswith((".xlsx", ".xls")):
                return pd.read_excel(file)
            elif file.endswith(".json"):
                return pd.read_json(file)
        else:  # Si c’est un fichier uploadé (BytesIO)
            if file.name.endswith(".csv"):
                return pd.read_csv(file)
            elif file.name.endswith((".xlsx", ".xls")):
                return pd.read_excel(file)
            elif file.name.endswith(".json"):
                return pd.read_json(file)
        st.error("Format non supporté.")
        return None
    except Exception as e:
        st.error(f"Erreur lors du chargement du fichier : {e}")
        return None


def go_to_clients():
    """Navigue vers la page clients après vérification de l'entrée utilisateur."""
    user_input = st.session_state.user_input.strip()
    if not user_input:
        st.error("⚠️ Le champ ne doit pas être vide.")
        return

    try:
        st.session_state.client_index = int(user_input)
        st.switch_page("pages/clients.py")
    except ValueError:
        st.error("❌ Veuillez saisir un nombre entier valide pour le numéro du client.")


def switch_page():
    """Déclenché automatiquement lors d’un changement de champ texte."""
    user_input = st.session_state.user_input.strip()
    if not user_input:
        st.session_state.error_msg = "⚠️ Le champ ne doit pas être vide."
        return

    try:
        st.session_state.client_index = int(user_input)
        st.session_state.switch_page_client = True
    except ValueError:
        st.session_state.error_msg = (
            "❌ Veuillez saisir un nombre entier valide pour le numéro du client."
        )


# --- INITIALISATION DES VARIABLES DE SESSION ---
st.session_state.setdefault("user_input", "")
st.session_state.setdefault("client_index", "")
st.session_state.setdefault("data_frame", None)
st.session_state.setdefault("switch_page_client", False)
st.session_state.setdefault("last_uploaded_file", "")
st.session_state.m_messages = []


# --- NAVIGATION AUTOMATIQUE SI DÉCLENCHÉE ---
if st.session_state.switch_page_client:
    st.switch_page("pages/clients.py")

# --- CHARGEMENT DU STYLE ---
load_css(CSS_PATH)

# --- SIDEBAR ---
st.sidebar.image("images/NEURONAIZE-LOGO-BASELINE.png", width="stretch")
st.sidebar.markdown(
    "### ⓘ&nbsp;&nbsp;&nbsp;&nbsp;À propos de nous :", unsafe_allow_html=True
)
st.sidebar.markdown(
    """
    <p style="text-align: justify;">
    Chez NeuronAIze, nous croyons au pouvoir de l’intelligence artificielle pour transformer la donnée brute en connaissance utile et exploitable.
    </p>
    <p style="text-align: justify;">
    Notre mission est de rendre les outils d’IA et d’analyse avancée accessibles aux entreprises et aux organisations, afin de leur permettre de prendre de meilleures décisions, plus rapidement et en toute confiance.
    </p>
    """,
    unsafe_allow_html=True,
)

# --- CONTENU PRINCIPAL ---
st.title("📂 Bienvenue !")
st.write("Veuillez télécharger un fichier (CSV, JSON ou Excel).")

# --- UPLOADER DE FICHIER ---
uploaded_file = st.file_uploader(
    "Glissez-déposez le fichier ici :",
    type=["csv", "json", "xlsx", "xls"],
    help="Formats supportés : CSV, JSON, Excel (.xlsx, .xls).",
)

# --- TRAITEMENT DU FICHIER (AVEC MÉMOIRE) ---
if uploaded_file:
    # Si nouveau fichier différent du précédent, on recharge
    if uploaded_file.name != st.session_state.last_uploaded_file:
        save_uploaded_file(uploaded_file)
        df = read_uploaded_file(uploaded_file)
        if df is not None:
            st.session_state.data_frame = df
            st.session_state.last_uploaded_file = uploaded_file.name
            st.success(f"✅ Nouveau fichier chargé : {uploaded_file.name}")
    else:
        st.success(f"✅ Fichier déjà chargé : {uploaded_file.name}")

if st.session_state.data_frame is None:
    st.info(
        "💡 Aucun fichier chargé. Veuillez en importer un ci-dessus pour commencer."
    )

# --- AFFICHAGE DU DATAFRAME SI DÉJÀ CHARGÉ ---
if st.session_state.data_frame is not None:
    df = st.session_state.data_frame
    st.write("Aperçu des données :")
    st.dataframe(df.head())

    # --- SAISIE DU NUMÉRO DE CLIENT ---
    error_placeholder = st.empty()
    st.text_input(
        "Numéro de client :",
        placeholder="Saisissez le numéro du client pour afficher sa fiche détaillée.",
        key="user_input",
        on_change=switch_page,
    )

    # --- BOUTON D’APPLICATION ---
    col1, col2, col3 = st.columns([5, 1, 2])
    with col3:
        if st.button("Appliquer", use_container_width=True, key="appliquer"):
            go_to_clients()

    # --- MESSAGE D’ERREUR SI NÉCESSAIRE ---
    if "error_msg" in st.session_state and st.session_state.error_msg:
        error_placeholder.error(st.session_state.error_msg)
        st.session_state.error_msg = ""  # reset après affichage
