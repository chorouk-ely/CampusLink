import sqlite3

connexion = sqlite3.connect('campuslink.db')
curseur = connexion.cursor()

curseur.execute(
    "INSERT INTO users (nom, email, mot_de_passe, role, classe) VALUES (?, ?, ?, ?, ?)",
    ("Alex Étudiant", "alex@supmti.ma", "1234", "etudiant", "GI-Ann3")
)

curseur.execute(
    "INSERT INTO users (nom, email, mot_de_passe, role, classe) VALUES (?, ?, ?, ?, ?)",
    ("Sara Benali", "sara@supmti.ma", "1234", "etudiant", "GI-Ann3")
)

curseur.execute(
    "INSERT INTO users (nom, email, mot_de_passe, role, classe) VALUES (?, ?, ?, ?, ?)",
    ("Prof Karim", "karim@supmti.ma", "1234", "enseignant", None)
)

connexion.commit()
connexion.close()

print("Comptes de test créés avec succès !")