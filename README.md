# CampusLink SUPMTI

Plateforme web de gestion academique developpee avec Flask (Python) dans le cadre d'un stage d'initiation de 3eme annee Genie Informatique a SUPMTI.

---

## Technologies utilisees

| Composant | Technologie |
|---|---|
| Backend | Python 3 / Flask |
| Base de donnees | SQLite 3 |
| Frontend | HTML5 / CSS3 / JavaScript |
| Generation PDF | fpdf2 |
| Gestion fichiers | Werkzeug |

---

## Installation

### Prerequis

- Python 3.10 ou superieur
- pip

### Etapes

1. Extraire le projet dans un dossier local

2. Installer les dependances :
```
pip install flask fpdf2
```

3. Creer la base de donnees :
```
python database.py
```

4. Inserer des comptes de test :
```
python seed.py
```

5. Lancer le serveur :
```
python app.py
```

6. Ouvrir dans le navigateur : `http://127.0.0.1:5000`

---

## Comptes de test

| Role | Email | Mot de passe |
|---|---|---|
| Etudiant | alex@supmti.ma | 1234 |
| Enseignant | karim@supmti.ma | 1234 |
| Admin | sophie@supmti.ma | 1234 |

---

## Structure du projet

```
CampusLink/
│
├── app.py                  # Point d'entree - toutes les routes Flask
├── database.py             # Creation des tables SQLite
├── seed.py                 # Insertion des donnees de test
├── translations.py         # Traductions FR / AR / EN
├── campuslink.db            # Base de donnees SQLite (generee)
│
├── static/
│   ├── css/                # Feuilles de style par espace
│   ├── js/                 # Scripts JavaScript
│   ├── images/             # Images fixes du site
│   └── uploads/            # Photos uploadees par l'admin
│
└── templates/
    ├── base.html            # Layout commun (sidebar, topbar)
    ├── index.html           # Page publique d'accueil
    ├── login.html           # Connexion
    ├── forgot_password.html
    ├── verify_code.html
    ├── reset_password.html
    ├── dashboard_etudiant.html
    ├── grades_etudiant.html
    ├── appeal.html
    ├── grade_entry.html
    ├── appeals_enseignant.html
    ├── settings.html
    ├── dashboard_admin.html
    ├── admin_announcements.html
    ├── edit_announcement.html
    ├── academic_structure.html
    ├── user_management.html
    ├── edit_user.html
    └── admin_appeals.html
```

---

## Base de donnees - 10 tables

| Table | Description |
|---|---|
| `users` | Tous les comptes avec role, CNE, CIN, photo |
| `notes` | Notes CC + Examen par module et semestre |
| `annonces` | Annonces publiees par l'admin |
| `messages` | Appels entre etudiants et enseignants |
| `departments` | Departements de l'ecole |
| `filieres` | Filieres par departement |
| `annees` | Annees par filiere |
| `semestres` | Semestres par annee |
| `modules_academiques` | Modules par semestre |
| `matieres` | Matieres avec coefficient par module |

---

## Fonctionnalites par role

### Page publique (sans connexion)
- Annonces reelles publiees par l'admin
- Liste des enseignants avec leur photo
- Changement de langue : Francais / Arabe / Anglais
- Recuperation de mot de passe par code de verification

### Etudiant
- Dashboard avec statistiques
- Notes par semestre (CC, Examen, Moyenne, Statut)
- Export du releve de notes en PDF
- Envoi de messages aux enseignants et consultation des reponses
- Changement de mot de passe

### Enseignant
- Saisie des notes par classe, module et semestre
- Calcul automatique de la moyenne selon le seuil
- Reception et reponse aux messages des etudiants (avec filtre par classe)
- Changement de mot de passe

### Administrateur
- Statistiques globales (etudiants, enseignants, classes, moyenne)
- Gestion complete des annonces (CRUD)
- Structure academique : Departement > Filiere > Annee > Semestre > Module > Matiere
- Gestion des utilisateurs avec photo, CNE, CIN
- Consultation de tous les appels etudiants/enseignants
- Changement de mot de passe

---

## Routes principales

| URL | Role | Description |
|---|---|---|
| `/` | Public | Page d'accueil |
| `/login` | Public | Connexion |
| `/logout` | Tous | Deconnexion |
| `/set-language/<lang>` | Public | Changement de langue |
| `/forgot-password` | Public | Demande de reinitialisation |
| `/verify-code` | Public | Verification du code recu |
| `/reset-password` | Public | Nouveau mot de passe |
| `/dashboard-etudiant` | Etudiant | Tableau de bord |
| `/grades-etudiant` | Etudiant | Tableau de notes |
| `/export-pdf-notes` | Etudiant | Telechargement PDF |
| `/send-appeal` | Etudiant | Message a un enseignant |
| `/settings-etudiant` | Etudiant | Changement de mot de passe |
| `/dashboard-enseignant` | Enseignant | Redirection vers saisie des notes |
| `/grade-entry` | Enseignant | Saisie des notes |
| `/appeals-enseignant` | Enseignant | Messages recus |
| `/settings-enseignant` | Enseignant | Changement de mot de passe |
| `/dashboard-admin` | Admin | Dashboard |
| `/admin/announcements` | Admin | Gestion des annonces |
| `/admin/academic-structure` | Admin | Structure academique |
| `/admin/users` | Admin | Gestion des utilisateurs |
| `/admin/appeals` | Admin | Consultation des appels |
| `/settings-admin` | Admin | Changement de mot de passe |

---

## Note sur la securite

Les mots de passe sont stockes en clair dans cette version (stage d'initiation).
Pour une mise en production, utiliser `werkzeug.security.generate_password_hash`.

Le code de verification pour la reinitialisation du mot de passe est simule (affiche dans la console du serveur) et non envoye par email reel.

---

## Auteur
El Youncha Malak -----El Youbi Chorouk

Stage d'initiation - 3 éme annee Genie Informatique
SUPMTI - 2026