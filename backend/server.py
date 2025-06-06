"""Server.py"""
import os
import shutil
from datetime import datetime
import json
import configparser
import uuid
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from user import UserManager
from database import try_account_access, add_account

app = Flask(__name__, template_folder="../projects", static_folder="../projects")
socketio = SocketIO(app, cors_allowed_origins="*")

config = configparser.ConfigParser()
config.read("config/service.config")

SECRET_KEY = config["app_keys"]["secret_key"]
app.secret_key = SECRET_KEY
user = UserManager("", "")

PROJECTS_FOLDER_DIR = "../projects"
if not os.path.exists(PROJECTS_FOLDER_DIR):
    os.makedirs(PROJECTS_FOLDER_DIR)

if not os.path.exists("../tasks.json"):
    with open("../tasks.json", "w", encoding="UTF-8") as tasks_file:
        file_template = {
            "tasks": [
                {
                    "name": "How to use",
                    "desc": "This new feature allows you to create tasks and keep track of your workflow",
                    "date": "Today"
                },
            ]
        }
        json.dump(file_template, indent=4, fp=tasks_file)

@socketio.on("connection")
def on_connection():
    """Runs when the frontend connects to the backend"""
    path = "../projects"
    dir_list = os.listdir(path)
    emit('projects_list', dir_list)

@socketio.on("create_project")
def handle_project_creation(project_name, html_filename, css_included, js_included):
    """Handles project creation"""
    project_dir = f"../projects/{project_name}"
    script_dir = f"../projects/{project_name}"
    username = user.get_username

    if ".html" not in html_filename:
        html_filename = html_filename + ".html"

    project_details_template = {
        "project_details": {
            "project_name": f"{project_name}",
            "creation_date": f"{datetime.today().strftime('%Y-%m-%d')}",
            "creator": f"{username}",
            "entry_point": f"{html_filename}",
            "js_file": f"{js_included}",
            "css_file": f"{css_included}"
        }
    }
    json_object = json.dumps(project_details_template, indent=4)


    html_template = f"""<link rel="stylesheet" href="{script_dir.replace('.', '')}/{project_name}.css"/>
<main>

    <script src="{script_dir.replace('.', '')}/{project_name}.js"></script>
</main>
"""

    if not os.path.exists(project_dir):
        if " " not in project_name:
            os.makedirs(project_dir)
            with open(os.path.join(project_dir, f"{html_filename}"), "w",
                      encoding="UTF-8") as file1:
                file1.write(html_template)

                if css_included == "Yes":
                    if not os.path.exists(f"{script_dir}/{project_name}.css"):
                        with open(os.path.join(script_dir, f"{project_name}.css"), "w",
                                encoding="UTF-8") as css_file:
                            css_file.write(f"/* This is the css file for {project_name} */")

                if js_included == "Yes":
                    if not os.path.exists(f"{script_dir}/{project_name}.js"):
                        with open(os.path.join(script_dir, f"{project_name}.js"),
                                  "w",
                                encoding="UTF-8") as js_file:
                            js_file.write(f"// This is the js file for {project_name}")

            with open(os.path.join(project_dir, 'project_details.json'), "w",
                      encoding="UTF-8") as prodetail:
                prodetail.write(json_object)

@socketio.on("delete_project")
def handle_project_deletion(project_name):
    """Handles project deletion"""

    project_dir = f"../projects/{project_name}"

    print(f"Deletion request received folder: {project_dir}")
    try:
        print(f"Project '{project_name}' at {project_dir} was deleted")
        shutil.rmtree(project_dir)
    except OSError as error:
        print(f"Failed to delete project: Error was passed: {error}")

@socketio.on("account_login")
def login_user(account_details):
    """Repsonsible for logging in a user"""
    if try_account_access(username=account_details["user_name"],
                          password=account_details["password"]) is True:
        user.get_username = account_details["user_name"]
        user.is_logged_in = True
        emit("login_successful", user.get_username)
        print(user.get_username)
    else:
        print("Failed to find acc")

@socketio.on("account_signup")
def signup_user(account_details):
    """Repsonsible for signing up in a user"""
    if add_account(username=account_details["user_name"],
                   password=account_details["password"]) is True:
        user.username = account_details["user_name"]
        user.is_logged_in = True
        emit("login_successful", user.get_username)

@socketio.on("logout_user")
def logout():
    """Logs a user out of their account"""
    user.is_logged_in = False
    user.username = ""
    user.id = ""
    emit("successful_logout")

@socketio.on("is_logged_in")
def check_login_status():
    """Checks to see if user is logged in"""
    if user.is_logged_in is True:
        emit("login_status", True)
        return True
    emit("login_status", False)
    return False

@socketio.on("get_tasks")
def get_tasks():
    """Gets all the task from the task file"""
    with open("../tasks.json", "r", encoding="UTF-8") as task_list:
        tasks = json.load(task_list)
        emit("received_tasks", tasks)

@socketio.on("add_task")
def add_task(task):
    """Adds a task to the task list"""
    uuid_gen = uuid.uuid4()
    task_data = {"name": task["task_name"], "desc": task["task_desc"], "date": task["date"], "task_id": str(uuid_gen)}
    if os.path.exists("../tasks.json") and os.path.getsize("../tasks.json") > 0:
        try:
            with open("../tasks.json", "r", encoding="UTF-8") as file:
                data = json.load(file)  # Load existing JSON data
        except json.JSONDecodeError:
            data = {"tasks": []}  # Create a new structure if file is corrupt
    else:
        data = {"tasks": []}  # Initialize structure if file does not exist

    data["tasks"].append(task_data)  # Append the new task

    with open("../tasks.json", "w", encoding="UTF-8") as file:
        json.dump(data, file, indent=4)  # Save updated JSON back to file

@socketio.on("delete_task")
def delete_task(task_name):
    """Deletes a task from the task list"""
    # Check if file exists and has valid JSON
    if os.path.exists("../tasks.json") and os.path.getsize("../tasks.json") > 0:
        try:
            with open("../tasks.json", "r", encoding="UTF-8") as file:
                data = json.load(file)  # Load existing JSON data
        except json.JSONDecodeError:
            print("Invalid JSON data.")
            return
    else:
        print("File does not exist or is empty.")
        return

        # Filter out the task to be deleted
    data["tasks"] = [task for task in data["tasks"] if task["name"] != task_name]

    with open("../tasks.json", "w", encoding="UTF_8") as file:
        json.dump(data, file, indent=4)  # Save updated JSON back to file

    print(f"Task '{task_name}' deleted from {"../tasks.json"}")

@socketio.on("get_project_data")
def get_project_data(project):
    """Gets the requested project's data"""
    render_file = ""
    with open(f"{PROJECTS_FOLDER_DIR}/{project}/project_details.json", encoding="UTF-8") as details:
        json_data = json.load(details)
        render_file = json_data["project_details"]["entry_point"]

    with open(f"{PROJECTS_FOLDER_DIR}/{project}/{render_file}",
              "r", encoding="UTF-8") as project_file:
        lines = project_file.read()
        emit("return_project_data", lines)

@socketio.on("project_write")
def project_write(project, data):
    """This writes the data to the project file"""
    render_file = ""
    with open(f"{PROJECTS_FOLDER_DIR}/{project}/project_details.json", encoding="UTF-8") as details:
        json_data = json.load(details)
        render_file = json_data["project_details"]["entry_point"]

    with open(f"{PROJECTS_FOLDER_DIR}/{project}/{render_file}",
              "w", 
              encoding="UTF-8") as project_file:
        project_file.write(data)

@app.route("/projects/<project_name>")
def projects(project_name):
    """Renders project folder for frontend"""
    with open(f"{PROJECTS_FOLDER_DIR}/{project_name}/project_details.json",
            "r", encoding="UTF-8") as details:
        project_details = json.load(details)
        entry = project_details["project_details"]["entry_point"]
        return render_template(f"{project_name}/{entry}")

# Note: this is not a production server
if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=8000)
