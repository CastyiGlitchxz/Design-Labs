const commandsBox = document.getElementById("commands")
const cmdLine = document.getElementById("cmdLine")
var lastMessage;

const print = (message, type) => {
    const command = document.createElement("p")
    command.innerHTML = message
    command.classList.add(type)
    commandsBox.appendChild(command)
}

const passError = (error) => {
    print(error, 'error')
}

const passWarning = (warning) => {
    print(warning, 'warning')
}

const clearTextbox = () => {
    cmdLine.value = ""
}

const clear = () => {
    const text = commandsBox.querySelectorAll('p')
    text.forEach(element => {
        commandsBox.removeChild(element)
    })
}

cmdLine.addEventListener("keydown", (e) => {
    if (event.key === "ArrowUp") {
        cmdLine.value = lastMessage;
    }
})

print("Welcome to console")

const commands = 
[
    print.name, 
    passWarning.name, 
    passError.name, 
    clear.name
]

const commandExist = (command, comparator) => {
    if (command.name != comparator)
    {
        passError(`Command '${comparator}' doesn't exist`)
    }
    else
    {
        print("Works!")
    }
}

cmdLine.addEventListener("keypress", (e) => {
    if (event.key === "Enter") {
        commands.forEach(element => {
                if (cmdLine.value == `${element}()`)
                {
                    `${element} + ()`
                    switch(cmdLine.value) {
                        case "print()":
                            print('test')
                            break;
                        case "passWarning()":
                            passWarning('e')
                            break;
                        case "passError()":
                            passError('e')
                            break;
                        case "clear()":
                            clear()
                            break;
                    }
                }
                lastMessage = cmdLine.value;
        });
    event.preventDefault();
    clearTextbox()
    }
})

cmdLine.innerText