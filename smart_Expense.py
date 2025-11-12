import json
import os
import time
from datetime import datetime
import calendar

EXPENSES_FILE = "expenses.json"
LOG_FILE = "app_log.txt"

def log_performance(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        print(f"\n Running {func.__name__}...")
        result = func(*args, **kwargs)
        end = time.time()
        duration = end - start
        log_line = f"Function '{func.__name__}' executed in {duration:.4f}s"
        Log_Message(log_line)
        print(f" {func.__name__} executed in {duration:.4f} seconds\n")
        return result
    return wrapper


def Log_Message(text: str):
    TimeStamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"{TimeStamp} {text}\n")



def load_expenses():
    if not os.path.exists(EXPENSES_FILE):
        with open(EXPENSES_FILE, "w") as f:
            json.dump([], f, ensure_ascii=False, indent=2)
    try:
        with open(EXPENSES_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, ValueError):
        backup = EXPENSES_FILE + ".bak"
        os.replace(EXPENSES_FILE, backup)
        print(f"[Warning] Corrupted {EXPENSES_FILE} moved to {backup}. Created a new one.")
        

def save_expenses(data):
    with open(EXPENSES_FILE, "w") as f:
        json.dump(data, f, indent=4)


@log_performance
def add_expense():
    date_input = input("Enter date (YYYY-MM-DD) [default: today]: ").strip()
    if not date_input:
        date_str = datetime.today().strftime("%Y-%m-%d")
    else:
        try:
            datetime.strptime(date_input, "%Y-%m-%d")
            date_str = date_input
        except ValueError:
            print(" Invalid date format. Use YYYY-MM-DD.")
            

    category = input("Enter category (e.g., Food, Travel, Shopping, Bills): ").strip()
    if category == "":
        category = "Default"
    amt_str = input("Enter amount:").strip()
    try:
        amount = float(amt_str)
    except ValueError:
        print(" Invalid amount.")
        return

    description = input("Enter description : ").strip() or ""

    record = {
        "date": date_str,
        "category": category,
        "amount": amount,
        "description": description or ""
    }

    data = load_expenses()
    data.append(record)
    save_expenses(data)
    print("-"*41)
    print(" Expense added successfully!\n")

@log_performance
def view_all_expenses():
    
    data = load_expenses()
    if not data:
        print("No expenses recorded yet.")
        return
    try:
        data.sort(key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d"))
    except Exception as e:
        print(f"Error sorting data: {e}")
        return

    print("\n--- All Expenses (Sorted by Date) ---")
    print(f"{'S.No':<5} {'Date':<12} {'Category':<15} {'Amount (₹)':>12} {'Description'}")
    print("-" * 65)

    total = 0.0
    for i, exp in enumerate(data, 1):
        date = exp.get("date", "")
        category = exp.get("category", "Misc")
        amount = float(exp.get("amount", 0.0))
        description = exp.get("description", "")
        total += amount

        # Formatted row
        print(f"{i:<5} {date:<12} {category:<15} {amount:>12.2f} {description}")

    print("-" * 65)
    print(f"{'Total Expenditure:':<34} ₹{total:.2f}")
    print(f"Total Records: {len(data)}")


@log_performance
def generate_monthly_summary():
    data = load_expenses()
    if not data:
        print("No expenses recorded yet.")
        return
    while True:
        summary_month =int(input("Enter the Month : "))
        summary_year  = int(input("Enter the Year (in yyyy formate): "))
        try:
            if not (1 <= summary_month <= 12):
                raise ValueError
            break
        except ValueError:
            print("Invalid month/year.")

    month_name = calendar.month_name[summary_month]

    summary_by_category = {}
    month_total = 0.0
    for e in data:
        try:
            e_date = datetime.strptime(e.get("date", ""), "%Y-%m-%d")
        except Exception:
            continue
        if e_date.month == summary_month and e_date.year == summary_year:
            cat = e.get("category", "Misc")
            amt = float(e.get("amount", 0.0))
            summary_by_category[cat] = summary_by_category.get(cat, 0.0) + amt
            month_total += amt


    print("\n--- Monthly Summary ---")
    if not summary_by_category:
            print("No expenses found for this month.")
    else:
            for cat, amt in summary_by_category.items():
                print(f"{cat}: ₹{amt:.2f}")
            print("-" * 41)
            print(f"Total: ₹{month_total:.2f}")
    

    save_summary = input("Do you want to save this summary as JSON? (y/n): ").strip().lower()
    if save_summary == "y":
        filename = f"summary_{summary_year}_{summary_month}.json"
        with open(filename, "w") as file:
            json.dump({
                "month": summary_month,
                "year": summary_year,
                "summary": summary_by_category,
                "total": month_total
            }, file, indent=4)
        print(f"Summary saved as {filename}")
        print("-"*30)


def main():
    print("\n ---------SMART EXPENSE TRACKER---------- ")
    while True:
        print("\n1. Add Expense")
        print("2. View All Expenses")
        print("3. Generate Monthly Summary")
        print("4. Exit")

        choice = input("\nEnter your choice (1-4): ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_all_expenses()
        elif choice == "3":
            generate_monthly_summary()
        elif choice == "4":
            print("Goodbye! ")
            break
        else:
            print(" Invalid choice. Please enter 1–4.")

if __name__ == "__main__":
    main()
