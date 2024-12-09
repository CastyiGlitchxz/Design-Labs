/* Main Engine for custom attributes and class minipulation */

const Main = document.querySelector('main')
const javascript_editor = document.getElementsByTagName("javascript_editor");
const JS_Button = document.getElementById("js_button");
const CSS_Button = document.getElementById("css_button");

JS_Button.onclick = function () {
    
}

CSS_Button.onclick = function () {
    
}

const createElement = (type) => {
    const new_element = document.createElement(`${type}`)
    new_element.innerHTML = "New Content";
    Main.appendChild(new_element)
}

const getText = (elem) => {
    elem.innerHTML
}

const setText = (elem, text) => {
    elem.innerHTML = text
}

const addClass = (elem, class_name) => {
    elem.classList.add(class_name)
}

const addId = (elem, id) => {
    elem.setAttribute('id', id)
}

socket.emit("request_project_javascript");

socket.on("javascript_received", (script) => {
    const submit_code_button = document.getElementById("submit_code_button");
    for (let index = 0; index < script.length; index++) {
        javascript_editor[0].getElementsByTagName("code")[0].innerHTML += script[index];
    }

    submit_code_button.onclick = function () {
        socket.emit("javascript_file_change", javascript_editor[0].getElementsByTagName("code")[0].innerHTML)
    }
});