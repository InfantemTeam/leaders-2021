#!/usr/bin/env python3

from quart import *

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
	return await render_template('book.html')

@app.route('/search')
async def search():
	return await render_template('search.html')

if (__name__ == '__main__'):
	app.run('0.0.0.0', debug=True)

# by InfantemTeam, 2021
# infantemteam@sdore.me
