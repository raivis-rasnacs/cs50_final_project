from flask import Flask, flash, redirect, render_template, request, session, url_for
from db_conn import cur

def show_product(id):
    res = cur.execute("SELECT * FROM Products WHERE ID = ?", (id, ))
    product = res.fetchall()
    return render_template("product_page.html", product=product[0])

def filter_products():
    if request.method == "POST":
        selectedCategories = request.get_json()["selectedCategories"]
        productsInCategories = []
        for category in selectedCategories:
            res = cur.execute("SELECT * FROM Products WHERE Category_ID = (SELECT ID FROM Categories WHERE Name = ?)", (category,))
            productsInCategories += res.fetchall()
        return {"products":productsInCategories}
filter_products.methods = ["POST", "GET"]

def all_products():
    if request.method == "POST":
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
        else:
            res = cur.execute("SELECT * FROM Products WHERE Category_id = (SELECT id FROM Categories WHERE Name = ?) ORDER BY Category_ID ASC", (selectedCategory,))
            productsOfCategory = res.fetchall()
        return render_template("products.html", products=productsOfCategory, categories=categories, selectedCategory=selectedCategory)
    else:
        res = cur.execute("SELECT * FROM Products;")
        products = res.fetchall()
        res = cur.execute("SELECT * FROM Categories ORDER BY Name ASC;")
        categories = res.fetchall()
        return render_template("products.html", products=products, categories=categories)
all_products.methods = ["GET", "POST"]