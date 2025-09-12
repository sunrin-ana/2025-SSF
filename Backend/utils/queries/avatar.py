class AvatarQueries:

    CREATE_TABLE = """
        CREATE TABLE IF NOT EXISTS avatars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL,
            avatar_type TEXT NOT NULL,
            top_clothe_type TEXT,
            bottom_clothe_type TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    """

    SELECT_USER_AVATAR = """
        SELECT * FROM avatars WHERE user_id = ?
    """

    INSERT_AVATAR = """
        INSERT INTO avatars (user_id, avatar_type, top_clothe_type, bottom_clothe_type)
        VALUES (?, ?, ?, ?)
    """

    UPDATE_AVATAR = """
        UPDATE avatars SET {fields} WHERE user_id = ?
    """