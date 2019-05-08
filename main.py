from flask import Flask, render_template
from flask import request
from flask import make_response
from flask import redirect
from flask import url_for

from models import User

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    email = request.cookies.get('email')
    user = None

    if email:
        user = User.fetch_one(query=["email", "==", email])

    return render_template('index.html', user=user)

@app.route("/login", methods=["POST"])
def login():
    name = request.form.get('user-name')
    email = request.form.get('user-email')

    user = User(name=name, email=email)
    user.create()

    response = make_response(redirect(url_for('index')))
    response.set_cookie('email', email)

    return response

@app.route("/logout", methods=["GET"])
def logout():
    response = make_response(redirect(url_for('index')))

    response.set_cookie('email', expires=0)

    return response

if __name__ == '__main__':
    app.run()
