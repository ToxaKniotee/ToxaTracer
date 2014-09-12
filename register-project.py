import webapp2
import jinja2
import os
import models

template_env = jinja2.Environment(loader = jinja2.FileSystemLoader(os.getcwd()))

class RegisterProject(webapp2.RequestHandler):
	def post(self):
		project_name        = self.request.get("project_name")
		project_description = self.request.get("project_description")
		project_start_date  = self.request.get("project_start_date")
		project_end_date    = self.request.get("project_end_date")
		project_client      = self.request.get("project_client")
		project_arq         = self.request.get("project_arq")
		project_lang        = self.request.get("project_lang")

		if models.check_projects(project_name):
			if models.add_project(project_name, project_description, project_start_date, project_end_date, project_client, project_arq, project_lang):
				self.response.out.write("Projecto agregado")
				return;
		self.response.out.write("Error")

application = webapp2.WSGIApplication([("/register-project", RegisterProject)], debug = True)
