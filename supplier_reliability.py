
import sqlite3
from datetime import datetime

DB_NAME = "assistant.db"


def connect_database():

    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row

    connection.execute("""
        CREATE TABLE IF NOT EXISTS supplier_performance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            supplier_id INTEGER NOT NULL,
            delivery_status TEXT NOT NULL,
            quality_issue INTEGER NOT NULL,
            notes TEXT,
            recorded_at TEXT NOT NULL,
            FOREIGN KEY (supplier_id) REFERENCES suppliers(id)
        )
    """)

    connection.commit()

    return connection


def view_suppliers():

    connection = connect_database()

    suppliers = connection.execute("""
        SELECT id, company_name, supplier_name
        FROM suppliers
        ORDER BY id
    """).fetchall()

    connection.close()

    print("\nREGISTERED SUPPLIERS")

    if not suppliers:
        print("No suppliers registered.")
        return

    for supplier in suppliers:

        name = supplier["company_name"] or supplier["supplier_name"]

        print(f"ID: {supplier['id']} | Supplier: {name}")


def record_performance():

    view_suppliers()

    try:
        supplier_id = int(input("\nEnter supplier ID: "))

    except ValueError:
        print("ERROR: Enter a valid supplier ID.")
        return

    connection = connect_database()

    supplier = connection.execute("""
        SELECT id
        FROM suppliers
        WHERE id = ?
    """, (supplier_id,)).fetchone()

    if not supplier:
        print("Supplier not found.")
        connection.close()
        return

    print("\nDELIVERY STATUS")
    print("1. Delivered on time")
    print("2. Delayed")

    delivery_choice = input("Choose an option: ").strip()

    if delivery_choice not in ("1", "2"):
        print("Invalid delivery choice.")
        connection.close()
        return

    delivery_status = (
        "On Time" if delivery_choice == "1" else "Delayed"
    )

    print("\nQUALITY CHECK")
    print("1. No quality issue")
    print("2. Quality issue reported")

    quality_choice = input("Choose an option: ").strip()

    if quality_choice not in ("1", "2"):
        print("Invalid quality choice.")
        connection.close()
        return

    quality_issue = 1 if quality_choice == "2" else 0

    notes = input("\nAdditional notes (press Enter to skip): ").strip()

    recorded_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    connection.execute("""
        INSERT INTO supplier_performance (
            supplier_id,
            delivery_status,
            quality_issue,
            notes,
            recorded_at
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        supplier_id,
        delivery_status,
        quality_issue,
        notes,
        recorded_at
    ))

    connection.commit()
    connection.close()

    print("\nSupplier performance record saved successfully.")


def view_reliability_report():

    connection = connect_database()

    reports = connection.execute("""
        SELECT
            s.id,
            COALESCE(s.company_name, s.supplier_name) AS supplier_name,
            COUNT(p.id) AS total_orders,
            SUM(
                CASE WHEN p.delivery_status = 'On Time'
                THEN 1 ELSE 0 END
            ) AS on_time_deliveries,
            SUM(
                CASE WHEN p.delivery_status = 'Delayed'
                THEN 1 ELSE 0 END
            ) AS delayed_deliveries,
            SUM(
                CASE WHEN p.quality_issue = 1
                THEN 1 ELSE 0 END
            ) AS quality_issues
        FROM suppliers s
        LEFT JOIN supplier_performance p
            ON s.id = p.supplier_id
        GROUP BY s.id
        ORDER BY s.id
    """).fetchall()

    connection.close()

    print("\nFACTORYMATE - SUPPLIER RELIABILITY REPORT")
    print("Based on owner-recorded performance data.")

    for report in reports:

        total = report["total_orders"]
        on_time = report["on_time_deliveries"] or 0
        delayed = report["delayed_deliveries"] or 0
        quality = report["quality_issues"] or 0

        print("\n======================================")
        print(f"Supplier: {report['supplier_name']}")
        print(f"Total recorded deliveries: {total}")

        if total == 0:
            print("Reliability: No performance data available.")
            continue

        percentage = (on_time / total) * 100

        print(f"On-time deliveries: {on_time}")
        print(f"Delayed deliveries: {delayed}")
        print(f"Quality issues: {quality}")
        print(f"On-time delivery rate: {percentage:.2f}%")

    print("\nNOTE:")
    print("This report uses recorded delivery outcomes.")
    print("It is not an independently verified supplier rating.")


def main():

    while True:

        print("\n========== FACTORYMATE ==========")
        print("SUPPLIER RELIABILITY TRACKER")
        print("1. View registered suppliers")
        print("2. Record supplier performance")
        print("3. View reliability report")
        print("4. Exit")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            view_suppliers()

        elif choice == "2":
            record_performance()

        elif choice == "3":
            view_reliability_report()

        elif choice == "4":
            print("\nExiting Supplier Reliability Tracker.")
            break

        else:
            print("\nInvalid option. Please try again.")


if __name__ == "__main__":
    main()
