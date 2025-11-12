

import json
import os
import time
from datetime import datetime, date
import calendar
from functools import wraps

EXPENSES_FILE = "expenses.json"
LOG_FILE = "app_log.txt"


def ensure_files():
    if not os.path.exists(EXPENSES_FILE):
        with open(EXPENSES_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)
    else:
        try:
            with open(EXPENSES_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, list):
                raise ValueError("expenses.json root is not a list")
        except (json.JSONDecodeError, ValueError):
            backup = EXPENSES_FILE + ".bak"
            try:
                os.replace(EXPENSES_FILE, backup)
                print(f"[Warning] Corrupted {EXPENSES_FILE} moved to {backup}. Created a new empty {EXPENSES_FILE}.")
            except Exception:
                print(f"[Warning] Could not create backup of corrupted {EXPENSES_FILE}. Overwriting.")
            with open(EXPENSES_FILE, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)


def log_message(text: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} {text}\n")


def log_and_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_dt = datetime.now()
        start_ts = time.perf_counter()
        print(f"[{start_dt.strftime('%Y-%m-%d %H:%M:%S')}] Starting '{func.__name__}'...")
        result = None
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            end_ts = time.perf_counter()
            duration = end_ts - start_ts
            log_line = f"Function '{func.__name__}' executed in {duration:.4f}s"
            log_message(log_line)
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {log_line}")
    return wrapper


def load_expenses():
    ensure_files()
    with open(EXPENSES_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            if not isinstance(data, list):
                return []
            return data
        except json.JSONDecodeError:
            return []


def save_expenses(expenses):
    with open(EXPENSES_FILE, "w", encoding="utf-8") as f:
        json.dump(expenses, f, ensure_ascii=False, indent=2)


@log_and_time
def add_expense():
    expenses = load_expenses()

    while True:
        raw_date = input("Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
        if raw_date == "":
            expense_date = date.today().strftime("%Y-%m-%d")
            break
        else:
            try:
                dt = datetime.strptime(raw_date, "%Y-%m-%d")
                expense_date = dt.strftime("%Y-%m-%d")
                break
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD (e.g., 2025-11-04).")

    category = input("Enter category (e.g., Food, Travel, Shopping, Bills): ").strip()
    if category == "":
        category = "Misc"

    while True:
        amt_str = input("Enter amount: ").strip()
        try:
            amount = float(amt_str)
            if amount < 0:
                print("Amount cannot be negative. Please enter a positive number.")
                continue
            break
        except ValueError:
            print("Invalid amount. Please enter a numeric value (e.g., 350 or 350.50).")

    description = input("Enter description (optional): ").strip()

    entry = {
        "date": expense_date,
        "category": category,
        "amount": round(amount, 2),
        "description": description,
    }

    expenses.append(entry)
    save_expenses(expenses)
    print("✅ Expense added successfully!")


@log_and_time
def view_expenses():
    expenses = load_expenses()
    if not expenses:
        print("No expenses recorded yet.")
        return

    def parse_date(e):
        try:
            return datetime.strptime(e.get("date", ""), "%Y-%m-%d")
        except Exception:
            return datetime.min

    expenses_sorted = sorted(expenses, key=parse_date)

    print("-" * 72)
    print(f"{'Date':<12} | {'Category':<15} | {'Amount':>10} | Description")
    print("-" * 72)
    total = 0.0
    for e in expenses_sorted:
        d = e.get("date", "")
        c = e.get("category", "")
        a = e.get("amount", 0.0)
        desc = e.get("description", "")
        total += float(a or 0.0)
        print(f"{d:<12} | {c:<15} | {a:10.2f} | {desc}")
    print("-" * 72)
    print(f"{'Total':<12} | {'':<15} | {total:10.2f}")
    print("-" * 72)


@log_and_time
def generate_monthly_summary(export=False):
    
    expenses = load_expenses()
    if not expenses:
        print("No expenses recorded yet.")
        return

    while True:
        raw = input("Enter month and year (MM YYYY) e.g., 11 2025: ").strip()
        parts = raw.split()
        if len(parts) != 2:
            print("Please enter month and year like: MM YYYY (e.g., 11 2025)")
            continue
        mm_str, yyyy_str = parts
        try:
            mm = int(mm_str)
            yyyy = int(yyyy_str)
            if not (1 <= mm <= 12):
                raise ValueError
            break
        except ValueError:
            print("Invalid month/year. Example input: 11 2025")

    month_name = calendar.month_name[mm]

    summary_by_category = {}
    month_total = 0.0
    for e in expenses:
        try:
            e_date = datetime.strptime(e.get("date", ""), "%Y-%m-%d")
        except Exception:
            continue
        if e_date.month == mm and e_date.year == yyyy:
            cat = e.get("category", "Misc")
            amt = float(e.get("amount", 0.0))
            summary_by_category[cat] = summary_by_category.get(cat, 0.0) + amt
            month_total += amt

    print()
    header = f" Monthly Summary: {month_name} {yyyy} "
    print(header)
    if not summary_by_category:
        print("No expenses found for this month.")
    else:
        for cat, amt in summary_by_category.items():
            print(f"{cat}: ₹{amt:.2f}")
        print("-" * 41)
        print(f"Total: ₹{month_total:.2f}")

def main_menu():
    ensure_files()
    menu = """
------- Smart Expense Tracker =====
1. Add Expense
2. View All Expenses
3. Generate Monthly Summary
4. Exit
--------
"""
    while True:
        print(menu)
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            generate_monthly_summary()
        elif choice == "4":
            print("Goodbye — expenses saved to", EXPENSES_FILE)
            break
        else:
            print("Invalid choice. Please enter 1-4.")


