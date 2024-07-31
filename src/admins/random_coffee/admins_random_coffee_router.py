from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from src.admins.random_coffee.admins_random_coffee_controller import AdminsRandomCoffeeController
from src.middlewares.admins_middleware import AdminsMiddleware
from utils.lexicon.load_lexicon import load_lexicon

router: Router = Router()

# Подключение middleware для защиты от несанкцианированного доступа в админку
router.message.middleware(AdminsMiddleware())
# router.callback_query.middleware(AdminsMiddleware())

admins_controller: AdminsRandomCoffeeController = AdminsRandomCoffeeController()

lexicon = load_lexicon()

replicas = lexicon.get("replicas")
buttons = lexicon.get("buttons")
callback_data = lexicon.get("callback_data")


@router.message(F.text == buttons['admin']['main_panel']['random_coffee']['main'])
async def process_admins_get_random_coffee_info(msg: Message) -> None:
    await admins_controller.admins_get_random_coffee_info(msg)


""" Обработка подписчиков """


@router.message(F.text == buttons['admin']['main_panel']['random_coffee']['subscribed'])
async def process_admins_get_subs_for_random_coffee(msg: Message) -> None:
    await admins_controller.admins_export_subscribed_for_random_coffee(msg)


# Обработка кнопки пагинации >> для подписанных
@router.callback_query(lambda query: query.data.startswith("admins_pagen_next_subs_for_random_coffee"))
async def process_admins_pagen_next_subs(clb_query: CallbackQuery, state: FSMContext) -> None:
    offset_split = str(clb_query.data.split("-")[1])

    offset = int(offset_split) + 1

    await admins_controller.admins_export_subscribed_for_random_coffee(msg=clb_query.message,
                                                                       offset=offset,
                                                                       edit=True)


# Обработка кнопки пагинации << для подписанных
@router.callback_query(lambda query: query.data.startswith("admins_pagen_backward_subs_for_random_coffee"))
async def process_admins_pagen_backward_subs(clb_query: CallbackQuery, state: FSMContext) -> None:
    offset_split = str(clb_query.data.split("-")[1])
    offset = int(offset_split) - 1

    await admins_controller.admins_export_subscribed_for_random_coffee(msg=clb_query.message,
                                                                       offset=offset,
                                                                       edit=True)


# Обработка кнопки пагинации "В начало" для подписанных
@router.callback_query(lambda query: query.data.startswith("admins_pagen_start_subs_for_random_coffee"))
async def process_admins_pagen_start_subs(clb_query: CallbackQuery, state: FSMContext) -> None:
    offset = 0

    await admins_controller.admins_export_subscribed_for_random_coffee(msg=clb_query.message,
                                                                       offset=offset,
                                                                       edit=True)


# Обработка кнопки пагинации "В конец" для подписанных
@router.callback_query(lambda query: query.data.startswith("admins_pagen_end_subs_for_random_coffee"))
async def process_admins_pagen_end_subs(clb_query: CallbackQuery, state: FSMContext) -> None:
    offset = await admins_controller.admins_get_count_subscribed_users_for_random_coffee() - 1

    await admins_controller.admins_export_subscribed_for_random_coffee(msg=clb_query.message,
                                                                       offset=offset,
                                                                       edit=True)


""" Конец обработки подписчиков """

""" Обработка отписчиков """


@router.message(F.text == buttons['admin']['main_panel']['random_coffee']['unsubscribed'])
async def process_admins_get_unsubs_for_random_coffee(msg: Message) -> None:
    await admins_controller.admins_export_unsubscribed_for_random_coffee(msg)


# Обработка кнопки пагинации >> для отписанных
@router.callback_query(lambda query: query.data.startswith("admins_pagen_next_unsubs_for_random_coffee"))
async def process_admins_pagen_next_unsubs(clb_query: CallbackQuery, state: FSMContext) -> None:
    offset_split = str(clb_query.data.split("-")[1])

    offset = int(offset_split) + 1

    await admins_controller.admins_export_unsubscribed_for_random_coffee(msg=clb_query.message,
                                                                         offset=offset,
                                                                         edit=True)


# Обработка кнопки пагинации << для отписанных
@router.callback_query(lambda query: query.data.startswith("admins_pagen_backward_unsubs_for_random_coffee"))
async def process_admins_pagen_backward_unsubs(clb_query: CallbackQuery, state: FSMContext) -> None:
    offset_split = str(clb_query.data.split("-")[1])
    offset = int(offset_split) - 1

    await admins_controller.admins_export_unsubscribed_for_random_coffee(msg=clb_query.message,
                                                                         offset=offset,
                                                                         edit=True)


# Обработка кнопки пагинации "В начало" для отписанных
@router.callback_query(lambda query: query.data.startswith("admins_pagen_start_unsubs_for_random_coffee"))
async def process_admins_pagen_start_unsubs(clb_query: CallbackQuery, state: FSMContext) -> None:
    offset = 0

    await admins_controller.admins_export_unsubscribed_for_random_coffee(msg=clb_query.message,
                                                                         offset=offset,
                                                                         edit=True)


# Обработка кнопки пагинации "В конец" для отписанных
@router.callback_query(lambda query: query.data.startswith("admins_pagen_end_unsubs_for_random_coffee"))
async def process_admins_pagen_end_unsubs(clb_query: CallbackQuery, state: FSMContext) -> None:
    offset = await admins_controller.admins_get_count_unsubscribed_users_for_random_coffee() - 1

    await admins_controller.admins_export_unsubscribed_for_random_coffee(msg=clb_query.message,
                                                                         offset=offset,
                                                                         edit=True)


""" Конец обработки отписчиков """
