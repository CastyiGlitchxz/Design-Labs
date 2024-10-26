/* Main Engine for custom attributes and class minipulation */

const Main = document.querySelector('main')

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