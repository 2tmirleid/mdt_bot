def create_users_for_events_model():
    return """CREATE TABLE IF NOT EXISTS users_for_events (
        _id      SERIAL PRIMARY KEY,
        user_id  SERIAL REFERENCES users  (_id),
        event_id SERIAL REFERENCES events (_id)
    )"""