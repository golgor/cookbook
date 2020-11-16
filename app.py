from flask import Flask, render_template, request
from database import insert_ingredient, list_ingredients

app = Flask(__name__)


# RUN 'export FLASK_ENV=development'
@app.route('/')
def index():
    """Index with cards for a variety of recipies.
    """
    return render_template("index.html")


@app.route('/recipies')
def list_recipies():
    """Route to list all recipies in the database in a list/table.
    """
    return render_template("list_recipies.html")


@app.route('/recipes/add', methods=['GET', 'POST'])
def add_recipies():
    """Route to add recipes to the database.
    """
    if request.method == 'POST':
        print(request.form.get("heading"))
        print(request.form.get("difficulty"))
        print(request.form.get("taste"))
        print(request.form.get("time"))
        print(request.form.get("short_info"))
        print(request.form.getlist("prep_input"))
    return render_template("add_recipe.html")


@app.route('/ingredients')
def ingredients():
    """Route to list all ingredients currently in the database.
    """
    return render_template(
        "list_ingredients.html",
        ingredients=list_ingredients()
    )


@app.route('/ingredients/add', methods=['GET', 'POST'])
def add_ingredients():
    """Route to add new ingredients to the database.
    """
    if request.method == 'POST':
        insert_ingredient(
            name=request.form.get("name"),
            type=request.form.get("type"),
            note=request.form.get("note")
        )
    return render_template("add_ingredient.html")


@app.route('/random')
def randomize():
    """Route to randomize and show a specific recipe.
    """
    return render_template("recipe.html")


@app.route('/test')
def test():
    """Route for testing purposes during development.
    """
    return render_template("recipe.html")


if __name__ == '__main__':
    app.run()
