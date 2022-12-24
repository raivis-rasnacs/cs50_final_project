from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from sqlite3 import connect
from random import sample
import sqlite3
import os

# Configure application
UPLOAD_FOLDER = "/static/images/products"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__,
            static_url_path="/static",
            static_folder="static")
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

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

# Responds to fetch with table contents
@app.route("/admin/view_data", methods = ['GET', 'POST'])
def admin_data():
    tableName = request.get_json()["selectedTab"].capitalize()
    if tableName == "Products":
        res = cur.execute("SELECT Products.ID, Brand, Model, Products.Description, Name, Price, Image_file FROM Products INNER JOIN Categories ON Categories.id = Products.Category_ID;")
        tableData = res.fetchall()
        print(tableData)
    else:
        res = cur.execute("SELECT * FROM {}".format(tableName))
        tableData = res.fetchall()
    return {"data":tableData}

@app.route("/admin/new_product", methods = ['GET', 'POST'])
def add_product():
    if request.method == "POST":
        global conn
        productData = request.get_json()["productData"]
        print(request.files)
        #if request.files:
        #    image = request.files["image"]
        #    filename = secure_filename(image.filename)
        #    image.save(os.path.join(app.config[UPLOAD_FOLDER], filename))
        
        sql = ''' INSERT INTO Products(Brand,Model,Description,Category_ID,Price,Image_file)
                    VALUES(?,?,?,?,?,?) '''
        
        if not "Image_file" in productData: productData["Image_file"] = "no-photo.jpg" 
        print(productData["Category"])
        
        res = cur.execute("SELECT ID FROM Categories WHERE Name = ?", (productData["Category"], ))
        category = res.fetchall()[0]

        try:
            cur.execute(sql, (
                    productData["Brand"], 
                    productData["Model"], 
                    productData["Description"], 
                    category[0], 
                    productData["Price"], 
                    productData["Image_file"]
            ))
            con.commit()
            return {"message":"Product added!"}
        except sqlite3.Error as e:
            print(e)
            return {"message":"Kļūda!"}
    else:
        res = cur.execute("SELECT Name FROM Categories;")
        categories = res.fetchall()
        print("hop")
        return render_template("new_product.html", categories=categories)

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