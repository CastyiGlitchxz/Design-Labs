const socket = io();

const users_name = window.localStorage.getItem("users_name");
let isKeyDown = false;
let all_connected_users = [];

socket.emit("users_name", users_name);

const create_user_list = () => {
    let list = document.createElement("div");
    list.classList.add("user_list");
    list.hidden = true;

    document.body.appendChild(list);
}

const open_user_list = () => {
    let user_list = document.getElementsByClassName("user_list")[0];
    user_list.hidden = false;
};

const close_user_list = () => {
    let user_list = document.getElementsByClassName("user_list")[0];
    user_list.hidden = true;
};

const add_user_toList = (user_name) => {
    let user_list = document.getElementsByClassName("user_list")[0];
    const user = document.createElement("button");
    user.innerHTML = user_name;

    user_list.appendChild(user);
};

document.addEventListener('keydown', function(event) {
    if (event.key === "p") {
        isKeyDown = true;
        open_user_list();
    }
});

document.addEventListener('keyup', function(event) {
    if (event.key === 'p') { 
        isKeyDown = false;
        close_user_list();
      }
});

socket.emit("connected_to_project");

socket.on("user_connected", (user) => {
    create_user_list();
    console.log(`${user} has connected to project`);
    if (!all_connected_users.includes(user)) {
        all_connected_users.push(user);
        for (let index = 0; index < all_connected_users.length; index++) {
            add_user_toList(all_connected_users[index]);
        }
    }
});