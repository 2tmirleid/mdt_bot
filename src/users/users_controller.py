from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup

from src.states.users.users_edit_profile_state import UsersEditProfileState
from src.users.keyboards.inline.users_inline_keyboards import UsersInlineKeyboards
from src.users.keyboards.reply.users_reply_keyboards import UsersReplyKeyboards
from src.users.users_service import UsersService
from utils.RCS.controller import Controller
from utils.lexicon.load_lexicon import load_lexicon
from utils.validator import Validator


class UsersController(Controller):
    def __init__(self):
        super().__init__()

        self.users_service: UsersService = UsersService()

        self.users_reply_keyboards: UsersReplyKeyboards = UsersReplyKeyboards()
        self.users_inline_keyboards: UsersInlineKeyboards = UsersInlineKeyboards()

        self.validator: Validator = Validator()

        self.lexicon = load_lexicon()
        self.replicas = self.lexicon.get("replicas")

    async def users_get_started(self, msg: Message) -> None:
        keyboard = await self.users_reply_keyboards.users_to_main_panel_reply_keyboard(markup=True)

        await msg.answer(self.replicas['user']['greeting'],
                         reply_markup=keyboard)

    async def users_get_main_menu_panel(self, msg: Message) -> None:
        keyboard = await self.users_reply_keyboards.users_main_menu_panel_reply_keyboard()

        await msg.answer(self.replicas['user']['other']['option'],
                         reply_markup=keyboard)

    async def users_get_profile(self, msg: Message) -> None:
        back_to_main_button = await self.users_inline_keyboards.users_dynamic_entity_to_main_menu_panel_keyboard()

        chat_id = msg.from_user.id

        edit_btn = await self.users_inline_keyboards.users_profile_inline_keyboard(profile_id=chat_id)

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                edit_btn,
                back_to_main_button
            ]
        )

        chat_id = msg.from_user.id

        user = await self.users_service.get_user_profile_by_chat_id(chat_id)

        photo = user[0]['photo']

        caption = (f"<b>{user[0]['full_name']}</b>\n\n"
                   f"Компания:\n{user[0]['company']}\n\n"
                   f"Должность:\n{user[0]['position']}\n\n" 
                   f"Город: {user[0]['city']}\n\n"
                   f"Отношение к РМ:\n{user[0]['rm_status']}\n\n"
                   f"Хобби:\n{user[0]['hobbies']}\n\n"
                   f"Ресурсы:\n{user[0]['resources']}\n\n"
                   f"Экспертиза:\n{user[0]['expertise']}\n\n"
                   f"Дата рождения: <i>{user[0]['birth_date']}</i>\n\n"
                   f"Телефон: {user[0]['phone']}")

        await msg.answer_photo(photo=photo,
                               caption=caption,
                               parse_mode="HTML",
                               reply_markup=keyboard
                               )

    async def users_edit_profile(self, msg: Message, state: FSMContext, chat_id) -> None:
        await state.set_state(UsersEditProfileState.tg_chat_id)

        await state.update_data(tg_chat_id=chat_id)

        back_to_main_button = await self.users_inline_keyboards.users_dynamic_entity_to_main_menu_panel_keyboard()

        edit_buttons = await self.users_inline_keyboards.users_edit_profile_inline_keyboard()

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                *edit_buttons,
                back_to_main_button
            ])

        await msg.answer(self.replicas['user']['edit']['property'],
                         reply_markup=keyboard)

        await state.set_state(UsersEditProfileState.property)

    async def users_get_edit_profile_property(self, msg: Message, state: FSMContext, property) -> None:
        await state.update_data(property=property)

        back_to_main_button = await (self.users_inline_keyboards.
                                     users_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

        await msg.answer(self.replicas['user']['edit']['value'],
                         reply_markup=back_to_main_button)

        await state.set_state(UsersEditProfileState.value)

    async def users_get_edit_profile_value(self, msg: Message, state: FSMContext) -> None:
        back_to_main_menu_btn = await (self.users_inline_keyboards.
                                       users_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

        data = await state.get_data()

        tg_chat_id = data.get("tg_chat_id")
        property = data.get("property")
        value = ""

        if property == "photo":
            if msg.photo[-1].file_id:
                value = msg.photo[-1].file_id
        elif property == "birth_date":
            is_valid, result = await self.validator.validate_date(date=msg.text)

            if not is_valid:
                await msg.answer(result)
                await msg.answer(self.replicas['user']['edit']['value'],
                                 reply_markup=back_to_main_menu_btn)

                await state.set_state(UsersEditProfileState.value)

                return
            else:
                value = msg.text
        elif property == "full_name":
            is_valid, result = await self.validator.validate_full_name(full_name=msg.text)

            if not is_valid:
                await msg.answer(result)
                await msg.answer(self.replicas['user']['edit']['value'],
                                 reply_markup=back_to_main_menu_btn)

                await state.set_state(UsersEditProfileState.value)

                return
            else:
                value = msg.text

        # elif property == "phone":
        #     is_valid, result = await self.validator.validate_description(description=msg.text)
        #
        #     if not is_valid:
        #         await msg.answer(result)
        #         await msg.answer(self.replicas['admin']['entities']['edit']['value'],
        #                          reply_markup=back_to_main_menu_btn)
        #
        #         await state.set_state(EditEventsState.value)
        #
        #         return
        #     else:
        #         value = msg.text

        elif property == "city":
            is_valid, result = await self.validator.validate_city(city=msg.text)

            if not is_valid:
                await msg.answer(result)
                await msg.answer(self.replicas['user']['edit']['value'],
                                 reply_markup=back_to_main_menu_btn)

                await state.set_state(UsersEditProfileState.value)

                return
            else:
                value = msg.text

        elif property == "company":
            is_valid, result = await self.validator.validate_company(company=msg.text)

            if not is_valid:
                await msg.answer(result)
                await msg.answer(self.replicas['user']['edit']['value'],
                                 reply_markup=back_to_main_menu_btn)

                await state.set_state(UsersEditProfileState.value)

                return
            else:
                value = msg.text

        elif property == "position":
            is_valid, result = await self.validator.validate_position(position=msg.text)

            if not is_valid:
                await msg.answer(result)
                await msg.answer(self.replicas['user']['edit']['value'],
                                 reply_markup=back_to_main_menu_btn)

                await state.set_state(UsersEditProfileState.value)

                return
            else:
                value = msg.text

        elif property == "rm_status":
            is_valid, result = await self.validator.validate_rm_status(status=msg.text)

            if not is_valid:
                await msg.answer(result)
                await msg.answer(self.replicas['user']['edit']['value'],
                                 reply_markup=back_to_main_menu_btn)

                await state.set_state(UsersEditProfileState.value)

                return
            else:
                value = msg.text

        elif property == "hobbies":
            is_valid, result = await self.validator.validate_hobbies(hobbies=msg.text)

            if not is_valid:
                await msg.answer(result)
                await msg.answer(self.replicas['user']['edit']['value'],
                                 reply_markup=back_to_main_menu_btn)

                await state.set_state(UsersEditProfileState.value)

                return
            else:
                value = msg.text

        elif property == "resources":
            is_valid, result = await self.validator.validate_resources(resources=msg.text)

            if not is_valid:
                await msg.answer(result)
                await msg.answer(self.replicas['user']['edit']['value'],
                                 reply_markup=back_to_main_menu_btn)

                await state.set_state(UsersEditProfileState.value)

                return
            else:
                value = msg.text

        elif property == "expertise":
            is_valid, result = await self.validator.validate_expertise(expertise=msg.text)

            if not is_valid:
                await msg.answer(result)
                await msg.answer(self.replicas['user']['edit']['value'],
                                 reply_markup=back_to_main_menu_btn)

                await state.set_state(UsersEditProfileState.value)

                return
            else:
                value = msg.text

        update_profile = await self.users_service.edit_profile(
            chat_id=tg_chat_id, property=property, value=value
        )
        await state.clear()

        if update_profile:
            await msg.answer(self.replicas['user']['edit']['finish'],
                             await self.users_get_profile(msg=msg))
        else:
            await msg.answer(self.replicas['general']['error'],
                             reply_markup=back_to_main_menu_btn)
