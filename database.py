import sqlite3


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
        ingredients = c.execute(
            "SELECT * FROM ingredient")
    print(ingredients.fetchall())
