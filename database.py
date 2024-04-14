from database_connect import engine
from sqlalchemy import text


def load_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("select * from inventory"))
        food_items = []
        for row in result.all():
            food_items.append(dict(row._mapping))
        return food_items

def load_fruit_from_db(id):
    with engine.connect() as conn:
        result = conn.execute(text(f"select * from inventory WHERE ItemID = '{id}'"))
        result_all = result.all()
        column_names = result.keys()
        rows = []
        for row in result_all:
            rows.append(dict(zip(column_names,row)))
        if len(rows) == 0:
            return None
        else:
            return rows[0]


def insert_into_database(data):
    try:
        with engine.connect() as conn:
            query = text(
                    f"INSERT INTO inventory (Name, Category, Quantity, ExpDate, SupplierID) VALUES ('{data['name']}', '{data['category']}', {data['quantity']}, '{data['exp_date']}', '{data['supplier_id']}')"
                )
            conn.execute(query)
            conn.commit()  # Commit changes to the database
        return True  # Return True if insertion is successful
    except Exception as e:
        print(f"Error inserting data into database: {e}")
        return False  # Return False if an error occurs during insertion
