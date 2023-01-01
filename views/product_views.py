from flask import Flask, flash, redirect, render_template, request, session, url_for
from db_conn import cur

def show_product(id):
    res = cur.execute("SELECT * FROM Products WHERE ID = ?", (id, ))
    product = res.fetchall()
    return render_template("product_page.html", product=product[0])

def filter_products(search_param = ""):
    if request.method == "POST":
        selectedCategories = request.get_json()["selectedCategories"]
        order = request.get_json()["sortingOrder"]
        searchParam = request.get_json()["searchParameter"]
        if searchParam != None:
            res = cur.execute("SELECT * FROM Products WHERE Brand LIKE ? OR Model LIKE ? OR Description LIKE ? ORDER BY Price ASC", ("%"+searchParam+"%", "%"+searchParam+"%", "%"+searchParam+"%", ))
        elif order == "asc":
            res = cur.execute("SELECT * FROM Products WHERE Category_ID IN (SELECT ID FROM Categories WHERE Name IN (%s)) ORDER BY Price ASC" % ("?," * len(selectedCategories))[:-1], selectedCategories)
        else:
            res = cur.execute("SELECT * FROM Products WHERE Category_ID IN (SELECT ID FROM Categories WHERE Name IN (%s)) ORDER BY Price DESC" % ("?," * len(selectedCategories))[:-1], selectedCategories)
        products = res.fetchall()
        return {"products":products}
    else:
        if search_param:
            res = cur.execute("SELECT Name FROM Categories ORDER BY Name ASC;")
            categories = res.fetchall()
        res = cur.execute("SELECT Name FROM Categories ORDER BY Name ASC;")
        categories = res.fetchall()

        # Gets highest price for filter
        res = cur.execute("SELECT MAX(Price) FROM Products;")
        highestPrice = res.fetchall()

        return render_template("products.html", categories=categories, search_param=search_param, highestPrice=highestPrice)
filter_products.methods = ["POST", "GET"]