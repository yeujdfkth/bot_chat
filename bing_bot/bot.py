import time
import configparser
import os

from pyrogram import Client, filters, types, enums
from pyrogram.errors.exceptions.not_acceptable_406 import ChannelPrivate
from pyrogram.errors.exceptions.forbidden_403 import Forbidden
from pyrogram.types import Chat

from parse import parse_bing


def parse_config():
    config_list = {}
    index = 0
    for root, dirs, files in os.walk('..'):
        for file in files:
            if file.split(".")[-1] == "ini":
                config_list[index] = file.split(".")[0]
                index += 1
    return config_list


API_ID = 19309010
API_HASH = "dfdf154157cca400bd53b00100468fa5"

config_list = parse_config()
name_config = config_list[int(input(f"Список конфигов: {parse_config()}\nНапиши цифру: "))]

config = configparser.ConfigParser()
config.read(name_config + ".ini", encoding="cp1251")

NAME_SESSION = config["INFO"]["NAME_SESSION"]
TIME = float(config["INFO"]["TIME"])
PROMT = config["INFO"]["PROMT"]

app = Client(NAME_SESSION, api_id=API_ID, api_hash=API_HASH, parse_mode=enums.parse_mode.ParseMode.HTML)


@app.on_message(filters.channel)
async def get_post(client, message: types.Message):
    chat_id = message.chat.id
    message_id = message.id
    response = await parse_bing(f"Вот пост: {message.text}. "
                                f"Напиши комментарий для этого поста от лица {PROMT} на пост:")
    try:
        msg = await app.get_discussion_message(chat_id, message_id)
        await msg.reply(text=response, quote=True)
        print("[+] Отправил пост")
    except ChannelPrivate:
        try:
            await app.leave_chat(chat_id)
        except Exception as e:
            print(f"Не страшная ощибка: {e}")

        for i in ["/start", "OK", "/start"]:
            await app.send_message('@spambot', i)
            time.sleep(3)
    except Forbidden:
        chat: Chat
        try:
            chat = await app.get_chat(chat_id)
            await chat.linked_chat.join()
        except Exception as e:
            print('Не удалось вступить в чат', e)
    except Exception as e:
        print('Хуй знает какая ошибка', e)

    time.sleep(TIME)

app.run()
