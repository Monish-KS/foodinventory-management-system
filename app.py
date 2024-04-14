from flask import Flask, render_template,jsonify

app = Flask(__name__)

Date = "2017-09-28 01:67"
data = [
    {
        "Date": "2017-09-28 05:57",
        "Order ID": "200398",
        "Name": "iPhone X 44Gb Grey",
        "Price": "$999.00",
        "Quantity": "1",
        "Total": "$999.00",
    },
    {
        "Date": "2017-09-28 05:57",
        "Order ID": "200397",
        "Name": "Samsung S8 Black",
        "Price": "$756.00",
        "Quantity": "1",
        "Total": "$756.00",
    },
    {
        "Date": "2017-09-26 05:57",
        "Order ID": "200396",
        "Name": "Game Console Controller",
        "Price": "$22.00",
        "Quantity": "2",
        "Total": "$44.00",
    },
    {
        "Date": "2017-09-25 23:06",
        "Order ID": "200392",
        "Name": "USB 3.0 Cable",
        "Price": "$10.00",
        "Quantity": "3",
        "Total": "$30.00",
    },
    {
        "Date": "2017-09-24 05:57",
        "Order ID": "200391",
        "Name": "Smartwatch 4.0 LTE Wifi",
        "Price": "$199.00",
        "Quantity": "6",
        "Total": "$1494.00",
    },
    {
        "Date": "2017-09-23 05:57",
        "Order ID": "200390",
        "Name": "Camera C430W 4k",
        "Price": "$699.00",
        "Quantity": "1",
        "Total": "$699.00",
    },
    {
        "Date": "2017-09-22 05:57",
        "Order ID": "200389",
        "Name": "Macbook Pro Retina 2017",
        "Price": "$2199.00",
        "Quantity": "1",
        "Total": "$2199.00",
    },
    {
        "Date": "2017-09-21 05:57",
        "Order ID": "200388",
        "Name": "Game Console Controller",
        "Price": "$999.00",
        "Quantity": "1",
        "Total": "$999.00",
    },
    {
        "Date": "2017-09-19 05:57",
        "Order ID": "200387",
        "Name": "iPhone X 64Gb Grey",
        "Price": "$999.00",
        "Quantity": "1",
        "Total": "$999.00",
    },
    {
        "Date": "2017-09-18 05:57",
        "Order ID": "200386",
        "Name": "iPhone X 64Gb Grey",
        "Price": "$999.00",
        "Quantity": "1",
        "Total": "$999.00",
    },
    {
        "Date": "2017-09-22 05:57",
        "Order ID": "200389",
        "Name": "Macbook Pro Retina 2017",
        "Price": "$2199.00",
        "Quantity": "1",
        "Total": "$2199.00",
    },
    {
        "Date": "2017-09-21 05:57",
        "Order ID": "200388",
        "Name": "Game Console Controller",
        "Price": "$999.00",
        "Quantity": "1",
        "Total": "$999.00",
    },
    {
        "Date": "2017-09-19 05:57",
        "Order ID": "200387",
        "Name": "iPhone X 64Gb Grey",
        "Price": "$999.00",
        "Quantity": "1",
        "Total": "$999.00",
    },
    {
        "Date": "2017-09-18 05:57",
        "Order ID": "200386",
        "Name": "iPhone X 64Gb Grey",
        "Price": "$999.00",
        "Quantity": "1",
        "Total": "$999.00",
    },
]


@app.route("/")
def hello_world():
    return render_template("home.html",data=data )

@app.route('/inventory')
def list_items():
    return jsonify(data)

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
