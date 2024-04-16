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


def insert_request_into_database(data):
    try:
        with engine.connect() as conn:
            query = text(f"INSERT INTO requests (requester_name, request_date, item_id, item_name, quantity, status) VALUES ('{data['requester_name']}', '{data['request_date']}', '{data['item_id']}','{data['item_name']}', {data['quantity']}, 'pending')")
            conn.execute(query)
            conn.commit()
        return True
    except Exception as e:
        print(f"Error inserting data into request database: {e}")
        return False


def load_requests_from_db():
    try:
        with engine.connect() as conn:
            
            result = conn.execute(text(f"Select * from requests"))
            requests = []
            for row in result.all():
                requests.append(dict(row._mapping))
            print(requests)
            return requests
    except Exception as e:
        print(f"Error from database: {e}")
        return None
    
def load_suppliers_from_db():
    try:
        with engine.connect() as conn:
            result = conn.execute(text(f"select * from supplier"))
            suppliers = []
            for row in result.all():
                suppliers.append(dict(row._mapping))
            print(suppliers)
            return suppliers
    except Exception as e:
        print(f"Can't reciever supplier data{e}")
        return None