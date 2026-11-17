# FactoryMate

### Your Smart Manufacturing Partner

**An Agentic AI-powered Procurement and Cost Intelligence Assistant for Small Manufacturers.**

## 1. Problem Statement

Small manufacturing businesses often depend on manual communication with suppliers to collect quotations and compare prices. Calculating material costs, GST, transportation and other expenses manually can lead to purchasing inefficiencies and incorrect customer quotations.

FactoryMate aims to simplify this process through an intelligent procurement and cost intelligence assistant.

## 2. Proposed Solution

FactoryMate helps small manufacturers collect supplier quotations, extract important details, compare estimated purchasing costs and maintain supplier price history.

The long-term vision is to make this assistant available through WhatsApp Business, with support for local languages such as Kannada and Kanglish.

## 3. Current Prototype Features

The current Python prototype includes:

- Telegram-based messaging interface for testing.
- Collection and storage of incoming messages.
- Basic extraction of material, quantity, price, GST and transportation details.
- Supplier directory and Telegram account linking.
- SQLite database for storing messages and quotations.
- Supplier cost comparison using material cost, GST and transportation.
- Basic supplier price history functionality.

## 4. How It Works

1. A supplier sends a quotation through the Telegram prototype.
2. FactoryMate stores the original message.
3. The quotation parser extracts available information.
4. The system links the quotation to a registered supplier when possible.
5. The cost comparison module estimates the total purchasing cost.
6. The manufacturer can review the available information before making a purchasing decision.

## 5. Technology Stack

- **Programming Language:** Python
- **Messaging Prototype:** Telegram Bot API
- **Database:** SQLite
- **Data Extraction:** Python regular expressions
- **Development Environment:** Visual Studio Code
- **Version Control:** Git and GitHub

## 6. Agentic AI Approach

FactoryMate follows a human-in-the-loop approach.

AI-assisted interpretation and automation are part of the product vision. Deterministic Python code handles numerical calculations, while the manufacturer retains control over supplier selection, purchase approval and payments.

The current prototype demonstrates foundational automation and procurement logic. It does not yet implement the complete AI-agent workflow.

## 7. Future Development Roadmap

- WhatsApp Business Platform integration.
- Kannada, Kanglish and Hindi language support.
- Voice message transcription.
- Image-based quotation extraction using OCR and vision models.
- Automated supplier follow-ups with owner approval.
- More comprehensive landed-cost calculations.
- Customer quotation and profit/loss analysis.
- Demand pooling between nearby manufacturing businesses.

## 8. Privacy and Reliability

- Supplier quotations are intended to remain private to each business.
- Important purchasing decisions remain under human control.
- Incomplete or unclear quotation information should be flagged rather than guessed.
- Real supplier data must be handled securely.

## 9. Current Prototype Status

FactoryMate is an early-stage working prototype. Telegram is currently used as a temporary testing interface; WhatsApp integration, advanced AI capabilities, multilingual processing and voice/image extraction are planned developments.

Some test outputs use sample data and should not be interpreted as real supplier quotations or verified savings.

## 10. Project Vision

FactoryMate aims to help small manufacturers make better purchasing decisions, understand their actual production costs and quote customer orders more confidently.

**One smarter purchase. One better quotation. One stronger manufacturing business.**
