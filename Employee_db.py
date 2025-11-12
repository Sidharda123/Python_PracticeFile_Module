import sqlite3
from datetime import datetime

# Decorator for Logging Operations
def logging_info(func):
    def wrapper(*args, **kwargs):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        result = func(*args, **kwargs)

        log_entry = f"[{now}] Function {func.__name__} is Executed.\n"
        print(log_entry)
        with open("logs.txt", 'a') as file:
            file.write(log_entry)
        return result
    return wrapper


@logging_info
def create_connection(db_name):
    con = None
    try:
        con = sqlite3.connect(db_name)
        print(f"Connection Created Successfully for : {db_name}")
    except sqlite3.Error as e:
        print(f"Error occurred in Creating Connection: {e}")
    return con
# Returns the Connection Object


@logging_info
def create_table(con):
    try:
        cursor = con.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Employees(
                Emp_ID INTEGER PRIMARY KEY,
                Name TEXT NOT NULL,
                Department TEXT NOT NULL,
                Salary INTEGER NOT NULL
            )
        ''')
        con.commit()
        print("Employee Table Created Successfully")
    except sqlite3.Error as e:
        print(f"An error occurred while creating the Table: {e}")


@logging_info
def insert_data(con, Emp_ID, Name, Department, Salary):
    try:
        cursor = con.cursor()
        cursor.execute(
            "INSERT INTO Employees (Emp_ID, Name, Department, Salary) VALUES (?, ?, ?, ?)",
            (Emp_ID, Name, Department, Salary)
        )
        con.commit()
        print(f"Employee {Name}'s Details Added Successfully")
    except sqlite3.Error as e:
        print(f"Error occurred in adding Employee {Name}'s Data: {e}")


@logging_info
def fetch_full_data(con):
    try:
        cursor = con.cursor()
        cursor.execute("SELECT * FROM Employees")
        rows = cursor.fetchall()
        if rows:
            for row in rows:
                print(row)
        else:
            print("No Data Found")
            return
        print("All Employee Data Fetched Successfully")

    except sqlite3.Error as e:
        print(f"Error occurred while Fetching Data: {e}")


@logging_info
def fetch_specific_row(con, Emp_ID):
    try:
        cursor = con.cursor()
        cursor.execute("SELECT * FROM Employees WHERE Emp_ID = ?", (Emp_ID,))
        rows = cursor.fetchall()
        if rows:
            for row in rows:
                print(row)
        else:
            print("No Data Found for given Employee ID")
            return
        print("Employee Data Fetched Successfully")

    except sqlite3.Error as e:
        print(f"Error occurred while Fetching Data: {e}")


@logging_info
def update_data(con, Emp_ID, Name=None, Department=None, Salary=None):
    try:
        cursor = con.cursor()
        cursor.execute('''
            UPDATE Employees
            SET
                Name = COALESCE(?, Name),
                Department = COALESCE(?, Department),
                Salary = COALESCE(?, Salary)
            WHERE Emp_ID = ?
        ''', (Name, Department, Salary, Emp_ID))
        
        con.commit()
        if cursor.rowcount > 0:
            print(f"Employee with ID {Emp_ID} updated successfully.")
        else:
            print(f"No employee found with ID {Emp_ID}.")
    except sqlite3.Error as e:
        print(f"Error occurred while updating data: {e}")

@logging_info
def delete_data(con, Emp_ID):
    try:
        cursor = con.cursor()
        cursor.execute("DELETE FROM Employees WHERE Emp_ID = ?", (Emp_ID,))
        con.commit()
        print(f"Employee with ID {Emp_ID}'s Data Deleted Successfully")
    except sqlite3.Error as e:
        print(f"Error occurred while performing Delete operation: {e}")


# --- Example usage ---
if __name__ == "__main__":
    connection = create_connection("company.db")
    create_table(connection)

    insert_data(connection, 101, "John Doe", "HR", 45000)
    insert_data(connection, 102, "Jane Smith", "IT", 60000)

    fetch_full_data(connection)
    fetch_specific_row(connection, 102)

    update_data(connection, 101, Salary=50000)
    delete_data(connection, 102)

    fetch_full_data(connection)
