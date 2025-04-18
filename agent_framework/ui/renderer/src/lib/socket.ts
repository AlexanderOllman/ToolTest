import { io } from "socket.io-client";
import { getEndpoint } from "./config";

export const socket = io(getEndpoint("socketIO")); 