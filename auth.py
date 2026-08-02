from database import connection, cursor


current_user = None


def register():

    print("\n===== USER REGISTRATION =====")

    name = input("Enter your name: ").strip()
    email = input("Enter your email: ").strip()
    password = input("Enter your password: ").strip()

    if name == "":
        print("Name cannot be empty!")
        return

    if email == "":
        print("Email cannot be empty!")
        return

    if password == "":
        print("Password cannot be empty!")
        return

    try:
        cursor.execute(
            """
            INSERT INTO users(name, email, password)
            VALUES (?, ?, ?)
            """,
            (name, email, password)
        )

        connection.commit()

        print("\nRegistration Successful!")

    except Exception:
        print("\nAn account with this email already exists.")



def login():
    global current_user

    print("\n===== LOGIN =====")

    email = input("Enter email: ").strip()
    password = input("Enter password: ").strip()


    cursor.execute(
        """
        SELECT name, email, password
        FROM users
        WHERE email = ?
        AND password = ?
        """,
        (email, password)
    )


    user = cursor.fetchone()


    if user:

        current_user = {
            "name": user[0],
            "email": user[1],
            "password": user[2]
        }

        print("\nLogin Successful!")
        print("Welcome,", current_user["name"])

        return current_user


    else:
        print("\nInvalid Email or Password")
        return None

from database import connection, cursor

def change_password(current_user):

    print("\n===== CHANGE PASSWORD =====")

    old_password = input("Enter Current Password: ").strip()

    cursor.execute(
        """
        SELECT password
        FROM users
        WHERE email = ?
        """,
        (current_user["email"],)
    )

    password = cursor.fetchone()

    if password[0] != old_password:
        print("\nCurrent password is incorrect!")
        return

    new_password = input("Enter New Password: ").strip()
    confirm_password = input("Confirm New Password: ").strip()

    if new_password == "":
        print("Password cannot be empty!")
        return

    if new_password != confirm_password:
        print("Passwords do not match!")
        return

    cursor.execute(
        """
        UPDATE users
        SET password = ?
        WHERE email = ?
        """,
        (
            new_password,
            current_user["email"]
        )
    )

    connection.commit()

    print("\nPassword changed successfully!")

from database import connection, cursor

def update_profile(current_user):

    print("\n===== UPDATE PROFILE =====")

    new_name = input("Enter New Name: ").strip()

    if new_name == "":
        print("Name cannot be empty!")
        return

    cursor.execute(
        """
        UPDATE users
        SET name = ?
        WHERE email = ?
        """,
        (
            new_name,
            current_user["email"]
        )
    )

    connection.commit()

    current_user["name"] = new_name

    print("\nProfile updated successfully!")
