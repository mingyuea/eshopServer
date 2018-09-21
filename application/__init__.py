import os
from flask import Flask
from flask_cors import CORS

def create_app(test_config=None):
	app = Flask(__name__, instance_relative_config=True)
	CORS(app)
	app.config.from_mapping(
		SECRET_KEY='dev',
		#DATABASE_URI='mysql://ming@localhost/3306',
	)

	if test_config is None:
		app.config.from_pyfile('config.py', silent=False)
	else:
		app.config.from_mapping(test_config)

	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass

	from . import db
	db.init_app(app)

	from . import auth
	app.register_blueprint(auth.bp)

	return app