from flask import Flask, render_template, request, jsonify, redirect
import database as db
import json


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
    return render_template(
        "list_recipies.html",
        recipies=db.select(
            "recipe",
            columns=("id", "name", "difficulty", "taste", "time")
        )
    )


@app.route('/recipes/add', methods=['GET', 'POST'])
def add_recipies():
    """Route to add recipes to the database.
    """
    if request.method == 'POST':
        db.add_recipe(
            name=request.form.get('title'),
            difficulty=request.form.get('difficulty'),
            taste=request.form.get('taste'),
            time=request.form.get('time'),
            preps=request.form.getlist('prep_input'),
            steps=request.form.getlist('recipe_steps_list'),
            ingredients=request.form.getlist('ingredient_input')
        )
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


@app.route('/recipes')
def show_recipe():
    recipe_id = request.args.get("id")
    if recipe_id:
        # Get all data from recipe table
        recipe = db.select(
            "recipe",
            columns=("name", "steps", "difficulty", "taste", "time"),
            id=recipe_id
        )[0]
        name = recipe[0]

        # Deserialize string into a dict.
        text = json.loads(recipe[1])

        # Create a simple list with all steps for preps and steps
        preps = [prep["text"] for prep in text["preps"]]
        steps = [step["text"] for step in text["steps"]]

        difficulty = recipe[2]
        taste = recipe[3]
        time = recipe[4]

        # Get all ingredients for the specific recipe
        ingredients = [
            list(ingredient)
            for ingredient
            in db.get_ingredients(recipe_id)]

        return render_template(
            "recipe.html",
            name=name,
            preps=preps,
            steps=steps,
            difficulty=difficulty,
            taste=taste,
            time=time,
            ingredients=ingredients
        )
    else:
        return render_template("index.html")


@app.route('/random')
def randomize():
    """Route to randomize and show a specific recipe.

    TODO: Add random number generator and change redirect accordingly.
    """
    return redirect("/recipes?id=1")


if __name__ == '__main__':
    app.run()
