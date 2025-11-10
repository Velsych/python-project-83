import os
from urllib.parse import urlparse
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

from page_analyzer.controller.db_controller import db_work,validator

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
def post_url():
    new_url = request.form.get('url')
    valid = validator(new_url)
    if not valid:
        app.logger.info("Пароль неверный, выполняю перенаправление на /")
        flash("Неверный юрл!", "fail")
        return redirect('/')
    if repo.name_check(valid):
        repo.add_url(valid)
        flash("Запись успешно добавлена", "success")
        app.logger.info("Запись добавлена, выполняется редирект")
        result = repo.get_last_id()
        return redirect(url_for("detail_url", id = result['id']))
    else:
        result = repo.get_by_name(str(valid))
        flash("Запись уже существует", "success")
        return redirect(url_for("detail_url", id = result['id']))
            
    


@app.route('/urls/<id>')
def detail_url(id):
    url = repo.get_by_id(id)
    messages = get_flashed_messages()
    checks = repo.get_url_cheks(id)
    if messages:
        app.logger.info("Есть flash сообщение")
    return render_template("urls/id.html",url=url,messages = messages,url_checks = checks)



@app.post('/urls/<id>/checks')
def check_url(id):
    repo.add_url_check(id)
    return redirect(url_for('detail_url',id = id))