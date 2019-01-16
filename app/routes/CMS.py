from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user, current_user, logout_user, login_required

from app import bcrypt

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


@CMS.route('/panel/slider', methods=['POST', 'GET'])
def slider():
        return render_template('cms/slider.html', form=None, message='Pomyślnie zedytowano slider.')


@CMS.route('/panel/teksty')
def texts():
    return render_template('cms/texts.html')


@CMS.route('/panel/ustawienia', methods=['POST', 'GET'])
def settings():
    return render_template('cms/settings.html', form=None, message='Pomyślnie zmieniono dane.')


@CMS.route('/panel/koncerty')
def concerts():
    return render_template('cms/concerts.html')


@CMS.route('/panel/gadzety')
def merch():
    return render_template('cms/merch.html')


@CMS.route('/panel/albumy')
def albums():
    return render_template('cms/albums.html')


@CMS.route('/panel/galeria')
def gallery():
    return render_template('cms/gallery.html')
