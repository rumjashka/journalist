import os

import requests
from flask import Flask, render_template, request, session, redirect, url_for
from os import path
from datetime import datetime
from file import add_file, get_file, get_work, get_post, edit_file
from mail import add_contact, get_contact
from database import Mongo
import mailgun


app = Flask(__name__, static_url_path='/static')
app.secret_key = os.environ['SECRET_KEY']


@app.route("/")
def home():
    images = []
    for filename in get_file():
        images.append({'file': 'http://127.0.0.1:5001/static/img/' + filename['file'], 'title': filename['title'],
                       'description': filename['description'], '_id':filename['_id']})
    return render_template('home.html', images=images)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        theme = request.form.get('theme', '')
        question = request.form.get('question', '')
        add_contact(name, email, theme, question)
    return render_template("contact.html")


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/list")
def list():
    posts=get_post()
    return render_template('list.html', posts=posts)


@app.route("/edit/<_id>", methods=['GET', 'POST'])
def edit(_id):
    if not session.get('login'):
        return redirect('/admin')
    if request.method == 'POST':
        _id = request.form['id']
        description = request.form['description']
        edit_file(_id, description)
        return redirect (url_for('list'))
    filename=get_work(_id)
    filename['file']='http://127.0.0.1:5001/static/img/'+filename['file']
    return render_template("edit.html", filename=filename, post_id=_id)

@app.route("/work/<_id>")
def work(_id):
    filename=get_work(_id)
    filename['file']='http://127.0.0.1:5001/static/img/'+filename['file']
    return render_template("work.html", filename=filename)


@app.route("/admin", methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        password = request.form['password']
        login = request.form['login']
        if check_user(login, password):
            session["login"] = login
            return redirect("/add_post")
    if session.get('login'):
        session['login'] = None
    return render_template("admin.html")


def check_user(login, password):
    user=Mongo.get_user(login)
    if user and user['password']== password:
        return True
    return False


@app.route('/messages')
def messages():
    messages=get_contact()
    return render_template('messages.html', messages=messages)

@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    if not session.get('login'):
        return redirect('/admin')
    if request.method =='POST':
        file = request.files['file']
        title=request.form['title']
        description=request.form['description']
        file.save(path.join ('static/img', file.filename))
        add_file(title, description, file.filename, datetime.utcnow())
        send_emails()
        return redirect('/')
    return render_template('add_post.html')


def send(email):
    return requests.post(
        mailgun.URL,
        auth=("api", mailgun.API_KEY),
        data={
            "from": mailgun.FROM,
            "to": email,
            "subject": "New post",
            "text": "New post is on the site! Click here to read http://127.0.0.1:5001/"
        }
    )

def send_emails():
    users=Mongo.get_all('journalist')
    for user in users:
        send(user['email'])

if (__name__ == "__main__"):
    Mongo.connect()
    app.run(port=5001, debug=True)
