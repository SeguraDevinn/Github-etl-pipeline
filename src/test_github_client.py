from extract.github_client import fetch_issues
import json

if __name__ == "__main__":
    issues = fetch_issues(state="open")

    print(f"Fetched {len(issues)} issues.")

    if issues:
        print("\n Sample issues keys:")
        print(issues[0].keys())

    print("\n Full sample record: ")
    print(json.dumps(issues[0], indent=2)[:2000])
    print(json.dumps(issues[1], indent=2)[:2000])
    print(json.dumps(issues[2], indent=2)[:2000])