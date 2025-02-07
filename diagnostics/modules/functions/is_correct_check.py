from re import fullmatch, Match
from datetime import datetime
from time import time


def is_correct_firstname(firstname: str) -> bool:
    candidate: Match | None = fullmatch(r"[А-Я][а-я]+", firstname)
    if candidate:
        return True
    return False


def is_correct_lastname(lastname: str) -> bool:
    candidate: Match | None = fullmatch(r"[А-Я][а-я]+", lastname)
    if candidate:
        return True
    return False


def is_correct_email(email: str) -> bool:
    candidate: Match | None = fullmatch(r"[A-Za-z0-9._-]+@[A-Za-z0-9.]+(ru|com|net|org)", email)
    if candidate:
        return True
    return False


def is_correct_class(_class: str) -> bool:
    if _class:
        return bool(fullmatch(r"1?[0-9]-[АБВГДЗИКЭЯ]", _class))

    return False


def is_correct_subject(subject: str) -> bool:
    if subject:
        return bool(
            fullmatch(
                r"математика|алгебра|геометрия|русский язык|литература|информатика|география|биология|история|обществознание|физика|английский язык|химия|читательская грамотность",
                subject
            )
        )

    return False


def is_correct_username(username: str) -> bool:
    candidate: Match = fullmatch(r"[a-zA-Z][a-zA-Z0-9]+[a-zA-Z0-9]+", username)
    if all((candidate, len(username) > 3)):
        return True
    return False


def is_correct_password(password: str) -> bool:
    if len(password) < 8:
        return False
    candidate: Match | None = fullmatch(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[^\w\s]).{8,}", password)
    if candidate:
        return True
    return False


def encoding_password(password: str) -> str:
    hashed_pass: int = sum([ord(char) for char in password])
    return "".join([str(hashed_pass)[:index] for index in range(len(str(hashed_pass)))])


def create_date_stamp():
    return int(time())


def check_link_time(send_time: int) -> bool:
    diff_time: int = int((time() - send_time) / 3600)
    if diff_time:
        return True
    return False


if __name__ == '__main__':
    #print(is_correct_firstname("Никита"))
    #print(is_correct_username("Nikita1234"))
    #print(is_correct_password("Nikita2$"))
    print(is_correct_email("irina.trushina2012@yandex.ru"))
    #print(is_correct_class("5-Э"))
    #print(encoding_password("Gram321@#321"))
    #print((create_date_stamp() - 1728140628) / 60)
    print(is_correct_subject("математика&информатика"))
