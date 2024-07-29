def create_users_for_events_model() -> str:
    return """CREATE TABLE IF NOT EXISTS users_for_events (
        _id      SERIAL PRIMARY KEY,
        user_id  SERIAL REFERENCES users  (_id)
        ON UPDATE CASCADE ON DELETE CASCADE, 
        event_id SERIAL REFERENCES events (_id)        
        ON UPDATE CASCADE ON DELETE CASCADE
    )"""