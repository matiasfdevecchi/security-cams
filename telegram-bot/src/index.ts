import { config } from 'dotenv';
import startTelegram from './delivery/telegram';

config();

console.log("Security Cam BOT v0.0.1")

startTelegram();