#!/usr/bin/env python3

import csv, json, hashlib, builtins, itertools
from . import *
from .db import *


def groupby(n: int, l): return ((*(j for j in i if j is not None),) for i in itertools.zip_longest(*(iter(l),)*n))

def with_user(f):
	@login_required
	async def decorated(*args, **kwargs):
		user = User.query.filter_by(id=current_user.auth_id).first()
		assert (user)
		return f(user, *args, **kwargs)
	decorated.__name__ = f.__name__  # endpoint name
	return decorated

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
	g.user = current_user._LocalProxy__local()  # fix jinja3 `auto_await()` bug

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
	if (request.method == 'GET'): return await render_template('login.html')

	form = await request.form
	try: email, password = form['email'], form['password']
	except Exception as ex: return abort(400, ex)

	user = User.query.filter_by(email=email).first()
	if (not user): return abort(418)
	if (not check_password_hash(user.password, password)): return abort(403)

	login_user(AuthUser(user.id))

	return 'OK'

@app.route('/logout')
async def logout():
	logout_user()

	return 'OK'

@app.route('/register', methods=('POST',))
async def register():
	form = await request.form
	try: name, surname, bdate, email, password = form['name'], form['surname'], form['bdate'], form['email'], form['password']
	except Exception as ex: return abort(400, ex)

	if (User.query.filter_by(email=email).first()): return abort(409, "Пользователь уже зарегистрирован!")

	user = User(email=email, password=generate_password_hash(password), name=name, surname=surname, bdate=bdate)

	db.session.add(user)
	db.session.commit()

	login_user(AuthUser(user.id))

	return 'OK'

@app.route('/oauth/vk', methods=('POST',))
async def oauth_vk():
	try:
		data = (await request.get_json())['session']
		h, sig, u = hashlib.md5((str().join(f"{i}={data[i]}" for i in ('expire', 'mid', 'secret', 'sid')) + app.config['VK_SECRET']).encode()).hexdigest(), data['sig'], data['user']
		vk_id, vk_name, vk_surname = u['id'], u['first_name'], u['last_name']
	except Exception as ex: return abort(400, ex)

	if (h.strip() != sig.strip()): return abort(403)

	user = User.query.filter_by(vk_id=vk_id).first()
	if (not user):
		user = User(name=vk_name, surname=vk_surname, vk_id=vk_id)
		db.session.add(user)
		db.session.commit()

	login_user(AuthUser(user.id))

	return 'OK'

@app.route('/lk')
@login_required
async def lk():
	return await render_template('lk.html')

@app.route('/edit_profile', methods=('POST',))
@with_user
async def edit_profile(user):
	form = await request.form
	try: name, surname, email, bdate = form['name'], form['surname'], form['email'], form['bdate']
	except Exception as ex: return abort(400, ex)

	user.name, user.surname, user.email, user.bdate = name, surname, email, bdate

	db.session.add(user)
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


@app.before_first_request
def before_first_request():
	print("Loading datasets...")
	books = app.config['BOOKS'] = {int(i['recId']): i for i in csv.DictReader(open('data/cat_3.csv'), delimiter=';')}
	rubrics = app.config['RUBRICS'] = {k: tuple(itertools.islice((Book(title, author, b) for i in v if (b := books.get(int(i))) and (title := b.get('title')) and (author := b.get('aut'))), 20)) for k, v in json.load(open('data/rubrics.json')).items() if k in app.config['CATEGORIES']}
	print("Data loaded.")


# by InfantemTeam, 2021
# infantemteam@sdore.me
