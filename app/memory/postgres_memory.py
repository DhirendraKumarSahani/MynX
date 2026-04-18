
import psycopg2
print("Working ✅")
import os
from dotenv import load_dotenv

load_dotenv()


class PostgresMemory:

    def __init__(self):
        self.conn = psycopg2.connect(
            os.getenv("DATABASE_URL")
        )
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS chat_memory (
            id SERIAL PRIMARY KEY,
            thread_id TEXT,
            role TEXT,
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        with self.conn.cursor() as cur:
            cur.execute(query)
            self.conn.commit()

    def save_message(self, thread_id, role, content):
        query = """
        INSERT INTO chat_memory (thread_id, role, content)
        VALUES (%s, %s, %s)
        """
        with self.conn.cursor() as cur:
            cur.execute(query, (thread_id, role, content))
            self.conn.commit()

    def get_messages(self, thread_id, limit=6):
        query = """
        SELECT role, content FROM chat_memory
        WHERE thread_id = %s
        ORDER BY id DESC
        LIMIT %s
        """
        with self.conn.cursor() as cur:
            cur.execute(query, (thread_id, limit))
            rows = cur.fetchall()

        return rows[::-1]  # oldest → latest