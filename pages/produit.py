import streamlit as st
import pathlib

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Produit",
    layout="wide",
    page_icon="images/NEURONAIZE-ICONE-BLANC.png",
)
if (
    "produit_page" not in st.session_state
    and "aff_content" not in st.session_state
    and "Advantage" not in st.session_state
    and "Advantage_list" not in st.session_state
    and "cout_list" not in st.session_state
):
    st.switch_page("pages/page_d'accueil.py")
# --- CONSTANTES ---
st.session_state.produit_page = False
CSS_PATH = pathlib.Path("assets/styles.css")
name_of_product = st.session_state.produit
results = "revenu mensuel stable, croissance financière à long terme"
advantages = st.session_state.Advantage
num_TAE = 5.2
num_Investissement = 100000
niv_risque = "Low"
frais = "Low/None"
ai_msg = "Bonjour 👋 Je suis votre assistant. Comment puis-je vous aider aujourd'hui ?"
Advantage_list = st.session_state.Advantage_list
cout_list = st.session_state.cout_list


# --- FONCTIONS UTILITAIRES ---
def load_css(file_path: pathlib.Path):
    """Charge une feuille de style CSS externe."""
    if file_path.exists():
        with open(file_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.warning(f"⚠️ Fichier CSS non trouvé : {file_path}")


def my_text():
    user_input = st.session_state.chat_input
    if user_input and user_input.text:
        st.session_state.m_messages.append(user_input.text)
    if user_input and user_input["files"]:
        st.session_state.m_messages.append(
            {"type": "image", "data": user_input["files"]}
        )


def toggle_eligibilite():
    st.session_state.show_eligibilite = not st.session_state.show_eligibilite


def toggle_Avantages():
    st.session_state.show_Avantages = not st.session_state.show_Avantages


def toggle_Frais_and_coûts():
    st.session_state.show_Frais_and_coûts = not st.session_state.show_Frais_and_coûts


# --- INITIALISATION DES VARIABLES DE SESSION ---
st.session_state.switch_page_produit = False
if "m_messages" not in st.session_state:
    st.session_state.m_messages = []
if "show_eligibilite" not in st.session_state:
    st.session_state.show_eligibilite = True  # Par défaut, masqué
if "show_Avantages" not in st.session_state:
    st.session_state.show_Avantages = True  # Par défaut, masqué
if "show_Frais_and_coûts" not in st.session_state:
    st.session_state.show_Frais_and_coûts = True  # Par défaut, masqué

# --- NAVIGATION AUTOMATIQUE SI DÉCLENCHÉE ---

# --- CHARGEMENT DU STYLE ---
load_css(CSS_PATH)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown(
        """
        <style>
        div[class*="st-key-btn1"] .stButton button {
            width: 100%;
            justify-content: flex-start;
        }
        div[class*="st-key-btn2"] .stButton button {
            width: 100%;
            justify-content: flex-start;
        }
        div[class*="st-key-btn3"] .stButton button {
            width: 100%;
            justify-content: flex-start;
        }
        div[class*="st-key-btn4"] .stButton button {
            width: 100%;
            justify-content: flex-start;
        }
        div[class*="st-key-btn5"] .stButton button {
            justify-content: flex-start;
            width: 100%;
        }         
        </style>
            """,
        unsafe_allow_html=True,
    )
    st.image("images/NEURONAIZE-LOGO-BASELINE.png", width="stretch")
    st.button(
        "Accueil",
        width="stretch",
        icon=":material/home:",
        type="tertiary",
        key="btn1",
    )
    st.button(
        "Comptes",
        width="stretch",
        icon=":material/manage_accounts:",
        type="tertiary",
        key="btn2",
    )
    st.button(
        "Paiements",
        width="stretch",
        icon=":material/payments:",
        type="tertiary",
        key="btn3",
    )
    st.button(
        "Aperçu/Analyse",
        width="stretch",
        icon=":material/area_chart:",
        type="tertiary",
        key="btn4",
    )
    st.button(
        "Produits",
        width="stretch",
        icon=":material/credit_card:",
        type="tertiary",
        key="btn5",
    )

# --- CONTENU PRINCIPAL ---
st.markdown(
    """
        <style>
        section[data-testid="stSidebar"] {
            width: 220px !important;  # Set the desired fixed width
        }
        </style>
        """,
    unsafe_allow_html=True,
)
with st.container(border=True):
    st.markdown(
        f"""
                    <p style='font-family:Arial; font-size:24px; font-weight:bold;'>
                        {name_of_product}
                    </p>
                    """,
        unsafe_allow_html=True,
    )
    st.write(
        "Investissez en toute confiance avec des rendements compétitifs et des avantages précieux."
    )
    col14, col24 = st.columns([1, 1])
    with col14:
        st.markdown(
            f"""
                    <p style='font-family:Arial; font-size:14px; font-weight:bold; margin-left: 50px;'>
                        Points clés :
                    </p>
                    """,
            unsafe_allow_html=True,
        )
        col11, col22 = st.columns([1, 1])
        with col11:
            with st.container(border=True, height="stretch"):
                st.markdown(
                    f"""
                    <p style='font-family:Arial; font-size:12px;'>
                        TAE estimé (%)
                    </p>
                    """,
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f"""
                    <p style='font-family:Arial; font-size:12px; font-weight:bold;'>
                        {num_TAE}
                    </p>
                    """,
                    unsafe_allow_html=True,
                )
            with st.container(border=True, height="stretch"):
                st.markdown(
                    f"""
                    <p style='font-family:Arial; font-size:12px;'>
                        Investissement minimum (DH)
                    </p>
                    """,
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f"""
                    <p style='font-family:Arial; font-size:12px; font-weight:bold;'>
                        {num_Investissement}
                    </p>
                    """,
                    unsafe_allow_html=True,
                )
        with col22:
            with st.container(border=True, height="stretch"):
                st.markdown(
                    f"""
                    <p style='font-family:Arial; font-size:12px;'>
                        Niveau de risque
                    </p>
                    """,
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f"""
                    <p style='font-family:Arial; font-size:14px; font-weight:bold; color: green;'>
                        {niv_risque}
                    </p>
                    """,
                    unsafe_allow_html=True,
                )
            with st.container(border=True, height="stretch"):
                st.markdown(
                    f"""
                    <p style='font-family:Arial; font-size:12px;'>
                        Frais
                    </p>
                    """,
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f"""
                    <p style='font-family:Arial; font-size:12px; font-weight:bold; color: green;'>
                        {frais}
                    </p>
                    """,
                    unsafe_allow_html=True,
                )
    with col24:
        st.markdown(
            f"""
                    <p style='font-family:Arial; font-size:14px; font-weight:bold;'>
                        Pourquoi ce produit est fait pour vous :
                    </p>
                    """,
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""
            <p style='font-family:Arial; font-size:14px; text-align: justify;'>
                En se basant sur votre profil affichant :
                <span style='color:blue; font-weight:bold;'>{results}</span>, 
                <span style='color:blue; font-weight:bold;'>{name_of_product}</span> 
                est une excellente recommandation. Il correspond à vos objectifs en offrant : 
                <span style='color:blue; font-weight:bold;'>{advantages}</span>, 
                tout en vous offrant la flexibilité dont vous avez besoin.
            </p>
            """,
            unsafe_allow_html=True,
        )
        st.button("Voir votre profil complet", type="secondary", key="btn_voir_p")
    st.markdown(
        """
            <hr style="margin-top:5px; margin-bottom:5px;">
        """,
        unsafe_allow_html=True,
    )
    st.button(
        "Avantages",
        icon=":material/workspace_premium:",
        type="tertiary",
        on_click=toggle_Avantages,
    )
    if st.session_state.show_Avantages:
        i = 0
        for ite in Advantage_list:
            if i % 2 == 0:
                cols = st.columns([1, 1])  # crée deux colonnes
                col_dict = {f"col{i}": cols[0], f"col{i+1}": cols[1]}
            with col_dict[f"col{i}"]:
                st.markdown(
                    f"""
                        <p style='font-family:Arial; font-size:12px;margin-left:50px;font-weight:bold;'>
                                    <span style="
                display:inline-block;
                width:7px;
                height:7px;
                background-color:blue;
                margin-right:8px;
                vertical-align:middle;
            "></span>
                            {ite}<br>
            <span style='color:gray; font-weight:bold;margin-left: 20px'>Lorem Ipsum is simply dummy text of the printing and</span><br>
            <span style='color:gray; font-weight:bold;margin-left: 20px'>typesetting industry.</span>
                        </p>
                        """,
                    unsafe_allow_html=True,
                )
            i = i + 1

    st.markdown(
        """
            <hr style="margin-top:5px; margin-bottom:5px;">
        """,
        unsafe_allow_html=True,
    )
    st.button(
        "Frais & coûts",
        icon=":material/point_of_sale:",
        type="tertiary",
        on_click=toggle_Frais_and_coûts,
    )
    if st.session_state.show_Frais_and_coûts:
        i = 0
        for ite in cout_list:
            if i % 2 == 0:
                cols = st.columns([1, 1])  # crée deux colonnes
                col_dict = {f"col{i}": cols[0], f"col{i+1}": cols[1]}
            with col_dict[f"col{i}"]:
                if cout_list[ite]:
                    text_part1 = cout_list[ite]
                    text_part2 = ""
                else:
                    text_part1 = "Lorem Ipsum is simply dummy text of the printing and"
                    text_part2 = "typesetting industry."
                st.markdown(
                    f"""
        <p style='font-family:Arial; font-size:12px;margin-left:50px;font-weight:bold;'>
            <span style="
                display:inline-block;
                width:7px;
                height:7px;
                background-color:blue;
                margin-right:8px;
                vertical-align:middle;
            "></span>
            {ite}<br>
        <span style='color:gray; font-weight:bold;margin-left:20px;'>{text_part1}</span><br>
        <span style='color:gray; font-weight:bold;margin-left:20px;'>{text_part2}</span>
        </p>
        """,
                    unsafe_allow_html=True,
                )

            i = i + 1
    st.markdown(
        """
            <hr style="margin-top:5px; margin-bottom:5px;">
        """,
        unsafe_allow_html=True,
    )
    Éligibilité = st.button(
        "Éligibilité",
        icon=":material/contract:",
        type="tertiary",
        on_click=toggle_eligibilite,
    )
    if st.session_state.show_eligibilite:
        with st.container():
            col13, col23 = st.columns([1, 1])
            with col13:
                st.markdown(
                    f"""
                        <p style='font-family:Arial; font-size:12px;margin-left:50px;font-weight:bold;'>
                                    <span style="
                display:inline-block;
                width:7px;
                height:7px;
                background-color:blue;
                margin-right:8px;
                vertical-align:middle;
            "></span>
                            Citoyen marocain
                        </p>
                        """,
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f"""
                        <p style='font-family:Arial; font-size:12px;margin-left:50px;font-weight:bold;'>
                                    <span style="
                display:inline-block;
                width:7px;
                height:7px;
                background-color:blue;
                margin-right:8px;
                vertical-align:middle;
            "></span>
                            Compte bancaire valide
                        </p>
                        """,
                    unsafe_allow_html=True,
                )
            with col23:
                st.markdown(
                    f"""
                        <p style='font-family:Arial; font-size:12px;margin-left:50px;font-weight:bold;'>
                                    <span style="
                display:inline-block;
                width:7px;
                height:7px;
                background-color:blue;
                margin-right:8px;
                vertical-align:middle;
            "></span>
                            Age 18 +
                        </p>
                        """,
                    unsafe_allow_html=True,
                )

with st.container(border=True):
    st.markdown(
        f"""
                    <p style='font-family:Arial; font-size:24px; font-weight:bold;'>
                        Assistant de chat
                    </p>
                    """,
        unsafe_allow_html=True,
    )
    st.write("Votre guide pour souscrire à ce produit")
    ai_message = st.container(border=True)
    with ai_message:
        #            st.markdown(
        #                f"""
        #                <div style="background-color:lightgray;width:350px;border-radius:20px;padding-left:20px;padding-top:10px;padding-bottom:1px;margin-bottom:10px;text-align : justify;padding-right:20px">
        #                    <p style='font-family:Arial; font-size:12px;'>
        #                    </p>
        #               </div>
        #                    """,
        #                unsafe_allow_html=True,
        #            )
        st.chat_message("assistant").write(ai_msg)
        for msg in st.session_state.m_messages:
            #                    st.markdown(
            #                        f"""
            #                        <div style="background-color:lightblue;width:350px;border-radius:20px;padding-left:20px;padding-top:10px;padding-bottom:1px;margin-bottom:10px;text-align : justify;padding-right:20px;margin-top:15px">
            #                            <p style='font-family:Arial; font-size:12px;'>
            #                            {msg}
            #                            </p>
            #                        </div>
            #                            """,
            #                        unsafe_allow_html=True,
            #                    )
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
    with st.container(border=True):
        st.chat_input(
            "Entrez votre message...",
            accept_file=True,
            file_type=["jpg", "jpeg", "png"],
            key="chat_input",
            on_submit=my_text,
        )
