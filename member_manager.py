from config import MEMBER_FILE
from storage import load_data, save_data, next_id
from utils import read_text, valid_email, print_table


def add_member():
    members = load_data(MEMBER_FILE)

    print("\n--- Register Library Member ---")
    name = read_text("Full name: ")
    email = read_text("Email address: ").lower()
    phone = read_text("Phone number: ")

    if not valid_email(email):
        print("Enter a valid email address.")
        return

    if not phone.isdigit() or not 10 <= len(phone) <= 15:
        print("Phone number must contain 10 to 15 digits.")
        return

    if any(m["email"].casefold() == email.casefold() for m in members):
        print("This email address is already registered.")
        return

    if any(m["phone"] == phone for m in members):
        print("This phone number is already registered.")
        return

    member = {
        "id": next_id(members),
        "name": name,
        "email": email,
        "phone": phone,
        "active": True
    }

    members.append(member)
    save_data(MEMBER_FILE, members)

    print(f"Member registered successfully. Member ID: {member['id']}")


def list_members():
    members = load_data(MEMBER_FILE)

    print_table(
        ["ID", "Name", "Email", "Phone", "Status"],
        [
            [
                m["id"], m["name"], m["email"], m["phone"],
                "Active" if m["active"] else "Inactive"
            ]
            for m in members
        ]
    )


def get_member(member_id):
    return next(
        (
            m for m in load_data(MEMBER_FILE)
            if m["id"] == member_id and m["active"]
        ),
        None
    )


def member_menu():
    while True:
        print("\n--- Member Management ---")
        print("1. Register member")
        print("2. View members")
        print("0. Back")

        choice = input("Choose: ").strip()

        if choice == "1":
            add_member()
        elif choice == "2":
            list_members()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")
