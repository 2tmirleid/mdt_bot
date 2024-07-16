from utils.ibot_engine_factory.date.date_formatter import IBotEngineDateFormatter


class AdminsErrorsFormatter:
    def __init__(self) -> None:
        self.date_formatter: IBotEngineDateFormatter = IBotEngineDateFormatter()

    async def forbidden_access(self, interloper_id) -> str:
        return f"[FORBIDDEN] - [{await self.date_formatter.get_date()}] - Пользователь с ID {interloper_id} пытался зайти как администратор"