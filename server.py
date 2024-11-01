"""Server.py"""
import os
import shutil
from flask import Flask
import flask
from flask_socketio import SocketIO, emit
from rpc import start_rich_presence
from configuration import ProjectManager, application

app = flask.Flask(__name__)
socketio = SocketIO(app)

RICH_PRESENCE_STATUS = "Discord is not connected"

project = ProjectManager (
  '',
  ''
)

HTML_TEMPLATE = """<main>

</main>
"""

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
    print("Files and directories in '", path, "' :")
    # prints all files
    print(dir_list)
    emit('projects_list', dir_list)

@socketio.on("create_project")
def handle_project_creation(project_name):
    """Handles project creation"""
    path = "./templates/labs/projects"
    dir_list = os.listdir(path)
    print("Files and directories in '", path, "' :")
    # prints all files
    print(dir_list)
    project_dir = f"./templates/labs/projects/{project_name}"
    if not os.path.exists(project_dir):
        if " " not in project_name:
            os.makedirs(project_dir)
            with open(os.path.join(project_dir, 'render.html'), "w", encoding="UTF-8") as file1:
                file1.write(HTML_TEMPLATE)
            emit('project_created', project_name)

@socketio.on("delete_project")
def handle_project_deletion(project_name):
    """Handles project deletion"""
    path = "./templates/labs/projects"
    dir_list = os.listdir(path)
    print("Files and directories in '", path, "' :")
    # prints all files
    print(dir_list)
    project_dir = f"./templates/labs/projects/{project_name}"
    print(f"Deletion request received foler: {project_dir}")
    try:
        print(f"Project '{project_name}' at {project_dir} was deleted")
        shutil.rmtree(project_dir)
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

@socketio.on("connected_to_project")
def handle_project_connections():
    """Handles users connecting to a project"""
    emit("user_connected", project.user, broadcast=True)
    print(f"User: '{project.user}' has connected to the project {project.project_name}")


@app.route("/")
def home():
    """Launches the home page"""
    template_string = "home.html"
    if RICH_PRESENCE_STATUS == "Discord is connected":
        start_rich_presence(f"{project.user} is browsing: Home | {application.app_name}")
    return flask.render_template(
        template_string,
        appName = application.app_name,
        project_name = project.project_name,
    )

@app.route("/projects")
def projects():
    """Returns porjects page"""
    template_string = "projects.html"
    if RICH_PRESENCE_STATUS == "Discord is connected":
        start_rich_presence(f"{project.user} is browsing: Projects | {application.app_name}")
    return flask.render_template(template_string,
                                 appName = application.app_name,
                                 project_name = project.project_name,)

@app.route("/projects/<project_name>")
def open_project(project_name):
    """Opens a project on users disk"""
    template_string = "base.html"
    project.project_name = project_name
    if RICH_PRESENCE_STATUS == "Discord is connected":
        start_rich_presence(f"{project.user} is Designing: {project_name}")
    return flask.render_template(template_string,
                                 selected_project = f"labs/projects/{project_name}/render.html",
                                 appName = f"{application.app_name} | {project.project_name}")

@app.route("/editor/<project_name>")
def editor(project_name):
    """Opens editor"""
    template_string = "editor.html"
    return flask.render_template(template_string,
                                 selected_project = f"labs/projects/{project_name}/render.html",
                                 appName = "Editor")


# Note: this is not a production server
if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=8000)
    # app.run(debug=True)
