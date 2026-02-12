from typing import List, Dict
from datetime import datetime, timezone
from utils.logger import get_logger
from utils.config import Config
from extract.pr_details_client import fetch_pr_details


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
            "pr_number": record.get("number"),
            "pr_id": record.get("id"),
            "pr_node_id": record.get("node_id"),
            "pr_api_url": record.get("pull_request", {}).get("url"),
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
            "pr_url": record.get("pull_request", {}).get("html_url"),
            "repo": f"{Config.REPO_OWNER}/{Config.REPO_NAME}",
            "ingested_at": ingested_at,
            "is_pull_request": True,
            "is_issue": False
        }

        transformed.append(pr)
    
    logger.info("Transformed %s pull records", len(transformed))
    return transformed

def enrich_pr_records(pr_records: List[Dict], max_enrich: int | None = None) -> List[Dict]:
    """
    Enrich PR records with detailed pull request metadata.
    """

    enriched = []

    for i, pr in enumerate(pr_records):

        if max_enrich is not None and i >= max_enrich:
            logger.info("Temporary enrichment limit reached (%s PRs)", max_enrich)
            break


        pr_number = pr["pr_number"]

        try:
            details = fetch_pr_details(pr_number)
        except Exception as e:
            logger.error(
                "Failed to enrich PR #%s: %s",
                pr_number,
                e
            )
            
            pr["enrichment_failed"] = True
            pr["enrichment_at"] = datetime.now(timezone.utc).isoformat()
            enriched.append(pr)
            continue

        pr.update({
            "merged": details.get("merged"),
            "merged_at": details.get("merged_at"),
            "additions": details.get("additions"),
            "deletions": details.get("deletions"),
            "changed_files": details.get("changed_files"),
            "review_comments": details.get("review_comments"),
            "base_branch": details.get("base", {}).get("ref"),
            "head_branch": details.get("head", {}).get("ref"),
            "enriched_at": datetime.now(timezone.utc).isoformat()
        })

        enriched.append(pr)

    logger.info(
        "Enriched %s PR records",
        len(enriched)
    )

    return enriched