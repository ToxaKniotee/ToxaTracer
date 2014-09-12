import webapp2
import jinja2
import os
import models

template_env = jinja2.Environment( loader = jinja2.FileSystemLoader( os.getcwd() ) )

class Login(webapp2.RequestHandler):
	def post(self):
		username = self.request.get("name")
		password = self.request.get("pass")

		if (username != "" and password != "") and models.login_user(username, password):
			template = template_env.get_template("login-r.html")
			self.response.out.write(template.render())
			return
		self.response.out.write("Error de login")

application = webapp2.WSGIApplication( [("/login", Login)], debug=True )