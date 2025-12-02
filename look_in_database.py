from sys import path

path.insert(0, "/home/nikita/PycharmProjects/diagnostics/diagnostics")
path.insert(0, "C:/Users/zelentsovna/PycharmProjects/site/diagnostics")

from diagnostics.modules.databases import Mathematics, MathematicsDB, Users, UsersDB

db = MathematicsDB
table = Mathematics

math = db()

for q in math.session.query(table).all():
    print(q)