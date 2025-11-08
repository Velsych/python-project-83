import os

from dotenv import load_dotenv
from flask import Flask,render_template,url_for,flash,redirect,get_flashed_messages

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route("/")
def index():
    return render_template('index.html'),200

@app.route('/urls')
def urls():
    url_list = []
    messages = get_flashed_messages()
    print(messages)
    return render_template("urls/index.html",messages = messages)

@app.post("/urls")
def check_url():
    flash("This is a message", "success")
    return redirect('/urls')