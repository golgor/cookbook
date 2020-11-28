import sqlite3
import json

_all_ = [
    "insert_ingredient",
    "get_ingredients_from_db",
    "get_ingredient_subset_from_db",
    "check_ingredient_from_db"
]


def insert_ingredient(name, ingredient_type, note):
    with sqlite3.connect('cookbook.db') as conn:
        c = conn.cursor()
        c.execute(
            "INSERT INTO ingredient (name, type, note) VALUES (?, ?, ?)",
            (name, ingredient_type, note)
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


# Heading: Title
# Difficulty: 1
# Taste: 2
# Time: 00:01:00
# Prep_input: ['{"text":"sätt på ugenn"}', '{"text":"tjosan"}']
# Ingredient_input: ['{"name":"Mjölk","amount":2,"unit":"l"}', '{"name":"Potatis","amount":2,"unit":"l"}']
# Recipe steps: ['{"text":"koka potatis"}', '{"text":"ät potatisen"}']


def add_recipe(name: str, difficulty: int, taste: int, time: str,
               preps: list, steps: list, ingredients: list):
    # Skapar tom dict dit jag lägger all text
    text = {}
    ingredient_dict = {}

    # Skapar preps och avkodar JSON för att skapa en dict i python
    text["preps"] = [json.loads(prep) for prep in preps]
    text["steps"] = [json.loads(step) for step in steps]

    # Kodar i JSON igen för att lagra som text i databasen
    json_text = json.dumps(text, ensure_ascii=False)

    # Insert into recipe database.
    with sqlite3.connect('cookbook.db') as conn:
        c = conn.cursor()
        c.execute(
            "INSERT INTO recipe (name, steps, difficulty, taste, time) \
                VALUES (?, ?, ?, ?, ?)",
            (name, json_text, difficulty, taste, time)
        )

        # Get the id from the newly added recipe
        id = c.execute(
            "SELECT id FROM recipe WHERE name = ?",
            (name,)
        ).fetchone()

    ingredient_dict["ingredients"] = [
        json.loads(ingredient) for ingredient in ingredients
    ]

    # Creating a list with all ingredient and add the id. Same order as ingredients in ingredient_list table. !!!! Change name with ingredient_id !!!!
    ingredient_list = [(*id, ing["name"], ing["amount"], ing["unit"]) for ing in ingredient_dict["ingredients"]]

    # Write to the database.
    with sqlite3.connect('cookbook.db') as conn:
        c = conn.cursor()
        c.executemany(
            "INSERT INTO ingredient_list VALUES (?, ?, ?, ?)",
            ingredient_list
        )


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
