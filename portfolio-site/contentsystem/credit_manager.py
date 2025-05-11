import sys
import os
import threading
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from database_manager import ContentDatabaseManager
import sqlite3
from typing import Tuple

class CreditManager:
    def __init__(self, db_path="/project/sandbox/user-workspace/instance/credits.db"):
        self.db_path = db_path
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"Database file not found at {self.db_path}")
        self.local = threading.local()

    def _get_connection(self):
        if not hasattr(self.local, 'conn'):
            self.local.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.local.conn.row_factory = sqlite3.Row
            self.local.cursor = self.local.conn.cursor()
        return self.local.conn, self.local.cursor

    def check_credits(self, username: str, feature: str, cost: int) -> Tuple[bool, str]:
        conn, cursor = self._get_connection()
        cursor.execute("""
            SELECT credits FROM user_credits WHERE username = ?
        """, (username,))
        row = cursor.fetchone()
        if not row:
            return False, "User not found"
        credits = row["credits"]
        if credits < cost:
            return False, "Insufficient credits"
        return True, ""

    def deduct_credits(self, username: str, feature: str, cost: int) -> None:
        conn, cursor = self._get_connection()
        cursor.execute("""
            UPDATE user_credits
            SET credits = credits - ?, last_updated = CURRENT_TIMESTAMP
            WHERE username = ? AND credits >= ?
        """, (cost, username, cost))
        conn.commit()

    def get_credits(self, username: str) -> int:
        conn, cursor = self._get_connection()
        cursor.execute("""
            SELECT credits FROM user_credits WHERE username = ?
        """, (username,))
        row = cursor.fetchone()
        if row:
            return row["credits"]
        return 0

    def close(self):
        if hasattr(self.local, 'conn'):
            self.local.conn.close()
