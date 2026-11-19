
import subprocess
import sys
from pathlib import Path


# FACTORYMATE COMMAND CENTER

BASE_DIR = Path(__file__).resolve().parent

MODULES = {
    "1": ("Supplier Directory", "supplier_directory.py"),
    "2": ("View Supplier Quotations", "view_quotations.py"),
    "3": ("Supplier Cost Comparison", "supplier_comparison.py"),
    "4": ("Supplier Price History", "price_history.py"),
    "5": ("Supplier Follow-up Assistant", "followup.py"),
    "6": ("Customer Order Costing", "order_costing.py"),
    "7": ("Supplier Delivery & Payment Terms", "supplier_terms.py"),
    "8": ("Supplier Reliability Tracker", "supplier_reliability.py"),
    "9": ("Telegram Supplier Bot", "bot.py"),
}


def run_module(module_name, filename):

    module_path = BASE_DIR / filename

    print("\n" + "=" * 50)

    if not module_path.exists():
        print("MODULE NOT FOUND:", filename)
        print("Please check that the file exists.")
        return

    print("Starting:", module_name)
    print("=" * 50)

    try:
        subprocess.run(
            [sys.executable, str(module_path)],
            cwd=BASE_DIR,
            check=False
        )

    except KeyboardInterrupt:
        print("\nModule stopped by user.")

    except Exception as error:
        print("Error starting module:", error)

    print("\nReturned to FactoryMate Command Center.")


def show_menu():

    print("\n")
    print("=" * 50)
    print("       FACTORYMATE COMMAND CENTER")
    print("       Your Smart Manufacturing Partner")
    print("=" * 50)

    print("\nSUPPLIER MANAGEMENT")
    print("1. Supplier Directory")
    print("2. View Supplier Quotations")
    print("3. Supplier Cost Comparison")
    print("4. Supplier Price History")
    print("5. Supplier Follow-up Assistant")

    print("\nCUSTOMER & PRODUCTION")
    print("6. Customer Order Costing")

    print("\nSUPPLIER INTELLIGENCE")
    print("7. Delivery & Payment Terms")
    print("8. Supplier Reliability Tracker")

    print("\nCOMMUNICATION")
    print("9. Start Telegram Supplier Bot")

    print("\n0. Exit")

    print("=" * 50)


def main():

    while True:

        show_menu()

        choice = input("\nChoose an option: ").strip()

        if choice == "0":

            print("\nThank you for using FactoryMate!")
            print("Command Center closed.")
            break

        elif choice in MODULES:

            module_name, filename = MODULES[choice]

            run_module(module_name, filename)

            input("\nPress Enter to return to the main menu...")

        else:

            print("\nInvalid option.")
            print("Please choose a number from 0 to 9.")


if __name__ == "__main__":
    main()
