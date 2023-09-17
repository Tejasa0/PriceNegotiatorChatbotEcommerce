import flask
from flask import Flask, render_template, request, jsonify, url_for, session, redirect
import json
import os
from flask_mailing import Mail, Message
# from flask_cores import CORES
# from flask_mysqldb import MySQL
import mysql.connector

from chat import getId

app = Flask(__name__)

app.secret_key = os.urandom(24)

connection = mysql.connector.connect(
    host='btj2pcqnecqmkjo9wygp-mysql.services.clever-cloud.com', database='btj2pcqnecqmkjo9wygp', user='upgildbxgpre1jd9', password='TWufPowuIZATC9n9ZL6B',port="3306"
)
# session['data'] = []

cursor = connection.cursor()
app.config['MAIL_USERNAME'] = "drpmayur@gmail.com"
app.config['MAIL_PASSWORD'] = "iinhxwuupzxdbrkv"
app.config['MAIL_PORT'] = 587
app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['USE_CREDENTIALS'] = True
app.config['VALIDATE_CERTS'] = True
# app.config['MAIL_DEFAULT_SENDER'] = "drpmayur@gmail.com"


mail = Mail(app)
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'Naitro'

# mysql = MySQL(app)
# Executing SQL Statements
# cursor.execute(''' INSERT INTO table_name VALUES(v1,v2...) ''')
# cursor.execute(''' DELETE FROM table_name WHERE condition ''')

# @app.route('/')
# def users():
#     cur = mysql.connection.cursor()
#     cur.execute('''SELECT user, host FROM mysql.user''')
#     rv = cur.fetchall()
#     return str(rv)
id1 = ""


@app.get("/")
def index():
    if 'user_id' in session:
        print(session['user_id'])

        flag = True
        return render_template("index.html", flag=flag, name=session['name'])
    else:
        flag = False
        return render_template("index.html", flag=flag)


# Menu Pages Endpoints STARTS HERE----------------------------------------------------------
@app.get("/about")
def about():
    flag1 = True
    if 'user_id' not in session:
        flag1 = False
    return render_template("about.html", flag=flag1)


@app.route('/send_mail', methods=['POST'])
async def simple_send():
    # Retrieve form data
    # sender_email=request.form['email']

    message = Message(
        # name=request.form['name'],
        # sender=sender_email,
        body=request.form['name'] + "\n" + request.form['email'] + "\n" + request.form['phone'] + "\n" + request.form[
            'text3'],
        subject="Form Submission",
        recipients=["tejaspatila0@gmail.com"]  # List of recipients, as many as you can pass
    )

    await mail.send_message(message)
    return redirect(url_for("contact"))


@app.get("/shop")
def shop():
    flag1 = True
    if 'user_id' not in session:
        flag1 = False
    if 'user_id' in session:

        return render_template("shop.html", name=session['name'], flag=flag1)
    else:
        return redirect('/login')


@app.route('/testimonial')
def testimonial():
    return render_template("testmonial.html")


@app.route('/contact')
def contact():
    flag1 = True
    if 'user_id' not in session:
        flag1 = False
    return render_template("contact.html", flag=flag1)


@app.route('/naitro')
def naitro():
    return render_template("naitro.html")


@app.get('/<string:id>')
def product(id):
    global id1
    id1 = id
    session['pId'] = id
    print(id1)
    print(session['pId'])
    cursor.execute(" Select pName,pDesc,maxPrice from productdetails where pId = '%s' " % id1)
    res = cursor.fetchone()
    if res == None:
        return render_template("index.html")
    connection.commit()
    # img="../static/images/Products/'%s'/'%s'"%id %id
    # cursor.close()

    print(session['user_id'])
    print(session['pId'])
    session.modified = True
    cursor.execute(
        'SELECT * FROM customer_product WHERE EmailId = %s AND pId = %s',
        (session['user_id'], session['pId'],))
    record = cursor.fetchone()
    # cursor.fetchall()
    print(record)
    if record is not None:
        return render_template("products.html", id=session['pId'], pName=res[0], pDesc=res[1], price=res[2],
                               negot_price=record[4], name=session['name'],flag=True)
    else:
        return render_template("products.html", id=session['pId'], pName=res[0], pDesc=res[1], price=res[2],
                               negot_price=res[2], name=session['name'],flag=True)


# Menu Pages Endpoints ENDS HERE----------------------------------------------------------
obj1 = None

# @app.route("/sendId")
# def sendId():
#     id = request.get_json().get('id')
#     global obj1
#     obj1 = getId(id)
#     print(obj1.upper_bound)

flag = 0
id = 0


@app.post("/predict")
def predict():
    global id

    text = request.get_json().get('message')
    # print(text)
    global obj1
    id1 = request.get_json().get('id1')
    if (id != id1):
        obj1 = getId(id1)
        id = id1
    # print(id)

    global flag
    # if flag == 0:
    #     obj1 = getId(id)
    # flag = 1
    response = obj1.get_response(text)
    message = {"answer": response}
    print(session['pId'])
    cursor.execute(
        'SELECT * FROM customer_product WHERE EmailId = %s AND pId = %s', (session['user_id'], session['pId'],))
    record = cursor.fetchone()
    cursor.fetchall()
    if record is not None:
        if record[3] != record[4]:
            message = {"answer": "You have already negotiated"}
            return jsonify(message)
    if obj1.done == 1:
        sql = "INSERT INTO customer_product (pId, EmailId, actual_price, negotiated_price) VALUES (%s, %s,%s,%s)"
        val = (obj1.id, session['user_id'], obj1.max_price, obj1.bot_price)
        cursor.execute(sql, val)
        cursor.fetchall()
        connection.commit()

    return jsonify(message)


# Login and Signup Endpoints STARTS HERE----------------------------------------------------------
@app.route("/signup")
def signup():
    if 'user_id' in session:
        return render_template("index.html")
    session.pop('user_id', None)
    return render_template("signup.html")


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    # Retrieve the product ID from the form data
    product_name = request.form.get('product_name')
    session['pName'] = product_name
    session.modified = True
    cursor.execute(
        'SELECT pId,maxPrice FROM productdetails WHERE pName = %s', (product_name,))
    res = cursor.fetchone()
    # cursor.fetchall()

    cursor1 = connection.cursor()
    cursor1.execute('SELECT negotiated_price FROM customer_product WHERE pId = %s and EmailId=%s',
                    (res[0], session['user_id']))
    res1 = cursor1.fetchone()
    # cursor.fetchall()

    if res1 is not None:
        query = "INSERT INTO cart (userId, productId, price) VALUES (%s, %s, %s)"
        values = (session['user_id'], res[0], res1[0])
        cursor.execute(query, values)
    else:
        query = "INSERT INTO cart (userId, productId, price) VALUES (%s, %s, %s)"
        values = (session['user_id'], res[0], res[1])
        cursor.execute(query, values)

    connection.commit()
    return redirect('/cart')


# import sqlite3


# ...

@app.route('/cart')
def cart():
    flag1 = True
    if 'user_id' not in session:
        flag1 = False
        return redirect('/index')

    cursor.execute('SELECT productId,price,cartId from cart where userId=%s', (session['user_id'],))
    # cursor.execute(query)
    cart_items = cursor.fetchall()

    products = []
    total = 0
    for producti in cart_items:
        cursor.execute('SELECT pName from productdetails where pId=%s', (producti[0],))
        pName = cursor.fetchone()
        # cursor.fetchall()
        product = {
            'id': producti[0],
            'name': pName,
            'price': producti[1],
            'cartId': producti[2]
        }
        total = total + int(producti[1])
        products.append(product)

    # Close the database connection
    connection.commit()

    # Render the cart page template with the product details
    return render_template('cart.html', products=products, total_amount=total, name1=session['name'], flag=flag1)


@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    cartId = request.form.get('cartId')
    query = "DELETE FROM cart WHERE cartId = %s"
    values = (cartId,)
    cursor.execute(query, values)
    connection.commit()

    return redirect('/cart')


@app.route('/empty')
def empty_cart():
    try:
        session.clear()
        return redirect(url_for('.products'))
    except Exception as e:
        print(e)


@app.route("/registered")
def registered():
    if len(session) != 0:
        return render_template("registered.html")
    return render_template("registered.html", var="Login First")


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST':
        fn = request.form['fn']
        ln = request.form['ln']
        mn = request.form['mn']
        mi = request.form['mi']
        pd = request.form['pd']
        cd = request.form['cd']
        if pd != cd:
            return render_template('signup.html', msg="Password and confirm password is different..")
        sql = "INSERT INTO customer_signup (FirstName, LastName, MobileNo, EmailId, Pwd) VALUES (%s, %s,%s ,%s, %s)"
        val = (fn, ln, mn, mi, pd)
        try:
            cursor.execute(sql, val)
            cursor.fetchall()
            connection.commit()

            return render_template('login.html', var="You have successfully registered...")
        except:
            cursor.fetchall()
            connection.commit()
            return render_template('signup.html',
                                   var="Account with given mobile already exists.Try with another mobile...")


@app.route('/logged')
def logged():
    # flag = False
    if 'user_id' in session:
        # flag=True
        return redirect(url_for("index"))
    return render_template("signup.html", var="Login First")


@app.get('/myfunc')
def myfunc():
    id = request.args.get('id')
    val = '/' + id
    print(val)
    if 'user_id' in session:
        print("In shop")
        return redirect(val)
    return redirect(url_for("index"))


@app.route('/login')
def login():
    if 'user_id' in session:
        return redirect(url_for("index"))
    return render_template("login.html", var="Login First")


@app.route('/login_validation', methods=['GET', 'POST'])
def login_validation():
    if request.method == 'POST':
        mn = request.form['mn1']
        pd = request.form['pd1']
        cursor.execute(
            'SELECT * FROM customer_signup WHERE EmailId = %s AND Pwd = %s', (mn, pd,))
        record = cursor.fetchall()
        if len(record) > 0:
            session['user_id'] = record[0][3]
            session['cart'] = []
            session['name'] = record[0][0] + " " + record[0][1]
            session.modified = True
            return redirect(url_for('index'))
    return render_template('login.html', var='Incorrect username / password !')


@app.route('/logout')
def logout():
    if 'user_id' in session:
        session.pop('user_id')
        session.pop('cart')
        session.modified = True
        session.pop('name')
        session.pop('pId')
        return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


# Login and Signup Endpoints END HERE----------------------------------------------------------


if __name__ == "__main__":
    app.run(debug=True)
