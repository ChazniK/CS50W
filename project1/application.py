import os
import gc

from flask import Flask, session, render_template, flash, request, url_for, redirect
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from passlib.hash import sha256_crypt


app = Flask(__name__)

# # Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    return render_template("register.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

@app.route("/login/", methods=['GET', 'POST'])
def login_page():
    error = ""
    try:
        if request.method == "POST":
            attempted_username = request.form['username']
            attempted_password = request.form['password']

            # flash(attempted_username)
            # flash(attempted_password)

            if attempted_username == "admin" and attempted_password == "password":
                return redirect(url_for('welcome'))
            else:
                error = "Invalid credentials entered, try again please"

        return render_template("login.html", error=error)
      
    except Exception as e:
        # flash(e)
        return render_template("login.html", error=error)

class RegistrationForm(Form):
    username = TextField('username', [validators.Length(min=4, max=50)])
    email = TextField('email', [validators.Length(min=6, max=50)])
    password = PasswordField('password', [validators.required(),
                                          validators.Length(min=6, max=50),
                                          validators.EqualTo('confirm_password', message="Passwords must match")])
    confirm_password = PasswordField('confirm_password')

    # accept_tos = BooleanField("I accept the Terms of Service and the Privacy Notice")

@app.route("/register/", methods=['GET', 'POST'])
def register():
    try:
        form = RegistrationForm(request.form)

        if request.method == "POST" and form.validate():
            username = form.username.data
            email = form.email.data
            password = sha256_crypt.encrypt(str(form.password.data))

            insert_user = db.execute("SELECT * from users WHERE  username = (%s)", username)
            if (int(len(insert_user))) > 0:
                flash("That username is already taken, please select another")
                return render_template("register.html", form=form)
            else:
                db.execute("""
                INSERT INTO users (username, email, password) 
                VALUES(%s, %s, %s)""",
                (username, email, password))

                db.commit()
                flash("Thanks for registering")
                db.close()
                gc.collect()

                session['logged_in'] = True
                session['username'] = username

                return redirect(url_for('welcome'))

    except Exception as e:
        return str(e)

@app.route("/books/")
def welcome():
    return render_template("books.html")