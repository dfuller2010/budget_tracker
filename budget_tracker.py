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
    pass
 
def view_month_expenses(data):
    pass
 
def delete_expense(data):
    pass
 
 
# -- Reports -------------------------------------------------------------------
 
def monthly_report(data):
    pass
 
 
# -- Main ----------------------------------------------------------------------
 
def main():
    pass
 
 
if __name__ == "__main__":
    main()