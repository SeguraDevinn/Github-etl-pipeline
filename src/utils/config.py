import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """
    Centralized configuration for the pipeline.
    """
    GITHUB_API_BASE_URL = "https://api.github.com"
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    REPO_OWNER = "apache"
    REPO_NAME = "airflow"
    PER_PAGE = 100
