// Connexion à la base spécifiée pour l'application
db = db.getSiblingDB("healthcare_db");

// Création de l'utilisateur applicatif
db.createUser({
  user: "app_user",
  pwd: "app_pwd_secure",
  roles: [
    { role: "readWrite", db: "healthcare_db" }
  ]
});

print("✅ Utilisateur 'app_user' créé pour la base 'healthcare_db'.");
