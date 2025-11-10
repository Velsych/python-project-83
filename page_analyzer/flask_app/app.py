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
    url_for
)
from validators import url

from page_analyzer.controller.db_controller import db_work

load_dotenv()


keepalive_kwargs = {
    "keepalives": 1,
    "keepalives_idle": 30,
    "keepalives_interval": 5,
    "keepalives_count": 5,
}


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

repo = db_work()



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
    if url(new_url):
         if repo.add_url(new_url):
            flash("Запись успешно добавлена", "success")
            app.logger.info("Запись добавлена, выполняется редирект")
            result = repo.get_last_id()
            return redirect(url_for("detail_url",result['id']))
         else:
             flash("Запись уже существует", "success")
             return redirect('/urls')
    else:
        app.logger.info("Пароль неверный, выполняю перенаправление на /")
        flash("Неверный юрл!", "fail")
        return redirect('/')


@app.route('/urls/<id>')
def detail_url(id):
    url = repo.get_one(id)
    messages = get_flashed_messages()
    if messages:
        app.logger.info("Есть flash сообщение")
    return render_template("urls/id.html",url=url)
    