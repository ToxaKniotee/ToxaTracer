import webapp2
import jinja2
import os
import models
import time
from gaesessions import get_current_session

template_env = jinja2.Environment( loader = jinja2.FileSystemLoader( os.getcwd() ) )

class IndexPage(webapp2.RequestHandler):

	def get(self):
		template = template_env.get_template("html/index.html")
		self.response.out.write( template.render() )

class LoginPage(webapp2.RequestHandler):

	def get(self):
		template = template_env.get_template("html/login.html")
		self.response.out.write( template.render() )

	def post(self):
		username = self.request.get("name")
		password = self.request.get("pass")

		if( username != "" and password != "" ) and models.login_user(username, password):
			self.redirect( "/main" )
			return

		context = {
			"message": "User/Password incorrectos"
		}

		template = template_env.get_template("html/login.html")
		self.response.out.write( template.render( context ) )

class RegisterPage(webapp2.RequestHandler):

	def get(self):
		template = template_env.get_template("html/register.html")
		self.response.out.write( template.render() )

	def post( self ):
		username   = self.request.get( "name" )
		email      = self.request.get( "email" )
		password   = self.request.get( "pass" )
		password_c = self.request.get( "pass_c" )

		if( not models.check_username( username ) ):
			context = {
				"message": "Username already exist"
			}

			template = template_env.get_template("html/register.html")
			self.response.out.write( template.render( context ) )
			return

		if( not models.check_email( email ) ):
			context = {
				"message": "Email already exist"
			}

			template = template_env.get_template("html/register.html")
			self.response.out.write( template.render( context ) )
			return

		if password == password_c:
			models.insert_user( username, email, password )
			self.response.out.write( "Registro Exitoso" )
			return

		context = {
			"message": "An Error ocurred"
		}

		template = template_env.get_template("html/register.html")
		self.response.out.write( template.render( context ) )

class RegisterProject( webapp2.RequestHandler ):

	def get( self ):
		template = template_env.get_template( "html/register-project.html" )
		self.response.out.write( template.render() )

	def post( self ):
		project_name        = self.request.get("project_name")
		project_description = self.request.get("project_description")
		project_start_date  = self.request.get("project_start_date")
		project_end_date    = self.request.get("project_end_date")
		project_client      = self.request.get("project_client")
		project_arq         = self.request.get("project_arq")
		project_lang        = self.request.get("project_lang")

		if models.check_projects( project_name ):
			if models.add_project( project_name, project_description, project_start_date, project_end_date, project_client, project_arq, project_lang ):
				self.redirect( "/req" )
				return
			self.response.out.write( "Error" )

class MainPage( webapp2.RequestHandler ):

	def get( self ):
		session = get_current_session()
		global_user = session.get( "global_user" )
		projects = models.return_projects();

		context = {
			"Username": global_user.user_name,
			"projects": projects
		}

		template = template_env.get_template( "html/main.html" )
		self.response.out.write( template.render( context ) )

class ReqPage( webapp2.RequestHandler ):

	def get( self ):
		session = get_current_session()
		global_project = session.get( "global_project" )

		#Se elimina el requerimiento
		v = self.request.get( "v" )
		if v:
			del global_project.no_func_req[int( v ) - 1]
			global_project.put()
			session["global_project"] = global_project
			self.redirect( "/req" )
			return

		# Se elimina un rol
		d = self.request.get( "d" )
		if d:
			models.delete_role( d )
			self.redirect( "/req" )
			return

		# Una espera insignificativa para que le de tiempo a la base de datos de actualizar la informacion
		time.sleep( 0.1 )

		context = {
			"name": global_project.name,
			"req": global_project.no_func_req,
			"roles": global_project.roles
		}

		template = template_env.get_template( "html/project-req.html" )
		self.response.out.write( template.render(context) )

	def post( self ):
		session = get_current_session()
		global_project = session.get( "global_project" )
		type_post = self.request.get( "type_post" )

		# Requerimientos no funcionales
		if type_post == "type_req":
			global_project.no_func_req.append( self.request.get( "txt_add_req" ) )

		# Roles
		if type_post == "type_role":
			models.add_role( self.request.get( "txt_user" ), global_project, self.request.get( "txt_role" ) )

		global_project.put()
		session["global_project"] = global_project
		self.redirect( "/req" )

application = webapp2.WSGIApplication( [ ("/", IndexPage), ("/login", LoginPage), ( "/register", RegisterPage ), ( "/register-project", RegisterProject ), ( "/main", MainPage ), ( "/req", ReqPage ) ], debug=True )