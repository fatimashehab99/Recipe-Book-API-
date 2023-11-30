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
        result = "Connection to the database is succeeded!"

    except Exception as e:
        result = f"Error connecting to the database: {str(e)}"


@app.route('/')
def hello_world():
    return "Hello, World ,fofof !"


@app.route("/second")
def sec():
    return "20"


if __name__ == '__main__':
    print("helloo")
    with app.app_context():
        db.create_all()
    app.run()
