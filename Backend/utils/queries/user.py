class UserQueries:
    """사용자 관련 쿼리"""

    CREATE_TABLE = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            profile_image_path TEXT DEFAULT 'upload/profile/default.jpg',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT TRUE
        )
    """

    INSERT_USER_WITHOUT_PROFILE = """
        INSERT INTO users (username, email, password_hash, salt)
        VALUES (?, ?, ?, ?)
    """

    INSERT_USER_WITH_PROFILE = """
        INSERT INTO users (username, email, password_hash, salt, profile_image_path)
        VALUES (?, ?, ?, ?, ?)
    """

    SELECT_BY_USERNAME = """
        SELECT * FROM users WHERE username = ?
    """

    SELECT_BY_EMAIL = """
        SELECT * FROM users WHERE email = ?
    """

    SELECT_BY_ID = """
        SELECT * FROM users WHERE id = ?
    """

    SELECT_BY_USERNAME_LIKE = """
        SELECT * FROM users WHERE username LIKE ?
    """

    DELETE_USER_BY_USERNAME = """
        DELETE FROM users WHERE username = ?
    """

    UPDATE_PROFILE_IMAGE_PATH_BY_USERNAME = """
        UPDATE users SET profile_image_path = ? WHERE username = ?
    """

    UPDATE_PROFILE_IMAGE_PATH_BY_ID = """
        UPDATE users SET profile_image_path = ? WHERE id = ?
    """

    UPDATE_USER_BY_ID = """
        UPDATE users SET {} WHERE id = ?
    """

    SELECT_USER_BY_EMAIL_AND_NOT_ID = """
        SELECT * FROM users WHERE email = ? AND id != ?
    """
