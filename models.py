from google.appengine.ext import db
from google.appengine.api import mail

class User(db.Model):
	user_name = db.StringProperty()
	password = db.StringProperty()
	email = db.StringProperty()
	activated = db.BooleanProperty()

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
	temp_user.activated = False
	temp_user.put()

	#Creamos el correo

	msg = "Activa tu correo en el siguiente enlace\n http://toxa-tracer.appspot.com/activate?v=" + (temp_user.key().id)
	mail.send_mail(
		sender = "admin@toxa-tracer.appspotmail.com",
		to = temp_user.email,
		subject = "Correo de prueba",
		body = msg)

def login_user(username, password):
	q = db.Query(User).filter("user_name", username)
	if not q:
		return False
	q = q.filter("password", password)
	if not q:
		return False
	if q.count() != 1:
		return False
	if q[0].activated == True:
		return True
	return False