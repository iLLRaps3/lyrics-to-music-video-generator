-- Extend the existing user_credits table or create a new table to track credits usage per feature

CREATE TABLE IF NOT EXISTS feature_credits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    feature_name TEXT NOT NULL,
    credits_used INTEGER NOT NULL DEFAULT 0,
    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user_credits(id)
);

-- Optionally, add indexes for performance
CREATE INDEX IF NOT EXISTS idx_feature_credits_user_feature ON feature_credits(user_id, feature_name);