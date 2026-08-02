import sqlite3
import csv
from database import connection, cursor
from auth import register, login,change_password,update_profile
from finance import (
    add_income,
    add_expense,
    view_transactions,
    view_balance,
    delete_transaction,
    edit_transaction
)

from reports import (
    search_transactions,
    export_to_csv,
    monthly_report,
    expense_summary
)
users = []
transactions = []
current_user = None

def show_menu():
    print("\n" + "=" * 40)
    print("    PERSONAL FINANCE MANAGER")
    print("=" * 40)
    print("1. Register")
    print("2. Login")
    print("3. About")
    print("4. View Registered Users")
    print("5. Exit")

        
def dashboard(current_user):

    while True:
        print("\n" + "=" * 40)
        print(f"Welcome, {current_user['name']}")
        print("=" * 40)
        print("         DASHBOARD")
        print("=" * 40)
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Transactions")
        print("4. View Balance")
        print("5. Delete Transaction")
        print("6. Edit Transaction")
        print("7. Search Transactions")
        print("8. Export to CSV")
        print("9. Monthly Report")
        print("10. Expense Summary")
        print("11. Change Password")
        print("12. Update Profile")
        print("13. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_income(current_user)

        elif choice == "2":
            add_expense(current_user)

        elif choice == "3":
            view_transactions(current_user)

        elif choice == "4":
            view_balance(current_user)

        elif choice == "5":
            delete_transaction(current_user)

        elif choice == "6":
            edit_transaction(current_user)

        elif choice == "7":
            search_transactions(current_user)

        elif choice == "8":
            export_to_csv(current_user)

        elif choice == "9":
            monthly_report(current_user)

        elif choice == "10":
            expense_summary(current_user)
        elif choice == "11":
            change_password(current_user)
        elif choice == "12":
            update_profile(current_user)

        elif choice == "13":
            print("\nLogged out successfully!")
            break

        else:
            print("Invalid Choice")


def search_transactions(current_user):
   

    print("\n===== SEARCH TRANSACTIONS =====")

    keyword = input("Enter keyword: ").strip()

    cursor.execute(
        """
        SELECT id, type, source, category, amount, date
        FROM transactions
        WHERE user_email = ?
        AND (
            source LIKE ?
            OR category LIKE ?
            OR type LIKE ?
        )
        """,
        (
            current_user["email"],
            "%" + keyword + "%",
            "%" + keyword + "%",
            "%" + keyword + "%"
        )
    )

    records = cursor.fetchall()

    if len(records) == 0:
        print("\nNo matching transactions found.")
        return

    for record in records:

        transaction_id = record[0]
        transaction_type = record[1]
        source = record[2]
        category = record[3]
        amount = record[4]
        date = record[5]

        print("-" * 40)
        print("ID      :", transaction_id)
        print("Type    :", transaction_type)

        if transaction_type == "Income":
            print("Source  :", source)
        else:
            print("Category:", category)

        print("Amount  :", amount)
        print("Date    :", date)

    print("-" * 40)
def export_to_csv(current_user):
   

    cursor.execute(
        """
        SELECT type, source, category, amount, date
        FROM transactions
        WHERE user_email = ?
        """,
        (current_user["email"],)
    )

    records = cursor.fetchall()

    if len(records) == 0:
        print("\nNo transactions to export.")
        return

    filename = current_user["email"].replace("@", "_") + "_transactions.csv"

    with open(filename, "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow(["Type", "Source", "Category", "Amount", "Date"])

        writer.writerows(records)

    print(f"\nTransactions exported successfully to '{filename}'")

def monthly_report(current_user):
   

    print("\n===== MONTHLY REPORT =====")

    month = input("Enter Month (MM): ").strip()
    year = input("Enter Year (YYYY): ").strip()

    total_income = 0
    total_expense = 0

    cursor.execute(
        """
        SELECT type, amount
        FROM transactions
        WHERE user_email = ?
        """,
        (current_user["email"],)
    )

    records = cursor.fetchall()

    for record in records:

        transaction_type = record[0]
        amount = record[1]

        cursor.execute(
            """
            SELECT date
            FROM transactions
            WHERE user_email = ?
            AND type = ?
            AND amount = ?
            """,
            (
                current_user["email"],
                transaction_type,
                amount
            )
        )

        date = cursor.fetchone()[0]

        parts = date.split("-")

        if len(parts) != 3:
            continue

        if parts[1] == month and parts[2] == year:

            if transaction_type == "Income":
                total_income += amount
            else:
                total_expense += amount

    balance = total_income - total_expense

    print("\n" + "=" * 40)
    print("MONTHLY FINANCIAL REPORT")
    print("=" * 40)
    print(f"Total Income : ₹{total_income}")
    print(f"Total Expense: ₹{total_expense}")
    print("-" * 40)
    print(f"Balance      : ₹{balance}")

def expense_summary(currennt_user):
   
    print("\n===== EXPENSE SUMMARY =====")

    cursor.execute(
        """
        SELECT category, SUM(amount)
        FROM transactions
        WHERE user_email = ?
        AND type = 'Expense'
        GROUP BY category
        """,
        (current_user["email"],)
    )

    records = cursor.fetchall()

    if len(records) == 0:
        print("No expense records found.")
        return

    print("-" * 35)

    total = 0

    for category, amount in records:
        print(f"{category:<15} ₹{amount}")
        total += amount

    print("-" * 35)
    print(f"Total Expense : ₹{total}")

while True:

    show_menu()

    choice = input("\nEnter your choice: ")

    if choice == "1":
        register()

    elif choice == "2":

        current_user = login()

        if current_user:
            dashboard(current_user)

    elif choice == "3":
        print("\nPersonal Finance Manager")
        print("Version 1.0")
        print("Developed by Kavi")

    elif choice == "4":

        print("\nRegistered users are stored in database.")

    elif choice == "5":
        print("\nThank you for using Personal Finance Manager.")
        break

    else:
        print("\nInvalid choice. Please try again.")

