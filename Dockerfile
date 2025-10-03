# Utilise une image Python officielle
FROM python:3.11-slim

# Définit le dossier de travail dans le conteneur
WORKDIR /app

# Copie requirements.txt et installe les dépendances
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copie ton script Python
COPY import_healthcare_mongo.py ./

# Par défaut, lance le script
CMD ["python", "import_healthcare_mongo.py"]