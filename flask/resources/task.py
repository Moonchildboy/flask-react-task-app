import models

from flask import Blueprint, request, jsonify
from flask_login import current_user,login_required
from playhouse.shortcuts import model_to_dict

task =  Blueprint('task', 'task')

@task.route('/', methods=['GET'])
@login_required
def task_index():
	current_user_task_dicts = [model_to_dict(task) for task in current.user.task]	
	print(current_user_task_dicts)

	return jsonify(
		data=current_user_task_dicts, 
		message="Successfully retrieved tasks",
		status=200
		), 200


@task.route('/<id>', methods=['GET'])
def get_one_task(id):
	task = models.Task.get_by_id(id)#hmmm, how are id's uniqely identified for tasks? 
	if not current_user.is_authenticated:
		return jsonify(
			data={
			'title': task.title, 
			'supporting_action': task.supporting_action 
			'status': task.status #will this be confusing? 
			}, 
			status=200
			), 200

	else: task_dict = model_to_dict(task)
		  task_dict['task'].pop('password')
		  if task.actor_id != current_user.id:
		  	task_dict.pop('created_at')
		  return jsonify(
		  		data=task_dict,
		  		message=f"Found task{task.id}",
		  		status=200
		  		), 200	

@task.route('/', methods=['POST'])
@login_required
def create_task():
	payload = request.get_json()
	print(payload)
	task = models.Task.create(
		title=payload['title'], 
		supporting_action=payload['supporting_action'],
		actor=current_user.id
	)
	print(task.__dict__)

	task_dict=model_to_dict(task)
	task_dict['actor'].pop('password')

	return jsonify(
		data=task_dict, 
		message="Successfully added task",
		status=201
		), 201

# tenatively skipping delete route; see update route below: 

@task.route('/<id>', methods=['PUT'])
@login_required
def update_task(id): 
	payload = request.get_json()
	task = models.Task.get_by_id(id)
	if task.actor.id == current_user.id:
		task.title = payload['title'] if 'title' in payload else None
		task.supporting_action = payload['supporting_action'] if 'supporting_action' in payload else None
		task.status = payload['status'] if 'status' in payload else None
		task.save()
		task_dict = model_to_dict(task)

		return jsonify(
			data=task_dict, 
			message="Successfully updated task!",
			status=200
			), 200
	else:
		return jsonify(
			data={
			'error':'Forbidden'
			},
			message=f"Task's actor_id({task.actor.id}) does not match that of the logged in user",
			status=403 
			), 403

@task.route('/<actor_id>', methods=['POST'])
def create_task_w_actor(actor_id):
	payload = request.get_json()
	print(payload)
	task = models.Task.create(
		title=payload['title'],
		supporting_action=payload['supporting_action'],
		status=actor_id
		)
	task_dict = model_to_dict(task)
	print(task_dict)

	task_dict['actor'].pop('password')

	return jsonify(
		data=task_dict, 
		message="Successfully created task",
		status=201
		), 201

@task.route('/<id>', methods=['Delete'])
def delete_task(id):
	task_to_delete = models.Task.get_by_id(id)
	if current_user.id == task_to_delete.actor.id:
		task_to_delete.delete_instance()
		return jsonify(
			date={},
			message="Successfully deleted task",
			status=200
			), 200
	else: 
		return jsonify(
			data={
			'error': 'Forbidden'
			}, 
			message="Task's actor_id does not match logged in user", 
			status=403
			), 403








