import sqlite3


_all_ = [
    "insert_ingredient",
    "get_ingredients_from_db",
    "get_ingredient_subset_from_db",
    "check_ingredient_from_db"
]


def insert_ingredient(name, type, note):
    with sqlite3.connect('cookbook.db') as conn:
        c = conn.cursor()
        c.execute(
            "INSERT INTO ingredient (name, type, note) VALUES (?, ?, ?)",
            (name, type, note)
        )


def get_ingredients_from_db():
    with sqlite3.connect('cookbook.db') as conn:
        c = conn.cursor()
        ingredients_list = c.execute(
            "SELECT * FROM ingredient")

    labels = ["id", "name", "type", "note"]
    ingredients = [
        dict(zip(labels, data))
        for data
        in ingredients_list.fetchall()
    ]
    return ingredients


def get_ingredient_subset_from_db(query):
    with sqlite3.connect('cookbook.db') as conn:
        c = conn.cursor()
        ingredients_list = c.execute(
            "SELECT name FROM ingredient WHERE name LIKE ?",
            ["%" + query + "%"]
        )
    return [ingredient[0] for ingredient in ingredients_list]


def check_ingredient_from_db(query):
    print(f"Query in function: {query}")
    with sqlite3.connect('cookbook.db') as conn:
        c = conn.cursor()
        ingredient = c.execute(
            "SELECT name FROM ingredient WHERE name LIKE ?",
            [query]
        ).fetchone()
    if ingredient:
        return True
    else:
        return False
