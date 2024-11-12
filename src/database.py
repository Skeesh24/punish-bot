import sqlite3
from os import getenv
from pathlib import Path

IDS_TO_LIMIT = getenv("IDS_TO_LIMIT").split(",")
WORDS_LIMIT = getenv("WORDS_LIMIT")
DATABASE_PATH = Path(__file__).parent / "data" / "database.db"

if not DATABASE_PATH.exists():
    DATABASE_PATH.mkdir()


def execute(sql: str, params: tuple | None = None) -> sqlite3.Cursor:
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(
        sql,
        params if params else (),
    )
    conn.commit()
    # conn.close()
    return cursor


def init_db():
    execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            words INTEGER
        );
        """
    )


def init_user(user_id: int | str, words: int | str) -> None:
    execute(
        """
        INSERT OR REPLACE INTO users (id, words) VALUES (
            ?, ?
        );
        """,
        (int(user_id), int(words)),
    )


def get_user_words_count(user_id: int | str) -> int:
    cursor = execute("SELECT words FROM users WHERE id = ?", (int(user_id),))
    result = cursor.fetchone()
    return result[0] if result else 0


def update_user_words_count(user_id: int | str, words: int | str = WORDS_LIMIT) -> None:
    execute(
        "INSERT OR REPLACE INTO users (id, words) VALUES (?, ?)",
        (int(user_id), int(words)),
    )


init_db()

for id_to_init in IDS_TO_LIMIT:
    init_user(id_to_init, WORDS_LIMIT)
