"""
Create a test user directly in the database without email verification
"""
import sqlite3
import os
from werkzeug.security import generate_password_hash
from datetime import datetime

db_path = 'db/dev.db'

if os.path.exists(db_path):
    print(f"Connecting to database: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # User details
        email = 'test@example.com'
        password = 'password123'
        name = 'Test User'

        # Check if user already exists
        cursor.execute("SELECT id FROM customer WHERE email = ?", (email,))
        if cursor.fetchone():
            print(f"⚠️  User {email} already exists!")
        else:
            # Generate password hash
            password_hash = generate_password_hash(password)

            # Insert user
            cursor.execute("""
                INSERT INTO customer
                (customer_no, phone, name, password, email, level, status, deleted_flag,
                 created_at, storage, total_storage)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                f'USER{datetime.now().strftime("%Y%m%d%H%M%S")}',  # customer_no
                None,  # phone
                name,
                password_hash,
                email,
                'common',  # level
                'enabled',  # status
                'N',  # deleted_flag
                datetime.now(),  # created_at
                0,  # storage
                104857600  # total_storage (100MB)
            ))

            conn.commit()
            print(f"✅ User created successfully!")
            print(f"   Email: {email}")
            print(f"   Password: {password}")
            print(f"   You can now log in at http://localhost:1475")

    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
    finally:
        conn.close()
else:
    print(f"❌ Database file not found: {db_path}")
