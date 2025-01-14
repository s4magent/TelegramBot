from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Ваш токен
telegram_token = "7378387007:AAEz8lMqQaNhnJk90U6HkxjcJXvcX-5bxO4"

# Функция, которая будет отвечать на команду /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        await update.message.reply("Привет! Я твой бот.")
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
