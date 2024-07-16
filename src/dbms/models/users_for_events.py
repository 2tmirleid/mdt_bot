def create_users_for_events_model():
    return """CREATE TABLE IF NOT EXISTS users_for_events (
        _id         SERIAL       PRIMARY KEY,
        tg_chat_id  VARCHAR(255),
        event_id    VARCHAR(255)
    )"""