import click
from flask import current_app, g
from flask.cli import with_appcontext
import mysql.connector as mysql

def get_db():
	if 'db' not in g:
		g.db = mysql.connect(
			user=current_app.config['DBUSER'],
			password=current_app.config['DBPASS'],
			host=current_app.config['DBHOST'],
			database=current_app.config['DBNAME']
		)
	return g.db


def close_db(e=None):
	db = g.pop('db', None)

	if db is not None:
		db.close()


def init_db():
	db = get_db()
	cursor = db.cursor()
	itemCodeList = []

	def executeFile(readFile):
		newStatement = ""
		for line in readFile:
			if line[-1] == ';':
				cursor.execute(newStatement)
				newStatement = ""
			else:
				newStatement += line
		db.commit()

	def dataToList(readFile):
		'''
		This will convert a file from lines of string into an array of arrays, which can then
		be used by the cursor.executemany() function. It takes a line, seperates the fields
		using ; as the delineator, converts strings into integers/floats where necessary,
		then appends them to the main array. The main array of arrays is then returned
		'''
		dataArr = []
		dataRow = ""
		for char in readFile:
			if char[-1] == '\n':
				dataRow = dataRow.split(";")
				for ind, chunk in enumerate(dataRow):
					csplit = chunk.split('.')
					if len(csplit) == 1 and csplit[0].isnumeric():
						csplit = int(chunk)
						dataRow[ind] = csplit
					elif len(csplit) == 2 and csplit[0].isnumeric() and csplit[1].isnumeric():
						csplit = float(chunk)
						dataRow[ind] = csplit
				dataArr.append(dataRow)
				dataRow = ""
			else:
				dataRow += char
		return dataArr

	with current_app.open_resource('schema.sql', mode='r') as f:
		statements = f.read()
		executeFile(statements)
		print(type(f))

	with current_app.open_resource('invData.txt', mode='r') as f1:
		fileData = f1.read()
		invData = dataToList(fileData)
		
		insertStmt = "INSERT INTO inventory (itemcode, name, price, rating, descrip, img) VALUES (%s, %s, %s, %s, %s, %s)"
		cursor.executemany(insertStmt, invData)
		#cursor.close()
		db.commit()

	cursor.execute("SELECT itemcode FROM inventory")
	itemCodes = cursor.fetchall()
	createCartTable = "CREATE TABLE cartdata (id INT PRIMARY KEY NOT NULL"
	
	for itemCode in itemCodes:
		createCartTable = createCartTable + ', ' + itemCode[0] + " INT(8)"
	createCartTable += ')'

	cursor.execute(createCartTable)
	db.commit()
	cursor.close()
	db.close()


@click.command('init-db')
@with_appcontext
def init_db_command():
	init_db()
	click.echo('Initialized MySQL database')


def init_app(app):
	app.teardown_appcontext(close_db)
	app.cli.add_command(init_db_command)