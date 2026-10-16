from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

BOOK_FILE = DATA_DIR / "books.json"
MEMBER_FILE = DATA_DIR / "members.json"
LOAN_FILE = DATA_DIR / "loans.json"

LOAN_PERIOD_DAYS = 14
FINE_PER_DAY = 5.0
MAX_ACTIVE_LOANS_PER_MEMBER = 3
