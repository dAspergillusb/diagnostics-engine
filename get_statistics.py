from sys import path

path.insert(0, "C:\\Users\\zelentsovna\\PycharmProjects\\site\\diagnostics")

from diagnostics.modules.databases import TeacherStatistics, TeacherStatisticsDB

teacher_statistics = TeacherStatisticsDB()

print(teacher_statistics)

