class PhotoQueries:
    CREATE_TABLE = """
        CREATE TABLE IF NOT EXISTS photos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            album_name TEXT NOT NULL,
            image_path TEXT NOT NULL,
            title TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    """

    CREATE_COMMENTS_TABLE = """
        CREATE TABLE IF NOT EXISTS photo_comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            photo_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (photo_id) REFERENCES photos (id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    """

    INSERT_PHOTO = """
        INSERT INTO photos (user_id, album_name, image_path, title, created_at)
        VALUES (?, ?, ?, ?, ?)
    """

    SELECT_USER_PHOTOS = """
        SELECT * FROM photos 
        WHERE user_id = ?
        ORDER BY created_at DESC 
        LIMIT ? OFFSET ?
    """

    SELECT_USER_PHOTOS_BY_ALBUM = """
        SELECT * FROM photos 
        WHERE user_id = ? AND album_name = ?
        ORDER BY created_at DESC 
        LIMIT ? OFFSET ?
    """

    SELECT_LATEST_USER_PHOTO = """
        SELECT * FROM photos WHERE user_id = ? ORDER BY id DESC LIMIT 1
    """

    SELECT_PHOTO_OWNER = """
        SELECT user_id FROM photos WHERE id = ?
    """

    SELECT_PHOTO_ALBUM_NAME = """
        SELECT album_name FROM photos WHERE id = ? AND user_id = ?
    """

    INSERT_COMMENT = """
        INSERT INTO photo_comments (photo_id, user_id, content, created_at)
        VALUES (?, ?, ?, ?)
    """

    SELECT_LATEST_COMMENT = """
        SELECT * FROM photo_comments WHERE photo_id = ? AND user_id = ? ORDER BY id DESC LIMIT 1
    """

    SELECT_PHOTO_COMMENTS = """
        SELECT pc.*, u.username 
        FROM photo_comments pc
        JOIN users u ON pc.user_id = u.id
        WHERE pc.photo_id = ?
        ORDER BY pc.created_at ASC
    """

    SELECT_PHOTO_BY_ID = """
        SELECT * FROM photos WHERE id = ? AND user_id = ?
    """

    DELETE_PHOTO = """
        DELETE FROM photos WHERE id = ? AND user_id = ?
    """

    UPDATE_PHOTO_PATH = """
        UPDATE photos SET image_path = ? WHERE id = ? AND user_id = ?
    """


class LetterQueries:
    CREATE_TABLE = """
        CREATE TABLE IF NOT EXISTS letters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            FOREIGN KEY (sender_id) REFERENCES users (id) ON DELETE CASCADE
        )
    """

    INSERT_LETTER = """
        INSERT INTO letters (sender_id, content)
        VALUES (?, ?)
    """

    SELECT_USER_LETTERS = """
        SELECT * FROM letters 
        WHERE sender_id = ?
    """

    SELECT_LATEST_USER_LETTER = """
        SELECT * FROM letters WHERE sender_id = ? LIMIT 1
    """

    SELECT_LETTER_BY_ID = """
        SELECT * FROM letters WHERE id = ? AND sender_id = ?
    """

    SELECT_LETTER_FOR_DELIVERY = """
        SELECT * FROM letters WHERE id = ?
    """

    SELECT_SENDER_USERNAME = """
        SELECT username FROM users WHERE id = ?
    """

    UPDATE_LETTER = """
        UPDATE letters SET content = ? WHERE id = ? AND sender_id = ?
    """

    DELETE_LETTER = """
        DELETE FROM letters WHERE id = ? AND sender_id = ?
    """


class DatabaseIndexes:
    USER_INDEXES = [
        "CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)",
        "CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)",
    ]

    DIARY_INDEXES = [
        "CREATE INDEX IF NOT EXISTS idx_diaries_user_id ON diaries(user_id)",
        "CREATE INDEX IF NOT EXISTS idx_diaries_category ON diaries(category)",
        "CREATE INDEX IF NOT EXISTS idx_diaries_created_at ON diaries(created_at)",
    ]

    PHOTO_INDEXES = [
        "CREATE INDEX IF NOT EXISTS idx_photos_user_id ON photos(user_id)",
        "CREATE INDEX IF NOT EXISTS idx_photos_album ON photos(album_name)",
        "CREATE INDEX IF NOT EXISTS idx_photo_comments_photo_id ON photo_comments(photo_id)",
    ]

    FRIENDSHIP_INDEXES = [
        "CREATE INDEX IF NOT EXISTS idx_friendships_user_id ON friendships(user_id)",
        "CREATE INDEX IF NOT EXISTS idx_friendships_friend_id ON friendships(friend_id)",
        "CREATE INDEX IF NOT EXISTS idx_friendships_status ON friendships(status)",
    ]

    LETTER_INDEXES = [
        "CREATE INDEX IF NOT EXISTS idx_letters_sender_id ON letters(sender_id)",
        "CREATE INDEX IF NOT EXISTS idx_letters_sent_date ON letters(sent_date)",
    ]

    AVATAR_INDEXES = [
        "CREATE INDEX IF NOT EXISTS idx_avatars_user_id ON avatars(user_id)",
    ]

    GUEST_BOOK_INDEXES = [
        "CREATE INDEX IF NOT EXISTS idx_guest_books_user_id ON guest_books(user_id)",
        "CREATE INDEX IF NOT EXISTS idx_guest_books_created_at ON guest_books(created_at)",
    ]
