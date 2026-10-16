from datetime import date

from config import BOOK_FILE, MEMBER_FILE, LOAN_FILE, FINE_PER_DAY
from storage import load_data
from utils import money, print_table


def dashboard():
    books = load_data(BOOK_FILE)
    members = load_data(MEMBER_FILE)
    loans = load_data(LOAN_FILE)

    active_loans = [loan for loan in loans if loan["status"] == "Issued"]
    returned_loans = [loan for loan in loans if loan["status"] == "Returned"]

    outstanding_fines = sum(
        float(loan["fine"])
        for loan in loans
        if float(loan["fine"]) > 0 and not loan["fine_paid"]
    )

    print("\n========== LIBRARY DASHBOARD ==========")
    print(f"Book titles:             {sum(b['active'] for b in books)}")
    print(f"Total copies:            {sum(b['total_copies'] for b in books if b['active'])}")
    print(f"Available copies:        {sum(b['available_copies'] for b in books if b['active'])}")
    print(f"Registered members:      {sum(m['active'] for m in members)}")
    print(f"Active loans:            {len(active_loans)}")
    print(f"Returned loans:          {len(returned_loans)}")
    print(f"Outstanding fines:       {money(outstanding_fines)}")
    print("=======================================")


def overdue_report():
    today = date.today()
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
        if loan["status"] != "Issued":
            continue

        due_date = date.fromisoformat(loan["due_date"])

        if due_date < today:
            overdue_days = (today - due_date).days
            estimated_fine = overdue_days * FINE_PER_DAY

            rows.append([
                loan["id"],
                members.get(loan["member_id"], "Unknown"),
                books.get(loan["book_id"], "Unknown"),
                loan["due_date"],
                overdue_days,
                money(estimated_fine)
            ])

    print_table(
        ["Loan ID", "Member", "Book", "Due Date", "Days Late", "Estimated Fine"],
        rows
    )


def member_history():
    try:
        member_id = int(input("Member ID: ").strip())
        if member_id <= 0:
            raise ValueError
    except ValueError:
        print("Enter a valid positive member ID.")
        return

    members = load_data(MEMBER_FILE)
    member = next((m for m in members if m["id"] == member_id), None)

    if not member:
        print("Member not found.")
        return

    loans = [
        loan for loan in load_data(LOAN_FILE)
        if loan["member_id"] == member_id
    ]

    books = {
        b["id"]: b["title"]
        for b in load_data(BOOK_FILE)
    }

    print(f"\nBorrowing history for {member['name']}")

    print_table(
        ["Loan ID", "Book", "Issue Date", "Due Date", "Return Date", "Status", "Fine"],
        [
            [
                loan["id"],
                books.get(loan["book_id"], "Unknown"),
                loan["issue_date"],
                loan["due_date"],
                loan["return_date"] or "-",
                loan["status"],
                money(loan["fine"])
            ]
            for loan in loans
        ]
    )


def report_menu():
    while True:
        print("\n--- Library Reports ---")
        print("1. Library dashboard")
        print("2. Overdue books")
        print("3. Member borrowing history")
        print("0. Back")

        choice = input("Choose: ").strip()

        if choice == "1":
            dashboard()
        elif choice == "2":
            overdue_report()
        elif choice == "3":
            member_history()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")
