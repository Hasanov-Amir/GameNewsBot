import asyncio
import config
import logging
import requests
import traceback
import re

from datetime import datetime
from bs4 import BeautifulSoup as BS
from aiogram import Bot, Dispatcher, executor, types

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

main_link = "https://vag1ffm.github.io/GameNews/"

with open("last.txt", "r") as temp_lastgames_fill:
    temp_games = [i for i in temp_lastgames_fill] # заполнение множества из файла last.txt

blocked_users = set()


async def game(a):

    """проверка на наличие новых статей на сайте"""

    while True:

        await asyncio.sleep(a)
        await bot.send_message(2138848839, f"{datetime.now()} цикл начался")

        try:

            r = requests.get("https://vag1ffm.github.io/GameNews/")
            html = BS(r.content, "html.parser")
            name = html.select(".right-side > .news")

        except:

            await bot.send_message(2138848839, f"{datetime.now()} c сайтом что то не так")
        
        if len(name):

            for el in name:

                try:

                    title = el.select(".news > .text > h2")

                    text_temp = title[0].text

                    text = re.sub(r"[^a-zA-Z]+", " ", text_temp)

                    if f"{text}\n" in temp_games:

                        pass

                    else:

                        photo = el.select(".news > .img > a > img")
                        genres = el.select(".news > .text > .janr")
                        about_game = el.select(".news > .text > .description")
                        link = el.select(".news > .text > .text-icon > a")
                        buyin = el.select(".news > .text > .text-icon > .buyin")

                        photo_photo = photo[0]['src']
                        photo_alt = photo[0]['alt']
                        photo_alt = photo_alt.title()
                        genre = genres[0].text
                        link = link[0]['href']
                        about_game = about_game[0].text
                        buyin = buyin[0].text
                        temp_games.append(f"{text}\n")
                        await bot.send_message(-1001243514321, f'*{text_temp}*[ ]({photo_photo})\n\n{genre}\n\n{about_game}\n\n{buyin} [{photo_alt}]({link})\n Больше инфы на [сайте]({main_link})❤', parse_mode='Markdown')
                        # await bot.send_message(2138848839, f'*{text_temp}*[ ]({photo_photo})\n\n{genre}\n\n{about_game}\n\n{buyin} [{photo_alt}]({link})\n Больше инфы на [сайте]({main_link})❤', parse_mode='Markdown')
                        await bot.send_message(2138848839, "я отправил")
                        # await bot.pin_chat_message(-1001243514321, message.MessageId)
                        
                except Exception as exc:

                    print(exc)
                    await bot.send_message(2138848839, "traceback.print_exc():")
                    traceback.print_exc()
                    print("____")
                
            await bot.send_message(2138848839, f"Список игр {datetime.now()}:\n{len(temp_games)}\n{temp_games}")

if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    loop.create_task(game(7200)) # 7200
    executor.start_polling(dp, skip_updates=True)