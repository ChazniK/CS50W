import os

from flask import Flask, render_template, request, flash
# from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("register.html")

@app.route("/register/", methods=["POST"])
def register_user():
    # Get form information
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    confirm = request.form.get("confirm_password")

    result = db.execute("""SELECT * FROM users 
                           WHERE username = :username AND email = :email""",
                           {"username": username, "email": email}).rowcount

    # flash(result)
    
    if result == 0:
        db.execute("""INSERT INTO users(username, email, password) 
                      VALUES(:username, :email, :password)""",
                      {"username": username, "email": email, "password": password})
        db.commit()
        return render_template("books.html", username=username, email=email, password=password)
    else:
        return render_template("books.html", username="Record already exists")

@app.route("/login/")
def login_user():
    return render_template("login.html")