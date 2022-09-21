import base64
import json
import os

from flask import Flask, render_template, request, redirect, url_for
from firebase_admin import credentials, firestore, initialize_app
# from flask_sqlalchemy import SQLAlchemy

# FIREBASE_SERVICE_KEY = json.loads(base64.b64decode(os.environ.get('FIREBASE_SERVICE_KEY')))

app = Flask(__name__)

firebase_credentials = credentials.Certificate("/Users/pjay/Downloads/cfg-flask-demo-firebase-adminsdk-8v72u-97e3923a27.json")
default_app = initialize_app(firebase_credentials)
db = firestore.client()
todo_ref = db.collection('tasks')

# /// = relative path, //// = absolute path
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)



class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/")
def home():
    todo_list = Todo.query.all()
    return render_template("base.html", todo_list=todo_list)


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)