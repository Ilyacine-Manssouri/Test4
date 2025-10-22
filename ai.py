import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn_extra.cluster import KMedoids
import joblib
from scipy.spatial.distance import cityblock
import os
from collections import Counter
import json

# 1. Charger les données
fichier_excel = "Data/Data_base/bddf2.xlsx"
data = pd.read_excel(fichier_excel)

# 2. Identifier les colonnes "Produit" et caractéristiques
columns_produits = [col for col in data.columns if "Produit" in col]
columns_features = [col for col in data.columns if col not in columns_produits]

# 3. Standardiser les caractéristiques
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data[columns_features])

# 4. Chercher le bon nombre de clusters (KMedoids avec manhattan)
inertias = []
K_range = range(1, 20)

for k in K_range:
    model = KMedoids(
        n_clusters=k, init="k-medoids++", metric="manhattan", random_state=42
    )
    model.fit(data_scaled)
    inertias.append(model.inertia_)

# Calcul de la courbure
diff1 = np.diff(inertias)
diff2 = np.diff(diff1)
threshold = np.percentile(diff2, 80)
candidate_elbows = np.argwhere(diff2 > threshold).flatten() + 2
k_max = 20
elbows_filtered = [k for k in candidate_elbows if k <= k_max]
selected_k = max(elbows_filtered) if elbows_filtered else 4

print(f"Clusters proposés : {elbows_filtered}")
print(f"Cluster sélectionné : {selected_k}")

# 📊 Visualisation
# plt.figure(figsize=(8, 5))
# plt.plot(K_range, inertias, marker="o", label="Inertie")
# for k in elbows_filtered:
#    plt.axvline(x=k, color="green", linestyle="--", alpha=0.5)
# plt.axvline(
#    x=selected_k, color="red", linestyle="--", label=f"Selected k = {selected_k}"
# )
# plt.title("Détection de plusieurs coudes (KMedoids)")
# plt.xlabel("k")
# plt.ylabel("Inertie")
# plt.legend()
# plt.grid(True)
# plt.show()

# 5. Clustering final avec le bon k
kmedoids_final = KMedoids(n_clusters=selected_k, random_state=42, metric="manhattan")
labels = kmedoids_final.fit_predict(data_scaled)
data["Cluster"] = labels


# 6. Attribution d’un libellé automatique au cluster
def nommer_cluster(row):
    age = row["Âge"]
    revenu = row["Revenu annuel"]
    digital_ops = row["Nb opérations digitales annuelles"]
    situation = row["Situation"]

    # Groupe d'âge
    if age < 30:
        age_group = "jeune"
    elif age < 45:
        age_group = "actif"
    else:
        age_group = "sénior"

    # Groupe de revenu
    if revenu < 30000:
        revenu_group = "très faible revenu"
    elif revenu < 100000:
        revenu_group = "revenu modeste"
    elif revenu < 200000:
        revenu_group = "revenu intermédiaire"
    elif revenu < 300000:
        revenu_group = "haut revenu"
    else:
        revenu_group = "très haut revenu"

    # Groupe digital
    if digital_ops < 10:
        digital_group = "peu digitalisé"
    elif digital_ops < 20:
        digital_group = "digitalisation modérée"
    else:
        digital_group = "très digitalisé"

    # Mapping situation
    mapping_situation = {
        0: "fonctionnaire",
        1: "salarié privé",
        2: "retraité",
        3: "étudiant",
        4: "indépendant",
        5: "inactif",
    }
    situation_label = mapping_situation.get(situation, "autre")

    return f"{age_group}, {situation_label}, {revenu_group}, {digital_group}"


data["Cluster Label"] = data.apply(nommer_cluster, axis=1)

# 7.1 Nombre total de personnes par cluster
cluster_counts = (
    data["Cluster"].value_counts().sort_index().rename("Nombre de personnes")
)

# 7.2 médiane des features
cluster_medians = data.groupby("Cluster")[columns_features].median().round(2)

# 7.3 Pourcentages des produits par cluster
cluster_products_pct = (
    data.groupby("Cluster")[columns_produits]
    .sum()
    .div(data.groupby("Cluster").size(), axis=0)
    .multiply(100)
    .round(1)
)

# 8. Fusion des résultats
summary = pd.concat([cluster_counts, cluster_medians, cluster_products_pct], axis=1)
summary.index.name = "Cluster"
summary.reset_index(inplace=True)

# 9. Ajouter un libellé global pour chaque cluster basé sur la modalité la plus fréquente
cluster_labels = data.groupby("Cluster")["Cluster Label"].agg(lambda x: x.mode()[0])
summary = summary.merge(cluster_labels, on="Cluster")

# 10. Export final
output_path = "Data/Clustering summaries/clustering_summary_kmedoids.xlsx"
summary.to_excel(output_path, index=False)

print(f"\nAnalyse cluster exportée avec libellés vers : {output_path}")


# Dossier de sauvegarde des modèles
model_folder = "Data/models"
os.makedirs(model_folder, exist_ok=True)

# Sauvegarde du scaler
joblib.dump(scaler, os.path.join(model_folder, "scaler_kmedoids.pkl"))

# Sauvegarde du modèle KMedoids
joblib.dump(kmedoids_final, os.path.join(model_folder, "kmedoids_model.pkl"))

print("✅ Scaler et modèle KMedoids sauvegardés avec succès dans :")
print(model_folder)


# --------- 1. DÉFINIR LE DOSSIER DES FICHIERS BANCAIRES ---------
chemin_dossier = "Data/Clustering summaries"

# --------- 2. LISTER LES FICHIERS EXCEL ---------
fichiers_excel = [f for f in os.listdir(chemin_dossier) if f.endswith(".xlsx")]

# --------- 3. IDENTIFIER TOUTES LES COLONNES PRODUITS ---------
ensemble_colonnes_produits = set()
dataframes_temp = []

for f in fichiers_excel:
    chemin_fichier = os.path.join(chemin_dossier, f)
    df = pd.read_excel(chemin_fichier)
    dataframes_temp.append((f, df))

    # Colonnes candidates = celles contenant "Produit"
    colonnes_produits = [col for col in df.columns if "Produit" in col]
    ensemble_colonnes_produits.update(colonnes_produits)

ensemble_colonnes_produits = list(ensemble_colonnes_produits)

# --------- 4. HARMONISER LES COLONNES ---------
dataframes = []
for f, df in dataframes_temp:
    # Ajouter les colonnes manquantes avec valeur 0
    for col in ensemble_colonnes_produits:
        if col not in df.columns:
            df[col] = 0

    # Ajouter identifiant banque
    code_banque = os.path.splitext(f)[0].split("_")[0]
    df["CodeBanque"] = code_banque

    dataframes.append(df)

# --------- 5. CONCATÉNER TOUS LES FICHIERS ---------
data_concatenee = pd.concat(dataframes, ignore_index=True)

# --------- 6. SAUVEGARDE ---------
chemin_sortie = "Data/concatene_banques.xlsx"
data_concatenee.to_excel(chemin_sortie, index=False)

print(f"✅ Fichiers fusionnés avec succès dans :\n{chemin_sortie}")


# Charger le fichier
file_path = "Data/concatene_banques.xlsx"
df = pd.read_excel(file_path)

# Colonnes spéciales avec règles différentes
col_sum = ["Nombre de personnes"]
col_mode = ["Statut marital", "Situation", "Propriétaire"]
col_age = ["Âge"]

# Colonnes à exclure du traitement
exclude_cols = ["Cluster", "CodeBanque", "Cluster Label"]


# Fonction pour calculer la valeur la plus fréquente (mode)
def mode_most_common(series):
    return Counter(series).most_common(1)[0][0]


# Fonction de fusion d'un groupe
def merge_group(group):
    total_people = group["Nombre de personnes"].sum()

    merged = {}
    # 1. Somme pour "Nombre de personnes"
    merged["Nombre de personnes"] = total_people

    # 2. Moyenne pondérée pour Âge
    merged["Âge"] = (group["Âge"] * group["Nombre de personnes"]).sum() / total_people

    # 3. Valeur la plus fréquente pour certaines colonnes
    for col in col_mode:
        merged[col] = mode_most_common(group[col])

    # 4. Moyenne pondérée pour les autres colonnes numériques
    other_cols = [
        c
        for c in group.columns
        if c not in (col_sum + col_mode + col_age + exclude_cols)
    ]
    for col in other_cols:
        merged[col] = (group[col] * group["Nombre de personnes"]).sum() / total_people

    # 5. Garder le Cluster Label
    merged["Cluster Label"] = group["Cluster Label"].iloc[0]

    return pd.Series(merged)


# Appliquer la fusion par Cluster Label
df_merged = df.groupby("Cluster Label", as_index=False).apply(merge_group)

# Réordonner les colonnes comme à l'origine (sans CodeBanque, mais avec un nouveau Cluster)
cols_order = ["Cluster"] + [c for c in df.columns if c not in ["Cluster", "CodeBanque"]]
df_merged.insert(0, "Cluster", range(len(df_merged)))

# Sauvegarder le fichier
output_path = "Data/meta.xlsx"
df_merged.to_excel(output_path, index=False)

print(f"Fichier fusionné sauvegardé : {output_path}")


# Fonction pour prédire le cluster
def predict_cluster(df_summary, client_features, features):
    summary_features = df_summary[features].values
    distances = [cityblock(client_features, row) for row in summary_features]
    closest_idx = np.argmin(distances)
    closest_cluster = df_summary.iloc[closest_idx]
    return closest_cluster["Cluster"], closest_cluster["Cluster Label"]


# Fonction pour obtenir les recommandations basées sur le clustering (seuil > 30 %)
def get_cluster_recommendations(
    closest_cluster, product_cols, df_client, source="Banque"
):
    recommendations = []
    for col in product_cols:
        if closest_cluster[col] > 30 and df_client[col].iloc[0] == 0:
            recommendations.append((col, closest_cluster[col], source))
    return recommendations


# Fonction pour obtenir les recommandations des experts (valeur 100)
def get_expert_recommendations(df_expert, cluster_id, product_cols, df_client):
    recommendations = []
    expert_row = df_expert[df_expert["Cluster"] == cluster_id]
    if not expert_row.empty:
        for col in product_cols:
            if expert_row[col].iloc[0] == 100 and df_client[col].iloc[0] == 0:
                recommendations.append((col, 100.0, "Expert"))
    return recommendations


# Charger les fichiers
meta_path = "Data/meta.xlsx"
client_path = "Data/client_input.xlsx"
local_summary_path = "Data/Clustering summaries/clustering_summary_kmedoids.xlsx"
expert_path = "Data/experts.xlsx"

df_meta = pd.read_excel(meta_path)
df_client = pd.read_excel(client_path)

# Colonnes à utiliser pour la prédiction (excluant les colonnes de produits)
features = [
    "Âge",
    "Revenu annuel",
    "Situation",
    "Statut marital",
    "Propriétaire",
    "Nombre d’enfants",
    "Nb mouvements créditeurs",
    "Montant mouvements créditeurs",
    "Nb mouvements débiteurs",
    "Montant mouvements débiteurs",
    "Nb transactions carte (national)",
    "Montant transactions carte (national)",
    "Nb transactions carte (international)",
    "Montant transactions carte (international)",
    "Nb opérations digitales annuelles",
]

# Colonnes des produits (basées sur le meta pour harmonisation globale)
product_cols = [col for col in df_meta.columns if col.startswith("Produit -")]

# Harmoniser les colonnes produits dans df_client
for col in product_cols:
    if col not in df_client.columns:
        df_client[col] = 0.0

# Extraire les caractéristiques du client
client_features = df_client[features].iloc[0].values

# Prédiction et recommandations sur le clustering local
print("\n--- Des Clients qui vous ressemblent au sein de la banque ---")
if os.path.exists(local_summary_path):
    df_local = pd.read_excel(local_summary_path)
    # Harmonisation des colonnes produits dans df_local
    for col in product_cols:
        if col not in df_local.columns:
            df_local[col] = 0.0

    # Prédire le cluster local
    local_cluster_id, local_cluster_label = predict_cluster(
        df_local, client_features, features
    )
    closest_local_cluster = df_local[df_local["Cluster"] == local_cluster_id]

    print(f"Vous appartenez au cluster: {local_cluster_label}")

    # 1. Recommandations basées sur le clustering local (> 30 %)
    local_recommendations = get_cluster_recommendations(
        closest_local_cluster.iloc[0], product_cols, df_client, source="Banque"
    )
    print("\nRecommandations basées sur les clients similaires :")
    if local_recommendations:
        for product, percentage, source in local_recommendations:
            print(f"- {product} ({percentage:.1f} % des clients du cluster)")
        results = [
            {"product": product, "percentage": percentage}
            for product, percentage, _ in local_recommendations
        ]
        local_recommendations_output_file = "Data/results/local_recommendations.json"

        with open(local_recommendations_output_file, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
    else:
        print(
            "Aucun produit recommandé (tous les produits avec > 30 % de souscription sont déjà détenus)."
        )

    # 2. Recommandations basées sur les experts (valeur 100)
    print("\nRecommandations basées sur les experts :")
    if os.path.exists(expert_path):
        df_expert = pd.read_excel(expert_path)
        # Harmonisation des colonnes produits dans df_expert
        for col in product_cols:
            if col not in df_expert.columns:
                df_expert[col] = 0.0
        expert_recommendations = get_expert_recommendations(
            df_expert, local_cluster_id, product_cols, df_client
        )
        if expert_recommendations:
            for product, _, source in expert_recommendations:
                print(f"- {product} ")
            results = [{"product": product} for product, _, _ in expert_recommendations]
            expert_recommendations_output_file = (
                "Data/results/expert_recommendations.json"
            )
            with open(expert_recommendations_output_file, "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
        else:
            print(
                "Aucun produit recommandé (tous les produits marqués par les experts sont déjà détenus)."
            )

    else:
        print(
            f"[AVERTISSEMENT] Fichier expert non trouvé : {expert_path}. Les recommandations d'experts sont ignorées."
        )
else:
    print(
        f"[ERREUR] Fichier local non trouvé : {local_summary_path}. Prédiction locale et recommandations ignorées."
    )

# Prédiction et recommandations sur le meta-clustering
print("\n--- Des Clients qui vous ressemblent au sein du marché bancaire ---")
meta_cluster_id, meta_cluster_label = predict_cluster(
    df_meta, client_features, features
)
closest_meta_cluster = df_meta[df_meta["Cluster"] == meta_cluster_id]
meta_recommendations = get_cluster_recommendations(
    closest_meta_cluster.iloc[0], product_cols, df_client, source="Meta"
)
print(f"Vous appartenez au cluster: {meta_cluster_label}")
print("\nRecommandations basées sur le marché bancaire :")
if meta_recommendations:
    for product, percentage, source in meta_recommendations:
        print(f"- {product} ({percentage:.1f} % des clients du cluster)")
    results = [
        {"product": product, "percentage": percentage}
        for product, percentage, _ in meta_recommendations
    ]
    meta_recommendations_output_file = "Data/results/meta_recommendations.json"

    with open(meta_recommendations_output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
else:
    print(
        "Aucun produit recommandé (tous les produits avec > 30 % de souscription sont déjà détenus)."
    )
