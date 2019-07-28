from os import listdir
from os.path import isfile, join

from flask import Blueprint, render_template, flash, redirect, url_for, request, abort
from flask_login import login_user, current_user, logout_user, login_required

from app import bcrypt, db, app
from app.forms.SliderForm import SliderForm

from app.models.MailModel import Mail

from app.forms.LoginForm import LoginForm
from app.forms.ConcertForm import ConcertForm
from app.forms.TextsForms import MusicTextForm, AboutTextForm
from app.forms.RiderForm import RiderForm
from app.models.functions import create_safe_filename, save_file, reformat_yt_link

from app.resources.ConcertsResource import Concerts, get_all_concerts, get_concert_by_id
from app.resources.SlidesResource import get_all_slides
from app.resources.TextsResource import get_text_by_page
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
    form = SliderForm()
    current_slides = get_all_slides()

    if request.method == 'GET':
        for field, slide in zip(form.slides, current_slides):
            field.slide_type.data = slide.type
            if slide.type == 'v':
                field.youtube.data = slide.content
            elif slide.type == 'i':
                field.picture.data = slide.content

    elif request.method == 'POST' and form.validate_on_submit():
        try:
            for field, slide in zip(form.slides, current_slides):
                if field.slide_type.data == 'v':
                    if not field.youtube.data:
                        flash("W slajdzie " + str(slide.order) + " wybrano typ 'Filmik' i nie dodano linku. Zachowano poprzedni slajd.", "info")
                    else:
                        slide.type = field.slide_type.data
                        slide.content = reformat_yt_link(field.youtube.data)

                elif field.slide_type.data == 'i':
                    photo_key = 'slides-' + str(slide.order-1) + '-picture'
                    if request.files.get(photo_key, False):
                        photo = request.files.get(photo_key, False)
                        photo_filename = create_safe_filename(photo, random=True, date=False)
                        save_file(photo, 'images/slides', photo_filename)

                        slide.type = field.slide_type.data
                        slide.content = photo_filename
                    else:
                        flash("W slajdzie " + str(slide.order) + " nie dodano nowego pliku mimo wyboru typu 'Obraz'. Zachowano poprzedni "
                              "slajd.", "info")
            db.session.commit()

        except Exception as e:
            print(e)
            flash('Przepraszamy! Wystąpił nieoczekiwany błąd.', 'error')
            mail = Mail('Błąd - CZZK', 'Błąd przy edycji slidera: ' + str(e), None,
                        recipients='psambek@gmail.com', raw_mail=True)
            # mail.send()

            return redirect(url_for('CMS.slider'))

        flash('Zaktualizowano rider.', 'success')

        return redirect(url_for('CMS.slider'))

    elif request.method == 'POST' and not form.validate_on_submit():
        flash('Formularz nie został wypełniony poprawnie.', 'warning')

    return render_template('cms/slider.html',
                           form=form,
                           )


@CMS.route('/admin/teksty/<string:text>', methods=['POST', 'GET'])
@login_required
def texts(text):
    form = None
    if text == 'muzyka':
        form = MusicTextForm()
    elif text == 'czzk':
        form = AboutTextForm()
    else:
        abort(404)

    content = get_text_by_page(text)

    if request.method == 'GET':
        for field, chapter in zip(form.chapters, content):
            field.title.data = chapter.title
            field.content.data = chapter.content

    elif request.method == 'POST' and form.validate_on_submit():
        for field, chapter in zip(form.chapters, content):
            chapter.title = field.title.data
            chapter.content = field.content.data

        try:
            db.session.commit()
        except Exception as e:
            flash('Przepraszamy! Wystąpił nieoczekiwany błąd.', 'error')
            mail = Mail('Błąd - CZZK', 'Błąd przy edycji tekstu ' + text + ': ' + str(e), None,
                        recipients='psambek@gmail.com', raw_mail=True)
            mail.send()

            return render_template('cms/text.html',
                                   name=text,
                                   text=content,
                                   form=form,
                                   noJquery=True
                                   )

        flash('Zaktualizowano tekst.', 'success')

        return redirect(url_for('CMS.texts', text=text))

    elif request.method == 'POST' and not form.validate_on_submit():
        flash('Formularz nie został wypełniony poprawnie.', 'warning')

    return render_template('cms/text.html',
                           name=text,
                           text=content,
                           form=form,
                           noJquery=True
                           )


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

    flash('Koncert został usunięty.', 'success')
    return redirect(url_for('CMS.all_concerts'))


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
    form = RiderForm()

    rider_dir = app.config['UPLOAD_FOLDER'] + '/files/rider'
    rider_files = [f for f in listdir(rider_dir) if isfile(join(rider_dir, f))]
    rider_files.sort(reverse=True)

    if rider_files:
        current_rider = rider_files[0]
    else:
        current_rider = None

    if request.method == 'POST' and form.validate_on_submit():
        try:
            new_rider = request.files['rider']
            new_rider_filename = create_safe_filename(new_rider, random=False, date=True)
            save_file(new_rider, 'files/rider', new_rider_filename )

        except Exception as e:
            print(e)
            flash('Przepraszamy! Wystąpił nieoczekiwany błąd.', 'error')
            mail = Mail('Błąd - CZZK', 'Błąd przy dodawaniu ridera: ' + str(e), None,
                        recipients='psambek@gmail.com', raw_mail=True)
            mail.send()

            return render_template('cms/rider.html',
                                   form=form,
                                   current_rider=current_rider
                                   )

        flash('Zaktualizowano rider.', 'success')

        return redirect(url_for('CMS.rider'))

    elif request.method == 'POST' and not form.validate_on_submit():
        flash('Formularz nie został wypełniony poprawnie.', 'warning')

    return render_template('cms/rider.html',
                           form=form,
                           current_rider=current_rider
                           )
