from flask import Flask, jsonify, g
from flask_login import LoginManager

from resources.users import users

import models

DEBUG = True
PORT = 8000

app = Flask(__name__)

app.secret_key = "Help is quantum"

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(userid):
	try:
		return models.User.get(models.User.id == userid)
	except models.DoesNotExist: 
		return None

app.register_blueprint(users, url_prefix='/api/v1/users')

@app.before_request
def before_request():

	g.db = models.DATABASE
	g.db.connect()

@app.after_request
def after_request(response):
	g.db.close()
	return response


if __name__ == '__main__':
	models.initialize()
	app.run(debug=DEBUG, port=PORT
		)
