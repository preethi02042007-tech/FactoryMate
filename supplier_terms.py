
import re
import sqlite3

DB_NAME = "assistant.db"


def get_quotations():

    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row

    query = """
        SELECT
            q.id,
            COALESCE(s.company_name, s.supplier_name, q.supplier)
                AS supplier_name,
            q.material,
            q.original_message
        FROM quotations q
        LEFT JOIN suppliers s
            ON q.supplier_id = s.id
        ORDER BY q.id DESC
    """

    quotations = connection.execute(query).fetchall()

    connection.close()

    return quotations


def extract_delivery_terms(message):

    if not message:
        return None

    text = message.lower()

    patterns = [
        r"\bdelivery\s+in\s+\d+\s+days?\b",
        r"\bdeliver(?:ed|y)?\s+within\s+\d+\s+days?\b",
        r"\bdispatch(?:ed)?\s+within\s+\d+\s+days?\b",
        r"\bready\s+in\s+\d+\s+days?\b",
        r"\bwithin\s+\d+\s+days?\b",
        r"\b\d+\s+days?\s+(?:delivery|dispatch)\b"
    ]

    for pattern in patterns:

        match = re.search(pattern, text)

        if match:
            return match.group(0)

    return None


def extract_payment_terms(message):

    if not message:
        return None

    text = message.lower()

    patterns = [
        r"\b\d+\s*%\s*advance\b",
        r"\b\d+\s*%\s*advance\s+payment\b",
        r"\bfull\s+advance(?:\s+payment)?\b",
        r"\badvance\s+payment\b",
        r"\bcash\s+on\s+delivery\b",
        r"\bpayment\s+on\s+delivery\b",
        r"\bpayment\s+after\s+delivery\b",
        r"\b\d+\s+days?\s+credit\b",
        r"\bcredit\s+of\s+\d+\s+days?\b"
    ]

    for pattern in patterns:

        match = re.search(pattern, text)

        if match:
            return match.group(0)

    return None


def review_supplier_terms():

    print("\nFACTORYMATE - DELIVERY & PAYMENT TERMS")
    print("SAMPLE / TEST DATA — NOT VERIFIED SUPPLIER TERMS")

    quotations = get_quotations()

    if not quotations:

        print("\nNo quotations found.")
        return

    for quotation in quotations:

        message = quotation["original_message"] or ""

        delivery = extract_delivery_terms(message)
        payment = extract_payment_terms(message)

        print("\n======================================")
        print(f"Quotation ID: {quotation['id']}")
        print(f"Supplier: {quotation['supplier_name'] or 'Unknown'}")
        print(f"Material: {quotation['material'] or 'Unknown'}")

        print("\nDELIVERY INFORMATION:")

        if delivery:
            print(f"Detected: {delivery}")
        else:
            print("Not provided or not recognised.")

        print("\nPAYMENT INFORMATION:")

        if payment:
            print(f"Detected: {payment}")
        else:
            print("Not provided or not recognised.")

        if not delivery or not payment:

            print("\nFOLLOW-UP REQUIRED:")

            if not delivery:
                print("- Ask supplier to confirm delivery time.")

            if not payment:
                print("- Ask supplier to confirm payment terms.")

        else:

            print("\nBoth delivery and payment terms detected.")

    print("\n======================================")
    print("NOTE:")
    print("Detected terms are extracted from original messages.")
    print("Please verify them with the supplier before making decisions.")


if __name__ == "__main__":

    review_supplier_terms()
