import webapp2
import jinja2
import os

template_env = jinja2.Environment( loader = jinja2.FileSystemLoader( os.getcwd() ) )

class LoginPage(webapp2.RequestHandler):
	def get(self):
		template = template_env.get_template("login.html")
		self.response.out.write( template.render() )

application =  webapp2.WSGIApplication( [ ("/login-Page", LoginPage) ], debug = True )