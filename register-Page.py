import webapp2
import os
import jinja2

template_env = jinja2.Environment( loader = jinja2.FileSystemLoader( os.getcwd() ) )

class RegisterPage(webapp2.RequestHandler):
	def get(self):
		template =  template_env.get_template("register.html")
		self.response.out.write( template.render() )

application = webapp2.WSGIApplication( [ ( "/register-Page", RegisterPage ) ], debug = True )