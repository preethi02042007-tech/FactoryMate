
import sqlite3

DB_NAME = "assistant.db"


def connect_db():
    return sqlite3.connect(DB_NAME)


def create_supplier_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS suppliers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            supplier_name TEXT NOT NULL,
            company_name TEXT,
            phone_number TEXT UNIQUE,
            telegram_chat_id INTEGER UNIQUE,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Add Telegram ID column if an older table does not have it
    cursor.execute("PRAGMA table_info(suppliers)")
    columns = [column[1] for column in cursor.fetchall()]

    if "telegram_chat_id" not in columns:
        cursor.execute(
            "ALTER TABLE suppliers ADD COLUMN telegram_chat_id INTEGER"
        )

    conn.commit()
    conn.close()


def add_supplier(supplier_name, company_name, phone_number):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO suppliers
            (supplier_name, company_name, phone_number)
            VALUES (?, ?, ?)
        """, (supplier_name, company_name, phone_number))

        conn.commit()
        print("Supplier registered successfully!")

    except sqlite3.IntegrityError:
        print("This phone number is already registered.")

    finally:
        conn.close()


def register_supplier():
    print("\nREGISTER SUPPLIER")

    supplier_name = input("Contact name: ").strip()
    company_name = input("Company name: ").strip()
    phone_number = input("Phone number with country code: ").strip()

    if not supplier_name or not company_name or not phone_number:
        print("All fields are required.")
        return

    add_supplier(supplier_name, company_name, phone_number)


def show_suppliers():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, supplier_name, company_name, phone_number,
               telegram_chat_id
        FROM suppliers
    """)

    suppliers = cursor.fetchall()

    print("\nREGISTERED SUPPLIERS")

    if not suppliers:
        print("No suppliers registered.")

    for supplier in suppliers:
        print("\nSupplier ID:", supplier[0])
        print("Contact:", supplier[1])
        print("Company:", supplier[2])
        print("Phone:", supplier[3])
        print("Telegram linked:", "Yes" if supplier[4] else "No")

    conn.close()


def find_supplier_by_phone(phone_number):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, supplier_name, company_name, phone_number
        FROM suppliers
        WHERE phone_number = ?
    """, (phone_number,))

    supplier = cursor.fetchone()
    conn.close()

    return supplier


def search_supplier():
    phone_number = input(
        "\nEnter supplier phone number with country code: "
    ).strip()

    supplier = find_supplier_by_phone(phone_number)

    if supplier:
        print("\nSUPPLIER FOUND")
        print("Supplier ID:", supplier[0])
        print("Contact:", supplier[1])
        print("Company:", supplier[2])
        print("Phone:", supplier[3])
    else:
        print("Supplier not found.")


def link_telegram_account():
    print("\nLINK TELEGRAM ACCOUNT")
    print("Use the Telegram ID received from your bot's /myid command.")

    supplier_id = input("Enter supplier ID: ").strip()
    telegram_id = input("Enter Telegram account ID: ").strip()

    if not supplier_id.isdigit() or not telegram_id.isdigit():
        print("Please enter numbers only.")
        return

    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            UPDATE suppliers
            SET telegram_chat_id = ?
            WHERE id = ?
        """, (int(telegram_id), int(supplier_id)))

        if cursor.rowcount == 0:
            print("Supplier ID not found.")
        else:
            conn.commit()
            print("Telegram account linked successfully!")

    except sqlite3.IntegrityError:
        print("This Telegram account is already linked to another supplier.")

    finally:
        conn.close()


def main():
    create_supplier_table()

    while True:
        print("\n===== SUPPLIER DIRECTORY =====")
        print("1. Register supplier")
        print("2. View all suppliers")
        print("3. Search supplier by phone")
        print("4. Link Telegram account")
        print("5. Exit")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            register_supplier()
        elif choice == "2":
            show_suppliers()
        elif choice == "3":
            search_supplier()
        elif choice == "4":
            link_telegram_account()
        elif choice == "5":
            print("Exiting supplier directory.")
            break
        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()
