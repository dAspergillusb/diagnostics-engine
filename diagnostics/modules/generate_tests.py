from os import listdir
from random import randint


ENGLISH_CLASSES: dict[int, str] = {
    2: "templates/english/school_junior",
    3: "templates/english/school_junior",
    4: "templates/english/school_junior",
    5: "templates/english/school_junior",
    6: "templates/english/school_junior",
    7: "templates/english/school_middle",
    8: "templates/english/school_middle",
    9: "templates/english/school_middle",
    10: "templates/english/school_senior",
    11: "templates/english/school_senior"
}


def get_variant_read_comprehension() -> str:
    variants: list[str] = [
        test.split(".")[0] for test in listdir("templates/reading_comprehension")
    ]
    return variants[randint(0, len(variants) - 1)]


def get_variant_english(school_class: int) -> str:
    variants: list[str] = listdir(ENGLISH_CLASSES.get(school_class, None))
    return variants[randint(0, len(variants) - 1)]


if __name__ == '__main__':
    print(get_variant_read_comprehension())
