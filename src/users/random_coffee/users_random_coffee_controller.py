from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from src.users.keyboards.inline.users_inline_keyboards import UsersInlineKeyboards
from src.users.keyboards.reply.users_reply_keyboards import UsersReplyKeyboards
from src.users.random_coffee.users_random_coffee_service import UsersRandomCoffeeService
from utils.RCS.controller import Controller
from utils.lexicon.load_lexicon import load_lexicon
from utils.validator import Validator


class UsersRandomCoffeeController(Controller):
    def __init__(self):
        super().__init__()

        self.users_service: UsersRandomCoffeeService = UsersRandomCoffeeService()

        self.users_reply_keyboards: UsersReplyKeyboards = UsersReplyKeyboards()
        self.users_inline_keyboards: UsersInlineKeyboards = UsersInlineKeyboards()

        self.validator: Validator = Validator()

        self.lexicon = load_lexicon()
        self.replicas = self.lexicon.get("replicas")
        self.buttons = self.lexicon.get("buttons")
        self.callback_data = self.lexicon.get("callback_data")

    async def users_get_random_coffee_info(self, msg: Message) -> None:
        chat_id = msg.from_user.id
        user_id = await self.users_service.get_user_id_by_tg_chat_id(chat_id)

        user = await self.users_service.get_if_user_in_random_coffee(user_id[0]['_id'])

        subscribe = user[0][0]

        back_to_main_menu_keyboard = await (self.users_inline_keyboards.
                                            users_dynamic_entity_to_main_menu_panel_keyboard())

        buttons = []

        if not subscribe:
            buttons.append(
                InlineKeyboardButton(text=self.buttons['user']['random_coffee']['subscribe'],
                                     callback_data=self.callback_data['user']['random_coffee']['subscribe'] +
                                                   f"-{user_id[0]['_id']}")
            )
        else:
            buttons.append(
                InlineKeyboardButton(text=self.buttons['user']['random_coffee']['unsubscribe'],
                                     callback_data=self.callback_data['user']['random_coffee']['unsubscribe'] +
                                                   f"-{user_id[0]['_id']}")
            )

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                buttons,
                back_to_main_menu_keyboard
            ]
        )

        await msg.answer(self.replicas['general']['random_coffee'],
                         parse_mode="HTML",
                         reply_markup=keyboard)

    async def users_subscribe_for_random_coffee(self, msg: Message, user_id) -> None:
        try:
            back_to_main_menu_btn = await (self.users_inline_keyboards.
                                           users_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

            is_user_subscribed = await self.users_service.get_if_user_in_random_coffee(user_id)

            if not is_user_subscribed[0][0]:
                user = await self.users_service.get_if_user_unsubscribed_for_random_coffee(user_id=user_id)

                if user:
                    await self.users_service.delete_user_from_unsubscribed_for_random_coffee(user_id=user_id)

                subscribe = await self.users_service.subscribe_user_for_random_coffee(user_id)

                if subscribe:
                    await msg.answer(self.replicas['user']['random_coffee']['subscribe'],
                                     reply_markup=back_to_main_menu_btn)
                else:
                    await msg.answer(self.replicas['general']['error'],
                                     reply_markup=back_to_main_menu_btn)
        except Exception as e:
            print(f"Error while subscribing user for random_coffee: {e}")

            back_to_main_menu_btn = await (self.users_inline_keyboards.
                                           users_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

            await msg.answer(self.replicas['general']['error'],
                             reply_markup=back_to_main_menu_btn)

    async def users_unsubscribe_for_random_coffee(self, msg: Message, user_id) -> None:
        try:
            back_to_main_menu_btn = await (self.users_inline_keyboards.
                                           users_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

            is_user_unsubscribed = await self.users_service.get_if_user_unsubscribed_for_random_coffee(user_id=user_id)

            if not is_user_unsubscribed[0][0]:
                user = await self.users_service.get_if_user_in_random_coffee(user_id)

                if user:
                    await self.users_service.delete_user_from_users_for_random_coffee(user_id=user_id)

                unsubscribe = await self.users_service.unsubscribe_user_for_random_coffee(user_id=user_id)

                if unsubscribe:
                    await msg.answer(self.replicas['user']['random_coffee']['unsubscribe'],
                                     reply_markup=back_to_main_menu_btn)
                else:
                    await msg.answer(self.replicas['general']['error'],
                                     reply_markup=back_to_main_menu_btn)
        except Exception as e:
            print(f"Error while unsubscribing user for random_coffee: {e}")

            back_to_main_menu_btn = await (self.users_inline_keyboards.
                                           users_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

            await msg.answer(self.replicas['general']['error'],
                             reply_markup=back_to_main_menu_btn)
