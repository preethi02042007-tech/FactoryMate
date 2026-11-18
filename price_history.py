
import sqlite3
from collections import defaultdict

DB_NAME = "assistant.db"


def get_price_history():

    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    query = """
        SELECT
            COALESCE(s.company_name, s.supplier_name, q.supplier)
                AS supplier_name,
            q.material,
            q.price_per_kg,
            DATE(q.created) AS price_date,
            q.id
        FROM quotations q
        INNER JOIN suppliers s
            ON q.supplier_id = s.id
        WHERE
            q.supplier_id IS NOT NULL
            AND q.material IS NOT NULL
            AND q.price_per_kg IS NOT NULL
        ORDER BY
            supplier_name,
            q.material,
            q.created ASC,
            q.id ASC
    """

    cursor.execute(query)
    records = cursor.fetchall()

    connection.close()

    return records


def remove_duplicate_entries(records):

    grouped = defaultdict(list)

    for record in records:

        key = (
            record["supplier_name"],
            record["material"]
        )

        grouped[key].append(record)

    cleaned_history = {}

    for key, entries in grouped.items():

        unique_entries = []
        seen = set()

        for entry in entries:

            duplicate_key = (
                entry["price_date"],
                entry["price_per_kg"]
            )

            if duplicate_key not in seen:
                unique_entries.append(entry)
                seen.add(duplicate_key)

        cleaned_history[key] = unique_entries

    return cleaned_history


def show_price_history():

    print("\nSUPPLIER PRICE HISTORY")
    print("SOURCE: SQLITE DATABASE")
    print("NOTE: SAMPLE / TEST DATA IS NOT REAL SUPPLIER DATA")

    records = get_price_history()

    if not records:
        print("\nNo registered supplier price records found.")
        return

    history = remove_duplicate_entries(records)

    for (supplier, material), entries in history.items():

        print("\n--------------------------")
        print(f"Supplier: {supplier}")
        print(f"Material: {material}")

        for entry in entries:

            print(
                f"Date: {entry['price_date']} | "
                f"Price: ₹{entry['price_per_kg']}/kg"
            )

        first_price = entries[0]["price_per_kg"]
        latest_price = entries[-1]["price_per_kg"]

        print(f"\nFirst recorded price: ₹{first_price}/kg")
        print(f"Latest recorded price: ₹{latest_price}/kg")

        difference = latest_price - first_price

        if difference > 0:
            print(f"Overall increase: ₹{difference}/kg")

        elif difference < 0:
            print(f"Overall decrease: ₹{abs(difference)}/kg")

        else:
            print("Overall price unchanged.")


if __name__ == "__main__":
    show_price_history()
