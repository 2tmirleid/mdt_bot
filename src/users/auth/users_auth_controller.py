import os

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.states.users.auth.users_auth_state import UsersAuthState
from src.users.auth.users_auth_service import UsersAuthService
from src.users.keyboards.reply.users_reply_keyboards import UsersReplyKeyboards
from src.users.users_service import UsersService
from utils.RCS.controller import Controller
from utils.lexicon.load_lexicon import load_lexicon
from utils.smtp.smtp_factory import IBotEngineSMTPFactory
from utils.validator import Validator


class UsersAuthController(Controller):
    def __init__(self):
        super().__init__()

        self.TOKEN = os.environ["TOKEN"]
        self.bot = Bot(token=self.TOKEN)

        self.validator: Validator = Validator()

        self.email_sender: IBotEngineSMTPFactory = IBotEngineSMTPFactory()

        self.users_service: UsersService = UsersService()
        self.users_auth_service: UsersAuthService = UsersAuthService()

        self.users_reply_keyboards: UsersReplyKeyboards = UsersReplyKeyboards()

        self.lexicon = load_lexicon()
        self.replicas = self.lexicon.get("replicas")

    async def users_form_moderate(self, msg: Message) -> None:
        await msg.answer(self.replicas['general']['moderate'])

    async def users_form_rejected(self, msg: Message) -> None:
        await msg.answer(self.replicas['user']['forms']['reject'])

    async def users_already_registered(self, msg: Message) -> None:
        keyboard = await self.users_reply_keyboards.users_to_main_panel_reply_keyboard(markup=True)

        await msg.answer(self.replicas['general']['already_registered'],
                         reply_markup=keyboard)

    async def check_if_user_phone_registered(self, phone) -> bool:
        user = await self.users_service.get_user_by_phone(phone)

        return True if user else False

    async def users_start_register(self, msg: Message) -> None:
        keyboard = await self.users_reply_keyboards.users_start_register_reply_keyboard()

        await msg.answer(self.replicas['general']['not_auth'],
                         reply_markup=keyboard)

    async def users_get_phone(self, msg: Message, state: FSMContext) -> None:
        keyboard = await self.users_reply_keyboards.users_send_phone_number_reply_keyboard()

        await msg.answer(self.replicas['user']['register']['phone'],
                         reply_markup=keyboard)

        await state.set_state(UsersAuthState.phone)

    async def users_get_photo(self, msg: Message, state: FSMContext, phone) -> None:
        await state.update_data(phone=phone)

        user_id = msg.from_user.id

        photos = await self.bot.get_user_profile_photos(user_id=user_id)

        if photos.total_count == 0:
            await msg.answer(self.replicas['user']['register']['photo'])

            await state.set_state(UsersAuthState.photo)
        else:
            photo_id = photos.photos[0][-1].file_id

            await state.update_data(photo=photo_id)

            await msg.answer(self.replicas['user']['register']['full_name'])

            await state.set_state(UsersAuthState.full_name)

    async def users_get_full_name(self, msg: Message, state: FSMContext) -> None:
        if msg.photo:
            await state.update_data(photo=msg.photo[-1].file_id)

            await msg.answer(self.replicas['user']['register']['full_name'])

            await state.set_state(UsersAuthState.full_name)
        else:
            full_name = msg.text

            is_valid, result = await self.validator.validate_full_name(full_name)

            if not is_valid:
                await msg.answer(result)

                await msg.answer(self.replicas['user']['register']['full_name'])

                await state.set_state(UsersAuthState.full_name)

                return
            else:
                await state.update_data(full_name=full_name)

                await msg.answer(self.replicas['user']['register']['birth_date'])

                await state.set_state(UsersAuthState.birth_date)

    async def users_get_city(self, msg: Message, state: FSMContext) -> None:
        is_valid, result = await self.validator.validate_date(date=msg.text)

        if not is_valid:
            await msg.answer(result)

            await msg.answer(self.replicas['user']['register']['birth_date'])

            await state.set_state(UsersAuthState.birth_date)

            return
        else:
            await state.update_data(birth_date=msg.text)

            await msg.answer(self.replicas['user']['register']['city'])

            await state.set_state(UsersAuthState.city)

    async def users_get_company(self, msg: Message, state: FSMContext) -> None:
        city = msg.text

        is_valid, result = await self.validator.validate_users_city(city)

        if not is_valid:
            await msg.answer(result)

            await msg.answer(self.replicas['user']['register']['city'])

            await state.set_state(UsersAuthState.city)

            return
        else:
            await state.update_data(city=city)

            await msg.answer(self.replicas['user']['register']['company'])

            await state.set_state(UsersAuthState.company)

    async def users_get_position(self, msg: Message, state: FSMContext) -> None:
        company = msg.text

        is_valid, result = await self.validator.validate_company(company)

        if not is_valid:
            await msg.answer(result)

            await msg.answer(self.replicas['user']['register']['company'])

            await state.set_state(UsersAuthState.company)

            return
        else:
            await state.update_data(company=company)

            await msg.answer(self.replicas['user']['register']['position'])

            await state.set_state(UsersAuthState.position)

    async def users_get_rm_status(self, msg: Message, state: FSMContext) -> None:
        position = msg.text

        is_valid, result = await self.validator.validate_position(position)

        if not is_valid:
            await msg.answer(result)

            await msg.answer(self.replicas['user']['register']['position'])

            await state.set_state(UsersAuthState.position)

            return
        else:
            await state.update_data(position=position)

            await msg.answer(self.replicas['user']['register']['rm_status'])

            await state.set_state(UsersAuthState.rm_status)

    async def users_get_hobbies(self, msg: Message, state: FSMContext) -> None:
        rm_status = msg.text

        is_valid, result = await self.validator.validate_rm_status(rm_status)

        if not is_valid:
            await msg.answer(result)

            await msg.answer(self.replicas['user']['register']['rm_status'])

            await state.set_state(UsersAuthState.rm_status)

            return
        else:
            await state.update_data(rm_status=rm_status)

            await msg.answer(self.replicas['user']['register']['hobbies'])

            await state.set_state(UsersAuthState.hobbies)

    async def users_get_resources(self, msg: Message, state: FSMContext) -> None:
        hobbies = msg.text

        is_valid, result = await self.validator.validate_hobbies(hobbies)

        if not is_valid:
            await msg.answer(result)

            await msg.answer(self.replicas['user']['register']['hobbies'])

            await state.set_state(UsersAuthState.hobbies)

            return
        else:
            await state.update_data(hobbies=hobbies)

            await msg.answer(self.replicas['user']['register']['resources'])

            await state.set_state(UsersAuthState.resources)

    async def users_get_expertise(self, msg: Message, state: FSMContext) -> None:
        resources = msg.text

        is_valid, result = await self.validator.validate_resources(resources)

        if not is_valid:
            await msg.answer(result)

            await msg.answer(self.replicas['user']['register']['resources'])

            await state.set_state(UsersAuthState.resources)

            return
        else:
            await state.update_data(resources=resources)

            await msg.answer(self.replicas['user']['register']['expertise'])

            await state.set_state(UsersAuthState.expertise)

    async def users_auth_finish(self, msg: Message, state: FSMContext) -> None:
        try:
            expertise = msg.text

            is_valid, result = await self.validator.validate_expertise(expertise)

            if not is_valid:
                await msg.answer(result)

                await msg.answer(self.replicas['user']['register']['expertise'])

                await state.set_state(UsersAuthState.expertise)

                return
            else:
                data = await state.get_data()

                user = {
                    "tg_chat_id": msg.from_user.id,
                    "tg_username": msg.from_user.username,
                    "phone": data.get("phone"),
                    "photo": data.get("photo"),
                    "full_name": data.get("full_name"),
                    "birth_date": data.get("birth_date"),
                    "city": data.get("city"),
                    "company": data.get("company"),
                    "position": data.get("position"),
                    "rm_status": data.get("rm_status"),
                    "hobbies": data.get("hobbies"),
                    "resources": data.get("resources"),
                    "expertise": expertise,
                }

                email_body = f"""
                            Пользователь с никнеймом {user['tg_username']} оставил заявку на регистрацию.\n\n
                            Его анкета:\n\n
                            Никнейм: {user['tg_username']}\n
                            Телефон: {user['phone']}\n
                            ФИО: {user['full_name']}\n
                            Дата рождения: {user['birth_date']}\n
                            Город: {user['city']}\n
                            Компания: {user['company']}\n
                            Должность: {user['position']}\n
                            Отношение к Мордовии: {user['rm_status']}\n
                            Хобби/Увлечения: {user['hobbies']}\n
                            Ресурсы: {user['resources']}\n
                            Экспертиза: {user['expertise']}
                        """

                save_user = await self.users_auth_service.save_user(user=user)

                if not save_user:
                    await msg.answer(self.replicas['general']['error'])

                    return

                await self.email_sender.send_email(body=email_body)

                await msg.answer(self.replicas['user']['register']['moderate'])

                await state.clear()
        except Exception as e:
            print(f"Error while saving user from controller: {e}")

            await msg.answer(self.replicas['general']['error'])

    async def users_save_tg_chat_id_and_tg_username(self, msg: Message, phone) -> None:
        try:
            chat_id = msg.from_user.id
            username = msg.from_user.username

            user = await self.users_auth_service.save_tg_chat_id_and_tg_username(chat_id, username, phone)

            if user:
                keyboard = await self.users_reply_keyboards.users_to_main_panel_reply_keyboard(markup=True)

                await msg.answer(self.replicas['user']['register']['finish'],
                                 reply_markup=keyboard)
        except Exception as e:
            print(f"Error while updating user chat_id and username from controller: {e}")

            await msg.answer(self.replicas['general']['error'])
