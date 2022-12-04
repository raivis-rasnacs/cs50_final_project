from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlite3 import connect

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Connect db
con = connect("data.db", check_same_thread=False)
cur = con.cursor()

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/filter", methods = ['GET', 'POST'])
def filter_products():
    if request.method == "POST":
        res = cur.execute("SELECT * FROM Categories;")
        categories = res.fetchall()
        selectedCategories = request.get_json()["selectedCategories"]
        productsInCategories = []
        for category in selectedCategories:
            res = cur.execute("SELECT * FROM Products WHERE Category_ID = (SELECT ID FROM Categories WHERE Name = ?)", (category,))
            productsInCategories += res.fetchall()
        return {"products":productsInCategories}

@app.route("/", methods = ['GET', 'POST'])
def index():
    if request.method == "GET":
        res = cur.execute("SELECT * FROM Products ORDER BY Price;")
        products = res.fetchall()
        res = cur.execute("SELECT * FROM Categories;")
        categories = res.fetchall()
        return render_template("index.html", products=products, categories=categories)

    elif request.method == "POST":
        selectedCategory = request.form.get("categoryFilter")
        order = request.form.get("order")
        res = cur.execute("SELECT * FROM Categories;")
        categories = res.fetchall()
        print(selectedCategory, order)
        if order is not None:
            if order == "toLowest":
                res = cur.execute("SELECT * FROM Products WHERE Category_id = (SELECT id FROM Categories WHERE Name = ?)", (selectedCategory,))
            else:
                res = cur.execute("SELECT * FROM Products WHERE Category_id = (SELECT id FROM Categories WHERE Name = ?) ORDER BY Price ASC", (selectedCategory,))
            productsOfCategory = res.fetchall()
            print(productsOfCategory)
            return render_template("index.html", products=productsOfCategory, categories=categories, selectedCategory=selectedCategory)
        else:
            res = cur.execute("SELECT * FROM Products WHERE Category_id = (SELECT id FROM Categories WHERE Name = ?)", (selectedCategory,))
            productsOfCategory = res.fetchall()
            return render_template("index.html", products=productsOfCategory, categories=categories, selectedCategory=selectedCategory)

if __name__ == "__main__":
    app.run(debug=True)