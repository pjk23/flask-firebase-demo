import base64
import json
import os

from flask import Flask, render_template, request, redirect, url_for, jsonify
from firebase_admin import credentials, firestore, initialize_app


app = Flask(__name__)

FIREBASE_SERVICE_KEY = json.loads(base64.b64decode(os.environ.get('FIREBASE_SERVICE_KEY')))

firebase_credentials = credentials.Certificate(FIREBASE_SERVICE_KEY)
default_app = initialize_app(firebase_credentials)
db = firestore.client()
todo_ref = db.collection('tasks')


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    todo_ref.add({'title': title, 'complete': False})
    return redirect(url_for("home"))


@app.route("/update/<string:todo_id>")
def update(todo_id):
    todo_ref.document(todo_id).update({'complete': True})
    return redirect(url_for("home"))


@app.route("/delete/<string:todo_id>")
def delete(todo_id):
    todo_ref.document(todo_id).delete()
    return redirect(url_for("home"))


@app.route("/")
def home():
    todos = [{**todo.to_dict(), 'id': todo.id} for todo in todo_ref.stream()]
    return render_template("base.html", todo_list=todos)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host = '0.0.0.0', port = port, debug=True)
    # app.run(debug=True)
