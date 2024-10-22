import TelegramBot, { Message } from "node-telegram-bot-api";
import { Command } from "../Command";

export class Imagen implements Command {
    public info(): string {
        return "/imagen";
    }

    public isValid(message: string): boolean {
        return message.match(new RegExp("^/imagen$")) !== null;
    }

    public async execute(bot: TelegramBot, chatId: number, message: Message): Promise<void> {
        try {
            // Enviar una foto
            const imageUrl = "https://www.adslzone.net/app/uploads-adslzone.net/2019/04/borrar-fondo-imagen-1.jpg"; // URL de la imagen o un path local
            await bot.sendPhoto(chatId, imageUrl, {
                caption: "Aquí tienes una imagen 😊"
            });
        } catch (e: any) {
            console.log("¡Oh! Ocasioné un error 😟", e);
        }
    }
}
