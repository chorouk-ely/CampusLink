import sqlite3

connexion = sqlite3.connect('campuslink.db')
curseur = connexion.cursor()

curseur.execute(
    "INSERT OR IGNORE INTO users (nom, email, mot_de_passe, role, classe, cne, cin, photo) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
    ("Alex Étudiant", "alex@supmti.ma", "1234", "etudiant", "GI-Ann3", "CNE001", "CIN001", "alex.png")
)

curseur.execute(
    "INSERT OR IGNORE INTO users (nom, email, mot_de_passe, role, classe, cne, cin, photo) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
    ("Prof Karim", "karim@supmti.ma", "1234", "enseignant", None, None, None, "karim.png")
)

curseur.execute(
    "INSERT OR IGNORE INTO users (nom, email, mot_de_passe, role, classe, cne, cin, photo) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
    ("Sophie Chen", "sophie@supmti.ma", "1234", "admin", None, None, None, "sophie.png")
)

connexion.commit()
connexion.close()

print("Comptes créés avec succès !")

