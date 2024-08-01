import os

from aiogram.types import Message, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton

from src.users.keyboards.inline.users_inline_keyboards import UsersInlineKeyboards
from src.users.keyboards.reply.users_reply_keyboards import UsersReplyKeyboards
from utils.RCS.controller import Controller
from utils.lexicon.load_lexicon import load_lexicon


class UsersClubsController(Controller):
    def __init__(self):
        super().__init__()

        self.users_reply_keyboards: UsersReplyKeyboards = UsersReplyKeyboards()
        self.users_inline_keyboards: UsersInlineKeyboards = UsersInlineKeyboards()

        self.lexicon = load_lexicon()
        self.replicas = self.lexicon.get("replicas")

    async def users_get_clubs_info(self, msg: Message) -> None:
        msg_text = self.replicas['general']['clubs']

        keyboard = await self.users_reply_keyboards.users_clubs_panel_keyboard()

        await msg.answer(text=msg_text,
                         reply_markup=keyboard,
                         parse_mode="HTML")

    async def users_get_clubs_mdt_it(self, msg: Message) -> None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, '..', 'static', 'clubs', 'club_it.jpg')

        photo = FSInputFile(file_path)

        msg_text = (f"<b>МДТ. IT-технологии</b> 🖥\n\n"
                    f"Представляем первый тематический клуб в нашем сообществе! Лидер клуба Антон Сокольников @antonflakon_s — архитектор платформ больших данных и ИИ.\n\n"
                    f"<b>О чем будем говорить?</b>\n\n"
                    f"— Сборка интернет-магазина с онлайн-кассой за пару дней (схема процесса). Начинаем продавать и продвигать сами.\n"
                    f"— Как автоматизировать простую рутину в компании без кода своими руками.\n"
                    f"— Сервисные IT-компании и специалисты: на что обратить внимание при подборе в найме?\n"
                    f"— Инфобез в малом и среднем бизнесе: как сделать так чтобы вашу базу не сливали сотрудники. Основные подходы и рекомендации.\n"
                    f"— Языковые модели врут: как не разочароваться, и извлечь максимум выгоды из промта.\n"
                    f"— Какие подходы из IT можно взять для традиционного бизнеса: гибкие методологии.\n\n"
                    f"<b>И о многом другом!</b>\n\n"
                    f"#Клуб_в_клубе")

        link = "https://t.me/+VTjP2RY5E_s1ODVi"

        await msg.answer_photo(photo=photo,
                               caption=msg_text,
                               parse_mode="HTML",
                               reply_markup=InlineKeyboardMarkup(
                                   inline_keyboard=[
                                       [InlineKeyboardButton(text="Хочу присоединиться",
                                                             url=link)]
                                   ]
                               ))

    async def users_get_clubs_mdt_woman(self, msg: Message) -> None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, '..', 'static', 'clubs', 'club_woman.jpg')

        photo = FSInputFile(file_path)

        msg_text = (f"🤗 <b>Мы рады видеть вас здесь</b>\n\n"
                    f"В МДТ Woman мы хотим создавать пространство для всех активных и целеустремлённых девушек и женщин, где вы обязательно найдёте поддержку, вдохновение и новые возможности для развития 🌸\n\n"
                    f"Вместе будем обсуждать здоровье, психологию, путешествия, бизнес и семью 🤭\n\n"
                    f"<i>Мы хотим делать то, что нравится нам и приносит радость. И всё это в тёплой и уютной компании</i> 🌿")

        link = "https://t.me/+nqEX7-I30Sw5MzYy"

        await msg.answer_photo(photo=photo,
                               caption=msg_text,
                               parse_mode="HTML",
                               reply_markup=InlineKeyboardMarkup(
                                   inline_keyboard=[
                                       [InlineKeyboardButton(text="Хочу присоединиться",
                                                             url=link)]
                                   ]
                               ))
