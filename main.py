from datetime import datetime
import time

import openai
from pyrogram import Client
from pyrogram import filters

openai.api_key = ""

app = Client(
    "my_account",
    api_id=,
    api_hash=""
)


async def chat_gpt(promt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=promt,
        max_tokens=1024,
        temperature=0.85,
    )
    return response.choices[0].text


@app.on_message(filters.channel)
async def handle_new_posts(client, message):
    start = time.time()
    if(message.edit_date is None or (datetime.utcfromtimestamp(message.edit_date)
                                     - datetime.utcfromtimestamp(message.date)).total_seconds() > 5):
        return
    linked = await get_linked(message)
    message_text = await chat_gpt(f"Пост: {message.text}\n"
                                  f"Ответь на пост как миллионер(ответ должен быть 7 слов)")
    message_to_answer = await get_forwarded_in_linked(message.message_id, linked)
    print(message.text)
    await app.send_message(linked.id, message_text.split("\n")[-1], reply_to_message_id=message_to_answer.message_id)
    print(f"ANSWERED TO: {message.chat.title} За {time.time() - start}")


async def get_forwarded_in_linked(message_id, linked):
    async for message in app.search_messages(linked.id, limit=1, filter="pinned"):
        return message


async def get_linked(msg):
    channel = await app.get_chat(msg.sender_chat.id)
    return channel.linked_chat


app.run()
