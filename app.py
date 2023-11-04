from flask import Flask, redirect, render_template, url_for, request, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE-URI']='sqlite:///głodny-online.db'
db=SQLAlchemy(app)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

class Users(db.Model):
    user_id = db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(200),nullable=False)
    surname=db.Column(db.String(200),nullable=False)
    email=db.Column(db.String(200),nullable=False)
    password=db.Column(db.String(200),nullable=False)
    date_time_of_account_creation=db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/register")
def register():
    return render_template("register.html")
    

if __name__ == "__main__":
    app.run(debug=True)
