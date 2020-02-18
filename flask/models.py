from peewee import *

from flask_login import UserMixin

DATABASE=SqliteDatabase('task.sqlite')

class User(UserMixin, Model): 
	username=CharField(unique=True)
	email=CharField(unique=True)
	password=CharField()

	class Meta:
		database = DATABASE

class Task(Model):
	title=CharField()
	supporting_action=CharField()
	status=CharField() #should take four values
	actor=ForeignKeyField(User, backref='task')
	# date=CharField() #(1).is CharField the correct value? (2).do I want/need to include 

	class Meta:
		database = DATABASE


def initialize():
	DATABASE.connect()
	DATABASE.create_tables([User, Task], safe=True)
	print('connected to DB')
	DATABASE.close()