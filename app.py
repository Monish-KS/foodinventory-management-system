from flask import Flask, render_template,jsonify,request,redirect, url_for
from database import load_from_db, load_fruit_from_db,insert_into_database,insert_request_into_database,load_requests_from_db,load_suppliers_from_db, load_user_details

app = Flask(__name__)

@app.route("/admin")
def admin():
    food_items = load_from_db()
    username = request.args.get('username')
    requests = load_requests_from_db()
    return render_template("admin_dashboard.html",food_items=food_items,requests = requests,username = username)

@app.route('/inventory')
def list_items():
    food_items = load_from_db()
    return jsonify(food_items)

@app.route('/get_suppliers')
def list_suppliers():
    suppliers = load_suppliers_from_db()
    return jsonify(suppliers)

@app.route("/submit_form", methods=["GET", "POST"])
def submit_form():
    if request.method == "GET":
        return render_template("add-inventory.html")
    elif request.method == "POST":
        form_data = request.json
        name = form_data.get("inputName")
        category = form_data.get("inputCategory")
        quantity_str = form_data.get("inputQuantity")  # Get quantity as string
        exp_date = form_data.get("inputExpDate")
        supplier_id = form_data.get("inputSupplierID")

        # Check if quantity is provided
        if quantity_str is None or not quantity_str.strip():
            print("Quantity is required")
            return "Error: Quantity is required"

        # Convert quantity to integer
        try:
            quantity = int(quantity_str)
        except ValueError:
            print("Invalid quantity")
            return "Error: Invalid quantity"

        form_data_send = {
            "name": name,
            "category": category,
            "quantity": quantity,
            "exp_date": exp_date,
            "supplier_id": supplier_id,
        }

        value = insert_into_database(form_data_send)
        if value:
            print("successful")
        else:
            print("error")
        return "Form Submitted successfully"

@app.route("/supply", methods=["GET", "POST"])
def submit_supplier_form():
    if request.method == "GET":
        username = request.args.get('username')
        return render_template("supplier_dashboard.html",username = username)
    elif request.method == "POST":
        form_data = request.json
        name = form_data.get("inputName")
        category = form_data.get("inputCategory")
        quantity_str = form_data.get("inputQuantity")  # Get quantity as string
        exp_date = form_data.get("inputExpDate")
        supplier_id = form_data.get("inputSupplierID")

        # Check if quantity is provided
        if quantity_str is None or not quantity_str.strip():
            print("Quantity is required")
            return "Error: Quantity is required"

        # Convert quantity to integer
        try:
            quantity = int(quantity_str)
        except ValueError:
            print("Invalid quantity")
            return "Error: Invalid quantity"

        form_data_send = {
            "name": name,
            "category": category,
            "quantity": quantity,
            "exp_date": exp_date,
            "supplier_id": supplier_id,
        }

        value = insert_into_database(form_data_send)
        if value:
            print("successful")
        else:
            print("error")
        return "Form Submitted successfully"


@app.route("/<id>")
def show_fruit(id):
    fruit = load_fruit_from_db(id)
    if fruit is None:
        return jsonify({"error": "Fruit not found"}), 404
    else:
        return jsonify(fruit)

@app.route('/request_page')
def show_request():
    requests = load_requests_from_db()
    return render_template("Reciever_dashboard.html", requests=requests)


@app.route("/request_form", methods=["GET", "POST"])
def request_form():
    if request.method == "GET":
        # Load data needed for the form, such as inventory items
        food_items = load_from_db()
        username = request.args.get('username')
        return render_template("request.html", food_items=food_items, username = username)
    elif request.method == "POST":
        # Get form data
        form_data = request.json
        print(form_data)
        requester_name = form_data.get("requesterName")
        request_date = form_data.get("requestDate")
        item_id = form_data.get("itemID")
        item_name = form_data.get("itemName")
        quantity_str = form_data.get("quantity")
        print(requester_name)
        if quantity_str is None or not quantity_str.strip():
            print("Quantity is required")
            return "Error: Quantity is required"

        # Convert quantity to integer
        try:
            quantity = int(quantity_str)
        except ValueError:
            print("Invalid quantity")
            return "Error: Invalid quantity"


        # Prepare data to insert into the request database
        request_data = {
            "requester_name": requester_name,
            "request_date": request_date,
            "item_id": item_id,
            "item_name": item_name,
            "quantity": quantity,
            "status": "pending",  # Set status to "pending"
        }

        # Insert data into the request database
        success = insert_request_into_database(request_data)

        if success:
            return "Request submitted successfully"
        else:
            return "Error submitting request"

@app.route('/login', methods = ['GET','POST'])
def user_login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        # Retrieve form data from the JSON request body
        form_data = request.json
        email = form_data.get("email")
        password = form_data.get("password")
        print(email, password)
        # Load user details from the database using the email
        user_details = load_user_details(email)
        username = user_details['username']
        print(user_details)
        if user_details is not None:
            # Check if the provided password matches the password from the database
            if password == user_details["Password"]:
                # Determine the user type and render the appropriate template
                user_type = user_details["UserType"]

            if user_type == 'admin':
                redirect_url = url_for('admin', username=username)
            elif user_type == 'supplier':
                redirect_url = url_for('submit_supplier_form', username=username)
            elif user_type == 'receiver':
                redirect_url = url_for('request_page', username=username)
            if redirect_url:
                return jsonify({"success": True, "redirectUrl": redirect_url, "username" : user_details['username']})
            else:
                # Unknown user type, return an error response
                return jsonify({"error": "Unknown user type"}), 400

        else:
            # User not found, return an error response
            return jsonify({"error": "User not found"}), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
