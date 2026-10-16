from config import BOOK_FILE
from storage import load_data, save_data, next_id
from utils import read_text, read_positive_int, print_table


def add_book():
    books = load_data(BOOK_FILE)

    print("\n--- Add Book ---")
    title = read_text("Book title: ")
    author = read_text("Author: ")
    isbn = read_text("ISBN: ")

    if any(
        book["isbn"].casefold() == isbn.casefold()
        for book in books
    ):
        print("A book with this ISBN already exists.")
        return

    category = read_text("Category: ")
    copies = read_positive_int("Number of copies: ")

    book = {
        "id": next_id(books),
        "title": title,
        "author": author,
        "isbn": isbn,
        "category": category,
        "total_copies": copies,
        "available_copies": copies,
        "active": True
    }

    books.append(book)
    save_data(BOOK_FILE, books)

    print(f"Book added successfully. Book ID: {book['id']}")


def list_books():
    books = load_data(BOOK_FILE)

    print_table(
        ["ID", "Title", "Author", "ISBN", "Category", "Total", "Available"],
        [
            [
                b["id"], b["title"], b["author"], b["isbn"],
                b["category"], b["total_copies"], b["available_copies"]
            ]
            for b in books if b["active"]
        ]
    )


def search_books():
    query = read_text("Search by title, author, ISBN, or category: ").casefold()
    books = load_data(BOOK_FILE)

    results = [
        b for b in books
        if b["active"] and any(
            query in str(b[field]).casefold()
            for field in ["title", "author", "isbn", "category"]
        )
    ]

    print_table(
        ["ID", "Title", "Author", "ISBN", "Category", "Available"],
        [
            [
                b["id"], b["title"], b["author"], b["isbn"],
                b["category"], b["available_copies"]
            ]
            for b in results
        ]
    )


def get_book(book_id):
    return next(
        (
            b for b in load_data(BOOK_FILE)
            if b["id"] == book_id and b["active"]
        ),
        None
    )


def book_menu():
    while True:
        print("\n--- Book Management ---")
        print("1. Add book")
        print("2. View books")
        print("3. Search books")
        print("0. Back")

        choice = input("Choose: ").strip()

        if choice == "1":
            add_book()
        elif choice == "2":
            list_books()
        elif choice == "3":
            search_books()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")
