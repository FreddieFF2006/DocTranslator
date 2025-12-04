"""
Migration script to add total_storage column to customer table
Run this once to update the database schema
"""
import sqlite3
import os

db_path = 'db/dev.db'

if os.path.exists(db_path):
    print(f"Connecting to database: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Check if column already exists
        cursor.execute("PRAGMA table_info(customer)")
        columns = [row[1] for row in cursor.fetchall()]

        if 'total_storage' not in columns:
            print("Adding total_storage column...")
            cursor.execute("""
                ALTER TABLE customer
                ADD COLUMN total_storage BIGINT DEFAULT 104857600
            """)
            conn.commit()
            print("✅ Successfully added total_storage column with default 100MB")
        else:
            print("ℹ️  total_storage column already exists")

    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
    finally:
        conn.close()
else:
    print(f"❌ Database file not found: {db_path}")
    print("The database will be created automatically when you start the app.")
