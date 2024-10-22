import TelegramBot, { Message } from "node-telegram-bot-api";
import { commandHandler } from "./commands/CommandHandler";

export class Bot {
  constructor(private token: string) { }

  public start() {
    const bot = new TelegramBot(this.token, { polling: true });
    bot.on('message', async (message: Message) => {
      const chatId = message.chat.id;
      await commandHandler.handle(bot, chatId, message);
    });
  }
}