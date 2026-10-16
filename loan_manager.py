from datetime import date, timedelta

from config import (
    BOOK_FILE,
    MEMBER_FILE,
    LOAN_FILE,
    LOAN_PERIOD_DAYS,
    FINE_PER_DAY,
    MAX_ACTIVE_LOANS_PER_MEMBER
)
from storage import load_data, save_data, next_id
from book_manager import get_book
from member_manager import get_member
from utils import read_positive_int, money, print_table, timestamp


def issue_book():
    print("\n--- Issue Book ---")

    member_id = read_positive_int("Member ID: ")
    member = get_member(member_id)

    if not member:
        print("Active member not found.")
        return

    book_id = read_positive_int("Book ID: ")
    book = get_book(book_id)

    if not book:
        print("Active book not found.")
        return

    if book["available_copies"] < 1:
        print("No copies of this book are currently available.")
        return

    loans = load_data(LOAN_FILE)

    active_member_loans = [
        loan for loan in loans
        if loan["member_id"] == member_id
        and loan["status"] == "Issued"
    ]

    if len(active_member_loans) >= MAX_ACTIVE_LOANS_PER_MEMBER:
        print(
            f"A member can have at most "
            f"{MAX_ACTIVE_LOANS_PER_MEMBER} active loans."
        )
        return

    loan = {
        "id": next_id(loans),
        "member_id": member_id,
        "book_id": book_id,
        "issue_date": date.today().isoformat(),
        "due_date": (
            date.today() + timedelta(days=LOAN_PERIOD_DAYS)
        ).isoformat(),
        "return_date": None,
        "fine": 0.0,
        "fine_paid": False,
        "status": "Issued",
        "created_at": timestamp()
    }

    # Save the loan before reducing the available copy count.
    loans.append(loan)
    save_data(LOAN_FILE, loans)

    try:
        books = load_data(BOOK_FILE)

        for stored_book in books:
            if stored_book["id"] == book_id:
                if stored_book["available_copies"] < 1:
                    raise ValueError("No copies remain available.")

                stored_book["available_copies"] -= 1
                break
        else:
            raise ValueError("Book was not found.")

        save_data(BOOK_FILE, books)

    except Exception:
        loans.pop()
        save_data(LOAN_FILE, loans)
        raise

    print("Book issued successfully.")
    print(f"Loan ID: {loan['id']}")
    print(f"Due date: {loan['due_date']}")


def calculate_fine(due_date, return_date):
    overdue_days = max(
        0,
        (return_date - date.fromisoformat(due_date)).days
    )
    return overdue_days * FINE_PER_DAY


def return_book():
    print("\n--- Return Book ---")

    loan_id = read_positive_int("Loan ID: ")
    loans = load_data(LOAN_FILE)

    loan = next(
        (
            item for item in loans
            if item["id"] == loan_id and item["status"] == "Issued"
        ),
        None
    )

    if not loan:
        print("Active loan not found.")
        return

    return_date = date.today()
    fine = calculate_fine(loan["due_date"], return_date)

    loan["return_date"] = return_date.isoformat()
    loan["fine"] = round(fine, 2)
    loan["fine_paid"] = fine == 0
    loan["status"] = "Returned"
    loan["returned_at"] = timestamp()

    # Save loan history before updating inventory.
    save_data(LOAN_FILE, loans)

    books = load_data(BOOK_FILE)

    for book in books:
        if book["id"] == loan["book_id"]:
            book["available_copies"] += 1
            break

    save_data(BOOK_FILE, books)

    print("Book returned successfully.")
    print(f"Overdue fine: {money(fine)}")

    if fine > 0:
        print("Fine status: Pending")
        print("Use the fine payment option after collecting the amount.")
    else:
        print("No fine is due.")


def pay_fine():
    print("\n--- Pay Overdue Fine ---")

    loan_id = read_positive_int("Loan ID: ")
    loans = load_data(LOAN_FILE)

    loan = next(
        (
            item for item in loans
            if item["id"] == loan_id
            and item["status"] == "Returned"
            and float(item["fine"]) > 0
        ),
        None
    )

    if not loan:
        print("No returned loan with a fine was found.")
        return

    if loan["fine_paid"]:
        print("This fine has already been paid.")
        return

    print(f"Fine amount: {money(loan['fine'])}")
    confirm = input("Confirm full payment? (yes/no): ").strip().lower()

    if confirm != "yes":
        print("Payment cancelled.")
        return

    loan["fine_paid"] = True
    loan["fine_paid_at"] = timestamp()
    save_data(LOAN_FILE, loans)

    print("Fine payment recorded successfully.")


def list_loans(status_filter=None):
    loans = load_data(LOAN_FILE)
    members = {
        m["id"]: m["name"]
        for m in load_data(MEMBER_FILE)
    }
    books = {
        b["id"]: b["title"]
        for b in load_data(BOOK_FILE)
    }

    rows = []

    for loan in loans:
        if status_filter and loan["status"] != status_filter:
            continue

        rows.append([
            loan["id"],
            members.get(loan["member_id"], "Unknown"),
            books.get(loan["book_id"], "Unknown"),
            loan["issue_date"],
            loan["due_date"],
            loan["return_date"] or "-",
            loan["status"],
            money(loan["fine"]),
            "Paid" if loan["fine_paid"] else (
                "Pending" if loan["fine"] > 0 else "-"
            )
        ])

    print_table(
        [
            "Loan ID", "Member", "Book", "Issued", "Due",
            "Returned", "Status", "Fine", "Fine Status"
        ],
        rows
    )


def loan_menu():
    while True:
        print("\n--- Book Issue and Return ---")
        print("1. Issue book")
        print("2. Return book")
        print("3. View all loans")
        print("4. View active loans")
        print("5. Pay overdue fine")
        print("0. Back")

        choice = input("Choose: ").strip()

        if choice == "1":
            issue_book()
        elif choice == "2":
            return_book()
        elif choice == "3":
            list_loans()
        elif choice == "4":
            list_loans("Issued")
        elif choice == "5":
            pay_fine()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")
