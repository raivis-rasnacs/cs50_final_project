from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from random import sample
from views import index_views, admin_views, product_views, auth_views, custom_views, cart_views, order_views
import db_conn
import os

# Configure application
UPLOAD_FOLDER = "static/images/products/"

app = Flask(__name__,
            static_url_path="/static",
            static_folder="static")
app.register_error_handler(404, custom_views.page_not_found)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
 
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

"""URL Maps"""
# Index views
app.add_url_rule('/', view_func=index_views.index)

# Admin
app.add_url_rule('/admin', view_func=admin_views.admin)
app.add_url_rule('/admin/view_data', view_func=admin_views.admin_data)
app.add_url_rule('/admin/new_product', view_func=admin_views.add_product)

# Products
app.add_url_rule('/products/<id>', view_func=product_views.show_product)
app.add_url_rule('/products', view_func=product_views.filter_products)
app.add_url_rule('/products/search/<search_param>', view_func=product_views.filter_products)

# Auth views
app.add_url_rule('/register', view_func=auth_views.register)
app.add_url_rule('/login', view_func=auth_views.login)
app.add_url_rule('/logout', view_func=auth_views.logout)

# Cart views
app.add_url_rule('/add_to_cart/<id>', view_func=cart_views.add_to_cart)
app.add_url_rule('/view_cart', view_func=cart_views.view_cart)
app.add_url_rule('/clear_cart', view_func=cart_views.clear_cart)

# Order views
app.add_url_rule('/new_order', view_func=order_views.new_order)
app.add_url_rule('/place_order', view_func=order_views.place_order)
app.add_url_rule('/orders', view_func=order_views.view_orders)
app.add_url_rule('/orders/<id>', view_func=order_views.show_order)
app.add_url_rule('/clear_orders', view_func=order_views.clear_orders)

# Custom views
app.add_url_rule('/about', view_func=custom_views.about)
app.add_url_rule('/payment', view_func=custom_views.payment)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

if __name__ == "__main__":
    app.run(debug=True)