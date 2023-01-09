from db import db


class Img(db.Model):
    month = db.Column(db.Text, unique=False, nullable=False)
    id = db.Column(db.Integer, primary_key=True, unique=False)
    img = db.Column(db.Text, unique=False, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
