from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InputMediaPhoto, InlineKeyboardButton

from src.states.users.users_search_residents_state import UsersSearchResidentsState
from src.users.keyboards.inline.users_inline_keyboards import UsersInlineKeyboards
from src.users.keyboards.reply.users_reply_keyboards import UsersReplyKeyboards
from src.users.residents.users_residents_service import UsersResidentsService
from utils.RCS.controller import Controller
from utils.lexicon.load_lexicon import load_lexicon
from utils.validator import Validator


class UsersResidentsController(Controller):
    def __init__(self):
        super().__init__()

        self.users_service: UsersResidentsService = UsersResidentsService()

        self.users_reply_keyboards: UsersReplyKeyboards = UsersReplyKeyboards()
        self.users_inline_keyboards: UsersInlineKeyboards = UsersInlineKeyboards()

        self.validator: Validator = Validator()

        self.lexicon = load_lexicon()
        self.replicas = self.lexicon.get("replicas")

        self.property = None
        self.value = None

    async def users_get_residents_search_property(self, msg: Message) -> None:
        back_to_main_menu = await (self.users_inline_keyboards.
                                   users_dynamic_entity_to_main_menu_panel_keyboard())

        buttons = await self.users_inline_keyboards.users_get_search_property()

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                *buttons,
                back_to_main_menu
            ]
        )

        await msg.answer(self.replicas['user']['residents']['main'],
                         reply_markup=keyboard)

    async def users_get_residents_search_value(self, msg: Message, state: FSMContext, property: str) -> None:
        await state.set_state(UsersSearchResidentsState.property)

        self.property = property

        await msg.answer(self.replicas['user']['residents']['value'])

        await state.set_state(UsersSearchResidentsState.value)

    async def users_get_residents(self, msg: Message, state: FSMContext, offset=0, edit=False) -> None:
        try:
            property = self.property
            value = self.value

            residents = await self.users_service.get_residents(
                offset=offset,
                property=property,
                value=value
            )

            if len(residents) > 0:

                pages = residents[0]['count']

                back_to_main_menu = await (self.users_inline_keyboards.
                                           users_dynamic_entity_to_main_menu_panel_keyboard())

                if pages > 0 :
                    pagen_callback_data = f"_search-{offset}"

                    pagen = await self.build_users_pagen(
                        pages=pages,
                        offset=offset,
                        callback_data=pagen_callback_data
                    )

                    call_btn = [
                        InlineKeyboardButton(text="Написать ✍",
                                             url=f"https://t.me/{residents[0]['tg_username']}/")
                    ]

                    keyboard = InlineKeyboardMarkup(
                        inline_keyboard=[
                            pagen,
                            call_btn,
                            back_to_main_menu
                        ])

                    photo = residents[0]['photo']

                    msg_text = (f"{offset + 1} из {pages}\n\n"
                                f"<b>{residents[0]['full_name']}</b>\n\n"
                                f"Компания:\n{residents[0]['company']}\n\n"
                                f"Должность:\n{residents[0]['position']}\n\n"
                                f"Город: {residents[0]['city']}\n\n"
                                f"Отношение к РМ:\n{residents[0]['rm_status']}\n\n"
                                f"Хобби:\n{residents[0]['hobbies']}\n\n"
                                f"Ресурсы:\n{residents[0]['resources']}\n\n"
                                f"Экспертиза:\n{residents[0]['expertise']}\n\n"
                                f"Дата рождения: <i>{residents[0]['birth_date']}</i>\n\n"
                                f"Телефон: {residents[0]['phone']}")

                    if edit:
                        media = InputMediaPhoto(media=photo, caption=msg_text, parse_mode="HTML")
                        await msg.edit_media(media=media, reply_markup=keyboard)
                    else:
                        await msg.answer_photo(photo=photo,
                                               caption=msg_text,
                                               reply_markup=keyboard,
                                               parse_mode="HTML")
            else:
                back_to_main_menu_btn = await (self.users_inline_keyboards.
                                               users_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

                await msg.answer(self.replicas['user']['other']['empty'],
                                 reply_markup=back_to_main_menu_btn)
        except Exception as e:
            print(f"Error while getting residents by user: {e}")

            back_to_main_menu_btn = await (self.users_inline_keyboards.
                                               users_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

            await msg.answer(self.replicas['general']['error'],
                             reply_markup=back_to_main_menu_btn)
