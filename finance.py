from database import connection, cursor


def add_income(current_user):

    print("\n===== ADD INCOME =====")

    source = input("Enter Income Source: ").strip()

    try:
        amount = float(input("Enter Amount: "))
    except ValueError:
        print("Invalid Amount!")
        return

    date = input("Enter Date (DD-MM-YYYY): ").strip()


    cursor.execute(
        """
        INSERT INTO transactions
        (user_email, type, source, category, amount, date)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            current_user["email"],
            "Income",
            source,
            "",
            amount,
            date
        )
    )

    connection.commit()

    print("\nIncome added successfully!")



def add_expense(current_user):

    print("\n===== ADD EXPENSE =====")

    category = input("Enter Expense Category: ").strip()

    try:
        amount = float(input("Enter Amount: "))
    except ValueError:
        print("Invalid Amount!")
        return

    date = input("Enter Date (DD-MM-YYYY): ").strip()


    cursor.execute(
        """
        INSERT INTO transactions
        (user_email, type, source, category, amount, date)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            current_user["email"],
            "Expense",
            "",
            category,
            amount,
            date
        )
    )

    connection.commit()

    print("\nExpense added successfully!")



def view_transactions(current_user):

    print("\n===== YOUR TRANSACTIONS =====")


    cursor.execute(
        """
        SELECT id, type, source, category, amount, date
        FROM transactions
        WHERE user_email = ?
        """,
        (current_user["email"],)
    )


    records = cursor.fetchall()


    if len(records) == 0:
        print("No transactions found.")
        return


    for record in records:

        print("-" * 40)
        print("ID:", record[0])
        print("Type:", record[1])

        if record[1] == "Income":
            print("Source:", record[2])
        else:
            print("Category:", record[3])

        print("Amount:", record[4])
        print("Date:", record[5])



def view_balance(current_user):

    cursor.execute(
        """
        SELECT type, amount
        FROM transactions
        WHERE user_email = ?
        """,
        (current_user["email"],)
    )


    records = cursor.fetchall()

    income = 0
    expense = 0


    for record in records:

        if record[0] == "Income":
            income += record[1]

        else:
            expense += record[1]


    print("\n===== BALANCE =====")
    print("Total Income :", income)
    print("Total Expense:", expense)
    print("Balance      :", income - expense)


def delete_transaction(current_user):

    print("\n===== DELETE TRANSACTION =====")

    view_transactions(current_user)

    try:
        transaction_id = int(input("\nEnter Transaction ID to delete: "))
    except ValueError:
        print("Invalid ID!")
        return


    cursor.execute(
        """
        DELETE FROM transactions
        WHERE id=? AND user_email=?
        """,
        (
            transaction_id,
            current_user["email"]
        )
    )


    connection.commit()


    if cursor.rowcount > 0:
        print("\nTransaction deleted successfully!")

    else:
        print("\nTransaction not found!")

def edit_transaction(current_user):

    print("\n===== EDIT TRANSACTION =====")

    view_transactions(current_user)

    try:
        transaction_id = int(input("\nEnter Transaction ID to edit: "))
    except ValueError:
        print("Invalid Transaction ID!")
        return

    try:
        new_amount = float(input("Enter New Amount: "))
    except ValueError:
        print("Invalid Amount!")
        return

    cursor.execute(
        """
        UPDATE transactions
        SET amount=?
        WHERE id=? AND user_email=?
        """,
        (
            new_amount,
            transaction_id,
            current_user["email"]
        )
    )

    connection.commit()

    if cursor.rowcount > 0:
        print("\nTransaction updated successfully!")
    else:
        print("\nTransaction not found!")
