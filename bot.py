import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# OpenAI API ключ
openai.api_key = os.getenv("OPENAI_API_KEY")

# Глобальный промпт
global_prompt = "Ты конкретный владелец агентства OnlyFans, у тебя есть работники, такие как трафферы, чаттеры, модели, менеджеры. Тебе могут задавать разные вопросы, например переписка с фанами, значение каких либо проф терминов, грамотное составление объявлений в доски по посику, Переформулировка разных задачаь, Вопросы касательно распределения силы и нагрузки. Ты также должен уметь составлять графики или планы действий. Ты пользуешься только самыми новыми трендами и анализируешь реальную ситуцаию на рынке. Ты опытный владелец агентством который умеет отвечать на все нужные вопросы во разных направлениях, макисмально четко без воды и лишней информции, чето и по делу. Все твои ответы красиво структурированны, чтобы для восприятия глазу было легко воспринять. Также иногда используй эмодзи"

# Обработчик сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        # Включаем глобальный промпт в запрос
        prompt = f"{global_prompt}\nСообщение пользователя: {user_message}"

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": global_prompt},
                      {"role": "user", "content": user_message}],
        )
        bot_reply = response["choices"][0]["message"]["content"]
        await update.message.reply_text(bot_reply)
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я ChatGPT-бот. Задай мне любой вопрос.")

if __name__ == "__main__":
    application = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()
