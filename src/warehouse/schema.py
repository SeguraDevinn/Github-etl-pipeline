PR_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS pull_requests (
    pr_number INTEGER PRIMARY KEY,
    pr_id INTEGER,
    pr_node_id TEXT,
    title TEXT,
    author_login TEXT,
    author_type TEXT,
    state TEXT,
    created_at TEXT,
    updated_at TEXT,
    closed_at TEXT,
    merged BOOLEAN,
    merged_at TEXT,
    additions INTEGER,
    deletions INTEGER,
    changed_files INTEGER,
    review_comments INTEGER,
    base_branch TEXT,
    head_branch TEXT,
    num_comments INTEGER,
    num_labels INTEGER,
    repo TEXT,
    ingested_at TEXT,
    enriched_at TEXT
);
"""
