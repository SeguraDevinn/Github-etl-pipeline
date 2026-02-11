import sqlite3

conn = sqlite3.connect("github_warehouse.db")
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM pull_requests;")
count = cursor.fetchone()[0]

print(f"Total rows in pull_requests: {count}")

cursor.execute("SELECT pr_number, title FROM pull_requests LIMIT 5;")
rows = cursor.fetchall()

print("\nSample rows:")
for row in rows:
    print(row)

conn.close()
