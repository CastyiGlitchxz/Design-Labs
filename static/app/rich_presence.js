const socket = io();

const discord_status_text = document.getElementById("discord_status_text");
const discord_status_button = document.getElementById("discord_status_button");
const discord_status_disconnect = document.getElementById("discord_status_disconnect");

socket.emit("request_presence_status");

const set_discord_status = (status) => {
    discord_status_text.innerHTML = status;
};

const start_discord_rpc = () => {
    socket.emit('activate_rpc');
}

const stop_discord_rpc = () => {
    socket.emit('stop_presence');
}

discord_status_button.onclick = function() {
    start_discord_rpc();
};

discord_status_disconnect.onclick = function() {
    stop_discord_rpc();
}

socket.on('send_presence_data', (presence_data) => {
    set_discord_status(presence_data);
});