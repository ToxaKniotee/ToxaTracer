from google.appengine.ext import db
from gaesessions import get_current_session

class User(db.Model):
	user_name = db.StringProperty()
	password  = db.StringProperty()
	email     = db.StringProperty()

class Project(db.Model):
	name        = db.StringProperty()
	description = db.StringProperty()
	start_date  = db.DateProperty()
	end_date    = db.DateProperty()
	client      = db.StringProperty()
	user        = db.ReferenceProperty(User, collection_name = "projects")

def add_project(project_name, project_description, project_start_date, project_end_date, project_client, project_arq, project_lang):
	session = get_current_session()
	global_user = session.get("global_user", 0)
	if not global_user:
		return False
	temp_project = Project()
	temp_project.name = project_name
	temp_project.client = project_client
	temp_project.user = global_user
	temp_project.put()
	return True

def return_projects():
	session = get_current_session()
	global_user = session.get("global_user", 0)
	q = dq.Query(Project).filter("user", global_user)
	return q

def check_projects(project_name):
	session = get_current_session()
	global_user = session.get("global_user", 0)
	q = db.Query(Project).filter("user", global_user.user_name)
	q = q.filter("name", project_name)
	result = q.get()
	if not result:
		return True
	return False

def check_username(user_id):
	q = db.Query(User).filter("user_name", user_id)
	player = q.get()
	if not player:
		return True
	return False

def check_email(user_email):
	q = db.Query(User).filter("email", user_email)
	player = q.get()
	if not player:
		return True
	return False

def insert_user(user_name, email, password):
	temp_user = User()
	temp_user.user_name = user_name
	temp_user.password = password
	temp_user.email = email
	temp_user.put()
	print(temp_user.key());

def login_user(username, password):
	q = db.Query(User).filter("user_name", username)
	if not q:
		return False
	q = q.filter("password", password)
	if not q:
		return False
	if q.count() != 1:
		return False
	session = get_current_session()
	global_user = session.get("global_user", 0)
	session["global_user"] = q[0]
	return True