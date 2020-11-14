from flask import Flask, render_template


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
    return render_template("list_items.html", heading="Recipies")


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
    return render_template("list_items.html", heading="Ingredients")


@app.route('/ingredients/add')
def add_ingredients():
    """[summary]

    Returns:
        [type]: [description]
    """
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
    return render_template("test.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0')
