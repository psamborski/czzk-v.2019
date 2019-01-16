from app import db


class Texts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    page = db.Column(db.String(120), nullable=False)
    order = db.Column(db.Integer(), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Text('{self.title}', '{self.page}')"


def get_text_by_page(page):
    """
    Get whole text by page.
    :return: All text's chapters.
    """

    chapters = Texts.query. \
        filter_by(page=page). \
        order_by(Texts.order.asc()). \
        all()

    return chapters
