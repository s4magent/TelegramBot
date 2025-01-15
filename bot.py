import os
import openai
import sqlite3
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Открываем OpenAI API ключ
openai.api_key = os.getenv("OPENAI_API_KEY")

# Создаем подключение к базе данных SQLite
conn = sqlite3.connect('chat_data.db')
cursor = conn.cursor()

# Создаем таблицу для хранения данных
cursor.execute('''CREATE TABLE IF NOT EXISTS chat_data (
    chat_id INTEGER,
    user_id INTEGER,
    message TEXT
)''')
conn.commit()

# Глобальный промпт
global_prompt = "Ты — опытный владелец агентства OnlyFans с командой: трафферами, чаттерами, моделями и менеджерами. Тебе могут задавать вопросы по множеству тем, связанным с управлением агентством. Например: как вести переписку с фанами, объяснение профессиональных терминов и принципов работы, составление привлекательных объявлений для досок, переформулировка задач и четкое распределение обязанностей, разработка графиков работы и планов действий, советы по распределению ресурсов и нагрузки. Ты всегда учитываешь актуальные тренды на рынке, анализируешь текущую ситуацию и даешь решения, опираясь на последние данные. Ты профессионал в своей области и отвечаешь на все вопросы ясно и по существу. Все твои ответы четкие и легко воспринимаемые, без лишней воды. Время от времени используешь эмодзи для улучшения восприятия. Важно: ты отвечаешь только на сообщения, содержащие @OFMchatting_bot. Если его нет в сообщении, не отвечай. Когда тебя добавляют в новую группу, ты обязан просканировать все предыдущие сообщения и обучиться на основе полученной информации, чтобы быть в курсе контекста общения."

# Кодовое слово для активации общения
secret_word = "hotimdeneg"

# Функция для сохранения сообщений в базе данных
def save_message(chat_id, user_id, message):
    cursor.execute('INSERT INTO chat_data (chat_id, user_id, message) VALUES (?, ?, ?)', (chat_id, user_id, message))
    conn.commit()

# Функция для генерации ответа с учетом сохраненной информации
def generate_response(chat_id, context):
    # Извлекаем все сообщения из базы данных
    cursor.execute('SELECT message FROM chat_data WHERE chat_id = ?', (chat_id,))
    messages = cursor.fetchall()
    
    # Формируем историю для GPT
    conversation_history = [{"role": "system", "content": global_prompt}]
    for message in messages:
        conversation_history.append({"role": "user", "content": message[0]})

    # Генерируем ответ с использованием GPT
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation_history,
    )
    
    return response['choices'][0]['message']['content']

# Обработчик сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    chat_id = update.message.chat.id  # ID чата (группы или канала)
    user_id = update.message.from_user.id

    # Если сообщение содержит @OFMchatting_bot, продолжаем обработку
    if "@OFMchatting_bot" in user_message:
        # Сохраняем только текстовые сообщения в базе данных
        save_message(chat_id, user_id, user_message)

        # Генерируем ответ с использованием накопленных данных
        bot_reply = generate_response(chat_id, context)
        
        # Отправляем ответ пользователю
        await update.message.reply_text(bot_reply)
    else:
        # Если нет упоминания @OFMchatting_bot, не отвечаем
        return

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Для начала общения введите кодовое слово.")

# Обработчик кодового слова
async def handle_secret_word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    user_id = update.message.from_user.id

    # Если кодовое слово введено, активируем пользователя
    if user_message.lower() == secret_word:
        context.user_data[user_id] = {'activated': True}
        await update.message.reply_text("Привет! Ты активировал бота. Теперь можешь задавать вопросы.")
    else:
        await update.message.reply_text(f"Чтобы начать общение, введите кодовое слово")

if __name__ == "__main__":
    # Создаем приложение и добавляем обработчики
    application = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_secret_word))

    # Запускаем бота
    application.run_polling()
