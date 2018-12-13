# Import the class 'Flask' from the 'flask' module, written by someone else.
# gives access to a variable called `session which can be used to keep vaules that are specific to a particular user
from flask import Flask, render_template, request, session

# an additional extension to sessions which allows them to be stored server-side
from flask_session import Session

# Instantiate a new web application called 'app', with '__name__' representing the current file
app = Flask(__name__) 

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# A decorator; when the user goes to the route '/, exceute the function immediately below
@app.route("/") 
def index():
    return "Hello, world!"

app = Flask(__name__)
