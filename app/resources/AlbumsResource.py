from app import db


class Albums(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    cover_file = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"Album('{self.title}', '{self.year}')"


def get_all_albums():
    """
    Get all albums sorted by year.
    :return: Albums data.
    """

    albums = Albums.query. \
        order_by(Albums.year.desc()).\
        all()

    return albums
