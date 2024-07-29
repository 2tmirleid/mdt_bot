import asyncio
import os

from dotenv import load_dotenv, find_dotenv

from src.admins import admins_router
from src.admins.events import admins_events_router
from src.admins.forms import admins_forms_router
from src.dbms.models.events import create_events_model
from src.dbms.models.unsubscribed_users_for_random_coffee import create_unsubscribed_users_for_random_coffee_model
from src.dbms.models.users import create_users_model
from src.dbms.models.users_for_events import create_users_for_events_model
from src.dbms.models.users_for_random_coffee import create_users_for_random_coffee_model
from src.users import users_router
from src.users.about import users_about_router
from src.users.auth import users_auth_router
from src.users.calendar import users_calendar_router
from src.users.contacts import users_contacts_router
from src.users.random_coffee import users_random_coffee_router
from src.users.residents import users_residents_router
from utils.ibot_engine_factory.factory import IBotEngineFactory

"""Main app class"""


class Main:
    def __init__(self):
        load_dotenv(find_dotenv())

        self.bot = IBotEngineFactory(token=os.environ["TOKEN"],
                                     models=[
                                         create_users_model,
                                         create_events_model,
                                         create_users_for_events_model,
                                         create_users_for_random_coffee_model,
                                         create_unsubscribed_users_for_random_coffee_model
                                     ],
                                     routers=[
                                         admins_router.router,
                                         admins_forms_router.router,
                                         admins_events_router.router,

                                         users_router.router,
                                         users_auth_router.router,
                                         users_about_router.router,
                                         users_contacts_router.router,
                                         users_residents_router.router,
                                         users_calendar_router.router,
                                         users_random_coffee_router.router
                                     ])

    async def start(self):
        await self.bot.launch()


if __name__ == "__main__":
    main = Main()
    asyncio.run(main.start())
