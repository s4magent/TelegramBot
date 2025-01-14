import openai
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Ваш токен Telegram
telegram_token = "7378387007:AAGRott_mvI9rdDiHnmrURllYNF-tkPL7EU"

# Установите ключ OpenAI API
openai.api_key = "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"  # Замените на ваш ключ OpenAI

# Функция, которая будет отвечать на команду /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        await context.bot.send_message(chat_id=update.message.chat_id, text="Привет! Я твой бот. Напиши что-нибудь, и я передам это ChatGPT.")
    else:
        print("Нет сообщения!")

# Функция, которая будет отправлять сообщения в ChatGPT и отвечать пользователю
async def chat_with_gpt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text  # Получаем сообщение пользователя

    try:
        # Отправляем запрос в OpenAI API
        response = openai.Completion.create(
            model="gpt-3.5-turbo",  # Используем модель GPT-3.5
            prompt=user_message,
            max_tokens=150  # Максимальное количество токенов для ответа
        )
        bot_response = response.choices[0].text.strip()  # Ответ ChatGPT

        # Отправляем ответ пользователю
        await update.message.reply_text(bot_response)

    except Exception as e:
        # Если возникла ошибка, отправляем сообщение о проблеме
        await update.message.reply_text("Произошла ошибка при обработке вашего запроса. Попробуйте позже.")
        print(f"Ошибка OpenAI: {e}")

# Основная функция
def main() -> None:
    application = Application.builder().token(telegram_token).build()

    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start", start))
    
    # Регистрируем обработчик текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_with_gpt))

    # Запускаем бота
    application.run_polling()

if __name__ == "__main__":
    main()
