
import re


def extract_quote(supplier_name, message):

    text = message.lower()

    # Extract material
    material = None

    if "mild steel" in text or "ms sheet" in text:
        material = "Mild Steel Sheet"

    # Extract quantity
    quantity_match = re.search(r"(\d+(?:\.\d+)?)\s*kg", text)
    quantity = float(quantity_match.group(1)) if quantity_match else None

    # Extract price per kg
    price_match = re.search(
        r"₹?\s*(\d+(?:\.\d+)?)\s*(?:/kg|per kg)",
        text
    )
    price = float(price_match.group(1)) if price_match else None

    # Extract GST rate
    gst_rate_match = re.search(
        r"gst\s*(\d+(?:\.\d+)?)\s*%|(\d+(?:\.\d+)?)\s*%\s*gst",
        text
    )

    gst_rate = None

    if gst_rate_match:
        gst_rate = float(
            gst_rate_match.group(1) or gst_rate_match.group(2)
        )

    # Extract GST status
    if "gst included" in text or "gst incl" in text:
        gst = "Included"

    elif re.search(
        r"(?:gst\s*(?:\d+(?:\.\d+)?\s*%)?|\d+(?:\.\d+)?\s*%\s*gst)\s*(?:is\s*)?(?:extra|separate)",
        text
    ):
        gst = "Extra"

    else:
        gst = "Unknown"

    # Extract transport
    transport_match = re.search(
        r"transport\s*(?:is\s*)?(?:₹|rs\.?)?\s*(\d+)",
        text
    )

    if "transport free" in text or "free transport" in text:
        transport = 0

    elif transport_match:
        transport = float(transport_match.group(1))

    else:
        transport = None

    return {
        "supplier": supplier_name,
        "material": material,
        "quantity_kg": quantity,
        "price_per_kg": price,
        "gst": gst,
        "gst_rate": gst_rate,
        "transport": transport
    }


# SAMPLE / TEST DATA — NOT REAL RESPONSES

if __name__ == "__main__":

    sample_quotes = [
        ("ABC Steels", "Mild Steel Sheet 100 kg, ₹65 per kg, GST 18% extra, transport 1200"),
        ("Sri Lakshmi Metals", "MS Sheet 100 kg, ₹62 per kg, 18% GST extra, transport 900"),
        ("Bharat Steel Traders", "Mild Steel Sheet 100 kg, ₹68 per kg, GST included, transport 0"),
        ("Krishna Metals", "Mild Steel Sheet 100 kg, ₹60 per kg, GST extra, transport free"),
        ("Ravi Industrial Suppliers", "MS Sheet 100 kg, ₹64 per kg, GST extra, transport 700")
    ]

    print("SAMPLE / TEST DATA — NOT REAL RESPONSES")

    for supplier, message in sample_quotes:

        result = extract_quote(supplier, message)

        print("\n--------------------------")
        print("SUPPLIER QUOTE DETAILS")

        for key, value in result.items():
            print(f"{key}: {value}")
