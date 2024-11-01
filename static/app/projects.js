const socket = io();
let selected_project = "";
let total_projects = [];

const project_creation_button = document.getElementById("project_creation_button");

const get_projects = () => {
    socket.emit('get_projects');
};
get_projects();

socket.on('projects_list', (projects) => {
    total_projects = projects;
    const projects_list = document.getElementById('projects_list');
    const delete_project_button = document.getElementById("delete_project_button");
    const open_project_button = document.getElementById("open_project_button");

    for (let index = 0; index < projects.length; index++) {
        const project = document.createElement('div');
        project.innerHTML = projects[index];
        project.classList.add("project_buttons");
        project.setAttribute('project_name', projects[index]);
        project.onclick = function() {
            selected_project = projects[index];
            console.log(selected_project);
            if (selected_project === projects[index]) {
                delete_project_button.hidden = false;
                open_project_button.hidden = false;

                project.classList.add("selected");
            }

            delete_project_button.onclick = function() {
                let deletion_message = prompt(`Type your project's name to delete "${selected_project}" `);

                if (deletion_message === selected_project) {
                    socket.emit("delete_project", selected_project);
                    document.querySelector(`[project_name='${selected_project}']`).remove();
                }
            }

            open_project_button.onclick = function(key) {
                if (key.shiftKey) {
                    window.location.href = `/editor/${projects[index]}`;
                } else {
                    window.location.href = `/projects/${projects[index]}`;
                }
            }

            project.ondblclick = function(key) {
                if (key.shiftKey) {
                    window.location.href = `/editor/${projects[index]}`;
                } else {
                    window.location.href = `/projects/${projects[index]}`;
                }    
            }
        }
        projects_list.appendChild(project);
    }
});

const createProject = () => {
    const project_creation_input = document.getElementById('project_creation_input');
    if (project_creation_input.value != "") {
        let project_name = project_creation_input.value;
        socket.emit('create_project', project_name);
    }
}

project_creation_button.onclick = function() {
    createProject();
};

socket.on('project_created', (project_name) => {
    window.location.href = `/projects/${project_name}`;
});