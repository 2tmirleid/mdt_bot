def create_events_model():
    return """CREATE TABLE IF NOT EXISTS events (
        _id              SERIAL       PRIMARY KEY,
        photo_id         VARCHAR(255),
        title            VARCHAR(150),
        city             VARCHAR(100),
        description      VARCHAR(600),
        event_date       VARCHAR(10),
        is_active        BOOLEAN      DEFAULT TRUE
    )"""