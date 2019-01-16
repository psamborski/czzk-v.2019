from flask_login import UserMixin

from app import db, login_manager


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    passwordHash = db.Column(db.String(240), nullable=False)
    email = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f"Student('{self.username}', '{self.email}')"


def get_user(username='admin-kurs'):  # TODO change/remove this default
    user = Users.query. \
        filter(Users.username == username). \
        first()

    return user


def get_admin_mail():
    user = get_user('admin-kurs')

    email = user.email

    return email


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))
