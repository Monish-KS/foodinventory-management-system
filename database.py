from database_connect import engine
from sqlalchemy import text


def load_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("select * from inventory"))
        food_items = []
        for row in result.all():
            food_items.append(dict(row._mapping))
        return food_items
