from . import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    scans = db.relationship('Scan', backref='user', lazy=True)
    programmations = db.relationship('Programmation', backref='user', lazy=True)

class Programmation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_programme = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    scans = db.relationship('Scan', backref='programmation', lazy=True)


class Scan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    programmation_id = db.Column(db.Integer, db.ForeignKey('programmation.id'), nullable=True)
    url = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    scan_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), nullable=False)
    type_scan = db.Column(db.String(255), nullable=False)
    commentaire = db.Column(db.String(255), nullable=True)
    criticite = db.Column(db.Integer, nullable=False)
    # Relation un-à-plusieurs avec Result
    results = db.relationship('Result', backref='scan', lazy=True)

    def __repr__(self):
        return f'<Scan {self.id}>'

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    scan_id = db.Column(db.Integer, db.ForeignKey('scan.id'), nullable=False)
    alert = db.Column(db.String(255), nullable=False)
    risk = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    solution = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f'<Result {self.id}>'

class Commentaire(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    scan_id = db.Column(db.Integer, db.ForeignKey('scan.id'), nullable=True)
    commentaire = db.Column(db.String(255), nullable=False)
    date_commentaire = db.Column(db.String(10), nullable=True)
