import TelegramBot, { Message } from "node-telegram-bot-api";
import { Imagen } from "./implementations/Imagen";

export interface Command {
    info(): string;
    isValid(message: string): boolean;
    execute(bot: TelegramBot, chatId: number, message: Message): Promise<void>;
}

export const commands = [new Imagen()];