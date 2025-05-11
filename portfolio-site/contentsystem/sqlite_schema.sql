-- SQLite schema for content system integration

CREATE TABLE IF NOT EXISTS viral_content (
    content_id TEXT PRIMARY KEY,
    content_data TEXT -- JSON serialized content data
);

CREATE TABLE IF NOT EXISTS hashtags (
    platform TEXT PRIMARY KEY,
    hashtags TEXT -- JSON serialized list of hashtags
);

CREATE TABLE IF NOT EXISTS scripts (
    content_id TEXT,
    script_type TEXT,
    script_data TEXT, -- JSON serialized script data
    PRIMARY KEY (content_id, script_type),
    FOREIGN KEY (content_id) REFERENCES viral_content(content_id)
);

CREATE TABLE IF NOT EXISTS metadata (
    content_id TEXT,
    platform TEXT,
    metadata TEXT, -- JSON serialized metadata
    PRIMARY KEY (content_id, platform),
    FOREIGN KEY (content_id) REFERENCES viral_content(content_id)
);

CREATE TABLE IF NOT EXISTS viral_techniques (
    content_id TEXT,
    technique_id INTEGER PRIMARY KEY AUTOINCREMENT,
    technique_data TEXT, -- JSON serialized technique data
    FOREIGN KEY (content_id) REFERENCES viral_content(content_id)
);