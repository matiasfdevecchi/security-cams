import { Bot } from "./Bot";

const startTelegram = async () => {
    console.log("Starting Telegram Bot");
    const token = process.env.TELEGRAM_TOKEN;
    if (token === undefined)
        throw new Error("TELEGRAM_TOKEN is not defined");

    const bot = new Bot(token);
    bot.start();
};

export default startTelegram;