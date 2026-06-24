import sqlite3

connexion = sqlite3.connect('campuslink.db')
curseur = connexion.cursor()

curseur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        mot_de_passe TEXT NOT NULL,
        role TEXT NOT NULL,
        classe TEXT
    )
''')

curseur.execute('''
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        etudiant_id INTEGER NOT NULL,
        module TEXT NOT NULL,
        semestre TEXT NOT NULL,
        cc_grade REAL,
        exam_grade REAL,
        seuil REAL DEFAULT 10,
        FOREIGN KEY (etudiant_id) REFERENCES users (id)
    )
''')

curseur.execute('''
    CREATE TABLE IF NOT EXISTS annonces (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titre TEXT NOT NULL,
        contenu TEXT NOT NULL,
        date_publication TEXT NOT NULL,
        archivee INTEGER DEFAULT 0
    )
''')

curseur.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        etudiant_id INTEGER NOT NULL,
        enseignant_id INTEGER NOT NULL,
        contenu TEXT NOT NULL,
        reponse TEXT,
        date_envoi TEXT NOT NULL,
        statut TEXT DEFAULT 'pending',
        FOREIGN KEY (etudiant_id) REFERENCES users (id),
        FOREIGN KEY (enseignant_id) REFERENCES users (id)
    )
''')

connexion.commit()
connexion.close()

print("Base de données créée avec succès !")