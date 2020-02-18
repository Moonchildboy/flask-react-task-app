
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