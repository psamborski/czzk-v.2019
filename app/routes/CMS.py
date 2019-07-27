from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_user, current_user, logout_user, login_required

from app import bcrypt

from app.forms.LoginForm import LoginForm
from app.forms.ConcertForm import ConcertForm

from app.resources.ConcertsResource import get_all_concerts
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
def add_course():
    form = ConcertForm()
    if request.method == 'POST' and form.validate_on_submit():
        course = Courses(
            name=form.name.data,
            organizingMeetingDate=form.organizing_meeting_date.data,
            organizingMeetingTime=form.organizing_meeting_time.data,
            startDate=form.start_date.data,
            startTime=form.start_time.data,
            cost=form.cost.data,
            studentLimit=form.limit.data,
            additionalData=form.additionalData.data
        )

        db.session.add(course)
        try:
            db.session.commit()
        except Exception as e:
            flash('Przepraszamy! Wystąpił nieoczekiwany błąd.', 'error')
            mail = Mail('Błąd - OSK Kurs', 'Błąd przy tworzeniu kursu: ' + str(e),
                        'psambek@gmail.com')
            mail.send()

            return render_template('cms/course-form.html', form=form, action='add')

        flash('Utworzono nowy kurs.', 'success')

        return redirect(url_for('CMS.all_courses'))

    elif request.method == 'POST' and not form.validate_on_submit():
        flash('Formularz nie został wypełniony poprawnie.', 'warning')

        return render_template('cms/course-form.html', form=form, action='add')

    return render_template('cms/course-form.html', form=form, action='add')


@CMS.route('/admin/kursy/<int:course_id>/edytuj', methods=['POST', 'GET'])
@login_required
def update_course(course_id):
    course = get_course_by_id(course_id)

    form = CourseForm()

    if request.method == 'POST' and form.validate_on_submit():
        course.name = form.name.data
        course.startDate = form.start_date.data
        course.startTime = form.start_time.data
        course.organizingMeetingDate = form.organizing_meeting_date.data
        course.organizingMeetingTime = form.organizing_meeting_time.data
        course.studentLimit = form.limit.data
        course.cost = form.cost.data
        course.additionalData = form.additionalData.data

        try:
            db.session.commit()
        except Exception as e:
            flash('Przepraszamy! Wystąpił nieoczekiwany błąd.', 'error')
            mail = Mail('Błąd - OSK Kurs', 'Błąd przy edycji kursu: ' + str(e),
                        'psambek@gmail.com')
            mail.send()

            return render_template('cms/course-form.html', form=form, action='edit')

        flash('Zaktualizowano kurs.', 'success')

        return redirect(url_for('CMS.specific_course', course_id=course_id))

    elif request.method == 'POST' and not form.validate_on_submit():
        flash('Formularz nie został wypełniony poprawnie.', 'warning')

        return render_template('cms/course-form.html', form=form, action='edit')

    elif request.method == 'GET':
        form.name.data = course.name
        form.start_date.data = course.startDate
        form.start_time.data = course.startTime
        form.organizing_meeting_date.data = course.organizingMeetingDate
        form.organizing_meeting_time.data = course.organizingMeetingTime
        form.limit.data = course.studentLimit
        form.cost.data = course.cost
        form.additionalData.data = course.additionalData

        return render_template('cms/course-form.html', form=form, action='edit')

    return render_template('cms/course-form.html', form=form, action='edit')


@CMS.route("/admin/kursy/<int:course_id>/usun", methods=['POST'])
@login_required
def delete_course(course_id):
    course = get_course_by_id(course_id)

    delete_students_by_course(course_id)

    try:
        db.session.delete(course)
        db.session.commit()
    except Exception as e:
        flash('Przepraszamy! Wystąpił nieoczekiwany błąd.', 'error')
        mail = Mail('Błąd - OSK Kurs', 'Błąd przy usuwaniu kursu: ' + str(e),
                    'psambek@gmail.com')
        mail.send()

        return redirect(url_for('CMS.all_courses'))

    # deleting multiple rows can be quicker with engine
    # https://stackoverflow.com/questions/39773560/sqlalchemy-how-do-you-delete-multiple-rows-without-querying
    # https: // docs.sqlalchemy.org / en / latest / core / connections.html

    flash('Kurs został usunięty.', 'success')
    return redirect(url_for('CMS.all_courses'))


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

