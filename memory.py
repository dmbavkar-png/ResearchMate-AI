import sqlite3


class Memory:

    def __init__(self, db_path="memory.db"):
        self.db_path = db_path
        self.initialize_database()

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def initialize_database(self):
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        conn.close()

    def save_message(self, role, content):
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO messages (role, content)
            VALUES (?, ?)
            """,
            (role, content)
        )

        conn.commit()
        conn.close()

    def get_context(self, limit=10):
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT role, content
            FROM messages
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,)
        )

        rows = cursor.fetchall()
        conn.close()

        # Reverse so conversation appears oldest -> newest
        rows.reverse()

        context = ""

        for role, content in rows:
            context += f"{role}: {content}\n"

        return context