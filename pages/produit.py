import streamlit as st
import pathlib

if (
    "produit_page" not in st.session_state
    or "aff_content" not in st.session_state
    or "Advantage" not in st.session_state
    or "Advantage_list" not in st.session_state
    or "cout_list" not in st.session_state
    or "english" not in st.session_state
):
    st.switch_page("pages/page_d'accueil.py")


def t(fr, en):
    """Renvoie fr ou en selon la langue choisie"""
    return en if st.session_state.english else fr


# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title=t("Produit", "Product"),
    layout="wide",
    page_icon="images/NEURONAIZE-ICONE-BLANC.png",
)

# --- CONSTANTES ---
st.session_state.produit_page = False
CSS_PATH = pathlib.Path("assets/styles.css")
name_of_product = st.session_state.produit
results = t(
    "revenu mensuel stable, croissance financière à long terme",
    "stable monthly income, long-term financial growth",
)
advantages = st.session_state.Advantage
num_TAE = 5.2
num_Investissement = 100000
niv_risque = t("faible", "Low")
frais = t("Faible/Aucun", "Low/None")
ai_msg = t(
    "Bonjour 👋 Je suis votre assistant. Comment puis-je vous aider aujourd'hui ?",
    "Hello 👋 I’m your assistant. How can I help you today?",
)
Advantage_list = st.session_state.Advantage_list
cout_list = st.session_state.cout_list


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


def switch_page_home():
    st.session_state["switch_page_home"] = True


def switch_page_client():
    st.session_state.switch_page_client = True


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
if st.session_state["switch_page_home"] == True:
    st.switch_page("pages/page_d'accueil.py")
if st.session_state["switch_page_client"] == True:
    st.switch_page("pages/clients.py")


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
        t("Accueil", "Home"),
        width="stretch",
        icon=":material/home:",
        type="tertiary",
        key="btn1",
        on_click=switch_page_home,
    )
    st.button(
        t("Comptes", "Accounts"),
        width="stretch",
        icon=":material/manage_accounts:",
        type="tertiary",
        key="btn2",
    )
    st.button(
        t("Paiements", "Payments"),
        width="stretch",
        icon=":material/payments:",
        type="tertiary",
        key="btn3",
    )
    st.button(
        t("Aperçu / Analyse", "Overview / Analysis"),
        width="stretch",
        icon=":material/area_chart:",
        type="tertiary",
        key="btn4",
        on_click=switch_page_client,
    )
    st.button(
        t("Produits", "Products"),
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
        t(
            "Investissez en toute confiance avec des rendements compétitifs et des avantages précieux.",
            "Invest with confidence, enjoying competitive returns and valuable benefits.",
        )
    )
    col14, col24 = st.columns([1, 1])
    with col14:
        text_part3 = t("Points clés :", "Key points :")
        st.markdown(
            f"""
                    <p style='font-family:Arial; font-size:14px; font-weight:bold; margin-left: 50px;'>
                        {text_part3}
                    </p>
                    """,
            unsafe_allow_html=True,
        )
        col11, col22 = st.columns([1, 1])
        with col11:
            text_part4 = t("TAE estimé (%)", "Estimated APR (%)")
            with st.container(border=True, height="stretch"):
                st.markdown(
                    f"""
                    <p style='font-family:Arial; font-size:12px;'>
                        {text_part4}
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
                text_part12 = t("Investissement minimum (DH)","Minimum investment (MAD)")
                st.markdown(
                    f"""
                    <p style='font-family:Arial; font-size:12px;'>
                        {text_part12}
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
                text_part5 = t("Niveau de risque", "Risk level")
                st.markdown(
                    f"""
                    <p style='font-family:Arial; font-size:12px;'>
                        {text_part5}
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
                text_part6 = t("Frais", "Fees")
                st.markdown(
                    f"""
                    <p style='font-family:Arial; font-size:12px;'>
                        {text_part6}
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
        text_part7 = t(
            "Pourquoi ce produit est fait pour vous :",
            "Why this product is right for you :",
        )
        text_part13 = t("En se basant sur votre profil affichant :","Based on your profile showing :")
        text_part14 = t("est une excellente recommandation. Il correspond à vos objectifs en offrant :","is an excellent recommendation. It aligns with your goals by offering :")
        text_part15 = t("tout en vous offrant la flexibilité dont vous avez besoin.","while providing you with the flexibility you need.")
        st.markdown(
            f"""
                    <p style='font-family:Arial; font-size:14px; font-weight:bold;'>
                        {text_part7}
                    </p>
                    """,
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""
            <p style='font-family:Arial; font-size:14px; text-align: justify;'>
                {text_part13}
                <span style='color:blue; font-weight:bold;'>{results}</span>, 
                <span style='color:blue; font-weight:bold;'>{name_of_product}</span> 
                {text_part14}
                <span style='color:blue; font-weight:bold;'>{advantages}</span>, 
                {text_part15}
            </p>
            """,
            unsafe_allow_html=True,
        )
        st.button(t("Voir votre profil complet","View your full profile"), type="secondary", key="btn_voir_p")
    st.markdown(
        """
            <hr style="margin-top:5px; margin-bottom:5px;">
        """,
        unsafe_allow_html=True,
    )
    st.button(
        t("Avantages","Benefits"),
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
        t("Frais & coûts","Fees & Costs"),
        icon=":material/point_of_sale:",
        type="tertiary",
        on_click=toggle_Frais_and_coûts,
    )
    if st.session_state.show_Frais_and_coûts:
        i = 0
        for ite, valeur in cout_list.items():
            if i % 2 == 0:
                cols = st.columns([1, 1])  # crée deux colonnes
                col_dict = {f"col{i}": cols[0], f"col{i+1}": cols[1]}
            with col_dict[f"col{i}"]:
                if valeur and valeur.strip() != "":
                    text_part1 = valeur
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
        t("Éligibilité","Eligibility"),
        icon=":material/contract:",
        type="tertiary",
        on_click=toggle_eligibilite,
    )
    if st.session_state.show_eligibilite:
        with st.container():
            col13, col23 = st.columns([1, 1])
            with col13:
                text_part8 = t("Citoyen marocain","Moroccan citizen")
                text_part9 = t("Compte bancaire valide","Valid bank account")
                text_part10 = t("Âge 18 +","Age 18 +")
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
                            {text_part8}
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
                            {text_part9}
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
                            {text_part10}
                        </p>
                        """,
                    unsafe_allow_html=True,
                )

with st.container(border=True):
    text_part11 = t("Assistant de chat","Chat assistant")
    st.markdown(
        f"""
                    <p style='font-family:Arial; font-size:24px; font-weight:bold;'>
                        {text_part11}
                    </p>
                    """,
        unsafe_allow_html=True,
    )
    st.write(t("Votre guide pour souscrire à ce produit","Your guide to subscribing to this product"))
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
            t("Entrez votre message...","Enter your message..."),
            accept_file=True,
            file_type=["jpg", "jpeg", "png"],
            key="chat_input",
            on_submit=my_text,
        )
