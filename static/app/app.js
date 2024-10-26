//import { Client } from "../../node_modules/discord-rpc";

const connection = window.localStorage.getItem('debugMode');
const cmdConsole = document.querySelector('console');

if (connection != 'true') 
{
    cmdConsole.setAttribute('style', 'display: none');
} 
else
{
    cmdConsole.setAttribute('style', 'display: grid');
}