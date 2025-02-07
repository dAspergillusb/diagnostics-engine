

def test_1_check(answers: dict[int, list[bool] | str]) -> tuple[list[int], list[str]]:
    questions: list[str] = [
        "Когда был основан заповедник «Кивач»",
        "Какие леса преобладают на территории заповедника «Кивач»?",
        "Какие формы рельефа можно увидеть в заповеднике «Кивач»?",
        "Выпиши цифру с картинки, где изображены «бараньи лбы»",
        "Расставь события легенды в правильной последовательности",
        "Выберите два утверждения, соответствующих информации из текста",
    ]
    marks: list[int] = []
    right_answers: dict[int, list[bool] | str] = {
        1: [False, False, False, True, False, False],
        2: [False, True, False, False, False, False],
        3: [True, False, False, True, False, True],
        4: "1",
        5: "2617534",
        6: [True, False, False, True, False, False]
    }
    for number in right_answers:
        if answers[number] == right_answers[number]:
            marks.append(1)
        else:
            marks.append(0)
    return marks, questions


def test_2_check(answers: dict[int, list[bool]]) -> tuple[list[int], list[str]]:
    questions: list[str] = [
        "Какова площадь Васюганских болот, самых больших в России и в мире?",
        "Когда начался процесс образования и увеличения площади Васюганских болот?",
        "Какова природно-ресурсная ценность Васюганских болот?",
        "Где находятся Васюганские болота?",
        "Чем насыщают воздух торфяные болота Сибири?",
        "Какую функцию выполняют Васюганские болота в экосистеме?",
    ]
    marks: list[int] = []
    right_answers: dict[int, list[bool] | str] = {
        1: [False, True, False, False, False, False],
        2: [False, True, False, False, False, False],
        3: [True, False, True, False, True, False],
        4: "3",
        5: "кислород",
        6: [True, False, False, False, False, False]
    }
    for number in right_answers:
        if answers[number] == right_answers[number]:
            marks.append(1)
        else:
            marks.append(0)
    return marks, questions


def test_3_check(answers: dict[int, list[bool] | str]) -> tuple[list[int], list[str]]:
    questions: list[str] = [
        "Какой из следующих факторов делает мопса подходящей породой для жизни в квартире?",
        "Какой уход требуется за шерстью пуделя?",
        "Какое качество корги отмечается в описании породы?",
        "Что необходимо для содержания бигля?",
        "Какие методы лучше использовать для дрессировки корги?",
        "В чем особенность характера кокер-спаниеля?",
        "Какой из следующих факторов делает золотистого ретривера популярной породой?",
        "Какой основной признак бигля?",
        "Какой из перечисленных аспектов лучше всего описывает джек-рассел-терьера?",
        "Каково основное требование к уходу за мопсом?",
        "Какое из качеств делает пуделя хорошим домашним питомцем?",
        "Какой тип активности требуется корги для поддержания здоровья?",
        "Верно ли то, что мопс легко поддается дрессировке и требует высокой физической активности?",
        "Верно ли то, что корги — это собаки небольшой размерности с длинными ногами?",
        "Верно ли то, что кокер-спаниель может быть с шерстью разной длины и густоты в зависимости от типа?",
    ]
    marks: list[int] = []
    right_answers: dict[int, list[bool] | str] = {
        1: [True, False, False, False, False, False],
        2: [False, False, False, True, False, False],
        3: [False, True, False, False, False, False],
        4: ["ухаживать", "длинными", "длинные", "ушами", "ухода", "уши"],
        5: ["игр"],
        6: [False, False, False, True, False, False],
        7: [False, True, False, False, False, False],
        8: [False, True, False, False, False, False],
        9: [False, False, False, False, True, False],
        10: [True, False, False, False, False, False],
        11: [False, False, False, True, False, False],
        12: [False, True, False, False, False, False],
        13: [False, True, False, False, False, False],
        14: [False, True, False, False, False, False],
        15: [True, False, False, False, False, False],
    }
    for number in right_answers:
        if answers[number] == right_answers[number]:
            marks.append(1)
        elif number == 4:
            for answer in right_answers[number]:
                if answer.lower() in answers[number].lower():
                    marks.append(1)
                    break
            else:
                marks.append(0)
        elif number == 5:
            for answer in right_answers[number]:
                if answer.lower() in answers[number].lower():
                    marks.append(1)
                    break
            else:
                marks.append(0)
        else:
            marks.append(0)
    return marks, questions


def test_4_check(answers: dict[int, list[bool] | str]) -> tuple[list[int], list[str]]:
    questions: list[str] = [
        "Что такое скетчинг?",
        "Откуда происходит название «скетчинг»?",
        "Кто активно использует технику скетчинга?",
        "Какие материалы чаще всего используются для скетчинга?",
        "Какова разница между скетчем и скетч-иллюстрацией?",
        "Сколько времени обычно уходит на создание скетча?",
        "Что называют скетч-иллюстрацией?",
        "Какой материал чаще всего используется для скетчинга?",
        "Какое из приведенных направлений не является разновидностью скетчинга?",
        "Какую пользу приносит овладение техникой скетчинга для начинающих художников?",
        "Что является основной идеей скетчинга?",
        "Какую роль скетчинг может играть в жизни людей?",
        "Верно ли то, что скетчинг стал известным как отдельное художественное направление в искусстве?",
        "Верно ли то, что основная идея скетчинга заключается в точной передаче всех деталей?",
        "Верно ли то, что скетч-иллюстрация — это простой и быстрый процесс?",
    ]
    marks: list[int] = []
    right_answers: dict[int, list[bool] | str] = {
        1: [False, True, False, False, False, False],
        2: [False, False, True, False, False, False],
        3: [False, True, False, False, False, False],
        4: [
            "маркеры, акварель, простые и цветные карандаши, линеры",
            "маркеры, акварель, простые и цветные карандаши, линеры.",
            "маркеры, акварель, простые и цветные карандаши и линеры",
            "маркеры, акварель, простые и цветные карандаши и линеры.",
            "Чаще всего для скетчинга используют маркеры, акварель, простые и цветные карандаши, линеры",
            "маркеры, акварель, карандаши, линеры",
            "маркеры, акварель, карандаши и линеры"
        ],
        5: [
            "этюд",
            "эскиз",
            "наброс",
            "зарисовк",
            "техник",
            "быстр",
            "рисун",
            "час",
            "профессиональ",
            "разновидн",
        ],
        6: [True, False, False, False, False, False],
        7: [True, False, False, False, False, False],
        8: [False, False, False, True, False, False],
        9: [True, False, False, False, False, False],
        10: [False, False, False, True, False, False],
        11: [False, False, False, False, True, False],
        12: [False, False, False, True, False, False],
        13: [True, False, False, False, False, False],
        14: [False, True, False, False, False, False],
        15: [False, True, False, False, False, False],
    }
    for number in right_answers:
        if answers[number] == right_answers[number]:
            marks.append(1)
        elif number == 4:
            for answer in right_answers[number]:
                if answer.lower() in answers[number].lower():
                    marks.append(1)
                    break
            else:
                marks.append(0)
        elif number == 5:
            count = 0
            for answer in right_answers[number]:
                if answer.lower() in answers[number].lower():
                    count += 1
                if count >= 5:
                    marks.append(1)
                    break
                print(count)
            else:
                marks.append(0)
        else:
            marks.append(0)
    return marks, questions


def test_5_check(answers: dict[int, list[bool]]):
    pass


def test_6_check(answers: dict[int, list[bool]]):
    pass


SUPPORTED_TESTS_RC = {
    "test_1": test_1_check,
    "test_2": test_2_check,
    "test_3": test_3_check,
    "test_4": test_4_check,
    "test_5": test_5_check,
    "test_6": test_6_check,
}

SUPPORTED_TESTS_EN = {
    "test_1": test_1_check,
    "test_2": test_2_check,
    "test_3": test_3_check,
    "test_4": test_4_check,
    "test_5": test_5_check,
    "test_6": test_6_check,
}
