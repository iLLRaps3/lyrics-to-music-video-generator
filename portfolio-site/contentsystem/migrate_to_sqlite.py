import json
import sqlite3
from tinydb import TinyDB

TINYDB_PATH = "content_assistant_data.json"
SQLITE_DB_PATH = "../instance/credits.db"  # Adjust path as needed

def migrate():
    # Connect to TinyDB
    tinydb = TinyDB(TINYDB_PATH)
    content_table = tinydb.table("viral_content")
    hashtags_table = tinydb.table("hashtags")

    # Connect to SQLite
    conn = sqlite3.connect(SQLITE_DB_PATH)
    cursor = conn.cursor()

    # Create tables if not exist
    with open("sqlite_schema.sql", "r") as f:
        cursor.executescript(f.read())

    # Migrate viral_content
    for item in content_table.all():
        content_id = item.get("content_id")
        content_data = json.dumps(item)
        cursor.execute("""
            INSERT OR REPLACE INTO viral_content (content_id, content_data)
            VALUES (?, ?)
        """, (content_id, content_data))

        # Migrate scripts if present
        scripts = item.get("scripts", {})
        for script_type, script_data in scripts.items():
            cursor.execute("""
                INSERT OR REPLACE INTO scripts (content_id, script_type, script_data)
                VALUES (?, ?, ?)
            """, (content_id, script_type, json.dumps(script_data)))

        # Migrate metadata if present
        metadata = item.get("metadata", {})
        for platform, meta_data in metadata.items():
            cursor.execute("""
                INSERT OR REPLACE INTO metadata (content_id, platform, metadata)
                VALUES (?, ?, ?)
            """, (content_id, platform, json.dumps(meta_data)))

        # Migrate viral_techniques if present
        techniques = item.get("viral_techniques", [])
        for technique in techniques:
            cursor.execute("""
                INSERT INTO viral_techniques (content_id, technique_data)
                VALUES (?, ?)
            """, (content_id, json.dumps(technique)))

    # Migrate hashtags
    for item in hashtags_table.all():
        platform = item.get("platform")
        hashtags = json.dumps(item.get("hashtags", []))
        cursor.execute("""
            INSERT OR REPLACE INTO hashtags (platform, hashtags)
            VALUES (?, ?)
        """, (platform, hashtags))

    conn.commit()
    conn.close()
    print("Migration from TinyDB to SQLite completed.")

if __name__ == "__main__":
    migrate()