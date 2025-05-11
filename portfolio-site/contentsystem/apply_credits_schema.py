import os
import sqlite3

def apply_schema(db_path="/project/sandbox/user-workspace/instance/credits.db", schema_file="credits_schema.sql"):
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database file not found at {db_path}")
    schema_path = os.path.join(os.path.dirname(__file__), schema_file)
    if not os.path.exists(schema_path):
        raise FileNotFoundError(f"Schema file not found at {schema_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    with open(schema_path, "r") as f:
        schema_sql = f.read()
    cursor.executescript(schema_sql)
    conn.commit()
    conn.close()
    print("Credits schema applied successfully.")

if __name__ == "__main__":
    apply_schema()