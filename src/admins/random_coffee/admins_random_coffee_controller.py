from aiogram.types import Message, InlineKeyboardMarkup

from src.admins.keyboards.inline.admins_inline_keyboards import AdminsInlineKeyboards
from src.admins.keyboards.reply.admins_reply_keyboards import AdminsReplyKeyboards
from src.admins.random_coffee.admins_random_coffee_service import AdminsRandomCoffeeService
from utils.RCS.controller import Controller
from utils.lexicon.load_lexicon import load_lexicon


class AdminsRandomCoffeeController(Controller):
    def __init__(self):
        super().__init__()
        self.admins_service: AdminsRandomCoffeeService = AdminsRandomCoffeeService()

        self.admins_reply_keyboards: AdminsReplyKeyboards = AdminsReplyKeyboards()
        self.admins_inline_keyboards: AdminsInlineKeyboards = AdminsInlineKeyboards()

        self.lexicon = load_lexicon()
        self.replicas = self.lexicon.get("replicas")

    async def admins_get_count_subscribed_users_for_random_coffee(self) -> int:
        count = await self.admins_service.get_count_subscribed_users_for_random_coffee()

        return count[0][0]

    async def admins_get_count_unsubscribed_users_for_random_coffee(self) -> int:
        count = await self.admins_service.get_count_unsubscribed_users_for_random_coffee()

        return count[0][0]

    async def admins_get_random_coffee_info(self, msg: Message) -> None:
        keyboard = await self.admins_reply_keyboards.admins_random_coffee_panel_keyboard()

        await msg.answer(self.replicas['admin']['other']['option'],
                         reply_markup=keyboard)

    async def admins_export_subscribed_for_random_coffee(self, msg: Message, offset=0, edit=False) -> None:
        try:
            back_to_main_menu_btn = await (self.admins_inline_keyboards.
                                           admins_dynamic_entity_to_main_menu_panel_keyboard())

            users = await self.admins_service.get_subscribed_users_for_random_coffee(offset=offset)

            users_count = await self.admins_service.get_count_subscribed_users_for_random_coffee()

            pages = users_count[0][0]

            pagen_callback_data = f"_subs_for_random_coffee-{offset}"

            if pages > 0:
                pagen = await self.build_admins_pagen(
                    pages=pages,
                    offset=offset,
                    callback_data=pagen_callback_data
                )

                keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                        pagen,
                        back_to_main_menu_btn
                    ])

                full_name = users[0]['full_name']

                username = users[0]['tg_username']

                msg_text = (f"{offset + 1} из {pages}\n\n"
                            f"<b><a href='https://t.me/{username}'>{full_name}</a></b>")

                if edit:
                    await msg.edit_text(text=msg_text,
                                        parse_mode="HTML",
                                        reply_markup=keyboard)
                else:
                    await msg.answer(text=msg_text,
                                     parse_mode="HTML",
                                     reply_markup=keyboard)
            else:
                back_to_main_menu_btn = await (self.admins_inline_keyboards.
                                               admins_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

                await msg.answer(self.replicas['admin']['other']['empty'],
                                 reply_markup=back_to_main_menu_btn)
        except Exception as e:
            print(f"Error while getting subs for random_coffee by admin: {e}")

            back_to_main_menu_btn = await (self.admins_inline_keyboards.
                                           admins_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

            await msg.answer(self.replicas['general']['error'],
                             reply_markup=back_to_main_menu_btn)

    async def admins_export_unsubscribed_for_random_coffee(self, msg: Message, offset=0, edit=False) -> None:
        try:
            back_to_main_menu_btn = await (self.admins_inline_keyboards.
                                           admins_dynamic_entity_to_main_menu_panel_keyboard())

            users = await self.admins_service.get_unsubscribed_users_for_random_coffee(offset=offset)

            users_count = await self.admins_service.get_count_unsubscribed_users_for_random_coffee()

            pages = users_count[0][0]

            pagen_callback_data = f"_unsubs_for_random_coffee-{offset}"

            if pages > 0:
                pagen = await self.build_admins_pagen(
                    pages=pages,
                    offset=offset,
                    callback_data=pagen_callback_data
                )

                keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                        pagen,
                        back_to_main_menu_btn
                    ])

                full_name = users[0]['full_name']

                username = users[0]['tg_username']

                msg_text = (f"{offset + 1} из {pages}\n\n"
                            f"<b><a href='https://t.me/{username}'>{full_name}</a></b>")

                if edit:
                    await msg.edit_text(text=msg_text,
                                        parse_mode="HTML",
                                        reply_markup=keyboard)
                else:
                    await msg.answer(text=msg_text,
                                     parse_mode="HTML",
                                     reply_markup=keyboard)
            else:
                back_to_main_menu_btn = await (self.admins_inline_keyboards.
                                               admins_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

                await msg.answer(self.replicas['admin']['other']['empty'],
                                 reply_markup=back_to_main_menu_btn)
        except Exception as e:
            print(f"Error while getting unsubs for random_coffee by admin: {e}")

            back_to_main_menu_btn = await (self.admins_inline_keyboards.
                                           admins_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

            await msg.answer(self.replicas['general']['error'],
                             reply_markup=back_to_main_menu_btn)
