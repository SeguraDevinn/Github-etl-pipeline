import time
from datetime import datetime, timezone

from extract.github_client import fetch_issues
from transform.pr_transformer import transform_prs, enrich_pr_records
from warehouse.db import initialize_database
from warehouse.pr_repository import insert_pull_requests, get_latest_updated_timestamp
from validation.pr_validation import validate_pr_records

def main():
    start_time = time.time()
    run_timestamp = datetime.now(timezone.utc).isoformat() + "Z"

    print("\n==============================")
    print("Starting GitHub ETL Pipeline")
    print("==============================")
    print(f"Run timestamp: {run_timestamp}")

    # Init database
    initialize_database()

    # Get watermark
    latest_ts = get_latest_updated_timestamp()
    print(f"Watermark used: {latest_ts}")

    # Extraction
    raw_issues = fetch_issues(since=latest_ts)
    issues_fetched = len(raw_issues)

    # Transform
    prs = transform_prs(raw_issues)
    prs_transformed = len(prs)

    # Enrich
    enriched = enrich_pr_records(prs)
    prs_enriched = len(enriched)

    # Validate
    validated = validate_pr_records(enriched)
    prs_validated = len(validated)

    # Load
    insert_pull_requests(validated)

    end_time = time.time()
    duration = round(end_time - start_time, 2)

    # Run Summary
    print("\nRun Summary")
    print("------------------------------")
    print(f"Issues fetched:     {issues_fetched}")
    print(f"PRs transformed:    {prs_transformed}")
    print(f"PRs enriched:       {prs_enriched}")
    print(f"PRs validated:      {prs_validated}")
    print(f"Duration (seconds): {duration}")
    print("==============================\n")

if __name__ == '__main__' :
    main()