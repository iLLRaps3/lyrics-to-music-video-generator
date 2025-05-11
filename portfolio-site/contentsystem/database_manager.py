import sqlite3
import json
from typing import Dict, Optional, List

class ContentDatabaseManager:
    """Manages database operations for viral content creation using SQLite."""

    def __init__(self, db_path: str = "../instance/credits.db"):
        """Initialize SQLite connection and create tables if they don't exist."""
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        """Create tables for content system if they don't exist."""
        self.cursor.executescript("""
        CREATE TABLE IF NOT EXISTS viral_content (
            content_id TEXT PRIMARY KEY,
            content_data TEXT
        );
        CREATE TABLE IF NOT EXISTS hashtags (
            platform TEXT PRIMARY KEY,
            hashtags TEXT
        );
        CREATE TABLE IF NOT EXISTS scripts (
            content_id TEXT,
            script_type TEXT,
            script_data TEXT,
            PRIMARY KEY (content_id, script_type),
            FOREIGN KEY (content_id) REFERENCES viral_content(content_id)
        );
        CREATE TABLE IF NOT EXISTS metadata (
            content_id TEXT,
            platform TEXT,
            metadata TEXT,
            PRIMARY KEY (content_id, platform),
            FOREIGN KEY (content_id) REFERENCES viral_content(content_id)
        );
        CREATE TABLE IF NOT EXISTS viral_techniques (
            content_id TEXT,
            technique_id INTEGER PRIMARY KEY AUTOINCREMENT,
            technique_data TEXT,
            FOREIGN KEY (content_id) REFERENCES viral_content(content_id)
        );
        """)
        self.conn.commit()

    def store_content(self, content_id: str, content_data: Dict) -> str:
        """Store or update viral content data."""
        content_json = json.dumps(content_data)
        self.cursor.execute("""
            INSERT INTO viral_content (content_id, content_data)
            VALUES (?, ?)
            ON CONFLICT(content_id) DO UPDATE SET content_data=excluded.content_data
        """, (content_id, content_json))
        self.conn.commit()
        return f"Content '{content_id}' has been stored or updated."

    def store_hashtags(self, platform: str, hashtags: List[str]) -> str:
        """Store or update platform-specific hashtags."""
        hashtags_json = json.dumps(hashtags)
        self.cursor.execute("""
            INSERT INTO hashtags (platform, hashtags)
            VALUES (?, ?)
            ON CONFLICT(platform) DO UPDATE SET hashtags=excluded.hashtags
        """, (platform, hashtags_json))
        self.conn.commit()
        return f"Hashtags for {platform} have been stored or updated."

    def get_content(self, content_id: str) -> Optional[Dict]:
        """Retrieve content data by content_id."""
        self.cursor.execute("SELECT content_data FROM viral_content WHERE content_id = ?", (content_id,))
        row = self.cursor.fetchone()
        if row:
            return json.loads(row["content_data"])
        return None

    def get_platform_hashtags(self, platform: str) -> Optional[List[str]]:
        """Retrieve hashtags for a platform."""
        self.cursor.execute("SELECT hashtags FROM hashtags WHERE platform = ?", (platform,))
        row = self.cursor.fetchone()
        if row:
            return json.loads(row["hashtags"])
        return None

    def store_script(self, content_id: str, script_type: str, script_data: Dict) -> str:
        """Store or update a script for content."""
        script_json = json.dumps(script_data)
        self.cursor.execute("""
            INSERT INTO scripts (content_id, script_type, script_data)
            VALUES (?, ?, ?)
            ON CONFLICT(content_id, script_type) DO UPDATE SET script_data=excluded.script_data
        """, (content_id, script_type, script_json))
        self.conn.commit()
        return f"{script_type.capitalize()} script for content '{content_id}' has been stored or updated."

    def store_metadata(self, content_id: str, platform: str, metadata: Dict) -> str:
        """Store or update metadata for content on a platform."""
        metadata_json = json.dumps(metadata)
        self.cursor.execute("""
            INSERT INTO metadata (content_id, platform, metadata)
            VALUES (?, ?, ?)
            ON CONFLICT(content_id, platform) DO UPDATE SET metadata=excluded.metadata
        """, (content_id, platform, metadata_json))
        self.conn.commit()
        return f"Metadata for {platform} content '{content_id}' has been stored or updated."

    def get_trending_hashtags(self, platform: str, limit: int = 50) -> List[str]:
        """Get trending hashtags for a platform."""
        hashtags = self.get_platform_hashtags(platform)
        if hashtags:
            return hashtags[:limit]
        return []

    def store_viral_techniques(self, content_id: str, techniques: List[Dict]) -> str:
        """Store or update viral techniques for content."""
        # Delete existing techniques for content_id
        self.cursor.execute("DELETE FROM viral_techniques WHERE content_id = ?", (content_id,))
        # Insert new techniques
        for technique in techniques:
            technique_json = json.dumps(technique)
            self.cursor.execute("""
                INSERT INTO viral_techniques (content_id, technique_data)
                VALUES (?, ?)
            """, (content_id, technique_json))
        self.conn.commit()
        return f"Viral techniques for content '{content_id}' have been stored or updated."

    def list_content(self) -> List[str]:
        """List all content IDs."""
        self.cursor.execute("SELECT content_id FROM viral_content")
        rows = self.cursor.fetchall()
        return [row["content_id"] for row in rows]

    def delete_content(self, content_id: str) -> str:
        """Delete content and related data."""
        self.cursor.execute("DELETE FROM viral_content WHERE content_id = ?", (content_id,))
        self.cursor.execute("DELETE FROM scripts WHERE content_id = ?", (content_id,))
        self.cursor.execute("DELETE FROM metadata WHERE content_id = ?", (content_id,))
        self.cursor.execute("DELETE FROM viral_techniques WHERE content_id = ?", (content_id,))
        self.conn.commit()
        return f"Content '{content_id}' and related data have been deleted."

    def clear_database(self) -> str:
        """Clear all content system data."""
        self.cursor.execute("DELETE FROM viral_content")
        self.cursor.execute("DELETE FROM hashtags")
        self.cursor.execute("DELETE FROM scripts")
        self.cursor.execute("DELETE FROM metadata")
        self.cursor.execute("DELETE FROM viral_techniques")
        self.conn.commit()
        return "Content system database has been cleared."
