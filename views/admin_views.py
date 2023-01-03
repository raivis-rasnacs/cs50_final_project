from flask import Flask, flash, redirect, render_template, request, session, url_for
from db_conn import cur, con
from helpers import allowed_file
from werkzeug.utils import secure_filename
from uuid import uuid4
import os
import sqlite3

def admin():
    if session["user_role"] == 1:
        return render_template("admin.html")
    else:
        flash("You must be admin to view this page")
        return redirect(url_for("index"))

# Responds to fetch with table contents
def admin_data():
    tableName = request.get_json()["selectedTab"].capitalize()
    if tableName == "Products":
        res = cur.execute("SELECT Products.ID, Brand, Model, Products.Description, Name, Price, Image_file FROM Products INNER JOIN Categories ON Categories.id = Products.Category_ID;")
        tableData = res.fetchall()
    else:
        res = cur.execute("SELECT * FROM {}".format(tableName))
        tableData = res.fetchall()
    return {"data":tableData}
admin_data.methods = ["POST", "GET"]

def add_product():
    if request.method == "POST":
        global conn
        brand = request.form["brand"]
        model = request.form["model"]
        description = request.form["description"]
        category = request.form["category"]
        price = request.form["price"]
        image = request.files['image']

        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join('static/images/products/', filename))
        
        sql = ''' INSERT INTO Products(ID,Brand,Model,Description,Category_ID,Price,Image_file)
                    VALUES(?,?,?,?,?,?,?) '''
        
        res = cur.execute("SELECT ID FROM Categories WHERE Name = ?", (category, ))
        category = res.fetchall()[0][0]

        try:
            cur.execute(sql, (
                    str(uuid4()),
                    brand, 
                    model, 
                    description, 
                    category, 
                    price, 
                    filename
            ))
            con.commit()
            flash("Product added!")
            return redirect(url_for("add_product"))
        except sqlite3.Error as e:
            flash("Something went wrong!")
            return redirect(url_for("add_product"))
    else:
        res = cur.execute("SELECT Name FROM Categories;")
        categories = res.fetchall()
        return render_template("new_product.html", categories=categories)
add_product.methods = ["POST", "GET"]