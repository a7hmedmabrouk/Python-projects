from expenses import Expense
import calendar
import datetime
import random

def main():
    print(f"📌 Runing Expense Tracking App")
    expenses_file_path = "G:\programming\AI Course\PProjects\Expense Tracking App\expense.csv"
    budget = 5000

    #generate_random_expenses(expenses_file_path, 1000)
    
    main_menu(expenses_file_path, budget)

def main_menu(expenses_file_path, budget):
    while True:
        print("Choose an option:")
        print("     1. Add Expense")
        print("     2. Show Expense Summary")
        print("     3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_expense(expenses_file_path)
        elif choice == "2":
            show_expense_summary_menu(expenses_file_path, budget)
        elif choice == "3":
            print("Exiting the app. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 3.")

def add_expense(expenses_file_path):
    expense = geting_user_expense()
    saveing_data_to_file(expense, expenses_file_path)
    print(green("Expense added successfully!"))

def geting_user_expense():
    print(f"📄 Geting user expense")
    expense_name = input("Enter the name of expense: ")
    expense_amount = float(input("Enter the amount of expense: "))   
    ##categoray i want him to choose first if he want to choose from the categorys or add new one 
    expense_category = ["🍔 Food", "🏡 Home", "🚌 Transportaion", "📖 Learning", "😜 Fun", "🚧 Others"]

    while True:
        print("please select a category: ")
        for i, categoryName in enumerate(expense_category):
            print(f"    {i+1}. {categoryName}")

        value_range = f"[{1} - {len(expense_category)}]"
        selected_index = int(input(f"Enter the category number {value_range}:")) - 1

        if selected_index in range(len(expense_category)):
            selected_category = expense_category[selected_index]
            new_expence = Expense(name = expense_name, category = selected_category, amount = expense_amount)
            return new_expence
        else:
            print("Invaled category number, please enter valid number: ")

def saveing_data_to_file(expense: Expense, expenses_file_path):
    with open(expenses_file_path, "a", encoding="utf-8") as f:
        f.write(f"{expense.name},{expense.category},{expense.amount}\n")  

def show_expense_summary_menu(expenses_file_path, budget):
    while True:
        print("Choose an option:")
        print("     1. Expense by category")
        print("     2. Total spent")
        print("     3. Remaining budget")
        print("     4. Budget per day and remaining days")
        print("     5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            summarize_expense_by_category(expenses_file_path)
        elif choice == "2":
            summarize_total_spent(expenses_file_path)
        elif choice == "3":
            summarize_remaining_budget(expenses_file_path, budget)
        elif choice == "4":
            summarize_budget_per_day_and_remaining_days(expenses_file_path, budget)
        elif choice == "5":
            print("Exiting the app. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 5.")

def summarize_expense_by_category(expenses_file_path):
    expenses = load_expenses(expenses_file_path)
    amount_by_category = {}
    for expense in expenses:
        key = expense.category
        amount_by_category[key] = amount_by_category.get(key, 0) + expense.amount

    print("Expense by category 💵")
    for category, amount in amount_by_category.items():
        print(green(f"    {category}: ${amount:.2f}"))

def summarize_total_spent(expenses_file_path):
    expenses = load_expenses(expenses_file_path)
    total_spent = sum(expense.amount for expense in expenses)
    print(red(f"🙁 Total Spent: ${total_spent:.2f}"))

def summarize_remaining_budget(expenses_file_path, budget):
    expenses = load_expenses(expenses_file_path)
    total_spent = sum(expense.amount for expense in expenses)
    remaining_budget = budget - total_spent
    print(green(f"🤑 Remaining Budget: ${remaining_budget:.2f}"))

def summarize_budget_per_day_and_remaining_days(expenses_file_path, budget):
    remaining_days = Get_Days_left_in_month()
    expenses = load_expenses(expenses_file_path)
    total_spent = sum(expense.amount for expense in expenses)
    remaining_budget = budget - total_spent
    daily_budget = remaining_budget / remaining_days
    print(green(f"👉 Budget per Day: ${daily_budget:.2f}, remaining days: {remaining_days}"))

def load_expenses(expenses_file_path):
    expenses = []
    with open(expenses_file_path, "r", encoding="utf-8") as f:
        for line in f:
            name, category, amount = line.strip().split(",")
            expenses.append(Expense(name=name, category=category, amount=float(amount)))
    return expenses

def Get_Days_left_in_month():
    now = datetime.datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    remaining_days = days_in_month - now.day
    return remaining_days

def green(text):
    return f"\033[92m{text}\033[0m"

def red(text):
    return f"\033[91m{text}\033[0m"

# Function to generate random expenses
def generate_random_expenses(file_path, num_expenses):
    categories = ["🍔 Food", "🏡 Home", "🚌 Transportaion", "📖 Learning", "😜 Fun", "🚧 Others"]
    with open(file_path, "a", encoding="utf-8") as f:
        for _ in range(num_expenses):
            name = f"Expense_{random.randint(1, 1000)}"
            category = random.choice(categories)
            amount = round(random.uniform(1, 100), 2)  # Generating random amount between 1 and 1000
            f.write(f"{name},{category},{amount}\n")

if __name__ == "__main__":
    main()