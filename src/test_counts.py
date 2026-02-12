from warehouse.db import get_connection

def check_counts():
    conn = get_connection()
    cursor = conn.cursor()

    # Total row count
    cursor.execute("SELECT COUNT(*) FROM pull_requests;")
    total = cursor.fetchone()[0]

    print(f"\nTotal rows in pull_requests: {total}")

    # Check for duplicates
    cursor.execute("""
        SELECT pr_number, COUNT(*)
        FROM pull_requests
        GROUP BY pr_number
        HAVING COUNT(*) > 1;
    """)
    duplicates = cursor.fetchall()

    if duplicates:
        print("\n❌ Duplicate PRs found:")
        for row in duplicates:
            print(f"PR #{row[0]} appears {row[1]} times")
    else:
        print("\n✅ No duplicate PRs found")

    conn.close()

if __name__ == "__main__":
    check_counts()
