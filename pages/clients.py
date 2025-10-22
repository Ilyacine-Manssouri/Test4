import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
from numpy.random import default_rng as rng
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


# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Clients",
    layout="wide",
    page_icon="images/NEURONAIZE-ICONE-BLANC.png",
)

if "data_frame" not in st.session_state or "client_index" not in st.session_state:
    st.switch_page("pages/page_d'accueil.py")

if st.session_state.client_index == "":
    st.switch_page("pages/page_d'accueil.py")

# --- CONSTANTES ---
CSS_PATH = pathlib.Path("assets/styles.css")
df = st.session_state.data_frame
client_index = int(st.session_state.client_index)
categories = {
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

local_recommendations_comptes_categorie = {}
local_recommendations_cartes_categorie = {}
local_recommendations_financement_immobilier_categorie = {}
local_recommendations_financement_à_la_consommation_categorie = {}
local_recommendations_assurance_categorie = {}
local_recommendations_retraite_et_prévoyance_categorie = {}
local_recommendations_epargne_et_placement_categorie = {}
local_recommendations_packs_bancaires_categorie = {}
local_recommendations = {
    "Comptes": local_recommendations_comptes_categorie,
    "Cartes": local_recommendations_cartes_categorie,
    "Financement immobilier": local_recommendations_financement_immobilier_categorie,
    "Financement à la consommation": local_recommendations_financement_à_la_consommation_categorie,
    "Assurance": local_recommendations_assurance_categorie,
    "Retraite & Prévoyance": local_recommendations_retraite_et_prévoyance_categorie,
    "Épargne & Placement": local_recommendations_epargne_et_placement_categorie,
    "Packs bancaires": local_recommendations_packs_bancaires_categorie,
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
    "Comptes": expert_recommendations_comptes_categorie,
    "Cartes": expert_recommendations_cartes_categorie,
    "Financement immobilier": expert_recommendations_financement_immobilier_categorie,
    "Financement à la consommation": expert_recommendations_financement_à_la_consommation_categorie,
    "Assurance": expert_recommendations_assurance_categorie,
    "Retraite & Prévoyance": expert_recommendations_retraite_et_prévoyance_categorie,
    "Épargne & Placement": expert_recommendations_epargne_et_placement_categorie,
    "Packs bancaires": expert_recommendations_packs_bancaires_categorie,
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
    "Comptes": meta_recommendations_comptes_categorie,
    "Cartes": meta_recommendations_cartes_categorie,
    "Financement immobilier": meta_recommendations_financement_immobilier_categorie,
    "Financement à la consommation": meta_recommendations_financement_à_la_consommation_categorie,
    "Assurance": meta_recommendations_assurance_categorie,
    "Retraite & Prévoyance": meta_recommendations_retraite_et_prévoyance_categorie,
    "Épargne & Placement": meta_recommendations_epargne_et_placement_categorie,
    "Packs bancaires": meta_recommendations_packs_bancaires_categorie,
}

Compte_chèque_en_DH = (
    "Compte courant en dirhams marocains pour gérer les opérations quotidiennes."
)
Compte_chèque_en_devises = (
    "Compte courant en devises étrangères pour les opérations internationales."
)
Compte_sur_carnet = (
    "Compte épargne rémunéré avec carnet pour suivre les dépôts et retraits."
)
Compte_à_terme = "Compte bloqué sur une durée déterminée avec intérêt garanti."
Carte_basique = "Carte bancaire simple pour retrait et paiement au quotidien."
Carte_Visa = "Carte de paiement internationale pour achats et retraits."
Carte_Visa_Premium = "Carte offrant plus de services : assurances voyage, bonus points."
Carte_Visa_Elite = (
    "Carte haut de gamme avec services premium et programmes de fidélité."
)
Carte_Visa_Infinite = "Carte très haut de gamme avec services exclusifs."
Crédit_Immo_avec_garantie_hypothécaire = (
    "Prêt immobilier garanti par hypothèque sur le bien."
)
Crédit_Immo_avec_garantie_liquide = (
    "Prêt immobilier garanti par un dépôt de fonds liquide."
)
Crédit_Immo_avec_remboursement_in_fine = (
    "Prêt remboursé en une seule fois à échéance finale."
)
Crédit_Immo_subventionné = "Prêt bénéficiant de taux réduits par l’État ou organisme."
Crédit_à_la_consommation_non_affecté = "Prêt personnel sans justificatif d’utilisation."
Crédit_Auto = "Prêt dédié à l’achat de véhicule neuf ou d’occasion."
Découvert = "Facilite le paiement en cas de manque temporaire de liquidité."
Assurance_décès_invalidité_adossée_à_un_financement = (
    "Protection du prêt en cas de décès ou invalidité."
)
Assurance_décès_toutes_causes = "Protection financière en cas de décès."
Multirisques_bâtiment = "Assurance habitation couvrant incendie, dégâts, vol."
Maladie_complémentaire = (
    "Couverture santé complémentaire aux remboursements CNOPS/CNSS."
)
Retraite_complémentaire = "Plan épargne retraite pour compléter la pension publique."
Retraite_complémentaire_en_UC = (
    "Retraite complémentaire investie en unités de compte (fonds actions/obligations)."
)
Épargne_Éducation = "Plan d’épargne pour financer études des enfants."
Épargne_Logement = "Épargne destinée à l’achat immobilier futur."
OPCVM_monétaires = "Fonds investissant en liquidités et titres court terme."
OPCVM_obligataires = "Fonds investissant en obligations, faible risque."
OPCVM_diversifiés = "Fonds combinant actions et obligations pour diversification."
OPCVM_actions = "Fonds investissant majoritairement en actions, risque plus élevé."
Pack_bancaire_basique = (
    "Ensemble de services bancaires standard (compte courant, carte)."
)
Pack_bancaire_étoffé = "Pack complet incluant cartes premium, épargne et assurances."

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
    "Jan",
    "Fév",
    "Mar",
    "Avr",
    "Mai",
    "Jun",
    "Jul",
    "Aoû",
    "Sep",
    "Oct",
    "Nov",
    "Déc",
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
monthly_income = np.clip(monthly_income, 1, None)
monthly_expenses = np.clip(monthly_expenses, 1, None)

monthly_data = pd.DataFrame(
    {"Income": monthly_income, "Expenses": monthly_expenses}, index=months
)

local_recommendations_output_file = "Data/results/local_recommendations.json"
meta_recommendations_output_file = "Data/results/meta_recommendations.json"
expert_recommendations_output_file = "Data/results/expert_recommendations.json"

Advantages_Compte_chèque_en_DH = [
    "Gestion facile des paiements",
    "Virements et retraits",
    "Carte bancaire associée",
]
Advantages_Compte_chèque_en_devises = [
    "Facilite les transactions internationales",
    "Convertibilité rapide",
]
Advantages_Compte_sur_carnet = ["Rendement sur les dépôts", "Flexibilité de retrait"]
Advantages_Compte_à_terme = ["Taux d’intérêt supérieur au compte épargne", "Sécurité"]
Advantages_Carte_basique = ["Accessibilité", "Sécurité", "Paiements électroniques"]
Advantages_Carte_Visa = ["Acceptée partout", "Sécurité", "Possibilité de crédit"]
Advantages_Carte_Visa_Premium = [
    "Assurance voyages",
    "Services conciergerie",
    "Plafonds plus élevés",
]
Advantages_Carte_Visa_Elite = [
    "Accès lounges",
    "Assurances complètes",
    "Service prioritaire",
]
Advantages_Carte_Visa_Infinite = [
    "Concierge personnel",
    "Assurances premium",
    "Programmes luxe",
]
Advantages_Crédit_Immo_avec_garantie_hypothécaire = [
    "Taux généralement plus bas",
    "Sécurise le prêt pour la banque",
]
Advantages_Crédit_Immo_avec_garantie_liquide = [
    "Plus rapide à mettre en place",
    "taux compétitif",
]
Advantages_Crédit_Immo_avec_remboursement_in_fine = [
    "Permet de libérer trésorerie mensuelle",
    "Adapté investissement locatif",
]
Advantages_Crédit_Immo_subventionné = ["Taux avantageux", "Soutien public"]
Advantages_Crédit_à_la_consommation_non_affecté = [
    "Rapidité",
    "Flexibilité",
    "Aucune obligation de destination",
]
Advantages_Crédit_Auto = [
    "Taux compétitif",
    "Remboursement échelonné",
    "Assurance souvent incluse",
]
Advantages_Découvert = ["Flexibilité", "Immédiat", "Couvre dépenses urgentes"]
Advantages_Assurance_décès_invalidité_adossée_à_un_financement = [
    "Sécurité pour la famille et la banque"
]
Advantages_Assurance_décès_toutes_causes = ["Sécurité famille", "Couverture complète"]
Advantages_Multirisques_bâtiment = ["Couverture complète", "Tranquillité"]
Advantages_Maladie_complémentaire = [
    "Accès à plus de soins",
    "Remboursements supérieurs",
]
Advantages_Retraite_complémentaire = [
    "Prévoit revenus à la retraite",
    "Avantage fiscal",
]
Advantages_Retraite_complémentaire_en_UC = [
    "Rendement potentiel plus élevé",
    "Diversification",
]
Advantages_Épargne_Éducation = ["Avantages fiscaux", "Sécurité des fonds"]
Advantages_Épargne_Logement = ["Rendement garanti", "Prime de l’État possible"]
Advantages_OPCVM_monétaires = ["Sécurité", "Liquidité élevée", "Rendement stable"]
Advantages_OPCVM_obligataires = [
    "Rendement supérieur au compte épargne",
    "Diversification",
]
Advantages_OPCVM_diversifiés = ["Rendement potentiellement plus élevé", "Risque modéré"]
Advantages_OPCVM_actions = [
    "Potentiel de rendement élevé",
    "Diversification internationale",
]
Advantages_Pack_bancaire_basique = ["Économie sur frais combinés", "Simplicité"]
Advantages_Pack_bancaire_étoffé = [
    "Services complets",
    "Réductions sur produits associés",
]

Coût_estimatif_des_frais_Compte_chèque_en_DH = {
    "Frais d’ouverture": "0 DH",
    "Frais mensuels": "20 - 50 DH",
    "Frais virements/chéquiers": "selon usage",
}
Coût_estimatif_des_frais_Compte_chèque_en_devises = {
    "Frais ouverture": "0 DH",
    "Frais tenue de compte": "50 - 100 DH/mois",
}
Coût_estimatif_des_frais_Compte_sur_carnet = {
    "Frais ouverture": "0 DH",
    "Frais gestion": "0 - 10 DH/mois",
}
Coût_estimatif_des_frais_Compte_à_terme = {
    "Frais ouverture": "0 DH",
    "Pas de frais mensuels": None,
    "Pénalités en cas de retrait anticipé": None,
}
Coût_estimatif_des_frais_Carte_basique = {
    "Frais annuels": "100 - 200 DH",
    "Retrait": "3 - 5 DH/transaction",
}
Coût_estimatif_des_frais_Carte_Visa = {
    "Frais annuels": "200 - 400 DH",
    "Retrait": "5 - 10 DH/transaction",
}
Coût_estimatif_des_frais_Carte_Visa_Premium = {
    "Frais annuels": "600 - 1000 DH",
    "Retrait": "5 - 10 DH/transaction",
}
Coût_estimatif_des_frais_Carte_Visa_Elite = {
    "Frais annuels": "1200 - 2000 DH",
    "Retrait": "5 - 10 DH/transaction",
}
Coût_estimatif_des_frais_Carte_Visa_Infinite = {
    "Frais annuels": "3000 - 5000 DH",
    "Retrait": "5 - 10 DH/transaction",
}
Coût_estimatif_des_frais_Crédit_Immo_avec_garantie_hypothécaire = {
    "Frais dossier": "1%" + " - 2% montant",
    "Assurance": "0,2% - 0,5% /an",
    "Intérêts selon taux marché": None,
}
Coût_estimatif_des_frais_Crédit_Immo_avec_garantie_liquide = {
    "Frais dossier": "1%",
    "Assurance": "0,2% - 0,5% /an",
}
Coût_estimatif_des_frais_Crédit_Immo_avec_remboursement_in_fine = {
    "Frais dossier": "1%",
    "Intérêts sur durée": None,
    "Assurance selon banque": None,
}
Coût_estimatif_des_frais_Crédit_Immo_subventionné = {
    "Frais minimes": None,
    "Intérêts réduits": None,
}
Coût_estimatif_des_frais_Crédit_à_la_consommation_non_affecté = {
    "Frais dossier": "1%" + " - 2%",
    "Taux 8-12% annuel": None,
}
Coût_estimatif_des_frais_Crédit_Auto = {
    "Frais dossier": "1%" + " - 2%",
    "Taux": "7%" + " - 10% annuel",
}
Coût_estimatif_des_frais_Découvert = {
    "Intérêts": "12%" + " - 18%",
    "Commissions": "50 - 100 DH/mois",
}
Coût_estimatif_des_frais_Assurance_décès_invalidité_adossée_à_un_financement = {
    "Prime": "0,2% - 0,5% du capital par an"
}
Coût_estimatif_des_frais_Assurance_décès_toutes_causes = {
    "Prime": "0,3% - 0,6% du capital par an"
}
Coût_estimatif_des_frais_Multirisques_bâtiment = {
    "Prime": "0,1% - 0,5% valeur du bien/an"
}
Coût_estimatif_des_frais_Maladie_complémentaire = {
    "Prime": "500 - 5000 DH/an selon couverture"
}
Coût_estimatif_des_frais_Retraite_complémentaire = {
    "Cotisation": "5%" + " - 20% revenu annuel"
}
Coût_estimatif_des_frais_Retraite_complémentaire_en_UC = {
    "Cotisation": "5%" + " - 20% revenu",
    "Frais gestion": "0,5%" + " - 2%",
}
Coût_estimatif_des_frais_Épargne_Éducation = {
    "Versements flexibles": None,
    "Frais tenue compte 0-50 DH/mois": None,
}
Coût_estimatif_des_frais_Épargne_Logement = {
    "Frais minimes",
    "Intérêts selon taux marché",
}
Coût_estimatif_des_frais_OPCVM_monétaires = {
    "Frais gestion": "0,2%" + " - 1%",
    "Souscription minimale": "1000 DH",
}
Coût_estimatif_des_frais_OPCVM_obligataires = {
    "Frais gestion": "0,3%" + " - 1%",
    "Souscription minimale": "1000 DH",
}
Coût_estimatif_des_frais_OPCVM_diversifiés = {
    "Frais gestion": "0,5% - 1,5%",
    "Souscription minimale": "1000 DH",
}
Coût_estimatif_des_frais_OPCVM_actions = {
    "Frais gestion": "0,5%" + " - 2%",
    "Souscription minimale": "1000 DH",
}
Coût_estimatif_des_frais_Pack_bancaire_basique = {"Abonnement": "50 - 150 DH/mois"}
Coût_estimatif_des_frais_Pack_bancaire_étoffé = {"Abonnement": "150 - 400 DH/mois"}

Advantages = {
    "Produit - Compte chèque en DH": [
        "Gestion facile des paiements, virements et retraits; carte bancaire associée",
        Advantages_Compte_chèque_en_DH,
        Coût_estimatif_des_frais_Compte_chèque_en_DH,
    ],
    "Produit - Compte chèque en devises": [
        "Facilite les transactions internationales, convertibilité rapide",
        Advantages_Compte_chèque_en_devises,
        Coût_estimatif_des_frais_Compte_chèque_en_devises,
    ],
    "Produit - Compte sur carnet": [
        "Rendement sur les dépôts, flexibilité de retrait",
        Advantages_Compte_sur_carnet,
        Coût_estimatif_des_frais_Compte_sur_carnet,
    ],
    "Produit - Compte à terme": [
        "Taux d’intérêt supérieur au compte épargne, sécurité",
        Advantages_Compte_à_terme,
        Coût_estimatif_des_frais_Compte_à_terme,
    ],
    "Produit - Carte basique": [
        "Accessibilité, sécurité, paiements électroniques",
        Advantages_Carte_basique,
        Coût_estimatif_des_frais_Carte_basique,
    ],
    "Produit - Carte Visa": [
        "Acceptée partout, sécurité, possibilité de crédit",
        Advantages_Carte_Visa,
        Coût_estimatif_des_frais_Carte_Visa,
    ],
    "Produit - Carte Visa Premium": [
        "Assurance voyages, services de conciergerie, plafonds plus élevés",
        Advantages_Carte_Visa_Premium,
        Coût_estimatif_des_frais_Carte_Visa_Premium,
    ],
    "Produit - Carte Visa Elite": [
        "Accès aux lounges, assurances complètes, service prioritaire",
        Advantages_Carte_Visa_Elite,
        Coût_estimatif_des_frais_Carte_Visa_Elite,
    ],
    "Produit - Carte Visa Infinite": [
        "Concierge personnel, assurances premium, programmes luxe",
        Advantages_Carte_Visa_Infinite,
        Coût_estimatif_des_frais_Carte_Visa_Infinite,
    ],
    "Produit - Crédit Immo avec garantie hypothécaire": [
        "Taux généralement plus bas, sécurise le prêt pour la banque",
        Advantages_Crédit_Immo_avec_garantie_hypothécaire,
        Coût_estimatif_des_frais_Crédit_Immo_avec_garantie_hypothécaire,
    ],
    "Produit - Crédit Immo avec garantie liquide": [
        "Plus rapide à mettre en place, taux compétitif",
        Advantages_Crédit_Immo_avec_garantie_liquide,
        Coût_estimatif_des_frais_Crédit_Immo_avec_garantie_liquide,
    ],
    "Produit - Crédit Immo avec remboursement in fine": [
        "Permet de libérer la trésorerie mensuelle, adapté à l’investissement locatif",
        Advantages_Crédit_Immo_avec_remboursement_in_fine,
        Coût_estimatif_des_frais_Crédit_Immo_avec_remboursement_in_fine,
    ],
    "Produit - Crédit Immo subventionné": [
        "Taux avantageux, soutien public",
        Advantages_Crédit_Immo_subventionné,
        Coût_estimatif_des_frais_Crédit_Immo_subventionné,
    ],
    "Produit - Crédit à la consommation non affecté": [
        "Rapidité, flexibilité, aucune obligation de destination",
        Advantages_Crédit_à_la_consommation_non_affecté,
        Coût_estimatif_des_frais_Crédit_à_la_consommation_non_affecté,
    ],
    "Produit - Crédit Auto": [
        "Taux compétitif, remboursement échelonné, assurance souvent incluse",
        Advantages_Crédit_Auto,
        Coût_estimatif_des_frais_Crédit_Auto,
    ],
    "Produit - Découvert": [
        "Flexibilité, immédiat, couvre les dépenses urgentes",
        Advantages_Découvert,
        Coût_estimatif_des_frais_Découvert,
    ],
    "Produit - Assurance décès invalidité adossée à un financement": [
        "Sécurité pour la famille et la banque",
        Advantages_Assurance_décès_invalidité_adossée_à_un_financement,
        Coût_estimatif_des_frais_Assurance_décès_invalidité_adossée_à_un_financement,
    ],
    "Produit - Assurance décès toutes causes": [
        "Sécurité pour la famille, couverture complète",
        Advantages_Assurance_décès_toutes_causes,
        Coût_estimatif_des_frais_Assurance_décès_toutes_causes,
    ],
    "Produit - Multirisques bâtiment": [
        "Couverture complète, tranquillité",
        Advantages_Multirisques_bâtiment,
        Coût_estimatif_des_frais_Multirisques_bâtiment,
    ],
    "Produit - Maladie complémentaire": [
        "Accès à plus de soins, remboursements supérieurs",
        Advantages_Maladie_complémentaire,
        Coût_estimatif_des_frais_Maladie_complémentaire,
    ],
    "Produit - Retraite complémentaire": [
        "Prévoit des revenus à la retraite, avantage fiscal",
        Advantages_Retraite_complémentaire,
        Coût_estimatif_des_frais_Retraite_complémentaire,
    ],
    "Produit - Retraite complémentaire en UC": [
        "Rendement potentiel plus élevé, diversification",
        Advantages_Retraite_complémentaire_en_UC,
        Coût_estimatif_des_frais_Retraite_complémentaire_en_UC,
    ],
    "Produit - Épargne Éducation": [
        "Avantages fiscaux, sécurité des fonds",
        Advantages_Épargne_Éducation,
        Coût_estimatif_des_frais_Épargne_Éducation,
    ],
    "Produit - Épargne Logement": [
        "Rendement garanti, prime de l’État possible",
        Advantages_Épargne_Logement,
        Coût_estimatif_des_frais_Épargne_Logement,
    ],
    "Produit - OPCVM monétaires": [
        "Sécurité, liquidité élevée, rendement stable",
        Advantages_OPCVM_monétaires,
        Coût_estimatif_des_frais_OPCVM_monétaires,
    ],
    "Produit - OPCVM obligataires": [
        "Rendement supérieur au compte épargne, diversification",
        Advantages_OPCVM_obligataires,
        Coût_estimatif_des_frais_OPCVM_obligataires,
    ],
    "Produit - OPCVM diversifiés": [
        "Rendement potentiellement plus élevé, risque modéré",
        Advantages_OPCVM_diversifiés,
        Coût_estimatif_des_frais_OPCVM_diversifiés,
    ],
    "Produit - OPCVM actions": [
        "Potentiel de rendement élevé, diversification internationale",
        Advantages_OPCVM_actions,
        Coût_estimatif_des_frais_OPCVM_actions,
    ],
    "Produit - Pack bancaire basique": [
        "Économie sur les frais combinés, simplicité",
        Advantages_Pack_bancaire_basique,
        Coût_estimatif_des_frais_Pack_bancaire_basique,
    ],
    "Produit - Pack bancaire étoffé": [
        "Services complets, réductions sur produits associés",
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
        st.warning(f"⚠️ Fichier CSS non trouvé : {file_path}")


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
            )


# --- INITIALISATION DES VARIABLES DE SESSION ---
st.session_state.switch_page_client = False
st.session_state.setdefault("produit_page", None)
st.session_state.setdefault("aff_content", False)
st.session_state.setdefault("process_done", False)
st.session_state.m_messages = []


# --- NAVIGATION AUTOMATIQUE SI DÉCLENCHÉE ---
if st.session_state["produit_page"] == True:
    st.switch_page("pages/produit.py")

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
        "Tableau de bord",
        width="stretch",
        icon=":material/dashboard:",
        type="tertiary",
        key="btn1",
    )
    st.button(
        "Clients",
        width="stretch",
        icon=":material/patient_list:",
        type="tertiary",
        key="btn2",
    )
    st.button(
        "Comptes",
        width="stretch",
        icon=":material/account_balance:",
        type="tertiary",
        key="btn3",
    )
    st.button(
        "Prêts",
        width="stretch",
        icon=":material/money_bag:",
        type="tertiary",
        key="btn4",
    )
    st.button(
        "Cartes",
        width="stretch",
        icon=":material/playing_cards:",
        type="tertiary",
        key="btn5",
    )
    st.button(
        "Investissements",
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
    st.title("Fiche détaillée du Client" + " " + str(client_index))
with col_input:
    user_input = st.text_input(
        "test",
        placeholder="Saisissez un autre numéro de client.",
        label_visibility="hidden",
        on_change=change_client,
        key="user_input",
    )

col11, col22 = st.columns([1.6, 3])
with col11:
    with st.container(border=True):
        nom = "Client" + " " + str(client_index)
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
        st.write("Âge :" + " " + str(df["Âge"].iat[client_index]))
        st.write("Statut marital :" + " " + str(df["Statut marital"].iat[client_index]))
        st.write("Situation :" + " " + str(df["Situation"].iat[client_index]))
        st.write(
            "Nombre d’enfants :" + " " + str(df["Nombre d’enfants"].iat[client_index])
        )
        col_Propriétaire, col_reponse_oui, col_reponse_non = st.columns([2.2, 1, 1])
        with col_Propriétaire:
            st.write("Propriétaire :")
        with col_reponse_oui:
            st.checkbox("oui", value=value_15, disabled=True, key="29")
        with col_reponse_non:
            st.checkbox("non", value=not value_15, disabled=True, key="30")
        st.write("Revenu annuel :" + " " + str(df["Revenu annuel"].iat[client_index]))
    with st.container(border=True):
        col_action, col_action_icon = st.columns([4.5, 1])
        with col_action:
            st.markdown(
                f"""
                <p style='font-family:Arial; font-size:24px; font-weight:bold;'>
                    {"Actions rapides"}
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
        div[class*="st-key-btn_money"] .stButton button {
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
            "Ouvrir un nouveau compte ",
            icon=":material/home:",
            width="stretch",
            key="btn_home",
        )
        st.button(
            "Demander un prêt",
            icon=":material/attach_money:",
            width="stretch",
            key="btn_money",
        )
        st.button(
            " Mise à jour du contact",
            icon=":material/update:",
            width="stretch",
            key="btn_update",
        )
        st.button(
            "Consulter les relevés",
            icon=":material/frame_inspect:",
            width="stretch",
            key="btn_inspect",
        )
        st.button(
            "Effectuer un virement",
            icon=":material/send_money:",
            width="stretch",
            key="btn_send",
        )
with col22:
    with st.container(border=True):
        col_produit, col_produit_icon = st.columns([6.5, 1])
        with col_produit:
            st.markdown(
                f"""
                <p style='font-family:Arial; font-size:24px; font-weight:bold;'>
                    {"Aperçu des produits"}
                </p>
                """,
                unsafe_allow_html=True,
            )
        with col_produit_icon:
            st.image("images/produit.png", width="stretch")
        st.markdown(
            f"""
                    <p style='font-family:Arial; font-size:15px; font-weight:bold; font-style:italic; color:blue;'>
                        Client {client_index} possède :
                    </p>
                    """,
            unsafe_allow_html=True,
        )
        col112, col122, col133 = st.columns([6.5, 1, 1])
        with col112:
            st.write(" Produit - Compte chèque en DH")
            st.write(" Produit - Compte chèque en devises")
            st.write(" Produit - Compte sur carnet")
            st.write(" Produit - Compte à terme")

            st.write(" Produit - Carte basique")
            st.write(" Produit - Carte visa")
            st.write(" Produit - Carte visa premium")
            st.write(" Produit - Carte visa elite")
            st.write(" Produit - Carte visa infinite")

            st.write(" Produit - Crédit Immo avec garantie hypothécaire")
            st.write(" Produit - Crédit Immo avec garantie liquide")
            st.write(" Produit - Crédit immo avec remboursement in fine")

            st.write(" Produit - Crédit à la consommation non affecté")
            st.write(" Produit - Crédit Auto")
        with col122:
            st.checkbox(
                "oui",
                value=value_1,
                disabled=True,
                key="1",
            )
            st.checkbox("oui", value=value_2, disabled=True, key="2")
            st.checkbox("oui", value=value_3, disabled=True, key="3")
            st.checkbox("oui", value=value_4, disabled=True, key="4")
            st.checkbox("oui", value=value_5, disabled=True, key="5")
            st.checkbox("oui", value=value_6, disabled=True, key="6")
            st.checkbox("oui", value=value_7, disabled=True, key="7")
            st.checkbox("oui", value=value_8, disabled=True, key="8")
            st.checkbox("oui", value=value_9, disabled=True, key="9")
            st.checkbox("oui", value=value_10, disabled=True, key="10")
            st.checkbox("oui", value=value_11, disabled=True, key="11")
            st.checkbox("oui", value=value_12, disabled=True, key="12")
            st.checkbox("oui", value=value_13, disabled=True, key="13")
            st.checkbox("oui", value=value_14, disabled=True, key="14")

        with col133:
            st.checkbox("non", disabled=True, value=not value_1, key="15")
            st.checkbox("non", disabled=True, value=not value_2, key="16")
            st.checkbox("non", disabled=True, value=not value_3, key="17")
            st.checkbox("non", disabled=True, value=not value_4, key="18")
            st.checkbox("non", disabled=True, value=not value_5, key="19")
            st.checkbox("non", disabled=True, value=not value_6, key="20")
            st.checkbox("non", disabled=True, value=not value_7, key="21")
            st.checkbox("non", disabled=True, value=not value_8, key="22")
            st.checkbox("non", disabled=True, value=not value_9, key="23")
            st.checkbox("non", disabled=True, value=not value_10, key="24")
            st.checkbox("non", disabled=True, value=not value_11, key="25")
            st.checkbox("non", disabled=True, value=not value_12, key="26")
            st.checkbox("non", disabled=True, value=not value_13, key="27")
            st.checkbox("non", disabled=True, value=not value_14, key="28")

    col1, col2, col3 = st.columns([1.6, 2, 1])
    with col1:
        col12, col21, col13 = st.columns([5, 1, 2])
        with col13:
            st.image("images/NEURONAIZE-ICONE-NOIR.png", width=40)
    with col2:
        analyser_btn = st.button("Analysez avec NeuronAize ", width=210, key="analyser")
if analyser_btn:
    st.session_state["aff_content"] = True
if st.session_state.aff_content == True:
    with st.container(border=True):
        st.markdown(
            f"""
                <p style='font-family:Arial; font-size:24px; font-weight:bold;'>
                    {"Synthèse financière"}
                </p>
                """,
            unsafe_allow_html=True,
        )
        col1111, col2222, col3333 = st.columns([1, 1, 1])
        with col1111:
            with st.container(border=True):
                st.write("Revenus totaux (cumul annuel)")
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
                    st.write("DH")
        with col2222:
            with st.container(border=True):
                st.write("Dépenses totales (cumul annuel)")
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
                    st.write("DH")
        with col3333:
            with st.container(border=True):
                st.write("Patrimoine net actuel")
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
                    st.write("DH")
        with st.container(border=True):
            st.markdown(
                f"""
                    <p style='font-family:Arial; font-size:24px; font-weight:bold;'>
                        {"Revenus vs Dépenses mensuels"}
                    </p>
                    """,
                unsafe_allow_html=True,
            )
            # --- DESIGN PERSONNALISÉ ---
            plt.style.use("seaborn-v0_8-whitegrid")  # joli fond clair moderne

            bar_width = 0.35
            r1 = np.arange(len(months))
            r2 = r1 + bar_width

            fig, ax = plt.subplots(figsize=(10, 6))

            # Couleurs harmonieuses
            income_color = "#4CAF50"  # vert doux
            expense_color = "#FFB74D"  # orange clair

            # Barres arrondies
            ax.bar(
                r1,
                monthly_data["Income"],
                width=bar_width,
                color=income_color,
                label="Revenus",
                edgecolor="white",
                linewidth=1,
            )
            ax.bar(
                r2,
                monthly_data["Expenses"],
                width=bar_width,
                color=expense_color,
                label="Dépenses",
                edgecolor="white",
                linewidth=1,
            )

            # Étiquettes et légendes
            ax.set_xticks(r1 + bar_width / 2)
            ax.set_xticklabels(months, fontsize=11, fontweight="bold")
            ax.set_xlabel("Mois", fontsize=12, labelpad=10)
            ax.set_ylabel("Montant (DH)", fontsize=12, labelpad=10)
            # 🔽 Légende en bas
            ax.legend(
                loc="upper center",  # position horizontale au centre
                bbox_to_anchor=(
                    0.5,
                    -0.15,
                ),  # décale vers le bas (valeur négative = sous le graphe)
                ncol=2,  # affiche la légende sur deux colonnes
                frameon=False,  # pas de cadre autour
                fontsize=10,
            )

            # Supprimer les bordures inutiles
            for spine in ["top", "right"]:
                ax.spines[spine].set_visible(False)

            # Espacement et affichage
            plt.tight_layout()
            st.pyplot(fig)
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
            with st.spinner("Patientez svp..."):
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
        st.markdown(
            f"""
                    <p style='font-family:Arial; font-size:24px; font-weight:bold;'>
                        {"Recommandations basées sur les clients similaires"}
                    </p>
                    """,
            unsafe_allow_html=True,
        )
        if os.path.exists(local_recommendations_output_file):
            with open(local_recommendations_output_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            for item in data:
                if item["product"] in categories["Comptes"]:
                    local_recommendations_comptes_categorie[item["product"]] = item[
                        "percentage"
                    ]

                if item["product"] in categories["Cartes"]:
                    local_recommendations_cartes_categorie[item["product"]] = item[
                        "percentage"
                    ]

                if item["product"] in categories["Financement immobilier"]:
                    local_recommendations_financement_immobilier_categorie[
                        item["product"]
                    ] = item["percentage"]

                if item["product"] in categories["Financement à la consommation"]:
                    local_recommendations_financement_à_la_consommation_categorie[
                        item["product"]
                    ] = item["percentage"]

                if item["product"] in categories["Assurance"]:
                    local_recommendations_assurance_categorie[item["product"]] = item[
                        "percentage"
                    ]

                if item["product"] in categories["Retraite & Prévoyance"]:
                    local_recommendations_retraite_et_prévoyance_categorie[
                        item["product"]
                    ] = item["percentage"]

                if item["product"] in categories["Épargne & Placement"]:
                    local_recommendations_epargne_et_placement_categorie[
                        item["product"]
                    ] = item["percentage"]

                if item["product"] in categories["Packs bancaires"]:
                    local_recommendations_packs_bancaires_categorie[item["product"]] = (
                        item["percentage"]
                    )

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
                                    if cat[i] == "Comptes":
                                        img = "images/comptes"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == "Cartes":
                                        img = "images/cartes"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == "Financement immobilier":
                                        img = "images/Financement immobilier"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == "Financement à la consommation":
                                        img = "images/financement à la consommation"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == "Assurance":
                                        img = "images/assurance"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == "Retraite & Prévoyance":
                                        img = "images/retraite & Prévoyance"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == "Épargne & Placement":
                                        img = "images/Épargne et Placement"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == "Packs bancaires":
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
                                    if reco == "Produit - Compte chèque en DH":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Compte_chèque_en_DH}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Compte chèque en devises":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Compte_chèque_en_devises}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Compte sur carnet":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Compte_sur_carnet}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Carte basique":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Carte_basique}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Carte Visa":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Carte_Visa}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Carte Visa Premium":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Carte_Visa_Premium}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Carte Visa Elite":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Carte_Visa_Elite}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Carte Visa Infinite":
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
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Crédit_Immo_avec_remboursement_in_fine}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Crédit Immo subventionné":
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
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Crédit_à_la_consommation_non_affecté}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Crédit Auto":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Crédit_Auto}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Découvert":
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
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Assurance_décès_toutes_causes}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Multirisques bâtiment":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Multirisques_bâtiment}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Maladie complémentaire":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Maladie_complémentaire}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Retraite complémentaire":
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
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Retraite_complémentaire_en_UC}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Épargne Éducation":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Épargne_Éducation}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Épargne Logement":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Épargne_Logement}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - OPCVM monétaires":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {OPCVM_monétaires}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - OPCVM obligataires":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {OPCVM_obligataires}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - OPCVM diversifiés":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {OPCVM_diversifiés}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - OPCVM actions":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {OPCVM_actions}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Pack bancaire basique":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Pack_bancaire_basique}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Pack bancaire étoffé":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Pack_bancaire_étoffé}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Compte à terme":
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
                                                    Adéquation en % :
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
                                            "En savoir plus / Souscrire",
                                            type="tertiary",
                                            width="stretch",
                                            key=f"btn_a_{j}",
                                            on_click=switch_page_produit,
                                            args=(reco,),
                                        )
                                    with col3b:
                                        st.button(
                                            "Estimer le coût / Obtenir un devis",
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
                                    if cat[i] == "Comptes":
                                        img = "images/comptes"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == "Cartes":
                                        img = "images/cartes"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == "Financement immobilier":
                                        img = "images/Financement immobilier"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == "Financement à la consommation":
                                        img = "images/financement à la consommation"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == "Assurance":
                                        img = "images/assurance"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == "Retraite & Prévoyance":
                                        img = "images/retraite & Prévoyance"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == "Épargne & Placement":
                                        img = "images/Épargne et Placement"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == "Packs bancaires":
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
                                    if reco == "Produit - Compte chèque en DH":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Compte_chèque_en_DH}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Compte chèque en devises":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Compte_chèque_en_devises}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Compte sur carnet":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Compte_sur_carnet}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Carte basique":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Carte_basique}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Carte Visa":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Carte_Visa}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Carte Visa Premium":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Carte_Visa_Premium}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Carte Visa Elite":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Carte_Visa_Elite}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Carte Visa Infinite":
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
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Crédit_Immo_avec_remboursement_in_fine}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Crédit Immo subventionné":
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
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Crédit_à_la_consommation_non_affecté}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Crédit Auto":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Crédit_Auto}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Découvert":
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
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Assurance_décès_toutes_causes}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Multirisques bâtiment":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Multirisques_bâtiment}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Maladie complémentaire":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Maladie_complémentaire}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Retraite complémentaire":
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
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Retraite_complémentaire_en_UC}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Épargne Éducation":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Épargne_Éducation}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Épargne Logement":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Épargne_Logement}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - OPCVM monétaires":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {OPCVM_monétaires}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - OPCVM obligataires":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {OPCVM_obligataires}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - OPCVM diversifiés":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {OPCVM_diversifiés}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - OPCVM actions":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {OPCVM_actions}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Pack bancaire basique":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Pack_bancaire_basique}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Pack bancaire étoffé":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Pack_bancaire_étoffé}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Compte à terme":
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
                                                    Adéquation en % :
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
                                            "En savoir plus / Souscrire",
                                            type="tertiary",
                                            width="stretch",
                                            key=f"btn_c_{j}",
                                            on_click=switch_page_produit,
                                            args=(reco,),
                                        )
                                    with col3b:
                                        st.button(
                                            "Estimer le coût / Obtenir un devis",
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
        st.markdown(
            f"""
        <p style='font-family:Arial; font-size:24px; font-weight:bold;'>
        {"Recommandations basées sur les experts"}
        </p>
        """,
            unsafe_allow_html=True,
        )
        if os.path.exists(expert_recommendations_output_file):
            with open(expert_recommendations_output_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            for item in data:
                if item["product"] in categories["Comptes"]:
                    expert_recommendations_comptes_categorie.append(item["product"])

                if item["product"] in categories["Cartes"]:
                    expert_recommendations_cartes_categorie.append(item["product"])

                if item["product"] in categories["Financement immobilier"]:
                    expert_recommendations_financement_immobilier_categorie.append(
                        item["product"]
                    )

                if item["product"] in categories["Financement à la consommation"]:
                    expert_recommendations_financement_à_la_consommation_categorie.append(
                        item["product"]
                    )

                if item["product"] in categories["Assurance"]:
                    expert_recommendations_assurance_categorie.append(item["product"])

                if item["product"] in categories["Retraite & Prévoyance"]:
                    expert_recommendations_retraite_et_prévoyance_categorie.append(
                        item["product"]
                    )

                if item["product"] in categories["Épargne & Placement"]:
                    expert_recommendations_epargne_et_placement_categorie.append(
                        item["product"]
                    )

                if item["product"] in categories["Packs bancaires"]:
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
                                    if cat[i] == "Comptes":
                                        img = "images/comptes"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == "Cartes":
                                        img = "images/cartes"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == "Financement immobilier":
                                        img = "images/Financement immobilier"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == "Financement à la consommation":
                                        img = "images/financement à la consommation"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == "Assurance":
                                        img = "images/assurance"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == "Retraite & Prévoyance":
                                        img = "images/retraite & Prévoyance"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == "Épargne & Placement":
                                        img = "images/Épargne et Placement"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == "Packs bancaires":
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
                                    if reco == "Produit - Compte chèque en DH":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Compte_chèque_en_DH}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Compte chèque en devises":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Compte_chèque_en_devises}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Compte sur carnet":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Compte_sur_carnet}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Carte basique":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Carte_basique}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Carte Visa":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Carte_Visa}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Carte Visa Premium":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Carte_Visa_Premium}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Carte Visa Elite":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Carte_Visa_Elite}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Carte Visa Infinite":
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
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Crédit_Immo_avec_remboursement_in_fine}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Crédit Immo subventionné":
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
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Crédit_à_la_consommation_non_affecté}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Crédit Auto":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Crédit_Auto}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Découvert":
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
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Assurance_décès_toutes_causes}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Multirisques bâtiment":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Multirisques_bâtiment}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Maladie complémentaire":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Maladie_complémentaire}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Retraite complémentaire":
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
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Retraite_complémentaire_en_UC}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Épargne Éducation":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Épargne_Éducation}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Épargne Logement":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Épargne_Logement}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - OPCVM monétaires":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {OPCVM_monétaires}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - OPCVM obligataires":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {OPCVM_obligataires}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - OPCVM diversifiés":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {OPCVM_diversifiés}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - OPCVM actions":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {OPCVM_actions}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Pack bancaire basique":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Pack_bancaire_basique}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Pack bancaire étoffé":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Pack_bancaire_étoffé}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Compte à terme":
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
                                            "En savoir plus / Souscrire",
                                            type="tertiary",
                                            width="stretch",
                                            key=f"btn_e_{j}",
                                            on_click=switch_page_produit,
                                            args=(reco,),
                                        )
                                    with col3b:
                                        st.button(
                                            "Estimer le coût / Obtenir un devis",
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
                                    if cat[i] == "Comptes":
                                        img = "images/comptes"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == "Cartes":
                                        img = "images/cartes"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == "Financement immobilier":
                                        img = "images/Financement immobilier"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == "Financement à la consommation":
                                        img = "images/financement à la consommation"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == "Assurance":
                                        img = "images/assurance"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == "Retraite & Prévoyance":
                                        img = "images/retraite & Prévoyance"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == "Épargne & Placement":
                                        img = "images/Épargne et Placement"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == "Packs bancaires":
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
                                    if reco == "Produit - Compte chèque en DH":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Compte_chèque_en_DH}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Compte chèque en devises":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Compte_chèque_en_devises}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Compte sur carnet":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Compte_sur_carnet}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Carte basique":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Carte_basique}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Carte Visa":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Carte_Visa}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Carte Visa Premium":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Carte_Visa_Premium}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Carte Visa Elite":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Carte_Visa_Elite}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Carte Visa Infinite":
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
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Crédit_Immo_avec_remboursement_in_fine}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Crédit Immo subventionné":
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
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Crédit_à_la_consommation_non_affecté}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Crédit Auto":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Crédit_Auto}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Découvert":
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
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Assurance_décès_toutes_causes}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Multirisques bâtiment":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Multirisques_bâtiment}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Maladie complémentaire":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Maladie_complémentaire}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Retraite complémentaire":
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
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Retraite_complémentaire_en_UC}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Épargne Éducation":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Épargne_Éducation}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Épargne Logement":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Épargne_Logement}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - OPCVM monétaires":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {OPCVM_monétaires}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - OPCVM obligataires":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {OPCVM_obligataires}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - OPCVM diversifiés":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {OPCVM_diversifiés}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - OPCVM actions":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {OPCVM_actions}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Pack bancaire basique":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Pack_bancaire_basique}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Pack bancaire étoffé":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Pack_bancaire_étoffé}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Compte à terme":
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
                                            "En savoir plus / Souscrire",
                                            type="tertiary",
                                            width="stretch",
                                            key=f"btn_f_{j}",
                                            on_click=switch_page_produit,
                                            args=(reco,),
                                        )
                                    with col3b:
                                        st.button(
                                            "Estimer le coût / Obtenir un devis",
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
        st.markdown(
            f"""
                    <p style='font-family:Arial; font-size:24px; font-weight:bold;'>
                        {"Recommandations basées sur le marché bancaire"}
                    </p>
                    """,
            unsafe_allow_html=True,
        )
        if os.path.exists(meta_recommendations_output_file):
            with open(meta_recommendations_output_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            for item in data:
                if item["product"] in categories["Comptes"]:
                    meta_recommendations_comptes_categorie[item["product"]] = item[
                        "percentage"
                    ]

                if item["product"] in categories["Cartes"]:
                    meta_recommendations_cartes_categorie[item["product"]] = item[
                        "percentage"
                    ]

                if item["product"] in categories["Financement immobilier"]:
                    meta_recommendations_financement_immobilier_categorie[
                        item["product"]
                    ] = item["percentage"]

                if item["product"] in categories["Financement à la consommation"]:
                    meta_recommendations_financement_à_la_consommation_categorie[
                        item["product"]
                    ] = item["percentage"]

                if item["product"] in categories["Assurance"]:
                    meta_recommendations_assurance_categorie[item["product"]] = item[
                        "percentage"
                    ]

                if item["product"] in categories["Retraite & Prévoyance"]:
                    meta_recommendations_retraite_et_prévoyance_categorie[
                        item["product"]
                    ] = item["percentage"]

                if item["product"] in categories["Épargne & Placement"]:
                    meta_recommendations_epargne_et_placement_categorie[
                        item["product"]
                    ] = item["percentage"]

                if item["product"] in categories["Packs bancaires"]:
                    meta_recommendations_packs_bancaires_categorie[item["product"]] = (
                        item["percentage"]
                    )

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
                                    if cat[i] == "Comptes":
                                        img = "images/comptes"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == "Cartes":
                                        img = "images/cartes"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == "Financement immobilier":
                                        img = "images/Financement immobilier"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == "Financement à la consommation":
                                        img = "images/financement à la consommation"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == "Assurance":
                                        img = "images/assurance"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == "Retraite & Prévoyance":
                                        img = "images/retraite & Prévoyance"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == "Épargne & Placement":
                                        img = "images/Épargne et Placement"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == "Packs bancaires":
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
                                    if reco == "Produit - Compte chèque en DH":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Compte_chèque_en_DH}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Compte chèque en devises":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Compte_chèque_en_devises}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Compte sur carnet":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Compte_sur_carnet}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Carte basique":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Carte_basique}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Carte Visa":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Carte_Visa}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Carte Visa Premium":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Carte_Visa_Premium}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Carte Visa Elite":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Carte_Visa_Elite}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Carte Visa Infinite":
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
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Crédit_Immo_avec_remboursement_in_fine}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Crédit Immo subventionné":
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
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Crédit_à_la_consommation_non_affecté}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Crédit Auto":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Crédit_Auto}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Découvert":
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
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Assurance_décès_toutes_causes}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Multirisques bâtiment":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Multirisques_bâtiment}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Maladie complémentaire":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Maladie_complémentaire}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Retraite complémentaire":
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
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Retraite_complémentaire_en_UC}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Épargne Éducation":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Épargne_Éducation}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Épargne Logement":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Épargne_Logement}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - OPCVM monétaires":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {OPCVM_monétaires}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - OPCVM obligataires":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {OPCVM_obligataires}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - OPCVM diversifiés":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {OPCVM_diversifiés}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - OPCVM actions":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {OPCVM_actions}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Pack bancaire basique":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Pack_bancaire_basique}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Pack bancaire étoffé":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Pack_bancaire_étoffé}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Compte à terme":
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
                                                    Adéquation en % :
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
                                            "En savoir plus / Souscrire",
                                            type="tertiary",
                                            width="stretch",
                                            key=f"btn_m_{j}",
                                            on_click=switch_page_produit,
                                            args=(reco,),
                                        )
                                    with col3b:
                                        st.button(
                                            "Estimer le coût / Obtenir un devis",
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
                                    if cat[i] == "Comptes":
                                        img = "images/comptes"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == "Cartes":
                                        img = "images/cartes"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == "Financement immobilier":
                                        img = "images/Financement immobilier"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == "Financement à la consommation":
                                        img = "images/financement à la consommation"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == "Assurance":
                                        img = "images/assurance"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == "Retraite & Prévoyance":
                                        img = "images/retraite & Prévoyance"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == "Épargne & Placement":
                                        img = "images/Épargne et Placement"
                                        st.image(
                                            f"{img}.png",
                                            width="stretch",
                                        )
                                    if cat[i] == "Packs bancaires":
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
                                    if reco == "Produit - Compte chèque en DH":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Compte_chèque_en_DH}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Compte chèque en devises":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Compte_chèque_en_devises}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Compte sur carnet":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Compte_sur_carnet}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Carte basique":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Carte_basique}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Carte Visa":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Carte_Visa}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Carte Visa Premium":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Carte_Visa_Premium}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Carte Visa Elite":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Carte_Visa_Elite}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Carte Visa Infinite":
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
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Crédit_Immo_avec_remboursement_in_fine}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Crédit Immo subventionné":
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
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Crédit_à_la_consommation_non_affecté}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Crédit Auto":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Crédit_Auto}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Découvert":
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
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Assurance_décès_toutes_causes}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Multirisques bâtiment":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Multirisques_bâtiment}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Maladie complémentaire":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Maladie_complémentaire}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Retraite complémentaire":
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
                                    ):
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Retraite_complémentaire_en_UC}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Épargne Éducation":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Épargne_Éducation}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Épargne Logement":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Épargne_Logement}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - OPCVM monétaires":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {OPCVM_monétaires}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - OPCVM obligataires":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {OPCVM_obligataires}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - OPCVM diversifiés":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {OPCVM_diversifiés}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - OPCVM actions":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {OPCVM_actions}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Pack bancaire basique":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Pack_bancaire_basique}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Pack bancaire étoffé":
                                        st.markdown(
                                            f"""
                                                <p style='font-family:Arial; font-size:12px;'>
                                                    {Pack_bancaire_étoffé}
                                                </p>
                                                """,
                                            unsafe_allow_html=True,
                                        )
                                    if reco == "Produit - Compte à terme":
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
                                                    Adéquation en % :
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
                                            "En savoir plus / Souscrire",
                                            type="tertiary",
                                            width="stretch",
                                            key=f"btn_x_{j}",
                                            on_click=switch_page_produit,
                                            args=(reco,),
                                        )
                                    with col3b:
                                        st.button(
                                            "Estimer le coût / Obtenir un devis",
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
