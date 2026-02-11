from extract.github_client import fetch_issues
from transform.pr_transformer import transform_prs, enrich_pr_records

def main():
    print("Fetching issues from GitHub...")
    raw_records = fetch_issues(max_pages=3)

    print(f"Raw records fetched: {len(raw_records)}")

    print("Transforming PRs...")
    prs = transform_prs(raw_records)
    print(f"PRs identified: {len(prs)}")

    print("Enriching PRs...")
    enriched_prs = enrich_pr_records(prs, max_enrich=5)
    print(f"PRs enriched: {len(enriched_prs)}")

    # Quick sanity sample
    if enriched_prs:
        sample = enriched_prs[0]
        print("\nSample enriched PR:")
        for k in sorted(sample.keys()):
            print(f"{k}: {sample[k]}")

if __name__ == "__main__":
    main()
