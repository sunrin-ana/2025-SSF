class RoomQueries:
    """마이 룸 관련 쿼리"""

    CREATE_TABLE = """
    CREATE TABLE IF NOT EXISTS rooms (
        id INTEGER PRIMARY KEY,
        user_id INTEGER UNIQUE,
        room_name TEXT,
        room_type TEXT
    )
    """
    CREATE_TABLE_ROOM_FURNITURE = """
        CREATE TABLE IF NOT EXISTS room_furnitures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_id INTEGER NOT NULL,
            furniture_name TEXT NOT NULL,
            x INTEGER NOT NULL,
            y INTEGER NOT NULL,
            FOREIGN KEY (room_id) REFERENCES rooms(id) ON DELETE CASCADE
        )
    """

    CREATE_TABLE_USER_FURNITURE = """
        CREATE TABLE IF NOT EXISTS user_furnitures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            furniture_name TEXT NOT NULL
        )
    """

    INSERT_USER_FURNITURE = """
        INSERT INTO user_furnitures (user_id, furniture_name) VALUES (?, ?)
    """

    INSERT_ROOM = """
        INSERT INTO rooms (user_id, room_name, room_type) VALUES (?, ?, ?)
    """

    INSERT_ROOM_FURNITURE = """
        INSERT INTO room_furnitures (room_id, furniture_name, x, y) VALUES (?, ?, ?, ?)
    """

    SELECT_ROOM_ID_BY_USER_ID = """
        SELECT id FROM rooms WHERE user_id = ?
    """

    SELECT_ROOM_BY_ID = """
        SELECT * FROM rooms WHERE id = ?
    """

    SELECT_FURNITURE = """
        SELECT * FROM furnitures
    """

    SELECT_ROOM_FURNITURE = """
        SELECT id, furniture_name, x, y FROM room_furnitures WHERE room_id = ?
    """

    SELECT_FURNITURE_ID_BY_X_Y = """
        SELECT id FROM room_furnitures WHERE room_id = ? AND x = ? AND y = ?
    """

    SELECT_USER_FURNITURE = """
        SELECT * FROM user_furnitures WHERE user_id = ?
    """

    UPDATE_ROOM_NAME = """
        UPDATE rooms SET room_name = ? WHERE id = ?
    """

    UPDATE_ROOM_TYPE = """
        UPDATE rooms SET room_type = ? WHERE id = ?
    """

    DELETE_FURNITURE = """
        DELETE FROM room_furnitures WHERE room_id = ? AND x = ? AND y = ?
    """

    SELECT_ROOM_BY_USER_ID = """
        SELECT * FROM rooms WHERE user_id = ?
    """
