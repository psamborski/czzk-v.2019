from app import db


class Albums(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Date(), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    cover_file = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"Album('{self.title}', '{self.year}')"
