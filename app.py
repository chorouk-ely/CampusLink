from flask import Flask, render_template, session, redirect, url_for, request
import sqlite3
from translations import TRANSLATIONS
import random
from datetime import datetime, timedelta


app = Flask(__name__)
app.secret_key = 'cle-secrete-a-changer-plus-tard'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/set-language/<lang>')
def set_language(lang):
    session['lang'] = lang
    return redirect(request.referrer or url_for('home'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    lang = session.get('lang', 'fr')
    t = TRANSLATIONS[lang]
    erreur = None

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        connexion = sqlite3.connect('campuslink.db')
        curseur = connexion.cursor()
        curseur.execute(
            "SELECT id, nom, role FROM users WHERE email = ? AND mot_de_passe = ?",
            (email, password)
        )
        utilisateur = curseur.fetchone()
        connexion.close()

        if utilisateur:
            session['user_id'] = utilisateur[0]
            session['user_nom'] = utilisateur[1]
            session['user_role'] = utilisateur[2]

            if utilisateur[2] == 'etudiant':
                return redirect(url_for('dashboard_etudiant'))
            elif utilisateur[2] == 'enseignant':
                return redirect(url_for('dashboard_enseignant'))
            elif utilisateur[2] == 'admin':
                return redirect(url_for('dashboard_admin'))
        else:
            erreur = "Email ou mot de passe incorrect."

    connexion = sqlite3.connect('campuslink.db')
    curseur = connexion.cursor()
    curseur.execute(
        "SELECT titre FROM annonces WHERE archivee = 0 ORDER BY date_publication DESC LIMIT 1"
    )
    resultat = curseur.fetchone()
    connexion.close()
    derniere_annonce = resultat[0] if resultat else "Aucune annonce pour le moment"

    return render_template('login.html', t=t, lang=lang, erreur=erreur, derniere_annonce=derniere_annonce)


@app.route('/dashboard-etudiant')
def dashboard_etudiant():
    if session.get('user_role') != 'etudiant':
        return redirect(url_for('login'))
    return render_template('dashboard_etudiant.html', nom=session.get('user_nom'))


@app.route('/dashboard-enseignant')
def dashboard_enseignant():
    if session.get('user_role') != 'enseignant':
        return redirect(url_for('login'))
    return render_template('dashboard_enseignant.html', nom=session.get('user_nom'))


@app.route('/grade-entry', methods=['GET', 'POST'])
def grade_entry():
    if session.get('user_role') != 'enseignant':
        return redirect(url_for('login'))

    connexion = sqlite3.connect('campuslink.db')
    curseur = connexion.cursor()

    curseur.execute("SELECT DISTINCT classe FROM users WHERE role = 'etudiant' AND classe IS NOT NULL")
    classes = [c[0] for c in curseur.fetchall()]

    classe_choisie = request.args.get('classe')
    module = request.args.get('module')
    semestre = request.args.get('semestre')

    if request.method == 'POST':
        classe_choisie = request.form.get('classe')
        module = request.form.get('module')
        semestre = request.form.get('semestre')

        curseur.execute("SELECT id FROM users WHERE role = 'etudiant' AND classe = ?", (classe_choisie,))
        ids_etudiants = [e[0] for e in curseur.fetchall()]

        for etudiant_id in ids_etudiants:
            cc = request.form.get(f'cc_{etudiant_id}')
            exam = request.form.get(f'exam_{etudiant_id}')
            seuil = request.form.get(f'seuil_{etudiant_id}') or 10

            curseur.execute(
                "SELECT id FROM notes WHERE etudiant_id = ? AND module = ? AND semestre = ?",
                (etudiant_id, module, semestre)
            )
            existant = curseur.fetchone()

            if existant:
                curseur.execute(
                    "UPDATE notes SET cc_grade = ?, exam_grade = ?, seuil = ? WHERE id = ?",
                    (cc, exam, seuil, existant[0])
                )
            else:
                curseur.execute(
                    "INSERT INTO notes (etudiant_id, module, semestre, cc_grade, exam_grade, seuil) VALUES (?, ?, ?, ?, ?, ?)",
                    (etudiant_id, module, semestre, cc, exam, seuil)
                )

        connexion.commit()

    etudiants_avec_notes = []
    if classe_choisie and module and semestre:
        curseur.execute('''
            SELECT users.id, users.nom, notes.cc_grade, notes.exam_grade, notes.seuil
            FROM users
            LEFT JOIN notes ON notes.etudiant_id = users.id AND notes.module = ? AND notes.semestre = ?
            WHERE users.role = 'etudiant' AND users.classe = ?
        ''', (module, semestre, classe_choisie))
        etudiants_avec_notes = curseur.fetchall()

    connexion.close()

    return render_template(
        'grade_entry.html',
        nom=session.get('user_nom'),
        classes=classes,
        classe_choisie=classe_choisie,
        module=module,
        semestre=semestre,
        etudiants=etudiants_avec_notes
    )


@app.route('/dashboard-admin')
def dashboard_admin():
    if session.get('user_role') != 'admin':
        return redirect(url_for('login'))

    connexion = sqlite3.connect('campuslink.db')
    curseur = connexion.cursor()

    curseur.execute("SELECT COUNT(*) FROM users WHERE role = 'etudiant'")
    total_etudiants = curseur.fetchone()[0]

    curseur.execute("SELECT COUNT(*) FROM users WHERE role = 'enseignant'")
    total_enseignants = curseur.fetchone()[0]

    curseur.execute("SELECT COUNT(DISTINCT classe) FROM users WHERE role = 'etudiant' AND classe IS NOT NULL")
    total_classes = curseur.fetchone()[0]

    curseur.execute("SELECT AVG((cc_grade + exam_grade) / 2) FROM notes WHERE cc_grade IS NOT NULL AND exam_grade IS NOT NULL")
    moyenne_generale = curseur.fetchone()[0]

    connexion.close()

    return render_template(
        'dashboard_admin.html',
        nom=session.get('user_nom'),
        total_etudiants=total_etudiants,
        total_enseignants=total_enseignants,
        total_classes=total_classes,
        moyenne_generale=round(moyenne_generale, 2) if moyenne_generale else 0
    )
import random
from datetime import datetime, timedelta

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    lang = session.get('lang', 'fr')
    t = TRANSLATIONS[lang]
    erreur = None

    if request.method == 'POST':
        email = request.form.get('email')

        connexion = sqlite3.connect('campuslink.db')
        curseur = connexion.cursor()
        curseur.execute("SELECT id FROM users WHERE email = ?", (email,))
        resultat = curseur.fetchone()
        connexion.close()

        if resultat:
            code = str(random.randint(100000, 999999))
            session['reset_email'] = email
            session['reset_code'] = code
            session['reset_code_time'] = datetime.now().isoformat()

            print(f"[SIMULATION EMAIL] Code envoyé à {email} : {code}")

            return redirect(url_for('verify_code'))
        else:
            erreur = "Aucun compte associé à cet email."

    return render_template('forgot_password.html', t=t, lang=lang, erreur=erreur)


@app.route('/verify-code', methods=['GET', 'POST'])
def verify_code():
    lang = session.get('lang', 'fr')
    t = TRANSLATIONS[lang]
    erreur = None

    if 'reset_email' not in session:
        return redirect(url_for('forgot_password'))

    if request.method == 'POST':
        code_saisi = request.form.get('code')
        code_time = datetime.fromisoformat(session.get('reset_code_time'))

        if datetime.now() - code_time > timedelta(minutes=10):
            erreur = "Le code a expiré, demandez-en un nouveau."
        elif code_saisi == session.get('reset_code'):
            session['code_verifie'] = True
            return redirect(url_for('reset_password'))
        else:
            erreur = "Code incorrect."

    return render_template('verify_code.html', t=t, lang=lang, erreur=erreur)


@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    lang = session.get('lang', 'fr')
    t = TRANSLATIONS[lang]

    if not session.get('code_verifie'):
        return redirect(url_for('forgot_password'))

    if request.method == 'POST':
        nouveau_mdp = request.form.get('password')
        email = session.get('reset_email')

        connexion = sqlite3.connect('campuslink.db')
        curseur = connexion.cursor()
        curseur.execute("UPDATE users SET mot_de_passe = ? WHERE email = ?", (nouveau_mdp, email))
        connexion.commit()
        connexion.close()

        session.pop('reset_email', None)
        session.pop('reset_code', None)
        session.pop('reset_code_time', None)
        session.pop('code_verifie', None)

        return redirect(url_for('login'))

    return render_template('reset_password.html', t=t, lang=lang)
@app.route('/attendance-etudiant')
def attendance_etudiant():
    if session.get('user_role') != 'etudiant':
        return redirect(url_for('login'))

    etudiant_id = session.get('user_id')

    connexion = sqlite3.connect('campuslink.db')
    curseur = connexion.cursor()
    curseur.execute(
        'SELECT module, semestre, presences, absences FROM attendance WHERE etudiant_id = ? ORDER BY module',
        (etudiant_id,)
    )
    rows = curseur.fetchall()
    connexion.close()

    attendance = [
        {'module': r[0], 'semestre': r[1], 'presences': r[2], 'absences': r[3]}
        for r in rows
    ]

    total_presences = sum(r['presences'] for r in attendance)
    total_absences  = sum(r['absences']  for r in attendance)
    total_seances   = total_presences + total_absences
    semestre        = attendance[0]['semestre'] if attendance else 'Semestre 1'

    return render_template(
        'attendance_etudiant.html',
        nom=session.get('user_nom'),
        attendance=attendance,
        total_presences=total_presences,
        total_absences=total_absences,
        total_seances=total_seances,
        semestre=semestre
    )

# ROUTE : Tableau de bord des notes de l'étudiant
# Affiche les notes par semestre (CC, Exam, Moyenne, Statut)
# avec le nombre de modules validés et en rattrapage

@app.route('/grades-etudiant')
def grades_etudiant():
    if session.get('user_role') != 'etudiant':
        return redirect(url_for('login'))

    etudiant_id = session.get('user_id')

    connexion = sqlite3.connect('campuslink.db')
    curseur = connexion.cursor()

    # Tous les semestres disponibles pour cet étudiant
    curseur.execute(
        "SELECT DISTINCT semestre FROM notes WHERE etudiant_id = ? ORDER BY semestre",
        (etudiant_id,)
    )
    semestres = [r[0] for r in curseur.fetchall()]
    if not semestres:
        semestres = ['Semestre 1']

    # Semestre actif (depuis l'URL ou le premier disponible)
    semestre_actif = request.args.get('semestre', semestres[0])

    # Notes du semestre actif
    curseur.execute('''
        SELECT module, semestre, cc_grade, exam_grade, seuil
        FROM notes
        WHERE etudiant_id = ? AND semestre = ?
        ORDER BY module
    ''', (etudiant_id, semestre_actif))
    rows = curseur.fetchall()
    connexion.close()

    notes = [
        {
            'module':     r[0],
            'semestre':   r[1],
            'cc_grade':   r[2],
            'exam_grade': r[3],
            'seuil':      r[4] if r[4] is not None else 10,
            'coeff':      2
        }
        for r in rows
    ]

    # Calcul passed / remedial
    passed  = 0
    remedial = 0
    for n in notes:
        if n['cc_grade'] is not None and n['exam_grade'] is not None:
            moyenne = n['cc_grade'] * 0.4 + n['exam_grade'] * 0.6
            if moyenne >= n['seuil']:
                passed += 1
            else:
                remedial += 1

    return render_template(
        'grades_etudiant.html',
        nom=session.get('user_nom'),
        notes=notes,
        semestres=semestres,
        semestre_actif=semestre_actif,
        passed=passed,
        remedial=remedial,
        total_modules=len(notes)
    )

# ROUTE : Envoi d'un appel de l'étudiant vers un professeur
# L'étudiant choisit un prof dans la liste et envoie un message
# Le message est stocké dans la table "messages" avec statut "pending"
from datetime import datetime

@app.route('/send-appeal', methods=['GET', 'POST'])
def send_appeal():
    if session.get('user_role') != 'etudiant':
        return redirect(url_for('login'))

    etudiant_id = session.get('user_id')
    success = False
    erreur = None
    form_contenu = ''
    form_enseignant = ''

    connexion = sqlite3.connect('campuslink.db')
    curseur = connexion.cursor()

    # Récupérer tous les professeurs depuis la base
    curseur.execute("SELECT id, nom, email FROM users WHERE role = 'enseignant' ORDER BY nom")
    rows = curseur.fetchall()
    professeurs = [{'id': r[0], 'nom': r[1], 'email': r[2]} for r in rows]

    if request.method == 'POST':
        contenu = request.form.get('contenu', '').strip()
        enseignant_id = request.form.get('enseignant_id')
        form_contenu = contenu
        form_enseignant = enseignant_id

        if not contenu or not enseignant_id:
            erreur = "Veuillez remplir tous les champs."
        else:
            curseur.execute('''
                INSERT INTO messages (etudiant_id, enseignant_id, contenu, date_envoi, statut)
                VALUES (?, ?, ?, ?, ?)
            ''', (etudiant_id, enseignant_id, contenu, datetime.now().strftime('%Y-%m-%d %H:%M'), 'pending'))
            connexion.commit()
            success = True
            form_contenu = ''
            form_enseignant = ''

    # Historique des messages envoyés par cet étudiant
    curseur.execute('''
        SELECT messages.contenu, messages.date_envoi, messages.statut, messages.reponse, users.nom
        FROM messages
        JOIN users ON users.id = messages.enseignant_id
        WHERE messages.etudiant_id = ?
        ORDER BY messages.date_envoi DESC
    ''', (etudiant_id,))
    rows_hist = curseur.fetchall()
    connexion.close()

    historique = [
        {
            'contenu':    r[0],
            'date_envoi': r[1],
            'statut':     r[2],
            'reponse':    r[3],
            'prof_nom':   r[4]
        }
        for r in rows_hist
    ]

    return render_template(
        'appeal.html',
        nom=session.get('user_nom'),
        professeurs=professeurs,
        success=success,
        erreur=erreur,
        historique=historique,
        form_contenu=form_contenu,
        form_enseignant=form_enseignant
    )

# ROUTE : Interface Appeals du professeur
# Le prof voit tous les messages reçus des étudiants,
# peut filtrer par classe et envoyer une réponse à un étudiant
# La réponse est stockée dans messages.reponse et le statut passe à 'answered'

@app.route('/appeals-enseignant', methods=['GET', 'POST'])
def appeals_enseignant():
    if session.get('user_role') != 'enseignant':
        return redirect(url_for('login'))

    enseignant_id = session.get('user_id')
    success = False

    connexion = sqlite3.connect('campuslink.db')
    curseur = connexion.cursor()

    # Enregistrer la réponse du prof
    if request.method == 'POST':
        message_id = request.form.get('message_id')
        reponse    = request.form.get('reponse', '').strip()

        if message_id and reponse:
            curseur.execute('''
                UPDATE messages
                SET reponse = ?, statut = 'answered'
                WHERE id = ? AND enseignant_id = ?
            ''', (reponse, message_id, enseignant_id))
            connexion.commit()
            success = True

    # Récupérer tous les messages adressés à ce prof
    curseur.execute('''
        SELECT messages.id, messages.contenu, messages.date_envoi,
               messages.statut, messages.reponse,
               users.nom, users.classe
        FROM messages
        JOIN users ON users.id = messages.etudiant_id
        WHERE messages.enseignant_id = ?
        ORDER BY messages.date_envoi DESC
    ''', (enseignant_id,))
    rows = curseur.fetchall()

    messages_pending  = []
    messages_answered = []

    for r in rows:
        msg = {
            'id':           r[0],
            'contenu':      r[1],
            'date_envoi':   r[2],
            'statut':       r[3],
            'reponse':      r[4],
            'etudiant_nom': r[5],
            'classe':       r[6]
        }
        if r[3] == 'pending':
            messages_pending.append(msg)
        else:
            messages_answered.append(msg)

    # Liste des classes disponibles pour le filtre
    curseur.execute("SELECT DISTINCT classe FROM users WHERE role = 'etudiant' AND classe IS NOT NULL ORDER BY classe")
    classes = [c[0] for c in curseur.fetchall()]

    connexion.close()

    return render_template(
        'appeals_enseignant.html',
        nom=session.get('user_nom'),
        messages_pending=messages_pending,
        messages_answered=messages_answered,
        classes=classes,
        success=success
    )

# FONCTION COMMUNE : Logique de changement de mot de passe
# Utilisée par les deux routes (étudiant et enseignant)
# Vérifie l'ancien MDP, que les deux nouveaux correspondent,
# puis fait UPDATE dans users et retourne (success, erreur)

def changer_mot_de_passe(user_id):
    ancien_mdp    = request.form.get('ancien_mdp', '').strip()
    nouveau_mdp   = request.form.get('nouveau_mdp', '').strip()
    confirmer_mdp = request.form.get('confirmer_mdp', '').strip()

    connexion = sqlite3.connect('campuslink.db')
    curseur = connexion.cursor()

    # Vérifier que l'ancien mot de passe est correct
    curseur.execute(
        "SELECT id FROM users WHERE id = ? AND mot_de_passe = ?",
        (user_id, ancien_mdp)
    )
    valide = curseur.fetchone()

    if not valide:
        connexion.close()
        return False, "L'ancien mot de passe est incorrect."

    if nouveau_mdp != confirmer_mdp:
        connexion.close()
        return False, "Les deux nouveaux mots de passe ne correspondent pas."

    if len(nouveau_mdp) < 4:
        connexion.close()
        return False, "Le nouveau mot de passe doit contenir au moins 4 caractères."

    # UPDATE dans la base de données
    curseur.execute(
        "UPDATE users SET mot_de_passe = ? WHERE id = ?",
        (nouveau_mdp, user_id)
    )
    connexion.commit()
    connexion.close()

    return True, None


# ROUTE : Settings étudiant

@app.route('/settings-etudiant', methods=['GET', 'POST'])
def settings_etudiant():
    if session.get('user_role') != 'etudiant':
        return redirect(url_for('login'))

    success, erreur = False, None

    if request.method == 'POST':
        success, erreur = changer_mot_de_passe(session.get('user_id'))

    return render_template(
        'settings.html',
        nom=session.get('user_nom'),
        role='etudiant',
        success=success,
        erreur=erreur
    )

# ROUTE : Settings enseignant

@app.route('/settings-enseignant', methods=['GET', 'POST'])
def settings_enseignant():
    if session.get('user_role') != 'enseignant':
        return redirect(url_for('login'))

    success, erreur = False, None

    if request.method == 'POST':
        success, erreur = changer_mot_de_passe(session.get('user_id'))

    return render_template(
        'settings.html',
        nom=session.get('user_nom'),
        role='enseignant',
        success=success,
        erreur=erreur
    )

if __name__ == '__main__':
    app.run(debug=True)
