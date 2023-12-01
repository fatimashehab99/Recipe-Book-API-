# Recipe-Book-API-
**Project Idea** : Building Recipe Book API using flask which is python framework to build APIs and SQLAlchemy which is SQL toolkit written in python

Steps:

1-Create a database in your local dataase and step up a connection as follow:
`app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:root@localhost/recipe_book'`
You can choose any sql database type

2-Run `python app.py` in the terminal to be able to create the database schema

3-Run `python seeds.py` in the terminal to create seeds(data) in the database table

4-Try the APIs build in the project

