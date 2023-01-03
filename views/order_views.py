from flask import Flask, flash, redirect, render_template, request, session, url_for
from db_conn import cur, con
from uuid import uuid4
from helpers import logged_in, set_cart_size_badge
from datetime import datetime
from random import randrange as rnd

def new_order():
    res = cur.execute('''SELECT COUNT(*) 
                        FROM Cart_items 
                        JOIN Products ON Products.ID = Cart_items.Product_ID
                        WHERE Cart_ID = (SELECT ID FROM Carts WHERE Customer_ID = ?) ORDER BY Products.Brand''', 
                        (session["user_id"], ))
    itemCount = res.fetchall()[0][0]
    if itemCount == 0:
        flash("You don't have any items in cart")
        return redirect(url_for("view_cart"))
    res = cur.execute("SELECT * FROM Delivery_options")
    deliveryOptions = res.fetchall()
    res = cur.execute("SELECT * FROM Users WHERE ID = ?", (session["user_id"], ))
    user = res.fetchall()[0]
    print(user)
    return render_template("new_order.html", deliveryOptions=deliveryOptions, userInfo=user)


def place_order():
    # Makes new order
    if request.method == "POST":
        try:
            delivery = request.form["delivery-type"]
            sql = 'INSERT INTO Orders(ID, Customer_ID, Order_date, Delivery_type_ID) VALUES(?, ?, ?, ?)'
            order_id = "".join([str(rnd(0, 10)) for _ in range(8)])
            cur.execute(sql, (order_id,
                            session["user_id"],
                            datetime.now().strftime("%Y/%m/%d %H:%M"),
                            delivery, ))
            con.commit()

            res = cur.execute('''SELECT Products.ID 
                                FROM Cart_items 
                                JOIN Products ON Products.ID = Cart_items.Product_ID
                                WHERE Cart_ID = (SELECT ID FROM Carts WHERE Customer_ID = ?) ORDER BY Products.Brand''', 
                                (session["user_id"], ))
            cart_items = res.fetchall()
            for item in cart_items:
                sql = 'INSERT INTO Ordered_items(ID, Product_ID, Order_ID) VALUES(?, ?, ?)'
                cur.execute(sql, (str(uuid4()),
                                item[0],
                                str(order_id), ))
                con.commit()

            flash("Order submitted")
        except:
            flash("Something went wrong")
        return redirect(url_for("clear_cart"))
place_order.methods = ["GET", "POST"]


def view_orders():
    res = cur.execute('''SELECT Orders.ID, Orders.Order_date, Delivery_options.Company 
                         FROM Orders 
                         JOIN Delivery_options ON Delivery_options.ID = Orders.Delivery_type_ID 
                         WHERE Customer_ID = ?''', 
                         (session["user_id"], ))
    orders = res.fetchall()
    return render_template("orders.html", orders=orders)


def show_order(id):
    res = cur.execute('''SELECT Products.Brand, Products.Model, Products.Price 
                         FROM Products 
                         JOIN Ordered_items ON Ordered_items.Product_ID = Products.ID 
                         WHERE Order_ID = ?''', (id, ))
    items = res.fetchall()
    print(items)
    return render_template("order_items.html", id=id, items=items)


def clear_orders():
    res = cur.execute("SELECT ID FROM Orders WHERE Customer_ID = ?", (session["user_id"], ))
    orders = res.fetchall()
    orders = [order[0] for order in orders]
    try:
        for order in orders:
            cur.execute("DELETE FROM Ordered_items WHERE Order_ID = ?", (order, ))
            con.commit()
            cur.execute("DELETE FROM Orders WHERE ID = ?", (order, ))
            con.commit()
        flash("All history cleared")
    except:
        flash("Something went wrong")
    return redirect(url_for("view_orders"))
