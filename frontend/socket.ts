import { io, Socket } from "socket.io-client";

export const socket: Socket = io("http://localhost:8000", {
    transports: ["websocket"],
    withCredentials: true,
    extraHeaders: {
      "Access-Control-Allow-Origin": "http://localhost:3000"
    }
});