@api.route('/api/profile', methods=('GET', 'POST'))
@with_user
async def api_profile(user):
	profile = Profile.query.filter_by(id=user.id).first()

	if (request.method == 'GET'): return ({k: v for k in ('age', 'education', 'wage') if (v := getattr(profile, k, None))} if (profile) else {})

	if (not profile): profile = Profile()

	form = await request.form
	try: age, education, wage = int(form['age']), int(form['education']), int(form['wage'])
	except Exception as ex: return abort(400, ex)

	profile.age, profile.education, profile.wage = age, education, wage

	db.session.add(profile)
	db.session.commit()

	return {}
