from flask import Flask, flash, redirect, render_template, request, session, url_for
from random import sample
from db_conn import cur

def index():
    if request.method == "POST":
        numOfProducts = request.get_json()["numberOfProducts"]
        res = cur.execute("SELECT * FROM Products;")
        products = res.fetchall()
        randomProducts = sample(products, k=numOfProducts)
        return {"products":randomProducts}
    else:
        return render_template("home.html")
index.methods = ["GET", "POST"]