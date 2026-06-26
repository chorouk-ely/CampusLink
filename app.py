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

if __name__ == '__main__':
    app.run(debug=True)
