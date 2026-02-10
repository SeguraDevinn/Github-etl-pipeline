from extract.pr_details_client import fetch_pr_details

if __name__ == "__main__":
    pr = fetch_pr_details(61740)

    print("Merged:", pr.get("merged"))
    print("Additions:", pr.get("additions"))
    print("Deletions:", pr.get("deletions"))
    print("Changed files:", pr.get("changed_files"))
