import sqlite3
import json

_all_ = [
    "insert_ingredient",
    "get_ingredients_from_db",
    "get_ingredient_subset_from_db",
    "check_ingredient_from_db"
]


def insert_ingredient(name, ingredient_type, note):
    """Inserting a new ingredient in the ingredient table.

    Args:
        name (str): The name of the ingredient.
        ingredient_type (str): The kind of ingredient.
        note (str): A special note to add.
    """
    insert(table="ingredient", name=name, type=ingredient_type, note=note)


def get_ingredients_from_db():
    """Get all entries in the ingredient table.

    Returns:
        list: A list with a dict (json) for each row.
    """
    ingredients_list = select(table="ingredient")
    labels = ["id", "name", "type", "note"]
    ingredients = [
        dict(zip(labels, data))
        for data
        in ingredients_list
    ]
    return ingredients


def get_ingredient_subset_from_db(query):
    """Search for a name that contains "query". For example it can be
    used to give autocomplete suggestions in a searchbox.

    Args:
        query (str): A string to search for in the database.

    Returns:
        list: Returns a list of matches for the given query.
    """
    ingredients_list = select(
        table="ingredient", columns=("name",), name=query, exact_match=False
    )
    return [ingredient[0] for ingredient in ingredients_list]


def check_ingredient_from_db(query):
    """Check if an ingredient by the name stored in "query" is in the database.

    Args:
        query (str): The name of the ingredient to look for.

    Returns:
        Bool: Returns True if the ingredient is found, False otherwise.
    """
    ingredient = select(table="ingredient", name=query)
    if ingredient:
        return True
    else:
        return False


def add_recipe(name: str, difficulty: int, taste: int, time: str,
               preps: list, steps: list, ingredients: list):
    # Create preps and steps as a dict.
    # Intention to export to JSON and store as text.
    text = {
        "preps": [json.loads(prep) for prep in preps],
        "steps": [json.loads(step) for step in steps]
    }

    # Insert a new recipe into the recipe table.
    insert(
        table="recipe",
        name=name,
        steps=json.dumps(text, ensure_ascii=False),
        difficulty=difficulty,
        taste=taste,
        time=time
    )

    # Get the id of the added recipe. To be used when adding ingredients
    # in ingredients_list table.
    # [0][0] due to fetchall that returns list of tuples.
    recipe_id = select(
        table="recipe", columns=("id",), single_match=True, name=name
    )

    # Loads the ingredients
    # from: a list with json strings
    # to: a list with dicts, one for each ingredient.
    ingredient_list = [
        json.loads(ingredient) for ingredient in ingredients
    ]

    # Creating a list with all ingredients and add the id.
    # Same order as ingredients in ingredient_list table.
    ingredient_list = [
        (
            recipe_id,
            select(
                table="ingredient",
                columns=("id",),
                name=ingredient["name"],
                single_match=True
            ),
            ingredient["amount"],
            ingredient["unit"]
        )
        for ingredient
        in ingredient_list
    ]

    # Insert an entry into ingredient list
    for recipe_id, ingredient_id, amount, unit in ingredient_list:
        insert(
            table="ingredient_list",
            recipe_id=recipe_id,
            ingredient_id=ingredient_id,
            amount=amount,
            unit=unit
        )


def insert(table, **kwargs):
    """Insert an entry into a specific table.

    Args:
        table (str): [description]
        kwargs (*): Each "key:value"-pair is a "column:value"
    """
    keys = list(kwargs.keys())
    values = list(kwargs.values())

    columns = "(" + ", ".join(keys) + ")"
    placeholders = "(" + ", ".join(["?"]*len(keys)) + ")"
    query_string = f"INSERT INTO {table} {columns} VALUES {placeholders}"

    with sqlite3.connect('cookbook.db') as conn:
        c = conn.cursor()
        c.execute(query_string, values)


def select(table, columns=None, exact_match=True, single_match=False, **kwargs):
    """Running a select query against a specific table.

    Kwargs is used as a filter. This function can only handle one filter
    variable and the query is built as 'WHERE key LIKE value'.

    Examples:
        select(table="ingredient"):
            SELECT * FROM ingredient
        select(table="ingredient", columns=("id",)):
            SELECT id FROM ingredient
        select(table="ingredient", name="Morot"):
            SELECT * FROM ingredient WHERE name LIKE "Morot"

    Args:
        table (str): Name of the table to query
        columns (tuple), optional): A tuple of the columns to return.
            If none, assumes *.

    Returns:
        list: A list with tuples, containing all the matches.
    """
    if len(kwargs) > 1:
        print("Only one keyword value is accepted.")
        return False

    if columns:
        columns_query = ", ".join(columns)
    else:
        columns_query = "*"

    query_string = f"SELECT {columns_query} FROM {table}"

    if kwargs:
        key = list(kwargs.keys())[0]
        if exact_match:
            value = list(kwargs.values())[0]
        else:
            # Wildcard placeholder for sql query added ('%').
            # Only makes sense with strings.
            value = "%" + str(list(kwargs.values())[0]) + "%"

        query_string += f" WHERE {key} LIKE ?"
        with sqlite3.connect('cookbook.db') as conn:
            c = conn.cursor()
            ret = c.execute(query_string, (value,)).fetchall()
    else:
        with sqlite3.connect('cookbook.db') as conn:
            c = conn.cursor()
            ret = c.execute(query_string).fetchall()

    # Extract the first element as long as ret is a iterable if requested.
    if single_match:
        while hasattr(ret, '__iter__'):
            ret = ret[0]
    return ret


def main():
    add_recipe(
        name="Title",
        difficulty=1,
        taste=2,
        time="00:01:00",
        preps=['{"text":"sätt på ugenn"}', '{"text":"tjosan"}'],
        steps=['{"text":"koka potatis"}', '{"text":"ät potatisen"}'],
        ingredients=[
            '{"name":"Mjölk","amount":2,"unit":"l"}',
            '{"name":"Potatis","amount":2,"unit":"l"}'
        ]
    )


if __name__ == '__main__':
    main()
