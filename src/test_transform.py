from extract.github_client import fetch_issues
from transform.pr_transformer import transform_prs

def main():
    print("fetching issues from Github...")
    raw_records = fetch_issues()

    print(f"Total raw records fetched: {len(raw_records)}")

    print("Transforming PRs...")
    prs = transform_prs(raw_records)

    print(f"Total PRs identified: {len(prs)}")

    if prs:
        print("\nSample transformed PR:")
        for key, value in prs[0].items():
            print(f"{key}: {value}")

if __name__ == '__main__':
    main()