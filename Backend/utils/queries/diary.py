class DiaryQueries:

    CREATE_TABLE = """
        CREATE TABLE IF NOT EXISTS diaries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            images TEXT,
            category TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_submitted BOOLEAN DEFAULT FALSE,
            email_sent BOOLEAN DEFAULT FALSE,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    """

    INSERT_DIARY = """
        INSERT INTO diaries (user_id, title, content, images, category, created_at, is_submitted, email_sent)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """

    SELECT_USER_DIARIES = """
        SELECT * FROM diaries 
        WHERE user_id = ?
        ORDER BY created_at DESC 
        LIMIT ? OFFSET ?
    """

    SELECT_USER_DIARIES_BY_CATEGORY = """
        SELECT * FROM diaries 
        WHERE user_id = ? AND category = ?
        ORDER BY created_at DESC 
        LIMIT ? OFFSET ?
    """

    SELECT_BY_ID = """
        SELECT * FROM diaries WHERE id = ?
    """

    SELECT_BY_ID_WITH_USER_ID = """
        SELECT * FROM diaries WHERE id = ? AND user_id = ? 
    """

    SELECT_LATEST_USER_DIARY = """
        SELECT * FROM diaries WHERE user_id = ? ORDER BY id DESC LIMIT 1
    """

    SELECT_IMAGES_BY_ID = """
        SELECT images FROM diaries WHERE id = ?
    """

    UPDATE_DIARY = """
        UPDATE diaries SET {fields} WHERE id = ? AND user_id = ?
    """

    DELETE_DIARY = """
        DELETE FROM diaries WHERE id = ? AND user_id = ?
    """

    UPDATE_SUBMISSION_STATUS = """
        UPDATE diaries SET is_submitted = ? WHERE id = ? AND user_id = ?
    """

    UPDATE_EMAIL_SENT = """
        UPDATE diaries SET email_sent = ? WHERE id = ?
    """

    UPDATE_DIARY_IMAGE_BY_ID = """
        UPDATE diaries SET images = ? WHERE id = ?
    """
