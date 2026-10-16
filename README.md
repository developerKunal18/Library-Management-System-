
# Library Management System

## Overview

A Python command-line application for managing library books, members, borrowing records, returns, and overdue fines. Data is stored locally in JSON files.

## Features

- Add and search books
- Register library members
- Track total and available copies
- Issue books and record due dates
- Return books and calculate overdue fines
- Record fine payments
- View active loans and borrowing history
- Generate overdue-book reports
- View library statistics

## Technologies

- Python 3.10+
- JSON file storage
- Python standard library

## Installation

1. Install Python 3.10 or later.
2. Clone or download this repository.
3. Open a terminal in the project directory.
4. Start the application:

   ```bash
   python main.py
   ```

No external packages are required.

## Project Structure

```text
day358_library_management/
├── main.py
├── config.py
├── storage.py
├── utils.py
├── book_manager.py
├── member_manager.py
├── loan_manager.py
├── report_manager.py
├── requirements.txt
├── .gitignore
├── README.md
└── data/
    ├── books.json
    ├── members.json
    └── loans.json
```

## How to Use

1. Add a book with its ISBN and copy count.
2. Register a library member.
3. Issue the book using the member ID and book ID.
4. Check the loan's due date.
5. Return the book and review any overdue fine.
6. Record payment for an outstanding fine.
7. Use reports to view overdue books and member history.

## Loan Rules

- The default loan period is 14 days.
- The maximum number of active loans per member is 3.
- The fine is ₹5 per overdue day.
- A book becomes available again when it is returned.
- Fines are calculated using calendar dates.

## Testing Checklist

- Add a book and try adding the same ISBN again.
- Register a member.
- Issue a book and verify its available-copy count decreases.
- Try issuing a book when no copies remain.
- Return a book and verify inventory increases.
- Test overdue fine calculation.
- Record a fine payment.
- Check member history and overdue reports.

## Data Storage

The application creates JSON files in the `data` directory. Back up these files regularly.

## Limitations

- This is a local learning project, not a production library platform.
- JSON storage is intended for single-user use.
- Fine collection is recorded manually.
- Login, access permissions, and barcode scanning are not included.
- It does not currently support reservations or renewals.

## Future Improvements

- Add book reservations and renewals.
- Add a graphical interface using Tkinter.
- Add CSV report export.
- Add automated tests using `unittest`.
- Migrate storage to SQLite or MySQL.
- Add login and librarian permissions.
