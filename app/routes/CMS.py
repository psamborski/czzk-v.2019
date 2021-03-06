from os import listdir
from os.path import isfile, join

from flask import Blueprint, render_template, flash, redirect, url_for, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename

from app import bcrypt, db, app

from app.forms.AlbumForm import AlbumForm
from app.forms.ConcertForm import ConcertForm
from app.forms.ContactDataForm import ContactDataForm
from app.forms.GalleryForm import GalleryForm
from app.forms.LoginForm import LoginForm
from app.forms.MerchItemForm import MerchItemForm
from app.forms.RiderForm import RiderForm
from app.forms.SizeTableForm import SizeTableForm
from app.forms.SliderForm import SliderForm
from app.forms.TextsForms import MusicTextForm, AboutTextForm

from app.models.GalleryModel import Gallery
from app.models.MailModel import Mail
from app.models.functions import create_safe_filename, save_file, reformat_yt_link, remove_file, move_file

from app.resources.AlbumsResource import Albums, get_album_by_id, get_all_albums_paginated
from app.resources.ConcertsResource import Concerts, get_all_concerts, get_concert_by_id
from app.resources.ContactDataResource import get_contact_item_by_key
from app.resources.GalleriesResource import get_all_galleries, Galleries, get_gallery_by_secure_title, get_gallery_by_id
from app.resources.MerchResource import get_all_merch_paginated, get_item_from_merch, Merch, get_item_by_id
from app.resources.SizeTablesResource import get_table_by_keyword
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
        try:
            user = get_user(username=form.login.data)
            if user and bcrypt.check_password_hash(user.passwordHash, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('CMS.index'))
            else:
                flash('Wprowadzono niepoprawny login lub hasło.', 'error')
        except Exception as e:
            print(e)
            flash('Przepraszamy! Wystąpił nieoczekiwany błąd.', 'error')
            mail = Mail('Błąd - CZZK', 'Błąd przy logowaniu: ' + str(e), None,
                        recipients='psambek@gmail.com', raw_mail=True)
            mail.send()

            return redirect(url_for('CMS.login'))

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
            field.display.data = slide.display
            if slide.type == 'v':
                field.youtube.data = slide.content
            elif slide.type == 'i':
                field.picture.data = slide.content

    elif request.method == 'POST' and form.validate_on_submit():
        try:
            for field, slide in zip(form.slides, current_slides):
                if field.slide_type.data == 'v' and field.display.data:
                    if not field.youtube.data:
                        flash("W slajdzie " + str(slide.order) + " wybrano typ 'Filmik' i nie dodano linku. Zachowano "
                                                                 "poprzedni slajd.", "info")
                    else:
                        slide.type = field.slide_type.data
                        slide.content = reformat_yt_link(field.youtube.data)

                elif field.slide_type.data == 'i' and field.display.data:
                    photo_key = 'slides-' + str(slide.order-1) + '-picture'
                    if request.files.get(photo_key, False):
                        photo = request.files.get(photo_key, False)
                        photo_filename = create_safe_filename(photo, random=True, date=False)
                        save_file(photo, 'images/slides', photo_filename)

                        slide.type = field.slide_type.data
                        slide.content = photo_filename
                    else:
                        flash("W slajdzie " + str(slide.order) + " nie dodano nowego pliku mimo wyboru typu 'Obraz'. "
                                                                 "Zachowano poprzedni "
                              "slajd.", "info")

                slide.display = field.display.data

            db.session.commit()

        except Exception as e:
            print(e)
            flash('Przepraszamy! Wystąpił nieoczekiwany błąd.', 'error')
            mail = Mail('Błąd - CZZK', 'Błąd przy edycji slidera: ' + str(e), None,
                        recipients='psambek@gmail.com', raw_mail=True)
            mail.send()

            return redirect(url_for('CMS.slider'))

        flash('Zaktualizowano slider.', 'success')

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
def all_albums():
    page = request.args.get('strona', 1, type=int)

    albums = get_all_albums_paginated(page)
    return render_template('cms/albums.html', albums=albums)


@CMS.route('/admin/albumy/dodaj', methods=['POST', 'GET'])
@login_required
def add_album():
    form = AlbumForm()
    if request.method == 'POST' and form.validate_on_submit():

        new_cover = request.files.get('cover', None)
        new_cover_filename = ''

        if new_cover:
            new_cover_filename = create_safe_filename(new_cover, random=True, date=False)
            save_file(new_cover, 'images/music', new_cover_filename)
        else:
            flash('Dodano album, ale nie dodano okładki.', 'warning')

        album = Albums(
            title=form.title.data,
            year=form.year.data,
            description=form.description.data,
            cover_file='music/' + new_cover_filename if new_cover else 'Brak pliku'
        )

        db.session.add(album)

        try:
            db.session.commit()
        except Exception as e:
            flash('Przepraszamy! Wystąpił nieoczekiwany błąd.', 'error')
            mail = Mail('Błąd - CZZK', 'Błąd przy tworzeniu albumu: ' + str(e), None,
                        recipients='psambek@gmail.com', raw_mail=True)
            mail.send()

            return render_template('cms/album-form.html', form=form, action='add', noJquery=True)

        flash('Utworzono nowy album.', 'success')

        return redirect(url_for('CMS.all_albums'))

    elif request.method == 'POST' and not form.validate_on_submit():
        flash('Formularz nie został wypełniony poprawnie.', 'warning')

        return render_template('cms/album-form.html', form=form, action='add', noJquery=True)

    return render_template('cms/album-form.html', form=form, action='add', noJquery=True)


@CMS.route('/admin/albumy/<int:album_id>/edytuj', methods=['POST', 'GET'])
@login_required
def update_album(album_id):
    page = request.args.get('strona', 1, type=int)

    album = get_album_by_id(album_id)

    form = AlbumForm()

    if request.method == 'POST' and form.validate_on_submit():
        album.title = form.title.data
        album.year = form.year.data
        album.description = form.description.data

        try:
            new_cover = request.files.get('cover', None)
            if new_cover:
                new_cover_filename = create_safe_filename(new_cover, random=True, date=False)
                save_file(new_cover, 'images/music', new_cover_filename)
                album.cover_file = 'music/' + new_cover_filename

            db.session.commit()
        except Exception as e:
            flash('Przepraszamy! Wystąpił nieoczekiwany błąd.', 'error')
            mail = Mail('Błąd - CZZK', 'Błąd przy edycji albumu: ' + str(e), None,
                        recipients='psambek@gmail.com', raw_mail=True)
            mail.send()

            return render_template('cms/album-form.html', form=form, action='edit', noJquery=True)

        flash('Zaktualizowano album.', 'success')

        return redirect(url_for('CMS.all_albums', strona=page))

    elif request.method == 'POST' and not form.validate_on_submit():
        flash('Formularz nie został wypełniony poprawnie.', 'warning')

        return render_template('cms/album-form.html', form=form, action='edit', noJquery=True)

    elif request.method == 'GET':
        form.title.data = album.title
        form.year.data = album.year
        form.description.data = album.description
        form.cover.data = album.cover_file

    return render_template('cms/album-form.html', form=form, action='edit', noJquery=True)


@CMS.route("/admin/albumy/<int:album_id>/usun", methods=['POST'])
@login_required
def delete_album(album_id):
    album = get_album_by_id(album_id)

    try:
        db.session.delete(album)
        db.session.commit()
    except Exception as e:
        flash('Przepraszamy! Wystąpił nieoczekiwany błąd.', 'error')
        mail = Mail('Błąd - OSK Kurs', 'Błąd przy usuwaniu kursu: ' + str(e), None,
                    recipients='psambek@gmail.com', raw_mail=True)
        mail.send()

        return redirect(url_for('CMS.all_albums'))

    flash('Koncert został usunięty.', 'success')
    return redirect(url_for('CMS.all_albums'))


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
            place=form.place.data,
            time=form.time.data
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
        print(concert.time)
        concert.name = form.name.data
        concert.date = form.date.data
        concert.place = form.place.data
        concert.time = form.time.data

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
        form.time.data = concert.time

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
def all_merch():
    page = request.args.get('strona', 1, type=int)

    merch = get_all_merch_paginated(page)
    return render_template('cms/merch.html', merch=merch)


@CMS.route('/admin/gadzety/dodaj', methods=['POST', 'GET'])
@login_required
def add_merch_item():
    form = MerchItemForm()

    if request.method == 'POST' and form.validate_on_submit():
        new_photo = request.files.get('photo', None)
        new_gif = request.files.get('animation', None)

        new_gif_filename, new_photo_filename = '', ''

        if new_photo:
            new_photo_filename = create_safe_filename(new_photo, random=True, date=False)
            save_file(new_photo, 'images/merch/static', new_photo_filename)
        else:
            flash("Dodano gadżet, ale nie wybrano żadnego zdjęcia.", "warning")

        if new_gif:
            new_gif_filename = create_safe_filename(new_gif, random=True, date=False)
            save_file(new_gif, 'images/merch/gifs', new_gif_filename)

        merch_item = Merch(
            name=form.name.data,
            short_name=form.short_name.data,
            safe_name=secure_filename(form.short_name.data),
            description=form.description.data,
            price=form.price.data or None,
            gif='gifs/' + new_gif_filename if new_gif else None,
            jpg='static/' + new_photo_filename if new_photo else None
        )

        try:
            db.session.add(merch_item)
            db.session.commit()
        except Exception as e:
            flash('Przepraszamy! Wystąpił nieoczekiwany błąd.', 'error')
            mail = Mail('Błąd - CZZK', 'Błąd przy edycji gadżetu: ' + str(e), None,
                        recipients='psambek@gmail.com', raw_mail=True)
            mail.send()

            return render_template('cms/merch-item-form.html', form=form, action='add')

        flash('Dodano gadżet.', 'success')

        return redirect(url_for('CMS.all_merch'))

    elif request.method == 'POST' and not form.validate_on_submit():
        flash('Formularz nie został wypełniony poprawnie.', 'warning')

    return render_template('cms/merch-item-form.html', form=form, action='add')


@CMS.route('/admin/gadzety/<string:merch_item_name>/edytuj', methods=['POST', 'GET'])
@login_required
def update_merch_item(merch_item_name):
    page = request.args.get('strona', 1, type=int)

    merch_item = get_item_from_merch(merch_item_name)

    form = MerchItemForm(merch_item)

    if request.method == 'POST' and form.validate_on_submit():
        merch_item.name = form.name.data
        merch_item.short_name = form.short_name.data
        merch_item.safe_name = secure_filename(form.short_name.data)
        merch_item.description = form.description.data
        merch_item.price = form.price.data

        try:
            new_photo = request.files.get('photo', None)
            new_gif = request.files.get('animation', None)
            if new_photo:
                new_photo_filename = create_safe_filename(new_photo, random=True, date=False)
                save_file(new_photo, 'images/merch/static', new_photo_filename)
                merch_item.jpg = 'static/' + new_photo_filename

            if new_gif:
                new_gif_filename = create_safe_filename(new_gif, random=True, date=False)
                save_file(new_gif, 'images/merch/gifs', new_gif_filename)
                merch_item.gif = 'gif/' + new_gif_filename

            db.session.commit()
        except Exception as e:
            flash('Przepraszamy! Wystąpił nieoczekiwany błąd.', 'error')
            mail = Mail('Błąd - CZZK', 'Błąd przy edycji gadżetu: ' + str(e), None,
                        recipients='psambek@gmail.com', raw_mail=True)
            mail.send()

            return render_template('cms/merch-item-form.html', form=form, action='edit')

        flash('Zaktualizowano gadżet.', 'success')

        return redirect(url_for('CMS.all_merch', strona=page))

    elif request.method == 'POST' and not form.validate_on_submit():
        flash('Formularz nie został wypełniony poprawnie.', 'warning')

        return render_template('cms/merch-item-form.html', form=form, action='edit')

    elif request.method == 'GET':
        form.name.data = merch_item.name
        form.short_name.data = merch_item.short_name
        form.description.data = merch_item.description
        form.photo.data = merch_item.jpg
        form.animation.data = merch_item.gif
        form.price.data = merch_item.price

    return render_template('cms/merch-item-form.html', form=form, action='edit')


@CMS.route('/admin/gadzety/<int:merch_item_id>/usun', methods=['POST'])
@login_required
def delete_merch_item(merch_item_id):
    item = get_item_by_id(merch_item_id)

    try:
        db.session.delete(item)
        db.session.commit()
    except Exception as e:
        flash('Przepraszamy! Wystąpił nieoczekiwany błąd.', 'error')
        mail = Mail('Błąd - OSK Kurs', 'Błąd przy usuwaniu gadżetu: ' + str(e), None,
                    recipients='psambek@gmail.com', raw_mail=True)
        mail.send()

        return redirect(url_for('CMS.all_merch'))

    flash('Gadżet został usunięty.', 'success')
    return redirect(url_for('CMS.all_merch'))


@CMS.route('/admin/gadzety/tabele/<string:table_keyword>', methods=['POST', 'GET'])
@login_required
def update_merch_size_table(table_keyword):
    form = SizeTableForm()

    restore = request.args.get('restore', False, type=bool)

    table = get_table_by_keyword(table_keyword)

    if request.method == 'GET':
        if restore:
            form.content.data = table.copy
        else:
            form.content.data = table.content

    elif request.method == 'POST' and form.validate_on_submit():
        table.content = form.content.data

        try:
            db.session.commit()
        except Exception as e:
            flash('Przepraszamy! Wystąpił nieoczekiwany błąd.', 'error')
            mail = Mail('Błąd - CZZK', 'Błąd przy edycji tabeli ' + table_keyword + ': ' + str(e), None,
                        recipients='psambek@gmail.com', raw_mail=True)
            mail.send()

            return render_template('cms/text.html',
                                   name=table_keyword,
                                   form=form,
                                   noJquery=True
                                   )

        flash('Zaktualizowano tabelę.', 'success')

        return redirect(url_for('CMS.all_merch'))

    elif request.method == 'POST' and not form.validate_on_submit():
        flash('Formularz nie został wypełniony poprawnie.', 'warning')

    return render_template('cms/size-table.html',
                           name=table_keyword,
                           form=form,
                           noJquery=True
                           )


@CMS.route('/admin/galerie')
@login_required
def all_galleries():
    page = request.args.get('strona', 1, type=int)

    galleries = get_all_galleries(page)
    return render_template('cms/gallery.html', galleries=galleries)


@CMS.route('/admin/galerie/dodaj', methods=['POST', 'GET'])
@login_required
def add_gallery():
    form = GalleryForm(None)

    if request.method == 'POST' and form.validate_on_submit():
        title = form.title.data
        author = form.author.data
        videos = form.videos.data
        secure_title = secure_filename(title)
        thumbnail = request.files.get('thumbnail', None)

        new_thumbnail_filename = ''
        if thumbnail:
            new_thumbnail_filename = create_safe_filename(thumbnail, random=True, date=False)

        images = request.files.getlist('images') if 'images' in request.files else ()

        gallery = Galleries(
            title=title,
            secure_title=secure_title,
            thumbnail_file=new_thumbnail_filename,
            videos=videos,
            author=author,
        )

        try:
            db.session.add(gallery)
            db.session.commit()
        except Exception as e:
            flash('Przepraszamy! Wystąpił nieoczekiwany błąd.', 'error')
            mail = Mail('Błąd - CZZK', 'Błąd przy dodawaniu galerii (wpis do bazy): ' + str(e), None,
                        recipients='psambek@gmail.com', raw_mail=True)
            mail.send()

            return render_template('cms/gallery-form.html', form=form, action='add')

        try:
            gallery = get_gallery_by_secure_title(secure_title)

            if thumbnail:
                save_file(thumbnail, 'images/galleries/' + str(gallery.id) + '/thumbnail', new_thumbnail_filename)

            for image in images:
                image_filename = create_safe_filename(image, random=True, date=False)
                save_file(image, 'images/galleries/' + str(gallery.id), image_filename)
        except Exception as e:
            flash('Przepraszamy! Wystąpił nieoczekiwany błąd.', 'error')
            mail = Mail('Błąd - CZZK', 'Błąd przy dodawaniu galerii (pobranie galerii z bazy, dodawanie fotek): ' + str(e), None,
                        recipients='psambek@gmail.com', raw_mail=True)
            mail.send()

            return render_template('cms/gallery-form.html', form=form, action='add')

        flash('Dodano galerię.', 'success')

        return redirect(url_for('CMS.all_galleries'))

    elif request.method == 'POST' and not form.validate_on_submit():
        flash('Formularz nie został wypełniony poprawnie.', 'warning')

    return render_template('cms/gallery-form.html', form=form, action='add')


@CMS.route('/admin/galerie/<string:gallery_secure_title>/edytuj', methods=['POST', 'GET'])
@login_required
def update_gallery(gallery_secure_title):
    gallery = get_gallery_by_secure_title(gallery_secure_title)

    gallery_model = Gallery(get_gallery_by_secure_title(gallery_secure_title))
    photos = gallery_model.get_photos()

    page = request.args.get('strona', 1, type=int)

    form = GalleryForm(gallery_secure_title)

    if request.method == 'POST' and form.validate_on_submit():
        try:
            gallery.title = form.title.data
            gallery.author = form.author.data
            gallery.videos = form.videos.data
            gallery.secure_title = secure_filename(form.title.data)
            thumbnail = request.files.get('thumbnail', None)

            if thumbnail:
                remove_file('/images/galleries/' + str(gallery.id) + '/thumbnail/' + gallery.thumbnail_file)
                new_thumbnail_filename = create_safe_filename(thumbnail, random=True, date=False)
                gallery.thumbnail_file = new_thumbnail_filename
                save_file(thumbnail, 'images/galleries/' + str(gallery.id) + '/thumbnail', new_thumbnail_filename)

            db.session.commit()

            images = request.files.getlist('images') if 'images' in request.files else ()

            for image in images:
                if image:
                    image_filename = create_safe_filename(image, random=True, date=False)
                    save_file(image, 'images/galleries/' + str(gallery.id), image_filename)

            db.session.commit()
        except Exception as e:
            flash('Przepraszamy! Wystąpił nieoczekiwany błąd.', 'error')
            mail = Mail('Błąd - CZZK', 'Błąd przy edycji galerii: ' + str(e), None,
                        recipients='psambek@gmail.com', raw_mail=True)
            mail.send()

            return render_template('cms/gallery-form.html',
                                   form=form,
                                   action='edit',
                                   photos=photos,
                                   gallery=gallery_model
                                   )

        flash('Zaktualizowano galerię.', 'success')

        return redirect(url_for('CMS.all_galleries', page=page))

    elif request.method == 'POST' and not form.validate_on_submit():
        flash('Formularz nie został wypełniony poprawnie.', 'warning')

        return render_template('cms/gallery-form.html',
                               form=form,
                               action='edit',
                               photos=photos,
                               gallery=gallery_model
                               )

    elif request.method == 'GET':
        form.title.data = gallery.title
        form.author.data = gallery.author
        form.videos.data = gallery.videos
        form.thumbnail.data = gallery.thumbnail_file

        # delete single photo
        if request.args.get('delete_filename'):
            try:
                delete_filename = request.args.get('delete_filename')
                remove_file('/images/galleries/' + str(gallery.id) + '/' + str(delete_filename))

                flash(f'Usunięto plik {str(delete_filename)}.', 'success')

                return redirect(url_for('CMS.update_gallery', gallery_secure_title=gallery_secure_title))
            except FileNotFoundError:
                flash('Nie ma takiego pliku.', 'warning')

                return redirect(url_for('CMS.update_gallery', gallery_secure_title=gallery_secure_title))
    return render_template('cms/gallery-form.html',
                           form=form,
                           action='edit',
                           photos=photos,
                           gallery=gallery_model
                           )


@CMS.route('/admin/galerie/<int:gallery_id>/usun', methods=['POST'])
@login_required
def delete_gallery(gallery_id):
    gallery = get_gallery_by_id(gallery_id)

    try:
        remove_file('/images/galleries/' + str(gallery.id), True)
        db.session.delete(gallery)
        db.session.commit()
    except Exception as e:
        flash('Przepraszamy! Wystąpił nieoczekiwany błąd.', 'error')
        mail = Mail('Błąd - OSK Kurs', 'Błąd przy usuwaniu galerii: ' + str(e), None,
                    recipients='psambek@gmail.com', raw_mail=True)
        mail.send()

        return redirect(url_for('CMS.all_galleries'))

    flash('Galeria została usunięta.', 'success')
    return redirect(url_for('CMS.all_galleries'))


@CMS.route('/admin/rider', methods=['POST', 'GET'])
@login_required
def rider():
    form = RiderForm()

    rider_dir = app.config['UPLOAD_FOLDER'] + '/files/rider/current'
    rider_files = [f for f in listdir(rider_dir) if isfile(join(rider_dir, f))]
    rider_files.sort(reverse=True)

    if rider_files:
        current_rider = rider_files[0]
    else:
        current_rider = None

    if request.method == 'POST' and form.validate_on_submit():
        try:
            if rider_files:
                for file in rider_files:
                    move_file(app.config['UPLOAD_FOLDER'] + '/files/rider/current/' + file, app.config['UPLOAD_FOLDER'] + '/files/rider/' + file)
            new_rider = request.files['rider']
            new_rider_filename = create_safe_filename(new_rider, random=True, date=False)
            save_file(new_rider, 'files/rider/current', new_rider_filename)

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


@CMS.route('/admin/dane', methods=['POST', 'GET'])
@login_required
def contact_data():
    form = ContactDataForm()

    phone = get_contact_item_by_key('phone')
    email = get_contact_item_by_key('email')

    if request.method == 'GET':
        form.phone.data = phone.value
        form.email.data = email.value

    elif request.method == 'POST' and form.validate_on_submit():
        phone.value = form.phone.data
        email.value = form.email.data

        try:
            db.session.commit()
        except Exception as e:
            flash('Przepraszamy! Wystąpił nieoczekiwany błąd.', 'error')
            mail = Mail('Błąd - CZZK', 'Błąd przy edycji danych kontaktowych: ' + str(e), None,
                        recipients='psambek@gmail.com', raw_mail=True)
            mail.send()

            return render_template('cms/contact-data-form.html', form=form)

        flash('Zaktualizowano dane.', 'success')

        return redirect(url_for('CMS.contact_data'))

    elif request.method == 'POST' and not form.validate_on_submit():
        flash('Formularz nie został wypełniony poprawnie.', 'warning')

    return render_template('cms/contact-data-form.html', form=form)
