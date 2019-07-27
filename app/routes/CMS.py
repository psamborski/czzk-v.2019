from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_user, current_user, logout_user, login_required

from app import bcrypt, db

from app.forms.LoginForm import LoginForm
from app.forms.ConcertForm import ConcertForm
from app.models.MailModel import Mail

from app.resources.ConcertsResource import Concerts, get_all_concerts, get_concert_by_id
from app.resources.UsersResource import get_user

CMS = Blueprint('CMS', __name__)


@CMS.route('/admin')
@login_required
def index():
    return render_template('cms/index.html')


@CMS.route('/admin/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('CMS.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = get_user(username=form.login.data)
        if user and bcrypt.check_password_hash(user.passwordHash, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('CMS.index'))
        else:
            flash('Wprowadzono niepoprawny login lub hasło.', 'error')

    return render_template('cms/login.html', form=form)


@CMS.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('CMS.login'))


@CMS.route('/admin/slider', methods=['POST', 'GET'])
@login_required
def slider():
    return render_template('cms/slider.html', form=None, message='Pomyślnie zedytowano slider.')


@CMS.route('/admin/teksty/<string:text>')
@login_required
def texts(text):
    return render_template('cms/texts.html')


@CMS.route('/admin/albumy')
@login_required
def albums():
    return render_template('cms/albums.html')


@CMS.route('/admin/koncerty')
@login_required
def all_concerts():
    page = request.args.get('strona', 1, type=int)

    concerts = get_all_concerts(page)
    return render_template('cms/concerts.html', concerts=concerts)


@CMS.route('/admin/koncerty/dodaj', methods=['POST', 'GET'])
@login_required
def add_concert():
    form = ConcertForm()
    if request.method == 'POST' and form.validate_on_submit():
        concert = Concerts(
            name=form.name.data,
            date=form.date.data,
            place=form.place.data
        )

        db.session.add(concert)
        try:
            db.session.commit()
        except Exception as e:
            flash('Przepraszamy! Wystąpił nieoczekiwany błąd.', 'error')
            mail = Mail('Błąd - CZZK', 'Błąd przy tworzeniu koncertu: ' + str(e), None,
                        recipients='psambek@gmail.com', raw_mail=True)
            mail.send()

            return render_template('cms/concert-form.html', form=form, action='add')

        flash('Utworzono nowy koncert.', 'success')

        return redirect(url_for('CMS.all_concerts'))

    elif request.method == 'POST' and not form.validate_on_submit():
        flash('Formularz nie został wypełniony poprawnie.', 'warning')

        return render_template('cms/concert-form.html', form=form, action='add')

    return render_template('cms/concert-form.html', form=form, action='add')


@CMS.route('/admin/koncerty/<int:concert_id>/edytuj', methods=['POST', 'GET'])
@login_required
def update_concert(concert_id):
    page = request.args.get('strona', 1, type=int)

    concert = get_concert_by_id(concert_id)

    form = ConcertForm()

    if request.method == 'POST' and form.validate_on_submit():
        concert.name = form.name.data
        concert.date = form.date.data
        concert.place = form.place.data

        try:
            db.session.commit()
        except Exception as e:
            flash('Przepraszamy! Wystąpił nieoczekiwany błąd.', 'error')
            mail = Mail('Błąd - CZZK', 'Błąd przy edycji koncertu: ' + str(e), None,
                        recipients='psambek@gmail.com', raw_mail=True)
            mail.send()

            return render_template('cms/concert-form.html', form=form, action='edit')

        flash('Zaktualizowano koncert.', 'success')

        return redirect(url_for('CMS.all_concerts', strona=page))

    elif request.method == 'POST' and not form.validate_on_submit():
        flash('Formularz nie został wypełniony poprawnie.', 'warning')

        return render_template('cms/concert-form.html', form=form, action='edit')

    elif request.method == 'GET':
        form.name.data = concert.name
        form.date.data = concert.date
        form.place.data = concert.place

        return render_template('cms/concert-form.html', form=form, action='edit')

    return render_template('cms/concert-form.html', form=form, action='edit')


@CMS.route("/admin/koncerty/<int:concert_id>/usun", methods=['POST'])
@login_required
def delete_concert(concert_id):
    concert = get_concert_by_id(concert_id)

    try:
        db.session.delete(concert)
        db.session.commit()
    except Exception as e:
        flash('Przepraszamy! Wystąpił nieoczekiwany błąd.', 'error')
        mail = Mail('Błąd - OSK Kurs', 'Błąd przy usuwaniu kursu: ' + str(e), None,
                    recipients='psambek@gmail.com', raw_mail=True)
        mail.send()

        return redirect(url_for('CMS.all_concerts'))

    # deleting multiple rows can be quicker with engine
    # https://stackoverflow.com/questions/39773560/sqlalchemy-how-do-you-delete-multiple-rows-without-querying
    # https: // docs.sqlalchemy.org / en / latest / core / connections.html

    flash('Koncert został usunięty.', 'success')
    return redirect(url_for('CMS.all_concerts'))


@CMS.route('/admin/koncerty/<int:id>')
@login_required
def specific_concert(id):
    return render_template('cms/concerts.html')


@CMS.route('/admin/audio')
@login_required
def audio():
    return render_template('cms/audio.html')


@CMS.route('/admin/gadzety')
@login_required
def merch():
    return render_template('cms/merch.html')


@CMS.route('/admin/galeria')
@login_required
def gallery():
    return render_template('cms/gallery.html')


@CMS.route('/admin/rider', methods=['POST', 'GET'])
@login_required
def rider():
    return render_template('cms/settings.html', form=None, message='Pomyślnie zmieniono dane.')


@CMS.route('/admin/kontakt', methods=['POST', 'GET'])
@login_required
def contact():
    # TODO ADD TABLE
    return render_template('cms/settings.html', form=None, message='Pomyślnie zmieniono dane.')
