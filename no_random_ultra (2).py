import time
import openai

from pyrogram import Client
from pyrogram import filters

app = Client(
    "my_account",
    api_id=15354199,
    api_hash="4b42c4babb1f7866c005b8c5a967add7"
)

openai.api_key = "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"


async def chat_gpt(promt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=promt,
        max_tokens=1024,
        temperature=0.85,
    )
    return response.choices[0].text


async def chat_gpt_message(chat_id, comment_id, post):
    print("CHAT GPT редачит комментарий!")
    result = await chat_gpt(f"Ответь в стиле гопника на пост\n{post}")
    await app.edit_message_text(chat_id, comment_id, result.split("\n")[-1])


@app.on_message(filters.channel)
async def handle_new_posts(client, message):
    start = time.time()
    if message.edit_date is None:
        return
    linked = await get_linked(message)
    message_to_answer = await get_forwarded_in_linked(message.message_id, linked)
    print(message.text)
    comment = await app.send_message(linked.id, "👍", reply_to_message_id=message_to_answer.message_id)
    print(f"ANSWERED TO: {message.chat.title} За {time.time() - start}")
    await chat_gpt_message(linked.id, comment.message_id, message.text)


async def get_forwarded_in_linked(message_id, linked):
    async for message in app.search_messages(linked.id, limit=1, filter="pinned"):
        return message


async def get_linked(msg):
    channel = await app.get_chat(msg.sender_chat.id)
    return channel.linked_chat

app.run()
