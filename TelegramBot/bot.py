import openai
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Укажите ваш API ключ
openai.api_key = "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"
telegram_token = "7378387007:AAEz8lMqQaNhnJk90U6HkxjcJXvcX-5bxO4"

# Функция обработки команд
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет, я твой бот!')

def main():
    updater = Updater(telegram_token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()