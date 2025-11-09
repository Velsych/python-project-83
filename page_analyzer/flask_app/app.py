import os

import psycopg2
from dotenv import load_dotenv
from flask import (
    Flask,
    flash,
    get_flashed_messages,
    redirect,
    render_template,
    request,
)
from validators import url

from page_analyzer.controller.db_controller import db_work

load_dotenv()


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL)
repo = db_work(conn)

@app.route("/")
def index():
    messages = get_flashed_messages()
    return render_template('index.html', messages=messages)


@app.route('/urls')
def urls():
    url_list = []
    messages = get_flashed_messages()
    if messages:
        app.logger.info("Есть flash сообщение")
    url_list = repo.get_all()
    return render_template("urls/index.html", messages=messages, all_rows=url_list)


@app.post("/urls")
def check_url():
    new_url = request.form.get('url')
    repo = db_work(conn)
    if url(new_url):
        repo.add_url(new_url)
        flash("Запись успешно добавлена", "success")
        app.logger.info("Запись добавлена, выполняется редирект")
        return redirect('/urls')
    else:
        app.logger.info("Пароль неверный, выполняю перенаправление на /")
        flash("Неверный юрл!", "fail")
        return redirect('/')
    