from app import db


class Galleries(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    secure_title = db.Column(db.String(120), nullable=False)
    thumbnail_file = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"Album('{self.title}')"


def get_all_galleries(page):
    """
    Get all galleries.
    :return: Galleries data.
    """

    galleries = Galleries.query. \
        order_by(Galleries.date.desc()). \
        paginate(page=page, per_page=9)

    return galleries


def get_gallery_by_secure_title(secure_title):
    """
    Get gallery by its secure title.
    :param secure_title:
    :return: Gallery data.
    """
    gallery = Galleries.query. \
        filter_by(secure_title=secure_title). \
        first_or_404()

    return gallery


# TODO unique gallery title
