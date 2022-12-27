from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from random import sample
from views import index_views, admin_views, product_views
import db_conn
import os

# Configure application
UPLOAD_FOLDER = "static/images/products/"

app = Flask(__name__,
            static_url_path="/static",
            static_folder="static")
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
app.add_url_rule('/products', view_func=product_views.all_products)
app.add_url_rule('/products/<id>', view_func=product_views.show_product)
app.add_url_rule('/products/filter', view_func=product_views.filter_products)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

if __name__ == "__main__":
    app.run(debug=True)