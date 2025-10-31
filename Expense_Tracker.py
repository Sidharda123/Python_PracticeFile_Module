
def read_expenses(filename):
    records = []
    try:
        with open(filename, 'r') as file:
            for line_num, line in enumerate(file, start=1):
                parts = line.strip().split(',')
                if len(parts) != 3:
                    print(f" Skipping line {line_num}: {line.strip()}")
                    continue
                date, category, amount = parts
                try:
                    amount = float(amount)
                    records.append((date, category, amount))
                except ValueError:
                    print(f"Skipping line {line_num} due to invalid amount: {amount}")
                    continue
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return []
    return records


def calculate_summary(records):
    category_totals = {}
    day_totals = {}
    total_expense = 0

    for date, category, amount in records:
        total_expense += amount
        category_totals[category] = category_totals.get(category, 0) + amount
        day_totals[date] = day_totals.get(date, 0) + amount

    if day_totals:
        highest_day = max(day_totals, key=day_totals.get)
        highest_day_amount = day_totals[highest_day]
    else:
        highest_day, highest_day_amount = None, 0

    return {
        "total_expense": total_expense,
        "category_totals": category_totals,
        "highest_day": highest_day,
        "highest_day_amount": highest_day_amount
    }


def write_summary(summary, filename):
    with open(filename, 'w') as file:
        file.write("================= Expense Summary (October 2025) =================\n")
        file.write(f"Total Monthly Expense: ₹{int(summary['total_expense'])}\n\n")
        file.write("Category-wise Breakdown:\n")
        for category, amount in summary["category_totals"].items():
            file.write(f"{category:<15}: ₹{int(amount)}\n")
        file.write("\n")
        if summary["highest_day"]:
            file.write(f"Highest Spending Day: {summary['highest_day']} (₹{int(summary['highest_day_amount'])})\n")
        else:
            file.write("Highest Spending Day: N/A\n")
        file.write("=================================================================\n")
    print(f"Summary written to {filename}")

import os
def main():
    input_file = "Expense_Data.txt"
    output_file = "Expense.txt"
    records = read_expenses(input_file)
    if not records:
        print("No valid records to process.")
        return

    summary = calculate_summary(records)
    write_summary(summary, output_file)
    os.startfile(output_file)


