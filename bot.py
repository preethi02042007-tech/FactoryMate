
import logging
logging.basicConfig(level=logging.INFO)

import os
import sqlite3

from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    filters
)

from quote_parser import extract_quote

TOKEN = os.environ["TELEGRAM_TOKEN"]

os.makedirs("media", exist_ok=True)

db = sqlite3.connect("assistant.db", check_same_thread=False)


# CREATE TABLES

db.execute("""
CREATE TABLE IF NOT EXISTS messages(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id INTEGER,
    direction TEXT,
    kind TEXT,
    text TEXT,
    file_path TEXT,
    created TEXT DEFAULT CURRENT_TIMESTAMP
)
""")

db.execute("""
CREATE TABLE IF NOT EXISTS quotations(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id INTEGER,
    supplier TEXT,
    material TEXT,
    quantity_kg REAL,
    price_per_kg REAL,
    gst TEXT,
    gst_rate REAL,
    transport REAL,
    original_message TEXT,
    created TEXT DEFAULT CURRENT_TIMESTAMP
)
""")

db.execute("""
CREATE TABLE IF NOT EXISTS suppliers(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    supplier_name TEXT NOT NULL,
    company_name TEXT,
    phone_number TEXT UNIQUE,
    telegram_chat_id INTEGER UNIQUE,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
)
""")

db.commit()


# ADD NEW COLUMNS TO EXISTING QUOTATIONS TABLE

def ensure_column(table, column, definition):

    cursor = db.execute(f"PRAGMA table_info({table})")

    existing_columns = [row[1] for row in cursor.fetchall()]

    if column not in existing_columns:
        db.execute(
            f"ALTER TABLE {table} ADD COLUMN {column} {definition}"
        )
        db.commit()


ensure_column("quotations", "supplier_id", "INTEGER")
ensure_column("quotations", "telegram_chat_id", "INTEGER")


# SAVE MESSAGES

def save(chat_id, direction, kind, text=None, file_path=None):

    db.execute(
        """
        INSERT INTO messages
        (chat_id, direction, kind, text, file_path)
        VALUES (?, ?, ?, ?, ?)
        """,
        (chat_id, direction, kind, text, file_path)
    )

    db.commit()


# FIND REGISTERED SUPPLIER USING TELEGRAM ACCOUNT ID

def find_supplier_by_telegram_id(chat_id):

    cursor = db.execute(
        """
        SELECT id, supplier_name, company_name
        FROM suppliers
        WHERE telegram_chat_id = ?
        """,
        (chat_id,)
    )

    return cursor.fetchone()


# SAVE QUOTATION

def save_quotation(chat_id, supplier, quote, original_message):

    supplier_id = supplier[0] if supplier else None

    if supplier:
        supplier_name = supplier[2] or supplier[1]
    else:
        supplier_name = "Unregistered Telegram account"

    db.execute(
        """
        INSERT INTO quotations
        (
            chat_id,
            supplier,
            material,
            quantity_kg,
            price_per_kg,
            gst,
            gst_rate,
            transport,
            original_message,
            supplier_id,
            telegram_chat_id
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            chat_id,
            supplier_name,
            quote["material"],
            quote["quantity_kg"],
            quote["price_per_kg"],
            quote["gst"],
            quote["gst_rate"],
            quote["transport"],
            original_message,
            supplier_id,
            chat_id
        )
    )

    db.commit()


# SHOW TELEGRAM ACCOUNT ID

async def my_id(update, context):

    chat_id = update.effective_chat.id

    await update.message.reply_text(
        "YOUR TELEGRAM ACCOUNT ID\n\n"
        + str(chat_id)
        + "\n\nShare this ID with the factory owner "
        "for manual supplier account linking."
    )


# HANDLE TEXT MESSAGES

async def on_text(update, context):

    m = update.message

    save(m.chat_id, "in", "text", m.text)

    if m.text.startswith("/"):
        return

    supplier = find_supplier_by_telegram_id(m.chat_id)

    if supplier:
        supplier_name = supplier[2] or supplier[1]
    else:
        supplier_name = "Unregistered Telegram account"

    quote = extract_quote(supplier_name, m.text)

    if (
        quote["material"] is not None
        and quote["quantity_kg"] is not None
        and quote["price_per_kg"] is not None
    ):

        save_quotation(m.chat_id, supplier, quote, m.text)

        if supplier:
            identity_message = (
                "Registered supplier: " + supplier_name
            )
        else:
            identity_message = (
                "Supplier account is not registered yet.\n"
                "Your quotation is saved as unverified."
            )

        reply = (
            "QUOTATION EXTRACTED AND SAVED\n\n"
            + identity_message + "\n"
            + "Material: " + str(quote["material"]) + "\n"
            + "Quantity: " + str(quote["quantity_kg"]) + " kg\n"
            + "Price: ₹" + str(quote["price_per_kg"]) + "/kg\n"
            + "GST: " + str(quote["gst"]) + "\n"
            + "GST rate: " + str(quote["gst_rate"]) + "\n"
            + "Transport: " + str(quote["transport"]) + "\n\n"
            + "Please verify these details."
        )

    else:

        reply = (
            "Message received and saved.\n\n"
            "I could not identify a complete quotation yet. "
            "Please provide material, quantity and price per kg."
        )

    await m.reply_text(reply)

    save(m.chat_id, "out", "text", reply)


# HANDLE VOICE MESSAGES

async def on_voice(update, context):

    m = update.message

    f = await m.voice.get_file()

    path = f"media/{m.message_id}.ogg"

    await f.download_to_drive(path)

    save(m.chat_id, "in", "voice", None, path)

    await m.reply_text(
        "Voice note saved. Voice quotation reading is not available yet."
    )


# HANDLE PHOTOS

async def on_photo(update, context):

    m = update.message

    f = await m.photo[-1].get_file()

    path = f"media/{m.message_id}.jpg"

    await f.download_to_drive(path)

    save(m.chat_id, "in", "photo", None, path)

    await m.reply_text(
        "Photo saved. Photo quotation reading is not available yet."
    )


# START COMMAND

async def start(update, context):

    await update.message.reply_text(
        "Welcome to Buying Assistant!\n\n"
        "Send a supplier quotation in text format.\n"
        "Use /myid to view your Telegram account ID."
    )


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("myid", my_id))

app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, on_text)
)

app.add_handler(MessageHandler(filters.VOICE, on_voice))
app.add_handler(MessageHandler(filters.PHOTO, on_photo))

app.run_polling()
