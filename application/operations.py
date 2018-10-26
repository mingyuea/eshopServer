from flask import (
	Blueprint, flash, g, request, session, current_app
)

from application.db import get_db, init_db
from application.cors_response import cors_res

bp = Blueprint('operations', __name__, url_prefix='/operations')

@bp.route('/initDB', methods=('GET',))
def initDB():
		init_db()
		return "The database has been init"

@bp.route('/inventory', methods=('GET',))
def inventory():
	db = get_db()
	cursor = db.cursor(dictionary=True)
	query = ('SELECT * FROM inventory')
	cursor.execute(query)
	resBody = cursor.fetchall()

	return cors_res(resBody)


@bp.route('/addcart', methods=('OPTIONS', 'POST'))
def addcart():
	if request.method == 'OPTIONS':
		return cors_res()
	else:
		userID = session.get("user_id")
		reqDict = request.get_json()
		itemcode = str(reqDict['itemcode'])
		itemAmt = reqDict['itemAmt']		
		resBody = {}

		if userID is not None:
			db = get_db()
			db.get_warnings = True
			cursor = db.cursor()
			query = ('SELECT ' + itemcode + ' FROM cartdata WHERE id = %s')
			cursor.execute(query, (userID, ))
			currentNum = cursor.fetchone()[0]

			if currentNum is None:
				stmt = ('UPDATE cartdata SET ' + itemcode + ' = 1 WHERE id = %s')
				cursor.execute(stmt, (userID,))
				cursor.fetchwarnings()
			else:
				currentNum = int(currentNum) + int(itemAmt)
				stmt = ('UPDATE cartdata SET ' + itemcode + ' = %s WHERE id = %s')
				cursor.execute(stmt, (currentNum, userID))

			countQuery = ('SELECT * FROM cartdata WHERE id = %s')
			cursor.execute(countQuery, (userID,))
			rowData = cursor.fetchone()
			itemCount = -1

			for item in rowData:
				if item is not None and item > 0:
					itemCount += 1

			cursor.close()
			db.commit()
			resBody['addSuccess'] = True
			resBody['itemCount'] = itemCount

			return cors_res(resBody)


@bp.route('/cart', methods=('OPTIONS', 'GET'))
def cart():
	if request.method == 'OPTIONS':
		return cors_res()
	else:
		userID = session.get('user_id')

		if userID is not None:
			db = get_db()
			cursor = db.cursor(dictionary=True)
			query = ('SELECT * FROM cartdata WHERE id = %s')

			cursor.execute(query, (userID,))
			cartData = cursor.fetchone()
			tmpCart = []

			for key, val in cartData.items():
				tmpObj = {}
				if key != 'id' and val is not None and val > 0:
					tmpObj['itemcode'] = key
					tmpObj['amt'] = val
					tmpCart.append(tmpObj)

			newQuery = ('SELECT * FROM inventory WHERE itemcode = %s')
			for item in tmpCart:
				cursor.execute(newQuery, (item['itemcode'],))
				item['itemData'] = cursor.fetchone()
			cursor.close()

			return cors_res(tmpCart)


@bp.route('/remove', methods={'OPTIONS', 'POST'})
def remove():
	if request.method == 'OPTIONS':
		return cors_res()
	else:
		userID = session.get('user_id');
		reqDict = request.get_json()
		itemcode = reqDict['itemCode']

		if userID is not None:
			db = get_db()
			cursor = db.cursor()
			stmt = ('UPDATE cartdata SET ' + itemcode + ' = NULL WHERE id = %s')
			cursor.execute(stmt, (userID, ))

			cursor.close()
			db.commit()

			res = {'remove': True}
			return cors_res(res)

		res = {'remove': False}
		return cors_res(res)

@bp.route('/search', methods=('POST','OPTIONS'))
def search():

	if(request.method == 'OPTIONS'):
		return cors_res()
	else:
		reqDict = request.get_json()
		searchIn = reqDict['searchIn']
		#current_app.logger.debug(reqDict)

		db = get_db()
		cursor = db.cursor(dictionary=True)
		query = ("SELECT * FROM inventory WHERE MATCH (name) AGAINST (%s IN NATURAL LANGUAGE MODE)")
		cursor.execute(query, (searchIn,))

		searchRes = cursor.fetchall()
		#current_app.logger.debug(searchRes)

		return cors_res(searchRes)
