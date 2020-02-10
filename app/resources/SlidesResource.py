from app import db


class Slides(db.Model):
    """
    Table for slides in slider on index page.
    """
    id = db.Column(db.Integer, primary_key=True)
    order = db.Column(db.Integer(), nullable=False)
    content = db.Column(db.String(120), nullable=False)
    type = db.Column(db.String(1), nullable=False)
    display = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self):
        return f"Album('{self.content}', '{self.type}')"


def get_all_slides():
    """
    Get all slides.
    :return: Slides data.
    """

    slides = Slides.query. \
        order_by(Slides.order.asc()). \
        all()

    return slides


def get_slides_for_display():
    """
    Get all slides for display.
    :return: Slides data.
    """

    slides = Slides.query. \
        filter_by(display=1). \
        order_by(Slides.order.asc()). \
        all()

    return slides
