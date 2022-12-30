from flask import session
from db_conn import con, cur

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def logged_in():
    if "user_id" in session:
        return True
    else:
        return False


def set_cart_size_badge():
    res = cur.execute('''SELECT COUNT(*) 
                        FROM Cart_items 
                        WHERE Cart_ID = (SELECT ID FROM Carts WHERE Customer_ID = ?)''', 
                        (session["user_id"], ))
    session["user_cart_size"] = res.fetchall()[0][0]