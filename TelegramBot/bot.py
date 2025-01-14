from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Ваш токен
telegram_token = "7378387007:AAGRott_mvI9rdDiHnmrURllYNF-tkPL7EU"

# Функция, которая будет отвечать на команду /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        await context.bot.send_message(chat_id=update.message.chat_id, text="Привет! Я твой бот.")
    else:
        print("Нет сообщения!")

# Основная функция
def main() -> None:
    application = Application.builder().token(telegram_token).build()

    # Регистрируем обработчик команды /start
    application.add_handler(CommandHandler("start", start))

    # Запускаем бота
    application.run_polling()

if __name__ == "__main__":
    main()
