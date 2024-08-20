from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from app.translate import translator
from app.models import User
from app.models import Scan
from app.models import Result
from app.models import Programmation
from app.models import Commentaire
from zapv2 import ZAPv2
from datetime import datetime
import time
from app import db

main = Blueprint('main', __name__)

login_manager = LoginManager()
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@main.route('/admin')
def admin():
    return render_template('admin.html')

@main.route('/s')
def s():
    return render_template('admin.html')

@main.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@main.route('/rapport')
def rapport():
    return render_template('rapport.html')

@main.route('/scan_p')
def scan_p():
    return render_template('scan_programmer.html')

@main.route('/test')
def test():
    return render_template('index.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Login unsuccessful. Check your email and/or password', 'danger')
    
    return render_template('login1.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'success')
    return redirect(url_for('main.login'))

@main.route('/')
def index():
    return render_template('index1.html')


@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
        new_user = User(username=username, email=email, password=hashed_password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Account created successfully', 'success')
        return redirect(url_for('main.login'))
    
    return render_template('register1.html')

@main.route('/scan', methods=['POST'])
def scan():
    url = request.form['url']
    
    # Initialisation de ZAP
    zap = ZAPv2(proxies={'http': 'http://localhost:8086', 'https': 'http://localhost:8086'})
    zap.urlopen(url)

    # Démarrer les scans
    scan_id = zap.spider.scan(url)
    while int(zap.spider.status(scan_id)) < 100:
        print('Scan de l\'araignée en cours...')
        time.sleep(1)

    print('Scan de l\'araignée terminé')
    ascan_id = zap.ascan.scan(url)
    while int(zap.ascan.status(ascan_id)) < 100:
        print('Scan actif en cours...')
        time.sleep(1)

    print('Scan actif terminé')

    # Récupération des alertes
    alerts = zap.core.alerts()
    alert_data = []

    # Création du scan dans la base de données
    scan_entry = Scan(
        url=url,
        description="Scan réalisé via ZAP",
        scan_date=datetime.utcnow(),
        status='Terminé',
        type_scan='Manuel',
        criticite=1
    )
    db.session.add(scan_entry)
    db.session.commit()

    print('XXXXXX ===> ', alerts)
    # Enregistrement des résultats dans la base de données
    for alert in alerts:
        result_entry = Result(
            scan_id=scan_entry.id,
            alert=alert.get('alert', 'Non spécifié'),
            risk=alert.get('risk', 'Non spécifié'),
            description=alert.get('desc', 'Non spécifié'),
            url=alert.get('url', 'Non spécifié'),
            solution=alert.get('solution', 'Non spécifié')
        )
    alert_data.append(result_entry)

    print('RRRRRRRRRRRRRRRR ===> ', alert_data)
    db.session.add_all(alert_data)
    db.session.commit()

    # Retour des résultats sous forme JSON
    return jsonify({'url': url, 'alerts': alert_data})