from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InputMediaPhoto, InlineKeyboardButton

from src.states.admins.events.admins_choose_events_city import AdminsChooseEventsCity
from src.states.users.users_choose_events_city import UsersChooseEventsCity
from src.users.calendar.users_calendar_service import UsersCalendarService
from src.users.keyboards.inline.users_inline_keyboards import UsersInlineKeyboards
from src.users.keyboards.reply.users_reply_keyboards import UsersReplyKeyboards
from utils.RCS.controller import Controller
from utils.lexicon.load_lexicon import load_lexicon
from utils.validator import Validator


class UsersCalendarController(Controller):
    def __init__(self):
        super().__init__()

        self.users_service:  UsersCalendarService = UsersCalendarService()

        self.users_reply_keyboards: UsersReplyKeyboards = UsersReplyKeyboards()
        self.users_inline_keyboards: UsersInlineKeyboards = UsersInlineKeyboards()

        self.validator: Validator = Validator()

        self.lexicon = load_lexicon()
        self.replicas = self.lexicon.get("replicas")

        self.city = None
        self.chat_id = None

    async def users_get_events_count(self, city: str) -> int:
        count = await self.users_service.get_events_count(city=city)

        return count[0][0]

    async def users_choose_city(self, msg: Message, state: FSMContext) -> None:
        keyboard = await self.users_reply_keyboards.users_events_city_panel_keyboard()

        await msg.answer(self.replicas['user']['events']['choice'],
                         reply_markup=keyboard)

        await state.set_state(UsersChooseEventsCity.city)

    async def users_get_events(self, msg: Message, state: FSMContext, offset=0, edit=False) -> None:
        try:
            if self.city is not None:
                available_cities = ["саранск", "москва"]

                if self.city.lower() not in available_cities:
                    await msg.answer(self.replicas['user']['events']['incorrect_city'])

                    await state.set_state(UsersChooseEventsCity.city)

                    return

            await state.clear()

            # Получение мероприятий с LIMIT 1 и OFFSET = offset
            events = await self.users_service.get_active_events(offset=offset, city=self.city)

            # Получение кол-ва мероприятий
            events_count = await self.users_service.get_events_count(city=self.city)

            back_to_main_menu_btn = await (self.users_inline_keyboards.
                                           users_dynamic_entity_to_main_menu_panel_keyboard())

            pages = events_count[0][0]

            # callback_data для кнопок пагинации
            pagen_callback_data = f"_events-{offset}"

            if pages > 0:
                # Формирование кнопок пагинации
                pagen = await self.build_users_pagen(
                    pages=pages,
                    offset=offset,
                    callback_data=pagen_callback_data
                )

                register_btn = []

                event_id = events[0]['_id']
                user_id = await self.users_service.get_user_id_by_chat_id(self.chat_id)

                is_user_for_event = await self.users_service.is_user_for_event(
                    user_id=user_id[0]['_id'],
                    event_id=event_id
                )

                if len(is_user_for_event) < 1:
                    register_btn.append(
                        InlineKeyboardButton(text="Иду", callback_data=f"user_register_for_event-{user_id[0]['_id']}-{event_id}-{offset}")
                    )
                else:
                    register_btn.append(
                        InlineKeyboardButton(text="Не иду", callback_data=f"user_unregister_for_event-{user_id[0]['_id']}-{event_id}-{offset}")
                    )

                # Соединение всех кнопок в одну клавиатуру
                keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                        pagen,
                        register_btn,
                        back_to_main_menu_btn
                    ])

                photo = events[0]['photo']

                msg_text = (f"{offset + 1} из {pages}\n\n"
                            f"<b>{events[0]['title']}</b>\n\n"
                            f"Описание:\n{events[0]['description']}\n\n"
                            f"Город: <i>{events[0]['city']}</i>\n\n"
                            f"Дата проведения: <i><u>{events[0]['event_date']}</u></i>\n\n")

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
            print(f"Error while getting events by user: {e}")

            back_to_main_menu_btn = await (self.users_inline_keyboards.
                                           users_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

            await msg.answer(self.replicas['general']['error'],
                             reply_markup=back_to_main_menu_btn)

    async def register_user_for_event(self, msg: Message, state: FSMContext, user_id, event_id, offset) -> None:
        register = await self.users_service.register_user_for_event(user_id, event_id)

        if register:
            await self.users_get_events(
                msg=msg,
                state=state,
                offset=offset
            )

            await msg.answer(self.replicas['user']['events']['register'])

            return
        else:
            back_to_main_menu_btn = await (self.users_inline_keyboards.
                                           users_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

            await msg.answer(self.replicas['general']['error'],
                             reply_markup=back_to_main_menu_btn)

    async def unregister_user_for_event(self, msg: Message, state: FSMContext, user_id, event_id, offset) -> None:
        unregister = await self.users_service.unregister_user_for_event(user_id, event_id)

        if unregister:
            await self.users_get_events(
                msg=msg,
                state=state,
                offset=offset
            )

            await msg.answer(self.replicas['user']['events']['unregister'])

            return
        else:
            back_to_main_menu_btn = await (self.users_inline_keyboards.
                                           users_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

            await msg.answer(self.replicas['general']['error'],
                             reply_markup=back_to_main_menu_btn)
