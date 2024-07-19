from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InputMediaPhoto

from src.admins.events.admins_events_service import AdminsEventsService
from src.admins.keyboards.inline.admins_inline_keyboards import AdminsInlineKeyboards
from src.admins.keyboards.reply.admins_reply_keyboards import AdminsReplyKeyboards
from src.states.admins.events.admins_choose_events_city import AdminsChooseEventsCity
from src.states.admins.events.create_events_state import CreateEventsState
from utils.RCS.controller import Controller
from utils.lexicon.load_lexicon import load_lexicon
from utils.validator import Validator


class AdminsEventsController(Controller):
    def __init__(self):
        super().__init__()

        self.validator: Validator = Validator()

        self.admins_service: AdminsEventsService = AdminsEventsService()

        self.admins_reply_keyboards: AdminsReplyKeyboards = AdminsReplyKeyboards()
        self.admins_inline_keyboards: AdminsInlineKeyboards = AdminsInlineKeyboards()

        self.lexicon = load_lexicon()
        self.replicas = self.lexicon.get("replicas")

        self.city = None
        self.event_id = None

    async def admins_get_events_count(self, city: str) -> int:
        count = await self.admins_service.get_events_count(city=city)

        return count[0][0]

    # Выбор города админом
    async def choose_city(self, msg: Message, state: FSMContext) -> None:
        keyboard = await self.admins_reply_keyboards.admins_events_city_panel_keyboard()

        await msg.answer(self.replicas['admin']['events']['choice'],
                         reply_markup=keyboard)

        await state.set_state(AdminsChooseEventsCity.city)

    # Вывод мероприятий с учетом выбранного города
    async def admins_get_events(self, msg: Message, state: FSMContext, offset=0, edit=False) -> None:
        try:
            if self.city is not None:
                available_cities = ["саранск", "москва"]

                if self.city.lower() not in available_cities:
                    await msg.answer(self.replicas['admin']['events']['incorrect_city'])

                    await state.set_state(AdminsChooseEventsCity.city)

                    return

            await state.clear()

            # Получение мероприятий с LIMIT 1 и OFFSET = offset
            events = await self.admins_service.get_events(offset=offset, city=self.city)

            # Получение кол-ва мероприятий
            events_count = await self.admins_service.get_events_count(city=self.city)

            back_to_main_menu_btn = await (self.admins_inline_keyboards.
                                           admins_dynamic_entity_to_main_menu_panel_keyboard())

            pages = events_count[0][0]

            # callback_data для кнопок пагинации
            pagen_callback_data = f"_events-{offset}"

            if pages > 0:
                inline_callback_data = f"_events-{events[0]['_id']}"
                export_callback_data = f"_users_for_events-{events[0]['_id']}"

                # Формирование кнопок пагинации
                pagen = await self.build_admins_pagen(
                    pages=pages,
                    offset=offset,
                    callback_data=pagen_callback_data
                )

                # Формирование кнопок для мероприятий
                buttons = await self.admins_inline_keyboards.admins_dynamic_entity_keyboard(
                    callback_data=inline_callback_data
                )

                export_btn = await self.admins_inline_keyboards.admins_export_event_inline_keyboard(
                    callback_data=export_callback_data
                )

                # Соединение всех кнопок в одну клавиатуру
                keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                        pagen,
                        buttons,
                        export_btn,
                        back_to_main_menu_btn
                    ])

                photo = events[0]['photo_id']

                msg_text = (f"{offset + 1} из {pages}\n\n"
                            f"<b>{events[0]['title']}</b>\n\n"
                            f"Описание:\n{events[0]['description']}\n\n"
                            f"Город: <i>{events[0]['city']}</i>\n\n"
                            f"Дата проведения: <i><u>{events[0]['event_date']}</u></i>\n\n"
                            f"Статус: {"Активно" if events[0]['is_active'] else "Не активно"}")

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
            print(f"Error while getting events by admin: {e}")

            back_to_main_menu_btn = await (self.admins_inline_keyboards.
                                           admins_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

            await msg.answer(self.replicas['general']['error'],
                             reply_markup=back_to_main_menu_btn)

    async def admins_add_event_photo(self, msg: Message, state: FSMContext) -> None:
        back_to_main_menu_btn = await (self.admins_inline_keyboards.
                                       admins_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

        await msg.answer(self.replicas['admin']['entities']['create']['photo'],
                         reply_markup=back_to_main_menu_btn)

        await state.set_state(CreateEventsState.photo)

    async def admins_add_event_title(self, msg: Message, state: FSMContext) -> None:
        await state.update_data(photo=msg.photo[-1].file_id)

        back_to_main_menu_btn = await (self.admins_inline_keyboards.
                                       admins_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

        await msg.answer(self.replicas['admin']['entities']['create']['title'],
                         reply_markup=back_to_main_menu_btn)

        await state.set_state(CreateEventsState.title)

    async def admins_add_event_description(self, msg: Message, state: FSMContext) -> None:
        back_to_main_menu_btn = await (self.admins_inline_keyboards.
                                       admins_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

        is_valid, result = await self.validator.validate_title(title=msg.text)

        if not is_valid:
            await msg.answer(result)
            await msg.answer(self.replicas['admin']['entities']['create']['title'],
                             reply_markup=back_to_main_menu_btn)

            await state.set_state(CreateEventsState.title)

            return
        else:
            await state.update_data(title=msg.text)

            await msg.answer(self.replicas['admin']['entities']['create']['description'],
                             reply_markup=back_to_main_menu_btn)

            await state.set_state(CreateEventsState.description)

    async def admins_add_event_date(self, msg: Message, state: FSMContext) -> None:
        back_to_main_menu_btn = await (self.admins_inline_keyboards.
                                       admins_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

        is_valid, result = await self.validator.validate_description(description=msg.text)

        if not is_valid:
            await msg.answer(result)
            await msg.answer(self.replicas['admin']['entities']['create']['description'],
                             reply_markup=back_to_main_menu_btn)

            await state.set_state(CreateEventsState.description)
        else:
            await state.update_data(description=msg.text)

            await msg.answer(self.replicas['admin']['entities']['create']['date'],
                             reply_markup=back_to_main_menu_btn)

            await state.set_state(CreateEventsState.event_date)

    async def admins_add_event_city(self, msg: Message, state: FSMContext) -> None:
        back_to_main_menu_btn = await (self.admins_inline_keyboards.
                                       admins_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

        is_valid, result = await self.validator.validate_date(date=msg.text)

        if not is_valid:
            await msg.answer(result)
            await msg.answer(self.replicas['admin']['entities']['create']['date'],
                             reply_markup=back_to_main_menu_btn)

            await state.set_state(CreateEventsState.event_date)
        else:
            back_to_main_menu_btn = await (self.admins_inline_keyboards.
                                           admins_dynamic_entity_to_main_menu_panel_keyboard())

            buttons = await self.admins_inline_keyboards.admins_events_city_inline_keyboard()

            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    *buttons,
                    back_to_main_menu_btn
                ])

            await state.update_data(event_date=msg.text)

            await msg.answer(self.replicas['admin']['entities']['create']['city'],
                             reply_markup=keyboard)

            await state.set_state(CreateEventsState.city)

    async def admins_add_event_finish(self, msg: Message, state: FSMContext, city: str) -> None:
        is_valid, result = await self.validator.validate_city(city=city)

        if not is_valid:
            back_to_main_menu_btn = await (self.admins_inline_keyboards.
                                           admins_dynamic_entity_to_main_menu_panel_keyboard())

            buttons = await self.admins_inline_keyboards.admins_events_city_inline_keyboard()

            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    *buttons,
                    back_to_main_menu_btn
                ])

            await msg.answer(result,
                             reply_markup=keyboard)

            await state.set_state(CreateEventsState.city)
        else:
            await state.update_data(city=city)

            data = await state.get_data()

            photo = data.get("photo")
            title = data.get("title")
            description = data.get("description")
            event_date = data.get("event_date")
            city = data.get("city")

            await state.clear()

            event = {
                "photo": photo,
                "title": title,
                "description": description,
                "event_date": event_date,
                "city": city
            }

            insert_event = await self.admins_service.add_event(event=event)

            if insert_event:
                await msg.answer(self.replicas['admin']['entities']['create']['finish'])

                await self.admins_get_events(msg=msg, state=state)
            else:
                back_to_main_menu_btn = await (self.admins_inline_keyboards.
                                               admins_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

                await msg.answer(self.replicas['general']['error'],
                                 reply_markup=back_to_main_menu_btn)

    async def admins_export_events(self, msg: Message, event_id, offset=0, edit=False) -> None:
        try:
            users = await self.admins_service.get_users_for_event(event_id=event_id, offset=offset)

            users_count = await self.admins_service.get_users_count_for_event(event_id=event_id)

            back_to_main_menu_btn = await (self.admins_inline_keyboards.
                                           admins_dynamic_entity_to_main_menu_panel_keyboard())

            pages = users_count[0][0]

            pagen_callback_data = f"_users_for_events-{offset}"

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
            print(f"Error while getting users for events by admin: {e}")

            back_to_main_menu_btn = await (self.admins_inline_keyboards.
                                           admins_dynamic_entity_to_main_menu_panel_keyboard(markup=True))

            await msg.answer(self.replicas['general']['error'],
                             reply_markup=back_to_main_menu_btn)

    async def admins_get_users_count_for_events(self, event_id) -> int:
        count = await self.admins_service.get_users_count_for_event(event_id=event_id)

        return count[0][0]
