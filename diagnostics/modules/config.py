from typing import Type
from .functions.key_operations import import_secret_key
from ._types import DataBase, BaseTable
from .databases import Algebra, AlgebraDB
from .databases import Geometry, GeometryDB
from .databases import Mathematics, MathematicsDB
from .databases import MathematicsBase, MathematicsBaseDB
from .databases import MathematicsProfile, MathematicsProfileDB
from .databases import Biology, BiologyDB
from .databases import Chemistry, ChemistryDB
from .databases import Geography, GeographyDB
from .databases import English, EnglishDB
from .databases import History, HistoryDB
from .databases import SocialScience, SocialScienceDB
from .databases import Russian, RussianDB
from .databases import ReadingComprehension, ReadingComprehensionDB
from .databases import OutwardThings, OutwardThingsDB
from .databases import Informatics, InformaticsDB
from .databases import Physics, PhysicsDB
from .databases import Literature, LiteratureDB
from .databases import ProbabilityTheory, ProbabilityTheoryDB
from .databases import MathematicsDepth, MathematicsDepthDB
from .databases import TeacherStatistics, TeacherStatisticsDB
from .databases import UsersStatistics, UsersStatisticsDB


HOST: str = "диагностики.1381.рф"
#HOST: str = "192.168.10.113"
#HOST: str = "5.101.152.4"
#HOST: str = "172.24.92.244"
#HOST: str = "192.168.3.3"
PORT: int = 5000
SECRET_KEY: str = import_secret_key()
ICON_WHITE: str = "/static/svg/icon_white.svg"
ICON_BLACK: str = "/static/svg/icon_black.svg"

"""MAIL_LOGIN: str = "diagnostics@1381.xn--p1ai"  # Name of mail that will send a messages of registration/restore password
MAIL_PASSWORD: str = "ptNT*Tesb3Dy"  # This password is not for account, it's for sendmail only!"""

SUBJECTS: dict[str, dict[str, BaseTable | DataBase]] = {
    "algebra": {"base": Algebra, "db": AlgebraDB},
    "geometry": {"base": Geometry, "db": GeometryDB},
    "mathematics": {"base": Mathematics, "db": MathematicsDB},
    "mathematics_depth": {"base": MathematicsDepth, "db": MathematicsDepthDB},
    "probability_theory": {"base": ProbabilityTheory, "db": ProbabilityTheoryDB},
    "mathematics_base": {"base": MathematicsBase, "db": MathematicsBaseDB},
    "mathematics_profile": {"base": MathematicsProfile, "db": MathematicsProfileDB},
    "biology": {"base": Biology, "db": BiologyDB},
    "chemistry": {"base": Chemistry, "db": ChemistryDB},
    "geography": {"base": Geography, "db": GeographyDB},
    "english": {"base": English, "db": EnglishDB},
    "history": {"base": History, "db": HistoryDB},
    "social_science": {"base": SocialScience, "db": SocialScienceDB},
    "russian": {"base": Russian, "db": RussianDB},
    "reading_comprehension": {"base": ReadingComprehension, "db": ReadingComprehensionDB},
    "informatics": {"base": Informatics, "db": InformaticsDB},
    "physics": {"base": Physics, "db": PhysicsDB},
    "literature": {"base": Literature, "db": LiteratureDB},
    "outward_things": {"base": OutwardThings, "db": OutwardThingsDB}
}

STATISTICS: dict[
    str,
    dict[str, Type[TeacherStatistics | TeacherStatisticsDB]] | dict[str, Type[UsersStatistics | UsersStatisticsDB]]
] = {
    "teacher": {"base": TeacherStatistics, "db": TeacherStatisticsDB},
    "student": {"base": UsersStatistics, "db": UsersStatisticsDB}
}

# Needed for change link type of subject to readable type.
SUBJECTS_NAME_TO_LINK: dict[str, str] = {
    "математика": "mathematics",
    "математика (углубленная)": "mathematics_depth",
    "теория вероятностей": "probability_theory",
    "математика (база)": "mathematics_base",
    "математика (профиль)": "mathematics_profile",
    "алгебра": "algebra",
    "геометрия": "geometry",
    "биология": "biology",
    "химия": "chemistry",
    "география": "geography",
    "английский язык": "english",
    "история": "history",
    "обществознание": "social_science",
    "русский язык": "russian",
    "информатика": "informatics",
    "читательская грамотность": "reading_comprehension",
    "физика": "physics",
    "литература": "literature",
    "окружающий мир": "outward_things"
}

#  Subjects ranges for school classes. What school class value of subject.
SUBJECTS_RANGES_FOR_CLASS: dict[str, range] = {
    "mathematics": range(2, 7),
    "mathematics_depth": range(7, 10),
    "probability_theory": range(7, 12),
    "mathematics_base": range(10, 12),
    "mathematics_profile": range(10, 12),
    "algebra": range(7, 10),
    "geometry": range(7, 10),
    "biology": range(5, 12),
    "chemistry": range(8, 12),
    "geography": range(5, 12),
    "english": range(2, 12),
    "history": range(5, 11),
    "social_science": range(6, 12),
    "russian": range(2, 12),
    "informatics": range(7, 12),
    "reading_comprehension": range(2, 7),
    "physics": range(7, 12),
    "literature": range(2, 12),
    "outward_things": range(2, 5)
}

ELEMENTARY_SCHOOL: list[str] = ["математика", "русский язык", "литература",
                                "окружающий мир", "английский язык", "читательская грамотность"]

UNIQUE_SUBJECTS: set[str] = {"english"}

SUPPORTED_IMAGE_TYPES: set[str] = {"jpg", "jpeg", "png", "svg"}

SUPPORTED_AUDIO_TYPES: set[str] = {"mp3"}

FOR_CARDS_ELEMENTARY: dict[int, tuple[str, str, str, str]] = {
    1: ("/static/images/for_subjects/english.svg", "Английский язык", "английскому языку", "english"),
    2: ("/static/images/for_subjects/literature.svg", "Литература", "литературе", "literature"),
    3: ("/static/images/for_subjects/mathematics.svg", "Математика", "математике", "mathematics"),
    4: ("/static/images/for_subjects/outward_things.svg", "Окружающий мир", "окружающий мир", "outward_things"),
    5: ("/static/images/for_subjects/russian.svg", "Русский язык", "русскому языку", "russian"),
    6: ("/static/images/for_subjects/reading_comprehension.svg", "Читательская грамотность", "читательской грамотности",
        "reading_comprehension"),
}

FOR_CARDS_JUNIOR: dict[int, tuple[str, str, str, str]] = {
    1: ("/static/images/for_subjects/english.svg", "Английский язык", "английскому языку", "english"),
    2: ("/static/images/for_subjects/biology.svg", "Биология", "биологии", "biology"),
    3: ("/static/images/for_subjects/geography.svg", "География", "географии", "geography"),
    4: ("/static/images/for_subjects/history.svg", "История", "истории", "history"),
    5: ("/static/images/for_subjects/literature.svg", "Литература", "литературе", "literature"),
    6: ("/static/images/for_subjects/mathematics.svg", "Математика", "математике", "mathematics"),
    7: ("/static/images/for_subjects/social_science.svg", "Обществознание", "обществознанию", "social_science"),
    8: ("/static/images/for_subjects/russian.svg", "Русский язык", "русскому языку", "russian"),
    9: ("/static/images/for_subjects/reading_comprehension.svg", "Читательская грамотность", "читательской грамотности",
        "reading_comprehension"),
}

FOR_CARDS_MIDDLE: dict[int, tuple[str, str, str, str]] = {
    1: ("/static/images/for_subjects/algebra.svg", "Алгебра", "алгебре", "algebra"),
    2: ("/static/images/for_subjects/english.svg", "Английский язык", "английскому языку", "english"),
    3: ("/static/images/for_subjects/biology.svg", "Биология", "биологии", "biology"),
    4: ("/static/images/for_subjects/geography.svg", "География", "географии", "geography"),
    5: ("/static/images/for_subjects/geometry.svg", "Геометрия", "геометрии", "geometry"),
    6: ("/static/images/for_subjects/informatics.svg", "Информатика", "информатике", "informatics"),
    7: ("/static/images/for_subjects/history.svg", "История", "истории", "history"),
    8: ("/static/images/for_subjects/literature.svg", "Литература", "литературе", "literature"),
    9: ("/static/images/for_subjects/mathematics.svg", "Математика (углубленная)", "математике (углубленная)", "mathematics_depth"),
    10: ("/static/images/for_subjects/social_science.svg", "Обществознание", "обществознанию", "social_science"),
    11: ("/static/images/for_subjects/russian.svg", "Русский язык", "русскому языку", "russian"),
    12: ("/static/images/for_subjects/probability_theory.svg", "Теория вероятностей", "теории вероятностей", "probability_theory"),
    13: ("/static/images/for_subjects/physics.svg", "Физика", "физике", "physics"),
    14: ("/static/images/for_subjects/chemistry.svg", "Химия", "химии", "chemistry")
}

FOR_CARDS_SENIOR: dict[int, tuple[str, str, str, str]] = {
    1: ("/static/images/for_subjects/english.svg", "Английский язык", "английскому языку", "english"),
    2: ("/static/images/for_subjects/biology.svg", "Биология", "биологии", "biology"),
    3: ("/static/images/for_subjects/geography.svg", "География", "географии", "geography"),
    4: ("/static/images/for_subjects/informatics.svg", "Информатика", "информатике", "informatics"),
    5: ("/static/images/for_subjects/history.svg", "История", "истории", "history"),
    6: ("/static/images/for_subjects/literature.svg", "Литература", "литературе", "literature"),
    7: ("/static/images/for_subjects/mathematics_base.svg", "Математика (база)", "математике базового уровня",
        "mathematics_base"),
    8: ("/static/images/for_subjects/mathematics_profile.svg", "Математика (профиль)", "математике профильного уровня",
        "mathematics_profile"),
    9: ("/static/images/for_subjects/social_science.svg", "Обществознание", "обществознанию", "social_science"),
    10: ("/static/images/for_subjects/russian.svg", "Русский язык", "русскому языку", "russian"),
    11: ("/static/images/for_subjects/probability_theory.svg", "Теория вероятностей", "теории вероятностей", "probability_theory"),
    12: ("/static/images/for_subjects/physics.svg", "Физика", "физике", "physics"),
    13: ("/static/images/for_subjects/chemistry.svg", "Химия", "химии", "chemistry")
}

TEST_DATA: dict[str, str] = {
    "title": "",
    "text": "",
    "image": "",
    "image_type": "",
    "answer_variants": "",
    "right_answer": ""
}

