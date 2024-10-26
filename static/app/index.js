const socket = io();

const get_projects = () => {
    socket.emit('get_projects');
};
get_projects();

socket.on('projects_list', (projects) => {
    const projects_list = document.getElementById('projects_list');
    for (let index = 0; index < projects.length; index++) {
        const project = document.createElement('button');
        project.innerHTML = projects[index];
        project.onclick = function(key) {
            if (key.shiftKey) {
                window.location.href = `/editor/${projects[index]}`;
            } else {
                window.location.href = `/projects/${projects[index]}`;
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

socket.on('project_created', (project_name) => {
    window.location.href = `/projects/${project_name}`;
});