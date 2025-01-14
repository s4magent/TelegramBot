{\rtf1\ansi\ansicpg1251\cocoartf2818
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;\f1\fnil\fcharset0 HelveticaNeue;}
{\colortbl;\red255\green255\blue255;\red0\green0\blue0;}
{\*\expandedcolortbl;;\cssrgb\c0\c1\c1;}
\paperw11900\paperh16840\margl1440\margr1440\vieww16600\viewh14740\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 from telegram import Update\
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext\
import openai\
\
# \uc0\u1047 \u1072 \u1084 \u1077 \u1085 \u1080 \u1090 \u1077  \u1082 \u1083 \u1102 \u1095 \u1080  \u1085 \u1072  \u1089 \u1074 \u1086 \u1080 \
TELEGRAM_TOKEN = "
\f1\fs26 \cf2 7378387007:AAEz8lMqQaNhnJk90U6HkxjcJXvcX-5bxO4
\f0\fs24 \cf0 "\
OPENAI_API_KEY = "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"\
\
openai.api_key = OPENAI_API_KEY\
\
# \uc0\u1060 \u1091 \u1085 \u1082 \u1094 \u1080 \u1103  \u1086 \u1073 \u1088 \u1072 \u1073 \u1086 \u1090 \u1082 \u1080  \u1089 \u1086 \u1086 \u1073 \u1097 \u1077 \u1085 \u1080 \u1081 \
def handle_message(update: Update, context: CallbackContext) -> None:\
    user_message = update.message.text\
    try:\
        response = openai.ChatCompletion.create(\
            model="gpt-3.5-turbo",\
            messages=[\{"role": "user", "content": user_message\}]\
        )\
        reply = response['choices'][0]['message']['content']\
    except Exception as e:\
        reply = f"\uc0\u1054 \u1096 \u1080 \u1073 \u1082 \u1072 : \{e\}"\
    update.message.reply_text(reply)\
\
# \uc0\u1054 \u1089 \u1085 \u1086 \u1074 \u1085 \u1072 \u1103  \u1092 \u1091 \u1085 \u1082 \u1094 \u1080 \u1103 \
def main():\
    updater = Updater(TELEGRAM_TOKEN)\
\
    # \uc0\u1054 \u1073 \u1088 \u1072 \u1073 \u1086 \u1090 \u1095 \u1080 \u1082  \u1090 \u1077 \u1082 \u1089 \u1090 \u1086 \u1074 \u1099 \u1093  \u1089 \u1086 \u1086 \u1073 \u1097 \u1077 \u1085 \u1080 \u1081 \
    updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))\
\
    # \uc0\u1047 \u1072 \u1087 \u1091 \u1089 \u1082  \u1073 \u1086 \u1090 \u1072 \
    updater.start_polling()\
    updater.idle()\
\
if __name__ == "__main__":\
    main()}