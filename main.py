#!/usr/bin/env python3

import csv, json, hashlib, builtins, itertools
from quart import *
from db import *

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


app = Quart(__name__)
app.config.from_object('config')

@app.before_request
async def before_request():
	g.builtins = builtins
	g.groupby = groupby


@app.route('/')
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

@app.route('/logout')
async def logout():
	logout_user()

@app.route('/register', methods=('POST',))
async def register():
	form = await request.form
	try: email, password = form['email'], form['password']
	except Exception as ex: return abort(400, ex)

	if (User.query.filter_by(email=email).first()): return abort(409)

	user = User(email=email, password=generate_password_hash(password))

	db.session.add(user)
	db.session.commit()

	login_user(AuthUser(user.id))

@app.route('/oauth/vk', methods=('POST',))
async def oauth_vk():
	data = await request.get_json()
	try: h, sig, u = hashlib.md5((str().join(f"{i}={data[i]}" for i in ('expire', 'mid', 'secret', 'sid')) + app.config['VK_SECRET']).encode()).hexdigest(), data['sig'], data['user']
	except Exception as ex: return abort(400, ex)

	if (h.strip() != sig.strip()): return abort(403)

	vk_id = user['id']

	user = User.query.filter_by(vk_id=vk_id).first()
	if (not user):
		user = User(name=user['first_name'], surname=user['last_name'], vk_id=vk_id)
		db.session.add(user)
		db.session.commit()

	login_user(AuthUser(user.id))

@app.route('/lk')
async def lk():
	return await render_template('lk.html')

@app.route('/book/<int:id>')
async def book(id):
	try: book = app.config['BOOKS'][id]
	except KeyError: return abort(404)

	return await render_template('book.html',
		book = book,
		similar_books = [Book('TODO', f"The Developer: Vol.{i}") for i in range(20)],
	)

@app.route('/search')
async def search():
	return await render_template('search.html')


@app.before_first_request
def before_first_request():
	print("Loading datasets...")
	books = app.config['BOOKS'] = {int(i['recId']): i for i in csv.DictReader(open('data/cat_3.csv'), delimiter=';')}
	rubrics = app.config['RUBRICS'] = {k: tuple(itertools.islice((Book(title, author, b) for i in v if (b := books.get(int(i))) and (title := b.get('title')) and (author := b.get('aut'))), 20)) for k, v in json.load(open('data/rubrics.json')).items() if k in app.config['CATEGORIES']}
	print("Data loaded.")

if (__name__ == '__main__'):
	app.run('0.0.0.0', debug=False, autoreload=True)

# by InfantemTeam, 2021
# infantemteam@sdore.me
