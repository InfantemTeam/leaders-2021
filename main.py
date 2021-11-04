#!/usr/bin/env python3

import csv, hmac, json, hashlib, builtins, itertools
from . import *
from . import ml
from .db import *


def groupby(n: int, l): return ((*(j for j in i if j is not None),) for i in itertools.zip_longest(*(iter(l),)*n))

class Book:
	__slots__ = ('title', 'author', 'extra')

	title: str
	author: str
	extra: dict

	def __init__(self, title, author, extra=None):
		self.title, self.author, self.extra = title, author, extra or {}


@app.before_request
async def before_request():
	g.builtins = builtins
	g.groupby = groupby
	user = User.query.filter_by(id=current_user.auth_id).first()
	g.user = user #._LocalProxy__local()  # fix jinja3 `auto_await()` bug

@app.errorhandler(Unauthorized)
async def redirect_to_login(*_):
	return redirect(url_for('login'))


@app.route('/')
@login_required
async def index():
	return await render_template('index.html',
		rubrics = app.config['RUBRICS'],
	)

@app.route('/login', methods=('GET', 'POST'))
async def login():
	if (request.method == 'GET'):
		if (g.user): return redirect(url_for('index'))
		return await render_template('login.html')

	try:
		form = await request.form
		email, password = form['email'], form['password']
	except Exception as ex: return abort(Response(str(ex), 400))

	user = User.query.filter_by(email=email).first()
	if (not user or not check_password_hash(user.password, password)): return abort(Response("Неверный логин или пароль", 403))

	login_user(AuthUser(user.id))

	return 'OK'

@app.route('/logout')
async def logout():
	logout_user()

	return redirect(url_for('index'))

@app.route('/register', methods=('POST',))
async def register():
	try:
		form = await request.form
		name, surname, bdate, email, password = form['name'], form['surname'], form['bdate'], form['email'], form['password']
	except Exception as ex: return abort(Response(str(ex), 400))

	if (User.query.filter_by(email=email).first()): return abort(Response("Пользователь уже зарегистрирован", 409))

	user = User(
		email = email,
		password = generate_password_hash(password),
		name = name,
		surname = surname,
		bdate = bdate,
	)

	db.session.add(user)
	db.session.commit()

	login_user(AuthUser(user.id))

	return 'OK'

@app.route('/oauth/vk', methods=('POST',))
async def oauth_vk():
	try:
		data = (await request.get_json())['session']
		h, sig, u = hashlib.md5((str().join(f"{i}={data[i]}" for i in ('expire', 'mid', 'secret', 'sid')) + app.config['VK_SECRET']).encode('utf-8')).hexdigest(), data['sig'], data['user']
		vk_id, vk_name, vk_surname = u['id'], u['first_name'], u['last_name']
	except Exception as ex: return abort(Response(str(ex), 400))

	if (h.strip() != sig.strip()): return abort(Response("Неверный токен. Попробуйте ещё раз", 403))

	user = User.query.filter_by(vk_id=vk_id).first()
	if (not user):
		user = User(
			name = vk_name,
			surname = vk_surname,
			vk_id = vk_id,
		)
		db.session.add(user)
		db.session.commit()

	login_user(AuthUser(user.id))

	return 'OK'

@app.route('/oauth/telegram', methods=('POST',))
async def oauth_telegram():
	try:
		data = await request.get_json()
		secret = hashlib.sha256(app.config['TELEGRAM_TOKEN'].encode('utf-8'))
		h, sig = data['hash'], hmac.new(secret.digest(), '\n'.join(f"{k}={v}" for k, v in sorted(data.items()) if k != 'hash').encode('utf-8'), digestmod=hashlib.sha256).hexdigest()
		telegram_id, telegram_name, telegram_surname = data['id'], data['first_name'], data['last_name']
	except Exception as ex: return abort(Response(str(ex), 400))

	if (h.strip() != sig.strip()): return abort(Response("Неверный токен. Попробуйте ещё раз", 403))

	user = User.query.filter_by(telegram_id=telegram_id).first()
	if (not user):
		user = User(
			name = telegram_name,
			surname = telegram_surname,
			telegram_id = telegram_id,
		)
		db.session.add(user)
		db.session.commit()

	login_user(AuthUser(user.id))

	return 'OK'

@app.route('/lk')
@login_required
async def lk():
	return await render_template('lk.html')

@app.route('/edit_profile', methods=('POST',))
@login_required
async def edit_profile():
	try:
		form = await request.form
		name, surname, email, bdate = form['name'], form['surname'], form['email'], form['bdate']
	except Exception as ex: return abort(Response(str(ex), 400))

	if (email):
		user = User.query.filter_by(email=email).first()
		if (user and user != g.user): return abort(Response("Данный E-mail уже используется", 409))

	if (name): g.user.name = name
	if (surname): g.user.surname = surname
	if (email): g.user.email = email
	if (bdate): g.user.bdate = bdate

	db.session.add(g.user)
	db.session.commit()

	return 'OK'

@app.route('/book/<int:id>')
@login_required
async def book(id):
	try: book = app.config['BOOKS'][id]
	except KeyError: return abort(404)

	return await render_template('book.html',
		book = book,
		similar_books = [Book('TODO', f"The Developer: Vol.{i}") for i in range(20)],
	)

@app.route('/search')
@login_required
async def search():
	return await render_template('search.html')

@app.route('/api/recomms')
async def api_recomms():
	try: user_id, count = int(request.args['user_id']), int(request.args['count'])
	except Exception as ex: return abort(Response(str(ex), 400))

	return ml.model_predict(user_id, count)

@app.route('/test')
async def test():
	if (not request.args): return '<h1>Тест рекомендаций для пользователя</h1><form action="/test">ID пользователя: <input type="number" name="id"><br>Количество: <input type="number" name="num"><br><input type="submit"></form>'

	try: id, num = int(request.args['id']), int(request.args['num'])
	except Exception as ex: return abort(Response(str(ex), 400))

	recommended_books = ml.model_recommend(id, num)

	return render_template_string(r"{% for i in recommended_books %}{{ book_card(i) }}{% endfor %}", recommended_books=recommended_books)


@app.before_first_request
def before_first_request():
	print("Loading datasets...")
	books = app.config['BOOKS'] = {int(i['recId']): i for i in csv.DictReader(open('data/cat_3.csv', encoding='cp1251'), delimiter=';')}
	rubrics = app.config['RUBRICS'] = {k: tuple(itertools.islice((Book(title, author, b) for i in v if (b := books.get(int(i))) and (title := b.get('title')) and (author := b.get('aut'))), 20)) for k, v in json.load(open('data/rubrics.json')).items() if k in app.config['CATEGORIES']}
	ml.init()
	print("Data loaded.")


# by InfantemTeam, 2021
# infantemteam@sdore.me
