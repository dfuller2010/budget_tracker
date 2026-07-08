import json
import os
from datetime import datetime
 
 
# -- Data ----------------------------------------------------------------------
 
def load_data():
    if os.path.exists("expenses.json"):
        with open("expenses.json", "r") as f:
            return json.load(f)
    return {
        "categories": ["Food", "Transport", "Bills", "Entertainment", "Other"],
        "expenses": []
    }
 
def save_data(data):
    with open("expenses.json", "w") as f:
        json.dump(data, f, indent=2)
 
 
# -- Categories ----------------------------------------------------------------
 
def get_categories(data):
    return data["categories"]
 
def add_category(data):
    categories = get_categories(data)
    print("\nCurrent categories:", ", ".join(categories))
    name = input("New category name: ").strip().title()
    if name in categories:
        print(f"'{name}' already exists.")
    elif name == "":
        print("Category name can't be blank.")
    else:
        categories.append(name)
        save_data(data)
        print(f"'{name}' added.")
    return data
 
 
# -- Expenses ------------------------------------------------------------------
 
def add_expense(data):
    categories = get_categories(data)
 
    # Amount
    while True:
        try:
            amount = float(input("\nAmount: $"))
            if amount <= 0:
                print("Amount must be greater than zero.")
                continue
            break
        except ValueError:
            print("Please enter a number.")
 
    # Category
    print("\nCategories:")
    for i, cat in enumerate(categories, 1):
        print(f"  {i}. {cat}")
    while True:
        try:
            choice = int(input("Choose a number: "))
            if 1 <= choice <= len(categories):
                category = categories[choice - 1]
                break
            else:
                print(f"Enter a number between 1 and {len(categories)}.")
        except ValueError:
            print("Please enter a number.")
 
    # Description
    description = input("Description: ").strip()
 
    # Date
    today = datetime.today().strftime("%Y-%m-%d")
    while True:
        date_input = input(f"Date (YYYY-MM-DD) [press Enter for today, {today}]: ").strip()
        if date_input == "":
            date = today
            break
        try:
            datetime.strptime(date_input, "%Y-%m-%d")
            date = date_input
            break
        except ValueError:
            print("Invalid date. Use YYYY-MM-DD format, e.g. 2026-06-15.")
 
    expense = {
        "amount": amount,
        "category": category,
        "description": description,
        "date": date
    }
    data["expenses"].append(expense)
    save_data(data)
    print(f"\nExpense added: ${amount:.2f} | {category} | {date}")
    return data
 
def view_all_expenses(data):
    expenses = data.get("expenses", [])
    if not expenses:
        print("\nNo expenses recorded.")
        return data

    # Sort by date then amount
    try:
        sorted_expenses = sorted(expenses, key=lambda e: (e.get("date", ""), -float(e.get("amount", 0))))
    except Exception:
        sorted_expenses = list(expenses)

    print()
    for i, e in enumerate(sorted_expenses, 1):
        amt = float(e.get("amount", 0))
        cat = e.get("category", "")
        desc = e.get("description", "")
        date = e.get("date", "")
        print(f"{i}. {date} | {cat} | ${amt:.2f} | {desc}")
    return data
 
def view_month_expenses(data):
    from datetime import datetime as _dt
    today = _dt.today()
    default = today.strftime("%Y-%m")
    month_input = input(f"Show month (YYYY-MM) [press Enter for {default}]: ").strip()
    if month_input == "":
        month = default
    else:
        try:
            _dt.strptime(month_input + "-01", "%Y-%m-%d")
            month = month_input
        except ValueError:
            print("Invalid month format. Use YYYY-MM.")
            return data

    filtered = [e for e in data.get("expenses", []) if e.get("date", "").startswith(month)]
    if not filtered:
        print(f"\nNo expenses found for {month}.")
        return data

    total = 0.0
    print()
    for i, e in enumerate(filtered, 1):
        amt = float(e.get("amount", 0))
        total += amt
        print(f"{i}. {e.get('date','')} | {e.get('category','')} | ${amt:.2f} | {e.get('description','')}")
    print(f"\nTotal for {month}: ${total:.2f}")
    return data
 
def delete_expense(data):
    expenses = data.get("expenses", [])
    if not expenses:
        print("\nNo expenses to delete.")
        return data

    view_all_expenses(data)
    try:
        choice = input("\nEnter expense number to delete (or press Enter to cancel): ").strip()
        if choice == "":
            print("Cancelled.")
            return data
        idx = int(choice)
        if 1 <= idx <= len(expenses):
            removed = expenses.pop(idx - 1)
            save_data(data)
            print(f"Removed expense: ${float(removed.get('amount',0)):.2f} | {removed.get('category','')} | {removed.get('date','')}")
        else:
            print("Invalid selection.")
    except ValueError:
        print("Please enter a valid number.")
    return data
 
 
# -- Reports -------------------------------------------------------------------
 
def monthly_report(data):
    from datetime import datetime as _dt
    default = _dt.today().strftime("%Y-%m")
    month_input = input(f"Report month (YYYY-MM) [press Enter for {default}]: ").strip()
    if month_input == "":
        month = default
    else:
        try:
            _dt.strptime(month_input + "-01", "%Y-%m-%d")
            month = month_input
        except ValueError:
            print("Invalid month format. Use YYYY-MM.")
            return data

    totals = {}
    for e in data.get("expenses", []):
        if not e.get("date", "").startswith(month):
            continue
        cat = e.get("category", "Other")
        amt = float(e.get("amount", 0))
        totals[cat] = totals.get(cat, 0.0) + amt

    if not totals:
        print(f"\nNo expenses for {month}.")
        return data

    overall = sum(totals.values())
    print(f"\nMonthly report for {month}:")
    for cat, amt in sorted(totals.items(), key=lambda x: -x[1]):
        print(f"- {cat}: ${amt:.2f}")
    print(f"Total: ${overall:.2f}")
    return data
 
 
# -- Main ----------------------------------------------------------------------
 
def main():
    data = load_data()
    actions = {
        "1": lambda d: add_expense(d),
        "2": lambda d: view_all_expenses(d),
        "3": lambda d: view_month_expenses(d),
        "4": lambda d: delete_expense(d),
        "5": lambda d: add_category(d),
        "6": lambda d: monthly_report(d),
    }

    while True:
        print("\nBudget Tracker")
        print("1) Add expense")
        print("2) View all expenses")
        print("3) View month expenses")
        print("4) Delete expense")
        print("5) Add category")
        print("6) Monthly report")
        print("7) Quit")
        choice = input("Choose an option: ").strip()
        if choice == "7" or choice.lower() in ("q", "quit", "exit"):
            print("Goodbye.")
            break
        action = actions.get(choice)
        if action:
            data = action(data) or data
        else:
            print("Invalid choice. Enter a number from the menu.")
 
 
if __name__ == "__main__":
    main()