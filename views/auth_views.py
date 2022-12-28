from flask import Flask, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from db_conn import cur, con
from uuid import uuid4

def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password_check = request.form["password-check"]
        if password != password_check:
            flash("Passwords don't match")
            return redirect(url_for("register"))
        first_name = request.form["first-name"]
        last_name = request.form["last-name"]
        e_mail = request.form["e-mail"]
        phone = request.form["phone"]
        address = request.form["address"]
        newUserSql = ''' INSERT INTO Users(ID,Username,Password,First_name,Last_name,E_mail, Phone, Address, Admin)
                    VALUES(?,?,?,?,?,?,?,?,?) '''
        try:
            cur.execute(newUserSql, (
                        str(uuid4()),
                        username, 
                        generate_password_hash(password), 
                        first_name, 
                        last_name, 
                        e_mail, 
                        phone,
                        address,
                        "0"
                ))
            con.commit()
            flash("Account created successfully!")
            return redirect(url_for("register"))
        except:
            flash("Something went wrong!")
            return redirect(url_for("register"))
    else:
        return render_template("register.html")
register.methods = ["GET", "POST"]


def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        res = cur.execute("SELECT ID, Password, Admin FROM Users WHERE Username = ?", (username, ))
        user = res.fetchall()
        if len(user) > 0:
            if check_password_hash(user[0][1], password):
                session["user_id"] = user[0][0]
                session["user_name"] = username
                session["user_role"] = user[0][2]
                flash("You are logged in")
            else:
                flash("Wrong password")
        else:
            flash("User not found, you are welcome to make a one")
            return redirect(url_for("register"))
        return redirect(url_for("index"))
    else:
        return render_template("login.html")
login.methods = ["GET", "POST"]


def logout():
    del(session["user_id"])
    del(session["user_name"])
    del(session["user_role"])
    flash("You are logged out")
    return redirect(url_for("index"))