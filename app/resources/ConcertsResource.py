from app import db
import datetime


class Concerts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(240), nullable=False)
    place = db.Column(db.String(120), nullable=False)
    date = db.Column(db.Date(), nullable=False)

    def __repr__(self):
        return f"Concert('{self.name}', '{self.date}')"


def get_concert_by_id(concert_id):
    """
    Get concert by ID.
    :return: Concert data or None.
    """
    concert = Concerts.query. \
        filter_by(id=concert_id). \
        first_or_404()

    return concert

def get_all_concerts(page):
    """
    Get all concerts.
    :return: Concerts data.
    """

    concerts = Concerts.query. \
        order_by(Concerts.date.desc()). \
        paginate(page=page, per_page=10)

    return concerts


def get_planned_concerts(limit=None):
    """
    Get planned concerts. If limit is passed, limit results.
    :return: Concerts data.
    """

    current_date = datetime.datetime.now().date()
    concerts = Concerts.query. \
        filter(Concerts.date >= current_date). \
        order_by(Concerts.date.asc()). \
        limit(limit).\
        all()

    return concerts


def get_past_concerts():
    """
    Get past concerts.
    :return: Concerts data.
    """

    current_date = datetime.datetime.now().date()
    concerts = Concerts.query. \
        filter(Concerts.date < current_date). \
        order_by(Concerts.date.desc()). \
        all()

    return concerts
