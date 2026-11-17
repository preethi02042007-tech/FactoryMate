
import sqlite3

DB_NAME = "assistant.db"


def get_saved_quotations():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            q.id,
            q.supplier,
            q.material,
            q.quantity_kg,
            q.price_per_kg,
            q.gst,
            q.gst_rate,
            q.transport,
            q.original_message,
            s.id AS registered_supplier_id
        FROM quotations q
        LEFT JOIN suppliers s
            ON q.supplier_id = s.id
        WHERE s.id IS NOT NULL
        ORDER BY q.id DESC
    """)

    quotations = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return quotations


def calculate_cost(quote):
    quantity = quote["quantity_kg"]
    price = quote["price_per_kg"]
    transport = quote["transport"] or 0

    material_cost = quantity * price
    cost_before_gst = material_cost + transport

    gst_status = (quote["gst"] or "Unknown").lower()
    gst_rate = quote["gst_rate"]

    if gst_status == "included":
        gst_amount = 0
        estimated_total = cost_before_gst

    elif gst_status == "extra" and gst_rate is not None:
        # Prototype assumption: GST on material cost only.
        gst_amount = material_cost * gst_rate / 100
        estimated_total = cost_before_gst + gst_amount

    else:
        gst_amount = None
        estimated_total = None

    return {
        "material_cost": material_cost,
        "transport": transport,
        "cost_before_gst": cost_before_gst,
        "gst_amount": gst_amount,
        "estimated_total": estimated_total
    }


def main():
    print("\nDATABASE-BASED SUPPLIER COST COMPARISON")
    print("SAMPLE / TEST DATA — NOT REAL SUPPLIER RESPONSES")
    print("Freight GST is not included in these prototype estimates.")

    quotations = get_saved_quotations()

    if not quotations:
        print("\nNo quotations from registered suppliers were found.")
        return

    comparable = []
    pending = []

    for quote in quotations:
        if (
            quote["quantity_kg"] is None
            or quote["price_per_kg"] is None
        ):
            continue

        result = calculate_cost(quote)

        item = {
            "quote": quote,
            "cost": result
        }

        if result["estimated_total"] is not None:
            comparable.append(item)
        else:
            pending.append(item)

    comparable.sort(
        key=lambda item: item["cost"]["estimated_total"]
    )

    print("\nSUPPLIER RANKING")

    if not comparable:
        print("No complete quotations available for ranking.")

    for rank, item in enumerate(comparable, start=1):
        quote = item["quote"]
        cost = item["cost"]

        print("\n--------------------------")
        print("Rank:", rank)
        print("Supplier:", quote["supplier"])
        print("Material:", quote["material"])
        print("Quantity:", quote["quantity_kg"], "kg")
        print("Price:", quote["price_per_kg"], "/kg")
        print("Material cost: ₹", cost["material_cost"])
        print("Transport: ₹", cost["transport"])
        print("GST status:", quote["gst"])
        print("GST rate:", quote["gst_rate"])
        print("GST amount: ₹", cost["gst_amount"])
        print("Estimated total: ₹", cost["estimated_total"])

    if pending:
        print("\nSUPPLIERS PENDING GST CONFIRMATION")

    for item in pending:
        quote = item["quote"]
        cost = item["cost"]

        print("\n--------------------------")
        print("Supplier:", quote["supplier"])
        print("Material:", quote["material"])
        print("Cost before GST: ₹", cost["cost_before_gst"])
        print("GST status:", quote["gst"])
        print("GST rate:", quote["gst_rate"])
        print("Estimated total: NOT AVAILABLE")
        print("Reason: GST information is incomplete.")


if __name__ == "__main__":
    main()
