from EdgeGPT import Chatbot


async def parse_bing(promt):
    bot = Chatbot(cookie_path="cookies.json")
    while True:
        response_dict = await bot.ask(prompt=promt)
        try:
            return response_dict['item']['messages'][1]['text'].replace("[^\\d^]", "")
        except Exception as e:
            print(f"{e}\nОбидно да?")
