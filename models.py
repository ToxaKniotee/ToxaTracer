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

def insert_user(user_name, email, password):
	temp_user = User()
	temp_user.user_name = user_name
	temp_user.password = password
	temp_user.email = email
	temp_user.put()