from config import BOOK_FILE, MEMBER_FILE, LOAN_FILE
from storage import ensure_file

from book_manager import book_menu
from member_manager import member_menu
from loan_manager import loan_menu
from report_manager import report_menu


def initialize():
    for file_path in [BOOK_FILE, MEMBER_FILE, LOAN_FILE]:
        ensure_file(file_path)


def main():
    initialize()

    while True:
        print("\n====================================")
        print("       LIBRARY MANAGEMENT SYSTEM")
        print("====================================")
        print("1. Book management")
        print("2. Member management")
        print("3. Issue and return books")
        print("4. Reports")
        print("0. Exit")

        choice = input("Enter your choice: ").strip()

        try:
            if choice == "1":
                book_menu()
            elif choice == "2":
                member_menu()
            elif choice == "3":
                loan_menu()
            elif choice == "4":
                report_menu()
            elif choice == "0":
                print("Thank you for using Library Management System.")
                break
            else:
                print("Invalid choice. Please try again.")

        except (OSError, ValueError, KeyError) as error:
            print(f"Operation failed: {error}")
            print("Check the input and JSON data files before retrying.")


if __name__ == "__main__":
    main()
