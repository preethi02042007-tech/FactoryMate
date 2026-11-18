
def calculate_order_cost(
    material_cost,
    labour_cost,
    transport_cost,
    other_expenses,
    selling_price
):

    total_cost = (
        material_cost
        + labour_cost
        + transport_cost
        + other_expenses
    )

    profit_or_loss = selling_price - total_cost

    if total_cost > 0:
        profit_margin = (profit_or_loss / selling_price * 100) if selling_price > 0 else 0
    else:
        profit_margin = 0

    return {
        "material_cost": material_cost,
        "labour_cost": labour_cost,
        "transport_cost": transport_cost,
        "other_expenses": other_expenses,
        "total_cost": total_cost,
        "selling_price": selling_price,
        "profit_or_loss": profit_or_loss,
        "profit_margin": profit_margin
    }


def main():

    print("\nFACTORYMATE - CUSTOMER ORDER COSTING")
    print("SAMPLE / TEST DATA — NOT REAL CUSTOMER ORDERS")

    print("\nEnter customer order details")

    try:

        material_cost = float(input("Raw material cost (₹): "))
        labour_cost = float(input("Labour cost (₹): "))
        transport_cost = float(input("Transportation cost (₹): "))
        other_expenses = float(input("Other production expenses (₹): "))
        selling_price = float(input("Customer selling price (₹): "))

        values = [
            material_cost,
            labour_cost,
            transport_cost,
            other_expenses,
            selling_price
        ]

        if any(value < 0 for value in values):
            print("\nERROR: Amounts cannot be negative.")
            return

        result = calculate_order_cost(
            material_cost,
            labour_cost,
            transport_cost,
            other_expenses,
            selling_price
        )

        print("\n========== ORDER COST REPORT ==========")

        print(f"Raw material cost: ₹{result['material_cost']:.2f}")
        print(f"Labour cost: ₹{result['labour_cost']:.2f}")
        print(f"Transportation: ₹{result['transport_cost']:.2f}")
        print(f"Other expenses: ₹{result['other_expenses']:.2f}")

        print("---------------------------------------")

        print(f"TOTAL PRODUCTION COST: ₹{result['total_cost']:.2f}")
        print(f"CUSTOMER SELLING PRICE: ₹{result['selling_price']:.2f}")

        print("---------------------------------------")

        if result["profit_or_loss"] > 0:

            print(f"EXPECTED PROFIT: ₹{result['profit_or_loss']:.2f}")
            print(f"PROFIT MARGIN: {result['profit_margin']:.2f}%")

        elif result["profit_or_loss"] < 0:

            print(f"EXPECTED LOSS: ₹{abs(result['profit_or_loss']):.2f}")

            if result["selling_price"] > 0:
                print(f"LOSS MARGIN: {abs(result['profit_margin']):.2f}%")

        else:

            print("BREAK-EVEN: No profit and no loss.")

        print("\nNOTE: This is an estimate based on entered costs.")
        print("Verify all expenses before accepting the customer order.")

    except ValueError:

        print("\nERROR: Please enter valid numerical amounts.")


if __name__ == "__main__":
    main()
