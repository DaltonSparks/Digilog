from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def db_init(app):
    db.init_app(app)

    # create tables if the db does not already exist
    with app.app_context():
        db.create_all()
