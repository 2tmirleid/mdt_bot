#!/usr/bin/python3

"""ЗАПУСК КАЖДЫЙ ПОНЕДЕЛЬНИК В 09:00"""

import asyncio
import os
import random

from aiogram import Bot

from src.users.random_coffee.users_random_coffee_service import UsersRandomCoffeeService

users_service: UsersRandomCoffeeService = UsersRandomCoffeeService()

# Создание нового экземпляра бота
token = os.environ["TOKEN"]
bot = Bot(token=token)


# Получаем кол-во подписанных
async def get_subs_count() -> int:
    subs_count = await users_service.get_count_subscribed_for_random_coffee()

    return subs_count[0][0]


# Получаем рандомного юзера
async def get_random_user(exclude_user_id=0) -> dict:
    subs_count = await get_subs_count() - 1

    random_num = random.randint(0, subs_count)

    return await users_service.get_random_profile_for_random_coffee(offset=random_num, exclude_user_id=0)


# Получаем список всех подписанных
async def get_subs() -> dict:
    return await users_service.get_subscribed_users_for_random_coffee()


async def get_caption(name: str, username: str, phone: str) -> str:
    return (f"👋 <b>Привет,</b> {name}!\n\n"
            f"<b>Новая неделя — это возможность открыться чему-то новому.</b>\n"
            f"И мы предлагаем тебе узнать участника МДТ с другой стороны благодаря <b>RANDOM COFFEE</b> ☕️\n\n"
            f"<i>Общение тет-а-тет — шанс открыть человека с новой стороны, ближе познакомиться, пообщаться, помочь друг другу и просто полезно провести время.</i>\n\n"
            f"<b>Как это будет? Очень просто:</b>\n\n"
            f"▶️ Мы уже выбрали твоего собеседника. Это будет @{username}\n"
            f"Номер телефона - {phone}\n"
            f"▶️ Теперь вам осталось договориться о месте и времени встречи.\n\n"
            f"Обсудите интересные идеи и, возможно, найдёте единомышленника или будущего партнёра по бизнесу. Кто знает, может, эта встреча станет началом чего-то большого 🔄\n\n"
            f"<b>Желаем вам отличного кофе и увлекательной беседы!</b>")


async def send_random_user_for_all_users() -> None:
    # Получаем всех подписчиков
    subs = await get_subs()
    # Получаем кол-во подписчиков
    subs_count = await get_subs_count()
    # Получаем рандомного юзера
    random_user = await get_random_user()

    # Если кол-во меньше 2х, то произойдет бесконечный цикл запросов к базе и она ляжет
    if subs_count >= 2:
        for sub in subs:
            # Если tg_chat_id рандомного юзера и юзера, которому бот отправит смс не равны, то ок
            if random_user[0]['tg_chat_id'] != sub['tg_chat_id']:
                caption = await get_caption(
                    name=sub['full_name'],
                    username=random_user[0]['tg_username'],
                    phone=random_user[0]['phone']
                )

                await bot.send_message(
                    chat_id=sub['tg_chat_id'],
                    text=caption,
                    parse_mode="HTML"
                )
            # Иначе - бот выберет другого рандомного юзера, исключая нашего из подборки
            else:
                exclude_random_user = await get_random_user(exclude_user_id=random_user[0]['tg_chat_id'])

                caption = await get_caption(
                    name=sub['full_name'],
                    username=exclude_random_user[0]['tg_username'],
                    phone=exclude_random_user[0]['phone']
                )

                await bot.send_message(
                    chat_id=sub['tg_chat_id'],
                    text=caption,
                    parse_mode="HTML"
                )


if __name__ == "__main__":
    asyncio.run(send_random_user_for_all_users())
