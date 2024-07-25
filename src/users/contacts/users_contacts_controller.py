import os

from aiogram.types import Message, FSInputFile, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

from src.users.keyboards.inline.users_inline_keyboards import UsersInlineKeyboards
from src.users.keyboards.reply.users_reply_keyboards import UsersReplyKeyboards
from utils.RCS.controller import Controller
from utils.lexicon.load_lexicon import load_lexicon


class UsersContactsController(Controller):
    def __init__(self):
        super().__init__()

        self.users_inline_keyboards: UsersInlineKeyboards = UsersInlineKeyboards()
        self.users_reply_keyboards: UsersReplyKeyboards = UsersReplyKeyboards()

        self.lexicon = load_lexicon()
        self.replicas = self.lexicon.get("replicas")

    async def users_get_contacts(self, msg: Message) -> None:
        back_to_main_menu_button = await self.users_reply_keyboards.users_to_main_panel_reply_keyboard()

        buttons = await self.users_reply_keyboards.users_contacts_reply_keyboard()

        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                buttons,
                back_to_main_menu_button
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )

        await msg.answer(self.replicas['general']['contacts'],
                         reply_markup=keyboard)

    async def users_get_ceo(self, msg: Message) -> None:
        back_to_main_menu_button = await (self.users_inline_keyboards.
                                          users_dynamic_entity_to_main_menu_panel_keyboard())

        button = [
            InlineKeyboardButton(text=self.buttons['user']['contacts']['call'],
                                 url="https://t.me/nepremenno_horosho/")
        ]

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                button,
                back_to_main_menu_button
            ]
        )

        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, '..', 'static', 'ceo.jpg')

        document = FSInputFile(file_path)

        caption = (f"Ларькина Анна\n(@nepremenno_horosho)\n\n" 
           f"Руководитель проектов Мордовского делового товарищества\n\n"
           f"Компетенции:\n\n"
           f"• экс-руководитель проектов digital-агентства NECTARIN;\n"
           f"• студентка Школы инноватики и предпринимательства НИУ ВШЭ;\n"
           f"• опыт работы в сфере реализации государственной молодежной политики;\n"
           f"• победитель Всероссийской премии «Время молодых» (2022);\n"
           f"• экс-заместитель Председателя Молодежной правительства Республики Мордовия;\n"
           f"• психология / ВКР по теме эмоционального самораскрытие личности в процессе общения.\n\n"
           f"Хобби / интересы:\n\n"
           f"Психологическая культура личности, изучение темы проблемы эстетического воспитания. Люблю формат public talk, природу, велосипед, чай, огород, музеи. Верю в людей и хочу свой журнал.")

        await msg.answer_photo(photo=document,
                               caption=caption,
                               reply_markup=keyboard)

    async def users_get_moderator(self, msg: Message) -> None:
        back_to_main_menu_button = await (self.users_inline_keyboards.
                                          users_dynamic_entity_to_main_menu_panel_keyboard())

        button = [
            InlineKeyboardButton(text=self.buttons['user']['contacts']['call'],
                                 url="https://t.me/OlgaAPetrova/")
        ]

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                button,
                back_to_main_menu_button
            ]
        )

        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, '..', 'static', 'moderator.jpg')

        document = FSInputFile(file_path)

        caption = (f"<b>Ольга Петрова</b> — член команды Мордовского делового товарищества, "
                   f"Модератор форум-групп, эксперт и бизнес-консультант.\n\n"
                   f"<b>Компетенции:</b>\n\n"
                   f"• HR-экспертиза\n" 
                   f"• Бизнес-процессы и оптимизация\n"
                   f"• Организационное развитие\n\n"
                   f"<b>Формы работы:</b>\n\n"
                   f"• Консалтинговые проекты\n"
                   f"• Трекинг предпринимателей и проектных команд\n"
                   f"• Тренинги\n"
                   f"• Фасилитация стратегических сессий\n\n"
                   f"<b>Хобби / интересы:</b> работа. Все остальное понемногу: читаю, рисую, много учусь, сад")


        await msg.answer_photo(photo=document,
                               caption=caption,
                               reply_markup=keyboard,
                               parse_mode="HTML")
