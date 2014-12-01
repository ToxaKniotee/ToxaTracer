from google.appengine.ext import db
from gaesessions import get_current_session
import datetime

def get(key):
    return db.get(key)

####################################################################################################
## User                                                                                           ##
####################################################################################################

class User(db.Model):
    name = db.StringProperty()
    password = db.StringProperty()
    email = db.StringProperty()
    arq = db.StringListProperty()
    languages = db.StringListProperty()

# Funcion que checa si ya existe un email en la base de datos
def check_email(email):
    query = db.Query(User).filter("email", email)
    user = query.get()
    if not user:
        return False
    return True

# Funcion que inserta un nuevo usuario a la base de datos
def insert_user(name, email, password):
    temp_user = User()
    temp_user.name = name
    temp_user.password = password
    temp_user.email = email
    temp_user.put()

# Funcion que checa si los datos son correctos
def login_user(email, password):
    # Obtenemos el email y checamos que exista
    query = db.Query(User).filter("email", email)
    if not query:
        return False

    # Obtenemos la contrasenia y nos aseguramos de que exista
    query = query.filter("password", password)
    if not query:
        return False

    # Nos aseguramos de que solo exista un valor
    if query.count() != 1:
        return False

    # Guardamos el el session el usuario y regresamos True
    set_global_user(query[0])
    return True

def get_global_user():
    session = get_current_session()
    return session.get("global_user")

def set_global_user(user):
    session = get_current_session()
    session["global_user"] = user

def add_arq(new_arq):
    user = get_global_user()
    user.arq.append(new_arq)
    user.put()
    set_global_user(user)

def add_language(new_language):
    user = get_global_user()
    user.languages.append(new_language)
    user.put()
    set_global_user(user)

####################################################################################################
## Projects                                                                                       ##
####################################################################################################

class Project(db.Model):
    name = db.StringProperty()
    user = db.ReferenceProperty(User, collection_name="projects")
    description = db.StringProperty()
    start_date = db.DateProperty()
    end_date = db.DateProperty()
    client = db.StringProperty()
    no_func_req = db.StringListProperty()
    owner = db.StringProperty()
    percentage = db.IntegerProperty()
    arq = db.StringProperty()
    language = db.StringProperty()

def add_project(project_name, project_description, project_start_date, project_end_date,
        project_client, project_owner, project_arq, project_lang):
    # Obtenemos el usuario
    global_user = get_global_user()

    # Creamos el projecto
    temp_project = Project()
    temp_project.description = project_description
    temp_project.name = project_name
    temp_project.client = project_client
    temp_project.owner = project_owner
    temp_project.user = global_user
    temp_project.start_date = datetime.datetime.strptime(project_start_date, "%d-%m-%Y").date()
    temp_project.end_date = datetime.datetime.strptime(project_end_date, "%d-%m-%Y").date()
    temp_project.no_func_req = []
    temp_project.arq = project_arq
    temp_project.language = project_lang
    temp_project.percentage = 0
    temp_project.put()

    # Regresamos el key del proyecto
    return temp_project.key()

def get_global_project():
    session = get_current_session()
    return session.get("global_project")

####################################################################################################
## Role                                                                                           ##
####################################################################################################

class Role(db.Model):
    email = db.StringProperty()
    project = db.ReferenceProperty(Project, collection_name="roles")
    role = db.StringProperty()

def add_role(user_email, project, role):
    #Insertamos el nuevo rol
    temp_role = Role()
    temp_role.email = user_email
    temp_role.project = project
    temp_role.role = role
    temp_role.put()

def delete_role(key):
    temp_role = db.get(key)
    temp_role.delete()

####################################################################################################
## Release                                                                                        ##
####################################################################################################

class Release(db.Model):
    name = db.StringProperty()
    description = db.StringProperty()
    release_date = db.DateProperty()
    percentage = db.IntegerProperty()
    requirements = db.StringListProperty()
    project = db.ReferenceProperty(Project, collection_name="releases")

def add_release(name, description, release_date, percentage, project):
    temp_release = Release()
    temp_release.name = name
    temp_release.description = description
    temp_release.release_date = datetime.datetime.strptime(release_date, "%d-%m-%Y").date()
    temp_release.percentage = int(percentage)
    temp_release.project = project
    temp_release.put()

####################################################################################################
## User's Stories                                                                                 ##
####################################################################################################

class UserStory(db.Model):
    name = db.StringProperty()
    priority = db.IntegerProperty()
    required_days = db.IntegerProperty()
    engineer = db.StringProperty()
    start_date = db.DateProperty()
    end_date = db.DateProperty()
    percentage = db.IntegerProperty()
    release = db.ReferenceProperty(Release, collection_name="user_stories")

def add_user_story(name, priority, required_days, engineer, start_date, end_date, percentage, release):
    temp_story = UserStory()
    temp_story.name = name
    temp_story.priority = int(priority)
    temp_story.required_days = int(required_days)
    temp_story.engineer = engineer
    temp_story.start_date = datetime.datetime.strptime(start_date, "%d-%m-%Y").date()
    temp_story.end_date = datetime.datetime.strptime(end_date, "%d-%m-%Y").date()
    temp_story.percentage = int(percentage)
    temp_story.release = release
    temp_story.put()
    return temp_story

####################################################################################################
## Tasks                                                                                          ##
####################################################################################################

class Task(db.Model):
    name = db.StringProperty()
    description = db.StringProperty()
    priority = db.IntegerProperty()
    start_date = db.DateProperty()
    required_hours = db.IntegerProperty()
    percentage = db.IntegerProperty()
    user_story = db.ReferenceProperty(UserStory, collection_name="tasks")

def add_task(name, description, priority, start_date, required_hours, percentage, user_story):
    temp_task = Task()
    temp_task.name = name
    temp_task.description = description
    temp_task.priority = int(priority)
    temp_task.start_date = datetime.datetime.strptime(start_date, "%d-%m-%Y").date()
    temp_task.required_hours = int(required_hours)
    temp_task.percentage = int(percentage)
    temp_task.user_story = user_story
    temp_task.put()
    return temp_task

####################################################################################################
## Tests                                                                                          ##
####################################################################################################

class Test(db.Model):
    name = db.StringProperty()
    task = db.ReferenceProperty(Task, collection_name="tests")

def add_test(name, task):
    temp_test = Test()
    temp_test.name = name
    temp_test.task = task
    temp_test.put()
    return temp_test
