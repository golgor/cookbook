from flask import Flask, render_template, request, jsonify
import database as db


app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False


# RUN 'export FLASK_ENV=development'
@app.route('/')
def index():
    """Index with cards for a variety of recipies.
    """
    return render_template("index.html")


@app.route('/recipies/list')
def list_recipies():
    """Route to list all recipies in the database in a list/table.
    """
    return render_template("list_recipies.html")


@app.route('/recipes/add', methods=['GET', 'POST'])
def add_recipies():
    """Route to add recipes to the database.
    """
    if request.method == 'POST':
        print(f"Heading: {request.form.get('heading')}")
        print(f"Difficulty: {request.form.get('difficulty')}")
        print(f"Taste: {request.form.get('taste')}")
        print(f"Time: {request.form.get('time')}")
        print(f"Short_info: {request.form.get('short_info')}")
        print(f"Prep_input: {request.form.getlist('prep_input')}")
        print(f"Ingredient_input: {request.form.getlist('ingredient_input')}")
    return render_template("add_recipe.html")


@app.route('/ingredients/list')
def list_ingredients():
    """Route to list all ingredients currently in the database.
    """
    return render_template(
        "list_ingredients.html",
        ingredients=db.get_ingredients_from_db()
    )


@app.route('/ingredients')
def ingredients():
    """Route to list all ingredients currently in the database.
    """
    query = request.args.get("q")
    ingredients = db.get_ingredient_subset_from_db(query)
    return jsonify(ingredients)


@app.route('/ingredients/check')
def check_ingredients():
    """Route to list all ingredients currently in the database.
    """
    query = request.args.get("q")
    print(f"Query recieved: {query}")
    ingredients = db.check_ingredient_from_db(query)
    return jsonify(ingredients)


@app.route('/ingredients/add', methods=['GET', 'POST'])
def add_ingredients():
    """Route to add new ingredients to the database.
    """
    if request.method == 'POST':
        db.insert_ingredient(
            name=request.form.get("name"),
            ingredient_type=request.form.get("type"),
            note=request.form.get("note"),
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
