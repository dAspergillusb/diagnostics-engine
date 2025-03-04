from secrets import token_urlsafe
from datetime import datetime


def generate_secret_key() -> tuple[str, str]:
    return str(datetime.now()).translate(str.maketrans(" :.", "---")), token_urlsafe(32)


def import_secret_key() -> str:
    with open("key/key", "r") as key:
        _date, secret_key = key.read().split()

    if (datetime.now() - datetime(*map(int, _date.split("-")))).days >= 7:
        new_date, new_key = generate_secret_key()
        with open("key/key", "w") as key:
            key.write(f"{new_date} {new_key}")
        return new_key

    return secret_key

