from datetime import datetime
from dataclasses import dataclass
from sqlalchemy import Column, String, Integer, Boolean


@dataclass(frozen=True)
class LogingLog:
    _date: datetime
    user_id: Column[Integer] | int
    username: Column[String] | str
    rank: str
    school_class: Column[String] | str

    def add_log_login(self) -> None:
        with open("log_loging.log", "a") as loging_log:
            loging_log.write(
                f"Login:: {str(self._date)}: {self.user_id}; {self.username}; {self.rank}; {self.school_class}\n"
            )

    def add_log_logout(self) -> None:
        with open("log_loging.log", "a") as loging_log:
            loging_log.write(
                f"Logout:: {str(self._date)}: {self.user_id}; {self.username}; {self.rank}; {self.school_class}\n"
            )


@dataclass(frozen=True)
class AddQuestionLog:
    _date: datetime
    subject: str
    username: Column[String] | str
    question_ids: list[Column[Integer]] | Column[Integer] | list[str]
    question_value: int = 0

    def add_log_new_entry(self) -> None:
        with open("log_subjects.log", "a") as subject_log:
            subject_log.write(
                f"New entry:: {str(self._date)}: {self.username}; {self.subject}; {self.question_value=}; {self.question_ids}\n"
            )

    def add_log_remove_entry(self) -> None:
        with open("log_subjects.log", "a") as subject_log:
            subject_log.write(
                f"Remove entry:: {str(self._date)}: {self.username}; {self.subject}; {self.question_value=}; {self.question_ids}\n"
            )


@dataclass(frozen=True)
class UsersRegisterLog:
    _date: datetime
    user_id: Column[Integer] | int
    username: Column[String] | str
    rank: str
    active: Column[Boolean] | bool

    def add_log_register(self) -> None:
        with open ("log_register.log", "a") as register_log:
            register_log.write(
                f"Registration:: {str(self._date)}; {self.user_id}; {self.username}; {self.rank}\n"
            )

    def add_log_activity(self) -> None:
        with open ("log_activity.log", "a") as register_log:
            if self.active:
                register_log.write(
                    f"User {self.user_id=}::{self.username} is now disabled.\n"
                )
            else:
                register_log.write(
                    f"User {self.user_id=}::{self.username} is now active.\n"
                )


@dataclass(frozen=True)
class StudentsStatisticsLog:
    _date: datetime
    user_id: Column[Integer] | int
    username: Column[String] | str
    school_class: Column[String] | str
    subject: str

    def add_statistics_log(self) -> None:
        with open("log_students_statistics.log", "a") as students_statistics_log:
            students_statistics_log.write(
                f"{str(self._date)}:: Statistics for {self.user_id}|{self.username} added with {self.school_class} class and {self.subject} subject.\n"
            )


@dataclass(frozen=True)
class EmailSenderLog:
    _date: datetime
    user_id: Column[Integer] | int
    username: Column[String] | str
    rank: str
    register: bool = False
    restore: bool = False

    def add_log_send_email(self):
        with open("log_email_sender.log", "a") as email_sender_log:
            if self.register:
                email_sender_log.write(
                    f"{str(self._date)}:: Registration information has sent to {self.user_id}|{self.username} ({self.rank})\n"
                )
            elif self.restore:
                email_sender_log.write(
                    f"{str(self._date)}:: Restore password has requested for {self.user_id}|{self.username}\n"
                )

