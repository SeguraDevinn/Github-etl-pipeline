from extract.github_client import fetch_issues
from transform.pr_transformer import transform_prs, enrich_pr_records
from warehouse.db import initialize_database
from warehouse.pr_repository import insert_pull_requests

def main():
    initialize_database()


    raw = fetch_issues(max_pages=2)
    prs = transform_prs(raw)
    enriched = enrich_pr_records(prs, max_enrich=5)

    insert_pull_requests(enriched)

    print("Warehouse test complete.")

if __name__ == '__main__' :
    main()