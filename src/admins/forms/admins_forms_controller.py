import os

from aiogram import Bot
from aiogram.types import Message, InlineKeyboardMarkup, InputMediaPhoto

from src.admins.forms.admins_forms_service import AdminsFormsService
from src.admins.keyboards.inline.admins_inline_keyboards import AdminsInlineKeyboards
from src.admins.keyboards.reply.admins_reply_keyboards import AdminsReplyKeyboards
from src.users.keyboards.reply.users_reply_keyboards import UsersReplyKeyboards
from src.users.users_service import UserService
from utils.RCS.controller import Controller
from utils.lexicon.load_lexicon import load_lexicon


class AdminsFormsController(Controller):
    def __init__(self):
        super().__init__()

        self.TOKEN = os.environ["TOKEN"]

        self.bot = Bot(token=self.TOKEN)

        self.admins_service: AdminsFormsService = AdminsFormsService()
        self.users_service: UserService = UserService()

        self.admins_reply_keyboards: AdminsReplyKeyboards = AdminsReplyKeyboards()
        self.admins_inline_keyboards: AdminsInlineKeyboards = AdminsInlineKeyboards()
        self.users_reply_keyboards: UsersReplyKeyboards = UsersReplyKeyboards()

        self.lexicon = load_lexicon()
        self.replicas = self.lexicon.get("replicas")

    # Вывод панели меню для сущности анкет
    async def get_forms_admins_menu_panel(self, msg: Message) -> None:
        keyboard = await self.admins_reply_keyboards.forms_admins_menu_panel_keyboard()

        await msg.answer(self.replicas['admin']['other']['option'],
                         reply_markup=keyboard)

    # Вывод новых анкет
    async def get_forms_admins_new(self, msg: Message, offset=0, edit=False) -> None:
        try:
            # Получение анкет с LIMIT 1 и OFFSET = offset
            forms = await self.admins_service.get_new_forms(offset=offset)

            # Получение кол-ва новых анкет
            forms_count = await self.admins_service.get_new_forms_count()

            back_to_main_menu_btn = await (self.admins_inline_keyboards.
                                           admins_dynamic_entity_to_main_menu_panel_keyboard())

            pages = forms_count[0][0]

            # callback_data для кнопок пагинации
            pagen_callback_data = f"_forms-{offset}"

            if pages > 0:
                inline_callback_data = f"_forms-{forms[0]['_id']}"

                # Формирование кнопок пагинации
                pagen = await self.build_admins_pagen(
                    pages=pages,
                    offset=offset,
                    callback_data=pagen_callback_data
                )

                # Формирование кнопок для новых анкет
                buttons = await self.admins_inline_keyboards.admins_new_forms_inline_keyboards(
                    callback_data=inline_callback_data
                )

                # Соединение всех кнопок в одну клавиатуру
                keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                        pagen,
                        *buttons,
                        back_to_main_menu_btn
                    ])

                photo = forms[0]['photo_id']

                msg_text = (f"{offset + 1} из {pages}\n\n"
                            f"<b>{forms[0]['full_name']}</b>\n\n"
                            f"Компания:\n{forms[0]['company']}\n\n"
                            f"Должность:\n{forms[0]['position']}\n\n"
                            f"Город:\n{forms[0]['city']}\n\n"
                            f"Отношение к РМ:\n{forms[0]['rm_status']}\n\n"
                            f"Хобби:\n{forms[0]['hobbies']}\n\n"
                            f"Ресурсы:\n{forms[0]['resources']}\n\n"
                            f"Экспертиза:\n{forms[0]['expertise']}\n\n"
                            f"Дата рождения: {forms[0]['birth_date']}\n\n"
                            f"Телефон: {forms[0]['phone']}")

                if edit:
                    media = InputMediaPhoto(media=photo, caption=msg_text, parse_mode="HTML")
                    await msg.edit_media(media=media, reply_markup=keyboard)
                else:
                    await msg.answer_photo(photo=photo,
                                           caption=msg_text,
                                           reply_markup=keyboard,
                                           parse_mode="HTML")
            else:
                back_to_main_menu_btn = await (self.admins_inline_keyboards.
                                               admins_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

                await msg.answer(self.replicas['admin']['other']['empty'],
                                 reply_markup=back_to_main_menu_btn)
        except Exception as e:
            print(f"Error while getting forms by admin: {e}")

            back_to_main_menu_btn = await (self.admins_inline_keyboards.
                                           admins_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

            await msg.answer(self.replicas['general']['error'],
                             reply_markup=back_to_main_menu_btn)

    # Подтверждение новой анкеты
    async def admins_accept_new_form(self, msg: Message, form_id) -> None:
        back_to_main_menu_btn = await (self.admins_inline_keyboards.
                                       admins_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

        try:
            form = await self.admins_service.accept_new_form(form_id)

            if form:
                user = await self.users_service.get_user_chat_id_by_id(form_id)

                await msg.answer(self.replicas['admin']['forms']['accept'],
                                 reply_markup=back_to_main_menu_btn)

                user_keyboard = await self.users_reply_keyboards.users_start_command()

                await self.bot.send_message(
                    chat_id=user[0]['tg_chat_id'],
                    text=self.replicas['user']['forms']['accept'],
                    reply_markup=user_keyboard
                )
        except Exception as e:
            print(f"Error while accepting form by admin: {e}")

            await msg.answer(self.replicas['general']['error'],
                             reply_markup=back_to_main_menu_btn)
