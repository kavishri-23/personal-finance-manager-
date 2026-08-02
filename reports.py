from database import connection, cursor
import csv


def search_transactions(current_user):

    print("\n===== SEARCH TRANSACTIONS =====")

    keyword = input("Enter category/source to search: ").strip()


    cursor.execute(
        """
        SELECT type, source, category, amount, date
        FROM transactions
        WHERE user_email=?
        AND (source LIKE ? OR category LIKE ?)
        """,
        (
            current_user["email"],
            "%" + keyword + "%",
            "%" + keyword + "%"
        )
    )


    records = cursor.fetchall()


    if len(records) == 0:
        print("No transactions found.")
        return


    for row in records:
        print("-" * 40)
        print("Type:", row[0])
        print("Source:", row[1])
        print("Category:", row[2])
        print("Amount:", row[3])
        print("Date:", row[4])



def export_to_csv(current_user):

    print("\n===== EXPORT TRANSACTIONS =====")

    cursor.execute(
        """
        SELECT type, source, category, amount, date
        FROM transactions
        WHERE user_email=?
        """,
        (current_user["email"],)
    )


    records = cursor.fetchall()


    if len(records) == 0:
        print("No transactions to export.")
        return


    with open("transactions.csv", "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow(
            [
                "Type",
                "Source",
                "Category",
                "Amount",
                "Date"
            ]
        )

        writer.writerows(records)


    print("Export completed successfully!")



def monthly_report(current_user):

    print("\n===== MONTHLY REPORT =====")

    month = input("Enter month (MM): ")

    cursor.execute(
        """
        SELECT type, SUM(amount)
        FROM transactions
        WHERE user_email=?
        AND date LIKE ?
        GROUP BY type
        """,
        (
            current_user["email"],
            "%-" + month + "-%"
        )
    )


    records = cursor.fetchall()


    if len(records) == 0:
        print("No records found.")
        return


    for row in records:
        print(row[0], ":", row[1])



def expense_summary(current_user):

    print("\n===== EXPENSE SUMMARY =====")


    cursor.execute(
        """
        SELECT category, SUM(amount)
        FROM transactions
        WHERE user_email=?
        AND type='Expense'
        GROUP BY category
        """,
        (current_user["email"],)
    )


    records = cursor.fetchall()


    if len(records) == 0:
        print("No expense records found.")
        return


    total = 0


    for category, amount in records:

        print(category, ":", amount)
        total += amount


    print("------------------------")
    print("Total Expense:", total)
