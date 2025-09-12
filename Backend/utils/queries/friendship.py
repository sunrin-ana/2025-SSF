class FriendshipQueries:
    """친구 관계 관련 쿼리"""

    CREATE_TABLE = """
        CREATE TABLE IF NOT EXISTS friendships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            friend_id INTEGER NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
            FOREIGN KEY (friend_id) REFERENCES users (id) ON DELETE CASCADE,
            UNIQUE(user_id, friend_id)
        )
    """

    SELECT_USER_BY_USERNAME = """
        SELECT id FROM users WHERE username = ?
    """

    SELECT_EXISTING_FRIENDSHIP = """
        SELECT * FROM friendships 
        WHERE (user_id = ? AND friend_id = ?) OR (user_id = ? AND friend_id = ?)
    """

    INSERT_FRIENDSHIP = """
        INSERT INTO friendships (user_id, friend_id, status, created_at)
        VALUES (?, ?, ?, ?)
    """

    SELECT_FRIENDSHIP_BY_IDS = """
        SELECT * FROM friendships WHERE user_id = ? AND friend_id = ?
    """

    SELECT_FRIENDSHIP_FOR_ACCEPT = """
        SELECT f.*, u.username 
        FROM friendships f
        JOIN users u ON f.user_id = u.id
        WHERE f.id = ? AND f.friend_id = ? AND f.status = ?
    """

    UPDATE_FRIENDSHIP_STATUS = """
        UPDATE friendships SET status = ? WHERE id = ?
    """

    SELECT_USER_FRIENDSHIPS = """
        SELECT f.*, u.username 
        FROM friendships f
        JOIN users u ON (
            CASE 
                WHEN f.user_id = ? THEN f.friend_id = u.id
                ELSE f.user_id = u.id
            END
        )
        WHERE (f.user_id = ? OR f.friend_id = ?) AND f.status = ?
        ORDER BY f.created_at DESC
    """

    SELECT_USER_FRIENDSHIPS_BY_STATUS = """
        SELECT f.*, u.username 
        FROM friendships f
        JOIN users u ON (
            CASE 
                WHEN f.user_id = ? THEN f.friend_id = u.id
                ELSE f.user_id = u.id
            END
        )
        WHERE (f.user_id = ? OR f.friend_id = ?) AND f.status = ?
        ORDER BY f.created_at DESC
    """

    DELETE_FRIENDSHIP = """
        DELETE FROM friendships 
        WHERE id = ? AND (user_id = ? OR friend_id = ?)
    """

    SELECT_PENDING_REQUESTS = """
        SELECT f.*, u.username 
        FROM friendships f
        JOIN users u ON f.user_id = u.id
        WHERE f.friend_id = ? AND f.status = ?
        ORDER BY f.created_at DESC
    """

    CHECK_FRIENDSHIP_STATUS = """
        SELECT * FROM friendships 
        WHERE ((user_id = ? AND friend_id = ?) OR (user_id = ? AND friend_id = ?))
        AND status = 'accepted'
    """
