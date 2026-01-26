import sqlite3
import os

DB_NAME = "instamanager.db"

def fix_db():
    if not os.path.exists(DB_NAME):
        print("DB file not found.")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # 1. Ensure a default client exists
    cursor.execute("SELECT id, name FROM clients LIMIT 1")
    client = cursor.fetchone()
    if not client:
        print("No clients found. Creating default client.")
        cursor.execute("INSERT INTO clients (name) VALUES ('Default Client')")
        client_id = cursor.lastrowid
    else:
        client_id = client[0]
        print(f"Using Client ID: {client_id} ({client[1]})")

    # 2. Update schedules: NULL client_id -> current client_id
    cursor.execute("UPDATE schedules SET client_id = ? WHERE client_id IS NULL", (client_id,))
    updated_schedules = cursor.rowcount
    if updated_schedules > 0:
        print(f"Updated {updated_schedules} schedule records with missing client_id.")

    # 3. Update images/texts: NULL client_id -> current client_id (Optional but good)
    cursor.execute("UPDATE images SET client_id = ? WHERE client_id IS NULL", (client_id,))
    cursor.execute("UPDATE texts SET client_id = ? WHERE client_id IS NULL", (client_id,))

    # 4. Sync Stores: Add any store_name found in schedules to stores table
    cursor.execute("SELECT DISTINCT store_name FROM schedules WHERE store_name IS NOT NULL AND store_name != ''")
    distinct_stores = [row[0] for row in cursor.fetchall()]

    added_stores = 0
    for s_name in distinct_stores:
        # Check existence
        cursor.execute("SELECT id FROM stores WHERE client_id = ? AND name = ?", (client_id, s_name))
        if not cursor.fetchone():
            cursor.execute("INSERT INTO stores (client_id, name) VALUES (?, ?)", (client_id, s_name))
            added_stores += 1
            print(f"  -> Added missing store: {s_name}")

    if added_stores > 0:
        print(f"Registered {added_stores} stores from historical schedule data.")
    else:
        print("All stores in schedules are already registered.")

    conn.commit()
    conn.close()
    print("Database fix completed.")

if __name__ == "__main__":
    fix_db()
