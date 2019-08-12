from app import db


class Merch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    short_name = db.Column(db.String(120), nullable=False)
    safe_name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    gif = db.Column(db.String(120), nullable=False)
    jpg = db.Column(db.String(120), nullable=False)
    size_table = db.Column(db.Integer, nullable=True, default=0)

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


def get_all_merch_paginated(page):
    """
    Get all merch paginated.
    :return: Merch data.
    """

    merch = Merch.query. \
        paginate(page=page, per_page=10)

    return merch


def get_item_from_merch(safe_name):
    """
    Get specific item from merch.
    :return: Item data.
    """

    item = Merch.query. \
        filter_by(safe_name=safe_name). \
        first_or_404()

    return item


def get_item_by_id(item_id):
    """
    Get specific item from merch.
    :return: Item data.
    """

    item = Merch.query. \
        filter_by(id=item_id). \
        first_or_404()

    return item
