import threading

from flask import Flask, render_template, request

import configparser
import os
import json

import psycopg2

from pyrogram import Client, filters
from pyrogram.types import Message, MessageEntity

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

dirPath = os.path.dirname(os.path.realpath(__file__))
app = Flask("tgResender", template_folder=f"{dirPath}/templates")
@app.route('/')
def main():

    args = request.args.to_dict()
    pageNow = int(args.get("page", 1))

    with open(f"{dirPath}/templates/page.html", encoding="UTF-8") as f:
        page = f.read()

    with psycopg2.connect(user=user, password=password, host=host, port=port, database=database) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM messages WHERE chatid = '{args.get('chat', chats[0])}' ORDER BY dt DESC LIMIT 30 OFFSET {(pageNow-1)*30}")
        res = cursor.fetchall()
        cursor.execute(f"SELECT count(*) FROM messages WHERE chatid = '{args.get('chat', chats[0])}'")
        count = cursor.fetchone()[0]

    collPages = count//30 + 1 if count%30!=0 else 0
        # print(res)

    messages = [""]*30

    for i, message in enumerate(res):
        chatId = message[0]
        chatName = message[1]
        userId = message[2]
        userName = message[3]
        text = message[4]
        date = message[5]
        ents = message[6]
        messages[i] = render_template("message.html",
                                      chatid=chatId,
                                      chatname=chatName,
                                      userid=userId,
                                      username=userName,
                                      text=text,
                                      day=date.day,
                                      month=date.month,
                                      year=date.year,
                                      time=date.strftime("%H:%M"))
        print(collPages)
        if collPages == 1:
            page1 = render_template("page.html",
                                    pageN="1",
                                    chatID = args.get('chat', chats[0]),
                                    active = "active")
            print(page1)
            page2 = ""
            page3 = ""
            page4 = ""

        elif collPages == 2:
            page1 = render_template("page.html",
                                    pageN="1",
                                    chatID=args.get('chat', chats[0]),
                                    active="active" if pageNow==1 else "")
            page2 = render_template("page.html",
                                    pageN="2",
                                    chatID=args.get('chat', chats[0]),
                                    active="active" if pageNow==2 else "")
            page3 = ""
            page4 = ""

        elif collPages == 3:
            page1 = render_template("page.html",
                                    pageN="1",
                                    chatID=args.get('chat', chats[0]),
                                    active="active" if pageNow==1 else "")
            page2 = render_template("page.html",
                                    pageN="2",
                                    chatID=args.get('chat', chats[0]),
                                    active="active" if pageNow==2 else "")
            page3 = render_template("page.html",
                                    paheN="3",
                                    pageN=args.get('chat', chats[0]),
                                    active="active" if pageNow==3 else "")
            page4 = ""

        else:
            page1 = render_template("page.html",
                                    pageN=f"{pageNow-1}" if pageNow!=1 else f"{pageNow}",
                                    chatID=args.get('chat', chats[0]),
                                    active="active" if pageNow==1 else "")
            page2 = render_template("page.html",
                                    pageN=f"{pageNow - int(pageNow == collPages)}" if pageNow!=1 else f"{pageNow+1}",
                                    chatID=args.get('chat', chats[0]),
                                    active="active" if pageNow!=1 and pageNow!=collPages else "")
            page3 = render_template("page.html",
                                    pageN=f"{pageNow+1 - int(pageNow == collPages)}" if pageNow!=1 else f"{pageNow+2}",
                                    chatID=args.get('chat', chats[0]),
                                    active="active" if pageNow==collPages else "")
            if pageNow!=collPages:
                page4 = render_template("page.html",
                                        pageN=f"{collPages}",
                                        chatID=args.get('chat', chats[0]),
                                        active="")
            else:
                page4 = ""


        for j in ents:
            messages[i] = messages[i].replace(j["text"], f"<a href = \"{j['url']}\"  target=\"_blank\">{j['text']}</a>")

    return render_template("main.html",
                           chat1URL=f"?chat={chats[0]}", Chat1Name=names[0],
                           chat2URL=f"?chat={chats[1]}", Chat2Name=names[1],
                           chat3URL=f"?chat={chats[2]}", Chat3Name=names[2],
                           chat4URL=f"?chat={chats[3]}", Chat4Name=names[3],
                           chat5URL=f"?chat={chats[4]}", Chat5Name=names[4],
                           chat6URL=f"?chat={chats[5]}", Chat6Name=names[5],
                           chat7URL=f"?chat={chats[6]}", Chat7Name=names[6],
                           chat8URL=f"?chat={chats[7]}", Chat8Name=names[7],
                           chat9URL=f"?chat={chats[8]}", Chat9Name=names[8],
                           chat10URL=f"?chat={chats[9]}", Chat10Name=names[9],
                           prevpage=f"{pageNow - 1}",
                           nextpage=f"{pageNow + 1}",
                           buttonPage1 = page1,
                           buttonPage2 = page2,
                           buttonPage3 = page3,
                           buttonPage4 = page4,
                           chatID=args.get('chat', chats[0]),

                           prevIsdisabled = "disabled" if pageNow==1 else "",
                           nextIsdisabled = "disabled" if pageNow==collPages else "",


                           msg1 = messages[0],
                           msg2 = messages[1],
                           msg3 = messages[2],
                           msg4 = messages[3],
                           msg5 = messages[4],
                           msg6 = messages[5],
                           msg7 = messages[6],
                           msg8 = messages[7],
                           msg9 = messages[8],
                           msg10 = messages[9],
                           msg11 = messages[10],
                           msg12 = messages[11],
                           msg13 = messages[12],
                           msg14 = messages[13],
                           msg15 = messages[14],
                           msg16=messages[15],
                           msg17=messages[16],
                           msg18=messages[17],
                           msg19=messages[18],
                           msg20=messages[19],
                           msg21=messages[20],
                           msg22=messages[21],
                           msg23=messages[22],
                           msg24=messages[23],
                           msg25=messages[24],
                           msg26=messages[25],
                           msg27=messages[26],
                           msg28=messages[27],
                           msg29=messages[28],
                           msg30=messages[29])




# Чтение конфига
config = configparser.ConfigParser()  # создаём объекта парсера
config.read(f"{dirPath}/config.ini", encoding="UTF-8")
chats = json.loads(config['Telegram']['chats'])
names = json.loads(config['Telegram']['names'])


host = config['Database']['host']
port = config['Database']['port']
user = config['Database']['user']
password = config['Database']['password']
database = config['Database']['database']

with psycopg2.connect(user=user, password=password, host=host, port=port, database=database) as conn:
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS messages(chatID INT8,chatName TEXT,userID INT8,userName TEXT,text TEXT,dt timestamp default now(), ent jsonb);")
    conn.commit()




#Создание бота
# Параметры Telegram
api_id = config["Telegram"]["apiID"]
api_hash = config["Telegram"]["apiHASH"]
phone = config["Telegram"]["phone"]
login = config["Telegram"]["login"]

bot = Client(name=login, api_id=api_id, api_hash=api_hash, phone_number=phone)



@bot.on_message(filters.command(["start"]))
def start(client: Client, message: Message):
    # print(message.chat.id)
    bot.send_message(chat_id=message.chat.id, text=f"Добавь меня к чатам")

@bot.on_message(filters.text)
def test(client: Client, message: Message):
    config.read(f"{dirPath}/config.ini")
    chats = json.loads(config['Telegram']['chats'])
    names = json.loads(config['Telegram']['names'])
    # print("..")
    if not message.chat.id in chats:
        return

    text = message.text
    entities_info = []
    if not message.entities is None:
        for entity in message.entities:
            # print(str(entity.type))
            start = entity.offset
            end = start + entity.length
            entity_text = text[start:end]
            if str(entity.type) == "MessageEntityType.TEXT_LINK":
                url = entity.url
            elif str(entity.type) == "MessageEntityType.MENTION":
                url = f"https://telegram.me/{entity_text[1:]}"
            else:
                continue

            # Извлекаем текст, соответствующий сущности


            # Формируем информацию о сущности
            info = {
                "text": entity_text,
                "url": url,
            }

            entities_info.append(info)





    with psycopg2.connect(user=user, password=password, host=host, port=port, database=database) as conn:
        cursor = conn.cursor()
        # print(f"INSERT INTO messages (chatID, chatName, userID, userName, text, ent)"\
        #                f"VALUES ({message.chat.id}, '{message.chat.title}', {message.from_user.id},"\
        #                f"'{message.from_user.username}', '{message.text}', '{json.dumps(entities_info)}');")
        cursor.execute(f"INSERT INTO messages (chatID, chatName, userID, userName, text, ent)"\
                       f"VALUES ({message.chat.id}, '{message.chat.title}', {message.from_user.id},"\
                       f"'{message.from_user.username}', '{message.text}', '{json.dumps(entities_info)}');")
        conn.commit()



def startBFL():
    app.run(host="0.0.0.0", port=80)

def startBot():
    while True:
        try:
            bot.run()
        except:
            pass
flaskThread = threading.Thread(target=startBFL)
flaskThread.start()

startBot()