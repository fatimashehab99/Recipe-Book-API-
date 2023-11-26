from app import db, app


class person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    lastname = db.Column(db.String(80))

    def __init__(self, username, lastname):
        self.username = username
        self.lastname = lastname


with app.app_context():
    db.create_all()
