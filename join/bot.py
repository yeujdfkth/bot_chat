import asyncio
from pyrogram import Client

api_id = 25205845
api_hash = "87d05772389e7fe982ef50738596b0c1"


async def main():
    async with Client(f"{api_id}", api_id, api_hash) as app:
    	with open('group.txt', 'r') as groupfile:
    		for group in groupfile:
    			try:
    				print(group.strip())
    				chat = await app.get_chat(str(group.strip()))
    				await asyncio.sleep(0.5)
    				await app.join_chat(chat.id)
    				await asyncio.sleep(400)
    				print(f"Вступили в группу {group}")
    			except:
    				pass



asyncio.run(main())


