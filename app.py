from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# DB connection
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:root@localhost/recipe_book'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# check connection
with app.app_context():
    try:
        db.create_all()
        x = "Connection to the database is succeeded!"

    except Exception as e:
        x = f"Error connecting to the database: {str(e)}"


@app.route('/')
def hello_world():  # put application's code here
    return x


if __name__ == '__main__':
    app.run()
