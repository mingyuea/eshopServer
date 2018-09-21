import functools

from flask import (
	Blueprint, flash, g, request, session, jsonify, current_app
)

from werkzeug.security import check_password_hash, generate_password_hash

from application.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/signup', methods=('POST',))
def signup():
	reqStr = str(request.data)
	reqArr = reqStr[3: -2]
	reqArr = reqArr.split(",")
	reqObj = {}

	for item in reqArr:
		itemArr = item.split(":")
		reqObj[itemArr[0][1:-1]] = itemArr[1][1:-1]

	username = reqObj["username"]
	password = reqObj["password"]
	db = get_db()
	cursor = db.cursor()
	error = None
	query = ("SELECT * FROM userinfo " 
		"WHERE username=%s")
	cursor.execute(query, (username,))

	'''you cannot do:

	var = cursor.execute(...)
	var.fetchone()

	nor:

	cursor.execute(query, (username,), multi=True).fetchone()

	because var is essentially a Nonetype, since thats what cursor.execute() returns. 
	It completed the execute() action but returns None. You have to use fetchone() on the 
	cursor object itself, which contains the results
	'''

	if not username:
		error = 'Username is required'
	elif not password:
		error = 'Password is required'
	elif cursor.fetchone() is not None:
		error = "Username already exists"
		

	if error is None:
		cursor.execute(
			'INSERT INTO userinfo (username, password) VALUES (%s, %s)',
			(username, generate_password_hash(password))
		)
		cursor.close()
		db.commit()
		res = {'actionSuccess': True}

		return jsonify(res)
	else:
		res = {'actionSuccess': False, 'error': error}
		return jsonify(res)

	flash(error)

@bp.route('/login', methods=('POST',))
def login():
	reqStr = str(request.data)
	reqArr = reqStr[3: -2]
	reqArr = reqArr.split(",")
	reqObj = {}

	for item in reqArr:
		itemArr = item.split(":")
		reqObj[itemArr[0][1:-1]] = itemArr[1][1:-1]

	username = reqObj["username"]
	password = reqObj["password"]

	error=None
	res = {}

	db = get_db()
	cursor = db.cursor(dictionary=True)
	query = ('SELECT * FROM userinfo WHERE username=%s')

	cursor.execute(query, (username,))
	user = cursor.fetchone()
	current_app.logger.debug(user)

	if user is None:
		error = 'Incorrect username or password'
	elif not check_password_hash(user['password'], password):
		error = 'Incorrect username or password'

	if error is None:
		session.clear()
		session['userID'] = user['id']

		res['actionSuccess']= True
	else:
		res['actionSuccess'] = False
		res['error'] = error
	
	return jsonify(res)

@bp.before_app_request
def load_logged_in_user():
	userID = session.get('userID')

	if userID is None:
		g.user = None
	else:
		db = get_db()
		cursor = db.cursor()
		cursor.execute("SELECT * FROM userinfo WHERE id = %d", (userID,))
		g.user = cursor.fetchone()

