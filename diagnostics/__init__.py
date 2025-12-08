from flask import (
    Flask
)
from modules import (
    register_main_pages,
    register_teacher_menu_pages,
    register_teacher_panel_pages,
    register_student_pages,
    register_tests_pages,
    register_admin_pages
)
from modules import (
    SECRET_KEY,
    HOST,
    PORT,
    MAX_FORM_MEMORY_SIZE
)


MAIN: Flask = Flask(import_name=__name__)
MAIN.config["SECRET_KEY"] = SECRET_KEY
MAIN.config["MAX_FORM_MEMORY_SIZE"] = MAX_FORM_MEMORY_SIZE
MAIN.config["MAX_CONTENT_LENGTH"] = MAX_FORM_MEMORY_SIZE
MAIN.config["MAX_FORM_PARTS"] = MAX_FORM_MEMORY_SIZE

# Register all endpoints to MAIN app
register_main_pages(main=MAIN)
register_teacher_menu_pages(main=MAIN)
register_teacher_panel_pages(main=MAIN)
register_student_pages(main=MAIN)
register_tests_pages(main=MAIN)
register_admin_pages(main=MAIN)


if __name__ == '__main__':
    MAIN.run(
        debug=True,
        host="127.0.0.1",
        port=PORT
    )
