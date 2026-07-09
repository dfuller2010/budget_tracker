"""
Simple terminal-based budget tracker.

Features:
- store categories and expenses in `expenses.json`
- add/view/delete expenses
- add categories and run a monthly report

This module is lightweight and uses plain JSON for persistence so it
is easy to inspect or migrate later.
"""

import json
import os
from datetime import datetime
 
 
# -- Data ----------------------------------------------------------------------
 
def load_data():
    """Load budget data from `expenses.json` if it exists.

    Returns a dict with keys `categories` and `expenses`.
    If the file does not exist a default structure is returned.
    """
    if os.path.exists("expenses.json"):
        with open("expenses.json", "r") as f:
            return json.load(f)
    # Default dataset when no file is present
    return {
        "categories": ["Food", "Transport", "Bills", "Entertainment", "Other"],
        "expenses": []
    }
 
def save_data(data):
    """Persist the given data dictionary to `expenses.json`.

    Uses a human-readable JSON indent for easier manual edits.
    """
    with open("expenses.json", "w") as f:
        json.dump(data, f, indent=2)
 
 
# -- Categories ----------------------------------------------------------------
 
def get_categories(data):
    """Return the list of category names from the data dict."""
    return data["categories"]
 
def add_category(data):
    """Prompt the user to add a new category and save it.

    Normalizes the name with `title()` and avoids duplicates.
    """
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
    """Interactively collect expense fields and append to data.

    Validates amount and date formats, then saves the data file.
    """
    categories = get_categories(data)

    # Amount: require a positive float
    while True:
        try:
            amount = float(input("\nAmount: $"))
            if amount <= 0:
                print("Amount must be greater than zero.")
                continue
            break
        except ValueError:
            print("Please enter a number.")

    # Category: present numbered choices
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

    # Description: free-form text
    description = input("Description: ").strip()

    # Date: allow empty input to use today's date; validate format otherwise
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

    # Construct and persist the new expense
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
    """Print all recorded expenses in a simple list.

    Tries to sort by date, then amount (descending) for readability.
    """
    expenses = data.get("expenses", [])
    if not expenses:
        print("\nNo expenses recorded.")
        return data

    # Sort by date then amount (descending)
    try:
        sorted_expenses = sorted(expenses, key=lambda e: (e.get("date", ""), -float(e.get("amount", 0))))
    except Exception:
        # If any expense records are malformed, fall back to unsorted
        sorted_expenses = list(expenses)

    # Display each expense with an index for possible deletion
    print()
    for i, e in enumerate(sorted_expenses, 1):
        amt = float(e.get("amount", 0))
        cat = e.get("category", "")
        desc = e.get("description", "")
        date = e.get("date", "")
        print(f"{i}. {date} | {cat} | ${amt:.2f} | {desc}")
    return data
 
def view_month_expenses(data):
    """Show expenses filtered to a specific month (YYYY-MM).

    If the user presses Enter the current month is used.
    Prints each matching expense and a monthly total.
    """
    from datetime import datetime as _dt
    today = _dt.today()
    default = today.strftime("%Y-%m")
    month_input = input(f"Show month (YYYY-MM) [press Enter for {default}]: ").strip()
    if month_input == "":
        month = default
    else:
        try:
            # Validate that the input represents a valid month
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
    """Delete an expense by its displayed index.

    Shows all expenses first so the user can choose the correct one.
    Press Enter to cancel deletion.
    """
    expenses = data.get("expenses", [])
    if not expenses:
        print("\nNo expenses to delete.")
        return data

    # Show existing expenses with indices
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
    """Aggregate expenses by category for a given month and print totals.

    Prompts for a month in `YYYY-MM` format and prints a simple report.
    """
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

    # Sum amounts per category for the requested month
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
    """Main interactive loop for the budget tracker CLI.

    Loads data, presents a simple numeric menu, and dispatches actions.
    """
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