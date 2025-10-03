# import_healthcare_mongo.py
"""
Script pour transformer un CSV de patients en documents MongoDB,
avec vérification automatique des données et import direct dans MongoDB.
"""

import pandas as pd
from bson import ObjectId
from pymongo import MongoClient

# -----------------------
# 1️⃣ Lecture du CSV
# -----------------------
#csv_path = r"C:\Users\matde\Documents\OpenClassrooms\Projet_5\archive\healthcare_dataset.csv"
csv_path = "/app/archive/healthcare_dataset.csv"
data = pd.read_csv(csv_path, low_memory=False)

print("\nInformations sur le dataset :")
data.info()
print("\nNombre de valeurs manquantes par colonne :")
print(data.isnull().sum())
print("\nNombre de doublons exacts :", data.duplicated().sum())

# -----------------------
# 2️⃣ Nettoyage des données
# -----------------------
data_clean = data.drop_duplicates()

# Colonnes pour identifier un patient unique
group_cols = ['Name', 'Age', 'Gender', 'Blood Type']
admission_cols = [col for col in data_clean.columns if col not in group_cols]

# -----------------------
# 3️⃣ Vérifier les patients avec plusieurs admissions
# -----------------------
multi_admissions = data_clean.groupby(group_cols).size()
multi_admissions = multi_admissions[multi_admissions > 1]

print(f"\nNombre de patients avec plusieurs admissions : {len(multi_admissions)}")
if len(multi_admissions) > 0:
    print("Exemple de patient avec plusieurs admissions :")
    print(multi_admissions.head(1))

# -----------------------
# 4️⃣ Regrouper les admissions par patient
# -----------------------
grouped = data_clean.groupby(group_cols).apply(
    lambda x: x[admission_cols].to_dict(orient='records')
).reset_index()

grouped.columns = group_cols + ['Admissions']

# -----------------------
# 5️⃣ Créer les documents MongoDB
# -----------------------
mongo_docs = []
for _, row in grouped.iterrows():
    mongo_docs.append({
        "_id": str(ObjectId()),  # Génère un ObjectId valide MongoDB
        "Name": row['Name'],
        "Age": row['Age'],
        "Gender": row['Gender'],
        "Blood Type": row['Blood Type'],
        "Admissions": row['Admissions']
    })

# -----------------------
# 6️⃣ Connexion à MongoDB
# -----------------------
client = MongoClient("mongodb://mongo:27017/")      # MongoDB local - nom du service docker à la place de localhost
db = client["healthcare_db"]                        # Nom de la base
collection = db["patients"]                         # Nom de la collection

# -----------------------
# 7️⃣ Nettoyer la collection existante (optionnel)
# -----------------------
collection.delete_many({})  # Supprime tous les documents existants
print("\nCollection 'patients' nettoyée.")

# -----------------------
# 8️⃣ Import direct dans MongoDB
# -----------------------
collection.insert_many(mongo_docs)
print(f"{len(mongo_docs)} documents insérés dans MongoDB avec succès !")

# -----------------------
# 9️⃣ Vérification simple
# -----------------------
# Patients avec plusieurs admissions
pipeline = [
    {"$project": {"Name": 1, "NumAdmissions": {"$size": "$Admissions"}}},
    {"$match": {"NumAdmissions": {"$gt": 1}}}
]

patients_multi = list(collection.aggregate(pipeline))
print(f"\nNombre de patients avec plusieurs admissions dans MongoDB : {len(patients_multi)}")
if patients_multi:
    print("Exemple :", patients_multi[0])
