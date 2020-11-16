import sqlite3
import json


def insert_ingredient(name, type, note):
    with sqlite3.connect('cookbook.db') as conn:
        c = conn.cursor()
        c.execute(
            "INSERT INTO ingredient (name, type, note) VALUES (?, ?, ?)",
            (name, type, note)
        )


def list_ingredients():
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
    # return json.dumps(ingredients, ensure_ascii=False)
    return ingredients
