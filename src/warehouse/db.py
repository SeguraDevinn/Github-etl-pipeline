import sqlite3
from pathlib import Path

from utils.logger import get_logger
from warehouse.schema import PR_TABLE_SQL

logger = get_logger(__name__)

DB_PATH = Path("github_warehouse.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

def initialize_database():
    logger.info("Initializing datebase...")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(PR_TABLE_SQL)

    conn.commit()
    conn.close()

    logger.info("Database initialized.")