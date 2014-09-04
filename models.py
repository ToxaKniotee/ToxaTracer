from google.appengine.ext import db

class User(db.Model):
	user_name = db.StringProperty()
	password = db.StringProperty()
	email = db.StringProperty()

def check_username(user_id):
	q = db.Query(User).filter("user_name", user_id)
	player = q.get()
	if not player:
		return True
	return False

def check_email(user_email):
	q = Query(User).filter("email".user_email)
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
	return True