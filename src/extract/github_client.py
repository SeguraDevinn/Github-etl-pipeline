import requests
from typing import List, Dict

from utils.config import Config
from utils.logger import get_logger

logger = get_logger(__name__)


# -------------------------
# Enable Auth Headers
# -------------------------

def _get_headers() -> Dict[str, str]:
    """
    Build headers for GitHub API requests.
    """
    if not Config.GITHUB_TOKEN:
        raise ValueError("GITHUB_TOKEN is not set in environment variables")

    return {
        "Authorization": f"Bearer {Config.GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }


# -------------------------
# API Call
# -------------------------

def fetch_issues(state: str = "all") -> List[Dict]:
    """
    Fetch all issues for a GitHub repository using pagination.

    Args:
        state: Issue state to fetch (open, closed, all)

    Returns:
        List of raw issue JSON objects
    """

    logger.info(
        "Starting issue fetch for %s/%s",
        Config.REPO_OWNER,
        Config.REPO_NAME
    )

    issues: List[Dict] = []
    page = 1

    url = f"{Config.GITHUB_API_BASE_URL}/repos/{Config.REPO_OWNER}/{Config.REPO_NAME}/issues"

    while True:
        logger.info("Fetching page %s", page)

        response = requests.get(
            url,
            headers= _get_headers(),
            params={
                "state": state,
                "per_page": Config.PER_PAGE,
                "page": page
            },
            timeout=30
        )

        if response.status_code != 200:
            logger.error(
                "Github API request failed (status %s): %s",
                response.status_code,
                response.text
            )
            response.raise_for_status()

        page_data = response.json()

        if not page_data:
            logger.info("No more data returned. Pagination complete.")
            break

        issues.extend(page_data)
        page += 1

    logger.info("Fetched %s total issues.", len(issues))

    return issues