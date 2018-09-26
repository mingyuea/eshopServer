from flask import (
	Blueprint, flash, g, request, session, current_app
)

from application.db import get_db
from application.cors_response import cors_res

bp = Blueprint('operations', __name__, url_prefix='/operations')

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
		#current_app.logger.debug(userID)
		#return cors_res()

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
				if item is not None:
					itemCount += 1

			current_app.logger.debug('itemcount is '+ str(itemCount))
			cursor.close()
			db.commit()
			resBody['addSuccess'] = True
			resBody['itemCount'] = itemCount
			return cors_res(resBody)

		'''else:
			tmpCart = session.get("tmp_cart")
			if tmpCart is None:
				tmpCart = [itemCode]
				session.clear()
			else:
				tmpCart.append(itemCode)
				
			session["tmp_cart"] = tmpCart'''

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
				if key != 'id' and val is not None:
					tmpObj['itemcode'] = key
					tmpObj['amt'] = val
					tmpCart.append(tmpObj)

			newQuery = ('SELECT * FROM inventory WHERE itemcode = %s')
			for item in tmpCart:
				cursor.execute(newQuery, (item['itemcode'],))
				item['itemData'] = cursor.fetchone()
			cursor.close()

			#current_app.logger.debug(tmpCart)
			return cors_res(tmpCart)