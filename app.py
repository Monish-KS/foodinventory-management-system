from flask import Flask, render_template,jsonify,request
from database import load_from_db, load_fruit_from_db,insert_into_database

app = Flask(__name__)

@app.route("/")
def hello_world():
    food_items = load_from_db()
    return render_template("home.html",food_items=food_items)

@app.route('/inventory')
def list_items():
    food_items = load_from_db()
    return jsonify(food_items)

@app.route('/submit_form', methods=['GET', 'POST'])
def submit_form():
    if request.method == 'GET':
        return render_template('add-inventory.html')
    elif request.method == 'POST':
        form_data = request.json
        name = form_data.get("inputName")
        category = form_data.get("inputCategory")
        quantity = int(form_data.get("inputQuantity"))
        exp_date = form_data.get("inputExpDate")
        supplier_id = form_data.get("inputSupplierID")

        form_data_send = {
            "name" : name,
            "category" : category,
            "quantity" : quantity,
            "exp_date" : exp_date,
            "supplier_id" : supplier_id
        }

        value = insert_into_database(form_data_send)
        if value:
            print("successful")
        else:
            print("error")
        return 'Form Submitted successfully'


@app.route("/<id>")
def show_fruit(id):
    fruit = load_fruit_from_db(id)
    if fruit is None:
        return jsonify({"error": "Fruit not found"}), 404
    else:
        return jsonify(fruit)


@app.route("/request", methods=["GET", "POST"])
def request_form():
    if request.method == "GET":
        return render_template("request.html")
    elif request.method == "POST":
        # Process the form submission here
        pass


if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
