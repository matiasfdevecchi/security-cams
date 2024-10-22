import TelegramBot, { Message } from "node-telegram-bot-api";
import { Command, commands } from "./Command";

export class CommandHandler {
    constructor(private commands: Command[]) { }

    public async handle(bot: TelegramBot, chatId: number, message: Message): Promise<void> {
        if (message.text === undefined) return;

        if (message.text === '/comandos') {
            if (this.commands.length === 0) {
                // return 'Parece que este bot no sabe hacer nada 😐'
                bot.sendMessage(chatId, 'Parece que este bot no sabe hacer nada 😐');
                return;
            };
            bot.sendMessage(chatId, 'Comandos disponibles:\n' + this.commands.map(c => c.info()).join("\n"));
            return;
        }

        const command = this.commands.find(c => c.isValid(message.text!));

        if (command)
            return await command.execute(bot, chatId, message);

        if (message.text.startsWith("/")) {
            bot.sendMessage(chatId, "Comando inválido, escribe /comandos para ver los comandos disponibles.");
            return;
        }

        return;
    }
}

export const commandHandler = new CommandHandler(commands);