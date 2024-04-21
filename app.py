from flask import Flask, render_template,jsonify,request,redirect, url_for, send_file
from database import load_from_db, load_fruit_from_db,insert_into_database,insert_request_into_database,load_requests_from_db,load_suppliers_from_db, load_user_details,update_request_status_in_db
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from io import BytesIO
from datetime import datetime,date

app = Flask(__name__)


@app.route('/')
def root():
    return redirect(url_for("user_login"))


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
    username = request.args.get('username')
    return render_template("reciever_dashboard.html", requests=requests,username = username)


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


@app.route("/update_request_status", methods=["POST"])
def update_request_status():
    # Retrieve data from the AJAX request
    form_data = request.json
    request_id = form_data.get("request_id")
    action = form_data.get("action")  # 'accept' or 'reject'

    # Update request status in the database
    if action == "accept":
        new_status = "Accepted"
    elif action == "reject":
        new_status = "Rejected"
    else:
        return jsonify({"error": "Invalid action"}), 400

    success = update_request_status_in_db(request_id, new_status)

    if success:
        return jsonify({"success": True})
    else:
        return jsonify({"error": "Failed to update request status"}), 500


@app.route("/generate_report")
def generate_report():
    # Retrieve data from the database
    food_items = load_from_db()

    # Create a new PDF file
    pdf_filename = "report.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=letter)

    # Set title and add a line
    c.setFont("Helvetica-Bold", 14)
    c.drawString(30, 750, "FoodBank Inventory Report")
    c.line(30, 745, 580, 745)  # Draw a line under the title

    # Set table headers
    headers = ["Item ID", "Name", "Category", "Quantity", "Exp Date", "Supplier ID"]
    data = [headers]

    # Populate the table data
    for item in food_items:
        # Convert `ExpDate` to a string if it is a `datetime.date` object
        exp_date_str = (
            item["ExpDate"].strftime("%Y-%m-%d")
            if hasattr(item["ExpDate"], "strftime")
            else str(item["ExpDate"])
        )

        row = [
            item["ItemID"],
            item["Name"],
            item["Category"],
            item["Quantity"],
            exp_date_str,
            item["SupplierID"],
        ]
        data.append(row)

    # Create the table and apply styles
    table = Table(data, colWidths=[80] * len(headers))
    style = TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),  # Header background color
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),  # Header text color
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),  # Center align all columns
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),  # Bold header font
            ("FONTSIZE", (0, 0), (-1, -1), 10),  # Font size
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),  # Padding for headers
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),  # Background color for rows
            ("GRID", (0, 0), (-1, -1), 1, colors.black),  # Add a grid to the table
        ]
    )
    table.setStyle(style)

    # Draw the table on the PDF
    table.wrapOn(c, 580, 680)
    table.drawOn(c, 30, 550)  # Adjust position of the table

    # Save the PDF file
    c.save()

    # Return the PDF file as a file download
    return send_file(pdf_filename, as_attachment=True)


@app.route("/generate_requests_report")
def generate_requests_report():
    # Retrieve requests data from the database
    requests = load_requests_from_db()

    # Create a dictionary to sum quantities for each item
    item_quantities = {}
    for request in requests:
        item_name = request["item_name"]
        quantity = request["quantity"]
        if item_name in item_quantities:
            item_quantities[item_name] += quantity
        else:
            item_quantities[item_name] = quantity

    # Create a new PDF file
    pdf_filename = "requests_report.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=letter)

    # Set title and add a line
    c.setFont("Helvetica-Bold", 14)
    c.drawString(30, 750, "Requests Report")
    c.line(30, 745, 580, 745)  # Draw a line under the title

    # Set table headers
    headers = [
        "Request ID",
        "Requester Name",
        "Request Date",
        "Item ID",
        "Item Name",
        "Quantity",
        "Status",
    ]
    data = [headers]

    # Populate the table data
    for request in requests:
        request_date_str = (
            request["request_date"].strftime("%Y-%m-%d")
            if hasattr(request["request_date"], "strftime")
            else str(request["request_date"])
        )
        row = [
            request["request_id"],
            request["requester_name"],
            request_date_str,
            request["item_id"],
            request["item_name"],
            request["quantity"],
            request["status"],
        ]
        data.append(row)

    # Create the table and apply styles
    table = Table(data, colWidths=[70] * len(headers))
    style = TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),  # Header background color
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),  # Header text color
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),  # Center align all columns
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),  # Bold header font
            ("FONTSIZE", (0, 0), (-1, -1), 10),  # Font size
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),  # Padding for headers
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),  # Background color for rows
            ("GRID", (0, 0), (-1, -1), 1, colors.black),  # Add a grid to the table
        ]
    )
    table.setStyle(style)

    # Draw the table on the PDF
    table.wrapOn(c, 580, 680)
    table.drawOn(c, 30, 550)  # Adjust position of the table

    # Create a pie chart for item quantities using Matplotlib
    # Use the item_quantities dictionary to plot the pie chart
    item_names = list(item_quantities.keys())
    quantities = list(item_quantities.values())

    # Create a figure for the pie chart
    fig, ax = plt.subplots(figsize=(4, 4))  # Smaller figure size

    # Plotting the pie chart
    ax.pie(quantities, labels=item_names, autopct="%1.1f%%")
    ax.set_title("Item Quantities")

    # Save the pie chart as an image
    pie_img_filename = "item_pie_chart.png"
    plt.savefig(pie_img_filename)

    # Add the pie chart image to the PDF below the table
    c.drawImage(
        pie_img_filename, 30, 200, width=300, height=300
    )  # Adjust the width and height as needed

    # Save the PDF file
    c.save()

    # Return the PDF file as a file download
    return send_file(pdf_filename, as_attachment=True)


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
