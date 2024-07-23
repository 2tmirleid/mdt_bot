def create_users_model():
    return """CREATE TABLE IF NOT EXISTS users (
        _id              SERIAL       PRIMARY KEY,
        tg_chat_id       VARCHAR(30)  UNIQUE,
        tg_username      VARCHAR(100) UNIQUE,
        phone            VARCHAR(12)  UNIQUE,
        photo            VARCHAR(255),
        full_name        VARCHAR(100),
        birth_date       VARCHAR(10),
        city             VARCHAR(50),
        company          VARCHAR(100),
        position         VARCHAR(100),
        rm_status        VARCHAR(100),
        hobbies          VARCHAR(120),
        resources        VARCHAR(120),
        expertise        VARCHAR(120),
        is_approved      BOOLEAN      DEFAULT FALSE,
        is_rejected      BOOLEAN      DEFAULT FALSE,
        is_admin         BOOLEAN      DEFAULT FALSE
    )"""