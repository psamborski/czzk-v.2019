import os
import secrets

from werkzeug.utils import secure_filename

from app import app


def create_safe_filename(file, random=True, date=False):
    random_hex = secrets.token_hex(6)
    f_name, f_ext = os.path.splitext(file.filename)
    if random:
        picture_fn = secure_filename(f_name)[:10] + "_" + random_hex + f_ext
    else:
        picture_fn = secure_filename(f_name) + f_ext

    if date:
        import datetime
        date = datetime.date.today().strftime("%Y-%m-%d")

        picture_fn = date + '_' + picture_fn

    return picture_fn


def save_file(file, relative_path, filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], relative_path, filename)
    file.save(file_path)

    return True


def remove_file(relative_path):
    os.remove(app.config['UPLOAD_FOLDER'] + relative_path)

    return True


def reformat_yt_link(link):
    core = 'https://www.youtube.com/embed/'
    if 'watch?v=' in str(link):
        equal_char_place = link.rfind('=')
        equal_char_place += 1
        new_link = core + link[equal_char_place:]
    else:
        slash_char_place = link.rfind('/')
        slash_char_place += 1
        new_link = core + link[slash_char_place:]

    return new_link




