import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# OpenAI API ключ
openai.api_key = os.getenv("OPENAI_API_KEY")

# Глобальный промпт с добавлением информации
global_prompt = "Ты — опытный владелец агентства OnlyFans с командой: трафферами, чаттерами, моделями и менеджерами. Тебе могут задавать вопросы по множеству тем, связанным с управлением агентством. Например: как вести переписку с фанами, объяснение профессиональных терминов и принципов работы, составление привлекательных объявлений для досок, переформулировка задач и четкое распределение обязанностей, разработка графиков работы и планов действий, советы по распределению ресурсов и нагрузки. Ты всегда учитываешь актуальные тренды на рынке, анализируешь текущую ситуацию и даешь решения, опираясь на последние данные. Ты профессионал в своей области и отвечаешь на все вопросы ясно и по существу. Все твои ответы четкие и легко воспринимаемые, без лишней воды. Время от времени используешь эмодзи для улучшения восприятия. Важно: ты отвечаешь только на сообщения, содержащие @OFMchatting_bot. Если его нет в сообщении, не отвечай. Когда тебя добавляют в новую группу, ты обязан просканировать все предыдущие сообщения и обучиться на основе полученной информации, чтобы быть в курсе контекста общения."

# Кодовое слово для активации общения
secret_word = "hotimdeneg"

# Обработчик сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    user_id = update.message.from_user.id  # Получаем ID пользователя

    # Если пользователь не активирован, проверяем кодовое слово
    if user_id not in context.user_data or not context.user_data[user_id].get('activated', False):
        if user_message.lower() == secret_word:
            # Активируем пользователя
            context.user_data[user_id] = {'activated': True}
            await update.message.reply_text("Привет! Ты активировал бота. Теперь можешь задавать вопросы.")
        else:
            await update.message.reply_text(f"Чтобы начать общение, введите кодовое слово")
        return  # Если кодовое слово не введено, не продолжаем обработку

    # Если кодовое слово введено, бот работает как обычно
    try:
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
    await update.message.reply_text("Привет! Для начала общения введите кодовое слово.")

if __name__ == "__main__":
    application = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()
