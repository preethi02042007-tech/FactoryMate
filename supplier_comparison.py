
import sqlite3

DB_NAME = "assistant.db"


def get_supplier_quotations(material):

    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    query = """
        SELECT
            q.id,
            q.supplier_id,
            COALESCE(s.company_name, s.supplier_name, q.supplier)
                AS supplier_name,
            q.material,
            q.quantity_kg,
            q.price_per_kg,
            q.gst,
            q.gst_rate,
            q.transport
        FROM quotations q
        LEFT JOIN suppliers s
            ON q.supplier_id = s.id
        WHERE LOWER(q.material) = LOWER(?)
          AND q.supplier_id IS NOT NULL
        ORDER BY q.id DESC
    """

    cursor.execute(query, (material,))
    quotations = cursor.fetchall()

    connection.close()

    return quotations


def calculate_estimated_cost(quotation):

    quantity = quotation["quantity_kg"] or 0
    price = quotation["price_per_kg"] or 0
    transport = quotation["transport"]

    material_cost = quantity * price
    transport_cost = transport or 0

    gst_status = quotation["gst"]
    gst_rate = quotation["gst_rate"]

    gst_cost = 0
    warning = None

    if gst_status and gst_status.lower() == "extra":

        if gst_rate is not None:
            gst_cost = material_cost * gst_rate / 100
        else:
            warning = "GST rate missing"

    elif not gst_status or gst_status.lower() in ("unknown", "none"):

        warning = "GST status unknown"

    estimated_total = material_cost + transport_cost + gst_cost

    return {
        "material_cost": material_cost,
        "transport_cost": transport_cost,
        "gst_cost": gst_cost,
        "estimated_total": estimated_total,
        "warning": warning
    }


def compare_suppliers():

    print("\nFACTORYMATE - SUPPLIER COMPARISON")
    print("SAMPLE / TEST DATA — NOT VERIFIED SUPPLIER OFFERS")

    material = input("\nEnter material name: ").strip()

    if not material:
        print("ERROR: Material name cannot be empty.")
        return

    quotations = get_supplier_quotations(material)

    if not quotations:

        print("\nNo registered supplier quotations found.")
        return

    results = []

    for quotation in quotations:

        if quotation["quantity_kg"] is None or quotation["price_per_kg"] is None:
            continue

        if quotation["quantity_kg"] <= 0 or quotation["price_per_kg"] < 0:
            continue

        cost = calculate_estimated_cost(quotation)

        results.append({
            "supplier": quotation["supplier_name"],
            "quantity": quotation["quantity_kg"],
            "price": quotation["price_per_kg"],
            "cost": cost
        })

    if not results:

        print("\nNo valid quotations available for comparison.")
        return

    results.sort(key=lambda item: item["cost"]["estimated_total"])

    print("\n========== SUPPLIER RANKING ==========")
    print("Ranking is based on estimated cost only.")

    for rank, item in enumerate(results, start=1):

        cost = item["cost"]

        print("\n--------------------------------------")
        print(f"RANK: {rank}")
        print(f"Supplier: {item['supplier']}")
        print(f"Quantity: {item['quantity']} kg")
        print(f"Price: ₹{item['price']}/kg")

        print(f"Material cost: ₹{cost['material_cost']:.2f}")
        print(f"Transport: ₹{cost['transport_cost']:.2f}")
        print(f"GST: ₹{cost['gst_cost']:.2f}")

        print(f"ESTIMATED TOTAL: ₹{cost['estimated_total']:.2f}")

        if cost["warning"]:
            print(f"WARNING: {cost['warning']}")

    print("\nNOTE:")
    print("This ranking considers estimated cost only.")
    print("It does not evaluate delivery, quality or payment terms.")
    print("Verify GST and other charges before selecting a supplier.")


if __name__ == "__main__":
    compare_suppliers()
