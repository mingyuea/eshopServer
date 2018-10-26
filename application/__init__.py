import os
from flask import Flask
from flask_cors import CORS

def create_app(test_config=None):
	app = Flask(__name__, instance_relative_config=True)
	#CORS(app)
	sk = os.environ['SECRET_KEY']
	app.config.from_mapping(
		SECRET_KEY=sk,
		#DATABASE_URI='mysql://ming@localhost/3306',
	)

	'''if test_config is None:
		app.config.from_pyfile('config.py', silent=False)
	else:
		app.config.from_mapping(test_config)

	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass'''

	#app.config.from_object('config')

	@app.route('/')
	def index():
		return "Server is running"

	@app.route('/test')
	def test():
		tstMsg = "The test environment value is: " + os.environ['TEST_VAL']
		return tstMsg

	import application.db as db
	db.init_app(app)

	import application.auth as auth
	app.register_blueprint(auth.bp)

	import application.operations as operations
	app.register_blueprint(operations.bp)
	
	return app

application = create_app()