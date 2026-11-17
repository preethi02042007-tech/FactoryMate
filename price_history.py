
import json
import os
from datetime import datetime

HISTORY_FILE = "supplier_price_history.json"


def load_history():

    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as file:
            return json.load(file)

    return {}


def save_history(history):

    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=4)


def record_price(supplier, material, price_per_kg):

    if not supplier or not material or price_per_kg is None:
        print("Cannot save price: information is missing.")
        return

    history = load_history()
    supplier_key = supplier + "|" + material
    previous_prices = history.get(supplier_key, [])

    if previous_prices:

        previous_price = previous_prices[-1]["price_per_kg"]

        print(f"Previous price: ₹{previous_price}/kg")
        print(f"New price: ₹{price_per_kg}/kg")

        difference = price_per_kg - previous_price

        if difference > 0:
            print(f"Price increased by ₹{difference}/kg")
        elif difference < 0:
            print(f"Price decreased by ₹{abs(difference)}/kg")
        else:
            print("Price has not changed.")

    else:
        print(f"No previous price for {supplier}.")

    today = datetime.now().strftime("%Y-%m-%d")

    if previous_prices:
        last_record = previous_prices[-1]

        if (
            last_record["price_per_kg"] == price_per_kg
            and last_record["date"] == today
        ):
            print("Same price already recorded today.")
            return

    previous_prices.append({
        "price_per_kg": price_per_kg,
        "date": today
    })

    history[supplier_key] = previous_prices
    save_history(history)


def show_price_history():

    history = load_history()

    print("\nSUPPLIER PRICE HISTORY")
    print("SAMPLE / TEST DATA — NOT REAL RESPONSES")

    if not history:
        print("No price history available.")
        return

    for supplier_key, records in history.items():

        supplier, material = supplier_key.split("|", 1)

        print("\n--------------------------")
        print("Supplier:", supplier)
        print("Material:", material)

        for record in records:
            print(
                f"Date: {record['date']} | "
                f"Price: ₹{record['price_per_kg']}/kg"
            )

        if len(records) >= 2:

            first_price = records[0]["price_per_kg"]
            latest_price = records[-1]["price_per_kg"]

            difference = latest_price - first_price

            print(f"First recorded price: ₹{first_price}/kg")
            print(f"Latest recorded price: ₹{latest_price}/kg")

            if difference > 0:
                print(f"Overall increase: ₹{difference}/kg")
            elif difference < 0:
                print(f"Overall decrease: ₹{abs(difference)}/kg")
            else:
                print("Overall price unchanged.")


if __name__ == "__main__":
    show_price_history()
