import os
from cs50 import SQL
from datetime import date
import psycopg2
from flask import Flask, render_template, request, redirect, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps


# app for Flask
app = Flask(__name__)

# setting a database
db = SQL(db = SQL(os.environ.get("DATABASE_URL"))

# for dates for db
now = date.today()

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        rows = db.execute("SELECT * FROM users WHERE username = :username", username=username)

        if len(rows) != 1 or not check_password_hash(rows[0]["pass"], password):
            return render_template ("incorrect.html")
        else:
            # Remember which user has logged in
            session["user_id"] = rows[0]["id"]

            # Redirect user to home page
            return redirect("/")

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/reg", methods=["GET", "POST"])
def reg():
    """Register user"""

    # if USER is refistering then do the fololowing
    if request.method == "POST":

        # inserting into db the user info
        result = db.execute("INSERT INTO users (username, pass) VALUES (:username, :passs)",
                            username=request.form.get("username"), passs=generate_password_hash(request.form.get("password")))

        # if we can't do that it means a user already exists with same name
        if not result:
            return ("This username is taken")
        # if success then remember the user
        else:
            # Remember which user has logged in
            session["user_id"] = result

            # and redirect the user to the main page
            return redirect("/")

    # if method = GET then just show the page
    else:
        return render_template("reg.html")
# ! ! ! ! ! ! ! ! !! ! ! ! ! ! ! ! ! ! !! ! ! ! ! ! ! ! ! ! !! ! ! ! ! ! ! ! ! ! !! ! ! ! ! ! ! ! ! ! !! !

# index page
@app.route("/")
@login_required
def index():
    return render_template ("index.html")

# register page
@app.route("/register", methods=["GET", "POST"])
@login_required
def register():
    if request.method == "POST":

        # getting all info from register form to store in db
        order = int(request.form.get("order"))
        first = request.form.get("first").upper()
        last = request.form.get("last").upper()
        phone = request.form.get("phone")
        brand = request.form.get("brand").upper()
        serial = request.form.get("serial").upper()
        services = request.form.get("services").upper()
        price = round((float(request.form.get("price"))), 2)

        # uploading all inf into db
        db.execute("INSERT INTO orders (order_num, first, last, phone, brand, serial, services, price, d_in, status) VALUES (:order_num, :first, :last, :phone, :brand, :serial, :services, :price, :d, :status)",
                   order_num=order, first=first, last=last, phone=phone, brand=brand, serial=serial, services=services, price=price, d=now, status="IN STORE")

        phone = "(" + phone[:3] + ") " + phone[3:6] + "-" + phone[6:]

        # redirect to "registered" page
        return render_template("registered.html",
                                order=order, first=first, last=last, phone=phone, brand=brand, serial=serial, services=services, price=price)

    else:
        # if "get" then just a form
        return render_template("register.html")


# find page
@app.route("/find", methods=["GET", "POST"])
@login_required
def find():
    if request.method == "POST":

        # if user is looking for an order by order number:
        if request.form.get("order"):
            rows = db.execute("SELECT * FROM orders WHERE order_num=:order", order=request.form.get("order"))
            rows = phonenumber(rows)
            rows = dateformat(rows)

            # if nothing came back - then just tell them
            if not rows:
                return render_template("notfound.html")
            # else tell show them info
            else:
                return render_template("found.html", orders = rows)

        # if user is looking for an order by lastname - give them all possible combinations:
        if request.form.get("last"):
            find = str(request.form.get("last"))
            rows = db.execute("SELECT * FROM orders WHERE last ~* :find", find=find)
            rows = phonenumber(rows)
            rows = dateformat(rows)


            # if nothing came back - then just tell them
            if not rows:
                return render_template("notfound.html")

            # if some came back that show them
            else:
                return render_template("found.html", orders = rows)

        # if user is looking for an order by phone number:
        if request.form.get("phone"):
            phone = str(request.form.get("phone"))
            rows = db.execute("SELECT * FROM orders WHERE phone ~* :phone", phone=phone)
            rows = phonenumber(rows)
            rows = dateformat(rows)

            # if nothing came back - then just tell them
            if not rows:
                return render_template("notfound.html")
            # show if found
            else:
                return render_template("found.html", orders=rows)


        # if user is looking for an order by phone number:
        if request.form.get("d_in"):
            d_in = request.form.get("d_in")
            rows = db.execute("SELECT * FROM orders WHERE d_in =:d_in", d_in=d_in)
            rows = phonenumber(rows)
            rows = dateformat(rows)

            # if nothing came back - then just tell them
            if not rows:
                return render_template("notfound.html")
            # show if found
            else:
                return render_template("found.html", orders=rows)


    else:

        # get ruquest is handled here:
        return render_template("find.html")


# this executes if a user chose a job
@app.route("/found", methods=["GET", "POST"])
@login_required
def reteditdelete():
    if request.method == "POST":

        # RETURNING
        if request.form.get("result"):
            jobtoreturn = request.form.get("result")
            rows = db.execute("SELECT * FROM orders WHERE id=:idd", idd=jobtoreturn)
            if not rows:
                return render_template("notfound.html")
            else:
                db.execute("UPDATE orders SET status=:status, out=:out WHERE id=:idd",
                            status="OUT OF STORE", out=now, idd=jobtoreturn)
                rows = db.execute("SELECT * FROM orders WHERE id=:idd", idd=jobtoreturn)
                rows = phonenumber(rows)
                row = dateformat(rows)
                return render_template("updated.html", orders=rows)

        # EDITITNG
        elif request.form.get("resulte"):
            jobtoedit = request.form.get("resulte")
            rows = db.execute("SELECT * FROM orders WHERE id=:idd", idd=jobtoedit)
            # if nothing came back - then just tell them
            if not rows:
                return render_template("notfound.html")
            # get that info - just values
            else:
                idd = rows[0]["id"]
                orderr = rows[0]["order_num"]
                first = rows[0]["first"]
                last = rows[0]["last"]
                phone = rows[0]["phone"]
                brand = rows[0]["brand"]
                serial = rows[0]["serial"]
                services = rows[0]["services"]
                price = rows[0]["price"]
                status = rows[0]["status"]

                # pass them to a form - the rest is javascript
                return render_template("editing.html",
                                       idd=idd, orderr=orderr, first=first, last=last, phone=phone, brand=brand, serial=serial, services=services, price=price, status=status)

        # DELETING
        elif request.form.get("resultd"):
            jobtodelete = request.form.get("resultd")
            rows = db.execute("DELETE FROM orders WHERE id=:idd", idd=jobtodelete)
            # if nothing came back - then just tell them
            if not rows:
                return render_template("notfound.html")

            else:
                return render_template("deleted.html")

        else:
            return render_template("notfound.html")


    else:
        return render_template("find.html")



#estimate is pure javascript with some HTML bootstrap
@app.route("/estimate")
@login_required
def estimate():
    return render_template("estimate.html")


# recent page. simple query returns 10 recent jobs
@app.route("/recent")
@login_required
def aall():

    rows = db.execute("SELECT * FROM orders ORDER BY id DESC LIMIT 10")

    rows = phonenumber(rows)
    rows = dateformat(rows)
    return render_template ("recent.html", orders=rows)


@app.route("/editing", methods=["GET", "POST"])
@login_required
def editing():
    if request.method == "POST":

        # getting all info from edit to store in db
        idd = int(request.form.get("id"))
        order = int(request.form.get("order"))
        first = request.form.get("first").upper()
        last = request.form.get("last").upper()
        phone = request.form.get("phone")
        brand = request.form.get("brand").upper()
        serial = request.form.get("serial").upper()
        services = request.form.get("services").upper()
        price = round((float(request.form.get("price"))), 2)
        status = request.form.get("status").upper()

        # uploading all info into db
        db.execute("UPDATE orders SET order_num=:order_num, first=:first, last=:last, phone=:phone, brand=:brand, serial=:serial, services=:services, price=:price, status=:status WHERE id=:idd",
                    idd=idd, order_num=order, first=first, last=last, phone=phone, brand=brand, serial=serial, services=services, price=price, status=status)

        # and show user updated order
        rows = db.execute("SELECT * FROM orders WHERE order_num=:order AND id=:idd", order=order, idd=idd)
        rows = phonenumber(rows)
        row = dateformat(rows)
        return render_template ("updated.html", orders=rows)

    else:
        return render_template ("edit.html")


def phonenumber(rows):
    i = 0
    for row in rows:
        phone = str(rows[i]["phone"])
        row["phone"] = "(" + phone[:3] + ") " + phone[3:6] + "-" + phone[6:]
        i += 1
    return rows


def dateformat(rows):
    i = 0

    for row in rows:
        iin = str(rows[i]["d_in"])

        row["d_in"] = iin[5:7] + "/" + iin[8:] + "/" + iin[2:4]

        out = str(rows[i]["out"])

        if out == "None":
            row["out"] = ""
        else:
            row["out"] = out[5:7] + "/" + out[8:] + "/" +  out[2:4]



        i += 1
    return rows


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)