import os
import shutil

from pprint import pprint
from pathlib import Path

TERMINAL_WIDTH = 80


def print_(obj, title=False, section=False):
    if isinstance(obj, dict):
        pprint(obj)
    elif title:
        print("*".center(TERMINAL_WIDTH, "*"))
        print(obj.center(TERMINAL_WIDTH))
        print("*".center(TERMINAL_WIDTH, "*"))
    elif section:
        print("-".center(TERMINAL_WIDTH, "-"))
        print(obj)
        print("-".center(TERMINAL_WIDTH, "-"))
    else:
        print(obj)


def reset_dir(dname):
    dirpath = Path(dname)
    if dirpath.exists():
        shutil.rmtree(dirpath)
    os.makedirs(dname)
