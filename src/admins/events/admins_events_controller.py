from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InputMediaPhoto

from src.admins.events.admins_events_service import AdminsEventsService
from src.admins.keyboards.inline.admins_inline_keyboards import AdminsInlineKeyboards
from src.admins.keyboards.reply.admins_reply_keyboards import AdminsReplyKeyboards
from src.states.admins.events.admins_choose_events_city import AdminsChooseEventsCity
from utils.RCS.controller import Controller
from utils.lexicon.load_lexicon import load_lexicon


class AdminsEventsController(Controller):
    def __init__(self):
        super().__init__()

        self.admins_service: AdminsEventsService = AdminsEventsService()

        self.admins_reply_keyboards: AdminsReplyKeyboards = AdminsReplyKeyboards()
        self.admins_inline_keyboards: AdminsInlineKeyboards = AdminsInlineKeyboards()

        self.lexicon = load_lexicon()
        self.replicas = self.lexicon.get("replicas")

        self.city = None

    # Выбор города админом
    async def choose_city(self, msg: Message, state: FSMContext) -> None:
        keyboard = await self.admins_reply_keyboards.admins_events_city_panel_keyboard()

        await msg.answer(self.replicas['admin']['events']['choice'],
                         reply_markup=keyboard)

        await state.set_state(AdminsChooseEventsCity.city)

    # Вывод мероприятий с учетом выбранного города
    async def admins_get_events(self, msg: Message, state: FSMContext, offset=0, edit=False) -> None:
        try:
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

                # Соединение всех кнопок в одну клавиатуру
                keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                        pagen,
                        buttons,
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
