# This Python file uses the following encoding: cp1251
import sys
import os
from string import ascii_uppercase
import platform

try:
    fname = sys.argv[1]
except:
    msg = """
    Usage: run from contest directory (same level as conf, problems)
    run: python3 parse_statement.py <file.tex>
    where file.tex is contest statement
    file.tex located at /_statement and has "/item/emph" before each task
    """
    print(msg)

dir_sep = '/'
if platform.system == 'Windows':
    dir_sep = '\\'

try:
    s = open(f"_statement{dir_sep}" + fname, encoding="cp1251").read()
    tasks = s.split("\item\emph")[1:]
    tasks = ["\item\emph" + prob_text for prob_text in tasks]
    tasks[-1] = tasks[-1][:tasks[-1].rfind('\end{enum')]
except Exception as error:
    print("Something got wrong, below are details:")
    print(error)

all_letters = list(ascii_uppercase) + ['Z' + let for let in ascii_uppercase]
subfolders = sorted([ f.path for f in os.scandir("problems") if f.is_dir() ])

for k in range(min(len(all_letters), len(subfolders))):
    with open(subfolders[k] + f"{dir_sep}statement.tex", 'w', encoding="cp1251") as f:
        f.write(tasks[k])
        print(f"Task statement for {all_letters[k]} is in the folder {subfolders[k]}")