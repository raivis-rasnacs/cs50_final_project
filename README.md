# CS50 Final Project : Daddy's Tools
#### VIDEO DEMO: [Link here](https://youtu.be/X3gpctG2OLI)
#### DESCRIPTION:

I made e-commerce store called "Daddy's Tools". 
It's built with Python Flask, Bootstrap, SQLite and JavaScript.

Database contains following tables:
* Users
* Products
* Carts
* Cart_items
* Orders
* Order_items
* Delivery_options

Project contains following:
* Main page that shows 3 random products
* Products page that shows all products divided into pages
* Cart functionality
* Order functionality
* Simple Admin panel with ability to add product and upload picture

Project folder contains sub-folders:
* 'templates' with all necessary html files for products page, home page, admin page etc.
* 'static' folder
    * css sub-folder includes several css files
        * admin_styles.css - styling for admin page (not shown in video)
        * form_styles - custom styling for forms in pages 'Register', 'Login', 'New order'
        * home_styles - styling for main page
        * styles.css - several css selectors for general layout, many helper selectors for padding, margins, colors etc.
    * js sub-folder includes files
        * bannerFetch.js - asks server for 3 random products and renders them on the home page
        * fetchTabs.js - this asks server for data in SQLite tables and renders that data in tables (not shown in video)
        * filterFetch.js - project's brains. This drives the products page. All filtering, sorting and products catalogue.
        * saveProduct.js - this is for admin page. Sends info and uploaded image file to server.
        * tabs.js - just a helper script for tabs interface in admin page (not shown in video)
    * images sub-folder includes page logo and all pictures for products
* view folder
    * admin_views.py - routes for admin page
    * auth_views.py - routes for login and register
    * cart_views.py - routes for cart functionality
    * custom_views.py - routes for pages 'about' and 'delivery', also custom error page
    * index_views.py - routes for main page
    * order_views.py - routes for order functionality
    * products_views.py - routes for showing products, adding products, filtering products
* .flaskenv includes some environment values for flask
* data.db is SQLite database file
* app.py is main file
* db_conn.py includes connection to sqlite
* helpers.py includes some helper functions like file type checker for image upload, authentication helper function and cart badge setter function
* requirements.txt includes required libraries

Project made in Latvia.
Author: Raivis Rasnačs
