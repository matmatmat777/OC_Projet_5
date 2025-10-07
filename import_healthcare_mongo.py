import pandas as pd
from bson import ObjectId
from pymongo import MongoClient
import os
import time
from pymongo.errors import ServerSelectionTimeoutError, BulkWriteError

# --- Lecture CSV ---
csv_path = "/app/archive/healthcare_dataset.csv"
data = pd.read_csv(csv_path, low_memory=False)

print("\nInformations sur le dataset :")
data.info()
print("\nNombre de valeurs manquantes par colonne :")
print(data.isnull().sum())
print("\nNombre de doublons exacts :", data.duplicated().sum())

# --- Nettoyage ---
data_clean = data.drop_duplicates()

group_cols = ['Name', 'Age', 'Gender', 'Blood Type']
admission_cols = [col for col in data_clean.columns if col not in group_cols]

# --- Patients avec multiples admissions ---
multi_admissions = data_clean.groupby(group_cols).size()
multi_admissions = multi_admissions[multi_admissions > 1]

print(f"\nNombre de patients avec plusieurs admissions : {len(multi_admissions)}")
if len(multi_admissions) > 0:
    print("Exemple de patient avec plusieurs admissions :")
    print(multi_admissions.head(1))

# --- Regrouper les admissions par patient ---
grouped = data_clean.groupby(group_cols).apply(
    lambda x: x[admission_cols].to_dict(orient='records')
).reset_index()

grouped.columns = group_cols + ['Admissions']

# --- Créer les documents MongoDB ---
mongo_docs = []
for _, row in grouped.iterrows():
    mongo_docs.append({
        "_id": str(ObjectId()),
        "Name": row['Name'],
        "Age": row['Age'],
        "Gender": row['Gender'],
        "Blood Type": row['Blood Type'],
        "Admissions": row['Admissions']
    })

# --- Connexion MongoDB ---
mongo_uri = os.environ.get("MONGO_URI")
if not mongo_uri:
    raise Exception("Variable d'environnement MONGO_URI non définie.")

client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)

# Attendre que MongoDB soit prêt
for i in range(20):  # retry jusqu'à 20 fois
    try:
        client.admin.command('ping')
        print("MongoDB connecté !")
        break
    except ServerSelectionTimeoutError:
        print("MongoDB non prêt, retry dans 3s...")
        time.sleep(3)
else:
    raise Exception("Impossible de se connecter à MongoDB")

db_name = os.environ.get("MONGO_DB", "healthcare_db")
db = client[db_name]
collection = db["patients"]

# --- Nettoyer la collection existante (optionnel) ---
# Uncomment si tu veux réinitialiser la collection à chaque exécution
# collection.delete_many({})

# --- Import direct ---
try:
    collection.insert_many(mongo_docs, ordered=False)
    print(f"{len(mongo_docs)} documents insérés dans MongoDB avec succès !")
except BulkWriteError as bwe:
    print("Erreur lors de l'insertion :")
    print(bwe.details)

# --- Vérification simple ---
pipeline = [
    {"$project": {"Name": 1, "NumAdmissions": {"$size": "$Admissions"}}},
    {"$match": {"NumAdmissions": {"$gt": 1}}}
]

patients_multi = list(collection.aggregate(pipeline))
print(f"\nNombre de patients avec plusieurs admissions dans MongoDB : {len(patients_multi)}")
if patients_multi:
    print("Exemple :", patients_multi[0])

#--- Vérification de l'utilisateur connecté ---
db_user = client.admin.command("connectionStatus")["authInfo"]["authenticatedUsers"]
print("Utilisateur authentifié :", db_user)
