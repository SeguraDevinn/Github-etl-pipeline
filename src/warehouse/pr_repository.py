from typing import List, Dict
from warehouse.db import get_connection
from utils.logger import get_logger

logger = get_logger(__name__)

INSERT_PR_SQL = """
INSERT INTO pull_requests (
    pr_number,
    pr_id,
    pr_node_id,
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
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
ON CONFLICT(pr_number) DO UPDATE SET
    pr_id=excluded.pr_id,
    pr_node_id=excluded.pr_node_id,
    title=excluded.title,
    author_login=excluded.author_login,
    author_type=excluded.author_type,
    state=excluded.state,
    created_at=excluded.created_at,
    updated_at=excluded.updated_at,
    closed_at=excluded.closed_at,
    merged=excluded.merged,
    merged_at=excluded.merged_at,
    additions=excluded.additions,
    deletions=excluded.deletions,
    changed_files=excluded.changed_files,
    review_comments=excluded.review_comments,
    base_branch=excluded.base_branch,
    head_branch=excluded.head_branch,
    num_comments=excluded.num_comments,
    num_labels=excluded.num_labels,
    repo=excluded.repo,
    ingested_at=excluded.ingested_at,
    enriched_at=excluded.enriched_at;
"""


def insert_pull_requests(pr_records : List[Dict]):
    logger.info("Inserting %s PR records into warehouse...", len(pr_records))

    conn = get_connection()
    cursor = conn.cursor()

    for pr in pr_records:
        cursor.execute(
            INSERT_PR_SQL,
            (
                pr.get("pr_number"),
                pr.get("pr_id"),
                pr.get("pr_node_id"),
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

def get_latest_updated_timestamp() -> str | None:
    """
    Returns the most recent updated_at timestamp from warehouse.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT MAX(updated_at) FROM pull_requests;")

    result = cursor.fetchone()[0]

    conn.close()

    return result
