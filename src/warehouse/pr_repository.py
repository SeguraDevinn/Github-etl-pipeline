from typing import List, Dict
from warehouse.db import get_connection
from utils.logger import get_logger

logger = get_logger(__name__)

INSERT_PR_SQL = """
INSERT OR REPLACE INTO pull_requests (
    pr_id,
    pr_node_id,
    pr_number,
    title,
    author_login,
    author_type,
    state,
    created_at,
    updated_at,
    closed_at,
    merged,
    merged_at,
    additions,
    deletions,
    changed_files,
    review_comments,
    base_branch,
    head_branch,
    num_comments,
    num_labels,
    repo,
    ingested_at,
    enriched_at
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
"""

def insert_pull_requests(pr_records : List[Dict]):
    logger.info("Inserting %s PR records into warehouse...", len(pr_records))

    conn = get_connection()
    cursor = conn.cursor()

    for pr in pr_records:
        cursor.execute(
            INSERT_PR_SQL,
            (
                pr.get("pr_id"),
                pr.get("pr_node_id"),
                pr.get("pr_number"),
                pr.get("title"),
                pr.get("author_login"),
                pr.get("author_type"),
                pr.get("state"),
                pr.get("created_at"),
                pr.get("updated_at"),
                pr.get("closed_at"),
                pr.get("merged"),
                pr.get("merged_at"),
                pr.get("additions"),
                pr.get("deletions"),
                pr.get("changed_files"),
                pr.get("review_comments"),
                pr.get("base_branch"),
                pr.get("head_branch"),
                pr.get("num_comments"),
                pr.get("num_labels"),
                pr.get("repo"),
                pr.get("ingested_at"),
                pr.get("enriched_at"),

            )
        )

    conn.commit()
    conn.close()

    logger.info("Insert complete.")