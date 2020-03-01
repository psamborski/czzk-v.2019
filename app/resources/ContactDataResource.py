from app import db


class ContactData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(120), nullable=False)
    value = db.Column(db.String(512), nullable=False)

    def __repr__(self):
        return f"Contact('{self.key}', '{self.value}')"


def get_contact_item_by_key(key):
    """
    Get contact item by key.
    :return: Contact item.
    """

    item = ContactData.query. \
        filter_by(key=key). \
        first_or_404()

    return item
