from datetime import datetime
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin, current_user
from sqlalchemy import DateTime
from servisas import db


class Vartotojas(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    vardas = db.Column('Vartotojo vardas', db.String(100), unique=True, nullable=False)
    el_pastas = db.Column('El.paštas', db.String(100), unique=True, nullable=False)
    slaptazodis = db.Column('Slaptažodis', db.String(100), nullable=False)
    nuotrauka = db.Column('Nuotrauka', db.String(100), nullable=True, default='default.jpg')
    is_admin = db.Column('Administratorius', db.Boolean(), default=False)
    is_darbuotojas = db.Column('Darbuotojas', db.Boolean(), default=False)

    def __repr__(self) -> str:
        return self.vardas


class Masina(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gamintojas = db.Column(db.String(50), nullable=False)
    modelis = db.Column(db.String(50), nullable=True)
    metai = db.Column(db.String(8), nullable=True)
    variklis = db.Column(db.String(50), nullable=True)
    valst_nr = db.Column(db.String(8), nullable=True)
    reg_nr = db.Column(db.String(30), nullable=False)
    vartotojas_id = db.Column(db.Integer, db.ForeignKey('vartotojas.id'))
    vartotojas = db.relationship("Vartotojas", lazy=True)

    def __repr__(self) -> str:
        return f'{self.gamintojas} {self.modelis} {self.reg_nr} {self.metai}'

    def __init__(self, gamintojas, modelis, reg_nr, vartotojas_id):
        self.gamintojas = gamintojas
        self.modelis = modelis
        self.reg_nr = reg_nr
        self.vartotojas_id = vartotojas_id
        


class Irasas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sukurta = db.Column('Sukurta', DateTime, default=datetime.utcnow())
    statusas = db.Column(db.String(50), default='naujas', nullable=False)
    problema = db.Column(db.String(200), nullable=False)
    suma = db.Column('Suma', db.Numeric(10,2), default=0)
    masina_id = db.Column(db.Integer, db.ForeignKey('masina.id'))
    masina = db.relationship("Masina", lazy=True)

    def __repr__(self) -> str:
        return f'{self.problema} @ {self.suma} {self.sukurta}'


class LimitedAdmin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin


