"""Server.py"""
import os
import shutil
from datetime import datetime
import json
import configparser
from flask import request
from flask_login import login_user, current_user, logout_user
import flask
from flask_socketio import SocketIO, emit
from user import login_manager, load_user
from database import try_account_access, add_account
from rpc import start_rich_presence, stop_rich_presence
from configuration import ProjectManager, application

app = flask.Flask(__name__)
socketio = SocketIO(app)

config = configparser.ConfigParser()
config.read("config/service.config")

SECRET_KEY = config["app_keys"]["secret_key"]

login_manager.init_app(app)
app.secret_key = SECRET_KEY

RICH_PRESENCE_STATUS = "Discord is not connected"

project = ProjectManager (
  '',
  ''
)

user_data = {
    "username": "",
    "userid": "",
}

PROJECTS_FOLDER_DIR = "./templates/labs/projects"
if not os.path.exists(PROJECTS_FOLDER_DIR):
    os.makedirs(PROJECTS_FOLDER_DIR)

@socketio.on("users_name")
def get_users_name(users_name):
    """Gets a user's name from web local storage"""
    project.user = users_name

@socketio.on("get_projects")
def handle_project_fetching():
    """Handles project fetching"""
    path = "./templates/labs/projects"
    dir_list = os.listdir(path)
    emit('projects_list', dir_list)

@socketio.on("create_project")
def handle_project_creation(project_name, html_filename, css_included, js_included):
    """Handles project creation"""
    if ".html" not in html_filename:
        html_filename = html_filename + ".html"

    project_details_template = {
        "project_details": {
            "project_name": f"{project_name}",
            "creation_date": f"{datetime.today().strftime('%Y-%m-%d')}",
            "creator": f"{project.user}",
            "entry_point": f"{html_filename}",
            "js_file": f"{js_included}",
            "css_file": f"{css_included}"
        }
    }
    json_object = json.dumps(project_details_template, indent=4)

    project_dir = f"./templates/labs/projects/{project_name}"
    script_dir = f"./static/project_scripts/{project_name}"

    html_template = f"""<link rel="stylesheet" href="{script_dir.replace('.', '')}/{project_name}.css"/>
<main>

    <script src="{script_dir.replace('.', '')}/{project_name}.js"></script>
</main>
"""

    if css_included is True or js_included is True:
        if not os.path.exists(script_dir):
            if " " not in project_name:
                os.makedirs(script_dir)

    if css_included is True:
        if not os.path.exists(f"{script_dir}/{project_name}.css"):
            with open(os.path.join(script_dir, f"{project_name}.css"), "w",
                      encoding="UTF-8") as css_file:
                css_file.write(f"/* This is the css file for {project_name} */")

    if js_included is True:
        if not os.path.exists(f"{script_dir}/{project_name}.js"):
            with open(os.path.join(script_dir, f"{project_name}.js"), "w",
                      encoding="UTF-8") as js_file:
                js_file.write(f"// This is the js file for {project_name}")

    if not os.path.exists(project_dir):
        if " " not in project_name:
            os.makedirs(project_dir)
            with open(os.path.join(project_dir, f"{html_filename}"), "w",
                      encoding="UTF-8") as file1:
                file1.write(html_template)
            with open(os.path.join(project_dir, 'project_details.json'), "w",
                      encoding="UTF-8") as prodetail:
                prodetail.write(json_object)
            emit('project_created', project_name)

@socketio.on("delete_project")
def handle_project_deletion(project_name):
    """Handles project deletion"""

    project_dir = f"./templates/labs/projects/{project_name}"
    script_dir = f"./static/project_scripts/{project_name}"

    print(f"Deletion request received foler: {project_dir}")
    try:
        print(f"Project '{project_name}' at {project_dir} was deleted")
        shutil.rmtree(project_dir)
        shutil.rmtree(script_dir)
    except OSError as error:
        print(f"Failed to delete project: Error was passed: {error}")

@socketio.on("activate_rpc")
def activate_discord_rpc():
    """Starts discord rpc on socket request"""
    global RICH_PRESENCE_STATUS
    RICH_PRESENCE_STATUS = "Discord is connected"
    rich_presence_handling()

@socketio.on("request_presence_status")
def rich_presence_handling():
    """Handles sending js discord presence status on refresh"""
    emit("send_presence_data", RICH_PRESENCE_STATUS)

@socketio.on("stop_presence")
def rich_presence_stopper():
    """Handles stopping discord rich presence on socket request"""
    stop_rich_presence()

@socketio.on("connected_to_project")
def handle_project_connections():
    """Handles users connecting to a project"""
    emit("user_connected", project.user, broadcast=True)
    print(f"User: '{project.user}' has connected to the project {project.project_name}")

@socketio.on("request_project_javascript")
def handle_javascript_sending():
    """Handles JavaScript requests"""
    script_dir = f"./static/project_scripts/{project.project_name}/{project.project_name}.js"
    with open(script_dir, "r", encoding="UTF-8") as js_file:
        for lines in js_file:
            emit("javascript_received", lines)

@socketio.on("javascript_file_change")
def handle_javascript_changes(code):
    """Handles JavaScript Changes"""
    script_dir = f"./static/project_scripts/{project.project_name}/{project.project_name}.js"
    with open(script_dir, "w", encoding="UTF-8") as js_file:
        js_file.write(code)

@app.route("/")
def home():
    """Launches the home page"""
    template_string = "home.html"
    u = user_data
    if RICH_PRESENCE_STATUS == "Discord is connected":
        start_rich_presence(f"{project.user} is browsing: Home | {application.app_name}")
    return flask.render_template(
        template_string,
        appName = application.app_name,
        project_name = project.project_name,
        hope = u['username'],
    )

@app.route("/login", methods=["POST", "GET"])
def login():
    """Returns login page"""
    template_string = "login/login.html"

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = try_account_access(username, password)

        if user is True:
            login_user(load_user(username))
            user_data.update({"username":load_user(username).username})
            user_data.update({"userid":load_user(username).get_id()})
            return flask.redirect(flask.url_for('home'))

    return flask.render_template(template_string, appName = application.app_name)

@app.route("/signup", methods=["POST", "GET"])
def signup():
    """Returns signup page"""
    template_string = "signup/signup.html"

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = try_account_access(username, password)

        if user is False:
            add_account(username, password)
            return flask.redirect(flask.url_for('login'))
    return flask.render_template(template_string, appName= application.app_name)

@app.route('/logout')
def logout():
    """Logs a user out"""
    logout_user()
    return flask.redirect(flask.url_for('login'))

@app.route("/projects")
def projects():
    """Returns projects page"""
    template_string = "projects.html"
    if current_user.is_authenticated:
        if RICH_PRESENCE_STATUS == "Discord is connected":
            start_rich_presence(f"{project.user} is browsing: Projects | {application.app_name}")
        return flask.render_template(template_string,
                                    appName = application.app_name)
    else:
        return flask.redirect(flask.url_for('login'))

@app.route("/projects/<project_name>")
def open_project(project_name):
    """Opens a project on users disk"""
    template_string = "base.html"
    project.project_name = project_name
    with open(f'templates/labs/projects/{project_name}/project_details.json', 
              encoding="UTF-8") as details:
        data = json.load(details)
        if RICH_PRESENCE_STATUS == "Discord is connected":
            start_rich_presence(f"{project.user} is Designing: {project_name}")
        return flask.render_template(template_string,
                                    selected_project = f"labs/projects/{project_name}/{data["project_details"]["entry_point"]}",
                                    appName = f"{application.app_name} | {project.project_name}")

@app.route("/editor/<project_name>")
def editor(project_name):
    """Opens editor"""
    template_string = "editor.html"
    project.project_name = project_name
    with open(f'templates/labs/projects/{project_name}/project_details.json',
              encoding="UTF-8") as details:
        data = json.load(details)
        return flask.render_template(template_string,
                                 selected_project = f"labs/projects/{project_name}/{data["project_details"]["entry_point"]}",
                                 appName = "Editor")

@app.errorhandler(404)
def not_found(e):
    """Envokes a 404 page when url not found on server"""
    return flask.render_template("404/404.html", appName = application.app_name), 404


# Note: this is not a production server
if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=8000)
    # app.run(debug=True)
