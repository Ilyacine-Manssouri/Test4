import streamlit as st
import pandas as pd

# import matplotlib.pyplot as plt
# import plotly.figure_factory as ff
import plotly.graph_objects as go  # pour créer le graphique mensuel

# from numpy.random import default_rng as rng
import numpy as np
import subprocess
import json
import os
import pathlib
import sys


# @st.cache_data
# def get_cached_data():
#    return st.session_state.get("data_frame"), st.session_state.get("client_index")
# df, client_index = get_cached_data()
# if df is None or client_index is None:
#    st.warning("⚠️ Données manquantes, retournez à la page précédente.")
#    st.image("images/no_session_found.png", width="content")
#    st.stop()

if (
    "data_frame" not in st.session_state
    or "client_index" not in st.session_state
    or "english" not in st.session_state
):
    st.switch_page("pages/page_d'accueil.py")

if st.session_state.client_index == "":
    st.switch_page("pages/page_d'accueil.py")


def t(fr, en):
    """Renvoie fr ou en selon la langue choisie"""
    return en if st.session_state.english else fr


# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Clients" if st.session_state.english != True else "Customers",
    layout="wide",
    page_icon="images/NEURONAIZE-ICONE-BLANC.png",
)

# --- CONSTANTES ---
text_6 = "Adéquation (%) :" if st.session_state.english != True else "Suitability (%) :"
CSS_PATH = pathlib.Path("assets/styles.css")
df = st.session_state.data_frame
client_index = int(st.session_state.client_index)
categories_fr = {
    "Comptes": [
        "Produit - Compte chèque en DH",
        "Produit - Compte chèque en devises",
        "Produit - Compte sur carnet",
        "Produit - Compte à terme",
    ],
    "Cartes": [
        "Produit - Carte basique",
        "Produit - Carte Visa",
        "Produit - Carte Visa Premium",
        "Produit - Carte Visa Elite",
        "Produit - Carte Visa Infinite",
    ],
    "Financement immobilier": [
        "Produit - Crédit Immo avec garantie hypothécaire",
        "Produit - Crédit Immo avec garantie liquide",
        "Produit - Crédit Immo avec remboursement in fine",
        "Produit - Crédit Immo subventionné",
    ],
    "Financement à la consommation": [
        "Produit - Crédit à la consommation non affecté",
        "Produit - Crédit Auto",
        "Produit - Découvert",
    ],
    "Assurance": [
        "Produit - Assurance décès invalidité adossée à un financement",
        "Produit - Assurance décès toutes causes",
        "Produit - Multirisques bâtiment",
        "Produit - Maladie complémentaire",
    ],
    "Retraite & Prévoyance": [
        "Produit - Retraite complémentaire",
        "Produit - Retraite complémentaire en UC",
    ],
    "Épargne & Placement": [
        "Produit - Épargne Éducation",
        "Produit - Épargne Logement",
        "Produit - OPCVM monétaires",
        "Produit - OPCVM obligataires",
        "Produit - OPCVM diversifiés",
        "Produit - OPCVM actions",
    ],
    "Packs bancaires": [
        "Produit - Pack bancaire basique",
        "Produit - Pack bancaire étoffé",
    ],
}

categories_eng = {
    "Comptes": [
        "Product - Checking account in MAD",
        "Product - Checking account in foreign currency",
        "Product - Savings account",
        "Product - Term deposit account",
    ],
    "Cartes": [
        "Product - Basic card",
        "Product - Visa card",
        "Product - Visa Premium card",
        "Product - Visa Elite card",
        "Product - Visa Infinite card",
    ],
    "Financement immobilier": [
        "Product - Mortgage loan with real estate guarantee",
        "Product - Mortgage loan with cash guarantee",
        "Product - Mortgage loan with bullet repayment",
        "Product - Subsidized mortgage loan",
    ],
    "Financement à la consommation": [
        "Product - Unsecured consumer loan",
        "Product - Auto loan",
        "Product - Overdraft facility",
    ],
    "Assurance": [
        "Product - Death and disability insurance linked to a loan",
        "Product - All-cause death insurance",
        "Product - Multi-risk building insurance",
        "Product - Supplementary health insurance",
    ],
    "Retraite & Prévoyance": [
        "Product - Supplementary retirement plan",
        "Product - Unit-linked supplementary retirement plan",
    ],
    "Épargne & Placement": [
        "Product - Education savings plan",
        "Product - Housing savings plan",
        "Product - Money market mutual fund (OPCVM)",
        "Product - Bond mutual fund (OPCVM)",
        "Product - Diversified mutual fund (OPCVM)",
        "Product - Equity mutual fund (OPCVM)",
    ],
    "Packs bancaires": [
        "Product - Basic banking package",
        "Product - Enhanced banking package",
    ],
}

C = "Comptes" if st.session_state.english != True else "Accounts"
Ca = "Cartes" if st.session_state.english != True else "Cards"
F = (
    "Financement immobilier"
    if st.session_state.english != True
    else "Real estate financing"
)
Fi = (
    "Financement à la consommation"
    if st.session_state.english != True
    else "Consumer financing"
)
A = "Assurance" if st.session_state.english != True else "Insurance"
R = (
    "Retraite & Prévoyance"
    if st.session_state.english != True
    else "Retirement & Provident plans"
)
E = (
    "Épargne & Placement"
    if st.session_state.english != True
    else "Savings & Investment"
)
P = "Packs bancaires" if st.session_state.english != True else "Banking packages"

local_recommendations_comptes_categorie = {}
local_recommendations_cartes_categorie = {}
local_recommendations_financement_immobilier_categorie = {}
local_recommendations_financement_à_la_consommation_categorie = {}
local_recommendations_assurance_categorie = {}
local_recommendations_retraite_et_prévoyance_categorie = {}
local_recommendations_epargne_et_placement_categorie = {}
local_recommendations_packs_bancaires_categorie = {}
local_recommendations = {
    C: local_recommendations_comptes_categorie,
    Ca: local_recommendations_cartes_categorie,
    F: local_recommendations_financement_immobilier_categorie,
    Fi: local_recommendations_financement_à_la_consommation_categorie,
    A: local_recommendations_assurance_categorie,
    R: local_recommendations_retraite_et_prévoyance_categorie,
    E: local_recommendations_epargne_et_placement_categorie,
    P: local_recommendations_packs_bancaires_categorie,
}

expert_recommendations_comptes_categorie = []
expert_recommendations_cartes_categorie = []
expert_recommendations_financement_immobilier_categorie = []
expert_recommendations_financement_à_la_consommation_categorie = []
expert_recommendations_assurance_categorie = []
expert_recommendations_retraite_et_prévoyance_categorie = []
expert_recommendations_epargne_et_placement_categorie = []
expert_recommendations_packs_bancaires_categorie = []
expert_recommendations = {
    C: expert_recommendations_comptes_categorie,
    Ca: expert_recommendations_cartes_categorie,
    F: expert_recommendations_financement_immobilier_categorie,
    Fi: expert_recommendations_financement_à_la_consommation_categorie,
    A: expert_recommendations_assurance_categorie,
    R: expert_recommendations_retraite_et_prévoyance_categorie,
    E: expert_recommendations_epargne_et_placement_categorie,
    P: expert_recommendations_packs_bancaires_categorie,
}

meta_recommendations_comptes_categorie = {}
meta_recommendations_cartes_categorie = {}
meta_recommendations_financement_immobilier_categorie = {}
meta_recommendations_financement_à_la_consommation_categorie = {}
meta_recommendations_assurance_categorie = {}
meta_recommendations_retraite_et_prévoyance_categorie = {}
meta_recommendations_epargne_et_placement_categorie = {}
meta_recommendations_packs_bancaires_categorie = {}
meta_recommendations = {
    C: meta_recommendations_comptes_categorie,
    Ca: meta_recommendations_cartes_categorie,
    F: meta_recommendations_financement_immobilier_categorie,
    Fi: meta_recommendations_financement_à_la_consommation_categorie,
    A: meta_recommendations_assurance_categorie,
    R: meta_recommendations_retraite_et_prévoyance_categorie,
    E: meta_recommendations_epargne_et_placement_categorie,
    P: meta_recommendations_packs_bancaires_categorie,
}

Compte_chèque_en_DH = (
    "Compte courant en dirhams marocains pour gérer les opérations quotidiennes."
    if st.session_state.english != True
    else "Current account in Moroccan dirhams for managing daily transactions."
)
Compte_chèque_en_devises = (
    "Compte courant en devises étrangères pour les opérations internationales."
    if st.session_state.english != True
    else "Foreign currency current account for international transactions."
)
Compte_sur_carnet = (
    "Compte épargne rémunéré avec carnet pour suivre les dépôts et retraits."
    if st.session_state.english != True
    else "Interest-bearing savings account with a booklet to track deposits and withdrawals."
)
Compte_à_terme = (
    "Compte bloqué sur une durée déterminée avec intérêt garanti."
    if st.session_state.english != True
    else "Fixed-term account with guaranteed interest over a set period."
)
Carte_basique = (
    "Carte bancaire simple pour retrait et paiement au quotidien."
    if st.session_state.english != True
    else "Basic bank card for everyday withdrawals and payments."
)
Carte_Visa = (
    "Carte de paiement internationale pour achats et retraits."
    if st.session_state.english != True
    else "International payment card for purchases and withdrawals."
)
Carte_Visa_Premium = (
    "Carte offrant plus de services : assurances voyage, bonus points."
    if st.session_state.english != True
    else "Card offering extra services: travel insurance, bonus points."
)
Carte_Visa_Elite = (
    "Carte haut de gamme avec services premium et programmes de fidélité."
    if st.session_state.english != True
    else "High-end card with premium services and loyalty programs."
)
Carte_Visa_Infinite = (
    "Carte très haut de gamme avec services exclusifs."
    if st.session_state.english != True
    else "Ultra-premium card with exclusive services."
)
Crédit_Immo_avec_garantie_hypothécaire = (
    "Prêt immobilier garanti par hypothèque sur le bien."
    if st.session_state.english != True
    else "Mortgage loan secured by property."
)
Crédit_Immo_avec_garantie_liquide = (
    "Prêt immobilier garanti par un dépôt de fonds liquide."
    if st.session_state.english != True
    else "Mortgage loan secured by a cash deposit."
)
Crédit_Immo_avec_remboursement_in_fine = (
    "Prêt remboursé en une seule fois à échéance finale."
    if st.session_state.english != True
    else "Loan repaid in a single payment at maturity."
)
Crédit_Immo_subventionné = (
    "Prêt bénéficiant de taux réduits par l’État ou organisme."
    if st.session_state.english != True
    else "Loan benefiting from reduced interest rates by the state or institution."
)
Crédit_à_la_consommation_non_affecté = (
    "Prêt personnel sans justificatif d’utilisation."
    if st.session_state.english != True
    else "Personal loan with no specific purpose required."
)
Crédit_Auto = (
    "Prêt dédié à l’achat de véhicule neuf ou d’occasion."
    if st.session_state.english != True
    else "Loan dedicated to purchasing a new or used vehicle."
)
Découvert = (
    "Facilite le paiement en cas de manque temporaire de liquidité."
    if st.session_state.english != True
    else "Allows payments in case of temporary lack of funds."
)
Assurance_décès_invalidité_adossée_à_un_financement = (
    "Protection du prêt en cas de décès ou invalidité."
    if st.session_state.english != True
    else "Loan protection in case of death or disability."
)
Assurance_décès_toutes_causes = (
    "Protection financière en cas de décès."
    if st.session_state.english != True
    else "Financial protection in the event of death."
)
Multirisques_bâtiment = (
    "Assurance habitation couvrant incendie, dégâts, vol."
    if st.session_state.english != True
    else "Home insurance covering fire, damage, and theft."
)
Maladie_complémentaire = (
    "Couverture santé complémentaire aux remboursements CNOPS/CNSS."
    if st.session_state.english != True
    else "Health coverage supplementing CNOPS/CNSS reimbursements."
)
Retraite_complémentaire = (
    "Plan épargne retraite pour compléter la pension publique."
    if st.session_state.english != True
    else "Retirement savings plan to supplement the public pension."
)
Retraite_complémentaire_en_UC = (
    "Retraite complémentaire investie en unités de compte (fonds actions/obligations)."
    if st.session_state.english != True
    else "Supplementary retirement plan invested in unit-linked funds (stocks/bonds)."
)
Épargne_Éducation = (
    "Plan d’épargne pour financer études des enfants."
    if st.session_state.english != True
    else "Savings plan to fund children’s education."
)
Épargne_Logement = (
    "Épargne destinée à l’achat immobilier futur."
    if st.session_state.english != True
    else "Savings intended for a future property purchase."
)
OPCVM_monétaires = (
    "Fonds investissant en liquidités et titres court terme."
    if st.session_state.english != True
    else "Funds investing in cash and short-term securities."
)
OPCVM_obligataires = (
    "Fonds investissant en obligations, faible risque."
    if st.session_state.english != True
    else "Funds investing in bonds with low risk."
)
OPCVM_diversifiés = (
    "Fonds combinant actions et obligations pour diversification."
    if st.session_state.english != True
    else "Funds combining stocks and bonds for diversification."
)
OPCVM_actions = (
    "Fonds investissant majoritairement en actions, risque plus élevé."
    if st.session_state.english != True
    else "Funds investing mainly in stocks with higher risk."
)
Pack_bancaire_basique = (
    "Ensemble de services bancaires standard (compte courant, carte)."
    if st.session_state.english != True
    else "Standard banking services package (current account, card)."
)
Pack_bancaire_étoffé = (
    "Pack complet incluant cartes premium, épargne et assurances."
    if st.session_state.english != True
    else "Comprehensive package including premium cards, savings, and insurance."
)

value_1 = df["Produit - Compte chèque en DH"].iat[client_index] != 0
value_2 = df["Produit - Compte chèque en devises"].iat[client_index] != 0
value_3 = df["Produit - Compte sur carnet"].iat[client_index] != 0
value_4 = df["Produit - Compte à terme"].iat[client_index] != 0
value_5 = df["Produit - Carte basique"].iat[client_index] != 0
value_6 = df["Produit - Carte Visa"].iat[client_index] != 0
value_7 = df["Produit - Carte Visa Premium"].iat[client_index] != 0
value_8 = df["Produit - Carte Visa Elite"].iat[client_index] != 0
value_9 = df["Produit - Carte Visa Infinite"].iat[client_index] != 0
value_10 = df["Produit - Crédit Immo avec garantie hypothécaire"].iat[client_index] != 0
value_11 = df["Produit - Crédit Immo avec garantie liquide"].iat[client_index] != 0
value_12 = df["Produit - Crédit Immo avec remboursement in fine"].iat[client_index] != 0
value_13 = df["Produit - Crédit à la consommation non affecté"].iat[client_index] != 0
value_14 = df["Produit - Crédit Auto"].iat[client_index] != 0
value_15 = df["Propriétaire"].iat[client_index] != 0
total_income = (
    df["Revenu annuel"].iat[client_index]
    + df["Montant mouvements créditeurs"].iat[client_index]
)
total_expenses = (
    df["Montant mouvements débiteurs"].iat[client_index]
    + df["Montant transactions carte (national)"].iat[client_index]
    + df["Montant transactions carte (international)"].iat[client_index]
)
current_net_worth = total_income - total_expenses

months = [
    "Jan" if st.session_state.english != True else "Jan",
    "Fév" if st.session_state.english != True else "Feb",
    "Mar" if st.session_state.english != True else "Mar",
    "Avr" if st.session_state.english != True else "Apr",
    "Mai" if st.session_state.english != True else "May",
    "Jun" if st.session_state.english != True else "Jun",
    "Jul" if st.session_state.english != True else "Jul",
    "Aoû" if st.session_state.english != True else "Aug",
    "Sep" if st.session_state.english != True else "Sep",
    "Oct" if st.session_state.english != True else "Oct",
    "Nov" if st.session_state.english != True else "Nov",
    "Déc" if st.session_state.english != True else "Dec",
]

# Exemple : générer des variations mensuelles à partir du total annuel pour que chaque client ait des valeurs différentes mais reproductibles
np.random.seed(client_index)

# Générer revenus et dépenses mensuels autour de la moyenne
monthly_income = np.random.normal(
    loc=(
        df["Revenu annuel"].iat[client_index]
        + df["Montant mouvements créditeurs"].iat[client_index]
    )
    / 12,
    scale=(
        df["Revenu annuel"].iat[client_index]
        + df["Montant mouvements créditeurs"].iat[client_index]
    )
    * 0.1,
    size=12,
)
monthly_expenses = np.random.normal(
    loc=(
        df["Montant mouvements débiteurs"].iat[client_index]
        + df["Montant transactions carte (national)"].iat[client_index]
        + df["Montant transactions carte (international)"].iat[client_index]
    )
    / 12,
    scale=(
        df["Montant mouvements débiteurs"].iat[client_index]
        + df["Montant transactions carte (national)"].iat[client_index]
        + df["Montant transactions carte (international)"].iat[client_index]
    )
    * 0.1,
    size=12,
)

# S'assurer que toutes les valeurs sont strictement supérieures à 0
monthly_income = np.clip(monthly_income, 2000, None)
monthly_expenses = np.clip(monthly_expenses, 2000, None)

monthly_data = pd.DataFrame(
    {"Income": monthly_income, "Expenses": monthly_expenses}, index=months
)

local_recommendations_output_file = "Data/results/local_recommendations.json"
meta_recommendations_output_file = "Data/results/meta_recommendations.json"
expert_recommendations_output_file = "Data/results/expert_recommendations.json"

Advantages_Compte_chèque_en_DH = [
    (
        "Gestion facile des paiements"
        if st.session_state.english != True
        else "Easy payment management"
    ),
    (
        "Virements et retraits"
        if st.session_state.english != True
        else "Transfers and withdrawals"
    ),
    (
        "Carte bancaire associée"
        if st.session_state.english != True
        else "Linked bank card"
    ),
]

Advantages_Compte_chèque_en_devises = [
    (
        "Facilite les transactions internationales"
        if st.session_state.english != True
        else "Facilitates international transactions"
    ),
    (
        "Convertibilité rapide"
        if st.session_state.english != True
        else "Quick convertibility"
    ),
]

Advantages_Compte_sur_carnet = [
    (
        "Rendement sur les dépôts"
        if st.session_state.english != True
        else "Return on deposits"
    ),
    (
        "Flexibilité de retrait"
        if st.session_state.english != True
        else "Withdrawal flexibility"
    ),
]

Advantages_Compte_à_terme = [
    (
        "Taux d’intérêt supérieur au compte épargne"
        if st.session_state.english != True
        else "Higher interest rate than savings account"
    ),
    "Sécurité" if st.session_state.english != True else "Security",
]

Advantages_Carte_basique = [
    "Accessibilité" if st.session_state.english != True else "Accessibility",
    "Sécurité" if st.session_state.english != True else "Security",
    (
        "Paiements électroniques"
        if st.session_state.english != True
        else "Electronic payments"
    ),
]

Advantages_Carte_Visa = [
    "Acceptée partout" if st.session_state.english != True else "Accepted worldwide",
    "Sécurité" if st.session_state.english != True else "Security",
    (
        "Possibilité de crédit"
        if st.session_state.english != True
        else "Credit option available"
    ),
]

Advantages_Carte_Visa_Premium = [
    "Assurance voyages" if st.session_state.english != True else "Travel insurance",
    (
        "Services conciergerie"
        if st.session_state.english != True
        else "Concierge services"
    ),
    "Plafonds plus élevés" if st.session_state.english != True else "Higher limits",
]

Advantages_Carte_Visa_Elite = [
    "Accès lounges" if st.session_state.english != True else "Lounge access",
    (
        "Assurances complètes"
        if st.session_state.english != True
        else "Comprehensive insurance"
    ),
    "Service prioritaire" if st.session_state.english != True else "Priority service",
]

Advantages_Carte_Visa_Infinite = [
    "Concierge personnel" if st.session_state.english != True else "Personal concierge",
    "Assurances premium" if st.session_state.english != True else "Premium insurance",
    "Programmes luxe" if st.session_state.english != True else "Luxury programs",
]

Advantages_Crédit_Immo_avec_garantie_hypothécaire = [
    (
        "Taux généralement plus bas"
        if st.session_state.english != True
        else "Generally lower interest rates"
    ),
    (
        "Sécurise le prêt pour la banque"
        if st.session_state.english != True
        else "Secures the loan for the bank"
    ),
]

Advantages_Crédit_Immo_avec_garantie_liquide = [
    (
        "Plus rapide à mettre en place"
        if st.session_state.english != True
        else "Faster to set up"
    ),
    "Taux compétitif" if st.session_state.english != True else "Competitive rate",
]

Advantages_Crédit_Immo_avec_remboursement_in_fine = [
    (
        "Permet de libérer trésorerie mensuelle"
        if st.session_state.english != True
        else "Frees up monthly cash flow"
    ),
    (
        "Adapté investissement locatif"
        if st.session_state.english != True
        else "Suitable for rental investment"
    ),
]

Advantages_Crédit_Immo_subventionné = [
    "Taux avantageux" if st.session_state.english != True else "Preferential rate",
    "Soutien public" if st.session_state.english != True else "Public support",
]

Advantages_Crédit_à_la_consommation_non_affecté = [
    "Rapidité" if st.session_state.english != True else "Speed",
    "Flexibilité" if st.session_state.english != True else "Flexibility",
    (
        "Aucune obligation de destination"
        if st.session_state.english != True
        else "No specific purpose required"
    ),
]

Advantages_Crédit_Auto = [
    "Taux compétitif" if st.session_state.english != True else "Competitive rate",
    (
        "Remboursement échelonné"
        if st.session_state.english != True
        else "Installment repayment"
    ),
    (
        "Assurance souvent incluse"
        if st.session_state.english != True
        else "Insurance often included"
    ),
]

Advantages_Découvert = [
    "Flexibilité" if st.session_state.english != True else "Flexibility",
    "Immédiat" if st.session_state.english != True else "Immediate access",
    (
        "Couvre dépenses urgentes"
        if st.session_state.english != True
        else "Covers urgent expenses"
    ),
]

Advantages_Assurance_décès_invalidité_adossée_à_un_financement = [
    (
        "Sécurité pour la famille et la banque"
        if st.session_state.english != True
        else "Security for both family and bank"
    ),
]

Advantages_Assurance_décès_toutes_causes = [
    "Sécurité famille" if st.session_state.english != True else "Family security",
    (
        "Couverture complète"
        if st.session_state.english != True
        else "Comprehensive coverage"
    ),
]

Advantages_Multirisques_bâtiment = [
    "Couverture complète" if st.session_state.english != True else "Full coverage",
    "Tranquillité" if st.session_state.english != True else "Peace of mind",
]

Advantages_Maladie_complémentaire = [
    (
        "Accès à plus de soins"
        if st.session_state.english != True
        else "Access to more healthcare options"
    ),
    (
        "Remboursements supérieurs"
        if st.session_state.english != True
        else "Higher reimbursements"
    ),
]

Advantages_Retraite_complémentaire = [
    (
        "Prévoit revenus à la retraite"
        if st.session_state.english != True
        else "Provides income at retirement"
    ),
    "Avantage fiscal" if st.session_state.english != True else "Tax benefit",
]

Advantages_Retraite_complémentaire_en_UC = [
    (
        "Rendement potentiel plus élevé"
        if st.session_state.english != True
        else "Potentially higher returns"
    ),
    "Diversification" if st.session_state.english != True else "Diversification",
]

Advantages_Épargne_Éducation = [
    "Avantages fiscaux" if st.session_state.english != True else "Tax advantages",
    "Sécurité des fonds" if st.session_state.english != True else "Fund security",
]

Advantages_Épargne_Logement = [
    "Rendement garanti" if st.session_state.english != True else "Guaranteed return",
    (
        "Prime de l’État possible"
        if st.session_state.english != True
        else "Possible state bonus"
    ),
]

Advantages_OPCVM_monétaires = [
    "Sécurité" if st.session_state.english != True else "Security",
    "Liquidité élevée" if st.session_state.english != True else "High liquidity",
    "Rendement stable" if st.session_state.english != True else "Stable return",
]

Advantages_OPCVM_obligataires = [
    (
        "Rendement supérieur au compte épargne"
        if st.session_state.english != True
        else "Higher return than savings account"
    ),
    "Diversification" if st.session_state.english != True else "Diversification",
]

Advantages_OPCVM_diversifiés = [
    (
        "Rendement potentiellement plus élevé"
        if st.session_state.english != True
        else "Potentially higher return"
    ),
    "Risque modéré" if st.session_state.english != True else "Moderate risk",
]

Advantages_OPCVM_actions = [
    (
        "Potentiel de rendement élevé"
        if st.session_state.english != True
        else "High return potential"
    ),
    (
        "Diversification internationale"
        if st.session_state.english != True
        else "International diversification"
    ),
]

Advantages_Pack_bancaire_basique = [
    (
        "Économie sur frais combinés"
        if st.session_state.english != True
        else "Savings on combined fees"
    ),
    "Simplicité" if st.session_state.english != True else "Simplicity",
]

Advantages_Pack_bancaire_étoffé = [
    (
        "Services complets"
        if st.session_state.english != True
        else "Comprehensive services"
    ),
    (
        "Réductions sur produits associés"
        if st.session_state.english != True
        else "Discounts on related products"
    ),
]

Coût_estimatif_des_frais_Compte_chèque_en_DH = {
    t("Frais d’ouverture", "Opening fees"): t("0 DH", "0 MAD"),
    t("Frais mensuels", "Monthly fees"): t("20 - 50 DH", "20 - 50 MAD"),
    t("Frais virements/chéquiers", "Transfers/Cheque book fees"): t(
        "selon usage", "depending on usage"
    ),
}

Coût_estimatif_des_frais_Compte_chèque_en_devises = {
    t("Frais ouverture", "Opening fees"): t("0 DH", "0 MAD"),
    t("Frais tenue de compte", "Account maintenance fees"): t(
        "50 - 100 DH/mois", "50 - 100 MAD/month"
    ),
}

Coût_estimatif_des_frais_Compte_sur_carnet = {
    t("Frais ouverture", "Opening fees"): t("0 DH", "0 MAD"),
    t("Frais gestion", "Management fees"): t("0 - 10 DH/mois", "0 - 10 MAD/month"),
}

Coût_estimatif_des_frais_Compte_à_terme = {
    t("Frais ouverture", "Opening fees"): t("0 DH", "0 MAD"),
    t("Pas de frais mensuels", "No monthly fees"): "",
    t("Pénalités en cas de retrait anticipé", "Penalties for early withdrawal"): "",
}

Coût_estimatif_des_frais_Carte_basique = {
    t("Frais annuels", "Annual fees"): t("100 - 200 DH", "100 - 200 MAD"),
    t("Retrait", "Withdrawal"): t("3 - 5 DH/transaction", "3 - 5 MAD/transaction"),
}

Coût_estimatif_des_frais_Carte_Visa = {
    t("Frais annuels", "Annual fees"): t("200 - 400 DH", "200 - 400 MAD"),
    t("Retrait", "Withdrawal"): t("5 - 10 DH/transaction", "5 - 10 MAD/transaction"),
}

Coût_estimatif_des_frais_Carte_Visa_Premium = {
    t("Frais annuels", "Annual fees"): t("600 - 1000 DH", "600 - 1000 MAD"),
    t("Retrait", "Withdrawal"): t("5 - 10 DH/transaction", "5 - 10 MAD/transaction"),
}

Coût_estimatif_des_frais_Carte_Visa_Elite = {
    t("Frais annuels", "Annual fees"): t("1200 - 2000 DH", "1200 - 2000 MAD"),
    t("Retrait", "Withdrawal"): t("5 - 10 DH/transaction", "5 - 10 MAD/transaction"),
}

Coût_estimatif_des_frais_Carte_Visa_Infinite = {
    t("Frais annuels", "Annual fees"): t("3000 - 5000 DH", "3000 - 5000 MAD"),
    t("Retrait", "Withdrawal"): t("5 - 10 DH/transaction", "5 - 10 MAD/transaction"),
}

Coût_estimatif_des_frais_Crédit_Immo_avec_garantie_hypothécaire = {
    t("Frais dossier", "Processing fees"): t(
        "1% - 2% du montant", "1% - 2% of the amount"
    ),
    t("Assurance", "Insurance"): t("0,2% - 0,5% /an", "0,2% - 0,5% /year"),
    t("Intérêts selon taux marché", "Interest rate according to market"): "",
}

Coût_estimatif_des_frais_Crédit_Immo_avec_garantie_liquide = {
    t("Frais dossier", "Processing fees"): "1%",
    t("Assurance", "Insurance"): t("0,2% - 0,5% /an", "0,2% - 0,5% /year"),
}

Coût_estimatif_des_frais_Crédit_Immo_avec_remboursement_in_fine = {
    t("Frais dossier", "Processing fees"): "1%",
    t("Intérêts sur durée", "Interest over duration"): "",
    t("Assurance selon banque", "Insurance depending on bank"): "",
}

Coût_estimatif_des_frais_Crédit_Immo_subventionné = {
    t("Frais minimes", "Minimal fees"): "",
    t("Intérêts réduits", "Reduced interest"): "",
}

Coût_estimatif_des_frais_Crédit_à_la_consommation_non_affecté = {
    t("Frais dossier", "Processing fees"): "1% - 2%",
    t("Taux 8-12% annuel", "8-12% annual rate"): "",
}

Coût_estimatif_des_frais_Crédit_Auto = {
    t("Frais dossier", "Processing fees"): "1% - 2%",
    t("Taux", "Rate"): t("7% - 10% annuel", "7% - 10% annual"),
}

Coût_estimatif_des_frais_Découvert = {
    t("Intérêts", "Interest"): "12% - 18%",
    t("Commissions", "Commissions"): t("50 - 100 DH/mois", "50 - 100 MAD/month"),
}

Coût_estimatif_des_frais_Assurance_décès_invalidité_adossée_à_un_financement = {
    t("Prime", "Premium"): t(
        "0,2% - 0,5% du capital par an", "0.2% - 0.5% of the capital per year"
    ),
}

Coût_estimatif_des_frais_Assurance_décès_toutes_causes = {
    t("Prime", "Premium"): t(
        "0,3% - 0,6% du capital par an", "0,3% - 0,6% of the capital per year"
    ),
}

Coût_estimatif_des_frais_Multirisques_bâtiment = {
    t("Prime", "Premium"): t(
        "0,1% - 0,5% valeur du bien/an", "0,1% - 0,5% value of the property/year"
    ),
}

Coût_estimatif_des_frais_Maladie_complémentaire = {
    t("Prime", "Premium"): t(
        "500 - 5000 DH/an selon couverture", "500 - 5000 MAD/year depending on coverage"
    ),
}

Coût_estimatif_des_frais_Retraite_complémentaire = {
    t("Cotisation", "Contribution"): t(
        "5% - 20% revenu annuel", "5% - 20% revenu annual"
    ),
}

Coût_estimatif_des_frais_Retraite_complémentaire_en_UC = {
    t("Cotisation", "Contribution"): t("5% - 20% revenu", "5% - 20% income"),
    t("Frais gestion", "Management fees"): "0,5% - 2%",
}

Coût_estimatif_des_frais_Épargne_Éducation = {
    t("Versements flexibles", "Flexible payments"): "",
    t("Frais tenue compte 0-50 DH/mois", "Account fees 0-50 MAD/month"): "",
}

Coût_estimatif_des_frais_Épargne_Logement = {
    t("Frais minimes", "Minimal fees"): "",
    t("Intérêts selon taux marché", "Interest according to market rate"): "",
}

Coût_estimatif_des_frais_OPCVM_monétaires = {
    t("Frais gestion", "Management fees"): "0,2% - 1%",
    t("Souscription minimale", "Minimum subscription"): t("1000 DH", "1000 MAD"),
}

Coût_estimatif_des_frais_OPCVM_obligataires = {
    t("Frais gestion", "Management fees"): "0,3% - 1%",
    t("Souscription minimale", "Minimum subscription"): t("1000 DH", "1000 MAD"),
}

Coût_estimatif_des_frais_OPCVM_diversifiés = {
    t("Frais gestion", "Management fees"): "0,5% - 1,5%",
    t("Souscription minimale", "Minimum subscription"): t("1000 DH", "1000 MAD"),
}

Coût_estimatif_des_frais_OPCVM_actions = {
    t("Frais gestion", "Management fees"): "0,5% - 2%",
    t("Souscription minimale", "Minimum subscription"): t("1000 DH", "1000 MAD"),
}

Coût_estimatif_des_frais_Pack_bancaire_basique = {
    t("Abonnement", "Subscription"): t("50 - 150 DH/mois", "50 - 150 MAD/month"),
}

Coût_estimatif_des_frais_Pack_bancaire_étoffé = {
    t("Abonnement", "Subscription"): t("150 - 400 DH/mois", "150 - 400 MAD/month"),
}

categories_eng = {
    "Comptes": [
        "Product - Checking account in MAD",
        "Product - Checking account in foreign currency",
        "Product - Savings account",
        "Product - Term deposit account",
    ],
    "Cartes": [
        "Product - Basic card",
        "Product - Visa card",
        "Product - Visa Premium card",
        "Product - Visa Elite card",
        "Product - Visa Infinite card",
    ],
    "Financement immobilier": [
        "Product - Mortgage loan with real estate guarantee",
        "Product - Mortgage loan with cash guarantee",
        "Product - Mortgage loan with bullet repayment",
        "Product - Subsidized mortgage loan",
    ],
    "Financement à la consommation": [
        "Product - Unsecured consumer loan",
        "Product - Auto loan",
        "Product - Overdraft facility",
    ],
    "Assurance": [
        "Product - Death and disability insurance linked to a loan",
        "Product - All-cause death insurance",
        "Product - Multi-risk building insurance",
        "Product - Supplementary health insurance",
    ],
    "Retraite & Prévoyance": [
        "Product - Supplementary retirement plan",
        "Product - Unit-linked supplementary retirement plan",
    ],
    "Épargne & Placement": [
        "Product - Education savings plan",
        "Product - Housing savings plan",
        "Product - Money market mutual fund (OPCVM)",
        "Product - Bond mutual fund (OPCVM)",
        "Product - Diversified mutual fund (OPCVM)",
        "Product - Equity mutual fund (OPCVM)",
    ],
    "Packs bancaires": [
        "Product - Basic banking package",
        "Product - Enhanced banking package",
    ],
}
Advantages = {
    "Produit - Compte chèque en DH" if st.session_state.english != True else "Product - Checking account in MAD": [
        "Gestion facile des paiements, virements et retraits; carte bancaire associée"
        if st.session_state.english != True
        else "Easy payment management, transfers and withdrawals; linked bank card",
        Advantages_Compte_chèque_en_DH,
        Coût_estimatif_des_frais_Compte_chèque_en_DH,
    ],
    "Produit - Compte chèque en devises" if st.session_state.english != True else "Product - Checking account in foreign currency": [
        "Facilite les transactions internationales, convertibilité rapide"
        if st.session_state.english != True
        else "Facilitates international transactions, fast convertibility",
        Advantages_Compte_chèque_en_devises,
        Coût_estimatif_des_frais_Compte_chèque_en_devises,
    ],
    "Produit - Compte sur carnet" if st.session_state.english != True else "Product - Savings account": [
        "Rendement sur les dépôts, flexibilité de retrait"
        if st.session_state.english != True
        else "Earnings on deposits, withdrawal flexibility",
        Advantages_Compte_sur_carnet,
        Coût_estimatif_des_frais_Compte_sur_carnet,
    ],
    "Produit - Compte à terme" if st.session_state.english != True else "Product - Term deposit account": [
        "Taux d’intérêt supérieur au compte épargne, sécurité"
        if st.session_state.english != True
        else "Higher interest rate than savings account, security",
        Advantages_Compte_à_terme,
        Coût_estimatif_des_frais_Compte_à_terme,
    ],
    "Produit - Carte basique" if st.session_state.english != True else "Product - Basic card": [
        "Accessibilité, sécurité, paiements électroniques"
        if st.session_state.english != True
        else "Accessibility, security, electronic payments",
        Advantages_Carte_basique,
        Coût_estimatif_des_frais_Carte_basique,
    ],
    "Produit - Carte Visa" if st.session_state.english != True else "Product - Visa card": [
        "Acceptée partout, sécurité, possibilité de crédit"
        if st.session_state.english != True
        else "Accepted everywhere, security, credit option",
        Advantages_Carte_Visa,
        Coût_estimatif_des_frais_Carte_Visa,
    ],
    "Produit - Carte Visa Premium" if st.session_state.english != True else "Product - Visa Premium card": [
        "Assurance voyages, services de conciergerie, plafonds plus élevés"
        if st.session_state.english != True
        else "Travel insurance, concierge services, higher limits",
        Advantages_Carte_Visa_Premium,
        Coût_estimatif_des_frais_Carte_Visa_Premium,
    ],
    "Produit - Carte Visa Elite" if st.session_state.english != True else "Product - Visa Elite card": [
        "Accès aux lounges, assurances complètes, service prioritaire"
        if st.session_state.english != True
        else "Lounge access, full insurance, priority service",
        Advantages_Carte_Visa_Elite,
        Coût_estimatif_des_frais_Carte_Visa_Elite,
    ],
    "Produit - Carte Visa Infinite" if st.session_state.english != True else "Product - Visa Infinite card": [
        "Concierge personnel, assurances premium, programmes luxe"
        if st.session_state.english != True
        else "Personal concierge, premium insurance, luxury programs",
        Advantages_Carte_Visa_Infinite,
        Coût_estimatif_des_frais_Carte_Visa_Infinite,
    ],
    "Produit - Crédit Immo avec garantie hypothécaire" if st.session_state.english != True else "Product - Mortgage loan with real estate guarantee": [
        "Taux généralement plus bas, sécurise le prêt pour la banque"
        if st.session_state.english != True
        else "Generally lower rate, secures the loan for the bank",
        Advantages_Crédit_Immo_avec_garantie_hypothécaire,
        Coût_estimatif_des_frais_Crédit_Immo_avec_garantie_hypothécaire,
    ],
    "Produit - Crédit Immo avec garantie liquide" if st.session_state.english != True else "Product - Mortgage loan with cash guarantee": [
        "Plus rapide à mettre en place, taux compétitif"
        if st.session_state.english != True
        else "Faster to implement, competitive rate",
        Advantages_Crédit_Immo_avec_garantie_liquide,
        Coût_estimatif_des_frais_Crédit_Immo_avec_garantie_liquide,
    ],
    "Produit - Crédit Immo avec remboursement in fine" if st.session_state.english != True else "Product - Mortgage loan with bullet repayment": [
        "Permet de libérer la trésorerie mensuelle, adapté à l’investissement locatif"
        if st.session_state.english != True
        else "Frees monthly cash flow, suitable for rental investment",
        Advantages_Crédit_Immo_avec_remboursement_in_fine,
        Coût_estimatif_des_frais_Crédit_Immo_avec_remboursement_in_fine,
    ],
    "Produit - Crédit Immo subventionné" if st.session_state.english != True else "Product - Subsidized mortgage loan": [
        "Taux avantageux, soutien public"
        if st.session_state.english != True
        else "Advantageous rate, public support",
        Advantages_Crédit_Immo_subventionné,
        Coût_estimatif_des_frais_Crédit_Immo_subventionné,
    ],
    "Produit - Crédit à la consommation non affecté" if st.session_state.english != True else "Product - Unsecured consumer loan": [
        "Rapidité, flexibilité, aucune obligation de destination"
        if st.session_state.english != True
        else "Fast, flexible, no usage obligation",
        Advantages_Crédit_à_la_consommation_non_affecté,
        Coût_estimatif_des_frais_Crédit_à_la_consommation_non_affecté,
    ],
    "Produit - Crédit Auto" if st.session_state.english != True else "Product - Auto loan": [
        "Taux compétitif, remboursement échelonné, assurance souvent incluse"
        if st.session_state.english != True
        else "Competitive rate, installment repayment, insurance often included",
        Advantages_Crédit_Auto,
        Coût_estimatif_des_frais_Crédit_Auto,
    ],
    "Produit - Découvert" if st.session_state.english != True else "Product - Overdraft facility": [
        "Flexibilité, immédiat, couvre les dépenses urgentes"
        if st.session_state.english != True
        else "Flexibility, immediate, covers urgent expenses",
        Advantages_Découvert,
        Coût_estimatif_des_frais_Découvert,
    ],
    "Produit - Assurance décès invalidité adossée à un financement" if st.session_state.english != True else "Product - Death and disability insurance linked to a loan": [
        "Sécurité pour la famille et la banque"
        if st.session_state.english != True
        else "Security for family and the bank",
        Advantages_Assurance_décès_invalidité_adossée_à_un_financement,
        Coût_estimatif_des_frais_Assurance_décès_invalidité_adossée_à_un_financement,
    ],
    "Produit - Assurance décès toutes causes" if st.session_state.english != True else "Product - All-cause death insurance": [
        "Sécurité pour la famille, couverture complète"
        if st.session_state.english != True
        else "Family security, full coverage",
        Advantages_Assurance_décès_toutes_causes,
        Coût_estimatif_des_frais_Assurance_décès_toutes_causes,
    ],
    "Produit - Multirisques bâtiment" if st.session_state.english != True else "Product - Multi-risk building insurance": [
        "Couverture complète, tranquillité"
        if st.session_state.english != True
        else "Full coverage, peace of mind",
        Advantages_Multirisques_bâtiment,
        Coût_estimatif_des_frais_Multirisques_bâtiment,
    ],
    "Produit - Maladie complémentaire" if st.session_state.english != True else "Product - Supplementary health insurance": [
        "Accès à plus de soins, remboursements supérieurs"
        if st.session_state.english != True
        else "Access to more care, higher reimbursements",
        Advantages_Maladie_complémentaire,
        Coût_estimatif_des_frais_Maladie_complémentaire,
    ],
    "Produit - Retraite complémentaire" if st.session_state.english != True else "Product - Supplementary retirement plan": [
        "Prévoit des revenus à la retraite, avantage fiscal"
        if st.session_state.english != True
        else "Provides retirement income, tax advantage",
        Advantages_Retraite_complémentaire,
        Coût_estimatif_des_frais_Retraite_complémentaire,
    ],
    "Produit - Retraite complémentaire en UC" if st.session_state.english != True else "Product - Unit-linked supplementary retirement plan": [
        "Rendement potentiel plus élevé, diversification"
        if st.session_state.english != True
        else "Potentially higher return, diversification",
        Advantages_Retraite_complémentaire_en_UC,
        Coût_estimatif_des_frais_Retraite_complémentaire_en_UC,
    ],
    "Produit - Épargne Éducation" if st.session_state.english != True else "Product - Education savings plan": [
        "Avantages fiscaux, sécurité des fonds"
        if st.session_state.english != True
        else "Tax advantages, fund security",
        Advantages_Épargne_Éducation,
        Coût_estimatif_des_frais_Épargne_Éducation,
    ],
    "Produit - Épargne Logement" if st.session_state.english != True else "Product - Housing savings plan": [
        "Rendement garanti, prime de l’État possible"
        if st.session_state.english != True
        else "Guaranteed return, possible state bonus",
        Advantages_Épargne_Logement,
        Coût_estimatif_des_frais_Épargne_Logement,
    ],
    "Produit - OPCVM monétaires" if st.session_state.english != True else "Product - Money market mutual fund (OPCVM)": [
        "Sécurité, liquidité élevée, rendement stable"
        if st.session_state.english != True
        else "Security, high liquidity, stable return",
        Advantages_OPCVM_monétaires,
        Coût_estimatif_des_frais_OPCVM_monétaires,
    ],
    "Produit - OPCVM obligataires" if st.session_state.english != True else "Product - Bond mutual fund (OPCVM)": [
        "Rendement supérieur au compte épargne, diversification"
        if st.session_state.english != True
        else "Higher return than savings account, diversification",
        Advantages_OPCVM_obligataires,
        Coût_estimatif_des_frais_OPCVM_obligataires,
    ],
    "Produit - OPCVM diversifiés" if st.session_state.english != True else "Product - Diversified mutual fund (OPCVM)": [
        "Rendement potentiellement plus élevé, risque modéré"
        if st.session_state.english != True
        else "Potentially higher return, moderate risk",
        Advantages_OPCVM_diversifiés,
        Coût_estimatif_des_frais_OPCVM_diversifiés,
    ],
    "Produit - OPCVM actions" if st.session_state.english != True else "Product - Equity mutual fund (OPCVM)": [
        "Potentiel de rendement élevé, diversification internationale"
        if st.session_state.english != True
        else "High return potential, international diversification",
        Advantages_OPCVM_actions,
        Coût_estimatif_des_frais_OPCVM_actions,
    ],
    "Produit - Pack bancaire basique" if st.session_state.english != True else "Product - Basic banking package": [
        "Économie sur les frais combinés, simplicité"
        if st.session_state.english != True
        else "Savings on combined fees, simplicity",
        Advantages_Pack_bancaire_basique,
        Coût_estimatif_des_frais_Pack_bancaire_basique,
    ],
    "Produit - Pack bancaire étoffé" if st.session_state.english != True else "Product - Enhanced banking package": [
        "Services complets, réductions sur produits associés"
        if st.session_state.english != True
        else "Full services, discounts on associated products",
        Advantages_Pack_bancaire_étoffé,
        Coût_estimatif_des_frais_Pack_bancaire_étoffé,
    ],
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


def switch_page_produit(produit):
    st.session_state["produit_page"] = True
    st.session_state.produit = produit
    st.session_state.Advantage = Advantages[produit][0]
    st.session_state.Advantage_list = Advantages[produit][1]
    st.session_state.cout_list = Advantages[produit][2]


def change_client():
    user_input = st.session_state.user_input.strip()
    if user_input and user_input.strip() != "":
        try:
            client_index = int(user_input)
            if client_index == st.session_state.client_index:
                return
            st.session_state.client_index = client_index
            st.session_state.process_done = False
        except ValueError:
            st.session_state.error_msg = (
                "❌ Veuillez saisir un nombre entier valide pour le numéro du client."
                if st.session_state.english != True
                else "❌ Please enter a valid integer for the client number."
            )


def switch_page_home():
    st.session_state["switch_page_home"] = True


# --- INITIALISATION DES VARIABLES DE SESSION ---
st.session_state.setdefault("switch_page_home", False)
st.session_state.switch_page_client = False
st.session_state.setdefault("produit_page", None)
st.session_state.m_messages = []


# --- NAVIGATION AUTOMATIQUE SI DÉCLENCHÉE ---
if st.session_state["produit_page"] == True:
    st.switch_page("pages/produit.py")
if st.session_state["switch_page_home"] == True:
    st.switch_page("pages/page_d'accueil.py")
# --- CHARGEMENT DU STYLE ---
load_css(CSS_PATH)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown(
        """
        <style>
        div[class*="st-key-btn0"] .stButton button {
            width: 100%;
            justify-content: flex-start;
        }        
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
        div[class*="st-key-btn6"] .stButton button {
            justify-content: flex-start;
            width: 100%;
        }           
        </style>
            """,
        unsafe_allow_html=True,
    )
    st.image("images/NEURONAIZE-LOGO-BASELINE.png", width="stretch")
    st.button(
        "Accueil" if st.session_state.english != True else "Home",
        width="stretch",
        icon=":material/home:",
        type="tertiary",
        key="btn0",
        on_click=switch_page_home,
    )
    st.button(
        "Tableau de bord" if st.session_state.english != True else "Dashboard",
        width="stretch",
        icon=":material/dashboard:",
        type="tertiary",
        key="btn1",
    )
    st.button(
        "Clients" if st.session_state.english != True else "Customers",
        width="stretch",
        icon=":material/patient_list:",
        type="tertiary",
        key="btn2",
    )
    st.button(
        "Comptes" if st.session_state.english != True else "Accounts",
        width="stretch",
        icon=":material/account_balance:",
        type="tertiary",
        key="btn3",
    )
    st.button(
        "Prêts" if st.session_state.english != True else "Loans",
        width="stretch",
        icon=":material/money_bag:",
        type="tertiary",
        key="btn4",
    )
    st.button(
        "Cartes" if st.session_state.english != True else "Cards",
        width="stretch",
        icon=":material/playing_cards:",
        type="tertiary",
        key="btn5",
    )
    st.button(
        "Investissements" if st.session_state.english != True else "Investments",
        width="stretch",
        icon=":material/wallet:",
        type="tertiary",
        key="btn6",
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
col_fiche_client, col_input = st.columns([3, 2])
error_placeholder = st.empty()
if "error_msg" in st.session_state and st.session_state.error_msg:
    error_placeholder.error(st.session_state.error_msg)
    st.session_state.error_msg = ""  # reset après affichage
with col_fiche_client:
    st.title(
        ("Fiche détaillée du Client" + " " + str(client_index))
        if st.session_state.english != True
        else "Detailed Client Profile" + " " + str(client_index)
    )
with col_input:
    user_input = st.text_input(
        "test",
        placeholder=(
            "Saisissez un autre numéro de client."
            if st.session_state.english != True
            else "Enter another client number."
        ),
        label_visibility="hidden",
        on_change=change_client,
        key="user_input",
    )

col11, col22 = st.columns([1.6, 3])
with col11:
    with st.container(border=True):
        nom = (
            ("Client" + " " + str(client_index))
            if st.session_state.english != True
            else "Customer" + " " + str(client_index)
        )
        col_client, col_icon_client = st.columns([3.5, 1])
        with col_client:
            st.markdown(
                f"""
                    <p style='font-family:Arial; font-size:24px; font-weight:bold;'>
                        {nom}
                    </p>
                    """,
                unsafe_allow_html=True,
            )
        with col_icon_client:
            st.image("images/client.png", width="stretch")
        st.write(
            ("Âge :" + " " + str(df["Âge"].iat[client_index]))
            if st.session_state.english != True
            else "Age :" + " " + str(df["Âge"].iat[client_index])
        )
        st.write(
            ("Statut marital :" + " " + str(df["Statut marital"].iat[client_index]))
            if st.session_state.english != True
            else "Marital status :" + " " + str(df["Statut marital"].iat[client_index])
        )
        st.write("Situation :" + " " + str(df["Situation"].iat[client_index]))
        st.write(
            ("Nombre d’enfants :" + " " + str(df["Nombre d’enfants"].iat[client_index]))
            if st.session_state.english != True
            else "Number of children :"
            + " "
            + str(df["Nombre d’enfants"].iat[client_index])
        )
        col_Propriétaire, col_reponse_oui, col_reponse_non = st.columns([2.2, 1, 1])
        with col_Propriétaire:
            st.write(
                "Propriétaire :"
                if st.session_state.english != True
                else "Property owner :"
            )
        with col_reponse_oui:
            st.checkbox(
                "oui" if st.session_state.english != True else "yes",
                value=value_15,
                disabled=True,
                key="29",
            )
        with col_reponse_non:
            st.checkbox(
                "non" if st.session_state.english != True else "no",
                value=not value_15,
                disabled=True,
                key="30",
            )
        st.write(
            ("Revenu annuel :" + " " + str(df["Revenu annuel"].iat[client_index]))
            if st.session_state.english != True
            else "Annual income :" + " " + str(df["Revenu annuel"].iat[client_index])
        )
    with st.container(border=True):
        col_action, col_action_icon = st.columns([4.5, 1])
        text = (
            "Actions rapides" if st.session_state.english != True else "Quick actions"
        )
        with col_action:
            st.markdown(
                f"""
                <p style='font-family:Arial; font-size:24px; font-weight:bold;'>
                    {text}
                </p>
                """,
                unsafe_allow_html=True,
            )
        with col_action_icon:
            st.image("images/action.png", width="stretch")
        st.markdown(
            """
        <style>
        div[class*="st-key-btn_home"] .stButton button {
            width: 100%;
            justify-content: flex-start;
        }
        div[class*="st-key-btn_hom"] .stButton button {
            width: 100%;
            justify-content: flex-start;
        }
        div[class*="st-key-btn_update"] .stButton button {
            width: 100%;
            justify-content: flex-start;
        }
        div[class*="st-key-btn_inspect"] .stButton button {
            width: 100%;
            justify-content: flex-start;
        }
        div[class*="st-key-btn_send"] .stButton button {
            justify-content: flex-start;
            width: 100%;
        }        
        </style>
            """,
            unsafe_allow_html=True,
        )
        st.button(
            (
                "Ouvrir un nouveau compte"
                if st.session_state.english != True
                else "Open a new account"
            ),
            icon=":material/home:",
            width="stretch",
            key="btn_home",
        )
        st.button(
            (
                "Demander un prêt"
                if st.session_state.english != True
                else "Request a loan"
            ),
            icon=":material/attach_money:",
            width="stretch",
            key="btn_hom",
        )
        st.button(
            (
                " Mise à jour du contact"
                if st.session_state.english != True
                else "Update contact"
            ),
            icon=":material/update:",
            width="stretch",
            key="btn_update",
        )
        st.button(
            (
                "Consulter les relevés"
                if st.session_state.english != True
                else "View statements"
            ),
            icon=":material/frame_inspect:",
            width="stretch",
            key="btn_inspect",
        )
        st.button(
            (
                "Effectuer un virement"
                if st.session_state.english != True
                else "Make a transfer"
            ),
            icon=":material/send_money:",
            width="stretch",
            key="btn_send",
        )

with col22:
    with st.container(border=True):
        col_produit, col_produit_icon = st.columns([6.5, 1])
        text_1 = (
            "Aperçu des produits"
            if st.session_state.english != True
            else "Product overview"
        )
        with col_produit:
            st.markdown(
                f"""
                <p style='font-family:Arial; font-size:24px; font-weight:bold;'>
                    {text_1}
                </p>
                """,
                unsafe_allow_html=True,
            )
        text_2 = (
            f"Client {client_index} possède :"
            if st.session_state.english != True
            else f"Client {client_index} owns :"
        )
        with col_produit_icon:
            st.image("images/produit.png", width="stretch")
        st.markdown(
            f"""
                    <p style='font-family:Arial; font-size:15px; font-weight:bold; font-style:italic; color:blue;'>
                        {text_2}
                    </p>
                    """,
            unsafe_allow_html=True,
        )
        col112, col122, col133 = st.columns([6.5, 1, 1])
        with col112:
            st.write(
                "Produit - Compte chèque en DH"
                if st.session_state.english != True
                else "Product - Checking account in MAD"
            )
            st.write(
                "Produit - Compte chèque en devises"
                if st.session_state.english != True
                else "Product - Foreign currency checking account"
            )
            st.write(
                "Produit - Compte sur carnet"
                if st.session_state.english != True
                else "Product - Passbook account"
            )
            st.write(
                "Produit - Compte à terme"
                if st.session_state.english != True
                else "Product - Term deposit account"
            )

            st.write(
                "Produit - Carte basique"
                if st.session_state.english != True
                else "Product - Basic card"
            )
            st.write(
                "Produit - Carte visa"
                if st.session_state.english != True
                else "Product - Visa card"
            )
            st.write(
                "Produit - Carte visa premium"
                if st.session_state.english != True
                else "Product - Visa Premium card"
            )
            st.write(
                "Produit - Carte visa elite"
                if st.session_state.english != True
                else "Product - Visa Elite card"
            )
            st.write(
                "Produit - Carte visa infinite"
                if st.session_state.english != True
                else "Product - Visa Infinite card"
            )

            st.write(
                "Produit - Crédit Immo avec garantie hypothécaire"
                if st.session_state.english != True
                else "Product - Mortgage-backed home loan"
            )
            st.write(
                "Produit - Crédit Immo avec garantie liquide"
                if st.session_state.english != True
                else "Product - Cash-backed home loan"
            )
            st.write(
                "Produit - Crédit immo avec remboursement in fine"
                if st.session_state.english != True
                else "Product - Bullet repayment home loan"
            )

            st.write(
                "Produit - Crédit à la consommation non affecté"
                if st.session_state.english != True
                else "Product - Unsecured consumer loan"
            )
            st.write(
                "Produit - Crédit Auto"
                if st.session_state.english != True
                else "Product - Auto loan"
            )
        with col122:
            st.checkbox(
                "oui" if st.session_state.english != True else "yes",
                value=value_1,
                disabled=True,
                key="1",
            )
            st.checkbox(
                "oui" if st.session_state.english != True else "yes",
                value=value_2,
                disabled=True,
                key="2",
            )
            st.checkbox(
                "oui" if st.session_state.english != True else "yes",
                value=value_3,
                disabled=True,
                key="3",
            )
            st.checkbox(
                "oui" if st.session_state.english != True else "yes",
                value=value_4,
                disabled=True,
                key="4",
            )
            st.checkbox(
                "oui" if st.session_state.english != True else "yes",
                value=value_5,
                disabled=True,
                key="5",
            )
            st.checkbox(
                "oui" if st.session_state.english != True else "yes",
                value=value_6,
                disabled=True,
                key="6",
            )
            st.checkbox(
                "oui" if st.session_state.english != True else "yes",
                value=value_7,
                disabled=True,
                key="7",
            )
            st.checkbox(
                "oui" if st.session_state.english != True else "yes",
                value=value_8,
                disabled=True,
                key="8",
            )
            st.checkbox(
                "oui" if st.session_state.english != True else "yes",
                value=value_9,
                disabled=True,
                key="9",
            )
            st.checkbox(
                "oui" if st.session_state.english != True else "yes",
                value=value_10,
                disabled=True,
                key="10",
            )
            st.checkbox(
                "oui" if st.session_state.english != True else "yes",
                value=value_11,
                disabled=True,
                key="11",
            )
            st.checkbox(
                "oui" if st.session_state.english != True else "yes",
                value=value_12,
                disabled=True,
                key="12",
            )
            st.checkbox(
                "oui" if st.session_state.english != True else "yes",
                value=value_13,
                disabled=True,
                key="13",
            )
            st.checkbox(
                "oui" if st.session_state.english != True else "yes",
                value=value_14,
                disabled=True,
                key="14",
            )

        with col133:
            st.checkbox(
                "non" if st.session_state.english != True else "no",
                disabled=True,
                value=not value_1,
                key="15",
            )
            st.checkbox(
                "non" if st.session_state.english != True else "no",
                disabled=True,
                value=not value_2,
                key="16",
            )
            st.checkbox(
                "non" if st.session_state.english != True else "no",
                disabled=True,
                value=not value_3,
                key="17",
            )
            st.checkbox(
                "non" if st.session_state.english != True else "no",
                disabled=True,
                value=not value_4,
                key="18",
            )
            st.checkbox(
                "non" if st.session_state.english != True else "no",
                disabled=True,
                value=not value_5,
                key="19",
            )
            st.checkbox(
                "non" if st.session_state.english != True else "no",
                disabled=True,
                value=not value_6,
                key="20",
            )
            st.checkbox(
                "non" if st.session_state.english != True else "no",
                disabled=True,
                value=not value_7,
                key="21",
            )
            st.checkbox(
                "non" if st.session_state.english != True else "no",
                disabled=True,
                value=not value_8,
                key="22",
            )
            st.checkbox(
                "non" if st.session_state.english != True else "no",
                disabled=True,
                value=not value_9,
                key="23",
            )
            st.checkbox(
                "non" if st.session_state.english != True else "no",
                disabled=True,
                value=not value_10,
                key="24",
            )
            st.checkbox(
                "non" if st.session_state.english != True else "no",
                disabled=True,
                value=not value_11,
                key="25",
            )
            st.checkbox(
                "non" if st.session_state.english != True else "no",
                disabled=True,
                value=not value_12,
                key="26",
            )
            st.checkbox(
                "non" if st.session_state.english != True else "no",
                disabled=True,
                value=not value_13,
                key="27",
            )
            st.checkbox(
                "non" if st.session_state.english != True else "no",
                disabled=True,
                value=not value_14,
                key="28",
            )

    col1, col2, col3 = st.columns([1.6, 2, 1])
    with col1:
        col12, col21, col13 = st.columns([5, 1, 2])
        with col13:
            st.image("images/NEURONAIZE-ICONE-NOIR.png", width=40)
    with col2:
        analyser_btn = st.button(
            (
                "Analysez avec NeuronAize "
                if st.session_state.english != True
                else "Analyse with NeuronAize"
            ),
            width=210,
            key="analyser",
        )
if analyser_btn:
    st.session_state["aff_content"] = True
    st.session_state.process_done = False
if st.session_state.aff_content == True:
    text_3 = (
        "Synthèse financière"
        if st.session_state.english != True
        else "Financial summary"
    )
    with st.container(border=True):
        st.markdown(
            f"""
                <p style='font-family:Arial; font-size:24px; font-weight:bold;'>
                    {text_3}
                </p>
                """,
            unsafe_allow_html=True,
        )
        col1111, col2222, col3333 = st.columns([1, 1, 1])
        with col1111:
            with st.container(border=True):
                st.write(
                    "Revenus totaux (cumul annuel)"
                    if st.session_state.english != True
                    else "Total income (year-to-date)"
                )
                st.markdown(
                    """
                    <hr style="margin-top:5px; margin-bottom:5px;">
                    """,
                    unsafe_allow_html=True,
                )
                col11111, col22222 = st.columns([5, 1])
                with col11111:
                    st.write(total_income)
                with col22222:
                    st.write("DH" if st.session_state.english != True else "MAD")
        with col2222:
            with st.container(border=True):
                st.write(
                    "Dépenses totales (cumul annuel)"
                    if st.session_state.english != True
                    else "Total expenses (year-to-date)"
                )
                st.markdown(
                    """
                    <hr style="margin-top:5px; margin-bottom:5px;">
                    """,
                    unsafe_allow_html=True,
                )
                col11111, col22222 = st.columns([5, 1])
                with col11111:
                    st.write(total_expenses)
                with col22222:
                    st.write("DH" if st.session_state.english != True else "MAD")
        with col3333:
            with st.container(border=True):
                st.write(
                    "Patrimoine net actuel"
                    if st.session_state.english != True
                    else "Current net worth"
                )
                st.markdown(
                    """
                    <hr style="margin-top:5px; margin-bottom:5px;">
                    """,
                    unsafe_allow_html=True,
                )
                col11111, col22222 = st.columns([5, 1])
                with col11111:
                    st.write(current_net_worth)
                with col22222:
                    st.write("DH" if st.session_state.english != True else "MAD")
        with st.container(border=True):
            text_4 = (
                "Revenus vs Dépenses mensuels"
                if st.session_state.english != True
                else "Monthly Income vs Expenses"
            )
            st.markdown(
                f"""
                    <p style='font-family:Arial; font-size:24px; font-weight:bold;'>
                        {text_4}
                    </p>
                    """,
                unsafe_allow_html=True,
            )
            # --- Créer le graphique ---
            fig = go.Figure()

            # Revenus
            fig.add_trace(
                go.Scatter(
                    x=months,
                    y=monthly_income,
                    mode="lines+markers",
                    name="Revenus" if st.session_state.english != True else "Income",
                    line=dict(color="#2ecc71", width=3),
                    marker=dict(size=8),
                )
            )

            # Dépenses
            fig.add_trace(
                go.Scatter(
                    x=months,
                    y=monthly_expenses,
                    mode="lines+markers",
                    name="Dépenses" if st.session_state.english != True else "Expenses",
                    line=dict(color="#e74c3c", width=3),
                    marker=dict(size=8),
                )
            )

            # --- Mise en forme ---
            fig.update_layout(
                title=(
                    "Évolution mensuelle des revenus et dépenses"
                    if st.session_state.english != True
                    else "Monthly evolution of income and expenses"
                ),
                xaxis_title="Mois" if st.session_state.english != True else "Months",
                yaxis_title=(
                    "Montant (DH)"
                    if st.session_state.english != True
                    else "Amount (MAD)"
                ),
                plot_bgcolor="white",
                font=dict(size=14),
                legend=dict(
                    title=(
                        "Catégories"
                        if st.session_state.english != True
                        else "Categories"
                    )
                ),
                hovermode="x unified",
            )

            # --- Affichage Streamlit ---
            st.plotly_chart(fig, use_container_width=True)
    if "process_done" in st.session_state and st.session_state.process_done == False:
        # 1️⃣ Récupérer les données du client sélectionné
        client_data = df.iloc[[client_index]]  # on garde la forme DataFrame

        # 2️⃣ Chemin du fichier Excel à écraser
        client_path = "Data/client_input.xlsx"

        # 3️⃣ Écrire les données dans l'Excel
        client_data.to_excel(client_path, index=False)

        # 4️⃣ Exécuter le script Python externe
        ai_script_path = "ai.py"

        try:
            with st.spinner(
                "Patientez svp..."
                if st.session_state.english != True
                else "Please wait..."
            ):
                # Exécute le script et attend qu'il se termine
                subprocess.run([f"{sys.executable}", ai_script_path], check=True)
                st.session_state.process_done = True
        except subprocess.CalledProcessError as e:
            st.session_state.error_msg = e
    error_placeholder = st.empty()
    if "error_msg" in st.session_state and st.session_state.error_msg:
        error_placeholder.error(st.session_state.error_msg)
        st.session_state.error_msg = ""  # reset après affichage

    with st.container(border=True, key="cont_clients"):
        text_5 = (
            "Recommandations basées sur les clients similaires"
            if st.session_state.english != True
            else "Recommendations based on similar clients"
        )
        st.markdown(
            f"""
                    <p style='font-family:Arial; font-size:24px; font-weight:bold;'>
                        {text_5}
                    </p>
                    """,
            unsafe_allow_html=True,
        )
        if os.path.exists(local_recommendations_output_file):
            with open(local_recommendations_output_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            for item in data:
                if item["product"] in categories_fr["Comptes"]:
                    index = categories_fr["Comptes"].index(item["product"])
                    if st.session_state.english:
                        local_recommendations_comptes_categorie[
                            categories_eng["Comptes"][index]
                        ] = item["percentage"]
                    else:
                        local_recommendations_comptes_categorie[item["product"]] = item[
                            "percentage"
                        ]

                if item["product"] in categories_fr["Cartes"]:
                    index = categories_fr["Cartes"].index(item["product"])
                    if st.session_state.english:
                        local_recommendations_cartes_categorie[
                            categories_eng["Cartes"][index]
                        ] = item["percentage"]
                    else:
                        local_recommendations_cartes_categorie[item["product"]] = item[
                            "percentage"
                        ]

                if item["product"] in categories_fr["Financement immobilier"]:
                    index = categories_fr["Financement immobilier"].index(
                        item["product"]
                    )
                    if st.session_state.english:
                        local_recommendations_financement_immobilier_categorie[
                            categories_eng["Financement immobilier"][index]
                        ] = item["percentage"]
                    else:
                        local_recommendations_financement_immobilier_categorie[
                            item["product"]
                        ] = item["percentage"]

                if item["product"] in categories_fr["Financement à la consommation"]:
                    index = categories_fr["Financement à la consommation"].index(
                        item["product"]
                    )
                    if st.session_state.english:
                        local_recommendations_financement_à_la_consommation_categorie[
                            categories_eng["Financement à la consommation"][index]
                        ] = item["percentage"]
                    else:
                        local_recommendations_financement_à_la_consommation_categorie[
                            item["product"]
                        ] = item["percentage"]

                if item["product"] in categories_fr["Assurance"]:
                    index = categories_fr["Assurance"].index(item["product"])
                    if st.session_state.english:
                        local_recommendations_assurance_categorie[
                            categories_eng["Assurance"][index]
                        ] = item["percentage"]
                    else:
                        local_recommendations_assurance_categorie[item["product"]] = (
                            item["percentage"]
                        )

                if item["product"] in categories_fr["Retraite & Prévoyance"]:
                    index = categories_fr["Retraite & Prévoyance"].index(
                        item["product"]
                    )
                    if st.session_state.english:
                        local_recommendations_retraite_et_prévoyance_categorie[
                            categories_eng["Retraite & Prévoyance"][index]
                        ] = item["percentage"]
                    else:
                        local_recommendations_retraite_et_prévoyance_categorie[
                            item["product"]
                        ] = item["percentage"]

                if item["product"] in categories_fr["Épargne & Placement"]:
                    index = categories_fr["Épargne & Placement"].index(item["product"])
                    if st.session_state.english:
                        local_recommendations_epargne_et_placement_categorie[
                            categories_eng["Épargne & Placement"][index]
                        ] = item["percentage"]
                    else:
                        local_recommendations_epargne_et_placement_categorie[
                            item["product"]
                        ] = item["percentage"]

                if item["product"] in categories_fr["Packs bancaires"]:
                    index = categories_fr["Packs bancaires"].index(item["product"])
                    if st.session_state.english:
                        local_recommendations_packs_bancaires_categorie[
                            categories_eng["Packs bancaires"][index]
                        ] = item["percentage"]
                    else:
                        local_recommendations_packs_bancaires_categorie[
                            item["product"]
                        ] = item["percentage"]

            if local_recommendations:
                cat = []
                j = 0
                for categ, reco in local_recommendations.items():
                    if reco:
                        cat.append(categ)
                i = 0
                ite_col1 = 0
                ite_col2 = 0
                cola1, colb1 = st.columns([1, 1])
                if len(cat) % 2 == 0:
                    ite_col1 = ite_col2 = len(cat) // 2
                else:
                    ite_col1 = (len(cat) + 1) // 2
                    ite_col2 = len(cat) - ite_col1
                with cola1:
                    for ite in range(ite_col1):
                        with st.container(border=True):
                            with st.container(border=True):
                                st.markdown(
                                    f"""
                                        <p style='font-family:Arial; font-size:14px; font-weight:bold;'>
                                            {cat[i]}
                                        </p>
                                        """,
                                    unsafe_allow_html=True,
                                )
                            k = 0
                            for reco, perc in local_recommendations[cat[i]].items():
                                col11a, col22b = st.columns([1, 4])
                                with col11a:
                                    if cat[i] == C:
                                        img = "images/comptes"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == Ca:
                                        img = "images/cartes"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == F:
                                        img = "images/Financement immobilier"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == Fi:
                                        img = "images/financement à la consommation"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == A:
                                        img = "images/assurance"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == R:
                                        img = "images/retraite & Prévoyance"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == E:
                                        img = "images/Épargne et Placement"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == P:
                                        img = "images/packs bancaires"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                with col22b:
                                    st.markdown(
                                        f"""
                                            <p style='font-family:Arial; font-size:12px; font-weight:bold;'>
                                                {reco}
                                            </p>
                                            """,
                                        unsafe_allow_html=True,
                                    )
                                    if (
                                        reco == "Produit - Compte chèque en DH"
                                        or reco == "Product - Checking account in MAD"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Compte_chèque_en_DH}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Compte chèque en devises"
                                        or reco
                                        == "Product - Checking account in foreign currency"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Compte_chèque_en_devises}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Compte sur carnet"
                                        or reco == "Product - Savings account"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Compte_sur_carnet}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Carte basique"
                                        or reco == "Product - Basic card"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Carte_basique}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Carte Visa"
                                        or reco == "Product - Visa card"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Carte_Visa}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Carte Visa Premium"
                                        or reco == "Product - Visa Premium card"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Carte_Visa_Premium}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Carte Visa Elite"
                                        or reco == "Product - Visa Elite card"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Carte_Visa_Elite}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Carte Visa Infinite"
                                        or reco == "Product - Visa Infinite card"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Carte_Visa_Infinite}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco
                                        == "Produit - Crédit Immo avec garantie hypothécaire"
                                        or reco
                                        == "Product - Mortgage loan with real estate guarantee"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Crédit_Immo_avec_garantie_hypothécaire}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco
                                        == "Produit - Crédit Immo avec garantie liquide"
                                        or reco
                                        == "Product - Mortgage loan with cash guarantee"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Crédit_Immo_avec_garantie_liquide}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco
                                        == "Produit - Crédit Immo avec remboursement in fine"
                                        or reco
                                        == "Product - Mortgage loan with bullet repayment"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Crédit_Immo_avec_remboursement_in_fine}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Crédit Immo subventionné"
                                        or reco == "Product - Subsidized mortgage loan"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Crédit_Immo_subventionné}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco
                                        == "Produit - Crédit à la consommation non affecté"
                                        or reco == "Product - Unsecured consumer loan"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Crédit_à_la_consommation_non_affecté}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Crédit Auto"
                                        or reco == "Product - Auto loan"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Crédit_Auto}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Découvert"
                                        or reco == "Product - Overdraft facility"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Découvert}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco
                                        == "Produit - Assurance décès invalidité adossée à un financement"
                                        or reco
                                        == "Product - Death and disability insurance linked to a loan"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Assurance_décès_invalidité_adossée_à_un_financement}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco
                                        == "Produit - Assurance décès toutes causes"
                                        or reco == "Product - All-cause death insurance"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Assurance_décès_toutes_causes}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Multirisques bâtiment"
                                        or reco
                                        == "Product - Multi-risk building insurance"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Multirisques_bâtiment}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Maladie complémentaire"
                                        or reco
                                        == "Product - Supplementary health insurance"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Maladie_complémentaire}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Retraite complémentaire"
                                        or reco
                                        == "Product - Supplementary retirement plan"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Retraite_complémentaire}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco
                                        == "Produit - Retraite complémentaire en UC"
                                        or reco
                                        == "Product - Unit-linked supplementary retirement plan"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Retraite_complémentaire_en_UC}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Épargne Éducation"
                                        or reco == "Product - Education savings plan"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Épargne_Éducation}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Épargne Logement"
                                        or reco == "Product - Housing savings plan"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Épargne_Logement}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - OPCVM monétaires"
                                        or reco
                                        == "Product - Money market mutual fund (OPCVM)"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {OPCVM_monétaires}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - OPCVM obligataires"
                                        or reco == "Product - Bond mutual fund (OPCVM)"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {OPCVM_obligataires}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - OPCVM diversifiés"
                                        or reco
                                        == "Product - Diversified mutual fund (OPCVM)"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {OPCVM_diversifiés}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - OPCVM actions"
                                        or reco
                                        == "Product - Equity mutual fund (OPCVM)"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {OPCVM_actions}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Pack bancaire basique"
                                        or reco == "Product - Basic banking package"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Pack_bancaire_basique}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Pack bancaire étoffé"
                                        or reco == "Product - Enhanced banking package"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Pack_bancaire_étoffé}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Compte à terme"
                                        or reco == "Product - Term deposit account"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Compte_à_terme}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    col1111111, col2222222, col3333333 = st.columns(
                                        [2, 2, 0.5]
                                    )
                                    with col1111111:
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {text_6}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    with col2222222:
                                        st.slider(
                                            label="Home",
                                            min_value=0.0,
                                            max_value=100.0,
                                            value=float(perc),
                                            step=0.1,
                                            disabled=True,
                                            label_visibility="hidden",
                                            width="stretch",
                                            key=f"a_{j}",
                                        )
                                    col2b, col3b = st.columns([2, 3])
                                    with col2b:
                                        st.button(
                                            (
                                                "En savoir plus / Souscrire"
                                                if st.session_state.english != True
                                                else "Learn more / Subscribe"
                                            ),
                                            type="tertiary",
                                            width="stretch",
                                            key=f"btn_a_{j}",
                                            on_click=switch_page_produit,
                                            args=(reco,),
                                        )
                                    with col3b:
                                        st.button(
                                            (
                                                "Estimer le coût / Obtenir un devis"
                                                if st.session_state.english != True
                                                else "Estimate cost / Get a quote"
                                            ),
                                            type="secondary",
                                            width="stretch",
                                            key=f"btn_b_{j}",
                                        )
                                if k < len(local_recommendations[cat[i]]) - 1:
                                    st.markdown(
                                        """
                                                <hr style="margin-top:5px; margin-bottom:5px;">
                                                """,
                                        unsafe_allow_html=True,
                                    )
                                    k = k + 1
                                j = j + 1
                            i = i + 1
                with colb1:
                    for ite in range(ite_col2):
                        with st.container(border=True):
                            with st.container(border=True):
                                st.markdown(
                                    f"""
                                        <p style='font-family:Arial; font-size:14px; font-weight:bold;'>
                                            {cat[i]}
                                        </p>
                                        """,
                                    unsafe_allow_html=True,
                                )
                            k = 0
                            for reco, perc in local_recommendations[cat[i]].items():
                                col11a, col22b = st.columns([1, 4])
                                with col11a:
                                    if cat[i] == C:
                                        img = "images/comptes"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == Ca:
                                        img = "images/cartes"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == F:
                                        img = "images/Financement immobilier"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == Fi:
                                        img = "images/financement à la consommation"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == A:
                                        img = "images/assurance"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == R:
                                        img = "images/retraite & Prévoyance"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == E:
                                        img = "images/Épargne et Placement"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == P:
                                        img = "images/packs bancaires"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                with col22b:
                                    st.markdown(
                                        f"""
                                            <p style='font-family:Arial; font-size:12px; font-weight:bold;'>
                                                {reco}
                                            </p>
                                            """,
                                        unsafe_allow_html=True,
                                    )
                                    if (
                                        reco == "Produit - Compte chèque en DH"
                                        or reco == "Product - Checking account in MAD"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Compte_chèque_en_DH}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Compte chèque en devises"
                                        or reco
                                        == "Product - Checking account in foreign currency"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Compte_chèque_en_devises}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Compte sur carnet"
                                        or reco == "Product - Savings account"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Compte_sur_carnet}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Carte basique"
                                        or reco == "Product - Basic card"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Carte_basique}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Carte Visa"
                                        or reco == "Product - Visa card"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Carte_Visa}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Carte Visa Premium"
                                        or reco == "Product - Visa Premium card"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Carte_Visa_Premium}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Carte Visa Elite"
                                        or reco == "Product - Visa Elite card"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Carte_Visa_Elite}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Carte Visa Infinite"
                                        or reco == "Product - Visa Infinite card"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Carte_Visa_Infinite}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco
                                        == "Produit - Crédit Immo avec garantie hypothécaire"
                                        or reco
                                        == "Product - Mortgage loan with real estate guarantee"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Crédit_Immo_avec_garantie_hypothécaire}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco
                                        == "Produit - Crédit Immo avec garantie liquide"
                                        or reco
                                        == "Product - Mortgage loan with cash guarantee"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Crédit_Immo_avec_garantie_liquide}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco
                                        == "Produit - Crédit Immo avec remboursement in fine"
                                        or reco
                                        == "Product - Mortgage loan with bullet repayment"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Crédit_Immo_avec_remboursement_in_fine}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Crédit Immo subventionné"
                                        or reco == "Product - Subsidized mortgage loan"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Crédit_Immo_subventionné}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco
                                        == "Produit - Crédit à la consommation non affecté"
                                        or reco == "Product - Unsecured consumer loan"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Crédit_à_la_consommation_non_affecté}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Crédit Auto"
                                        or reco == "Product - Auto loan"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Crédit_Auto}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Découvert"
                                        or reco == "Product - Overdraft facility"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Découvert}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco
                                        == "Produit - Assurance décès invalidité adossée à un financement"
                                        or reco
                                        == "Product - Death and disability insurance linked to a loan"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Assurance_décès_invalidité_adossée_à_un_financement}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco
                                        == "Produit - Assurance décès toutes causes"
                                        or reco == "Product - All-cause death insurance"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Assurance_décès_toutes_causes}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Multirisques bâtiment"
                                        or reco
                                        == "Product - Multi-risk building insurance"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Multirisques_bâtiment}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Maladie complémentaire"
                                        or reco
                                        == "Product - Supplementary health insurance"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Maladie_complémentaire}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Retraite complémentaire"
                                        or reco
                                        == "Product - Supplementary retirement plan"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Retraite_complémentaire}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco
                                        == "Produit - Retraite complémentaire en UC"
                                        or reco
                                        == "Product - Unit-linked supplementary retirement plan"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Retraite_complémentaire_en_UC}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Épargne Éducation"
                                        or reco == "Product - Education savings plan"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Épargne_Éducation}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Épargne Logement"
                                        or reco == "Product - Housing savings plan"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Épargne_Logement}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - OPCVM monétaires"
                                        or reco
                                        == "Product - Money market mutual fund (OPCVM)"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {OPCVM_monétaires}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - OPCVM obligataires"
                                        or reco == "Product - Bond mutual fund (OPCVM)"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {OPCVM_obligataires}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - OPCVM diversifiés"
                                        or reco
                                        == "Product - Diversified mutual fund (OPCVM)"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {OPCVM_diversifiés}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - OPCVM actions"
                                        or reco
                                        == "Product - Equity mutual fund (OPCVM)"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {OPCVM_actions}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Pack bancaire basique"
                                        or reco == "Product - Basic banking package"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Pack_bancaire_basique}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Pack bancaire étoffé"
                                        or reco == "Product - Enhanced banking package"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Pack_bancaire_étoffé}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Compte à terme"
                                        or reco == "Product - Term deposit account"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Compte_à_terme}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    col1111111, col2222222, col3333333 = st.columns(
                                        [2, 2, 0.5]
                                    )
                                    with col1111111:
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {text_6}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    with col2222222:
                                        st.slider(
                                            label="Homee",
                                            min_value=0.0,
                                            max_value=100.0,
                                            value=float(perc),
                                            step=0.1,
                                            disabled=True,
                                            label_visibility="hidden",
                                            width="stretch",
                                            key=f"b_{j}",
                                        )
                                    col2b, col3b = st.columns([2, 3])
                                    with col2b:
                                        st.button(
                                            (
                                                "En savoir plus / Souscrire"
                                                if st.session_state.english != True
                                                else "Learn more / Subscribe"
                                            ),
                                            type="tertiary",
                                            width="stretch",
                                            key=f"btn_c_{j}",
                                            on_click=switch_page_produit,
                                            args=(reco,),
                                        )
                                    with col3b:
                                        st.button(
                                            (
                                                "Estimer le coût / Obtenir un devis"
                                                if st.session_state.english != True
                                                else "Estimate cost / Get a quote"
                                            ),
                                            type="secondary",
                                            width="stretch",
                                            key=f"btn_d_{j}",
                                        )
                                if k < len(local_recommendations[cat[i]]) - 1:
                                    st.markdown(
                                        """
                                                <hr style="margin-top:5px; margin-bottom:5px;">
                                                """,
                                        unsafe_allow_html=True,
                                    )
                                    k = k + 1
                                j = j + 1
                            i = i + 1
    with st.container(border=True):
        text_7 = (
            "Recommandations basées sur les experts"
            if st.session_state.english != True
            else "Recommendations based on experts"
        )
        st.markdown(
            f"""
        <p style='font-family:Arial; font-size:24px; font-weight:bold;'>
        {text_7}
        </p>
        """,
            unsafe_allow_html=True,
        )
        if os.path.exists(expert_recommendations_output_file):
            with open(expert_recommendations_output_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            for item in data:
                if item["product"] in categories_fr["Comptes"]:
                    index = categories_fr["Comptes"].index(item["product"])
                    if st.session_state.english:
                        expert_recommendations_comptes_categorie.append(
                            categories_eng["Comptes"][index]
                        )
                    else:
                        expert_recommendations_comptes_categorie.append(item["product"])

                if item["product"] in categories_fr["Cartes"]:
                    index = categories_fr["Cartes"].index(item["product"])
                    if st.session_state.english:
                        expert_recommendations_cartes_categorie.append(
                            categories_eng["Cartes"][index]
                        )
                    else:
                        expert_recommendations_cartes_categorie.append(item["product"])

                if item["product"] in categories_fr["Financement immobilier"]:
                    index = categories_fr["Financement immobilier"].index(
                        item["product"]
                    )
                    if st.session_state.english:
                        expert_recommendations_financement_immobilier_categorie.append(
                            categories_eng["Financement immobilier"][index]
                        )
                    else:
                        expert_recommendations_financement_immobilier_categorie.append(
                            item["product"]
                        )

                if item["product"] in categories_fr["Financement à la consommation"]:
                    index = categories_fr["Financement à la consommation"].index(
                        item["product"]
                    )
                    if st.session_state.english:
                        expert_recommendations_financement_à_la_consommation_categorie.append(
                            categories_eng["Financement à la consommation"][index]
                        )
                    else:
                        expert_recommendations_financement_à_la_consommation_categorie.append(
                            item["product"]
                        )

                if item["product"] in categories_fr["Assurance"]:
                    index = categories_fr["Assurance"].index(item["product"])
                    if st.session_state.english:
                        expert_recommendations_assurance_categorie.append(
                            categories_eng["Assurance"][index]
                        )
                    else:
                        expert_recommendations_assurance_categorie.append(
                            item["product"]
                        )

                if item["product"] in categories_fr["Retraite & Prévoyance"]:
                    index = categories_fr["Retraite & Prévoyance"].index(
                        item["product"]
                    )
                    if st.session_state.english:
                        expert_recommendations_retraite_et_prévoyance_categorie.append(
                            categories_eng["Retraite & Prévoyance"][index]
                        )
                    else:
                        expert_recommendations_retraite_et_prévoyance_categorie.append(
                            item["product"]
                        )

                if item["product"] in categories_fr["Épargne & Placement"]:
                    index = categories_fr["Épargne & Placement"].index(item["product"])
                    if st.session_state.english:
                        expert_recommendations_epargne_et_placement_categorie.append(
                            categories_eng["Épargne & Placement"][index]
                        )
                    else:
                        expert_recommendations_epargne_et_placement_categorie.append(
                            item["product"]
                        )

                if item["product"] in categories_fr["Packs bancaires"]:
                    index = categories_fr["Packs bancaires"].index(item["product"])
                    if st.session_state.english:
                        expert_recommendations_packs_bancaires_categorie.append(
                            categories_eng["Packs bancaires"][index]
                        )
                    else:
                        expert_recommendations_packs_bancaires_categorie.append(
                            item["product"]
                        )
            if expert_recommendations:
                cat = []
                j = 0
                for categ, reco in expert_recommendations.items():
                    if reco:
                        cat.append(categ)
                i = 0
                ite_col1 = 0
                ite_col2 = 0
                cola1, colb1 = st.columns([1, 1])
                if len(cat) % 2 == 0:
                    ite_col1 = ite_col2 = len(cat) // 2
                else:
                    ite_col1 = (len(cat) + 1) // 2
                    ite_col2 = len(cat) - ite_col1
                with cola1:
                    for ite in range(ite_col1):
                        with st.container(border=True):
                            with st.container(border=True):
                                st.markdown(
                                    f"""
                                        <p style='font-family:Arial; font-size:14px; font-weight:bold;'>
                                            {cat[i]}
                                        </p>
                                        """,
                                    unsafe_allow_html=True,
                                )
                            k = 0
                            for reco in expert_recommendations[cat[i]]:
                                col11a, col22b = st.columns([1, 4])
                                with col11a:
                                    if cat[i] == C:
                                        img = "images/comptes"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == Ca:
                                        img = "images/cartes"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == F:
                                        img = "images/Financement immobilier"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == Fi:
                                        img = "images/financement à la consommation"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == A:
                                        img = "images/assurance"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == R:
                                        img = "images/retraite & Prévoyance"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == E:
                                        img = "images/Épargne et Placement"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == P:
                                        img = "images/packs bancaires"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                with col22b:
                                    st.markdown(
                                        f"""
                                            <p style='font-family:Arial; font-size:12px; font-weight:bold;'>
                                                {reco}
                                            </p>
                                            """,
                                        unsafe_allow_html=True,
                                    )
                                    if (
                                        reco == "Produit - Compte chèque en DH"
                                        or reco == "Product - Checking account in MAD"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Compte_chèque_en_DH}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Compte chèque en devises"
                                        or reco
                                        == "Product - Checking account in foreign currency"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Compte_chèque_en_devises}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Compte sur carnet"
                                        or reco == "Product - Savings account"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Compte_sur_carnet}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Carte basique"
                                        or reco == "Product - Basic card"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Carte_basique}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Carte Visa"
                                        or reco == "Product - Visa card"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Carte_Visa}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Carte Visa Premium"
                                        or reco == "Product - Visa Premium card"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Carte_Visa_Premium}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Carte Visa Elite"
                                        or reco == "Product - Visa Elite card"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Carte_Visa_Elite}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Carte Visa Infinite"
                                        or reco == "Product - Visa Infinite card"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Carte_Visa_Infinite}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco
                                        == "Produit - Crédit Immo avec garantie hypothécaire"
                                        or reco
                                        == "Product - Mortgage loan with real estate guarantee"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Crédit_Immo_avec_garantie_hypothécaire}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco
                                        == "Produit - Crédit Immo avec garantie liquide"
                                        or reco
                                        == "Product - Mortgage loan with cash guarantee"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Crédit_Immo_avec_garantie_liquide}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco
                                        == "Produit - Crédit Immo avec remboursement in fine"
                                        or reco
                                        == "Product - Mortgage loan with bullet repayment"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Crédit_Immo_avec_remboursement_in_fine}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Crédit Immo subventionné"
                                        or reco == "Product - Subsidized mortgage loan"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Crédit_Immo_subventionné}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco
                                        == "Produit - Crédit à la consommation non affecté"
                                        or reco == "Product - Unsecured consumer loan"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Crédit_à_la_consommation_non_affecté}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Crédit Auto"
                                        or reco == "Product - Auto loan"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Crédit_Auto}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Découvert"
                                        or reco == "Product - Overdraft facility"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Découvert}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco
                                        == "Produit - Assurance décès invalidité adossée à un financement"
                                        or reco
                                        == "Product - Death and disability insurance linked to a loan"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Assurance_décès_invalidité_adossée_à_un_financement}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco
                                        == "Produit - Assurance décès toutes causes"
                                        or reco == "Product - All-cause death insurance"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Assurance_décès_toutes_causes}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Multirisques bâtiment"
                                        or reco
                                        == "Product - Multi-risk building insurance"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Multirisques_bâtiment}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Maladie complémentaire"
                                        or reco
                                        == "Product - Supplementary health insurance"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Maladie_complémentaire}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Retraite complémentaire"
                                        or reco
                                        == "Product - Supplementary retirement plan"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Retraite_complémentaire}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco
                                        == "Produit - Retraite complémentaire en UC"
                                        or reco
                                        == "Product - Unit-linked supplementary retirement plan"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Retraite_complémentaire_en_UC}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Épargne Éducation"
                                        or reco == "Product - Education savings plan"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Épargne_Éducation}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Épargne Logement"
                                        or reco == "Product - Housing savings plan"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Épargne_Logement}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - OPCVM monétaires"
                                        or reco
                                        == "Product - Money market mutual fund (OPCVM)"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {OPCVM_monétaires}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - OPCVM obligataires"
                                        or reco == "Product - Bond mutual fund (OPCVM)"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {OPCVM_obligataires}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - OPCVM diversifiés"
                                        or reco
                                        == "Product - Diversified mutual fund (OPCVM)"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {OPCVM_diversifiés}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - OPCVM actions"
                                        or reco
                                        == "Product - Equity mutual fund (OPCVM)"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {OPCVM_actions}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Pack bancaire basique"
                                        or reco == "Product - Basic banking package"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Pack_bancaire_basique}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Pack bancaire étoffé"
                                        or reco == "Product - Enhanced banking package"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Pack_bancaire_étoffé}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Compte à terme"
                                        or reco == "Product - Term deposit account"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Compte_à_terme}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    col1111111, col2222222, col3333333 = st.columns(
                                        [2, 2, 0.5]
                                    )
                                    col2b, col3b = st.columns([2, 3])
                                    with col2b:
                                        st.button(
                                            (
                                                "En savoir plus / Souscrire"
                                                if st.session_state.english != True
                                                else "Learn more / Subscribe"
                                            ),
                                            type="tertiary",
                                            width="stretch",
                                            key=f"btn_e_{j}",
                                            on_click=switch_page_produit,
                                            args=(reco,),
                                        )
                                    with col3b:
                                        st.button(
                                            (
                                                "Estimer le coût / Obtenir un devis"
                                                if st.session_state.english != True
                                                else "Estimate cost / Get a quote"
                                            ),
                                            type="secondary",
                                            width="stretch",
                                            key=f"btn_g_{j}",
                                        )
                                if k < len(expert_recommendations[cat[i]]) - 1:
                                    st.markdown(
                                        """
                                                <hr style="margin-top:5px; margin-bottom:5px;">
                                                """,
                                        unsafe_allow_html=True,
                                    )
                                    k = k + 1
                                j = j + 1
                            i = i + 1
                with colb1:
                    for ite in range(ite_col2):
                        with st.container(border=True):
                            with st.container(border=True):
                                st.markdown(
                                    f"""
                                        <p style='font-family:Arial; font-size:14px; font-weight:bold;'>
                                            {cat[i]}
                                        </p>
                                        """,
                                    unsafe_allow_html=True,
                                )
                            k = 0
                            for reco in expert_recommendations[cat[i]]:
                                col11a, col22b = st.columns([1, 4])
                                with col11a:
                                    if cat[i] == C:
                                        img = "images/comptes"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == Ca:
                                        img = "images/cartes"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == F:
                                        img = "images/Financement immobilier"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == Fi:
                                        img = "images/financement à la consommation"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == A:
                                        img = "images/assurance"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == R:
                                        img = "images/retraite & Prévoyance"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == E:
                                        img = "images/Épargne et Placement"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == P:
                                        img = "images/packs bancaires"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                with col22b:
                                    st.markdown(
                                        f"""
                                            <p style='font-family:Arial; font-size:12px; font-weight:bold;'>
                                                {reco}
                                            </p>
                                            """,
                                        unsafe_allow_html=True,
                                    )
                                    if (
                                        reco == "Produit - Compte chèque en DH"
                                        or reco == "Product - Checking account in MAD"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Compte_chèque_en_DH}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Compte chèque en devises"
                                        or reco
                                        == "Product - Checking account in foreign currency"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Compte_chèque_en_devises}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Compte sur carnet"
                                        or reco == "Product - Savings account"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Compte_sur_carnet}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Carte basique"
                                        or reco == "Product - Basic card"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Carte_basique}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Carte Visa"
                                        or reco == "Product - Visa card"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Carte_Visa}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Carte Visa Premium"
                                        or reco == "Product - Visa Premium card"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Carte_Visa_Premium}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Carte Visa Elite"
                                        or reco == "Product - Visa Elite card"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Carte_Visa_Elite}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Carte Visa Infinite"
                                        or reco == "Product - Visa Infinite card"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Carte_Visa_Infinite}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco
                                        == "Produit - Crédit Immo avec garantie hypothécaire"
                                        or reco
                                        == "Product - Mortgage loan with real estate guarantee"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Crédit_Immo_avec_garantie_hypothécaire}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco
                                        == "Produit - Crédit Immo avec garantie liquide"
                                        or reco
                                        == "Product - Mortgage loan with cash guarantee"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Crédit_Immo_avec_garantie_liquide}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco
                                        == "Produit - Crédit Immo avec remboursement in fine"
                                        or reco
                                        == "Product - Mortgage loan with bullet repayment"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Crédit_Immo_avec_remboursement_in_fine}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Crédit Immo subventionné"
                                        or reco == "Product - Subsidized mortgage loan"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Crédit_Immo_subventionné}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco
                                        == "Produit - Crédit à la consommation non affecté"
                                        or reco == "Product - Unsecured consumer loan"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Crédit_à_la_consommation_non_affecté}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Crédit Auto"
                                        or reco == "Product - Auto loan"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Crédit_Auto}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Découvert"
                                        or reco == "Product - Overdraft facility"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Découvert}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco
                                        == "Produit - Assurance décès invalidité adossée à un financement"
                                        or reco
                                        == "Product - Death and disability insurance linked to a loan"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Assurance_décès_invalidité_adossée_à_un_financement}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco
                                        == "Produit - Assurance décès toutes causes"
                                        or reco == "Product - All-cause death insurance"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Assurance_décès_toutes_causes}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Multirisques bâtiment"
                                        or reco
                                        == "Product - Multi-risk building insurance"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Multirisques_bâtiment}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Maladie complémentaire"
                                        or reco
                                        == "Product - Supplementary health insurance"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Maladie_complémentaire}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Retraite complémentaire"
                                        or reco
                                        == "Product - Supplementary retirement plan"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Retraite_complémentaire}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco
                                        == "Produit - Retraite complémentaire en UC"
                                        or reco
                                        == "Product - Unit-linked supplementary retirement plan"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Retraite_complémentaire_en_UC}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Épargne Éducation"
                                        or reco == "Product - Education savings plan"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Épargne_Éducation}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Épargne Logement"
                                        or reco == "Product - Housing savings plan"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Épargne_Logement}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - OPCVM monétaires"
                                        or reco
                                        == "Product - Money market mutual fund (OPCVM)"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {OPCVM_monétaires}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - OPCVM obligataires"
                                        or reco == "Product - Bond mutual fund (OPCVM)"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {OPCVM_obligataires}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - OPCVM diversifiés"
                                        or reco
                                        == "Product - Diversified mutual fund (OPCVM)"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {OPCVM_diversifiés}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - OPCVM actions"
                                        or reco
                                        == "Product - Equity mutual fund (OPCVM)"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {OPCVM_actions}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Pack bancaire basique"
                                        or reco == "Product - Basic banking package"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Pack_bancaire_basique}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Pack bancaire étoffé"
                                        or reco == "Product - Enhanced banking package"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Pack_bancaire_étoffé}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Compte à terme"
                                        or reco == "Product - Term deposit account"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Compte_à_terme}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    col1111111, col2222222, col3333333 = st.columns(
                                        [2, 2, 0.5]
                                    )
                                    col2b, col3b = st.columns([2, 3])
                                    with col2b:
                                        st.button(
                                            (
                                                "En savoir plus / Souscrire"
                                                if st.session_state.english != True
                                                else "Learn more / Subscribe"
                                            ),
                                            type="tertiary",
                                            width="stretch",
                                            key=f"btn_f_{j}",
                                            on_click=switch_page_produit,
                                            args=(reco,),
                                        )
                                    with col3b:
                                        st.button(
                                            (
                                                "Estimer le coût / Obtenir un devis"
                                                if st.session_state.english != True
                                                else "Estimate cost / Get a quote"
                                            ),
                                            type="secondary",
                                            width="stretch",
                                            key=f"btn_k_{j}",
                                        )
                                if k < len(expert_recommendations[cat[i]]) - 1:
                                    st.markdown(
                                        """
                                                <hr style="margin-top:5px; margin-bottom:5px;">
                                                """,
                                        unsafe_allow_html=True,
                                    )
                                    k = k + 1
                                j = j + 1
                            i = i + 1

    with st.container(border=True):
        text_8 = (
            "Recommandations basées sur le marché bancaire"
            if st.session_state.english != True
            else "Recommendations based on the banking market"
        )
        st.markdown(
            f"""
                    <p style='font-family:Arial; font-size:24px; font-weight:bold;'>
                        {text_8}
                    </p>
                    """,
            unsafe_allow_html=True,
        )
        if os.path.exists(meta_recommendations_output_file):
            with open(meta_recommendations_output_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            for item in data:
                if item["product"] in categories_fr["Comptes"]:
                    index = categories_fr["Comptes"].index(item["product"])
                    if st.session_state.english:
                        meta_recommendations_comptes_categorie[
                            categories_eng["Comptes"][index]
                        ] = item["percentage"]
                    else:
                        meta_recommendations_comptes_categorie[item["product"]] = item[
                            "percentage"
                        ]

                if item["product"] in categories_fr["Cartes"]:
                    index = categories_fr["Cartes"].index(item["product"])
                    if st.session_state.english:
                        meta_recommendations_cartes_categorie[
                            categories_eng["Cartes"][index]
                        ] = item["percentage"]
                    else:
                        meta_recommendations_cartes_categorie[item["product"]] = item[
                            "percentage"
                        ]

                if item["product"] in categories_fr["Financement immobilier"]:
                    index = categories_fr["Financement immobilier"].index(
                        item["product"]
                    )
                    if st.session_state.english:
                        meta_recommendations_financement_immobilier_categorie[
                            categories_eng["Financement immobilier"][index]
                        ] = item["percentage"]
                    else:
                        meta_recommendations_financement_immobilier_categorie[
                            item["product"]
                        ] = item["percentage"]

                if item["product"] in categories_fr["Financement à la consommation"]:
                    index = categories_fr["Financement à la consommation"].index(
                        item["product"]
                    )
                    if st.session_state.english:
                        meta_recommendations_financement_à_la_consommation_categorie[
                            categories_eng["Financement à la consommation"][index]
                        ] = item["percentage"]
                    else:
                        meta_recommendations_financement_à_la_consommation_categorie[
                            item["product"]
                        ] = item["percentage"]

                if item["product"] in categories_fr["Assurance"]:
                    index = categories_fr["Assurance"].index(item["product"])
                    if st.session_state.english:
                        meta_recommendations_assurance_categorie[
                            categories_eng["Assurance"][index]
                        ] = item["percentage"]
                    else:
                        meta_recommendations_assurance_categorie[item["product"]] = (
                            item["percentage"]
                        )

                if item["product"] in categories_fr["Retraite & Prévoyance"]:
                    index = categories_fr["Retraite & Prévoyance"].index(
                        item["product"]
                    )
                    if st.session_state.english:
                        meta_recommendations_retraite_et_prévoyance_categorie[
                            categories_eng["Retraite & Prévoyance"][index]
                        ] = item["percentage"]
                    else:
                        meta_recommendations_retraite_et_prévoyance_categorie[
                            item["product"]
                        ] = item["percentage"]

                if item["product"] in categories_fr["Épargne & Placement"]:
                    index = categories_fr["Épargne & Placement"].index(item["product"])
                    if st.session_state.english:
                        meta_recommendations_epargne_et_placement_categorie[
                            categories_eng["Épargne & Placement"][index]
                        ] = item["percentage"]
                    else:
                        meta_recommendations_epargne_et_placement_categorie[
                            item["product"]
                        ] = item["percentage"]

                if item["product"] in categories_fr["Packs bancaires"]:
                    index = categories_fr["Packs bancaires"].index(item["product"])
                    if st.session_state.english:
                        meta_recommendations_packs_bancaires_categorie[
                            categories_eng["Packs bancaires"][index]
                        ] = item["percentage"]
                    else:
                        meta_recommendations_packs_bancaires_categorie[
                            item["product"]
                        ] = item["percentage"]
            if meta_recommendations:
                cat = []
                j = 0
                for categ, reco in meta_recommendations.items():
                    if reco:
                        cat.append(categ)
                i = 0
                ite_col1 = 0
                ite_col2 = 0
                cola1, colb1 = st.columns([1, 1])
                if len(cat) % 2 == 0:
                    ite_col1 = ite_col2 = len(cat) // 2
                else:
                    ite_col1 = (len(cat) + 1) // 2
                    ite_col2 = len(cat) - ite_col1
                with cola1:
                    for ite in range(ite_col1):
                        with st.container(border=True):
                            with st.container(border=True):
                                st.markdown(
                                    f"""
                                        <p style='font-family:Arial; font-size:14px; font-weight:bold;'>
                                            {cat[i]}
                                        </p>
                                        """,
                                    unsafe_allow_html=True,
                                )
                            k = 0
                            for reco, perc in meta_recommendations[cat[i]].items():
                                col11a, col22b = st.columns([1, 4])
                                with col11a:
                                    if cat[i] == C:
                                        img = "images/comptes"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == Ca:
                                        img = "images/cartes"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == F:
                                        img = "images/Financement immobilier"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == Fi:
                                        img = "images/financement à la consommation"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == A:
                                        img = "images/assurance"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == R:
                                        img = "images/retraite & Prévoyance"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == E:
                                        img = "images/Épargne et Placement"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == P:
                                        img = "images/packs bancaires"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                with col22b:
                                    st.markdown(
                                        f"""
                                            <p style='font-family:Arial; font-size:12px; font-weight:bold;'>
                                                {reco}
                                            </p>
                                            """,
                                        unsafe_allow_html=True,
                                    )
                                    if (
                                        reco == "Produit - Compte chèque en DH"
                                        or reco == "Product - Checking account in MAD"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Compte_chèque_en_DH}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Compte chèque en devises"
                                        or reco
                                        == "Product - Checking account in foreign currency"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Compte_chèque_en_devises}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Compte sur carnet"
                                        or reco == "Product - Savings account"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Compte_sur_carnet}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Carte basique"
                                        or reco == "Product - Basic card"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Carte_basique}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Carte Visa"
                                        or reco == "Product - Visa card"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Carte_Visa}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Carte Visa Premium"
                                        or reco == "Product - Visa Premium card"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Carte_Visa_Premium}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Carte Visa Elite"
                                        or reco == "Product - Visa Elite card"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Carte_Visa_Elite}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Carte Visa Infinite"
                                        or reco == "Product - Visa Infinite card"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Carte_Visa_Infinite}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco
                                        == "Produit - Crédit Immo avec garantie hypothécaire"
                                        or reco
                                        == "Product - Mortgage loan with real estate guarantee"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Crédit_Immo_avec_garantie_hypothécaire}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco
                                        == "Produit - Crédit Immo avec garantie liquide"
                                        or reco
                                        == "Product - Mortgage loan with cash guarantee"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Crédit_Immo_avec_garantie_liquide}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco
                                        == "Produit - Crédit Immo avec remboursement in fine"
                                        or reco
                                        == "Product - Mortgage loan with bullet repayment"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Crédit_Immo_avec_remboursement_in_fine}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Crédit Immo subventionné"
                                        or reco == "Product - Subsidized mortgage loan"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Crédit_Immo_subventionné}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco
                                        == "Produit - Crédit à la consommation non affecté"
                                        or reco == "Product - Unsecured consumer loan"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Crédit_à_la_consommation_non_affecté}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Crédit Auto"
                                        or reco == "Product - Auto loan"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Crédit_Auto}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Découvert"
                                        or reco == "Product - Overdraft facility"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Découvert}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco
                                        == "Produit - Assurance décès invalidité adossée à un financement"
                                        or reco
                                        == "Product - Death and disability insurance linked to a loan"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Assurance_décès_invalidité_adossée_à_un_financement}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco
                                        == "Produit - Assurance décès toutes causes"
                                        or reco == "Product - All-cause death insurance"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Assurance_décès_toutes_causes}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Multirisques bâtiment"
                                        or reco
                                        == "Product - Multi-risk building insurance"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Multirisques_bâtiment}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Maladie complémentaire"
                                        or reco
                                        == "Product - Supplementary health insurance"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Maladie_complémentaire}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Retraite complémentaire"
                                        or reco
                                        == "Product - Supplementary retirement plan"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Retraite_complémentaire}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco
                                        == "Produit - Retraite complémentaire en UC"
                                        or reco
                                        == "Product - Unit-linked supplementary retirement plan"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Retraite_complémentaire_en_UC}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Épargne Éducation"
                                        or reco == "Product - Education savings plan"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Épargne_Éducation}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Épargne Logement"
                                        or reco == "Product - Housing savings plan"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Épargne_Logement}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - OPCVM monétaires"
                                        or reco
                                        == "Product - Money market mutual fund (OPCVM)"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {OPCVM_monétaires}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - OPCVM obligataires"
                                        or reco == "Product - Bond mutual fund (OPCVM)"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {OPCVM_obligataires}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - OPCVM diversifiés"
                                        or reco
                                        == "Product - Diversified mutual fund (OPCVM)"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {OPCVM_diversifiés}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - OPCVM actions"
                                        or reco
                                        == "Product - Equity mutual fund (OPCVM)"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {OPCVM_actions}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Pack bancaire basique"
                                        or reco == "Product - Basic banking package"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Pack_bancaire_basique}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Pack bancaire étoffé"
                                        or reco == "Product - Enhanced banking package"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Pack_bancaire_étoffé}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Compte à terme"
                                        or reco == "Product - Term deposit account"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Compte_à_terme}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    col1111111, col2222222, col3333333 = st.columns(
                                        [2, 2, 0.5]
                                    )
                                    with col1111111:
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {text_6}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    with col2222222:
                                        st.slider(
                                            label="Homeee",
                                            min_value=0.0,
                                            max_value=100.0,
                                            value=float(perc),
                                            step=0.1,
                                            disabled=True,
                                            label_visibility="hidden",
                                            width="stretch",
                                            key=f"c_{j}",
                                        )
                                    col2b, col3b = st.columns([2, 3])
                                    with col2b:
                                        st.button(
                                            (
                                                "En savoir plus / Souscrire"
                                                if st.session_state.english != True
                                                else "Learn more / Subscribe"
                                            ),
                                            type="tertiary",
                                            width="stretch",
                                            key=f"btn_m_{j}",
                                            on_click=switch_page_produit,
                                            args=(reco,),
                                        )
                                    with col3b:
                                        st.button(
                                            (
                                                "Estimer le coût / Obtenir un devis"
                                                if st.session_state.english != True
                                                else "Estimate cost / Get a quote"
                                            ),
                                            type="secondary",
                                            width="stretch",
                                            key=f"btn_n_{j}",
                                        )
                                if k < len(meta_recommendations[cat[i]]) - 1:
                                    st.markdown(
                                        """
                                                <hr style="margin-top:5px; margin-bottom:5px;">
                                                """,
                                        unsafe_allow_html=True,
                                    )
                                    k = k + 1
                                j = j + 1
                            i = i + 1
                with colb1:
                    for ite in range(ite_col2):
                        with st.container(border=True):
                            with st.container(border=True):
                                st.markdown(
                                    f"""
                                        <p style='font-family:Arial; font-size:14px; font-weight:bold;'>
                                            {cat[i]}
                                        </p>
                                        """,
                                    unsafe_allow_html=True,
                                )
                            k = 0
                            for reco, perc in meta_recommendations[cat[i]].items():
                                col11a, col22b = st.columns([1, 4])
                                with col11a:
                                    if cat[i] == C:
                                        img = "images/comptes"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == Ca:
                                        img = "images/cartes"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == F:
                                        img = "images/Financement immobilier"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == Fi:
                                        img = "images/financement à la consommation"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == A:
                                        img = "images/assurance"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == R:
                                        img = "images/retraite & Prévoyance"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == E:
                                        img = "images/Épargne et Placement"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == P:
                                        img = "images/packs bancaires"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                with col22b:
                                    st.markdown(
                                        f"""
                                            <p style='font-family:Arial; font-size:12px; font-weight:bold;'>
                                                {reco}
                                            </p>
                                            """,
                                        unsafe_allow_html=True,
                                    )
                                    if (
                                        reco == "Produit - Compte chèque en DH"
                                        or reco == "Product - Checking account in MAD"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Compte_chèque_en_DH}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Compte chèque en devises"
                                        or reco
                                        == "Product - Checking account in foreign currency"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Compte_chèque_en_devises}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Compte sur carnet"
                                        or reco == "Product - Savings account"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Compte_sur_carnet}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Carte basique"
                                        or reco == "Product - Basic card"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Carte_basique}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Carte Visa"
                                        or reco == "Product - Visa card"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Carte_Visa}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Carte Visa Premium"
                                        or reco == "Product - Visa Premium card"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Carte_Visa_Premium}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Carte Visa Elite"
                                        or reco == "Product - Visa Elite card"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Carte_Visa_Elite}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Carte Visa Infinite"
                                        or reco == "Product - Visa Infinite card"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Carte_Visa_Infinite}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco
                                        == "Produit - Crédit Immo avec garantie hypothécaire"
                                        or reco
                                        == "Product - Mortgage loan with real estate guarantee"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Crédit_Immo_avec_garantie_hypothécaire}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco
                                        == "Produit - Crédit Immo avec garantie liquide"
                                        or reco
                                        == "Product - Mortgage loan with cash guarantee"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Crédit_Immo_avec_garantie_liquide}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco
                                        == "Produit - Crédit Immo avec remboursement in fine"
                                        or reco
                                        == "Product - Mortgage loan with bullet repayment"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Crédit_Immo_avec_remboursement_in_fine}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Crédit Immo subventionné"
                                        or reco == "Product - Subsidized mortgage loan"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Crédit_Immo_subventionné}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco
                                        == "Produit - Crédit à la consommation non affecté"
                                        or reco == "Product - Unsecured consumer loan"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Crédit_à_la_consommation_non_affecté}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Crédit Auto"
                                        or reco == "Product - Auto loan"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Crédit_Auto}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Découvert"
                                        or reco == "Product - Overdraft facility"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Découvert}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco
                                        == "Produit - Assurance décès invalidité adossée à un financement"
                                        or reco
                                        == "Product - Death and disability insurance linked to a loan"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Assurance_décès_invalidité_adossée_à_un_financement}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco
                                        == "Produit - Assurance décès toutes causes"
                                        or reco == "Product - All-cause death insurance"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Assurance_décès_toutes_causes}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Multirisques bâtiment"
                                        or reco
                                        == "Product - Multi-risk building insurance"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Multirisques_bâtiment}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Maladie complémentaire"
                                        or reco
                                        == "Product - Supplementary health insurance"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Maladie_complémentaire}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Retraite complémentaire"
                                        or reco
                                        == "Product - Supplementary retirement plan"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Retraite_complémentaire}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco
                                        == "Produit - Retraite complémentaire en UC"
                                        or reco
                                        == "Product - Unit-linked supplementary retirement plan"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Retraite_complémentaire_en_UC}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Épargne Éducation"
                                        or reco == "Product - Education savings plan"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Épargne_Éducation}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Épargne Logement"
                                        or reco == "Product - Housing savings plan"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Épargne_Logement}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - OPCVM monétaires"
                                        or reco
                                        == "Product - Money market mutual fund (OPCVM)"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {OPCVM_monétaires}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - OPCVM obligataires"
                                        or reco == "Product - Bond mutual fund (OPCVM)"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {OPCVM_obligataires}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - OPCVM diversifiés"
                                        or reco
                                        == "Product - Diversified mutual fund (OPCVM)"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {OPCVM_diversifiés}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - OPCVM actions"
                                        or reco
                                        == "Product - Equity mutual fund (OPCVM)"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {OPCVM_actions}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Pack bancaire basique"
                                        or reco == "Product - Basic banking package"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Pack_bancaire_basique}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Pack bancaire étoffé"
                                        or reco == "Product - Enhanced banking package"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Pack_bancaire_étoffé}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if (
                                        reco == "Produit - Compte à terme"
                                        or reco == "Product - Term deposit account"
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Compte_à_terme}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    col1111111, col2222222, col3333333 = st.columns(
                                        [2, 2, 0.5]
                                    )
                                    with col1111111:
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {text_6}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    with col2222222:
                                        st.slider(
                                            label="Homeeee",
                                            min_value=0.0,
                                            max_value=100.0,
                                            value=float(perc),
                                            step=0.1,
                                            disabled=True,
                                            label_visibility="hidden",
                                            width="stretch",
                                            key=f"d_{j}",
                                        )
                                    col2b, col3b = st.columns([2, 3])
                                    with col2b:
                                        st.button(
                                            (
                                                "En savoir plus / Souscrire"
                                                if st.session_state.english != True
                                                else "Learn more / Subscribe"
                                            ),
                                            type="tertiary",
                                            width="stretch",
                                            key=f"btn_x_{j}",
                                            on_click=switch_page_produit,
                                            args=(reco,),
                                        )
                                    with col3b:
                                        st.button(
                                            (
                                                "Estimer le coût / Obtenir un devis"
                                                if st.session_state.english != True
                                                else "Estimate cost / Get a quote"
                                            ),
                                            type="secondary",
                                            width="stretch",
                                            key=f"btn_y_{j}",
                                        )
                                if k < len(meta_recommendations[cat[i]]) - 1:
                                    st.markdown(
                                        """
                                                <hr style="margin-top:5px; margin-bottom:5px;">
                                                """,
                                        unsafe_allow_html=True,
                                    )
                                    k = k + 1
                                j = j + 1
                            i = i + 1
