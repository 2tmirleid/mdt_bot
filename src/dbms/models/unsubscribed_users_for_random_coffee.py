def create_unsubscribed_users_for_random_coffee_model() -> str:
    return f"""
        CREATE TABLE IF NOT EXISTS unsubscribed_users_for_random_coffee (
            _id     SERIAL PRIMARY KEY,
            user_id SERIAL REFERENCES users (_id)
            ON UPDATE CASCADE ON DELETE CASCADE
        );
    """