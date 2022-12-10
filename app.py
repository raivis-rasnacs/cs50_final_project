from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlite3 import connect
from random import sample

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

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/admin/data", methods = ['GET', 'POST'])
def admin_data():
    tableName = request.get_json()["selectedTab"].capitalize()
    res = cur.execute("SELECT * FROM {}".format(tableName))
    tableData = res.fetchall()
    print(tableData)
    return {"data":tableData}

@app.route("/products/<id>")
def show_product(id):
    res = cur.execute("SELECT * FROM Products WHERE id = ?", (id[1:-1], ))
    product = res.fetchall()
    print(product)
    return render_template("product_page.html", product=product[0])

@app.route("/", methods = ['GET', 'POST'])
def home():
    if request.method == "POST":
        numOfProducts = request.get_json()["numberOfProducts"]
        res = cur.execute("SELECT * FROM Products;")
        products = res.fetchall()
        randomProducts = sample(products, k=numOfProducts)
        print(randomProducts)
        return {"products":randomProducts}
    else:
        return render_template("home.html")

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

@app.route("/products", methods = ['GET', 'POST'])
def index():
    if request.method == "GET":
        res = cur.execute("SELECT * FROM Products ORDER BY Price;")
        products = res.fetchall()
        res = cur.execute("SELECT * FROM Categories;")
        categories = res.fetchall()
        return render_template("products.html", products=products, categories=categories)

    elif request.method == "POST":
        selectedCategory = request.form.get("categoryFilter")
        order = request.form.get("order")
        res = cur.execute("SELECT * FROM Categories;")
        categories = res.fetchall()
        if order is not None:
            if order == "toLowest":
                res = cur.execute("SELECT * FROM Products WHERE Category_id = (SELECT id FROM Categories WHERE Name = ?)", (selectedCategory,))
            else:
                res = cur.execute("SELECT * FROM Products WHERE Category_id = (SELECT id FROM Categories WHERE Name = ?) ORDER BY Price ASC", (selectedCategory,))
            productsOfCategory = res.fetchall()
            print(productsOfCategory)
            #return render_template("products.html", products=productsOfCategory, categories=categories, selectedCategory=selectedCategory)
        else:
            res = cur.execute("SELECT * FROM Products WHERE Category_id = (SELECT id FROM Categories WHERE Name = ?)", (selectedCategory,))
            productsOfCategory = res.fetchall()
        return render_template("products.html", products=productsOfCategory, categories=categories, selectedCategory=selectedCategory)

if __name__ == "__main__":
    app.run(debug=True)