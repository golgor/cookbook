from flask import Flask, render_template, request
from database import insert_ingredient, list_ingredients

app = Flask(__name__)


# RUN 'export FLASK_ENV=development'
@app.route('/')
def index():
    """[summary]

    Returns:
        [type]: [description]
    """
    return render_template("index.html")


@app.route('/recipies')
def list_recipies():
    """[summary]

    Returns:
        [type]: [description]
    """
    return render_template("list_recipies.html")


@app.route('/recipes/add')
def add_recipies():
    """[summary]

    Returns:
        [type]: [description]
    """
    return render_template("add_recipe.html")


@app.route('/ingredients')
def ingredients():
    """[summary]

    Returns:
        [type]: [description]
    """
    return render_template(
        "list_ingredients.html",
        ingredients=list_ingredients()
    )


@app.route('/ingredients/add', methods=['GET', 'POST'])
def add_ingredients():
    """[summary]

    Returns:
        [type]: [description]
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
    """[summary]

    Returns:
        [type]: [description]
    """
    return render_template("recipe.html")


@app.route('/test')
def test():
    """[summary]

    Returns:
        [type]: [description]
    """
    return render_template("recipe.html")


if __name__ == '__main__':
    app.run()
