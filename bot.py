import telegram

from environs import Env
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

env = Env()
env.read_env()
bot_token = env('BOT_TOKEN')

def main():
    updater = Updater(bot_token)
    updater.dispatcher.add_handler(CommandHandler('hello', hello))

    # updater.start_polling()
    # updater.idle()


def hello(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'Hello {update.effective_user.first_name}')


if __name__ == '__main__':
    bot = telegram.Bot(token=bot_token)
    bot.send_message(chat_id='@devapil4', text="I'm sorry Dave I'm afraid I can't do that.")
    main()