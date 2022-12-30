from flask import Flask, flash, redirect, render_template, request, session, url_for
from db_conn import cur

def show_product(id):
    res = cur.execute("SELECT * FROM Products WHERE ID = ?", (id, ))
    product = res.fetchall()
    return render_template("product_page.html", product=product[0])

def filter_products():
    if request.method == "POST":
        selectedCategories = request.get_json()["selectedCategories"]
        order = request.get_json()["sortingOrder"]
        if order == "asc":
            res = cur.execute('SELECT * FROM Products WHERE Category_ID IN (SELECT ID FROM Categories WHERE Name IN (%s)) ORDER BY Price ASC' % ("?," * len(selectedCategories))[:-1], selectedCategories)
        else:
            res = cur.execute('SELECT * FROM Products WHERE Category_ID IN (SELECT ID FROM Categories WHERE Name IN (%s)) ORDER BY Price DESC' % ("?," * len(selectedCategories))[:-1], selectedCategories)
        products = res.fetchall()
        return {"products":products}
    else:
        res = cur.execute("SELECT Name FROM Categories ORDER BY Name ASC;")
        categories = res.fetchall()
        return render_template("products.html", categories=categories)
filter_products.methods = ["POST", "GET"]