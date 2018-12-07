from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def register():
    return render_template("register.html")

@app.route("/info", methods=["POST"])
def info():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    confirm_password = request.form.get("confrim_password")
    return render_template("info.html", username=username, email=email, password=password, confirm_password=confirm_password)
