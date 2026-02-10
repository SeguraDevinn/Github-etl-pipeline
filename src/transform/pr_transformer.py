from typing import List, Dict
from datetime import datetime, timezone
from utils.logger import get_logger
from utils.config import Config

logger = get_logger(__name__)

def _is_pull_request(record: Dict) -> bool:
    """
    Determine whether a GitHub record represents a Pull Request.
    """
    node_id = record.get("node_id", "")
    return node_id.startswith("PR_")

def transform_prs(raw_records:List[Dict]) -> List[Dict]:
    """
    Transform raw GitHub issue records into normalized pull request records.
    """

    logger.info("Starting pr transformation for %s records", len(raw_records))

    transformed: List[Dict] = []
    ingested_at = datetime.now(timezone.utc).isoformat()

    for record in raw_records:
        if not _is_pull_request(record):
            continue

        pr = {
            "pr_id": record.get("id"),
            "pr_node_id": record.get("node_id"),
            "pr_number": record.get("number"),
            "title": record.get("title"),
            "author_login": record.get("user", {}).get("login"),
            "author_type": record.get("user", {}).get("type"),
            "state": record.get("state"),
            "created_at": record.get("created_at"),
            "updated_at": record.get("updated_at"),
            "closed_at": record.get("closed_at"),
            "num_comments": record.get("comments"),
            "labels": [label.get("name") for label in record.get("labels", [])],
            "num_labels": len(record.get("labels", [])),
            "repo": f"{Config.REPO_OWNER}/{Config.REPO_NAME}",
            "ingested_at": ingested_at
        }

        transformed.append(pr)
    
    logger.info("Transformed %s pull records", len(transformed))
    return transformed