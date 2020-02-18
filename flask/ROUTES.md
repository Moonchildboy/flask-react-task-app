	USERS:
		POST '/REGISTER' <<--allows users to instatiate themeselves in the app
		POST '/LOGIN' <<--takes credentials to use app	
		GET '/LOGGED_IN' <<--tracks current user
		GET '/LOGOUT' <<--allows session to end
	TASKS:
		GET '/' <<-- list of all tasks
		GET '/ID' <<-- show individual task
		POST '/' <<-- create task
		DELETE '/ID' <<-- delete task
		PUT '/ID' <<-- make changes to task 
		POST '/USERID' <<-- relate task owner
		


