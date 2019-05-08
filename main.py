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
    error = request.cookies.get('error')
    user = None

    if email:
        user = User.fetch_one(query=["email", "==", email])

    response = make_response(render_template('index.html', user=user, error=error))

    if error:
        response.set_cookie('error', expires=0  )

    return response

@app.route("/login", methods=["POST"])
def login():
    name = request.form.get('user-name')
    email = request.form.get('user-email')

    user = User.fetch_one(query=["email", "==", email])

    response = make_response(redirect(url_for('index')))

    if not user:
        user = User(name=name, email=email)
        user.create()

        response.set_cookie('email', email)

        return response

    response.set_cookie('error', 'This user already exists')

    return response
@app.route("/users", methods=["GET"])
def users():
    email = request.cookies.get('email')
    user = None

    if email:
        user = User.fetch_one(query=["email", "==", email])

    users = User.fetch()

    return render_template('users.html', users=users, user=user)

@app.route("/logout", methods=["GET"])
def logout():
    response = make_response(redirect(url_for('index')))

    response.set_cookie('email', expires=0)

    return response

if __name__ == '__main__':
    app.run()
