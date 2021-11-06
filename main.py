#!/usr/bin/env python3

import csv, hmac, json, time, asyncio, hashlib, os.path, builtins, itertools, threading
from . import *
from . import ml
from .db import *


def groupby(n: int, l): return ((*(j for j in i if j is not None),) for i in itertools.zip_longest(*(iter(l),)*n))

class Book:
	__slots__ = ('id', 'title', 'author', 'extra')

	id: int
	title: str
	author: str
	extra: dict

	def __init__(self, id, title, author, extra=None):
		self.id, self.title, self.author, self.extra = id, title, author, extra or {}

	@classmethod
	def get(cls, id):
		if (not (b := app.config['BOOKS'].get(id))): return None
		if (not (title := b.get('title'))): return None
		if (not (author := b.get('aut'))): return None
		return cls(id, title, author, b)

@app.before_request
async def before_request():
	await app.loaded_flag.wait()

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

	user = None

	if (email.isdecimal()):
		user = User.query.filter_by(id=int(email)).first()
		password = True
	else:
		user = User.query.filter_by(email=email).first()

	if (not user or not (password is True or check_password_hash(user.password, password))):
		#app.logger.info
		print(f"Failed login attempt ({email}): incorrect {'password' if (user) else 'login'}.")
		return abort(Response("Неверный логин или пароль", 403))

	login_user(AuthUser(user.id))

	return 'OK'

@app.route('/login_guest', methods=('POST',))
async def login_guest():
	login_user(AuthUser(''))

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
	recommended_books = [b for i in ml.model_recommend(g.user.id, 20) if (b := Book.get(i))]
	print(recommended_books)
	read_books = [b for i in ml.user_history(g.user.id) if (b := Book.get(i))]

	return await render_template('lk.html',
		recommended_books = recommended_books,
		read_books = read_books,
	)

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
	try: book = Book.get(id)
	except KeyError: return abort(404)

	similar_books = [b for i in ml.model_find_similar(id) if (b := Book.get(i))]

	return await render_template('book.html',
		book = book,
		similar_books = similar_books,
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

	recommended_books = [b for i in ml.model_recommend(id, num) if (b := Book.get(i))]

	return await render_template_string(r'{% from "common.html" import book_card %}{% for i in recommended_books %}{{ book_card(i) }}{% endfor %}',
		recommended_books = recommended_books,
	)


def load_data():
	print("Loading datasets...")
	books = app.config['BOOKS'] = {int(i['recId']): i for i in itertools.chain(*(csv.DictReader(open(f"data/cat_{c}.csv", encoding='cp1251'), delimiter=';') for c in range(1, 4)))}
	rubrics = app.config['RUBRICS'] = {k: tuple(itertools.islice((b for i in v if (b := Book.get(i))), 20)) for k, v in json.load(open('data/rubrics.json')).items() if k in app.config['CATEGORIES']}

	print("Loading model...")
	retrain = (os.path.exists('model.npy') and (time.time() - os.path.getmtime('model.npy')) >= 60*60*24)
	ml.init(retrain=retrain)

	print("Data loaded.")
	app.loaded_flag.set()

@app.before_serving
def before_serving():
	app.loaded_flag = asyncio.Event()
	threading.Thread(target=load_data, daemon=True).start()

# by InfantemTeam, 2021
# infantemteam@sdore.me
