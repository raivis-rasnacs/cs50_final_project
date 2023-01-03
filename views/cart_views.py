from flask import Flask, flash, redirect, render_template, request, session, url_for
from db_conn import cur, con
from uuid import uuid4
from helpers import logged_in, set_cart_size_badge

def add_to_cart(id):
    if not logged_in():
        flash("You must be logged in to use cart")
        return redirect(url_for("show_product", id=id))

    # Checks if user has cart already
    res = cur.execute("SELECT ID FROM Carts WHERE Customer_ID = ?", (session["user_id"], ))
    cart = res.fetchall()
    if len(cart) == 0:
        cart_id = new_cart(session["user_id"])
    else:
        cart_id = cart[0][0]

    try:
        sql = 'INSERT INTO Cart_items(ID,Product_ID,Cart_ID) VALUES(?,?,?)'
        cur.execute(sql, (str(uuid4()), id, cart_id))
        con.commit()
        set_cart_size_badge()
        flash("Product added to your cart")
        return redirect(url_for("show_product", id=id))
    except:
        flash("Something went wrong")
        return redirect(url_for("show_product", id=id))


# Assistant function for add_to_cart
def new_cart(user_id):
    sql = 'INSERT INTO Carts(ID,Customer_ID) VALUES(?,?)'
    cart_id = str(uuid4())
    cur.execute(sql, (cart_id, user_id))
    con.commit()
    return cart_id


def view_cart():
    res = cur.execute('''SELECT Products.Brand, Products.Model, COUNT(*) 
                        FROM Cart_items 
                        JOIN Products ON Products.ID = Cart_items.Product_ID
                        WHERE Cart_ID = (SELECT ID FROM Carts WHERE Customer_ID = ?) 
                        GROUP BY Products.ID''', 
                        (session["user_id"], ))
    items = res.fetchall()
    return render_template("cart.html", items=items)


def clear_cart():
    sql = 'DELETE FROM Cart_items WHERE Cart_ID = (SELECT ID FROM Carts WHERE Customer_ID = ?)'
    cur.execute(sql, (session["user_id"], ))
    con.commit()
    set_cart_size_badge()
    return redirect(url_for("view_cart"))


