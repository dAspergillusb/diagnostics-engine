from sys import path

path.insert(0, "/home/nikita/PycharmProjects/diagnostics/diagnostics")

from diagnostics.modules.databases import Mathematics, MathematicsDB

math = MathematicsDB()

for q in math.session.query(Mathematics).all():
    print(q)