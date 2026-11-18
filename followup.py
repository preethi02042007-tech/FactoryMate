
import re
import sqlite3

DB_NAME = "assistant.db"


def get_incomplete_quotations():

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
            q.transport,
            q.original_message,
            q.created
        FROM quotations q
        LEFT JOIN suppliers s
            ON q.supplier_id = s.id
        ORDER BY q.id DESC
    """

    cursor.execute(query)
    quotations = cursor.fetchall()

    connection.close()

    return quotations


def has_delivery_information(message):

    if not message:
        return False

    text = message.lower()

    delivery_patterns = [
        r"\bdelivery\b",
        r"\bdeliver(?:y|ed)?\b",
        r"\bdispatch(?:ed)?\b",
        r"\bready\s+in\b",
        r"\bwithin\s+\d+\s+days?\b",
        r"\b\d+\s+days?\s+(?:delivery|dispatch)\b",
    ]

    for pattern in delivery_patterns:

        if re.search(pattern, text):
            return True

    return False


def identify_missing_information(quotation):

    missing = []

    gst_status = quotation["gst"]

    if not gst_status or gst_status.lower() in ("unknown", "none"):

        missing.append("GST status")

    elif gst_status.lower() == "extra" and quotation["gst_rate"] is None:

        missing.append("GST rate")

    if quotation["transport"] is None:

        missing.append("transportation charges")

    original_message = quotation["original_message"]

    if not has_delivery_information(original_message):

        missing.append("expected delivery date")

    return missing


def create_followup_message(supplier, material, missing):

    details = ", ".join(missing)

    message = (
        f"Hello {supplier},\n\n"
        f"Thank you for sharing your quotation for {material}.\n\n"
        f"Could you please confirm the following details: "
        f"{details}?\n\n"
        f"Thank you."
    )

    return message


def review_followups():

    print("\nFACTORYMATE - SUPPLIER FOLLOW-UP ASSISTANT")
    print("SAMPLE / TEST DATA — NOT REAL SUPPLIER RESPONSES")

    quotations = get_incomplete_quotations()

    if not quotations:

        print("\nNo quotations found in the database.")
        return

    incomplete_count = 0

    for quotation in quotations:

        missing = identify_missing_information(quotation)

        if not missing:
            continue

        incomplete_count += 1

        supplier = quotation["supplier_name"] or "Unknown Supplier"
        material = quotation["material"] or "Unknown Material"

        print("\n================================")
        print(f"Quotation ID: {quotation['id']}")
        print(f"Supplier: {supplier}")
        print(f"Material: {material}")
        print(f"Quantity: {quotation['quantity_kg']} kg")
        print(f"Price: ₹{quotation['price_per_kg']}/kg")

        if quotation["supplier_id"] is None:

            print("\nSUPPLIER VERIFICATION: NOT REGISTERED")
            print("Warning: Verify supplier identity before contacting.")

        else:

            print("\nSUPPLIER VERIFICATION: REGISTERED")

        print("\nMISSING INFORMATION:")

        for item in missing:

            print(f"- {item}")

        draft = create_followup_message(
            supplier,
            material,
            missing
        )

        print("\nFOLLOW-UP MESSAGE DRAFT:")
        print("------------------------")
        print(draft)

        print("\nSTATUS: Waiting for owner review.")
        print("No message has been sent.")

    if incomplete_count == 0:

        print("\nAll quotations have the required information.")

    print(f"\nTotal incomplete quotations: {incomplete_count}")


if __name__ == "__main__":

    review_followups()
