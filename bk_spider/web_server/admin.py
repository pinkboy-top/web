from flask import Flask, render_template, redirect, request

app = Flask(__name__)
app.debug = True


@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user_name = request.form['username']
        password = request.form['password']
        if user_name == "admin" and password == "admin":
            return redirect("index")
        else:
            return render_template("login.html")
    return render_template("login.html")
