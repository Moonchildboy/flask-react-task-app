
import models
from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user
from playhouse.shortcuts import model_to_dict

users = Blueprint('users', 'users')

@users.route('/register', methods=['POST']) 
def register():
	payload = request.get_json()
	payload['email'] = payload['email']
	payload['username'] = payload['username'] 
	#should password be included at this stage?
	try: 
		models.User.get(models.User.email == payload['email'])
		return jsonify(
			data={},
			message="A user with that email",
			status=401
			), 401
	except models.DoesNotExist: 
		created_user = models.User.create(
			username=payload['username'],
			email=payload['email'], 
			password=generate_password_hash(payload['password'])
			)
		login_user(created_user)
		user_dict = model_to_dict(created_user)

		user_dict.pop('password')

		return jsonify(
			data=user_dict,
			message=f"Successfully registered {user_dict['email']}",
			status=201
			), 201 

@users.route('/login', methods=['POST'])
def login(): 
	payload = request.get_json()
	payload['email'] = payload['email'].lower()
	payload['username'] = payload['username'].lower()

	try:
		user = models.User.get(models.User.email == payload['email'])
		user_dict = model_to_dict(user)
		password_is_good = check_password_hash(user_dict['password'], payload['password'])

		if password_is_good:
			login_user(user)
			user_dict.pop('password')
			return jsonify(
				data=user_dict,
				message="Successfully logged in!",
				status=200
				), 200
		else:
			print('try another password, foo')
			return jsonify(
				data={},
				message="email or password is incorrect",
				status=401
				), 401

	except models.DoesNotExist:
		print('username is no good')
		return jsonify(
			data={}, 
			message="email or password is incorrect",
			status=401
			), 401
		#will I need an all route for testing?

@users.route('/logged_in', mehtods=['GET']) #how do I test this route?
def get_logged_in_user():
	if not current_user.is_authenticated:
		return jsonify(
			data={},
			message="No user is currently logged in",
			status=401
			), 401
	else: 
		user_dict = model_to_dict(current_user)
		user_dict.pop('password')
		return jsonify(
			data=user_dict,
			message=f"Current user is {user_dict['email']}",
			status=200
			), 200


@users.route('/logout', methods=['GET'])
def logout():
	login_user()
	return jsonify(
		data={},
		message="Successfully logged out",
		status=200 
		), 200

















