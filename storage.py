import json
from pathlib import Path


def ensure_file(file_path):
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    if not path.exists():
        path.write_text("[]", encoding="utf-8")


def load_data(file_path):
    ensure_file(file_path)

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError(f"Expected a JSON list in {file_path}")

        return data

    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Invalid JSON in {file_path}. Repair the file before continuing."
        ) from exc


def save_data(file_path, data):
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    temp_path = path.with_suffix(path.suffix + ".tmp")

    with open(temp_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    temp_path.replace(path)


def next_id(records):
    return max(
        (int(record.get("id", 0)) for record in records),
        default=0
    ) + 1
