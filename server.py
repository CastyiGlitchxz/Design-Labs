"""Server.py"""
import os
from flask import Flask
import flask
from flask_socketio import SocketIO, emit
from configuration import projectManager, application

app = flask.Flask(__name__)
socketio = SocketIO(app)

project = projectManager (
  '',
  'CastyiGlitchxz'
)

HTML_TEMPLATE = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        {% include 'header.html' %}
        <title>{{appName}}</title>
    </head>
    <body>
        
    </body>
    </html>
"""
projects_folder_dir = f"./templates/labs/projects"
if not os.path.exists(projects_folder_dir):
    os.makedirs(projects_folder_dir)

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
        os.makedirs(project_dir)
        with open(os.path.join(project_dir, 'render.html'), "w", encoding="UTF-8") as file1:
            file1.write(HTML_TEMPLATE)
    emit('project_created', project_name)

@app.route("/")
def home():
    """Launches the home page"""
    template_string = "home.html"
    return flask.render_template(
        template_string,
        appName = application.appName,
        project_name = project.projectName,
    )

@app.route("/projects/<project_name>")
def open_project(project_name):
    """Opens a project on users disk"""
    template_string = "base.html"
    project.projectName = project_name
    # start_rich_presence(f"{project.user} has the project: {project.projectName} opened")
    return flask.render_template(template_string,
                                 selected_project = f"labs/projects/{project_name}/render.html",
                                 appName = f"{application.appName} | {project.projectName}")

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
    app.run(debug=True)
