from os import mkdir
from modules.config import SUBJECTS


for subject in SUBJECTS:
    mkdir(f"static/images/{subject}")