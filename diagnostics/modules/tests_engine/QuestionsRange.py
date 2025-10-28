class QuestionsRange:


    def __init__(self, subject: str, school_class: str):
        self.subject = subject
        self.school_class = school_class

        self.SUBJECT_QUESTIONS_RANGE: dict[str, dict[str, range]] = {
            "mathematics": {"2": range(1, 8), "3": range(1, 8), "4": range(1, 8),
                            "5": range(1, 8), "6": range(1, 8), "7": range(1, 8), "8": range(1, 8),
                            "9": range(1, 8), "10": range(1, 8), "11": range(1, 8)},
            """"mathematics_depth": {"7": range(1, 13), "8": range(1, 13), "9": range(1, 13)},
            "mathematics_base": {"10": range(1, 18), "11": range(1, 18)},
            "mathematics_profile": {"10": range(1, 12), "11": range(1, 12)},
            "algebra": {"7": range(1, 11), "8": range(1, 12), "9": range(1, 13)},
            "geometry": {"7": range(1, 11), "8": range(1, 12), "9": range(1, 13)},"""
            "biology": {"5": range(1, 16), "6": range(1, 16), "7": range(1, 16), "8": range(1, 18), "9": range(1, 19),
                        "10": range(1, 18), "11": range(1, 18)},
            "chemistry": {"8": range(1, 11), "9": range(1, 12), "10": range(1, 14), "11": range(1, 15)},
            "geography": {"5": range(1, 9), "6": range(1, 12), "7": range(1, 13), "8": range(1, 14), "9": range(1, 17),
                        "10": range(1, 18), "11": range(1, 18)},
            "history": {"5": range(1, 17), "6": range(1, 13), "7": range(1, 13), "8": range(1, 17), "9": range(1, 16),
                        "10": range(1, 16), "11": range(1, 16)},
            "social_science": {"6": range(1, 11), "7": range(1, 11), "8": range(1, 15), "9": range(1, 17),
                        "10": range(1, 18), "11": range(1, 19)},
            "russian": {"2": range(1, 7), "3": range(1, 7), "4": range(1, 17), "5": range(1, 18), "6": range(1, 18),
                        "7": range(1, 17), "8": range(1, 19), "9": range(1, 11), "10": range(1, 17), "11": range(1, 17)},
            "informatics": {"7": range(1, 9), "8": range(1, 13), "9": range(1, 11),
                            "10": range(1, 13), "11": range(1, 13)},
            "physics": {"7": range(1, 13), "8": range(1, 11), "9": range(1, 15), "10": range(1, 16), "11": range(1, 11)},
            "literature": {"2": range(1, 7), "3": range(1, 7), "4": range(1, 7), "5": range(1, 7), "6": range(1, 7),
                        "7": range(1, 15), "8": range(1, 12), "9": range(1, 10), "10": range(1, 10), "11": range(1, 10)},
            "outward_things": {"2": range(1, 7), "3": range(1, 7), "4": range(1, 7)},
            "probability_theory": {"7": range(1, 9), "8": range(1, 9), "9": range(1, 9),
                                   "10": range(1, 11), "11": range(1, 11)},
            "reading_comprehension": {"2": range(1, 16), "3": range(1, 16), "4": range(1, 16),
                                      "5": range(1, 16), "6": range(1, 16)},
            "english": {"2": range(1, 5), "3": range(1, 5), "4": range(1, 5), "5": range(1, 5), "6": range(1, 5),
                        "7": range(1, 5), "8": range(1, 5), "9": range(1, 5), "10": range(1, 7), "11": range(1, 7)}
        }

    def get_range(self) -> range:
        return self.SUBJECT_QUESTIONS_RANGE.get(self.subject).get(self.school_class)

