from google.appengine.ext import db
from gaesessions import get_current_session
import datetime

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
	no_func_req = db.StringListProperty()

class Roles( db.Model ):
	user = db.ReferenceProperty( User, collection_name = "works" )
	project = db.ReferenceProperty( Project, collection_name = "roles" )
	role = db.StringProperty()

def add_role( user_email, project, role ):
	#recuperamos el usuario
	q = db.Query( User ).filter( "email", user_email )
	q.get()
	user = q[0]

	#Insertamos el nuevo rol
	temp_role = Roles()
	temp_role.user = user
	temp_role.project = project
	temp_role.role = role
	temp_role.put()

def delete_role( key ):
	temp_role = db.get( key )
	temp_role.delete()

def check_user( email ):
	q = db.Query( User ).filter( "email", email )
	user = q.get()
	if not user:
		return False
	return True

def add_project(project_name, project_description, project_start_date, project_end_date, project_client, project_arq, project_lang):
	session = get_current_session()
	global_user = session.get("global_user", 0)
	if not global_user:
		return False
	temp_project             = Project()
	temp_project.description = project_description
	temp_project.name        = project_name
	temp_project.client      = project_client
	temp_project.user        = global_user
	temp_project.start_date  = datetime.datetime.strptime( project_start_date, "%Y-%m-%d" ).date()
	temp_project.end_date    = datetime.datetime.strptime( project_end_date, "%Y-%m-%d" ).date()
	temp_project.no_func_req = []
	temp_project.put()
	session = get_current_session()
	global_project = session.get( "global_project" )
	session["global_project"] = temp_project
	return True

def return_projects():
	session = get_current_session()
	global_user = session.get("global_user", 0)
	q = db.Query(Project).filter("user", global_user)
	q.get()
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