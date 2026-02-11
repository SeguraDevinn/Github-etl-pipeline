from extract.github_client import fetch_issues
from transform.pr_transformer import transform_prs, enrich_pr_records
from warehouse.db import initialize_database
from warehouse.pr_repository import insert_pull_requests, get_latest_updated_timestamp
from validation.pr_validation import validate_pr_records

def main():
    initialize_database()

    latest_ts = get_latest_updated_timestamp()

    print(f"Latest warehouse timestamp: {latest_ts}")

    raw = fetch_issues(max_pages=2, since=latest_ts)
    prs = transform_prs(raw)
    enriched = enrich_pr_records(prs, max_enrich=5)

    validated = validate_pr_records(enriched)

    insert_pull_requests(validated)

    print("Warehouse test complete.")

if __name__ == '__main__' :
    main()