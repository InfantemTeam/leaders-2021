#!/usr/bin/env python3

import csv, json, builtins, itertools
from quart import *

def groupby(n: int, l): return ((*(j for j in i if j is not None),) for i in itertools.zip_longest(*(iter(l),)*n))

class Book:
	__slots__ = ('title', 'author')

	title: str
	author: str

	def __init__(self, title, author):
		self.title, self.author = title, author


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

@app.route('/login')
async def login():
	return await render_template('login.html')

@app.route('/lk')
async def lk():
	return await render_template('lk.html')

@app.route('/book')
async def book():
	return await render_template('book.html',
		book = Book('Mein Kampf', 'Hitler A.'),
		similar_books = [Book('TODO', f"The Developer: Vol.{i}") for i in range(20)],
	)

@app.route('/search')
async def search():
	return await render_template('search.html')


@app.before_first_request
def before_first_request():
	print("Loading datasets...")
	books = app.config['BOOKS'] = {int(i['recId']): i for i in csv.DictReader(open('data/cat_3.csv'), delimiter=';')}
	rubrics = app.config['RUBRICS'] = {k: tuple(itertools.islice((Book(title, author) for i in v if (b := books.get(int(i))) and (title := b.get('title')) and (author := b.get('aut'))), 20)) for k, v in json.load(open('data/rubrics.json')).items() if k in app.config['CATEGORIES']}
	print("Data loaded.")

if (__name__ == '__main__'):
	app.run('0.0.0.0', debug=True)

# by InfantemTeam, 2021
# infantemteam@sdore.me
