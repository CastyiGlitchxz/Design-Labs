/* eslint-disable @typescript-eslint/no-explicit-any */
/* eslint-disable @next/next/no-img-element */

'use client'

import login_styling from "./login.module.css"
import favicon from "../favicon.ico"
import { useEffect, useState } from "react"
import { socket } from "../../../socket"

export default function Signup() {
    const [accountData, setaccountData] = useState({
        user_name: "",
        password: "",
    })

    const setInformation = (event: any) => {
        const {name, value} = event.target;
        setaccountData(prevState => ({
            ...prevState,
            [name]: value,
        }));
    };

    function signup() {
        socket.emit("account_signup", accountData);
    }

    useEffect(() => {
        socket.once("login_successful", (data) => {
            sessionStorage.setItem("user_name", data);
            window.location.href = ".";
        })
    })

    return (
        <div className={login_styling["login-container"]}>
            <div className={login_styling["login-centered-content"]}>
                <img src={favicon.src} width="90" height="90" id={login_styling["logo"]} alt="Something meaningful"/>

                <div className={login_styling["input-container"]}>
                    <span className={login_styling["login-input-container"]}>
                        <i className="fa-regular fa-circle-user"></i>
                        <input type="text" name="user_name" id="" placeholder="Username" required onChange={setInformation}/>
                    </span>

                    <span className={login_styling["login-input-container"]}>
                        <i className="fa-solid fa-lock"></i>
                        <input type="password" name="password" id="" placeholder="Password" required onChange={setInformation}/>
                    </span>
                </div>

                <button className={login_styling["login-button"]} onClick={() => signup()}>Signup</button>
                <a href="/login">Have an account?</a>
            </div>
        </div>
    )
}