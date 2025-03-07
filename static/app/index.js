const socket = io();

const users_name = window.localStorage.getItem("users_name");
socket.emit("users_name", users_name);

document.addEventListener('DOMContentLoaded', (event) => {
    document.querySelectorAll('pre code').forEach((block) => {
      hljs.highlightElement(block);
    });
});

if (window.matchMedia("(max-width: 80rem)").matches) {
    const navbar = document.getElementsByClassName("nav_home")[0]
    const close_nav = () => {
        navbar.classList.add('nav_closed')
        navbar.classList.remove('nav_opened')
    }

    const open_nav = () => {
        navbar.classList.add('nav_opened')
        navbar.classList.remove('nav_closed')
    }

    const burger_button = document.createElement('button');
    burger_button.innerHTML = '<i class="fa-solid fa-bars"></i>';
    burger_button.classList.add('burger_button');
    burger_button.onclick = function() {
        if (navbar.classList.contains('nav_closed')) {
            open_nav();
        } else if (navbar.classList.contains('nav_opened')) {
            close_nav();
        }
    }
    navbar.insertBefore(burger_button, document.getElementsByClassName('nav_links')[0]);
}