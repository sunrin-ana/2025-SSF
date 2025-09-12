class GuestBookQueries:
    CREATE_TABLE = """
        CREATE TABLE IF NOT EXISTS guest_books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            target_user_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    """

    INSERT_GUEST_BOOK = """
        INSERT INTO guest_books (target_user_id, user_id, content, created_at)
        VALUES (?, ?, ?, ?)
    """

    SELECT_TARGET_USER_GUEST_BOOKS = """
        SELECT * FROM guest_books 
        WHERE target_user_id = ?
        ORDER BY created_at DESC 
        LIMIT ? OFFSET ?
    """

    SELECT_GUEST_BOOK_BY_ID = """
        SELECT * FROM guest_books WHERE id = ?
    """

    SELECT_GUEST_BOOK_BY_USER_ID = """
        SELECT * FROM guest_books WHERE user_id = ? ORDER BY created_at DESC LIMIT 1
    """

    UPDATE_GUEST_BOOK_BY_ID = """
        UPDATE guest_books SET content = ?, updated_at=CURRENT_TIMESTAMP WHERE id = ?
    """

    DELETE_GUEST_BOOK = """
        DELETE FROM guest_books WHERE id = ? AND user_id = ?
    """
