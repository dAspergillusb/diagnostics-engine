from .is_correct_check import (
    is_correct_email,
    is_correct_class,
    is_correct_subject,
    is_correct_lastname,
    is_correct_password,
    is_correct_username,
    is_correct_firstname,
    encoding_password,
    create_date_stamp,
    check_link_time
)
from .reg_login import (
    check_session_login_failed,
    made_login,
    get_registration_args,
    is_data_correct,
    add_user_log_email_send,
)
from .students_teachers import (
    choose_student_grade,
    get_test_attempt_page,
    get_teacher_panel_main
)
from .databases_connections import (
    connect_database_subject,
    connect_database_users,
    connect_database_statistics
)
from .questions_and_answers import (
    get_questions_range,
    get_answers,
    get_right_answers_and_answers,
    save_one_question,
    save_all_questions,
    get_datas_rc,
    get_block_data_english,
    add_statistics_and_log,
    get_teacher_questions,
    get_data_question_to_change
)
from .files_operations import (
    write_test_image,
    write_image_file,
    write_audio_file,
    get_filepath
)
from .key_operations import import_secret_key