import csv
import os
from datetime import datetime

class ExpenseTracker:
    def __init__(self):
        self.categories = {
            'Food': ['Groceries', 'Dining Out'],
            'Transportation': ['Fuel', 'Public Transport'],
            'Housing': ['Rent', 'Utilities'],
            'Entertainment': ['Movies', 'Concerts'],
            'Others': ['Shopping', 'Miscellaneous']
        }
        self.monthly_budget = 0
        self.expenses = {}

    def load_budget(self, budget_file):
        if os.path.exists(budget_file):
            with open(budget_file, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.monthly_budget = float(row['Monthly Budget'])
        else:
            print("Budget file not found. Creating a new one.")

    def load_expenses(self, expenses_file):
        if os.path.exists(expenses_file):
            with open(expenses_file, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    date = datetime.strptime(row['Date'], '%d-%m-%Y').date()
                    if date not in self.expenses:
                        self.expenses[date] = {}
                    category = row['Category']
                    subcategory = row['Subcategory']
                    amount = float(row['Amount'])
                    if category not in self.expenses[date]:
                        self.expenses[date][category] = {}
                    if subcategory not in self.expenses[date][category]:
                        self.expenses[date][category][subcategory] = amount
                    else:
                        self.expenses[date][category][subcategory] += amount
        else:
            print("Expenses file not found. Creating a new one.")

    def record_expense(self):
        print("Categories:")
        for i, category in enumerate(self.categories.keys(), 1):
            print(f"{i}. {category}")
        category_choice = int(input("Choose a category: "))
        category_list = list(self.categories.keys())
        category = category_list[category_choice - 1]
        subcategories = self.categories[category]
        print(f"Subcategories for {category}:")
        for i, subcategory in enumerate(subcategories, 1):
            print(f"{i}. {subcategory}")
        subcategory_choice = int(input("Choose a subcategory: "))
        subcategory = subcategories[subcategory_choice - 1]
        amount = float(input("Enter amount: "))
        
        today = datetime.today().date()
        if today not in self.expenses:
            self.expenses[today] = {}
        if category not in self.expenses[today]:
            self.expenses[today][category] = {}
        if subcategory not in self.expenses[today][category]:
            self.expenses[today][category][subcategory] = amount
        else:
            self.expenses[today][category][subcategory] += amount
        print("Expense recorded successfully.")

    def save_expenses(self, expenses_file):
        with open(expenses_file, 'w', newline='') as file:
            fieldnames = ['Date', 'Category', 'Subcategory', 'Amount']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for date, categories in self.expenses.items():
                for category, subcategories in categories.items():
                    for subcategory, amount in subcategories.items():
                        writer.writerow({'Date': date.strftime('%d-%m-%Y'),
                                         'Category': category,
                                         'Subcategory': subcategory,
                                         'Amount': amount})

    def set_monthly_budget(self, amount):
        self.monthly_budget = amount
        print("Monthly budget set successfully.")

    def show_monthly_budget(self):
        print(f"Monthly Budget: ${self.monthly_budget}")

    def show_expenses(self):
        print("Expenses:")
        for date, categories in self.expenses.items():
            print(f"On {date.strftime('%d-%m-%Y')}:")
            for category, subcategories in categories.items():
                print(f" {category}:")
                for subcategory, amount in subcategories.items():
                    print(f"  - {subcategory}: ${amount}")

    def calculate_savings(self, month_year):
        savings = 0
        for date, categories in self.expenses.items():
            if date.strftime('%m-%Y') == month_year:
                for category, subcategories in categories.items():
                    for subcategory, amount in subcategories.items():
                        savings += amount
        return self.monthly_budget - savings

# Example Usage:

def main():
    tracker = ExpenseTracker()
    budget_file = "budget.csv"
    expenses_file = "expenses.csv"

    # Load existing data
    tracker.load_budget(budget_file)
    tracker.load_expenses(expenses_file)

    # Display Menu
    while True:
        print("\nExpense Tracker Menu:")
        print("1. Record Expense")
        print("2. Set Monthly Budget")
        print("3. Show Monthly Budget")
        print("4. Show Monthly Expenses")
        print("5. Calculate Savings")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            tracker.record_expense()
            tracker.save_expenses(expenses_file)
        elif choice == '2':
            amount = float(input("Enter monthly budget amount: "))
            tracker.set_monthly_budget(amount)
        elif choice == '3':
            tracker.show_monthly_budget()
        elif choice == '4':
            tracker.show_expenses()
        elif choice == '5':
            month_year = input("Enter month and year (MM-YYYY): ")
            savings = tracker.calculate_savings(month_year)
            print(f"Savings for {month_year}: ${savings}")
        elif choice == '6':
            tracker.save_expenses(expenses_file)
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()
#by- Anuvrat Deswal

