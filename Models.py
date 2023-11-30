from datetime import datetime

from app import db, app


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


with app.app_context():
    # creating tables' schemas
    db.create_all()
    # creating seeds
    ingredients = [
        Ingredient("Black Pepper",
                   "Black pepper, derived from the dried berries of the Piper nigrum vine,"
                   " adds a pungent and versatile flavor to dishes, serving as a staple spice"
                   " with digestive benefits and a history of trade and cultural significance"),
        Ingredient("Onion",
                   " pungent and versatile vegetable, adds layers of flavor to dishes"),
        Ingredient("Garlic",
                   "with its distinct aroma and savory taste, enhances culinary creations with depth and richnes"),
        Ingredient("Baking Powder",
                   "a leavening agent composed of a combination of an acid and a base, is used in baking to "
                   "promote the rising of dough and batter, resulting in light and fluffy baked goods")
    ]
    db.session.add_all(ingredients)
    db.session.commit()

    categories = [
        Category("desserts", " a delightful and indulgent course typically enjoyed after a meal, encompasses"
                             " a wide array of sweet treats, from cakes and pies to ice cream and pastries"),
        Category("stew", " a hearty and savory dish, involves slow-cooking ingredients such as meat, vegetables,"
                         " and seasonings in a flavorful liquid, resulting in a rich and comforting one-pot meal")
    ]
    db.session.add_all(categories)
    db.session.commit()

    recipes = [
        Recipe("Chicken and Vegetable Stew",
               "A wholesome chicken and vegetable stew combines tender pieces of chicken with an assortment "
               "of colorful vegetables such as carrots, celery, and peas. Slow-cooked in a flavorful broth, "
               "this stew is seasoned with aromatic herbs, creating a comforting and nutritious meal",
               "Begin by browning seasoned chicken pieces in a large pot, then sauté aromatic onions and garlic. "
               "Add colorful vegetables such as carrots and celery, pour in a flavorful broth, and simmer on low "
               "heat until the chicken is tender and the vegetables are cooked to perfection",
               "", 2),
        Recipe("Classic Apple Pie",
               "A classic apple pie is a timeless dessert that showcases a flaky, buttery crust enveloping slices "
               "of tart apples seasoned with cinnamon and sugar. Baked to golden perfection, the pie is often served"
               " warm and topped with a scoop of vanilla ice cream for a delightful combination of textures and flavors",
               "Prepare a flaky pie crust, roll it out, and place it in a pie dish. Fill the crust with a mixture of thinly"
               "\ sliced apples tossed in cinnamon and sugar, cover with a second crust, and bake until golden brown. Allow"
               " the pie to cool before serving for a delightful dessert with the perfect balance of sweet and tart flavors",
               "", 1)
    ]
    db.session.add_all(recipes)
    db.session.commit()

    ingredient_recipes = [
        IngredientRecipe(1, 1),
        IngredientRecipe(2, 1),
        IngredientRecipe(3, 1),
        IngredientRecipe(4, 2)
    ]
    db.session.add_all(ingredient_recipes)
    db.session.commit()

