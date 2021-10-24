#!/usr/bin/env python3

import itertools
from quart import *

def groupby(n, l): return ((*(j for j in i if j is not None),) for i in itertools.zip_longest(*(iter(l),)*n))

class Book:
	title: str
	author: str

	def __init__(self, title, author):
		self.title, self.author = title, author


app = Quart(__name__)

@app.route('/')
async def index():
	return await render_template('index.html')

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
		similar_books = tuple(groupby(5, [Book('TODO', f"The Developer: Vol.{i}") for i in range(20)])),
	)

@app.route('/search')
async def search():
	return await render_template('search.html')

if (__name__ == '__main__'):
	app.run('0.0.0.0', debug=True)

# by InfantemTeam, 2021
# infantemteam@sdore.me
