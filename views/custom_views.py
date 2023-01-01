from flask import Flask, flash, redirect, render_template, request, session, url_for


def about():
    return render_template("custom.html", 
                            content='''Just a simple e-commerce project for CS50\nBuilt with Flask and Bootstrap''', 
                            title="About")

def payment():
    return render_template("custom.html", 
                            content="Payment and delivery information coming soon...", 
                            title="Payment")

def page_not_found(message):
    return render_template("custom.html", 
                            content=f"Ooops..\nThis page doesn't exist\n{message}", 
                            title="404")