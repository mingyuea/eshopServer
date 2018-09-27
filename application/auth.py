import functools
import json

from flask import (
	Blueprint, flash, g, request, session, current_app
)

from werkzeug.security import check_password_hash, generate_password_hash
from application.db import get_db
from application.cors_response import cors_res

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/init', methods=('GET',))
def init():
	userID = session.get('user_id')

	if userID is None:
		res = {"signedIn": False}
		session.clear()
	else:
		db = get_db()
		cursor = db.cursor()
		query = ("SELECT username FROM userinfo WHERE id=%s")
		cursor.execute(query, (userID,))
		username = cursor.fetchone()
		res = {"signedIn": True, "username": username[0]}
		
	resp = cors_res(res=res)

	return resp


@bp.route('/signup', methods=('POST','OPTIONS'))
def signup():
	if request.method == 'OPTIONS':
		return cors_res()
	else:
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

			newQuery = ('SELECT id FROM userinfo WHERE username=%s')
			cursor.execute(newQuery, (username,))
			user_id= cursor.fetchone()[0]

			newStmt = ('INSERT INTO cartdata (id) VALUES (%s)')
			cursor.execute(newStmt, (user_id,))

			session.permanent = True
			session['user_id'] = user_id

			cursor.close()
			db.commit()

			res = {'actionSuccess': True}

			return cors_res(res)
		else:
			res = {'actionSuccess': False, 'error': error}
			return cors_res(res)

		flash(error)


@bp.route('/login', methods=('POST','OPTIONS'))
def login():
	if request.method == 'OPTIONS':
		resp = cors_res()
		return resp
	else:
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

		if user is None:
			error = 'Incorrect username or password'
		elif not check_password_hash(user['password'], password):
			error = 'Incorrect username or password'

		if error is None:
			session.clear()
			session.permanent = True
			session['user_id'] = user['id']

			res['actionSuccess']= True
		else:
			res['actionSuccess'] = False
			res['error'] = error

		resp = cors_res(res)
		return resp

'''@bp.before_app_request
def load_logged_in_user():
	userID = session.get('userID')

	if userID is None:
		g.user = None
	else:
		db = get_db()
		cursor = db.cursor()
		cursor.execute("SELECT * FROM userinfo WHERE id = %s", (userID,))
		g.user = cursor.fetchone()'''

@bp.route('/logout', methods=('GET',))
def logout():
	session.clear()
	res = {}

	if session.get('user_id') is None:
		res['logout'] = True
	else:
		res['logout'] = False
		
	resp = cors_res(res)
	return resp
