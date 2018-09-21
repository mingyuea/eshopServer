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

	def executeFile(readFile):
		newStatement = ""
		for line in readFile:
			if line[-1] == ';':
				cursor.execute(newStatement)
				newStatement = ""
			else:
				newStatement += line
		cursor.close()
		db.commit()

	with current_app.open_resource('schema.sql', mode='r') as f:
		statements = f.read()
		executeFile(statements)
		print(type(f))
		#write a function that will execute init schema.sql

@click.command('init-db')
@with_appcontext
def init_db_command():
	init_db()
	click.echo('Initialized MySQL database')

def init_app(app):
	app.teardown_appcontext(close_db)
	app.cli.add_command(init_db_command)