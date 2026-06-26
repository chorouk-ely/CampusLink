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

# Récupérer les IDs des étudiants
curseur.execute("SELECT id FROM users WHERE email = 'alex@supmti.ma'")
alex_id = curseur.fetchone()[0]

curseur.execute("SELECT id FROM users WHERE email = 'sara@supmti.ma'")
sara_id = curseur.fetchone()[0]

# Attendance pour Alex
curseur.execute("INSERT INTO attendance (etudiant_id, module, semestre, presences, absences) VALUES (?, ?, ?, ?, ?)",
    (alex_id, "(1) Introduction à l'informatique", "Semestre 1", 18, 2))
curseur.execute("INSERT INTO attendance (etudiant_id, module, semestre, presences, absences) VALUES (?, ?, ?, ?, ?)",
    (alex_id, "(2) Mathématiques discrètes", "Semestre 1", 15, 5))
curseur.execute("INSERT INTO attendance (etudiant_id, module, semestre, presences, absences) VALUES (?, ?, ?, ?, ?)",
    (alex_id, "(3) Algorithmique", "Semestre 1", 19, 1))

# Attendance pour Sara
curseur.execute("INSERT INTO attendance (etudiant_id, module, semestre, presences, absences) VALUES (?, ?, ?, ?, ?)",
    (sara_id, "(1) Introduction à l'informatique", "Semestre 1", 17, 3))
curseur.execute("INSERT INTO attendance (etudiant_id, module, semestre, presences, absences) VALUES (?, ?, ?, ?, ?)",
    (sara_id, "(2) Mathématiques discrètes", "Semestre 1", 14, 6))
curseur.execute("INSERT INTO attendance (etudiant_id, module, semestre, presences, absences) VALUES (?, ?, ?, ?, ?)",
    (sara_id, "(3) Algorithmique", "Semestre 1", 20, 0))

connexion.commit()
connexion.close()

print("Attendance ajoutée avec succès !")