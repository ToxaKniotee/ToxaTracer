import webapp2
import jinja2
import os
import models
import time
from gaesessions import get_current_session

TEMPLATE_ENV = jinja2.Environment(loader=jinja2.FileSystemLoader(os.getcwd()))

class IndexPage(webapp2.RequestHandler):
    def get(self):
        render_page(self, "login.html")

    def post(self):
        # Obtenemos el email y el password
        email = self.request.get("email_login")
        password = self.request.get("pass_login")

        # Nos aseguramos de que no son vacios y mandamos a llamar a la funcion para validar los
        # datos
        if email != "" and password != "" and models.login_user(email, password):
            self.redirect("/main")
            return

        # Datos invalidos o error
        render_page(self, "login.html", {"error_message": True})

class RegisterPage(webapp2.RequestHandler):
    def get(self):
        render_page(self, "register.html")

    def post(self):
        username = self.request.get("name_register")
        email = self.request.get("email_register")
        password = self.request.get("password_register")
        password_c = self.request.get("password_confirmation_register")

        # Checamos que no eista el mismo email
        if models.check_email(email):
            render_page(self, "register.html", {
                "class": "danger",
                "message": "Email already exists"})
            return

        # Checamos que las contrasenias sean las mismas
        if password == password_c:
            # Insertamos el usuario
            models.insert_user(username, email, password)
            render_page(self, "register.html", {
                "class": "success",
                "message": "Successful registration!"})
            return

        render_page(self, "register.html", {
            "class": "danger",
            "message": "An unknow error has occurred"})

class MainPage(webapp2.RequestHandler):
    def get(self):
        # Obtenemos el usuario que se acaba de registrar y lo regresamos
        global_user = models.get_global_user()
        render_page(self, "projects.html", {"user": global_user})

    def post(self):
        action = self.request.get("action")
        print "post"

        # Agregar Proyecto
        if action == "add_project":
            project_name = self.request.get("name_project")
            project_description = self.request.get("description_project")
            project_start_date = self.request.get("input_start_date_project")
            project_end_date = self.request.get("input_completition_date_project")
            project_client = self.request.get("client_project")
            project_arq = self.request.get("architecture_project")
            project_lang = self.request.get("language_project")
            project_owner = self.request.get("owner_project")

            # Agregamos el proyecto
            project_key = models.add_project(project_name, project_description, project_start_date,
                project_end_date, project_client, project_owner, project_arq, project_lang)
            self.redirect("/project?project=" + str(project_key))
            return
        # Agregar arquitectura
        elif action == "add_arq":
            models.add_arq(self.request.get("architecture_project"))
            self.redirect("/main#architecture_section")
        # Agregar lenguaje
        elif action == "add_language":
            models.add_language(self.request.get("language_project"))
            self.redirect("/main#language_section")

class ProjectPage(webapp2.RequestHandler):
    def get(self):
        project = models.get(self.request.get("project"))

        # Una espera insignificativa para que le de tiempo a la base de datos de actualizar la
        # informacion
        time.sleep(0.1)

        context = {"project" : project}
        render_page(self, "project.html", context)

    def post(self):
        project = models.get(self.request.get("project"))
        action = self.request.get("action")
        post = ""

        # Agregar requerimientos no funcionales
        if action == "add_requirement":
            project.no_func_req.append(self.request.get("requirement_project"))
            post = "#requirements_section"
        # Eliminar requerimientos no funcionales
        elif action == "remove_requirement":
            index = int(self.request.get("index"))
            del project.no_func_req[index]
            post = "#requirements_section"
        # Agregar Rol
        elif action == "add_role":
            email = self.request.get("email_rol_project")
            role = self.request.get("name_rol_project")
            models.add_role(email, project, role)
            post = "#roles_section"
        # Eliminar rol
        elif action == "remove_role":
            models.delete_role(self.request.get("index"))
            post = "#roles_section"
        # Agregar Release
        elif action == "add_release":
            name = self.request.get("name_release")
            description = self.request.get("description_release")
            release_date = self.request.get("input_deadline_release")
            percentage = self.request.get("percentage_release")
            models.add_release(name, description, release_date, percentage, project)
            post = "#releases_section"

        project.put()
        self.redirect("/project?project=" + str(project.key()) + post)

class ReleasePage(webapp2.RequestHandler):
    def get(self):
        release = models.get(self.request.get("release"))
        context = {"release": release}

        # Una espera insignificativa para que le de tiempo a la base de datos de actualizar la
        # informacion
        time.sleep(0.1)

        render_page(self, "release.html", context)

    def post(self):
        release = models.get(self.request.get("release"))
        action = self.request.get("action")
        post = ""

        # Agregar una historia de usuario
        if action == "add_user_story":
            name = self.request.get("name_story")
            priority = self.request.get("priority_story")
            required_days = self.request.get("days_story")
            engineer = self.request.get("responsible_story")
            start_date = self.request.get("input_start_date_story")
            end_date = self.request.get("input_completition_date_story")
            percentage = self.request.get("percentage_story")
            models.add_user_story(
                name, priority, required_days, engineer, start_date, end_date, percentage, release)
            post = "#user_histories_section"
        # Agregar requerimiento
        elif action == "add_requirement":
            release.requirements.append(self.request.get("requirements_description_release"))
            release.put()
            post = "#portafolio"
        # Eliminar requerimiento
        elif action == "remove_requirement":
            index = int(self.request.get("index")) - 1
            del release.requirements[index]
            release.put()
            post = "#portafolio"

        self.redirect("/release?release=" + str(release.key()) + post)

class UserStoryPage(webapp2.RequestHandler):
    def get(self):
        user_story = models.get(self.request.get("user_story"))
        context = {"user_story": user_story}

        # Una espera insignificativa para que le de tiempo a la base de datos de actualizar la
        # informacion
        time.sleep(0.1)

        render_page(self, "story.html", context)

    def post(self):
        user_story = models.get(self.request.get("user_story"))
        action = self.request.get("action")

        # Agregamos una nueva tarea
        if action == "add_task":
            name = self.request.get("name_task")
            description = self.request.get("description_task")
            priority = self.request.get("priority_task")
            start_date = self.request.get("input_start_date_task")
            required_hours = self.request.get("hours_task")
            percentage = self.request.get("percentage_task")
            models.add_task(
                name, description, priority, start_date, required_hours, percentage, user_story)

        self.redirect("/story?user_story=" + str(user_story.key()))

class TaskPage(webapp2.RequestHandler):
    def get(self):
        task = models.get(self.request.get("task"))

        # Una espera insignificativa para que le de tiempo a la base de datos de actualizar la
        # informacion
        time.sleep(0.2)

        context = {"task": task}
        render_page(self, "task.html", context)

    def post(self):
        task = models.get(self.request.get("task"))
        action = self.request.get("action")

        # Agregar test
        if action == "add_test":
            name = self.request.get("name_test")
            models.add_test(name, task)

        self.redirect("/task?task=" + str(task.key()))

def render_page(page_app, web_page, context=None):
    # Inicializamos el contexto en caso de ser vacio
    if context is None:
        context = {}
    template = TEMPLATE_ENV.get_template("assets/html/" + web_page)
    page_app.response.out.write(template.render(context))

APP = webapp2.WSGIApplication(
    [
        ("/", IndexPage), ("/register", RegisterPage), ("/main", MainPage),
        ("/project", ProjectPage), ("/release", ReleasePage), ("/story", UserStoryPage),
        ("/task", TaskPage)],
    debug=True)
