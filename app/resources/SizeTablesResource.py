from app import db


class SizeTables(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(120), nullable=False)
    key = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)
    copy = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Size table('{self.key}', '{self.content}')"


def get_table_by_keyword(keyword):
    """
    Get table by keyword.
    :return: Table's content.
    """

    table = SizeTables.query. \
        filter_by(keyword=keyword). \
        first()

    return table


def get_table_by_key(key):
    """
    Get table by key.
    :return: Table's content.
    """

    table = SizeTables.query. \
        filter_by(key=key). \
        first()

    return table
