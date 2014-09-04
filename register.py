import webapp2
import jinja2
import os
import models

template_env = jinja2.Environment( loader = jinja2.FileSystemLoader( os.getcwd() ) )

class Register(webapp2.RequestHandler):
	def post(self):
		username = self.request.get("name")
		email = self.request.get("email")
		password = self.request.get("pass")
		password_c = self.request.get("pass_c")

		if models.check_username(username) and password == password_c and models.check_email(email):
			models.insert_user(username, email, password)
			self.response.out.write("Registro exitoso")
			return
		self.response.out.write("Error de registro")

application = webapp2.WSGIApplication( [("/register", Register)], debug=True )