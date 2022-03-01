from datetime import datetime
from flask import redirect, request, render_template, flash, url_for
from flask_bcrypt import Bcrypt
from flask_login import logout_user, login_user, login_required, current_user

from servisas.models import Vartotojas, LimitedAdmin, Masina, Irasas
from servisas.pictures import save_picture
from servisas import forms
from servisas import app, db, admin


admin.add_view(LimitedAdmin(Vartotojas, db.session))
admin.add_view(LimitedAdmin(Irasas, db.session))
admin.add_view(LimitedAdmin(Masina, db.session))
bcrypt = Bcrypt(app)


@app.route('/')
def home():
    flash('Sveiki atvykę, prisijungėte prie sistemos', 'info')
    return render_template('base.html', current_user=current_user)

@app.route('/admin')
@login_required
def admin():
    return redirect(url_for(admin))


@app.route('/registracija', methods=['GET', 'POST'])
def registracija():
    if current_user.is_authenticated:
        flash('Atsijunkite, kad priregistruoti naują vartotoją.')
        return redirect(url_for('home'))
    form = forms.RegistracijosForma()
    if form.validate_on_submit():
        koduotas_slaptazodis = bcrypt.generate_password_hash(form.slaptazodis.data).decode('utf-8')
        is_first_user = not Vartotojas.query.first()
        naujas_vartotojas = Vartotojas(
            vardas = form.vardas.data,
            el_pastas = form.el_pastas.data,
            slaptazodis = koduotas_slaptazodis,
            is_admin = is_first_user,
            is_darbuotojas = is_first_user
        )
        db.session.add(naujas_vartotojas)
        db.session.commit()
        flash('Sėkmingai prisiregistravote! Galite prisijungti.', 'success')
        return redirect(url_for('home'))
    return render_template('registracija.html', form=form, current_user=current_user)


@app.route('/prisijungimas', methods=['GET', 'POST'])
def prisijungimas():
    next_page = request.args.get('next')
    if current_user.is_authenticated:
        flash('Vartotojas jau prisijungęs. Atsijunkite ir bandykite iš naujo.')
        return redirect(next_page) if next_page else redirect(url_for('home'))
    form = forms.PrisijungimoForma()
    if form.validate_on_submit():
        user = Vartotojas.query.filter_by(el_pastas=form.el_pastas.data).first()
        if user and bcrypt.check_password_hash(user.slaptazodis, form.slaptazodis.data):
            login_user(user, remember=form.prisiminti.data)
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Prisijungti nepavyko, neteisingas el.paštas arba slaptažodis.', 'danger')
    return render_template('prisijungimas.html', form=form, current_user=current_user)


@app.route('/atsijungimas')
def atsijungimas():
    logout_user()
    next_page = request.args.get('next')
    return redirect(next_page) if next_page else redirect(url_for('home'))


@app.route('/profilis', methods=['GET', 'POST', 'FILE'])
@login_required
def profilis():
    form = forms.ProfilioForma()
    if form.validate_on_submit():
        print('form data', form.nuotrauka.data)
        if form.nuotrauka.data:
            current_user.nuotrauka = save_picture(form.nuotrauka.data)
            print('CU', current_user.nuotrauka)
        current_user.vardas = form.vardas.data
        current_user.el_pastas = form.el_pastas.data
        current_user.is_admin = form.is_admin.data
        db.session.commit()
        flash('Profilis atnaujintas!', 'success')
        return redirect(url_for('profilis'))
    elif request.method == "GET":
        form.vardas.data = current_user.vardas
        form.el_pastas.data = current_user.el_pastas
        form.is_admin.data = current_user.is_admin
    nuotrauka = url_for('static', filename='profilio_nuotraukos/'+(current_user.nuotrauka or 'default.jpg'))
    return render_template('profilis.html', current_user=current_user, form=form, nuotrauka=nuotrauka)


@app.route('/ivedimas', methods=['GET', 'POST'])
@login_required
def ivedimas():
    form = forms.IvedimoForma()
    if form.validate_on_submit():
        nauja_masina = Masina(
            gamintojas = form.gamintojas.data,
            modelis = form.modelis.data,
            metai = form.metai.data,
            variklis = form.variklis.data,
            valst_nr = form.valst_nr.data,
            reg_nr = form.reg_nr.data,
            vartotojas_id = current_user.id
        )
        db.session.add(nauja_masina)
        db.session.commit()
        flash('Registracija atlikta sėkmingai.', 'success')
        return redirect(url_for('home'))
    return render_template('ivedimas.html', form=form, current_user=current_user)

@app.route('/irasai')
@login_required
def records():
    page = request.args.get('page', 1, type=int)
    visi_masinos = Masina.query.filter_by(vartotojas_id=current_user.id).paginate(page=page, per_page=5)
    return render_template("irasai.html", visi_masinos=visi_masinos)

@app.route('/irasas', methods=['GET', 'POST'])
@login_required
def irasas():
    form = forms.IrasasForma()
    if form.validate_on_submit():
        naujas_irasas = Irasas(
            problema = form.problema.data,
            masina_id = form.masina.data.id,
            statusas = form.statusas.data,
            suma = form.suma.data
        )
        db.session.add(naujas_irasas)
        db.session.commit()
        flash('Duomenys atnaujinti', 'success')
        return redirect(url_for('home'))
    # naujas_irasas = Irasas.query.all()
    return render_template("irasas.html", form=form, datetime=datetime)



@app.errorhandler(404)
def klaida_404(klaida):
    return render_template("klaida.html", klaida=404), 404

@app.errorhandler(404)
def klaida_403(klaida):
    return render_template("klaida.html", klaida=403), 403

@app.errorhandler(404)
def klaida_500(klaida):
    return render_template("klaida.html", klaida=500), 500