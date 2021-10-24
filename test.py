from quart import *

app = Quart(__name__)

@app.route('/')
async def index():
	return await render_template('index.html')

@app.route('/profile/edit')
async def profile_edit():
	return await render_template('profile_edit.html')

app.run('0.0.0.0', debug=True)
