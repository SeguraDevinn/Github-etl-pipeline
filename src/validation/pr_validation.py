from typing import List, Dict
from utils.logger import get_logger

logger = get_logger(__name__)

def validate_pr_records(pr_records: List[Dict]) -> List[Dict]:
    """
    Validate PR records before loading into warehouse.
    Returns only valid records.
    """

    valid_records = []

    for pr in pr_records:
        # Rule: Pr number must exist
        if pr.get("pr_number") is None:
            logger.error("Validation failed: Missing pr_number.")
            continue

        # Rule: Must have created and updated, with a created > updated
        created = pr.get("created_at")
        updated = pr.get("updated_at")

        if created and updated and created > updated:
            logger.error(
                "Validation failed: created_at > updated_at for PR #%s",
                pr.get("pr_number")
            )
            continue

        #Rule: Must have additions or deletions greater than 0
        additions = pr.get("additions") or 0
        deletions = pr.get("deletions") or 0

        if additions < 0 or deletions < 0:
            logger.error(
                "Validation failed: negative code changes for PR #%s",
                pr.get("pr_number")
            )
            continue
        
        valid_records.append(pr)

    logger.info(
        "Validation complete: %s valid / %s total",
        len(valid_records),
        len(pr_records)
    )

    return valid_records