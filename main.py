import threading

from flask import Flask, render_template
import telebot
import configparser
import os
import json
import psycopg2
dirPath = os.path.dirname(os.path.realpath(__file__))
app = Flask("tgResender")
@app.route('/')
def main():
    with open("message.html", encoding="UTF-8") as f:
        file = f.read()
        print(file)
    print(render_template("main.html",
                           chat1URL=f"127.0.0.1&chat={chats[0]}", Chat1Name=names[0],
                           chat2URL=f"127.0.0.1&chat={chats[1]}", Chat2Name=names[1],
                           chat3URL=f"127.0.0.1&chat={chats[2]}", Chat3Name=names[2],
                           chat4URL=f"127.0.0.1&chat={chats[3]}", Chat4Name=names[3],
                           chat5URL=f"127.0.0.1&chat={chats[4]}", Chat5Name=names[4],
                           chat6URL=f"127.0.0.1&chat={chats[5]}", Chat6Name=names[5],
                           chat7URL=f"127.0.0.1&chat={chats[6]}", Chat7Name=names[6],
                           chat8URL=f"127.0.0.1&chat={chats[7]}", Chat8Name=names[7],
                           chat9URL=f"127.0.0.1&chat={chats[8]}", Chat9Name=names[8],
                           chat10URL=f"127.0.0.1&chat={chats[9]}", Chat10Name=names[9],
                           message1 = file))
    return render_template("main.html",
                           chat1URL=f"127.0.0.1&chat={chats[0]}", Chat1Name=names[0],
                           chat2URL=f"127.0.0.1&chat={chats[1]}", Chat2Name=names[1],
                           chat3URL=f"127.0.0.1&chat={chats[2]}", Chat3Name=names[2],
                           chat4URL=f"127.0.0.1&chat={chats[3]}", Chat4Name=names[3],
                           chat5URL=f"127.0.0.1&chat={chats[4]}", Chat5Name=names[4],
                           chat6URL=f"127.0.0.1&chat={chats[5]}", Chat6Name=names[5],
                           chat7URL=f"127.0.0.1&chat={chats[6]}", Chat7Name=names[6],
                           chat8URL=f"127.0.0.1&chat={chats[7]}", Chat8Name=names[7],
                           chat9URL=f"127.0.0.1&chat={chats[8]}", Chat9Name=names[8],
                           chat10URL=f"127.0.0.1&chat={chats[9]}", Chat10Name=names[9],
                           msg1 = file)



msg = """    <div class="message1">
        <img src="/../chatAvatars/tt.jpg" alt="Аватар" class="avatar">
        <div class="message-content">
            <div class="message-header">
                <span class="date">5 октября 2023, 14:30</span>
                <a href="https://example.com/user123" class="user-link">@alex_petrov</a>
                <h3 class="chat-title">Чат разработчиков</h3>
            </div>
            <p class="message-text">
                Привет! Напоминаю, что завтра собрание в 10:00. Не забудьте подготовить отчеты по проекту. Давайте обсудим новые идеи!
            </p>
        </div>
    </div>"""
# Чтение конфига
config = configparser.ConfigParser()  # создаём объекта парсера
config.read(f"{dirPath}/config.ini")
TOKEN = config['Telegram']['token']
chats = json.loads(config['Telegram']['chats'])
names = json.loads(config['Telegram']['names'])


host = config['Database']['host']
port = config['Database']['port']
user = config['Database']['user']
password = config['Database']['password']
database = config['Database']['database']

with psycopg2.connect(user=user, password=password, host=host, port=port, database=database) as conn:
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS messages(chatID INT8,chatName TEXT,userID INT8,userName TEXT,text TEXT,dt timestamp default now());")
    conn.commit()


#Чтение json
with open(f"{dirPath}/chats.json", encoding="UTF-8") as f:
    chatsJSON = json.loads(f.read())

#Создание бота
bot = telebot.TeleBot(TOKEN)



@bot.message_handler(commands=["start"])
def start(message):
    print(message.chat.id)
    bot.send_message(message.chat.id, f"Добавь меня к чатам")

@bot.message_handler(content_types=["text"])
def test(message):
    if not message.chat.id in chats:
        return

    with psycopg2.connect(user=user, password=password, host=host, port=port, database=database) as conn:
        cursor = conn.cursor()
        # print(f"INSERT INTO messages (chatID, chatName, userID, userName, text)"\
        #                f"VALUES ({message.chat.id}, {message.chat.title}, {message.from_user.id},"\
        #                f"{message.from_user.username}, {message.text})")
        cursor.execute(f"INSERT INTO messages (chatID, chatName, userID, userName, text)"\
                       f"VALUES ({message.chat.id}, '{message.chat.title}', {message.from_user.id},"\
                       f"'{message.from_user.username}', '{message.text}')")
        conn.commit()

    # print(message.chat.id, message.chat.title, message.from_user.id, message.from_user.username, message.text)


def startBFL():
    app.run(host="0.0.0.0", port=80)

def startBot():
    bot.polling(none_stop=True)
flaskThread = threading.Thread(target=startBFL)
flaskThread.start()

startBot()