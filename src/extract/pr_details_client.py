import requests
from typing import Dict

from utils.config import Config
from utils.logger import get_logger
from extract.github_client import _get_headers

logger = get_logger(__name__)

def fetch_pr_details(pr_number: int) -> Dict:
    """
    Fetch detailed pull request data for a single PR.
    """
    url = (
        f"{Config.GITHUB_API_BASE_URL}/repos/"
        f"{Config.REPO_OWNER}/{Config.REPO_NAME}/pulls/{pr_number}"
    )

    logger.info("Fetching PR details for PR #%s", pr_number)

    response = requests.get(
        url,
        headers = _get_headers(),
        timeout=30
    )

    if response.status_code != 200:
        logger.error(
            "Failed to fetch PR#%s (Status %s): %s",
            pr_number,
            response.status_code,
            response.text
        )
        response.raise_for_status()


    return response.json()