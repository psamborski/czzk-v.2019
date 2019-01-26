from app import db


class Merch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    short_name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    gif = db.Column(db.String(120), nullable=False)
    jpg = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"Album('{self.name}', '{self.description}')"


def get_all_merch():
    """
    Get all merch.
    :return: Merch data.
    """

    merch = Merch.query. \
        all()

    return merch
