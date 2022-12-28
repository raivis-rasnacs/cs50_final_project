from flask import Flask, flash, redirect, render_template, request, session, url_for


def about():
    return render_template("custom.html", 
                            content="Just a simple Flask project for CS50", 
                            title="About")

def payment():
    return render_template("custom.html", 
                            content="Payment and delivery information coming soon...", 
                            title="Payment")