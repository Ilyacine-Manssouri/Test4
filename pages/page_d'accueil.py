import streamlit as st
import pandas as pd
import pathlib
import os

# --- LANGUE PAR DÉFAUT ---
st.session_state.setdefault("english", True)

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Page d'accueil" if st.session_state.english != True else "Home page",
    layout="wide",
    page_icon="images/NEURONAIZE-ICONE-BLANC.png",
)

# --- CONSTANTES ---
OUTPUT_DIR = "Data/Data_base"
CSS_PATH = pathlib.Path("assets/styles.css")
languages = {
    "EN": {
        "button": "Browse Files",
        "instructions": "Drag and drop files here",
        "limits": "Limit 200MB per file",
    },
    "Fr": {
        "button": "Rechercher",
        "instructions": "Glissez les fichiers ici",
        "limits": "Limite de 200 Mo par fichier",
    },
}


# --- FONCTIONS UTILITAIRES ---
def load_css(file_path: pathlib.Path):
    """Charge une feuille de style CSS externe."""
    if file_path.exists():
        with open(file_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.warning(
            f"⚠️ Fichier CSS non trouvé : {file_path}"
            if st.session_state.english != True
            else f"⚠️ CSS file not found: {file_path}"
        )


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
        st.error(
            "Format non supporté."
            if st.session_state.english != True
            else "Unsupported format."
        )
        return None
    except Exception as e:
        st.error(
            f"Erreur lors du chargement du fichier : {e}"
            if st.session_state.english != True
            else f"Error while loading file: {e}"
        )
        return None


def go_to_clients():
    """Navigue vers la page clients après vérification de l'entrée utilisateur."""
    user_input = st.session_state.user_input.strip()
    if not user_input:
        st.error(
            "⚠️ Le champ ne doit pas être vide."
            if st.session_state.english != True
            else "⚠️ The field cannot be empty."
        )
        return
    try:
        if st.session_state.client_index != int(user_input):
            st.session_state.client_index = int(user_input)
            st.session_state["switch_page_home"] = False
            st.session_state.aff_content = False
            st.session_state.switch_page_client = True
        else:
            st.session_state["switch_page_home"] = False
            st.session_state.switch_page_client = True
    except ValueError:
        st.error(
            "❌ Veuillez saisir un nombre entier valide pour le numéro du client."
            if st.session_state.english != True
            else "❌ Please enter a valid integer for the client number."
        )


def t(fr, en):
    """Renvoie fr ou en selon la langue choisie"""
    return en if st.session_state.english else fr


def switch_page():
    """Déclenché automatiquement lors d’un changement de champ texte."""
    user_input = st.session_state.user_input.strip()
    if not user_input:
        st.session_state.error_msg = (
            "⚠️ Le champ ne doit pas être vide."
            if st.session_state.english != True
            else "⚠️ The field cannot be empty."
        )
        return
    try:
        if st.session_state.client_index != int(user_input):
            st.session_state.client_index = int(user_input)
            st.session_state.aff_content = False
            st.session_state.process_done = False
            st.session_state.switch_page_client = True
        else:
            st.session_state.switch_page_client = True
    except ValueError:
        st.session_state.error_msg = (
            "❌ Veuillez saisir un nombre entier valide pour le numéro du client."
            if st.session_state.english != True
            else "❌ Please enter a valid integer for the client number."
        )


def switch_lang_en():
    st.session_state.english = not st.session_state.english


def my_text():
    user_input = st.session_state.chat_input
    if user_input and user_input.text:
        st.session_state.my_messages.append(user_input.text)
    if user_input and user_input["files"]:
        st.session_state.my_messages.append(
            {"type": "image", "data": user_input["files"]}
        )


def clear_msg():
    st.session_state.my_messages = []


ai_msg = t(
    "Bonjour 👋 Je suis votre assistant. Comment puis-je vous aider aujourd'hui ?",
    "Hello 👋 I’m your assistant. How can I help you today?",
)

# --- INITIALISATION DES VARIABLES DE SESSION ---
st.session_state["switch_page_home"] = False
st.session_state.setdefault("user_input", "")
st.session_state.setdefault("client_index", "")
st.session_state.setdefault("data_frame", None)
st.session_state.setdefault("switch_page_client", False)
st.session_state.setdefault("last_uploaded_file", "")
st.session_state.setdefault("process_done", None)
st.session_state.m_messages = []
st.session_state.setdefault("my_messages", [])


# --- NAVIGATION AUTOMATIQUE SI DÉCLENCHÉE ---
if st.session_state.switch_page_client:
    st.switch_page("pages/clients.py")


# --- CHARGEMENT DU STYLE ---
load_css(CSS_PATH)


# --- SIDEBAR ---
text3 = (
    "### ⓘ&nbsp;&nbsp;&nbsp;&nbsp;À propos de nous :"
    if st.session_state.english != True
    else "### ⓘ&nbsp;&nbsp;&nbsp;&nbsp;About us:"
)
st.sidebar.image("images/NEURONAIZE-LOGO-BASELINE.png", width="stretch")
st.sidebar.markdown(text3, unsafe_allow_html=True)

text1 = (
    "Chez NeuronAIze, nous croyons au pouvoir de l’intelligence artificielle pour transformer la donnée brute en connaissance utile et exploitable."
    if st.session_state.english != True
    else "At NeuronAIze, we believe in the power of artificial intelligence to transform raw data into useful and actionable knowledge."
)
text2 = (
    "Notre mission est de rendre les outils d’IA et d’analyse avancée accessibles aux entreprises et aux organisations, afin de leur permettre de prendre de meilleures décisions, plus rapidement et en toute confiance."
    if st.session_state.english != True
    else "Our mission is to make AI and advanced analytics tools accessible to businesses and organizations, empowering them to make better decisions — faster and with confidence."
)

st.sidebar.markdown(
    f"""
    <p style="text-align: justify;">
    {text1}
    </p>
    <p style="text-align: justify;">
    {text2}
    </p>
    """,
    unsafe_allow_html=True,
)


# --- CONTENU PRINCIPAL ---
st.markdown(
    """
        <style>
        section[data-testid="stSidebar"] {
            width: 300px !important;  # Set the desired fixed width
        }
        </style>
        """,
    unsafe_allow_html=True,
)

col11, col22 = st.columns([10, 1])
with col11:
    st.title("📂 Bienvenue !" if st.session_state.english != True else "📂 Welcome!")
    st.write(
        "Veuillez télécharger un fichier (CSV, JSON ou Excel)."
        if st.session_state.english != True
        else "Please upload a file (CSV, JSON, or Excel)."
    )
with col22:
    st.button(
        "Anglais" if st.session_state.english != True else "French",
        key="btn_en",
        on_click=switch_lang_en,
        help=(
            "Cliquer ici pour changer la langue en anglais"
            if st.session_state.english != True
            else "Click here to change the language to French"
        ),
        width="stretch",
    )
# --- UPLOADER DE FICHIER ---
if not st.session_state.english:
    custom_css = """
    <style>

    /* 2) Replace the "Drag and drop file here" visible text */
    div[data-testid="stFileUploader"] div[data-testid="stFileUploaderDropzoneInstructions"] .st-emotion-cache-kt79cc > span:first-child {
        visibility: hidden !important;
    }
    div[data-testid="stFileUploader"] label[data-testid="stWidgetLabel"] {
        margin-top: -16px !important; /* tweak this value */
    }
    div[data-testid="stFileUploader"] div[data-testid="stFileUploaderDropzoneInstructions"] .st-emotion-cache-kt79cc > span:first-child::after {
        content: "Glissez le fichier ici";
        visibility: visible !important;
        font-size: 1rem;
        display: flex;
        justify-content: flex-start;
        margin-top: -25px;
    }
    /* Texte de limite : "Limit 200MB per file..." */
    div[data-testid="stFileUploaderDropzoneInstructions"] > div > span:last-child {
        visibility: hidden !important;
    }
    div[data-testid="stFileUploader"] div[data-testid="stFileUploaderDropzoneInstructions"] .st-emotion-cache-kt79cc > span:nth-child(2)::after {
        content: "fichier • CSV, JSON, XLSX, XLS";
        visibility: visible !important;
        display: flex;
        justify-content: flex-start;
        font-size: 0.85rem;
        margin-top: -22px;
    }
    /* 4) Replace the "Browse files" button text
    Hide the original text, then place our own via ::after on the button. */
    div[data-testid="stFileUploader"] span[class*="epvm6"] button[data-testid="stBaseButton-secondary"] {
        color: transparent !important;        /* hide original text */
        position: relative !important;
    }
    div[data-testid="stFileUploader"] span[class*="epvm6"] button[data-testid="stBaseButton-secondary"]::after {
        content: "Parcourir";
        position: absolute;
        color: black;
        font-weight: 400;
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)
else:
    custom_css = """
    <style>
    div[data-testid="stFileUploader"] label[data-testid="stWidgetLabel"] {
        margin-top: -16px !important; /* tweak this value */
    }
    /* Texte de limite : "Limit 200MB per file..." */
    div[data-testid="stFileUploaderDropzoneInstructions"] > div > span:last-child {
        visibility: hidden !important;
    }
    div[data-testid="stFileUploader"] div[data-testid="stFileUploaderDropzoneInstructions"] .st-emotion-cache-kt79cc > span:nth-child(2)::after {
        content: "file • CSV, JSON, XLSX, XLS";
        visibility: visible !important;
        display: flex;
        justify-content: flex-start;
        font-size: 0.85rem;
        margin-top: -22px;
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)


uploaded_file = st.file_uploader(
    (
        "Glissez-déposez le fichier ici :"
        if st.session_state.english != True
        else "Drag and drop your file here:"
    ),
    type=["csv", "json", "xlsx", "xls"],
    help=(
        "Formats supportés : CSV, JSON, Excel (.xlsx, .xls)."
        if st.session_state.english != True
        else "Supported formats: CSV, JSON, Excel (.xlsx, .xls)."
    ),
)


# --- TRAITEMENT DU FICHIER (AVEC MÉMOIRE) ---
if uploaded_file:
    if uploaded_file.name != st.session_state.last_uploaded_file:
        save_uploaded_file(uploaded_file)
        df = read_uploaded_file(uploaded_file)
        if df is not None:
            st.session_state.data_frame = df
            st.session_state.last_uploaded_file = uploaded_file.name
            st.success(
                f"✅ Nouveau fichier chargé : {uploaded_file.name}"
                if st.session_state.english != True
                else f"✅ New file loaded: {uploaded_file.name}"
            )
    else:
        st.success(
            f"✅ Fichier déjà chargé : {uploaded_file.name}"
            if st.session_state.english != True
            else f"✅ File already loaded: {uploaded_file.name}"
        )

if st.session_state.data_frame is None:
    st.info(
        "💡 &nbsp;Aucun fichier chargé. Veuillez en importer un ci-dessus pour commencer."
        if st.session_state.english != True
        else "💡 &nbsp;No file loaded. Please upload one above to get started."
    )

# --- AFFICHAGE DU DATAFRAME SI DÉJÀ CHARGÉ ---
if st.session_state.data_frame is not None:
    df = st.session_state.data_frame
    st.write(
        "Aperçu des données :" if st.session_state.english != True else "Data preview:"
    )
    st.dataframe(df.head())

    error_placeholder = st.empty()
    st.text_input(
        "Numéro de client :" if st.session_state.english != True else "Client number:",
        placeholder=(
            "Saisissez le numéro du client pour afficher sa fiche détaillée."
            if st.session_state.english != True
            else "Enter the client number to display their detailed profile."
        ),
        key="user_input",
        on_change=switch_page,
    )

    col1, col2, col3 = st.columns([5, 1, 2])
    with col3:
        if st.button(
            "Appliquer" if st.session_state.english != True else "Apply",
            use_container_width=True,
            key="appliquer",
        ):
            go_to_clients()

    if "error_msg" in st.session_state and st.session_state.error_msg:
        error_placeholder.error(st.session_state.error_msg)
        st.session_state.error_msg = ""  # reset après affichage

with st.popover(
    "Ask Ai" if st.session_state.english == True else "Demander à l’IA",
    icon=":material/smart_toy:",
):
    st.write(
        t(
            "Votre guide pour souscrire à ce produit",
            "Your guide to subscribing to this product",
        )
    )
    ai_message = (
        st.container(border=True, height="content")
        if st.session_state["my_messages"] == []
        else st.container(border=True, height=250)
    )
    with ai_message:
        st.chat_message("assistant").write(ai_msg)
        for msg in st.session_state.my_messages:
            if isinstance(msg, str):
                st.chat_message("user").write(msg)
                st.chat_message("assistant").write(msg)
            if isinstance(msg, dict) and msg.get("type") == "image":
                with st.chat_message("user"):
                    st.image(
                        msg["data"],
                        width="content",
                    )
                with st.chat_message("assistant"):
                    st.image(
                        msg["data"],
                        width="content",
                    )
    st.chat_input(
        t("Entrez votre message...", "Enter your message..."),
        accept_file=True,
        file_type=["jpg", "jpeg", "png"],
        key="chat_input",
        on_submit=my_text,
    )
