from diagnostics.modules.databases.UsersDB import UsersDB
from diagnostics.modules.databases.AlgebraDB import AlgebraDB
from diagnostics.modules.databases.BiologyDB import BiologyDB
from diagnostics.modules.databases.ChemistryDB import ChemistryDB
from diagnostics.modules.databases.GeographyDB import GeographyDB
from diagnostics.modules.databases.GeometryDB import GeometryDB
from diagnostics.modules.databases.HistoryDB import HistoryDB
from diagnostics.modules.databases.InformaticsDB import InformaticsDB
from diagnostics.modules.databases.MathematicsDB import MathematicsDB
from diagnostics.modules.databases.PhysicsDB import PhysicsDB
from diagnostics.modules.databases.RussianDB import RussianDB
from diagnostics.modules.databases.SocialScienceDB import SocialScienceDB
from diagnostics.modules.databases.LiteratureDB import LiteratureDB

def create_databases():
    try:
        UsersDB()
        AlgebraDB()
        BiologyDB()
        ChemistryDB()
        #EnglishDB()
        GeographyDB()
        GeometryDB()
        HistoryDB()
        InformaticsDB()
        MathematicsDB()
        PhysicsDB()
        RussianDB()
        SocialScienceDB()
        LiteratureDB()
    except:
        return False
    return True


if __name__ == '__main__':
    create_databases()