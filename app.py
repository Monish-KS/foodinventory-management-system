from flask import Flask, render_template,jsonify
from database import load_from_db

app = Flask(__name__)

@app.route("/")
def hello_world():
    food_items = load_from_db()
    return render_template("home.html",food_items=food_items)

@app.route('/inventory')
def list_items():
    food_items = load_from_db()
    return jsonify(food_items)

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
