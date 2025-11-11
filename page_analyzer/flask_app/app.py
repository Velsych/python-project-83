import datetime
import os

import requests
from dotenv import load_dotenv
from flask import (
    Flask,
    flash,
    get_flashed_messages,
    redirect,
    render_template,
    request,
    url_for,
)

from page_analyzer.controller.db_controller import DbManager, UrlRepository
from page_analyzer.controller.validators import html_parser, validator

load_dotenv()


DATABASE_URL = os.getenv('DATABASE_URL')


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

db_manager = DbManager(DATABASE_URL)
repo = UrlRepository(db_manager)


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
    return render_template("urls/index.html", messages=messages,
                            all_rows=url_list)


@app.post("/urls")
def post_url():
    new_url = request.form.get('url')
    valid_url = validator(new_url)
    if not valid_url:
        app.logger.info("Неверный юрл.")
        flash("Некорректный URL", "fail")
        messages = get_flashed_messages()
        return render_template('index.html', messages=messages), 422
    if repo.name_check(valid_url):
        current_date = datetime.date.today()
        repo.add_url(valid_url, current_date)
        flash("Страница успешно добавлена", "success")
        app.logger.info("Запись добавлена, выполняется редирект")
        result = repo.get_last_id()
        return redirect(url_for("detail_url", id=result['id']))
    else:
        result = repo.get_by_name(valid_url)
        flash("Страница уже существует", "success")
        return redirect(url_for("detail_url", id=result['id']))
            

@app.route('/urls/<id>')
def detail_url(id):
    url = repo.get_by_id(id)
    messages = get_flashed_messages(with_categories=True)
    checks = repo.get_url_checks(id)
    if messages:
        app.logger.info("Есть flash сообщение")
    return render_template("urls/id.html", url=url, messages=messages,
                            url_checks=checks)


@app.post('/urls/<id>/checks')
def check_url(id):
    url_id = repo.get_by_id(id)
    current_date = datetime.date.today()
    try:
        res = requests.get(url_id['name'], timeout=5.000)
        status = res.status_code
        html = res.text
        h1, title, description = html_parser(html)
        res.raise_for_status()
    except requests.exceptions.RequestException:
        flash('Произошла ошибка при проверке', 'fail')
        return redirect(url_for('detail_url', id=id))
    except requests.exceptions.Timeout:
        flash('Произошла ошибка при проверке', 'fail')
        return redirect(url_for('detail_url', id=id))
    else:
        repo.add_url_check(id, current_date, status, h1, title, description)
        flash('Страница успешно проверена', 'success')
        return redirect(url_for('detail_url', id=id))
    

@app.errorhandler(404)
def error_404(e):
    return render_template('error_404.html')


@app.errorhandler(500)
def error_500(e):
    return render_template('error_500.html')