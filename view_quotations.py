
import sqlite3

db = sqlite3.connect("assistant.db")

cursor = db.cursor()

cursor.execute("""
    SELECT
        id,
        supplier,
        material,
        quantity_kg,
        price_per_kg,
        gst,
        gst_rate,
        transport,
        original_message,
        created
    FROM quotations
    ORDER BY id DESC
""")

records = cursor.fetchall()

print("\nSAVED SUPPLIER QUOTATIONS")
print("SAMPLE / TEST DATA — NOT REAL SUPPLIER RESPONSES")

if not records:
    print("\nNo quotations found.")

else:
    for record in records:
        print("\n-----------------------------")
        print("Quotation ID:", record[0])
        print("Supplier:", record[1])
        print("Material:", record[2])
        print("Quantity:", record[3], "kg")
        print("Price:", record[4], "/kg")
        print("GST:", record[5])
        print("GST Rate:", record[6])
        print("Transport:", record[7])
        print("Original Message:", record[8])
        print("Saved At:", record[9])

    print("\nTotal saved quotations:", len(records))

db.close()
