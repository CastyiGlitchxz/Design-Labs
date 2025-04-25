import { useEffect, useState } from "react";
import { socket } from "./socket";

function Get_user() {
    const [user, setUser] = useState<string | null>(null);

    useEffect(() => {
        setUser(sessionStorage.getItem("user_name"))
    }, [])

    return user
}

function Is_logged_in() {
    const [status, setStatus] = useState(false)
    socket.emit("is_logged_in");
    
    socket.on("login_status", (result) => {
        if (result === true) {
            setStatus(true)
        }
    })

    return status;
}

socket.on("successful_logout", () => {
    window.location.href = "/login"
})

function logout() {
    socket.emit("logout_user")
    sessionStorage.removeItem("user_name")
}

function login() {
    window.location.href = "/login"
}

export {logout, login, Get_user, Is_logged_in}