from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import SubmitField, BooleanField, StringField, PasswordField, IntegerField, SelectField
from wtforms_sqlalchemy.fields import QuerySelectField

from wtforms.validators import DataRequired, ValidationError, EqualTo, Email

from servisas import models

MESSAGE_BAD_EMAIL = 'Neteisingas el.pašto adresas.'

class RegistracijosForma(FlaskForm):
    vardas = StringField('Vardas', [DataRequired()])
    el_pastas = StringField('El.paštas', [DataRequired(), Email(MESSAGE_BAD_EMAIL)])
    slaptazodis = PasswordField('Slaptažodis', [DataRequired()])
    patvirtinimas = PasswordField('Pakartokite slaptažodį', [EqualTo('slaptazodis', "Slaptažodis turi sutapti.")])
    submit = SubmitField('Prisiregistruoti')

    def tikrinti_varda(self, vardas):
        vartotojas = models.Vartotojas.query.filter_by(vardas=vardas.data).first()
        if vartotojas:
            raise ValidationError('Toks vartotojas jau egzistuoja. Pasirinkite kitą vardą.')

    def tikrinti_pasta(self, el_pastas):
        vartotojas = models.Vartotojas.query.filter_by(el_pastas=el_pastas.data).first()
        if vartotojas:
            raise ValidationError('Vartotojas su jūsų nurodytu el.pašto adresu jau egzistuoja.')


class PrisijungimoForma(FlaskForm):
    el_pastas = StringField('El. paštas', [DataRequired(), Email(MESSAGE_BAD_EMAIL)])
    slaptazodis = PasswordField('Slaptažodis', [DataRequired()])
    prisiminti = BooleanField('Prisiminti mane')
    submit = SubmitField('Prisijungti')


class ProfilioForma(FlaskForm):
    vardas = StringField('Vardas', [DataRequired()])
    el_pastas = StringField('El.paštas', [DataRequired(), Email(MESSAGE_BAD_EMAIL)])
    nuotrauka = FileField('Atnaujinti profilio nuotrauką', validators=[FileAllowed(['jpg', 'png'])])
    is_admin = BooleanField('Administratorius')
    submit = SubmitField('Atnaujinti')

    def tikrinti_varda(self, vardas):
        vartotojas = models.Vartotojas.query.filter_by(vardas=vardas.data).first()
        if vartotojas:
            raise ValidationError('Toks vartotojas jau egzistuoja. Pasirinkite kitą vardą.')

    def tikrinti_pasta(self, el_pastas):
        vartotojas = models.Vartotojas.query.filter_by(el_pastas=el_pastas.data).first()
        if vartotojas:
            raise ValidationError('Vartotojas su jūsų nurodytu el.pašto adresu jau egzistuoja.')

class IvedimoForma(FlaskForm):
    gamintojas = StringField('Gamintojas', [DataRequired()])
    modelis = StringField('Modelis', [DataRequired()])
    metai = StringField('Pagaminmo metai', [DataRequired()])
    variklis = StringField('Variklis', [DataRequired()])
    valst_nr = StringField('Valstybinis nr.', [DataRequired()])
    reg_nr = StringField('Registracijos nr., VIN kodas', [DataRequired()])
    submit = SubmitField('Registruoti')


# def car_query():
#     return models.Masina.query.all()

class IrasasForma(FlaskForm):
    problema = StringField('Gedimo aprasymas', [DataRequired()])
    suma = IntegerField('Kaina', default=0)
    gamintojas = StringField('Gamintojas', [DataRequired()])
    # masina = QuerySelectField('Pasirinkite automobili',
    #     query_factory=car_query, 
    #     allow_blank=False, 
    #     get_label=lambda obj: str(f'{obj.gamintojas} {obj.modelis}, {obj.reg_nr}'), )
    submit = SubmitField('Issaugoti')

class TaisomasGedimasForm(FlaskForm):
    problema = StringField('Gedimo aprasymas', [DataRequired()])
    statusas = StringField('Remonto statusas', [DataRequired()])
    # statusas = SelectField('Statusas', choices=['naujas','priimta', 'taisoma', 'sutaisyta', 'grazinama', 'atiduota'], default="naujas")
    suma = IntegerField('Kaina', default=0)
    submit = SubmitField('Issaugoti')