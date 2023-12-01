from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
# DB connection
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:root@localhost/recipe_book'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Test your db connection
""""
with app.app_context():
    try:
        db.create_all()
        result = "Connection to the database is succeeded!"

    except Exception as e:
        result = f"Error connecting to the database: {str(e)}"
"""


# models
class Ingredient(db.Model):
    __tablename__ = "ingredients"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(250))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name, description):
        self.name = name
        self.description = description


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(250))
    sort_number = db.Column(db.Integer, default=0)
    is_hidden = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    recipes = db.relationship('Recipe', backref='categories', lazy=True)

    def __init__(self, name, description):
        self.name = name
        self.description = description


class Recipe(db.Model):
    __tablename__ = "recipes"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(500))
    procedure = db.Column(db.String(500))
    link = db.Column(db.String(250))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    sort_number = db.Column(db.Integer, default=0)
    is_hidden = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    ingredients = db.relationship('Ingredient', secondary='ingredient_recipe', backref='recipes')

    def __init__(self, name, description, procedure, link, category_id):
        self.name = name
        self.description = description
        self.procedure = procedure
        self.link = link
        self.category_id = category_id


class IngredientRecipe(db.Model):
    __tablename__ = "ingredient_recipe"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey("ingredients.id"))
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.id"))

    def __init__(self, ingredient_id, recipe_id):
        self.ingredient_id = ingredient_id
        self.recipe_id = recipe_id


@app.route('/')
def hello_world():
    return "Hello to my Recipe Book API kindly try the APIs in the read me file and hope you will enjoy it"


@app.route("/recipes")
def getRecipes():
    recipes = Recipe.query.join(Category) \
        .filter(Recipe.is_hidden == False).order_by(Recipe.sort_number).all()
    jsonRecipes = [{
        "id": recipe.id,
        "recipe_name": recipe.name,
        "recipe_description": recipe.description,
        "recipe_procedure": recipe.procedure,
        "recipe_link": recipe.link,
        "category_name": recipe.categories.name,
        "category_id": recipe.categories.id
    }
        for recipe in recipes
    ]
    return jsonify(jsonRecipes)


@app.route("/categories")
def getCategories():
    categories = Category.query.filter(Category.is_hidden == False) \
        .order_by(Category.sort_number).all()
    jsonCategories = [{
        "id": category.id,
        "category_name": category.name,
        "category_description": category.description
    }
        for category in categories
    ]
    return jsonify(jsonCategories)


@app.route("/recipes/<int:recipe_id>")
def getRecipeById(recipe_id):
    recipe = Recipe.query.filter_by(id=recipe_id, is_hidden=False).first()
    if (recipe):
        ingredients = Ingredient.query.join(IngredientRecipe) \
            .filter(IngredientRecipe.recipe_id == recipe_id).all()
        jsonIngredients = [{
            "ingredient_id": ingredient.id,
            "ingredient_name": ingredient.name,
            "ingredient_description": ingredient.description
        }
            for ingredient in ingredients
        ]
        recipe = {
            "recipe_id": recipe.id,
            "recipe_name": recipe.name,
            "recipe_description": recipe.description,
            "recipe_procedure": recipe.procedure,
            "recipe_link": recipe.link,

        }
        data = {
            "recipe": recipe,
            "ingredients": jsonIngredients
        }
        return jsonify(data)
    else:
        message = {"message": "Recipe Not Found"}
        return message, 404


@app.route("/recipes/ingredients/<int:ingredient_id>")
def getIngredientById(ingredient_id):
    ingredient = Ingredient.query.filter_by(id=ingredient_id).first()
    if (ingredient):
        jsonIngredient = {
            "ingredient_id": ingredient.id,
            "ingredient_name": ingredient.name,
            "ingredient_description": ingredient.description
        }
        return jsonify(jsonIngredient)
    else:
        message = {"message": "Ingredient Not Found"}
        return message, 404


@app.route("/recipes/categories/<string:category>")
def getRecipeByCategory(category):
    category = Category.query.filter(Category.name.ilike(f"%{category}%"), Category.is_hidden == False) \
        .first()
    if (category):
        jsonCategory = {
            "category_id": category.id
        }
        recipes = Recipe.query.filter(Recipe.category_id == jsonCategory['category_id'], Category.is_hidden == False) \
            .order_by(Category.sort_number).all()

        jsonRecipes = [{
            "recipe_id": recipe.id,
            "recipe_name": recipe.name,
            "recipe_description": recipe.description,
            "recipe_procedure": recipe.procedure,
            "recipe_link": recipe.link,
        }
            for recipe in recipes]
        return jsonify(jsonRecipes)

    else:
        message = {"message": "Category Not Found"}
        return message, 404


@app.route("/recipes/ingredients/<string:ingredient>")
def getRecipesByIngredient(ingredient):
    ingredient = Ingredient.query.filter(Ingredient.name.ilike(f"%{ingredient}%")).first()
    if (ingredient):
        jsonIngredient = {
            "ingredient_id": ingredient.id
        }
        recipes = Recipe.query.join(IngredientRecipe) \
            .filter(IngredientRecipe.ingredient_id == jsonIngredient['ingredient_id'],
                    Recipe.is_hidden == False).order_by(Recipe.sort_number).all()
        if (recipes):
            jsonRecipes = [{
                "recipe_id": recipe.id,
                "recipe_name": recipe.name,
                "recipe_description": recipe.description,
                "recipe_procedure": recipe.procedure,
                "recipe_link": recipe.link,
            } for recipe in recipes]
            return jsonify(jsonRecipes)
        else:
            message = {"message": 'No Recipe Found'}
            return message, 404

    else:
        message = {"message": "Ingredient Not Found"}
        return message, 404


@app.route("/recipe", methods=['POST'])
def addRecipe():
    data = request.get_json()
    try:
        recipe = Recipe(data['name'], data['description'], data['procedure'], data['link'], data['category_id'])
        db.session.add(recipe)
        db.session.commit()
        message = {"message": "Recipe is added"}
        return message, 200
    except:
        message = {"message": "Failed"}
        return message, 403


@app.route("/ingredient", methods=['POST'])
def addIngredient():
    data = request.get_json()
    try:
        ingredient = Ingredient(data['name'], data['description'])
        db.session.add(ingredient)
        db.session.commit()
        message = {"message": "Ingredient is added"}
        return message, 200
    except:
        message = {"message": "Failed"}
        return message, 403


@app.route("/recipe/ingredient", methods=['POST'])
def addIngredientToRecipe():
    data = request.get_json()
    try:
        ingredient = IngredientRecipe(data['ingredient_id'], data['recipe_id'])
        db.session.add(ingredient)
        db.session.commit()
        message = {"message": "Ingredient is added"}
        return message, 200
    except:
        message = {"message": "Failed"}
        return message, 403


if __name__ == '__main__':
    with app.app_context():
        # create db schemas
        db.create_all()
    app.run()
