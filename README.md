# Projet 5 – Migration CSV vers MongoDB
## *1 Objectif du projet*

Transférer les datas du fichier healthcare_dataset.csv vers MongoDB sous une structure "MongoDB like" :
    - Un document par patient  
    - Chaque patient possède un tableau d'admissions contenant toutes ses hospitalisations  
    - Nettoyage auto des doublons  
    - Vérification des données manquantes  

Dans ce projet vous verrez :  
    - La manipulation de mongoDB: CRUD  
    - Tansformation de données avec Python Pandas  
    - La création d'un pipe automatisé d'import des données  


## *2 Structure des données*

Le CSV initial contient les colonnes suivantes :  

Name	STRING	Nom du patient  
Age	INTEGER	Âge en années  
Gender	STRING	"Male" / "Female"  
Blood Type	STRING	Groupe sanguin (A+, O-, …)  
Medical Condition	STRING	Diagnostic principal   
Date of Admission	DATE	Date d’admission  
Doctor	STRING	Nom du médecin  
Hospital	STRING	Nom de l’hôpital  
Insurance Provider	STRING	Ex : Aetna, Medicare  
Billing Amount	FLOAT	Montant facturé  
Room Number	STRING	Numéro de chambre  
Admission Type	STRING	"Emergency", "Elective", "Urgent"  
Discharge Date	DATE	Date de sortie  
Medication	STRING	Médicaments administrés  
Test Results	STRING	"Normal", "Abnormal", "Inconclusive"  


Structure finale (json) :  
```
{
  "_id": {
    "$oid": "68de447c75d9bf09c0cc7be2"
  },
  "Name": "AARON bAldWIN Jr.",
  "Age": 20,
  "Gender": "Male",
  "Blood Type": "O-",
  "Admissions": [
    {
      "Medical Condition": "Hypertension",
      "Date of Admission": "2020-10-10",
      "Doctor": "Amy Farley",
      "Hospital": "Flores Friedman and White,",
      "Insurance Provider": "Medicare",
      "Billing Amount": 29740.9601987263,
      "Room Number": 104,
      "Admission Type": "Urgent",
      "Discharge Date": "2020-11-05",
      "Medication": "Paracetamol",
      "Test Results": "Abnormal"
    }
  ]
},
```


## *3 Pré-requis*

- Python 3.x  
- MongoDB installé localement et en cours d’exécution  
- Modules Python :  
    - pandas  
    - pymongo  
    - dnspython  

Vous pouvez installer toutes les dépendances via :

```pip install -r requirements.txt```


## *4 Utilisation du script*

Mettre healthcare_dataset.csv dans le dossier archive/
Exécuter le script : python import_healthcare_mongo.py

Le script effectue
- Lecture du CSV  
- Nettoyage des doublons  
- Vérification des valeurs nulles
- Groupement des admissions par patients ayant name, age, gender et blood type similaires  
- Création du json healthcare_dataset.json
- Import auto dans la base MongoDB healthcare et la collection patients

*!!! ATTENTION a chaque éxécution la collection est supprimée et recréée*


## *5 Validation des données*

Le script affiche:
- Nombre de doublons supprimés
- Le nombre de valeurs manquantes par colonnes
- Le nombre de patients avec plusieurs admissions


## *6 Structure des fichiers*

Projet_5/  
|  
|- archive/  
|   |-healthcare_dataset.csv  
|   |-healthcare_dataset.json  
|  
|-import_healthcare_mongo.py  
|-requirements.txt  
|-README.md  


